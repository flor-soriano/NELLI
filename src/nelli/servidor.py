"""Servidor HTTP mínimo para el front: POST /api/verificar -> tarjeta JSON.

Sin dependencias nuevas (http.server). Sirve web/ y feed/ y la API del motor.
Sin MODEL_API_KEY trabaja con reglas solas; con llave usa Spark (la IA solo sube).
Uso: .venv/bin/python -m nelli.servidor [--puerto 8000]
"""
import argparse
import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from dotenv import load_dotenv

from . import RAIZ, __version__, defensas, emulador, integridad
from .nelli import Entrada, verificar

load_dotenv(RAIZ / ".env")
WEB, FEED = RAIZ / "web", RAIZ / "feed"
TIPOS = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
         ".json": "application/json; charset=utf-8", ".css": "text/css; charset=utf-8",
         ".svg": "image/svg+xml", ".png": "image/png", ".webp": "image/webp"}
# Topes de subida (CWE-400): una captura o una nota de voz nunca pesan esto.
MAX_CUERPO = 20 * 1024 * 1024
# IPs del proxy inverso de confianza (separadas por coma). Solo de ellas se cree X-Forwarded-For.
PROXIES_CONFIANZA = {p.strip() for p in os.environ.get("NELLI_PROXY_CONFIANZA", "").split(",") if p.strip()}
CSP = ("default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; "
       "img-src 'self' data: blob:; media-src 'self' blob:; connect-src 'self'; font-src 'self'; "
       "object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'")
EXT_IMAGEN = {".png", ".jpg", ".jpeg", ".webp"}
EXT_AUDIO = {".wav", ".mp3", ".ogg", ".opus", ".m4a", ".webm", ".flac", ".amr", ".aac", ".3gp", ".caf"}
SEMAFORO = threading.BoundedSemaphore(int(os.environ.get("NELLI_MAX_SIMULTANEAS", "4")))
TOPE = defensas.TopeOrigen(maximo=int(os.environ.get("NELLI_TOPE_HORA", "60")))


def hay_llave() -> bool:
    return bool(os.environ.get("MODEL_API_KEY", "").strip())


def ruta_estatica(p: str) -> Path | None:
    """/web/<archivo> y /feed/<archivo>: solo archivos del front con tipo conocido, nunca fuera de su carpeta."""
    for prefijo, base in (("/web/", WEB), ("/feed/", FEED)):
        if p.startswith(prefijo):
            ruta = (base / unquote(p[len(prefijo):])).resolve()
            if base.resolve() in ruta.parents and ruta.suffix in TIPOS and ruta.is_file():
                return ruta
    return None


def _leer_multipart(cuerpo: bytes, tipo_contenido: str) -> tuple[dict, dict]:
    """multipart/form-data sin dependencias: ({campo: texto}, {campo: (nombre, bytes)})."""
    campos: dict[str, str] = {}
    archivos: dict[str, tuple[str, bytes]] = {}
    if "boundary=" not in tipo_contenido:
        return campos, archivos
    marca = tipo_contenido.split("boundary=", 1)[1].strip().strip('"')
    for bloque in cuerpo.split(("--" + marca).encode()):
        if b"\r\n\r\n" not in bloque:
            continue
        cab, _, datos = bloque.partition(b"\r\n\r\n")
        datos = datos[:-2] if datos.endswith(b"\r\n") else datos
        disp = ""
        for linea in cab.decode("utf-8", "replace").split("\r\n"):
            if linea.lower().startswith("content-disposition:"):
                disp = linea
        if 'name="' not in disp:
            continue
        nombre = disp.split('name="', 1)[1].split('"', 1)[0]
        if 'filename="' in disp:
            archivo = disp.split('filename="', 1)[1].split('"', 1)[0]
            if archivo:
                archivos[nombre] = (archivo, datos)
        elif nombre:
            campos[nombre] = datos.decode("utf-8", "replace")
    return campos, archivos


