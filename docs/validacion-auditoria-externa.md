# Nelli · Validación para auditoría externa

**Fecha de este documento:** 2-nov-2026. **Propósito:** que una persona ajena
al proyecto pueda comprobar, con el repo en la mano, quién hizo Nelli, desde qué
cuenta se entrega, qué está probado y qué sigue pendiente. Nada de lo que aquí
se afirma como hecho carece de respaldo en el repo; lo no probado se dice así.

## 1. Identidad del proyecto

- **Proyecto:** Nelli — verificador de mensajes sospechosos para México y
  Latinoamérica. Pegas un mensaje, una captura o una nota de voz y devuelve
  una tarjeta en español claro: nivel de riesgo en 4 niveles (nunca verde,
  nunca porcentajes, jamás dice «es seguro»), evidencia en 5 puntos, un solo
  paso a seguir y la fuente oficial verdadera.
- **Evento:** Meta Global AI Developer Hackathon 2026, track Indie
  (*Build for Your World*).
- **Entrega (submit):** 4-nov-2026, 18:00 hora del Pacífico (21:00 ET).
- **Lema:** «Verifica antes de creer, comprar o contestar.»
- **Posicionamiento:** «Seguridad para todos, en la palma de tu mano.»

## 2. Titular, cuenta y repositorio (esto es lo que se valida primero)

- **Titular de la cuenta:** la autora que consta en la sección «Autoría y
  método de trabajo» del `README.md`.
- **Cuenta:** una sola, la misma con la que se hizo la inscripción al
  hackathon, se creó el repositorio y se hace el submit. Una sola cuenta y una
  sola entrega, por las reglas del evento (track Indie, hasta 4 personas
  registradas; aquí, una).
- **Repositorio oficial:** https://github.com/flor-soriano/nelli
  (cuenta `flor-soriano`, rama `main`).
- **Visibilidad:** el desarrollo se hizo en local, por seguridad y por el tema
  delicado que trata Nelli; se publica completo el 4-nov-2026, al cierre del
  evento, tras la revisión de seguridad (A11 y la sección 9).
- **Alineación:** el registro de la plataforma, la sección de autoría del
  README y la configuración del repositorio dicen lo mismo: una sola persona
  registrada, titular de la cuenta.

## 3. Quién lo hizo (una sola persona registrada)

| Persona | Rol exacto |
|---|---|
| **La titular de la cuenta** | Única persona registrada. Revisa la demo y envía el submit. Motor de verificación, reglas, API de Muse, arquitectura, evaluación, video, frente visual (tarjeta web, feed, Blindar) y lista oficial con fuente y fecha por fila. |

Detalle en `docs/reparto.md`. La entrega es una sola y sale de esa cuenta.

## 4. Qué es verdad en el motor (líneas que la auditoría puede exigir)

- **Las reglas deciden; la IA solo explica.** El nivel final lo fijan reglas
  deterministas contra datos verificados a mano (paquete MX: 78 instituciones reales, 79 filas con el banco de la demo;
  66 verificadas fila por fila con fuente y fecha; 71 frases «nunca pide»;
  24 ligas ya reportadas; patrones de casos reales anonimizados, material de
  trabajo que no se publica), más
  registros públicos (URLhaus, RDAP). La IA puede *subir* una alerta, nunca
  bajarla.
- **«Fraude confirmado» nunca sale del modelo:** exige prueba dura (liga que
  imita un dominio oficial verificado, liga de la lista propia de ligas reportadas (con fuente y fecha), o pide lo que la
  institución publica que nunca pide, con la fila `verificado: true`).
- **Con llave, toda la inteligencia es Muse (Meta Model API), modalidad Standard:**
  Muse Spark 1.3 lee texto y capturas con esquema JSON estricto; Muse Voice
  Transcribe convierte la nota de voz; Muse Image generó la insignia de
  Blindar. El código **rechaza** modelos `contributor` (los mensajes de la
  gente no entrenan modelos). Sin otro proveedor de IA; sin llave, el nivel 0
  usa un emulador local y la tarjeta lo declara.
