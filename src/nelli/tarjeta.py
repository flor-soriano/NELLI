"""Arma la tarjeta: etiqueta, 5 puntos, un paso, botones y licencia. Plantillas escritas por personas; la IA solo llena huecos."""
import json
import os
from functools import lru_cache

from . import ETIQUETAS, NO_PUDE, PAQUETE_MX, __version__
from . import defensas
from . import reglas as motor
from .herramientas import lista_oficial

BOTONES = ["Reportar", "Bloquear", "Pregúntale a alguien de confianza", "Ya caí, ¿qué hago?"]
ROJOS = {"fraude_confirmado", "muy_probablemente_fraude"}
PIDE_TEXTO = {
    "nada": "no pide nada", "dinero": "dinero (depósito, transferencia o pago)", "datos_bancarios": "datos de tu tarjeta o cuenta",
    "contrasena_o_nip": "tu contraseña o NIP", "codigo_verificacion": "un código de verificación", "documentos": "documentos (INE, comprobantes)",
    "abrir_liga": "abrir una liga", "llamar": "llamar a un número", "pasar_a_otro_chat": "pasarte a otra app de mensajes", "descargar_app": "descargar una app", "otro": "otra cosa",
    "pide_datos_sensibles": "datos sensibles (NIP, código, tarjeta o validar datos)", "pide_dinero": "dinero (depósito, transferencia o pago)",
    "codigo_whatsapp": "tu código de WhatsApp", "otro_chat": "pasarte a otra app de mensajes",
}


@lru_cache(maxsize=1)
def plantillas() -> dict:
    ruta = PAQUETE_MX / "plantillas-v2.json"
    return json.loads((ruta if ruta.exists() else PAQUETE_MX / "plantillas-v1.json").read_text(encoding="utf-8"))


def desactivar(liga: str) -> str:
    return liga.replace("https://", "hxxps://").replace("http://", "hxxp://").replace(".", "[.]")


def _punto(n: int, titulo: str, texto: str, estado: str) -> dict:
    return {"n": n, "titulo": titulo, "texto": texto, "estado": estado}  # estado: ok | alerta | no_revisado


