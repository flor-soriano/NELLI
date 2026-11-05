"""Sigue redirecciones SIN cargar la página final, bloquea direcciones privadas (SSRF) y marca acortadores."""
import ipaddress
import re
import socket
from urllib.parse import urljoin, urlsplit

import httpx

ACORTADORES = {
    "bit.ly", "tinyurl.com", "cutt.ly", "t.co", "goo.gl", "is.gd", "rb.gy", "shorturl.at", "acortar.link", "n9.cl",
    "s.id", "rebrand.ly", "ow.ly", "buff.ly", "lnkd.in", "t.ly", "short.io", "tiny.cc", "v.gd", "qr.ae", "soo.gd",
}
TLDS_FRECUENTES = r"(com|mx|net|org|info|xyz|top|club|site|online|shop|store|live|app|io|co|me|ly|link|click|gl|ru|cn|cc|tk|ga|cf|ml|gq|biz|us|es|ar|pe|cl|br|do|gt|sv|hn|ni|pa|cr|ec|ve|bo|py|uy|edu|gob|gov|id|at|to|vip|rest|cam|icu|pw|ai|cfd|sbs|lol|one)"
_RE_LIGA = re.compile(
    r"(?:(?:https?|hxxps?)://[^\s<>\"'()\[\]]+)|(?:\b(?:[a-z0-9-]+\[?\.\]?)+" + TLDS_FRECUENTES + r"\b(?:/[^\s<>\"'()\[\]]*)?)",
    re.IGNORECASE,
)


def extraer_ligas(texto: str) -> list[str]:
    vistas, salida = set(), []
    for m in _RE_LIGA.finditer(texto or ""):
        liga = m.group(0).rstrip(".,;:!?")
        if not re.search(r"[a-z]", liga, re.I):
            continue
        n = normalizar(liga)
        if n not in vistas:
            vistas.add(n)
            salida.append(liga)
    return salida


def normalizar(liga: str) -> str:
    liga = liga.strip().replace("[.]", ".").replace("(.)", ".").replace("hxxp", "http")
    if not re.match(r"^[a-z][a-z0-9+.-]*://", liga, re.I):
        liga = "http://" + liga
    return liga


def host_de(liga: str) -> str:
    return (urlsplit(normalizar(liga)).hostname or "").lower()


def resolver(host: str) -> list[str] | None:
    """Direcciones IP del host, sin repetir; None si no resuelve. Un host que ya es IP se devuelve tal cual."""
    try:
        return [str(ipaddress.ip_address(host))]
    except ValueError:
        pass
    # IP escrita como un solo número («2130706433», «0x7f000001»): algunos sistemas la resuelven y otros no;
    # aquí se interpreta siempre, para que la revisión de red privada no dependa del sistema.
    if re.fullmatch(r"0x[0-9a-f]+|\d+", host, re.I):
        try:
            return [str(ipaddress.ip_address(int(host, 16 if host.lower().startswith("0x") else 10)))]
        except ValueError:
            return None
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return None
    return list(dict.fromkeys(i[4][0] for i in infos))


def _alguna_privada(ips: list[str]) -> bool:
    return any(not ipaddress.ip_address(ip).is_global for ip in ips)


def es_privada(host: str) -> bool | None:
    """True si el host apunta a red privada/loopback/link-local/reservada; None si no se pudo resolver."""
    if host in ("localhost",) or host.endswith(".local") or host.endswith(".internal"):
        return True
    ips = resolver(host)
    if ips is None:
        return None
    return _alguna_privada(ips)


def _con_ip(liga: str, ip: str) -> str:
    """La misma liga pero apuntando a la IP ya revisada (sin usuario:clave en la URL)."""
    p = urlsplit(liga)
    puerto = f":{p.port}" if p.port else ""
    return p._replace(netloc=(f"[{ip}]" if ":" in ip else ip) + puerto).geturl()


def seguir(liga: str, red: bool = True, max_saltos: int = 5, timeout: float = 5.0) -> dict:
    actual = normalizar(liga)
    cadena = [actual]
    salida = {"liga": liga, "cadena": cadena, "destino": actual, "host": host_de(actual), "host_destino": host_de(actual),
              "acortador": host_de(actual) in ACORTADORES, "https": actual.lower().startswith("https://"),
              "saltos": 0, "bloqueada_privada": False, "error": None, "revisada_en_red": False}
    if not red:
        return salida
    try:
        with httpx.Client(follow_redirects=False, timeout=timeout,
                          headers={"User-Agent": "Nelli/0.1 (verificador; no carga paginas)"}) as c:
            for _ in range(max_saltos):
                host = host_de(actual)
                local = host in ("localhost",) or host.endswith(".local") or host.endswith(".internal")
                ips = None if local else resolver(host)
                if local or (ips and _alguna_privada(ips)):
                    salida.update(bloqueada_privada=True, error="destino en red privada; no se sigue")
                    break
                if not ips:
                    salida["error"] = f"no resuelve: {host}"
                    break
                # Se conecta a la IP que ya se revisó (con Host y SNI del nombre): así una segunda resolución
                # del DNS no puede cambiar el destino después de la comprobación (DNS rebinding).
                destino = _con_ip(actual, ips[0])
                extra = {"headers": {"Host": host}, "extensions": {"sni_hostname": host}}
                r = c.head(destino, **extra)
                if r.status_code in (405, 403, 400):
                    with c.stream("GET", destino, **extra) as g:  # solo encabezados; el cuerpo nunca se lee
                        r = g
                salida["revisada_en_red"] = True
                if r.status_code in (301, 302, 303, 307, 308) and r.headers.get("location"):
                    actual = urljoin(actual, r.headers["location"])
                    cadena.append(actual)
                    continue
                salida["estado_http"] = r.status_code
                break
    except httpx.HTTPError as e:
        salida["error"] = f"{type(e).__name__}"
    salida.update(destino=actual, host_destino=host_de(actual), saltos=len(cadena) - 1,
                  https=actual.lower().startswith("https://"))
    return salida
