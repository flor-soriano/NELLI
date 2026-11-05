# Nelli · verify before you believe, buy or reply

> **Unaffiliated prototype — not a Meta product.** Nelli is an independent hackathon project built *with* the Meta Model API; it is not made, endorsed or affiliated with Meta. It has its own front end and its own visual identity: no Meta logos, colors or brand assets are used.

**Nelli** (Nahuatl: *truth*; *nelti*, "to be verified") is a single-task verification agent for everyone in Mexico and Latin America who receives suspicious messages, posts or reels. Security for all, in the palm of your hand: it was designed for the hardest case (a 60-70-year-old who fears breaking something), so anyone can use it alone. It takes a text, a screenshot, a voice note or a link and returns a **card**: a plain-Spanish label on four levels, the **evidence in 5 points**, one step to take, the verified official source, and the buttons Report · Block · "Ask someone you trust" · "I already fell for it" · "Shield my account in 7 minutes". **Rules decide; the AI explains.** The AI can raise an alert, never lower it, and "Confirmed fraud" only comes from hard evidence that does not depend on the model. Built for the Meta Global AI Developer Hackathon 2026 (Indie track, *Build for Your World*) entirely on Meta's Muse via the Meta Model API (Muse Spark 1.3, Muse Voice Transcribe, Muse Image) and open-weight Prompt Guard 2. Full stack and truth sources: `docs/muse-potenciada.md`. Vision: built to be adoptable by Meta inside Facebook/WhatsApp (`docs/vision-adopcion-meta.md`) — claimed as vision, never as fact, until Meta signs it.

> **Hardening (built during the event, Nov 2–4, 2026):** every hardening measure in the engine was added test-first (A1–A12 in `BUILD-LOG.md`, Day 8, and Group B on Day 9), and the repository went through a security review before going public (`SECURITY.md`). At runtime, with an API key, all of Nelli's intelligence is Muse; without one, level 0 runs a local stand-in and the card says so.

---

Nelli es la capa de verificación que podría ir **sobre el mismo reel, post, anuncio o mensaje**: un aviso, un botón **Verificar** y una tarjeta con la etiqueta en palabras sencillas, la prueba a la vista en 5 puntos, un solo paso, la fuente oficial y los botones. En el concurso se construye el **motor real** con los modelos de Meta, un **prototipo del feed** y una **tarjeta web** donde cualquiera pega un mensaje, sube una captura, una nota de voz o una liga. No conversa; verifica.

## Cuatro niveles y un estado

| Etiqueta | Cuándo | Quién la da |
|---|---|---|
| **Fraude confirmado** | la liga imita a un dominio de la lista oficial · la liga ya está reportada · pide algo que la institución publica que nunca pide | solo las reglas: fila verificada de la lista oficial, o liga de la lista propia de ligas reportadas (con fuente y fecha) |
| **Muy probablemente es fraude** | pide dinero, NIP o código con prisa · texto dirigido a una IA · imitación aún sin verificar | reglas o IA |
| **Posible fraude** | una señal suelta | reglas o IA |
| **No vemos señales claras** | ninguna señal. Nunca dice «seguro» | si nadie subió el nivel |
| **No pude revisarlo** | captura ilegible, sin mensaje que revisar o demasiadas consultas desde el mismo origen (un audio de más de 3 minutos no se rechaza: se revisan los primeros 3 y se avisa) | el sistema; nunca adivina |

Sin verde y sin porcentajes.

## Arquitectura (4 capas)

- **Negocio**: persona ve contenido con señales → aviso → Verificar → tarjeta → Reportar/Bloquear → Blindar cuenta.
- **Información**: paquete MX versionado (`paquete-mx/`: lista oficial de dominios con fuente y fecha por fila, los «nunca» de cada institución, 15 tipos de estafa, plantillas escritas a mano, reglas). Nada de usuarios se guarda; archivos borrados al terminar; orígenes solo como hash.
- **Aplicaciones**: `src/nelli/` — `nelli.py` (orquestación) · `leer.py` (Spark 1.3 con `response_format` json_schema estricto; el mensaje entra como **dato** entre delimitadores) · `reglas.py` (decide) · `tarjeta.py` (5 puntos) · `defensas.py` (negativa fija, inyección, Prompt Guard 2, topes) · `herramientas/` (`check_url` sin cargar páginas y con bloqueo de redes privadas, `lista_oficial`, `rdap`, `urlhaus`, `qr`) · `muse.py` (cliente de la Meta Model API con costos por llamada) · `feed/` y `web/` (front).
- **Tecnología**: Meta Model API en Standard (`muse-spark-1.3`, `muse-voice-transcribe-1.0`, `muse-image-1.0`) · Prompt Guard 2 local · Python 3.12+ · ffmpeg.

## Hecho con Muse (Meta Model API)

Con llave, toda la lectura la hace Muse, siempre en modo Standard (nada de lo que se manda entrena modelos); el código rechaza cualquier modelo `-contributor`.