def armar(decision: dict, senales: dict, ligas_info: list, lectura: dict | None, entrada, tipo: str, no_pude: list[str]) -> dict:
    nivel = decision["nivel"]
    pl = plantillas()
    p = pl["tipos"].get(tipo) or pl["tipos"]["otro"]
    imitan = [f for f in ligas_info if f["imita"]]
    oficiales = [f for f in ligas_info if f["oficial"]]
    nunca = motor.nunca_aplica(senales, entrada.canal, (entrada.texto or "") + " " + ((lectura or {}).get("texto_visto") or ""))

    _dice_ia = (lectura or {}).get("dice_ser")
    dice = defensas.limpiar_texto_ia(_dice_ia, 80) if _dice_ia else (_dice_ser(senales) or "no se presenta (desconocido)")
    if imitan:
        p1 = _punto(1, "¿Quién está detrás?", f"Dice ser {dice}, pero la liga no es de {imitan[0]['imita']['institucion']}.", "alerta")
    elif oficiales:
        p1 = _punto(1, "¿Quién está detrás?", f"Dice ser {dice}; la liga sí es la oficial de {oficiales[0]['oficial']['institucion']}.", "ok")
    else:
        p1 = _punto(1, "¿Quién está detrás?", f"Dice ser {dice}. Llegó por {entrada.canal}; no pude confirmar quién lo mandó.", "no_revisado")

    pide = (lectura or {}).get("pide") or [k for k in ("pide_datos_sensibles", "pide_dinero", "codigo_whatsapp", "otro_chat") if k in senales] or ["nada"]
    pide_txt = ", ".join(dict.fromkeys(PIDE_TEXTO.get(x, x) for x in pide))
    prisa = " Con prisa." if ("presion" in senales or (lectura or {}).get("presion") == "fuerte") else ""
    p2 = _punto(2, "¿Qué te pide hacer?", f"Te pide: {pide_txt}.{prisa}", "alerta" if pide != ["nada"] else "ok")

    if nunca:
        n = nunca[0]
        p3 = _punto(3, "¿Se sostiene lo que dice?", n["nunca"] + ("" if n.get("verificado") else " (fuente oficial pendiente de anotar)."), "alerta")
    elif p["prueba"] and nivel != "sin_senales_claras":
        p3 = _punto(3, "¿Se sostiene lo que dice?", p["prueba"], "alerta")
    else:
        p3 = _punto(3, "¿Se sostiene lo que dice?", "No pude revisar: sin una fuente oficial a la mano para este caso.", "no_revisado")

    if not ligas_info:
        p4 = _punto(4, "¿A dónde te lleva la liga?", "No trae liga.", "ok")
    else:
        partes, estado = [], "ok"
        for f in ligas_info:
            s = desactivar(f["destino"])
            if f["acortador"]:
                s = f"{desactivar(f['liga'])} está acortada → lleva a {s}" if f["saltos"] else f"{desactivar(f['liga'])} está acortada (no pude ver el destino)"
            if f.get("origen") == "ia":
                s += " (liga leída de tu captura)"
            if f["imita"]:
                s += f". {f['motivo']}"; estado = "alerta"
            elif f["oficial"]:
                s += f" (dominio oficial de {f['oficial']['institucion']})"
            if f["edad"]:
                s += f"; dominio registrado hace {f['edad']['edad_dias']} días"
                if f["edad"]["edad_dias"] < motor.cargar()["edad_joven_dias"] and estado != "alerta":
                    estado = "alerta"
            if f["revisada_en_red"] and not f["https"] and not f["oficial"]:
                s += "; sin candado (https)"
            if f["bloqueada_privada"]:
                s += "; apunta a una red privada: no se sigue"
            if f["error"] and not f["revisada_en_red"]:
                s += "; no pude seguirla" + ("" if f["error"].startswith("destino") else f" ({f['error']})")
                estado = estado if estado == "alerta" else "no_revisado"
            partes.append(s)
        p4 = _punto(4, "¿A dónde te lleva la liga?", " · ".join(partes), estado)

    reportadas = [f for f in ligas_info if f["reportada_propia"] or (f["urlhaus"] or {}).get("reportada")]
    if reportadas:
        p5 = _punto(5, "¿Qué dicen los demás?", f"La liga {desactivar(reportadas[0]['host_destino'])} ya está reportada.", "alerta")
    elif any((f["urlhaus"] or {}).get("reportada") is False for f in ligas_info):
        p5 = _punto(5, "¿Qué dicen los demás?", "Sin reportes en URLhaus hoy (eso no la hace buena).", "ok")
    else:
        p5 = _punto(5, "¿Qué dicen los demás?", "No pude revisar: sin reportes a la mano en esta versión.", "no_revisado")

    paso = p["paso"] if nivel != "sin_senales_claras" else "Si te pide dinero o datos, confirma por otro lado antes de hacer nada."
    fuente = None
    if imitan:
        fuente = {"institucion": imitan[0]["imita"]["institucion"], "dominio_oficial": imitan[0]["imita"]["dominios"][0]}
    elif oficiales:
        fuente = {"institucion": oficiales[0]["oficial"]["institucion"], "dominio_oficial": oficiales[0]["oficial"]["dominios"][0]}
    elif nunca:
        fuente = {"institucion": nunca[0]["institucion"], "fuente": nunca[0]["fuente"]}

    etiqueta = ETIQUETAS[nivel]
    return {
        "version": __version__, "nivel": nivel, "etiqueta": etiqueta, "tipo": tipo,
        "tipo_nombre": motor.cargar_tipos().get(tipo, {}).get("nombre", tipo),
        "puntos": [p1, p2, p3, p4, p5], "paso": paso,
        "botones": BOTONES + (["Blindar mi cuenta en 7 minutos"] if nivel in ROJOS else []),
        "mensaje_confianza": f"Oye, me llegó este mensaje y Nelli lo marcó como «{etiqueta}». ¿Tú qué opinas? No abras la liga.",
        "ya_cai": p["ya_cai"], "fuente_verificada": fuente,
        "ligas_desactivadas": [desactivar(f["liga"]) for f in ligas_info],
        "decidio": decision["quien"], "razones": decision["razones"],
        "licencia": {
            "revisado_contra": [lista_oficial.version(), motor.version(), f"plantillas {pl['version']} ({pl['fecha']})"],
            # Nunca se presenta el emulador como Muse: si corre el emulador local, la tarjeta lo dice.
            "ia": ("emulación local (no es Muse; con llave entra Muse)" if os.environ.get("NELLI_EMULADOR") == "1"
                   else "muse-spark-1.3 (solo explica y puede subir)") if lectura else "sin IA: reglas solas",
            "no_pude_ver": no_pude, "canal": entrada.canal,
            "como_repetirlo": f"nelli verificar --canal {entrada.canal}{' --sin-ia' if not lectura else ''} \"<el mismo texto>\"",
        },
    }


