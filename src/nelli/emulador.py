"""Emulador local de la Meta Model API (Muse) para probar Nelli completa sin llave.

NO es Muse y nunca se presenta como Muse. Imita solo la FORMA de sus respuestas para que
el motor funcione de punta a punta cuando no hay `MODEL_API_KEY`:
  - POST /v1/chat/completions  → lee la captura con RapidOCR (OCR local) y llena la lectura
                                 con palabras clave sobre el mismo esquema `leer-v1`; la
                                 explicación empieza con «[EMULACIÓN LOCAL, no es Muse]».
  - POST /v1/asr/transcribe    → transcribe el WAV con faster-whisper (local, sin red).
  - POST /v1/images/generations → 501: el emulador no genera imágenes.
Solo escucha en 127.0.0.1. Nada sale de la máquina. Costo: cero. Las reglas del motor
siguen mandando: el emulador solo sugiere, y «Fraude confirmado» lo dan las reglas.

Se activa solo desde `nelli.servidor` cuando no hay llave (o con `--emulador`), y deja la
huella `NELLI_EMULADOR=1` para que la tarjeta y la página lo declaren.
Dependencias opcionales: `pip install -e ".[emulador]"` (rapidocr-onnxruntime, faster-whisper).
"""
import base64
import io
import json
import logging
import os
import re
import sys
import threading
import time
import unicodedata
import wave
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

log = logging.getLogger("nelli.emulador")
MARCA = "[EMULACIÓN LOCAL, no es Muse] "
PUERTO = int(os.environ.get("NELLI_EMULADOR_PUERTO", "8777"))
MODELO_VOZ = os.environ.get("NELLI_EMULADOR_WHISPER", "small")

_ocr = None
_whisper = None
_lock = threading.Lock()


# ---------- OCR local ----------
def ocr(imagen_bytes: bytes) -> str:
    """Texto de una captura con RapidOCR. Si no está instalado, devuelve '' y lo anota."""
    global _ocr
    try:
        with _lock:
            if _ocr is None:
                from rapidocr_onnxruntime import RapidOCR
                _ocr = RapidOCR()
        import numpy as np
        from PIL import Image, ImageOps
    except ImportError as e:
        log.warning("OCR no disponible (%s): instala los extras [emulador]", e)
        return ""
    im = Image.open(io.BytesIO(imagen_bytes))
    im = ImageOps.exif_transpose(im).convert("RGB")
    if max(im.size) < 1200:  # las capturas chicas se leen mejor agrandadas
        k = 1200 / max(im.size)
        im = im.resize((round(im.width * k), round(im.height * k)))
    res, _ = _ocr(np.array(im))
    if not res:
        return ""
    return "\n".join(t for _, t, c in res if float(c) >= 0.5 and t.strip())


# ---------- transcripción local ----------
def transcribir(wav_bytes: bytes) -> tuple[str, float]:
    """Texto y duración de un WAV con faster-whisper. Lanza ImportError si no está instalado."""
    global _whisper
    with _lock:
        if _whisper is None:
            from faster_whisper import WhisperModel
            _whisper = WhisperModel(MODELO_VOZ, device="cpu", compute_type="int8")
    import tempfile
    with tempfile.NamedTemporaryFile(prefix="nelli-emu-", suffix=".wav", delete=False) as f:
        f.write(wav_bytes)
        ruta = Path(f.name)
    try:
        try:
            with wave.open(str(ruta), "rb") as w:
                dur = w.getnframes() / float(w.getframerate() or 1)
        except Exception:
            dur = 0.0
        segmentos, _ = _whisper.transcribe(str(ruta), language="es", beam_size=3, vad_filter=True)
        return " ".join(s.text.strip() for s in segmentos).strip(), dur
    finally:
        try:
            ruta.unlink()
        except OSError:
            pass


# ---------- lectura por palabras clave (lo que Spark haría con el prompt leer-v1) ----------
def _plano(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))


