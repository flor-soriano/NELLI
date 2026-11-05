"""Lista oficial de dominios (paquete MX) y detección de imitaciones. Sin red."""
import json
import re
from functools import lru_cache

from .. import PAQUETE_MX

SUFIJOS_DOBLES = {
    "com.mx", "gob.mx", "org.mx", "edu.mx", "net.mx", "com.co", "gov.co", "edu.co", "org.co", "com.pe", "gob.pe",
    "org.pe", "com.ar", "gob.ar", "gov.ar", "com.br", "gov.br", "org.br", "co.uk", "com.gt", "com.sv", "com.hn",
    "com.ni", "com.do", "com.ec", "gob.ec", "com.ve", "gob.ve", "com.bo", "gob.bo", "com.py", "gov.py", "com.uy",
    "gub.uy", "gob.cl", "com.pa", "gob.pa", "com.cr", "go.cr",
}


@lru_cache(maxsize=1)
def cargar() -> dict:
    ruta = PAQUETE_MX / "dominios-v2.json"
    return json.loads((ruta if ruta.exists() else PAQUETE_MX / "dominios-v1.json").read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def cargar_reportadas() -> dict:
    ruta = PAQUETE_MX / "ligas-reportadas-v2.json"
    return json.loads((ruta if ruta.exists() else PAQUETE_MX / "ligas-reportadas-v1.json").read_text(encoding="utf-8"))


def version() -> str:
    d = cargar()
    return f"lista oficial {d['version']} ({d['fecha']})"


def dominio_registrable(host: str) -> str:
    host = host.lower().strip(".")
    partes = host.split(".")
    if len(partes) >= 3 and ".".join(partes[-2:]) in SUFIJOS_DOBLES:
        return ".".join(partes[-3:])
    return ".".join(partes[-2:]) if len(partes) >= 2 else host


def es_punycode(host: str) -> bool:
    return any(p.startswith("xn--") for p in host.lower().split("."))


def _distancia(a: str, b: str) -> int:
    if abs(len(a) - len(b)) > 2:
        return 3
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        fila = [i]
        for j, cb in enumerate(b, 1):
            fila.append(min(prev[j] + 1, fila[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = fila
    return prev[-1]


def buscar(host: str) -> dict:
    """{'oficial': fila|None, 'imita': fila|None, 'motivo': str, 'registrable': str, 'punycode': bool}"""
    host = (host or "").lower().strip().strip(".")
    reg = dominio_registrable(host)
    salida = {"oficial": None, "imita": None, "motivo": "", "registrable": reg, "punycode": es_punycode(host)}
    filas = cargar()["filas"]
    for fila in filas:
        for d in fila["dominios"]:
            if host == d or reg == d or host.endswith("." + d):
                if d in ("gob.mx",):  # dominio paraguas: cuenta como oficial del gobierno, no de una institución concreta
                    salida.update(oficial={"institucion": "Gobierno de México (gob.mx)", "dominios": [d], "verificado": fila.get("verificado", False)}, motivo=f"{host} está bajo {d}")
                else:
                    salida.update(oficial=fila, motivo=f"{host} es dominio oficial de {fila['institucion']}")
                return salida
    plano = re.sub(r"[^a-z0-9]", "", host)
    sld = reg.split(".")[0]
    # Palabras genéricas que vienen de subdominios (link.spinbyoxxo, blog.nu,
    # ayuda.izzi): nunca son marca. Sin esto, wa.link «imitaba» a Spin by OXXO
    # y disparaba Fraude confirmado con una liga oficial de WhatsApp.
    genericas = {"link", "blog", "ayuda", "help", "mail", "group", "citas", "data",
                 "www", "app", "support", "banco", "ftp2", "micrs", "dgtc", "ovica"}
    for fila in filas:
        for marca in fila.get("marca", []):
            m = re.sub(r"[^a-z0-9]", "", marca)
            if len(m) >= 4 and m not in genericas and m in plano:
                salida.update(imita=fila, motivo=f"{host} usa la marca «{marca}» pero no es {', '.join(fila['dominios'])}")
                return salida
        for d in fila["dominios"]:
            if d in ("gob.mx",):
                continue
            sld_of = d.split(".")[0]
            if len(sld_of) >= 5 and sld != sld_of and _distancia(sld, sld_of) <= 1:
                salida.update(imita=fila, motivo=f"{host} se parece a {d} (una letra de diferencia)")
                return salida
    return salida


def reportada(host: str) -> dict | None:
    reg = dominio_registrable((host or "").lower())
    for fila in cargar_reportadas()["filas"]:
        if fila["dominio"] == reg or fila["dominio"] == host:
            return fila
    return None