def _dice_ser(senales: dict) -> str | None:
    for s, nombre in (("sat", "el SAT"), ("cfe", "la CFE o un servicio"), ("banco", "un banco"), ("paqueteria", "una paquetería"),
                      ("suplantacion_gobierno", "una dependencia de gobierno"), ("aviso_meta", "Meta o Facebook"),
                      ("familiar_apuro", "un familiar"), ("extorsion", "un grupo delictivo")):
        if s in senales:
            return nombre
    return None


def no_pude_revisar(motivo: str, entrada) -> dict:
    return {"version": __version__, "nivel": NO_PUDE, "etiqueta": ETIQUETAS[NO_PUDE], "tipo": "ninguno", "puntos": [],
            "paso": "Manda el texto del mensaje o una captura más clara. Si te pide dinero o datos, confirma por otro lado.",
            "botones": ["Pregúntale a alguien de confianza"], "razones": [motivo], "decidio": "sistema",
            "licencia": {"ia": "—", "no_pude_ver": [motivo], "canal": entrada.canal, "revisado_contra": []}}


def negativa(entrada) -> dict:
    from .defensas import NEGATIVA
    return {"version": __version__, "nivel": "negativa", "etiqueta": "No puedo ayudar con eso", "tipo": "ninguno", "puntos": [],
            "paso": NEGATIVA, "botones": [], "razones": ["la petición es redactar o disimular una estafa"], "decidio": "defensas",
            "licencia": {"ia": "—", "no_pude_ver": [], "canal": entrada.canal, "revisado_contra": ["negativa fija v1"]}}


def texto_plano(t: dict) -> str:
    lineas = [f"━━ {t['etiqueta'].upper()} ━━", f"Tipo: {t.get('tipo_nombre', t.get('tipo'))} · decidió: {t.get('decidio')}"]
    for p in t.get("puntos", []):
        marca = {"ok": "✓", "alerta": "!", "no_revisado": "?"}[p["estado"]]
        lineas.append(f" {p['n']} {marca} {p['titulo']} {p['texto']}")
    lineas.append(f"→ {t['paso']}")
    if t.get("botones"):
        lineas.append("[ " + " ] [ ".join(t["botones"]) + " ]")
    if t.get("razones"):
        lineas.append("Razones: " + " | ".join(t["razones"]))
    lic = t.get("licencia", {})
    lineas.append(f"Licencia: {'; '.join(lic.get('revisado_contra', []))} · IA: {lic.get('ia')}" + (f" · no pude ver: {', '.join(lic['no_pude_ver'])}" if lic.get("no_pude_ver") else ""))
    return "\n".join(lineas)