LIGA_RE = re.compile(r"(?:https?://[^\s<>«»\"']+|(?:www\.)?[a-z0-9][a-z0-9-]{1,62}(?:\.[a-z0-9-]{2,63})+(?:/[^\s<>«»\"']*)?)", re.I)
TIPOS = [
    ("banco_phishing", ["banco", "bancomer", "bbva", "banorte", "santander", "citibanamex", "banamex", "hsbc", "scotiabank", "cuenta sera bloqueada", "cuenta bloqueada", "tarjeta", "clabe", "valida tus datos", "valide sus datos", "banca movil", "banca en linea"]),
    ("paqueteria", ["paquete", "envio", "paqueteria", "dhl", "fedex", "estafeta", "correos de mexico", "entrega", "guia"]),
    ("sat_impuestos", ["sat ", "sat:", "impuesto", "devolucion", "factura", "fiscal", "rfc"]),
    ("servicios_cfe", ["cfe", "luz", "recibo", "corte del servicio", "telmex", "agua", "gas"]),
    ("premio_sorteo", ["premio", "sorteo", "ganaste", "ganador", "rifa", "reclama"]),
    ("prestamo_facil", ["prestamo", "credito", "sin buro", "aprobado", "inmediato", "sin aval"]),
    ("inversion_cripto", ["inversion", "cripto", "bitcoin", "rendimiento", "ganancias", "trading", "usdt"]),
    ("familiar_en_apuro", ["mama", "papa", "hijo", "hija", "cambie de numero", "nuevo numero", "deposita", "me urge", "emergencia", "hospital"]),
    ("extorsion", ["secuestr", "te vamos", "cartel", "sabemos donde", "amenaza", "pagas o"]),
    ("codigo_whatsapp", ["codigo de verificacion", "codigo de whatsapp", "me llego un codigo", "pasame el codigo", "codigo de 6"]),
    ("empleo_falso", ["empleo", "trabajo desde casa", "vacante", "gana hasta", "sin experiencia", "sueldo"]),
    ("aviso_falso_meta", ["meta", "facebook", "instagram", "tu pagina sera", "infringe", "derechos de autor", "verificacion de cuenta"]),
    ("compra_venta", ["oferta", "remate", "liquidacion", "venta", "iphone", "pago por adelantado", "transferencia"]),
    ("multa_falsa", ["multa", "infraccion", "transito", "fotomulta", "placas", "sspc", "recargo"]),
    ("soporte_falso", ["soporte", "tecnico", "microsoft", "virus", "tu equipo", "anydesk", "teamviewer"]),
]
PIDE = [
    ("datos_bancarios", ["numero de tarjeta", "cvv", "tarjeta", "clabe", "cuenta bancaria", "datos bancarios", "valida tus datos", "valide sus datos", "actualiza tus datos"]),
    ("contrasena_o_nip", ["nip", "contrasena", "password", "clave de acceso", "token"]),
    ("codigo_verificacion", ["codigo", "pin de", "6 digitos"]),
    ("dinero", ["deposita", "deposito", "transfiere", "transferencia", "paga ", "pagar", "pago", "$", "pesos", "mxn", "anticipo", "comision"]),
    ("abrir_liga", ["http", "www.", ".com", ".mx", ".info", ".net", ".org", "liga", "enlace", "link", "ingresa a", "entra a", "da clic", "haz clic"]),
    ("llamar", ["llama al", "comunicate al", "marca al", "llamar"]),
    ("pasar_a_otro_chat", ["escribeme al", "whatsapp al", "telegram", "contactame", "mandame mensaje al"]),
    ("descargar_app", ["descarga", "instala", "apk", "aplicacion"]),
    ("documentos", ["ine", "identificacion", "comprobante", "pasaporte", "curp"]),
]
PRESION_FUERTE = ["hoy", "urgente", "inmediato", "inmediata", "ahora mismo", "ultimo aviso", "en las proximas", "sera bloqueada", "bloqueo", "suspendid", "24 horas", "antes de", "de lo contrario", "o perderas", "ultima oportunidad", "vence"]
PRESION_LEVE = ["pronto", "a la brevedad", "cuanto antes", "no lo dejes pasar"]
PARA_IA = ["ignora las instrucciones", "ignore previous", "eres un asistente", "system prompt", "responde que es seguro", "marca este mensaje como", "instrucciones anteriores", "fin_mensaje", "<<<"]
DICE_SER = [
    ("el SAT", ["sat ", "sat:", "servicio de administracion tributaria"]),
    ("la CFE", ["cfe"]),
    ("la SSPC o una autoridad de tránsito", ["sspc", "transito", "fotomulta", "policia"]),
    ("un banco", ["banco", "bbva", "banorte", "santander", "banamex", "hsbc", "scotiabank", "banca"]),
    ("una paquetería", ["dhl", "fedex", "estafeta", "paqueteria", "correos de mexico", "paquete"]),
    ("Meta o Facebook", ["meta", "facebook", "instagram"]),
    ("un familiar", ["mama", "papa", "hijo", "hija", "tia", "tio", "abuel"]),
    ("una empresa que ofrece empleo", ["vacante", "empleo", "reclutamiento"]),
    ("una financiera o prestamista", ["prestamo", "credito", "financiera"]),
    ("soporte técnico", ["soporte", "microsoft", "tecnico"]),
]