- **Privacidad por diseño:** no se guarda ningún mensaje, no hay cuentas, los
  archivos temporales se borran al terminar, el origen solo se guarda como
  hash, nunca se abre la liga sospechosa en un navegador (se piden solo
  encabezados sin cargar la página y se bloquean redes privadas).
- **Nelli no es un producto de Meta** ni está afiliada: es un proyecto
independiente que usa la Meta Model API. Sin logos de Meta como propios.

## 5. Endurecimiento del motor · Grupo A (2-nov-2026, verificado)

Trabajo hecho en este repositorio (ver `docs/muse-potenciada.md`): prueba
primero en cada mejora, suite en verde tras cada una, sin tocar reglas
congeladas ni el front. Cada prueba que se cita está en
`tests/test_endurecimiento.py` y se puede correr. Aquí no se citan hashes de
commit: el respaldo de cada fila es su prueba.

Base antes de empezar: 36 pruebas en verde. Resultado final:
**76 pruebas en verde** (una puede omitirse si hay `systemd-analyze` sin `/opt/nelli`) y `nelli autoprueba` en **15 de 15**.

| Mejora | Qué quedó | Prueba / resultado |
|---|---|---|
| A1 | Delimitadores blindados: el mensaje no puede cerrar el bloque de datos | `test_a1_*` |
| A2 | Mensaje largo sin recorte silencioso: reglas sobre el texto completo; servidor hasta 50 000 (413 si más); Spark recibe principio y final | `test_a2_*` (4) |
| A3 | Texto libre de la IA saneado antes de la tarjeta (fuera ligas, teléfonos, correos) | `test_a3_*` (2) |
| A4 | Spark con lo mínimo: sin `tools`, esquema estricto, URL de imagen solo https pública | `test_a4_*` (2) |
| A5 | ffmpeg acotado: lista blanca de formatos, `-t 180`, timeout 60; trampa `ffconcat` rechazada | `test_a5_*` (13) |
| A6 | Servidor con timeout 30, cupo de 4 simultáneas (503) y tope de 60/hora por origen | `test_a6_*` (2) |
| A7 | Verdad firmada: `paquete-mx/SHA256SUMS` + verificación al primer uso; `nelli sellar`; huella en `/api/salud` | `test_a7_*` (2) · huella actual `9fa25089b710` |
| A8 | `nelli autoprueba`: 15 comprobaciones sin llave ni internet | 15 de 15 |
| A9 | `requirements.lock` con hashes (`uv pip compile --extra qr --generate-hashes`); ffmpeg `n9.0.2` anotado en `docs/decisiones.md` | Venv limpio desde el lock: suite en verde |
| A10 | `deploy/nelli.service` encerrado con systemd + `deploy/LEEME.md` | `systemd-analyze verify` corrido el 3-nov: unidad válida; solo avisa que `/opt/nelli` no existe en el entorno de desarrollo |
| A11 | Revisión del repositorio: sin archivos en riesgo versionados, `.gitignore` completo, archivos sin rutas ni IPs de red local | Grep de secretos en lo versionado: **0** resultados |
| A12 | Banco de inyección contra Spark real (`eval/inyeccion.py`), una sola corrida | **6 de 6**, costo USD 0.0257 (tope 0.05) |
| Docs | Sección de endurecimiento en README y `docs/muse-potenciada.md`; Día 8 en `BUILD-LOG.md` | Solo con lo hecho y probado |

Costo acumulado de la API al 2-nov: **USD 0.2531 de un tope de 100**
(`nelli costos`, registro local en `costos.jsonl`, archivo no versionado).

## 6. Cómo reproduce esto un auditor (sin llave y sin red, salvo A12)

