"""Orquestación: el viaje del mensaje, paso por paso. Presentación (web/, feed/, puente) → aquí → servicios."""
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from . import defensas, leer, reglas, tarjeta
from .herramientas import check_url, qr
from .muse import Muse, SinLlave


@dataclass
class Entrada:
    texto: str = ""
    canal: str = "desconocido"       # whatsapp | sms | email | messenger | feed | web | desconocido
    origen: str = "cli"              # quién pregunta (número, IP, sesión): solo se guarda su hash
    imagen: str | None = None        # ruta a PNG/JPG
    audio: str | None = None         # ruta a OGG/MP3/WAV
    ligas: list[str] = field(default_factory=list)
    borrar_archivos: bool = False    # True en servidor: los archivos bajados se borran al terminar


# «3gp» se añadió a la lista: es el formato que reporta ffprobe para .3gp, extensión permitida del servidor.
FORMATOS_AUDIO = "wav,mp3,ogg,mov,matroska,flac,aac,amr,caf,3gp"


def _ejecutable(nombre: str) -> str:
    """Ruta completa de ffmpeg/ffprobe: NELLI_FFMPEG / NELLI_FFPROBE si están, si no la que resuelve el PATH
    al arrancar (y no una búsqueda en cada llamada)."""
    fijo = os.environ.get("NELLI_" + nombre.upper(), "").strip()
    if fijo:
        return fijo
    return shutil.which(nombre) or nombre


def convertir_a_wav(ruta_audio: str, destino_dir: str) -> str:
    salida = str(Path(destino_dir) / "voz.wav")
    subprocess.run([_ejecutable("ffmpeg"), "-nostdin", "-y", "-loglevel", "error",
                    "-protocol_whitelist", "file", "-format_whitelist", FORMATOS_AUDIO,
                    "-i", ruta_audio, "-t", "180", "-ac", "1", "-ar", "16000", salida],
                   check=True, timeout=60, stdin=subprocess.DEVNULL)
    return salida


def duracion_audio(ruta_audio: str) -> float:
    """Segundos según ffprobe; 0 si no se pudo medir."""
    try:
        r = subprocess.run([_ejecutable("ffprobe"), "-v", "error", "-show_entries", "format=duration",
                            "-of", "default=noprint_wrappers=1:nokey=1", ruta_audio],
                           capture_output=True, text=True, timeout=30, stdin=subprocess.DEVNULL)
        return float(r.stdout.strip())
    except Exception:
        return 0.0


def verificar(entrada: Entrada, con_ia: bool = True, red: bool = True, muse: Muse | None = None,
              tope: defensas.TopeOrigen | None = None) -> dict:
    if tope and not tope.permite(entrada.origen):
        return tarjeta.no_pude_revisar("Demasiadas consultas desde este origen; intenta más tarde.", entrada)
    texto, no_pude, tmp = entrada.texto or "", [], None
    try:
        if con_ia and muse is None:
            try:
                muse = Muse()
            except SinLlave as e:
                no_pude.append(str(e)); con_ia = False

        if entrada.audio:
            if not con_ia:
                no_pude.append("la nota de voz (sin IA no se transcribe)")
            else:
                tmp = tempfile.mkdtemp(prefix="nelli-")
                try:
                    wav = convertir_a_wav(entrada.audio, tmp)
                except Exception:
                    no_pude.append("la nota de voz (no se pudo convertir)")
                else:
                    try:
                        if duracion_audio(entrada.audio) > 180:
                            no_pude.append("la nota dura más de 3 minutos: revisé los primeros 3")
                        texto_voz, _ = muse.transcribir(wav)
                        texto = (texto + "\n" + texto_voz).strip()
                    except Exception as e:
                        no_pude.append(f"la nota de voz ({type(e).__name__})")

        if defensas.pide_mejorar_estafa(texto):
            return tarjeta.negativa(entrada)

        if len(texto) > leer.MAX_TEXTO:
            no_pude.append("el mensaje es muy largo: la IA leyó el principio y el final; las reglas lo revisaron completo")
        lectura = None
        if con_ia and (texto or entrada.imagen):
            try:
                lectura = leer.leer(muse, texto=texto or None, imagen=entrada.imagen, canal=entrada.canal)
            except Exception as e:
                no_pude.append(f"la IA no respondió ({type(e).__name__}); solo reglas")
            if lectura and lectura.get("texto_visto") and not texto:
                texto = lectura["texto_visto"]
        ligas_qr = qr.leer_qr(entrada.imagen) if entrada.imagen else None
        if entrada.imagen and ligas_qr is None and not lectura:
            no_pude.append("la captura (sin IA ni lector de QR no la puedo leer)")
        if lectura and lectura.get("_error"):
            no_pude.append(f"la IA no devolvió una lectura válida ({lectura['_error']}); solo reglas")
        if lectura and lectura.get("legible") is False and not texto.strip():
            return tarjeta.no_pude_revisar("La captura no se lee bien; manda otra más clara o el texto.", entrada)

        vistas = check_url.extraer_ligas(texto) + check_url.extraer_ligas((lectura or {}).get("texto_visto") or "")
        hosts_vistos = {check_url.host_de(l) for l in vistas + (ligas_qr or []) + entrada.ligas}
        origenes, ligas = {}, []
        for liga, origen in ([(l, "texto") for l in entrada.ligas]
                             + [(l, "texto") for l in check_url.extraer_ligas(texto)]
                             + [(l, "qr") for l in (ligas_qr or [])]
                             + [(l, "texto" if check_url.host_de(l) in hosts_vistos else "ia")
                                for l in ((lectura or {}).get("ligas") or [])]):
            if liga not in origenes:
                origenes[liga], ligas = origen, ligas + [liga]
        if not texto.strip() and not ligas:
            return tarjeta.no_pude_revisar("No hay mensaje que revisar.", entrada)

        senales = reglas.senales_texto(texto)
        guard = defensas.prompt_guard(texto)
        if guard is None:
            no_pude.append("Prompt Guard 2 (no instalado aún)")
        elif guard["etiqueta"].upper() in ("INJECTION", "JAILBREAK", "MALICIOUS", "LABEL_1") and guard["puntaje"] >= 0.8:
            senales["prompt_guard"] = f"{guard['etiqueta']} {guard['puntaje']}"
        ligas_info = reglas.senales_ligas(ligas, red=red, origenes=origenes) if ligas else []
        if ligas:
            senales["liga"] = str(len(ligas))
            if not red:
                no_pude.append("la red estaba apagada: no seguí redirecciones ni consulté RDAP/URLhaus")
        senales.update(reglas.senales_de_ligas(ligas_info))

        decision = reglas.decidir(senales, lectura, canal=entrada.canal, ligas_info=ligas_info, texto=texto)
        tipo = reglas.tipo_probable(senales, lectura, ligas_info)
        t = tarjeta.armar(decision, senales, ligas_info, lectura, entrada, tipo, no_pude)
        t["_trazas"] = {"senales": senales, "ligas": ligas_info, "lectura": lectura, "decision": decision}
        return t
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)
        if entrada.borrar_archivos:
            for ruta in (entrada.imagen, entrada.audio):
                if ruta and os.path.exists(ruta):
                    os.remove(ruta)
