#!/usr/bin/env python3
"""Quema subtitulos EN con placa oscura sobre el master sin subtitulos.
Uso: python quemar_subs.py <master.mp4> <subs.srt> <salida.mp4>
Dibuja cada frase con PIL (Inter SemiBold, blanco, placa negra 65%) y la anima con ffmpeg overlay.
El audio se pasa sin tocar (ya normalizado en la pasada de loudness si se aplica despues)."""
import re, subprocess, sys, os, tempfile
import os
from PIL import Image, ImageDraw, ImageFont

master, srt_path, salida = sys.argv[1:4]
FONT = os.environ.get("NELLI_FUENTE_SUBS", "/usr/local/share/fonts/inter/InterDisplay-SemiBold.ttf")
W, H, TAM = 1080, 1920, 46

def ts(s):
    h, m, rest = s.split(":"); sec, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000

subs = []
for block in open(srt_path, encoding="utf-8").read().strip().split("\n\n"):
    lines = block.splitlines()
    a, b = [ts(x.strip()) for x in lines[1].split("-->")]
    subs.append((a, b, " ".join(lines[2:])))

font = ImageFont.truetype(FONT, TAM)
tmp = tempfile.mkdtemp(prefix="nelli-subs-")  # carpeta temporal propia, no una ruta fija compartida
inputs = ["-i", master]
filters = []
prev = "[0:v]"
for i, (a, b, texto) in enumerate(subs):
    # partir en 2 lineas si hace falta (max ~34 caracteres por linea medido en pixeles)
    words, lineas, cur = texto.split(), [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if font.getlength(cand) > 880 and cur:
            lineas.append(cur); cur = w
        else:
            cur = cand
    if cur: lineas.append(cur)
    anchos = [font.getlength(l) for l in lineas]
    asc, desc = font.getmetrics(); lh = int((asc + desc) * 1.12)
    pad_x, pad_y = 34, 20
    cw, ch = int(max(anchos)) + pad_x * 2, lh * len(lineas) + pad_y * 2
    img = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, cw - 1, ch - 1], radius=18, fill=(0, 0, 0, 168))
    for j, (l, w) in enumerate(zip(lineas, anchos)):
        d.text(((cw - w) / 2, pad_y + j * lh), l, font=font, fill=(255, 255, 255, 255))
    p = f"{tmp}/s{i:02d}.png"; img.save(p)
    inputs += ["-i", p]
    nxt = f"[v{i}]"
    x = "(W-w)/2"; y = "1500-h/2"
    filters.append(f"{prev}[{i+1}:v]overlay=x={x}:y={y}:enable='between(t,{a:.3f},{b:.3f})'{nxt}")
    prev = nxt

fc = ";".join(filters)
cmd = ["ffmpeg", "-y", "-v", "error"] + inputs + ["-filter_complex", fc, "-map", prev, "-map", "0:a",
       "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "60", "-c:a", "copy", salida]
subprocess.run(cmd, check=True)
print("OK", salida, len(subs), "frases")