| Modelo | Dónde | Qué hace |
|---|---|---|
| **Muse Spark 1.3** (`muse-spark-1.3`) | `src/nelli/muse.py`, `src/nelli/leer.py`, `skills/leer-v1.md` | Lee el texto o la captura con `response_format` de esquema JSON estricto (`src/nelli/esquema/leer-v1.json`) y explica en español claro. Solo puede subir el nivel, nunca bajarlo; «Fraude confirmado» no existe en su esquema. |
| **Muse Voice Transcribe** (`muse-voice-transcribe-1.0`) | `muse.py:transcribir()` | Convierte la nota de voz (WAV mono 16 kHz, preparado con ffmpeg) en texto, que se revisa igual que un mensaje escrito. |
| **Muse Image** (`muse-image-1.0`) | `muse.py:generar_imagen()` | Generó la insignia «Cuenta blindada» (`web/insignia-blindar.png`) y las fotos del feed de demostración (`feed/img/*.png`). |
| **Prompt Guard 2** (pesos abiertos de Meta, opcional) | `src/nelli/defensas.py`, `scripts/instalar-prompt-guard.sh` | Filtro local contra inyección; se instala aparte con licencia propia y, si no está, la tarjeta lo declara. |

Alrededor del motor, sin IA: Python 3.12, `httpx` para la API, `uv` con `requirements.lock` fijado por hash, ffmpeg (conversión de audio con lista blanca de formatos y tope de 180 s), `http.server` de la biblioteca estándar para el servidor, systemd para encerrar el servicio (`deploy/`), y RapidOCR + faster-whisper solo dentro del emulador local del nivel 0. Detalle de la pila y de las fuentes de verdad: `docs/muse-potenciada.md`.

## Cómo correrlo

```bash
uv venv .venv && uv pip sync requirements.lock && uv pip install --no-deps -e .
cp .env.example .env            # pon tu MODEL_API_KEY (dev.meta.ai, Standard)
nelli verificar --canal sms "BANCO REAL: tu cuenta será bloqueada hoy. Valida tus datos en bancoreal-info.com/validar"
nelli verificar --sin-ia "..."  # reglas solas (rival 1), sin llave
nelli verificar --imagen captura.png --canal whatsapp
nelli verificar --audio nota.ogg --canal whatsapp
nelli probar-muse               # una llamada real a Spark, con tokens y costo
python eval/correr.py --sin-ia  # los dos errores con intervalo de Wilson 95 %
uv pip install pytest           # las pruebas no van en el lock
pytest -q
```

## Probarlo si acabas de clonar (4 niveles)

El repo no trae llaves ni el modelo de Prompt Guard: son de cada quien. Por eso la prueba va por niveles y el nivel 1 ya funciona sin cuentas de nada.

**Nivel 0 · Sin llave, con todo encendido (emulador local; no es Muse).** `uv pip install -e ".[emulador]"` y `python -m nelli.servidor`: si no hay `MODEL_API_KEY`, el servidor levanta solo `nelli.emulador` en la propia computadora (puerto 8777), un servidor local que imita la *forma* de la Meta Model API para que capturas y notas de voz también funcionen: lee la imagen con RapidOCR, transcribe con faster-whisper (modelo `small`, se baja una vez) y llena la lectura con palabras clave sobre el mismo esquema `leer-v1`. Las reglas siguen mandando y «Fraude confirmado» solo lo dan ellas. Todo queda marcado: la tarjeta dice «IA: emulación local (no es Muse)», la página avisa arriba, `/api/salud` devuelve `"emulador": true` y `costos.jsonl` registra `emulador-local` a 0 USD. Sirve para probar la experiencia completa sin cuenta; lo que se evaluó y lo que enseña el video es Muse (nivel 2). `--sin-emulador` deja reglas solas; `--emulador` lo fuerza aunque haya llave.

**Nivel 1 · Sin cuentas (reglas solas).** Tras instalar: `nelli verificar --sin-ia "BANCO REAL: tu cuenta será bloqueada hoy. Valida tus datos en bancoreal-info.com/validar"` debe dar «Fraude confirmado», y `pytest -q` debe dar toda la suite en verde (76 pruebas; una puede omitirse si hay `systemd-analyze` sin `/opt/nelli`). La evaluación demo: `python eval/correr.py --sin-ia`.

**Nivel 2 · Con la Meta Model API (Nelli completa).** Crea tu llave en dev.meta.ai (Standard, nunca contributor), ponla en `.env` como `MODEL_API_KEY=` y corre `nelli probar-muse` (una llamada real, con tokens y costo) y `nelli verificar` ya con IA, captura (`--imagen`) o nota de voz (`--audio`). La evaluación de 50 casos de la sección «Resultados» se repite con `python eval/correr.py eval/casos-documentados-50.jsonl --sin-red` (con IA) y `--sin-ia` (reglas solas). El servidor de la demo: `python -m nelli.servidor` y abrir `http://localhost:8000` (solo escucha en la propia computadora).

