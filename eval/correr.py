"""Evaluación: los dos errores (fraudes escapados · legítimos marcados) con intervalo de Wilson 95 %, por rival.
Uso: .venv/bin/python eval/correr.py [casos.jsonl] [--sin-ia] [--sin-red]
Rivales: reglas solas (--sin-ia) · Nelli completo (reglas + Spark). Spark solo y Scamio se corren con sus propios scripts (día 4).
"""
import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from dotenv import load_dotenv  # noqa: E402
from nelli import RAIZ  # noqa: E402
from nelli.nelli import Entrada, verificar  # noqa: E402

load_dotenv(RAIZ / ".env")
ROJO = {"fraude_confirmado", "muy_probablemente_fraude"}


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float, float]:
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    den = 1 + z * z / n
    centro = (p + z * z / (2 * n)) / den
    ancho = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (p, max(0.0, centro - ancho), min(1.0, centro + ancho))


def fmt(k, n):
    p, lo, hi = wilson(k, n)
    return f"{k}/{n} = {p:.1%} (IC95 {lo:.1%}–{hi:.1%})"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("casos", nargs="?", default=str(RAIZ / "casos" / "demo.jsonl"))
    ap.add_argument("--sin-ia", action="store_true"); ap.add_argument("--sin-red", action="store_true")
    ap.add_argument("--salida", help="jsonl con una fila por caso")
    a = ap.parse_args()
    casos = [json.loads(l) for l in Path(a.casos).read_text(encoding="utf-8").splitlines() if l.strip()]
    filas, niveles = [], Counter()
    for c in casos:
        t = verificar(Entrada(texto=c["texto"], canal=c.get("canal", "desconocido")), con_ia=not a.sin_ia, red=not a.sin_red)
        filas.append({"id": c["id"], "verdad": c["verdad"], "dificil": c.get("dificil", False), "nivel": t["nivel"], "tipo": t.get("tipo"), "decidio": t.get("decidio")})
        niveles[t["nivel"]] += 1
    legit = [f for f in filas if f["verdad"] == "legitimo"]
    dificil = [f for f in legit if f["dificil"]]
    fraude = [f for f in filas if f["verdad"] == "fraude"]
    print(f"rival: {'reglas solas' if a.sin_ia else 'Nelli (reglas + Spark)'} · red: {'no' if a.sin_red else 'sí'} · casos: {len(filas)}")
    print("legítimos marcados rojo (falsas alarmas):       ", fmt(sum(f['nivel'] in ROJO for f in legit), len(legit)))
    print("  de ellos, difíciles marcados rojo:           ", fmt(sum(f['nivel'] in ROJO for f in dificil), len(dificil)))
    print("fraudes escapados (sin señales / no pude):     ", fmt(sum(f['nivel'] in ('sin_senales_claras', 'no_pude_revisar') for f in fraude), len(fraude)))
    print("«Fraude confirmado» sobre un legítimo (meta 0):", sum(f['nivel'] == 'fraude_confirmado' for f in legit))
    print("niveles:", dict(niveles))
    for f in filas:
        marca = "·" if (f["verdad"] == "fraude") == (f["nivel"] in ROJO | {"posible_fraude"}) else "✗"
        print(f" {marca} {f['id']:<14} {f['verdad']:<9} {'difícil' if f['dificil'] else '':<8} → {f['nivel']:<26} {f['tipo']}")
    if a.salida:
        Path(a.salida).write_text("\n".join(json.dumps(f, ensure_ascii=False) for f in filas) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
