"""La verdad no se cambia sin firma: SHA256SUMS del paquete, el prompt y el esquema.

`sellar` lo corre una persona tras revisar el diff; `verificar` corre al primer uso.
"""
import hashlib
from pathlib import Path

from . import RAIZ


class IntegridadRota(RuntimeError):
    pass


def _rutas(base: Path) -> list[Path]:
    rutas = sorted((base / "paquete-mx").glob("*.json"))
    rutas += [base / "skills" / "leer-v1.md", base / "src" / "nelli" / "esquema" / "leer-v1.json"]
    return rutas


def _sha(ruta: Path) -> str:
    # Los saltos de línea no son contenido: un clon de Windows (CRLF) sella igual.
    return hashlib.sha256(ruta.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def sellar(base: Path | None = None) -> Path:
    base = Path(base) if base else RAIZ
    destino = base / "paquete-mx" / "SHA256SUMS"
    lineas = [f"{_sha(r)}  {r.relative_to(base).as_posix()}" for r in _rutas(base)]
    destino.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    return destino


def verificar(base: Path | None = None) -> None:
    base = Path(base) if base else RAIZ
    sums = base / "paquete-mx" / "SHA256SUMS"
    if not sums.is_file():
        raise IntegridadRota("Falta paquete-mx/SHA256SUMS. Revisa el paquete y corre «nelli sellar».")
    esperados = {}
    for linea in sums.read_text(encoding="utf-8").splitlines():
        if not linea.strip():
            continue
        partes = linea.split(None, 1)
        if len(partes) != 2:
            raise IntegridadRota(f"SHA256SUMS con línea inválida: {linea[:40]}")
        esperados[partes[1].strip().lstrip("*")] = partes[0]
    for rel, esperado in esperados.items():
        ruta = base / rel
        if not ruta.is_file() or _sha(ruta) != esperado:
            raise IntegridadRota(f"El paquete cambió sin sellar: {rel}. Revisa el diff y corre «nelli sellar».")


def huella(base: Path | None = None) -> str:
    base = Path(base) if base else RAIZ
    sums = base / "paquete-mx" / "SHA256SUMS"
    if not sums.is_file():
        return "sin-sellar-"
    return _sha(sums)[:12]
