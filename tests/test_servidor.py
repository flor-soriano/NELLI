"""Servidor HTTP: la API devuelve la tarjeta del motor. Sin red externa ni IA."""
import json
import urllib.request

import pytest

from nelli.servidor import manejar_verificar, ruta_estatica


def test_verificar_sin_llave_usa_reglas():
    codigo, t = manejar_verificar(json.dumps(
        {"texto": "BANCO REAL: tu cuenta será bloqueada hoy. Valida tus datos en bancoreal-info.com/validar",
         "canal": "sms", "sin_ia": True}).encode("utf-8"))
    assert codigo == 200
    assert t["nivel"] == "fraude_confirmado"
    assert len(t["puntos"]) == 5
    assert "_trazas" not in t


def test_verificar_rechaza_vacio_y_json_roto():
    assert manejar_verificar(b'{"texto": "  "}')[0] == 400
    assert manejar_verificar(b"no es json")[0] == 400


def test_estaticos_del_front_sin_salir_de_su_carpeta():
    assert ruta_estatica("/web/nelli.css").name == "nelli.css"
    assert ruta_estatica("/web/tarjeta.js").name == "tarjeta.js"
    assert ruta_estatica("/feed/index.html").name == "index.html"
    assert ruta_estatica("/web/../src/nelli/servidor.py") is None
    assert ruta_estatica("/web/%2e%2e/.env.example") is None
    assert ruta_estatica("/web/..%5c.env.example") is None
    assert ruta_estatica("/web/no-existe.css") is None
    assert ruta_estatica("/src/nelli/servidor.py") is None

def _multipart(campos: dict, archivo: tuple | None) -> tuple[bytes, str]:
    frontera = "----prueba-nelli"
    partes = []
    for k, v in campos.items():
        partes.append(f"--{frontera}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode())
    if archivo:
        nombre, datos = archivo
        partes.append(f"--{frontera}\r\nContent-Disposition: form-data; name=\"imagen\"; filename=\"{nombre}\"\r\nContent-Type: image/png\r\n\r\n".encode() + datos + b"\r\n")
    partes.append(f"--{frontera}--\r\n".encode())
    return b"".join(partes), f"multipart/form-data; boundary={frontera}"


def test_verificar_multipart_acepta_captura_sin_ia(monkeypatch):
    monkeypatch.setattr("nelli.servidor.hay_llave", lambda: False)
    cuerpo, tipo = _multipart({"canal": "sms"}, ("captura.png", b"\x89PNG\r\n\x1a\n"))
    codigo, t = manejar_verificar(cuerpo, tipo)
    assert codigo == 200
    assert t["nivel"] == "no_pude_revisar"


def test_verificar_multipart_rechaza_vacio(monkeypatch):
    monkeypatch.setattr("nelli.servidor.hay_llave", lambda: False)
    cuerpo, tipo = _multipart({"canal": "web"}, None)
    assert manejar_verificar(cuerpo, tipo)[0] == 400


def test_verificar_multipart_rechaza_formato_y_gigante(monkeypatch):
    monkeypatch.setattr("nelli.servidor.hay_llave", lambda: False)
    cuerpo, tipo = _multipart({"canal": "web"}, ("mal.exe", b"MZ"))
    assert manejar_verificar(cuerpo, tipo)[0] == 400
    assert manejar_verificar(b"x" * 21, tipo)[0] in (400, 413)  # sin frontera: 400
    from nelli.servidor import MAX_CUERPO
    assert manejar_verificar(b"x" * (MAX_CUERPO + 1), "application/json")[0] == 413

