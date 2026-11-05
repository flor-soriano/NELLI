"""Filtros de entrada: negativa fija, señal de inyección, Prompt Guard 2 (si está instalado) y tope por origen."""
import collections
import hashlib
import os
import re
import time
import unicodedata

NEGATIVA = "No puedo ayudar con eso. Nelli solo revisa mensajes que te llegaron; no redacta ni mejora mensajes."

_PATRONES_NEGATIVA = [
    r"que (mi |este |el |tu )?(mensaje|texto|correo|sms|anuncio) (no )?(parezca|suene|se vea) (menos )?(fraude|estafa|sospechoso|real|legitimo|oficial|del banco|de un banco|de verdad)",
    r"(ayuda(me)?|quiero|necesito|puedes|podrias|como hago) .{0,40}(mensaje|texto|correo|sms) .{0,20}(no parezca|parezca|suene|se vea|convenza|cuele)",
    r"(haz|has|hacer|hagas) que (mi |este |el )?(mensaje|texto|correo|sms) (no )?(parezca|suene|se vea) (menos )?(fraude|estafa|sospechoso|real|legitimo|del banco|de un banco|oficial)",
    r"mejora(r|me)? (mi|este|el) (mensaje|estafa|phishing|texto para)",
    r"redacta(me)? (un |el )?(mensaje|correo|sms|texto) (para|que) .*(deposit|transfier|pague|datos|contrasena|codigo|clabe|convenz)",
    r"(escribe|redacta|genera|crea)(me)? (un |una )?(estafa|phishing|fraude)",
    r"como (hago|hacer|puedo hacer) (una |un )?(estafa|fraude|phishing)",
    r"que (parezca|se vea) (del|de un|de el) (banco|sat|gobierno|imss|cfe)",
    r"convence(lo|la|los|las)? de que (me )?(deposite|pague|mande|transfiera)",
]
_PATRONES_IA = [
    r"ignora (todas )?(las |tus )?(instrucciones|reglas|indicaciones)",
    r"ignore (all )?(previous|prior|the above|your) (instructions|rules)",
    r"system prompt", r"eres un asistente", r"you are an? (assistant|ai|model)",
    r"clasifica(lo)? como (seguro|legitimo|no fraude|sin senales)", r"marca(lo)? como (seguro|legitimo|sin senales)",
    r"di que (es seguro|no es fraude|no hay senales)", r"nivel[_ ]sugerido", r"no vemos senales claras",
    r"\bassistant:", r"\bdeveloper:", r"<\|", r"\[inst\]",
    r"<<<|>>>",
]


def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFD", texto or "")
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", texto.lower()).strip()


def pide_mejorar_estafa(texto: str) -> bool:
    t = normalizar(texto)
    return any(re.search(p, t) for p in _PATRONES_NEGATIVA)


def texto_para_ia(texto: str) -> str | None:
    """Devuelve el fragmento que parece dirigido a una IA, o None."""
    t = normalizar(texto)
    for p in _PATRONES_IA:
        m = re.search(p, t)
        if m:
            return m.group(0)
    return None


_RE_CORREO = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_RE_CUENTA = re.compile(r"@[\w.]+")
_RE_TELEFONO = re.compile(r"(?:\+?52[\s.-]?)?(?:\(?\d{2,3}\)?[\s.-]?)?\d{3,4}[\s.-]\d{4}\b|\b\d{7,}\b")


def limpiar_texto_ia(s: str | None, maximo: int) -> str:
    """Sanea texto libre de la IA antes de la tarjeta: fuera ligas, teléfonos, correos y cuentas."""
    from .herramientas.check_url import _RE_LIGA

    limpio = _RE_CORREO.sub("[dato quitado]", s or "")
    limpio = _RE_LIGA.sub("[dato quitado]", limpio)
    limpio = _RE_CUENTA.sub("[dato quitado]", limpio)
    limpio = _RE_TELEFONO.sub("[dato quitado]", limpio)
    limpio = re.sub(r"\s+", " ", limpio).strip()
    if not limpio:
        return "desconocido"
    return limpio[:maximo].rstrip()


def prompt_guard(texto: str) -> dict | None:
    """Prompt Guard 2 (pesos abiertos, 86M) si NELLI_PROMPT_GUARD apunta a un modelo local; si no, None (= no revisado)."""
    ruta = os.environ.get("NELLI_PROMPT_GUARD")
    if not ruta:
        return None
    try:
        from transformers import pipeline  # import tardío: solo si existe el modelo
    except Exception:
        return None
    clasificador = _cargar_guard(ruta)
    salidas = clasificador(texto[:2000], truncation=True, max_length=512)
    mejor = max(salidas, key=lambda s: s["score"]) if isinstance(salidas, list) else salidas
    return {"etiqueta": mejor["label"], "puntaje": round(float(mejor["score"]), 3)}


_guard = None


def _cargar_guard(ruta):
    global _guard
    if _guard is None:
        from transformers import pipeline
        _guard = pipeline("text-classification", model=ruta)
    return _guard


_SAL_PROCESO: str | None = None


def _sal() -> str:
    """Sal del hash de orígenes. Si falta NELLI_SAL se genera una al azar por proceso: los hashes
    siguen sirviendo para el tope (viven en memoria) y nadie puede revertirlos con una sal conocida."""
    global _SAL_PROCESO
    sal = os.environ.get("NELLI_SAL", "").strip()
    if sal:
        return sal
    if _SAL_PROCESO is None:
        import secrets
        _SAL_PROCESO = secrets.token_hex(16)
    return _SAL_PROCESO


class TopeOrigen:
    """Tope de consultas por origen (hash del número o IP) por ventana. Nada de contenido."""

    def __init__(self, maximo: int = 30, ventana_s: int = 3600):
        self.maximo, self.ventana = maximo, ventana_s
        self._marcas = collections.defaultdict(collections.deque)

    @staticmethod
    def hash_origen(origen: str) -> str:
        return hashlib.sha256((_sal() + (origen or "anonimo")).encode()).hexdigest()[:16]

    def permite(self, origen: str) -> bool:
        ahora = time.monotonic()
        cola = self._marcas[self.hash_origen(origen)]
        while cola and ahora - cola[0] > self.ventana:
            cola.popleft()
        if len(cola) >= self.maximo:
            return False
        cola.append(ahora)
        return True
