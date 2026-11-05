"""URLhaus (abuse.ch): ¿la liga ya está reportada? Requiere llave gratuita en URLHAUS_KEY; sin llave → None."""
import os

import httpx


def reportada(liga: str, red: bool = True, timeout: float = 6.0) -> dict | None:
    llave = os.environ.get("URLHAUS_KEY")
    if not red or not llave:
        return None
    try:
        r = httpx.post("https://urlhaus-api.abuse.ch/v1/url/", data={"url": liga},
                       headers={"Auth-Key": llave}, timeout=timeout)
        d = r.json()
        if d.get("query_status") == "ok":
            return {"reportada": True, "estado": d.get("url_status"), "amenaza": d.get("threat"), "fecha": d.get("date_added")}
        if d.get("query_status") == "no_results":
            return {"reportada": False}
    except Exception:
        return None
    return None
