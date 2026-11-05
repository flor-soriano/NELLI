"""Pruebas de leer.py sin red ni llave: Spark se sustituye por una IA falsa.

Contrato que se protege:
- el mensaje entra como DATO entre delimitadores y lo fijo (developer) va primero;
- la IA nunca da «fraude_confirmado» (se baja a «muy_probablemente»);
- una negativa, un JSON roto o una respuesta sin choices NO revientan ni
  tapan lo que las reglas sí pueden decidir sobre el texto.
"""
import json

from nelli import leer
from nelli.nelli import Entrada, verificar

LECTURA_OK = {
    "legible": True, "texto_visto": "", "dice_ser": "un banco",
    "pide": ["datos_bancarios"], "presion": "fuerte", "ligas": [],
    "texto_para_ia": False, "tipo_probable": "banco_phishing",
    "nivel_sugerido": "muy_probablemente_fraude",
    "explicacion": "Pide datos con prisa.",
}


class MuseFalso:
    """Imita a muse.Muse.chat: devuelve (datos, uso, usd) y guarda los mensajes."""

    def __init__(self, contenido=None, mensaje_extra=None, datos=None):
        self.contenido = contenido
        self.mensaje_extra = mensaje_extra or {}
        self.datos = datos
        self.mensajes = None

    def chat(self, mensajes, esquema=None, esfuerzo="low", nota="leer", **kw):
        self.mensajes = mensajes
        if self.datos is not None:
            return self.datos, {"prompt_tokens": 10}, 0.001
        msg = {"content": self.contenido, **self.mensaje_extra}
        return {"choices": [{"message": msg}]}, {"prompt_tokens": 10}, 0.001


def leer_con(contenido=None, **kw):
    return leer.leer(MuseFalso(contenido=contenido, **kw), texto="hola", canal="sms")


def test_mensaje_entra_como_dato_y_developer_primero():
    falso = MuseFalso(contenido=json.dumps(LECTURA_OK))
    leer.leer(falso, texto="BANCO: valida tus datos hoy", canal="sms")
    assert falso.mensajes[0]["role"] == "developer"
    assert "LEER y EXTRAER" in falso.mensajes[0]["content"]
    texto_user = falso.mensajes[1]["content"][0]["text"]
    assert "CANAL POR EL QUE LLEGÓ: sms" in texto_user
    assert "<<<MENSAJE>>>\nBANCO: valida tus datos hoy\n<<<FIN_MENSAJE>>>" in texto_user


def test_lectura_ok_conserva_uso_y_costo():
    out = leer_con(json.dumps(LECTURA_OK))
    assert out["nivel_sugerido"] == "muy_probablemente_fraude"
    assert out["pide"] == ["datos_bancarios"] and out["_usd"] == 0.001


def test_ia_nunca_da_confirmado_desde_leer():
    out = leer_con(json.dumps({**LECTURA_OK, "nivel_sugerido": "fraude_confirmado"}))
    assert out["nivel_sugerido"] == "muy_probablemente_fraude"


def test_negativa_del_modelo_es_no_pude_sin_reventar():
    out = leer_con(None, mensaje_extra={"refusal": "no puedo"})
    assert out["legible"] is False and out["nivel_sugerido"] == "no_pude_revisar"


def test_json_invalido_no_revienta():
    out = leer_con("esto no es json {")
    assert out["nivel_sugerido"] == "no_pude_revisar" and out.get("_error")


def test_respuesta_sin_choices_no_revienta():
    out = leer.leer(MuseFalso(datos={"error": {"message": "fallo"}}), texto="hola", canal="sms")
    assert out["nivel_sugerido"] == "no_pude_revisar" and out.get("_error")


def test_campos_fuera_de_enum_se_ajustan():
    mala = {**LECTURA_OK, "pide": ["inventado", "dinero"], "presion": "altisima",
            "tipo_probable": "???", "ligas": "no-es-lista"}
    out = leer_con(json.dumps(mala))
    assert out["pide"] == ["dinero"] and out["presion"] == "ninguna"
    assert out["tipo_probable"] in ("otro", "ninguno") and out["ligas"] == []


def test_lectura_ilegible_no_tapa_las_reglas_si_hay_texto():
    falso = MuseFalso(contenido=json.dumps({**LECTURA_OK, "legible": False, "nivel_sugerido": "no_pude_revisar"}))
    t = verificar(
        Entrada(texto="BANCO REAL: tu cuenta será bloqueada hoy. Valida tus datos en bancoreal-info.com/validar", canal="sms"),
        con_ia=True, red=False, muse=falso,
    )
    assert t["nivel"] == "fraude_confirmado"  # deciden las reglas, no el «no pude» de la IA
