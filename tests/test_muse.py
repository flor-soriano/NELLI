"""Voz contra transporte falso: la forma multipart que la API sí acepta (`docs/nota-voz-2026-10-30.md`, 30-oct).

Sin red ni llave real: `request` (JSON con audioEncoding WAV) + `audio` (el WAV),
y la respuesta trae el texto en `transcript`.
"""
import json
import wave

import httpx

from nelli import costos
from nelli.muse import Muse


def _wav(ruta, segundos: float = 1.0) -> None:
    with wave.open(str(ruta), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(16000)
        w.writeframes(b"\x00\x00" * int(16000 * segundos))


def test_transcribir_manda_request_y_audio_y_lee_transcript(tmp_path, monkeypatch):
    monkeypatch.setattr(costos, "ARCHIVO", tmp_path / "costos.jsonl")
    visto = {}

    def responder(request: httpx.Request) -> httpx.Response:
        visto["cuerpo"] = request.read()
        visto["tipo"] = request.headers.get("content-type", "")
        return httpx.Response(200, json={"transcript": "Hola, soy tu hijo, cambié de número.",
                                         "audioDurationMs": 1000, "turns": []})

    cliente = Muse(llave="de-prueba")
    cliente.cliente = httpx.Client(base_url="https://api.meta.ai/v1",
                                   transport=httpx.MockTransport(responder))
    ruta = tmp_path / "nota.wav"
    _wav(ruta)

    texto, datos = cliente.transcribir(ruta)

    assert texto == "Hola, soy tu hijo, cambié de número."
    assert datos["audioDurationMs"] == 1000
    cuerpo = visto["cuerpo"].decode("utf-8", "replace")
    assert "multipart/form-data" in visto["tipo"]
    assert 'name="request"' in cuerpo and 'name="audio"' in cuerpo
    assert '"audioEncoding": "WAV"' in cuerpo and '"model": "muse-voice-transcribe-1.0"' in cuerpo
    fila = json.loads((tmp_path / "costos.jsonl").read_text(encoding="utf-8").strip())
    assert fila["modelo"] == "muse-voice-transcribe-1.0" and fila["nota"] == "transcribir"


def test_generar_imagen_guarda_b64(tmp_path, monkeypatch):
    import base64
    monkeypatch.setattr(costos, "ARCHIVO", tmp_path / "costos.jsonl")
    png = base64.b64encode(b"\x89PNG-falso").decode()

    def responder(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/images/generations"
        assert json.loads(request.content)["model"] == "muse-image-1.0"
        return httpx.Response(200, json={"data": [{"b64_json": png}]})

    cliente = Muse(llave="de-prueba")
    cliente.cliente = httpx.Client(base_url="https://api.meta.ai/v1",
                                   transport=httpx.MockTransport(responder))
    destino = cliente.generar_imagen("un escudo", tmp_path / "insignia.png")
    assert destino.read_bytes() == b"\x89PNG-falso"
    fila = json.loads((tmp_path / "costos.jsonl").read_text(encoding="utf-8").strip())
    assert fila["modelo"] == "muse-image-1.0" and fila["usd"] == costos.PRECIO_POR_IMAGEN