def manejar_verificar(cuerpo: bytes, tipo_contenido: str = "", origen: str = "anonimo",
                      tope: defensas.TopeOrigen | None = None) -> tuple[int, dict]:
    if len(cuerpo) > MAX_CUERPO:
        return 413, {"error": "El archivo es demasiado grande"}
    if tipo_contenido.startswith("multipart/form-data"):
        return _verificar_multipart(cuerpo, tipo_contenido, origen=origen, tope=tope)
    try:
        datos = json.loads(cuerpo or b"{}")
    except (json.JSONDecodeError, ValueError):
        return 400, {"error": "JSON inválido"}
    texto = datos.get("texto") or ""
    if not isinstance(texto, str) or not texto.strip():
        return 400, {"error": "Falta el texto del mensaje"}
    if len(texto) > 50000:
        return 413, {"error": "El mensaje es demasiado largo"}
    canal = datos.get("canal") or "web"
    if canal not in ("whatsapp", "sms", "email", "messenger", "feed", "web", "desconocido"):
        canal = "desconocido"
    con_ia = hay_llave() and not datos.get("sin_ia", False)
    t = verificar(Entrada(texto=texto, canal=canal, origen=origen), con_ia=con_ia,
                  red=bool(datos.get("red", False)), tope=tope if tope is not None else TOPE)
    t.pop("_trazas", None)
    return 200, t


def _verificar_multipart(cuerpo: bytes, tipo_contenido: str, origen: str = "anonimo",
                         tope: defensas.TopeOrigen | None = None) -> tuple[int, dict]:
    """La pantalla manda la captura o la nota de voz como FormData (imagen|audio, canal)."""
    import tempfile

    campos, archivos = _leer_multipart(cuerpo, tipo_contenido)
    texto = campos.get("texto", "") or ""
    if len(texto) > 50000:
        return 413, {"error": "El mensaje es demasiado largo"}
    canal = campos.get("canal", "web")
    if canal not in ("whatsapp", "sms", "email", "messenger", "feed", "web", "desconocido"):
        canal = "desconocido"
    rutas: list[Path] = []
    try:
        entrada = Entrada(texto=texto, canal=canal, origen=origen)
        for campo in ("imagen", "audio"):
            if campo in archivos:
                nombre, datos = archivos[campo]
                sufijo = Path(nombre).suffix.lower()
                permitidas = EXT_IMAGEN if campo == "imagen" else EXT_AUDIO
                if sufijo not in permitidas:
                    return 400, {"error": "Formato de archivo no soportado"}
                with tempfile.NamedTemporaryFile(delete=False, suffix=sufijo, prefix="nelli-") as f:
                    f.write(datos)
                    rutas.append(Path(f.name))
                if campo == "imagen":
                    entrada.imagen = str(rutas[-1])
                else:
                    entrada.audio = str(rutas[-1])
                break
        if not entrada.imagen and not entrada.audio and not texto.strip():
            return 400, {"error": "Falta el texto del mensaje"}
        con_ia = hay_llave() and campos.get("sin_ia") not in ("1", "true", "True")
        t = verificar(entrada, con_ia=con_ia, red=True, tope=tope if tope is not None else TOPE)
        t.pop("_trazas", None)
        return 200, t
    finally:
        for r in rutas:
            r.unlink(missing_ok=True)