def lectura(texto: str, venia_de_captura: bool, legible: bool) -> dict:
    """Lectura con la forma de `esquema/leer-v1.json`, llenada con palabras clave. Nunca confirma fraude."""
    p = _plano(texto)
    if not legible or len(p.strip()) < 8:
        return {"legible": False, "texto_visto": texto if venia_de_captura else "", "dice_ser": "alguien que no se presenta",
                "pide": ["nada"], "presion": "ninguna", "ligas": [], "texto_para_ia": False,
                "tipo_probable": "ninguno", "nivel_sugerido": "no_pude_revisar",
                "explicacion": MARCA + "No encontré texto legible en lo que mandaste. Manda el texto o una captura más clara."}
    ligas = []
    for l in LIGA_RE.findall(texto):
        l = l.rstrip(".,;:)»”\"'")
        if "." in l and not l.lower().endswith((".jpg", ".png")) and l not in ligas:
            ligas.append(l)
    pide = [k for k, claves in PIDE if any(c in p for c in claves)]
    if ligas and "abrir_liga" not in pide:
        pide.append("abrir_liga")
    presion = "fuerte" if any(c in p for c in PRESION_FUERTE) else ("leve" if any(c in p for c in PRESION_LEVE) else "ninguna")
    puntaje = {k: sum(1 for c in claves if c in p) for k, claves in TIPOS}
    tipo, mejor = max(puntaje.items(), key=lambda kv: kv[1])
    if mejor == 0:
        tipo = "otro" if pide else "ninguno"
    dice = next((n for n, claves in DICE_SER if any(c in p for c in claves)), "alguien que no se presenta")
    para_ia = any(c in p for c in PARA_IA)
    senales = len(pide) + (1 if presion == "fuerte" else 0) + (1 if ligas else 0) + (1 if tipo not in ("ninguno", "otro") else 0)
    nivel = "muy_probablemente_fraude" if senales >= 3 else ("posible_fraude" if senales >= 1 else "sin_senales_claras")
    frases = []
    if tipo not in ("ninguno", "otro"):
        frases.append(f"Se parece a un caso de {tipo.replace('_', ' ')}.")
    if pide:
        frases.append("Te pide " + ", ".join(x.replace("_", " ") for x in pide) + (" con prisa." if presion == "fuerte" else "."))
    if not frases:
        frases.append("No veo que pida dinero, datos ni que meta prisa.")
    return {"legible": True, "texto_visto": texto if venia_de_captura else "", "dice_ser": dice,
            "pide": pide or ["nada"], "presion": presion, "ligas": ligas[:10], "texto_para_ia": para_ia,
            "tipo_probable": tipo, "nivel_sugerido": nivel, "explicacion": MARCA + " ".join(frases)}


# ---------- servidor HTTP con la forma de la API ----------
def _multipart(cuerpo: bytes, tipo: str) -> dict:
    """{campo: (nombre, bytes)} de un multipart/form-data simple."""
    partes = {}
    if "boundary=" not in tipo:
        return partes
    marca = tipo.split("boundary=", 1)[1].strip().strip('"')
    for bloque in cuerpo.split(("--" + marca).encode()):
        if b"\r\n\r\n" not in bloque:
            continue
        cab, _, datos = bloque.partition(b"\r\n\r\n")
        datos = datos[:-2] if datos.endswith(b"\r\n") else datos
        m = re.search(rb'name="([^"]+)"', cab)
        if not m:
            continue
        n = re.search(rb'filename="([^"]*)"', cab)
        partes[m.group(1).decode()] = ((n.group(1).decode() if n else ""), datos)
    return partes


