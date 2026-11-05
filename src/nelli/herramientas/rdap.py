"""Antigüedad del dominio por RDAP público (rdap.org hace el bootstrap). Sin llave. Si no hay dato → None."""
import datetime as dt

import httpx


def edad_dominio(dominio: str, red: bool = True, timeout: float = 6.0) -> dict | None:
    if not red or not dominio:
        return None
    try:
        r = httpx.get(f"https://rdap.org/domain/{dominio}", follow_redirects=True, timeout=timeout,
                      headers={"Accept": "application/rdap+json"})
        if r.status_code != 200:
            return None
        for ev in r.json().get("events", []):
            if ev.get("eventAction") == "registration" and ev.get("eventDate"):
                fecha = dt.datetime.fromisoformat(ev["eventDate"].replace("Z", "+00:00"))
                dias = (dt.datetime.now(dt.timezone.utc) - fecha).days
                return {"registrado": fecha.date().isoformat(), "edad_dias": dias}
    except Exception:
        return None
    return None
