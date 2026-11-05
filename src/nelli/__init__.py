"""Nelli · verifica antes de creer, comprar o contestar. Las reglas deciden; la IA explica."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
PAQUETE_MX = RAIZ / "paquete-mx"
__version__ = "0.2.0-dia3"

NIVELES = ["sin_senales_claras", "posible_fraude", "muy_probablemente_fraude", "fraude_confirmado"]
NO_PUDE = "no_pude_revisar"
ETIQUETAS = {
    "fraude_confirmado": "Fraude confirmado",
    "muy_probablemente_fraude": "Muy probablemente es fraude",
    "posible_fraude": "Posible fraude",
    "sin_senales_claras": "No vemos señales claras",
    NO_PUDE: "No pude revisarlo",
}


def mayor(*niveles: str) -> str:
    """El nivel más alto entre varios; ignora None y 'no_pude_revisar'."""
    validos = [n for n in niveles if n in NIVELES]
    if not validos:
        return NO_PUDE
    return max(validos, key=NIVELES.index)