**Nivel 3 · Prompt Guard 2 (el extra de Hugging Face).** Es un modelo de Meta con licencia: no puede viajar dentro del repo (pesa 1.1 GB y su licencia se acepta por persona). Cada quien lo instala con su cuenta: acepta la licencia en https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M, entra con `.venv/bin/hf auth login` y corre `bash scripts/instalar-prompt-guard.sh`. Queda en `modelos/` (fuera de git) y se activa solo cuando lo pides: `NELLI_PROMPT_GUARD=modelos/prompt-guard-2 nelli verificar "..."`. Sin esto, Nelli funciona igual y la tarjeta declara «Prompt Guard 2 (no instalado aún)» en vez de fingir que lo revisó.

La prueba de inyección contra Spark real (A12) vive en `eval/inyeccion.py` y gasta unos centavos de API por corrida.

## Resultados

Prueba del 3-nov-2026 sobre 50 casos documentados el 31-oct-2026 (`eval/casos-documentados-50.jsonl`: 45 fraudes y 5 legítimos (4 marcados como difíciles), textos citados o reconstruidos desde alertas públicas en `docs/casos-reales-50-2026-10-31.md`, sin nombres, teléfonos ni ligas vivas). Las reglas v2 son del 28-oct: estos casos no se usaron para ajustarlas. Corrida sin red (las ligas son inventadas y desarmadas), una sola vez por rival, con intervalo de Wilson 95 %:

| Rival | Fraudes escapados | Legítimos marcados en rojo | «Confirmado» sobre un legítimo |
|---|---|---|---|
| Reglas solas | 15/45 = 33.3 % (IC95 21.4–47.9 %) | 0/5 = 0 % (IC95 0–43.4 %) | 0 |
| Muse Spark solo (su `nivel_sugerido`) * | 1/45 = 2.2 % (IC95 0.4–11.6 %) | 0/5 = 0 % (IC95 0–43.4 %) | 0 |
| Nelli (reglas + Muse Spark) | 1/45 = 2.2 % (IC95 0.4–11.6 %) | 0/5 = 0 % (IC95 0–43.4 %) | 0 |

\* La fila «Spark solo» se corrió a mano el 3-nov leyendo el `nivel_sugerido` de cada lectura; no hay script en el repo que la repita, así que `eval/correr.py` solo reproduce las otras dos filas.

El único fraude escapado con Nelli completa es el QR pegado sin texto que revisar (d36): no hay mensaje que juzgar. La muestra de legítimos es chica (5) y el plan inicial era de ~600 casos con corpus ciego, que no se alcanzó a construir: estas cifras son esa prueba reducida. Bitdefender Scamio no se corrió (es una prueba manual externa). La demo de 16 casos (`casos/demo.jsonl`, reglas solas): 0 escapados y 0 legítimos en rojo.

## Previo vs. evento

| Ya existía antes del 26-oct (se declara) | Construido durante el evento |
|---|---|
| El concepto en papel; alertas públicas de CONDUSEF, SAT, CFE, WhatsApp y Meta; documentos oficiales de MX/CO/PE | Todo el código, el paquete MX, el corpus de evaluación, el prototipo del feed, la tarjeta web, el chequeo de 7 minutos, la evaluación, el endurecimiento del motor (2 y 3-nov) y la revisión de seguridad (4-nov) |

## Lo que Nelli no hace

No abre ligas en un navegador · no guarda mensajes · no reporta ni bloquea en nombre de nadie · no manda tu mensaje a nadie salvo a la Meta Model API para leerlo (consulta el dominio de la liga sin cargar la página, el registro público RDAP y, si hay llave, URLhaus) · no analiza documentos ni apps · nunca dice «es seguro» · no redacta ni mejora mensajes.

## Autoría y método de trabajo

Flor Soriano, única persona registrada en el concurso y titular de la cuenta `flor-soriano` en GitHub.

Nelli se desarrolló y se probó en local, en la computadora de la autora, del 26-oct al 4-nov-2026: código, paquete MX, pruebas, pantallas y evaluación, con `BUILD-LOG.md` como diario fechado de cada avance y `docs/decisiones.md` como registro de decisiones. Se trabajó en local por seguridad, por el tema delicado que trata Nelli, y se publica completa en GitHub el 4-nov-2026, al cierre del evento.

## Licencias

| Qué | Licencia | Texto |
|---|---|---|
| El programa (`src/`, `web/`, `feed/`, `eval/`, `scripts/`, `tests/`) | GNU AGPL-3.0 | `LICENSE` |
| Manual, textos, casos documentados e ilustraciones (`docs/`, `web/manual.html`, `feed/img/`, `video/`) | CC BY-NC-SA 4.0 | `LICENSE-CONTENIDO` |
| El nombre «Nelli» y su logotipo | Todos los derechos reservados: no se incluyen en ninguna de las dos licencias | — |

En corto: puedes usar, estudiar, modificar y compartir el programa; si lo modificas y lo ofreces a otras personas (también como servicio en línea), tienes que publicar tu código completo bajo la misma licencia. Para usarlo sin publicar tu código hace falta una licencia comercial aparte: escribe a flor@eldialogo.com.

El paquete `paquete-mx/` cita páginas oficiales de instituciones mexicanas; esas frases son de sus autores y se citan con liga y fecha.
