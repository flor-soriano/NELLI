"""Emulador local de Muse (nivel 0): misma forma que la API, siempre marcado como emulación, sin red ni llave."""
import os

from nelli import emulador, leer
from nelli.muse import Muse


def test_lectura_por_palabras_clave_va_marcada_y_nunca_confirma():
    l = emulador.lectura("BANCO REAL: tu cuenta será bloqueada HOY. Valida tu NIP en bancoreal-info.com/validar",
                         venia_de_captura=False, legible=True)
    assert l["explicacion"].startswith(emulador.MARCA)
    assert "contrasena_o_nip" in l["pide"] and "abrir_liga" in l["pide"]
    assert l["presion"] == "fuerte"
    assert l["ligas"] == ["bancoreal-info.com/validar"]
    assert l["tipo_probable"] == "banco_phishing" and l["dice_ser"] == "un banco"
    assert l["nivel_sugerido"] in leer.NIVELES_PERMITIDOS  # «fraude_confirmado» no existe aquí


def test_sin_texto_legible_dice_no_pude():
    l = emulador.lectura("", venia_de_captura=True, legible=False)
    assert l["legible"] is False and l["nivel_sugerido"] == "no_pude_revisar"
    assert l["explicacion"].startswith(emulador.MARCA)


def test_mensaje_tranquilo_sin_senales():
    l = emulador.lectura("Hola, nos vemos el sábado en la comida de la tía. Lleva el pastel.", venia_de_captura=False, legible=True)
    assert l["nivel_sugerido"] == "sin_senales_claras" and l["pide"] == ["nada"] and l["ligas"] == []


def test_chat_por_http_con_el_cliente_real(monkeypatch):
    srv = emulador.servir(0)  # puerto libre
    try:
        monkeypatch.setattr("nelli.costos.registrar", lambda *a, **k: None)
        m = Muse(llave="de-prueba", base=f"http://127.0.0.1:{srv.server_address[1]}/v1")
        lec = leer.leer(m, texto="Ganaste un premio, paga $350 de envío hoy en premios-mx.info/reclamar", canal="whatsapp")
        assert lec["explicacion"].startswith(emulador.MARCA)
        assert lec["tipo_probable"] == "premio_sorteo" and "dinero" in lec["pide"]
        assert lec["_usd"] == 0
    finally:
        srv.shutdown()


def test_activar_deja_huella_y_apunta_el_motor(monkeypatch):
    for k in ("NELLI_EMULADOR", "MUSE_BASE_URL", "MODEL_API_KEY"):
        monkeypatch.setenv(k, "")  # se restauran al terminar
    srv = emulador.activar(0)
    try:
        assert emulador.activo() and os.environ["MUSE_BASE_URL"].startswith("http://127.0.0.1:")
        assert Muse().cliente.base_url.host == "127.0.0.1"
    finally:
        srv.shutdown()