class Manejador(BaseHTTPRequestHandler):
    timeout = 30

    def log_message(self, *a):
        pass

    def _enviar(self, codigo, cuerpo: bytes, tipo="application/json; charset=utf-8"):
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(cuerpo)))
        # Cabeceras de seguridad (el proxy puede sumar las suyas): nada embebido en otros sitios,
        # nada cargado de fuera y sin adivinar tipos. El front lleva estilos y scripts en línea.
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Security-Policy", CSP)
        self.end_headers()
        self.wfile.write(cuerpo)

    def _origen(self) -> str:
        """IP de quien pregunta. Detrás del proxy de confianza (NELLI_PROXY_CONFIANZA) se toma X-Forwarded-For,
        para que el tope por origen no cuente a todos los usuarios como uno solo."""
        ip = self.client_address[0]
        if ip in PROXIES_CONFIANZA:
            reenviada = (self.headers.get("X-Forwarded-For") or "").split(",")[0].strip()
            if reenviada:
                return reenviada
        return ip

    def _json(self, codigo, obj):
        self._enviar(codigo, json.dumps(obj, ensure_ascii=False).encode("utf-8"))

    def _archivo(self, ruta: Path):
        if not ruta.is_file():
            return self._json(404, {"error": "no está"})
        self._enviar(200, ruta.read_bytes(), TIPOS.get(ruta.suffix, "application/octet-stream"))

    def do_GET(self):
        p = urlparse(self.path).path
        if p in ("/", "/index.html"):
            return self._archivo(WEB / "index.html")
        if p in ("/manual", "/manual.html"):
            return self._archivo(WEB / "manual.html")
        if p in ("/blindar", "/blindar.html"):
            return self._archivo(WEB / "blindar.html")
        if p in ("/feed", "/feed/", "/feed/index.html"):
            return self._archivo(FEED / "index.html")
        if p == "/tarjeta.js":
            return self._archivo(WEB / "tarjeta.js")
        if p == "/insignia-blindar.png":
            return self._archivo(WEB / "insignia-blindar.png")
        if p == "/ejemplo-tarjeta.json":
            return self._archivo(WEB / "ejemplo-tarjeta.json")
        if p == "/api/salud":
            return self._json(200, {"ok": True, "version": __version__, "ia": hay_llave(), "paquete": integridad.huella(),
                                    "emulador": emulador.activo()})
        ruta = ruta_estatica(p)
        if ruta:
            return self._archivo(ruta)
        return self._json(404, {"error": "no está"})

    def do_POST(self):
        if urlparse(self.path).path != "/api/verificar":
            return self._json(404, {"error": "no está"})
        if not SEMAFORO.acquire(blocking=False):
            self.close_connection = True
            return self._json(503, {"error": "Nelli está ocupada; intenta en un minuto"})
        try:
            try:
                largo = int(self.headers.get("Content-Length") or 0)
            except ValueError:
                return self._json(400, {"error": "Content-Length inválido"})
            if largo < 0:  # un largo negativo haría que read(-1) leyera sin tope
                return self._json(400, {"error": "Content-Length inválido"})
            if largo > MAX_CUERPO:
                return self._json(413, {"error": "El archivo es demasiado grande"})
            codigo, obj = manejar_verificar(self.rfile.read(largo) if largo else b"{}",
                                            self.headers.get("Content-Type") or "",
                                            origen=self._origen())
            return self._json(codigo, obj)
        finally:
            SEMAFORO.release()


def main(argv=None):
    ap = argparse.ArgumentParser(prog="nelli-servidor")
    ap.add_argument("--puerto", type=int, default=int(os.environ.get("PORT", "8000")))
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--emulador", action="store_true", help="usa el emulador local de Muse aunque haya llave (pruebas)")
    ap.add_argument("--sin-emulador", action="store_true", help="sin llave, reglas solas: no levantar el emulador")
    a = ap.parse_args(argv)
    integridad.verificar()
    # Sin llave, Nelli completa se prueba con el emulador local (nelli.emulador). NO es Muse y la tarjeta lo dice.
    if a.emulador or (not hay_llave() and not a.sin_emulador):
        emulador.activar()
    srv = ThreadingHTTPServer((a.host, a.puerto), Manejador)
    modo = "EMULACIÓN LOCAL, no es Muse" if emulador.activo() else ("sí" if hay_llave() else "no, reglas solas")
    print(f"Nelli {__version__} en http://{a.host}:{a.puerto} (IA: {modo})")
    srv.serve_forever()


if __name__ == "__main__":
    main()
