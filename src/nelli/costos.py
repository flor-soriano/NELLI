"""Registro de costos por llamada (costos.jsonl) y tope por proyecto. Nada de contenido de usuarios aquí."""
import json
import os
import datetime as dt
from pathlib import Path

from . import RAIZ

ARCHIVO = Path(os.environ.get("NELLI_COSTOS", RAIZ / "costos.jsonl"))
TOPE_USD = float(os.environ.get("NELLI_TOPE_USD", "100"))

# USD por millón de tokens: (entrada, entrada en caché, salida). Fuente: dev.meta.ai/docs, capturado 26-oct-2026.
PRECIOS = {
    "muse-spark-1.3": (1.25, 0.15, 4.25),
    "muse-wonder-1.0": (4.00, 0.20, 20.00),
}
PRECIO_VOZ_POR_HORA = 0.18
PRECIO_POR_IMAGEN = 0.01


class TopeCostos(RuntimeError):
    pass


def total_usd() -> float:
    if not ARCHIVO.exists():
        return 0.0
    total = 0.0
    for linea in ARCHIVO.read_text(encoding="utf-8").splitlines():
        if linea.strip():
            total += float(json.loads(linea).get("usd", 0))
    return round(total, 6)


def verificar_tope(estimado: float = 0.0) -> None:
    gastado = total_usd()
    if gastado + estimado > TOPE_USD:
        raise TopeCostos(f"Tope de USD {TOPE_USD} alcanzado (gastado {gastado:.4f}). Revisa el gasto antes de seguir.")


def costo_chat(modelo: str, uso: dict) -> float:
    entrada, cache, salida = PRECIOS.get(modelo, PRECIOS["muse-spark-1.3"])
    prompt = int(uso.get("prompt_tokens", 0))
    en_cache = int((uso.get("prompt_tokens_details") or {}).get("cached_tokens", 0))
    completion = int(uso.get("completion_tokens", 0))
    return round(((prompt - en_cache) * entrada + en_cache * cache + completion * salida) / 1_000_000, 6)


def registrar(modelo: str, usd: float, segundos: float, uso: dict | None = None, nota: str = "") -> None:
    fila = {
        "ts": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "modelo": modelo,
        "usd": round(usd, 6),
        "segundos": round(segundos, 2),
        "uso": uso or {},
        "nota": nota,
    }
    with ARCHIVO.open("a", encoding="utf-8") as f:
        f.write(json.dumps(fila, ensure_ascii=False) + "\n")