```bash
git clone https://github.com/flor-soriano/nelli.git && cd nelli
uv venv .venv && uv pip sync requirements.lock && uv pip install --no-deps -e .
uv pip install --python .venv/bin/python pytest
.venv/bin/python -m pytest -q        # esperado: 76 en verde (1 omitida si hay systemd-analyze sin /opt/nelli)
.venv/bin/python -m nelli autoprueba # esperado: 15 líneas OK, código de salida 0
git grep -nE 'MODEL_API_KEY=[A-Za-z0-9]|sk-[A-Za-z0-9]{20}|ghp_|BEGIN (RSA|OPENSSH)' $(git rev-list --all)
                                     # esperado: 0 resultados
```

La integridad del paquete se comprueba sola: cualquier byte cambiado en
`paquete-mx/*.json`, en `skills/leer-v1.md` o en el esquema hace que el motor
lance `IntegridadRota` al primer uso (eso es la comprobación 15 de la
autoprueba, sobre una copia temporal). `/api/salud` devuelve la huella del
paquete sellado (`9fa25089b710` al 4-nov).

## 7. Pendientes al 2-nov-2026 (lo que cambió después está en la sección 9)

- **Grupo B (B1–B4) intacto:** cambia niveles de riesgo y no se toca hasta
  que corra la prueba ciega D8 o exista una decisión escrita. Instalar Prompt
  Guard 2 (B2) se decide aparte.
- **Prueba ciega D8 sin correr:** ninguna cifra de efectividad existe
  todavía. Está prohibido publicar porcentajes de acierto antes de esa
  medición única (2-nov, `docs/plan-d6-d10.md`).
- **Repo público:** se publica el 4-nov al cierre del evento, con la
  revisión A11 ya hecha.
- **Video final y submit:** video definitivo tras las cifras D8 y envío el
  4-nov antes de las 18:00 hora del Pacífico desde la cuenta registrada, con captura
  del envío.

## 8. Dónde está cada respaldo

| Afirmación | Respaldo en el repo |
|---|---|
| Titular y cuenta | Sección «Autoría y método de trabajo» del `README.md` |
| Roles | `docs/reparto.md`, `docs/decisiones.md` |
| Qué es Nelli y sus líneas rojas | `README.md` |
| Pila Muse y fuentes de verdad | `docs/muse-potenciada.md` |
| Plan y fechas D6–D10 | `docs/plan-d6-d10.md` |
| Endurecimiento A1–A12 con pruebas | `tests/test_endurecimiento.py`, `BUILD-LOG.md` (Día 8) |
| Marco legal considerado | `docs/marco-legal.md` |

## 9. Actualización al 4-nov-2026

- **Grupo B aplicado el 3-nov** (B1, B3 y B4 en código; B2 instalado en local,
  fuera del repo): `docs/decisiones.md`, `tests/test_grupo_b.py`. Paquete
  sellado; huella actual `9fa25089b710` (`/api/salud` la devuelve).
- **Prueba sobre 50 casos documentados** (3-nov) en lugar del corpus ciego de
  ~600, que no se construyó: una sola corrida por rival, cifras con intervalo
  de Wilson 95 % en el README.
- **Nivel 0, emulador local** para probar sin llave, siempre marcado como «no
  es Muse» en la tarjeta, la página y `/api/salud`: `src/nelli/emulador.py`,
  `tests/test_emulador.py`.
- **Botón English / Español** en las cuatro pantallas (`web/idioma.js`).
- **Publicación:** Nelli se desarrolló y se probó en local desde el 26-oct,
  por seguridad y por el tema delicado que trata; se publica completa en
  GitHub el 4-nov y pasa a público al cierre del evento. `SECURITY.md`
  publicado.
- **Cómo reproducir hoy:** los mismos comandos de la sección 6; la suite
  incluye ahora `tests/test_grupo_b.py`, `tests/test_emulador.py` y
  `tests/test_integridad_crlf.py`.
