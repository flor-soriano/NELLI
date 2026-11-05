# Nota · Distinguir voz humana de voz IA (30-oct-2026)

Idea evaluada: que Nelli diga si una nota de voz es humana o de computadora.

Verificado hoy: la transcripción de Muse Voice solo devuelve texto, duración
y turnos; no trae marca de voz sintética, y Spark no recibe audio crudo. El
motor no tiene ninguna señal de autenticidad de voz, así que hoy **no** se
puede distinguir sin inventar.

Mientras tanto, la pantalla ya avisa honesto al revisar audio: «todavía no
distingo si la voz es humana o de computadora».

La capacidad real sería un modelo anti-suplantación de audio (tipo AASIST)
con su propia evaluación: es decisión del motor, no parche de front.

## Evidencia (30-oct, con llave real)

Respuesta cruda de `POST /v1/asr/transcribe` con un WAV de prueba:

```json
{"sessionId": "voyager/transcribe/...", "transcript": "Hola, soy tu hijo, cambié de número...",
 "audioDurationMs": 9200, "turns": []}
```

Solo hay texto, duración y turnos: ningún campo de hablante, de voz sintética
ni de confianza por voz. En el código, `muse.py` solo expone `chat/completions` (texto e
`image_url`) y esa transcripción; `leer.py` lee imágenes, no audio. Sin una
señal de entrada, cualquier «es voz IA» sería inventado: por eso la pantalla
avisa que no lo distingue en vez de simularlo.

Segunda prueba (30-oct): mandar el WAV crudo a Spark 1.3 como parte
`input_audio` en `/v1/chat/completions`. La API acepta la petición (200),
pero en dos corridas (120 y 700 tokens) todo el presupuesto se fue en
razonamiento y `content` volvió vacío: no hay juicio de voz usable por esa
vía tampoco. Bloqueo concreto: sin un modelo detector evaluado, la distinción
voz humana/IA no se ofrece; la previa de audio y el aviso honesto de la
pantalla se quedan como están.
