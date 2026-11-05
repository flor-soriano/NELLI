"""Cliente mínimo de la Meta Model API (Muse). Standard siempre; nunca contributor.
Base y modelos: dev.meta.ai/docs, capturado 26-oct-2026. Compatible con Chat Completions.
"""
import base64
import json
import mimetypes
import os
import random
import time
import wave
from pathlib import Path

import httpx

from urllib.parse import urlsplit

from . import costos
from .herramientas import check_url

BASE = os.environ.get("MUSE_BASE_URL", "https://api.meta.ai/v1")
MODELO_SPARK = "muse-spark-1.3"
MODELO_VOZ = "muse-voice-transcribe-1.0"
MODELO_IMAGEN = "muse-image-1.0"
REINTENTABLES = {429, 500, 502, 503, 504}


class SinLlave(RuntimeError):
    pass


class Muse:
    def __init__(self, llave: str | None = None, base: str | None = None, timeout: float = 90.0):
        llave = llave or os.environ.get("MODEL_API_KEY")
        if not llave:
            raise SinLlave("Falta MODEL_API_KEY en .env (créala en dev.meta.ai; ver .env.example)")
        # La base se lee al crear el cliente (no al importar) para que el emulador local pueda apuntarla.
        base = base or os.environ.get("MUSE_BASE_URL", BASE)
        self.cliente = httpx.Client(base_url=base, headers={"Authorization": f"Bearer {llave}"}, timeout=timeout)

    def _post(self, ruta: str, intentos: int = 5, **kw) -> httpx.Response:
        for i in range(intentos):
            r = self.cliente.post(ruta, **kw)
            if r.status_code in REINTENTABLES and i < intentos - 1:
                espera = r.headers.get("Retry-After")
                # random solo reparte la espera entre reintentos; no es para nada criptográfico.
                segundos = float(espera) if espera and espera.replace(".", "", 1).isdigit() else min(2 ** i + random.random(), 30)  # nosec B311
                time.sleep(segundos)
                continue
            r.raise_for_status()
            return r
        raise RuntimeError("sin respuesta tras reintentos")

    def chat(self, mensajes: list, esquema: dict | None = None, modelo: str = MODELO_SPARK,
             esfuerzo: str = "low", herramientas: list | None = None, max_tokens: int = 1200, nota: str = "chat"):
        if "contributor" in modelo:
            raise ValueError("Nunca contributor en Nelli (Meta entrenaría con mensajes de usuarios)")
        costos.verificar_tope()
        cuerpo = {"model": modelo, "messages": mensajes, "max_tokens": max_tokens, "reasoning_effort": esfuerzo}
        if esquema:
            cuerpo["response_format"] = {
                "type": "json_schema",
                "json_schema": {"name": esquema["nombre"], "strict": True, "schema": esquema["schema"]},
            }
        if herramientas:
            cuerpo["tools"] = herramientas
        t0 = time.monotonic()
        datos = self._post("/chat/completions", json=cuerpo).json()
        segundos = time.monotonic() - t0
        uso = datos.get("usage", {}) or {}
        usd = costos.costo_chat(modelo, uso)
        # Se registra el modelo que contestó: con el emulador local queda «emulador-local…» a 0 USD, nunca como Muse.
        costos.registrar(datos.get("model") or modelo, usd, segundos, uso, nota=nota)
        return datos, uso, usd

    def transcribir(self, ruta_wav: str | Path, idioma: str = "es") -> tuple[str, dict]:
        """POST /v1/asr/transcribe con WAV mono 16 kHz.

        Forma probada con la API real (30-oct, `docs/nota-voz-2026-10-30.md`):
        multipart con `request` (JSON: model, language, audioEncoding "WAV") y
        `audio` (el WAV). La respuesta trae el texto en `transcript`.
        """
        costos.verificar_tope()
        ruta = Path(ruta_wav)
        duracion = _duracion_wav(ruta)
        peticion = json.dumps({"model": MODELO_VOZ, "language": idioma, "audioEncoding": "WAV"})
        t0 = time.monotonic()
        with ruta.open("rb") as f:
            r = self._post("/asr/transcribe",
                           files={"request": (None, peticion, "application/json"),
                                  "audio": (ruta.name, f, "audio/wav")})
        segundos = time.monotonic() - t0
        datos = r.json()
        duracion = duracion or (datos.get("audioDurationMs") or 0) / 1000.0
        # El emulador local contesta con su propio `model` (no es Muse) y no cuesta nada.
        modelo = datos.get("model") or MODELO_VOZ
        usd = (duracion / 3600.0) * costos.PRECIO_VOZ_POR_HORA if modelo == MODELO_VOZ else 0.0
        costos.registrar(modelo, usd, segundos, {"segundos_audio": round(duracion, 1)}, nota="transcribir")
        texto = datos.get("transcript") or datos.get("text") or ""
        return texto.strip(), datos


    def generar_imagen(self, prompt: str, destino: str | Path) -> Path:
        """POST /images/generations con muse-image-1.0; guarda PNG/JPG en destino.

        La respuesta (formato estándar de `images/generations`) trae `data[0].b64_json` o `data[0].url`.
        Costo fijo por imagen según costos.PRECIO_POR_IMAGEN.
        """
        costos.verificar_tope()
        t0 = time.monotonic()
        datos = self._post("/images/generations",
                           json={"model": MODELO_IMAGEN, "prompt": prompt}).json()
        segundos = time.monotonic() - t0
        costos.registrar(MODELO_IMAGEN, costos.PRECIO_POR_IMAGEN, segundos, {}, nota="generar_imagen")
        item = (datos.get("data") or [{}])[0]
        destino = Path(destino)
        destino.parent.mkdir(parents=True, exist_ok=True)
        if item.get("b64_json"):
            destino.write_bytes(base64.b64decode(item["b64_json"]))
        elif item.get("url"):
            partes = urlsplit(item["url"])
            if partes.scheme != "https" or check_url.es_privada(partes.hostname or "") is not False:
                raise RuntimeError("La URL de la imagen no es https pública; no se baja")
            destino.write_bytes(httpx.get(item["url"], timeout=60).content)
        else:
            raise RuntimeError("La API de imagen no devolvió b64_json ni url")
        return destino


def _duracion_wav(ruta: Path) -> float:
    try:
        with wave.open(str(ruta), "rb") as w:
            return w.getnframes() / float(w.getframerate() or 1)
    except Exception:
        return 0.0


def imagen_a_data_url(ruta: str | Path) -> str:
    ruta = Path(ruta)
    tipo = mimetypes.guess_type(ruta.name)[0] or "image/png"
    return f"data:{tipo};base64," + base64.b64encode(ruta.read_bytes()).decode()