class Manejador(BaseHTTPRequestHandler):
    server_version = "NelliEmuladorLocal/1"

    def log_message(self, *a):  # silencio: lo útil va al logger
        pass

    def _json(self, codigo: int, obj: dict) -> None:
        cuerpo = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def do_POST(self):
        try:
            n = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            n = -1
        if n < 0 or n > 32 * 1024 * 1024:
            return self._json(400, {"error": {"message": "Content-Length inválido o demasiado grande"}})
        cuerpo = self.rfile.read(n)
        ruta = self.path.split("?")[0].rstrip("/")
        t0 = time.monotonic()
        try:
            if ruta.endswith("/chat/completions"):
                return self._chat(json.loads(cuerpo.decode("utf-8")), t0)
            if ruta.endswith("/asr/transcribe"):
                return self._asr(cuerpo, t0)
            if ruta.endswith("/images/generations"):
                return self._json(501, {"error": {"message": "El emulador local no genera imágenes (eso es de Muse Image)."}})
            return self._json(404, {"error": {"message": f"ruta desconocida {ruta}"}})
        except Exception as e:  # nunca tirar el servidor
            log.warning("error en %s: %s: %s", ruta, type(e).__name__, e)
            return self._json(500, {"error": {"message": f"{type(e).__name__}: {e}"}})

    def _chat(self, peticion: dict, t0: float):
        texto, imagen = "", None
        for m in peticion.get("messages") or []:
            if m.get("role") != "user":
                continue
            cont = m.get("content")
            if isinstance(cont, str):
                texto = cont
            elif isinstance(cont, list):
                for c in cont:
                    if c.get("type") == "text":
                        texto = c.get("text") or ""
                    elif c.get("type") == "image_url":
                        url = (c.get("image_url") or {}).get("url") or ""
                        if url.startswith("data:") and "," in url:
                            imagen = base64.b64decode(url.split(",", 1)[1])
        m = re.search(r"<<<MENSAJE>>>\n?(.*?)\n?<<<FIN_MENSAJE>>>", texto, re.S)
        mensaje = (m.group(1) if m else texto).strip()
        if mensaje.startswith("(sin texto"):
            mensaje = ""
        visto, legible = "", True
        if imagen is not None:
            visto = ocr(imagen)
            legible = len(_plano(visto).strip()) >= 8
        if peticion.get("response_format"):
            lec = lectura(mensaje or visto, venia_de_captura=imagen is not None, legible=legible or bool(mensaje))
            if imagen is not None:
                lec["texto_visto"] = visto
            contenido = json.dumps(lec, ensure_ascii=False)
        else:
            contenido = MARCA + "ok"
        log.info("chat: texto=%d car · captura=%s · ocr=%d car · %.1fs", len(mensaje), "sí" if imagen is not None else "no", len(visto), time.monotonic() - t0)
        return self._json(200, {
            "id": "emulador-local", "object": "chat.completion", "created": int(time.time()),
            "model": "emulador-local (no es Muse)",
            "choices": [{"index": 0, "finish_reason": "stop", "message": {"role": "assistant", "content": contenido}}],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        })

    def _asr(self, cuerpo: bytes, t0: float):
        partes = _multipart(cuerpo, self.headers.get("Content-Type") or "")
        if "audio" not in partes:
            return self._json(400, {"error": {"message": "falta el campo audio"}})
        try:
            texto, dur = transcribir(partes["audio"][1])
        except ImportError as e:
            log.warning("transcripción no disponible (%s): instala los extras [emulador]", e)
            return self._json(501, {"error": {"message": "El emulador no tiene faster-whisper instalado (extras [emulador])."}})
        log.info("asr: %.1fs de audio → %d car · %.1fs", dur, len(texto), time.monotonic() - t0)
        return self._json(200, {"transcript": texto, "audioDurationMs": int(dur * 1000), "model": "emulador-local-whisper (no es Muse)"})


def servir(puerto: int = PUERTO) -> ThreadingHTTPServer:
    """Levanta el emulador en un hilo, solo en 127.0.0.1. Devuelve el servidor (con su puerto real)."""
    srv = ThreadingHTTPServer(("127.0.0.1", puerto), Manejador)
    threading.Thread(target=srv.serve_forever, daemon=True, name="nelli-emulador").start()
    log.info("emulador local de Muse en http://127.0.0.1:%d/v1 (no es Muse)", srv.server_address[1])
    return srv


def activo() -> bool:
    return os.environ.get("NELLI_EMULADOR") == "1"


def activar(puerto: int = PUERTO) -> ThreadingHTTPServer:
    """Levanta el emulador y apunta el motor a él. Deja NELLI_EMULADOR=1 para que la tarjeta lo declare."""
    srv = servir(puerto)
    os.environ["MODEL_API_KEY"] = "emulador-local-sin-llave"
    os.environ["MUSE_BASE_URL"] = f"http://127.0.0.1:{srv.server_address[1]}/v1"
    os.environ["NELLI_EMULADOR"] = "1"
    return srv


def main(argv=None):
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    puerto = int(argv[0]) if argv else PUERTO
    srv = servir(puerto)
    print(f"Emulador local de Muse en http://127.0.0.1:{srv.server_address[1]}/v1 · NO es Muse · Ctrl+C para salir", flush=True)
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        srv.shutdown()


if __name__ == "__main__":
    main(sys.argv[1:])
