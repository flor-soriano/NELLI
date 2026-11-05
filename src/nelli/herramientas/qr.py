"""Lee códigos QR de una imagen (pyzbar + Pillow si están instalados). Sin ellos → None (no revisado)."""


def leer_qr(ruta_imagen: str) -> list[str] | None:
    try:
        from PIL import Image
        from pyzbar.pyzbar import decode
    except Exception:
        return None
    try:
        return [d.data.decode("utf-8", "replace") for d in decode(Image.open(ruta_imagen))]
    except Exception:
        return None
