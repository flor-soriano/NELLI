"""Motor de reglas. Las reglas deciden el nivel; la IA solo puede subirlo. «Fraude confirmado» solo por regla con prueba dura."""
import json
import re
from functools import lru_cache

from . import NIVELES, PAQUETE_MX, integridad, mayor
from .defensas import limpiar_texto_ia, normalizar, texto_para_ia as _frag_ia
from .herramientas import check_url, lista_oficial, rdap, urlhaus


@lru_cache(maxsize=1)
def cargar() -> dict:
    integridad.verificar()
    ruta = PAQUETE_MX / "reglas-v2.json"
    return json.loads((ruta if ruta.exists() else PAQUETE_MX / "reglas-v1.json").read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def cargar_nunca() -> dict:
    ruta = PAQUETE_MX / "nunca-v2.json"
    return json.loads((ruta if ruta.exists() else PAQUETE_MX / "nunca-v1.json").read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def cargar_tipos() -> dict:
    ruta = PAQUETE_MX / "tipos-v2.json"
    d = json.loads((ruta if ruta.exists() else PAQUETE_MX / "tipos-v1.json").read_text(encoding="utf-8"))
    return {t["id"]: t for t in d["tipos"]}


def version() -> str:
    r, n = cargar(), cargar_nunca()
    return f"reglas {r['version']} ({r['fecha']}) · nunca {n['version']} ({n['fecha']})"


def senales_texto(texto: str) -> dict:
    t = normalizar(texto)
    senales = {}
    for nombre, patron in cargar()["patrones"].items():
        m = re.search(patron, t)
        if m:
            senales[nombre] = m.group(0)
    frag = _frag_ia(texto)
    if frag:
        senales["texto_para_ia"] = frag
    return senales


def senales_ligas(ligas: list[str], red: bool = True, origenes: dict | None = None) -> list[dict]:
    salida = []
    for liga in ligas:
        info = check_url.seguir(liga, red=red)
        h0, hf = info["host"], info["host_destino"]
        b0 = lista_oficial.buscar(h0)
        bf = lista_oficial.buscar(hf) if hf != h0 else b0
        oficial = bf["oficial"] or b0["oficial"]
        # Si el destino final es un dominio oficial, la liga no «imita» a nadie:
        # un acortador oficial (wa.link) no puede confirmar fraude por imitación.
        imita = None if oficial else (bf["imita"] or b0["imita"])
        edad = None
        if red and not oficial and not info["bloqueada_privada"] and hf:
            edad = rdap.edad_dominio(bf["registrable"], red=red)
        salida.append({
            **{k: info[k] for k in ("liga", "destino", "host", "host_destino", "cadena", "acortador", "https", "saltos",
                                    "error", "bloqueada_privada", "revisada_en_red")},
            "oficial": oficial, "imita": imita, "motivo": bf["motivo"] or b0["motivo"],
            "punycode": b0["punycode"] or bf["punycode"], "registrable": bf["registrable"],
            "reportada_propia": lista_oficial.reportada(hf) or lista_oficial.reportada(h0),
            "urlhaus": urlhaus.reportada(info["destino"], red=red), "edad": edad,
            "origen": (origenes or {}).get(liga, "texto"),
        })
    return salida


def senales_de_ligas(filas: list[dict]) -> dict:
    r, s = cargar(), {}
    for f in filas:
        if f["imita"]:
            s["dominio_imita"] = f["motivo"]
        if f["reportada_propia"] or (f["urlhaus"] or {}).get("reportada"):
            s["liga_reportada"] = f["host_destino"]
        if f["acortador"]:
            s["liga_acortada"] = f["host"]
        if f["punycode"]:
            s["punycode"] = f["host"]
        if f["edad"]:
            if f["edad"]["edad_dias"] < r["edad_nueva_dias"]:
                s["dominio_nuevo"] = f"{f['registrable']}: {f['edad']['edad_dias']} días"
            elif f["edad"]["edad_dias"] < r["edad_joven_dias"]:
                s["dominio_joven"] = f"{f['registrable']}: {f['edad']['edad_dias']} días"
        if not f["oficial"]:
            s["liga_no_oficial"] = f["host_destino"]
            if not f["imita"]:
                s["liga_desconocida"] = f["host_destino"]
            if f["revisada_en_red"] and not f["https"]:
                s["liga_sin_https"] = f["destino"]
    return s


def nunca_aplica(senales: dict, canal: str, texto: str = "") -> list[dict]:
    t = normalizar(texto) if texto else ""
    hits = []
    for fila in cargar_nunca()["filas"]:
        d = fila["detecta"]
        if d["senal"] not in senales:
            continue
        marcas = fila.get("marcas") or []
        if marcas and (not t or not any(m in t for m in marcas)):
            continue
        if "canal" in d and canal not in d["canal"]:
            continue
        if "y" in d:
            claves = ["liga_no_oficial" if x == "liga" else x for x in d["y"]]
            if not any(k in senales for k in claves):
                continue
        hits.append(fila)
    return hits


def decidir(senales: dict, lectura: dict | None, canal: str = "desconocido", ligas_info: list | None = None, texto: str = "") -> dict:
    r = cargar()
    razones, confirmado = [], []
    liga_solo_ia = False
    for f in ligas_info or []:
        solo_ia = f.get("origen") == "ia"
        if f["imita"]:
            inst, doms = f["imita"]["institucion"], ", ".join(f["imita"]["dominios"])
            if f["imita"].get("verificado") and not solo_ia:
                confirmado.append(f"La liga {f['host_destino']} imita a {inst} y no es su dominio oficial ({doms})")
            elif solo_ia:
                liga_solo_ia = True
                razones.append(f"La liga {f['host_destino']} imita a {inst} ({doms}), pero solo la leyó la IA de la captura: sube la alerta, no confirma")
            else:
                razones.append(f"La liga {f['host_destino']} imita a {inst} ({doms}); la fila aún no está verificada en la lista oficial, por eso no se confirma")
        if f["reportada_propia"]:
            if solo_ia:
                liga_solo_ia = True
                razones.append(f"La liga {f['host_destino']} ya está reportada, pero solo la leyó la IA de la captura: no confirma")
            else:
                confirmado.append(f"La liga {f['host_destino']} ya está reportada ({f['reportada_propia'].get('fuente', 'lista propia')})")
        if (f["urlhaus"] or {}).get("reportada"):
            if solo_ia:
                liga_solo_ia = True
                razones.append(f"URLhaus ya tiene reportada la liga {f['host_destino']}, pero solo la leyó la IA de la captura: no confirma")
            else:
                confirmado.append(f"URLhaus ya tiene reportada la liga {f['host_destino']}")
    nunca = nunca_aplica(senales, canal, texto)
    for n in nunca:
        if n.get("verificado"):
            confirmado.append(n["nunca"])
        else:
            razones.append(f"{n['institucion']}: {n['nunca']} (fuente pendiente de verificar: no se confirma)")
            senales.setdefault("nunca_sin_verificar", n["id"])

    fuertes = [s for s in r["fuertes"] if s in senales]
    debiles = [s for s in r["debiles"] if s in senales]
    contexto = set(r.get("contexto", []))
    pares = [p for p in r["pares_que_suben_a_muy_probable"] if all(x in senales for x in p)]
    if confirmado:
        nivel = "fraude_confirmado"
        razones = confirmado + razones
    elif ("texto_para_ia" in senales or "prompt_guard" in senales or len(fuertes) >= 2 or pares
          or "nunca_sin_verificar" in senales or "dominio_imita" in senales or liga_solo_ia):
        nivel = "muy_probablemente_fraude"
    elif fuertes or [d for d in debiles if d not in contexto]:
        nivel = "posible_fraude"
    else:
        nivel = "sin_senales_claras"
    razones += [f"señal fuerte · {s}: «{senales[s]}»" for s in fuertes]
    razones += [f"señal · {s}: «{senales[s]}»" for s in debiles]
    nivel_reglas, quien, nivel_ia = nivel, "reglas", None

    if lectura:
        nivel_ia = lectura.get("nivel_sugerido")
        if nivel_ia == "fraude_confirmado":  # imposible por esquema; por si acaso
            nivel_ia = "muy_probablemente_fraude"
        if lectura.get("texto_para_ia"):
            nivel_ia = mayor(nivel_ia, "muy_probablemente_fraude")
            razones.append("la IA vio texto dirigido a una IA dentro del mensaje")
        pide = set(lectura.get("pide") or [])
        if pide & {"dinero", "datos_bancarios", "contrasena_o_nip", "codigo_verificacion"} and lectura.get("presion") == "fuerte":
            nivel_ia = mayor(nivel_ia, "muy_probablemente_fraude")
        if nivel_ia in NIVELES and NIVELES.index(nivel_ia) > NIVELES.index(nivel_reglas):
            nivel, quien = nivel_ia, "ia (subió el nivel)"
            razones.append(f"la IA sugirió «{nivel_ia}»: {limpiar_texto_ia(lectura.get('explicacion', ''), 300)}")
    return {"nivel": nivel, "nivel_reglas": nivel_reglas, "nivel_ia": nivel_ia, "quien": quien,
            "razones": razones, "fuertes": fuertes, "debiles": debiles, "nunca": [n["id"] for n in nunca]}


def tipo_probable(senales: dict, lectura: dict | None, ligas_info: list | None = None) -> str:
    r = cargar()
    if lectura and lectura.get("tipo_probable") not in (None, "otro", "ninguno"):
        return lectura["tipo_probable"]
    for s in r["orden_tipo"]:
        if s in senales:
            return r["tipo_por_senal"][s]
    for f in ligas_info or []:
        if f["imita"]:
            sector = f["imita"].get("sector")
            return {"banco": "banco_phishing", "meta": "aviso_falso_meta", "paqueteria": "paqueteria",
                    "gobierno": "otro", "servicios": "servicios_cfe", "fintech": "banco_phishing", "comercio": "compra_venta"}.get(sector, "otro")
    return "otro" if senales else "ninguno"
