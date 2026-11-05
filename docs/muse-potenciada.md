# Nelli potenciada por Muse · seguridad para todos, en la palma de tu mano

**Posicionamiento:** Nelli no es «para viejitos». Es seguridad para todos.
Se diseñó con la persona más exigente en mente — 60 a 70 años, vista cansada,
miedo de romper algo — porque si ella lo usa sola, lo usa cualquiera:
el joven con prisa, la mamá que vende por WhatsApp, el repartidor, el negocio.

## La pila Muse (Meta Model API) que ya corre en Nelli

Todo lo inteligente de Nelli es Muse, el modelo de Meta. Nada de otro proveedor.

| Pieza Muse | Archivo | Qué hace en Nelli |
|---|---|---|
| **Muse Spark 1.3** `muse-spark-1.3` | `src/nelli/muse.py`, `leer.py`, `skills/leer-v1.md` | Lee el texto, la captura y el mensaje reenviado con `json_schema` estricto. Explica en español claro. **Solo puede subir la alerta, nunca bajarla.** |
| **Muse Voice Transcribe** `muse-voice-transcribe-1.0` | `muse.py:transcribir()` | Convierte la nota de voz en texto para revisarla igual que un mensaje escrito. |
| **Muse Image** `muse-image-1.0` | `muse.py:generar_imagen()` | Generó la insignia «Cuenta blindada» de Blindar (`web/insignia-blindar.png`, 30-oct-2026) y las fotos del feed de demostración (`feed/img/*.png`). |
| **Prompt Guard 2** (pesos abiertos de Meta) | `src/nelli/defensas.py` | Filtro local opcional contra inyección: el mensaje del estafador entra como dato, nunca como orden. |
| Cliente propio + costos | `muse.py`, `costos.py` | Standard siempre; el código **rechaza** modelos `contributor` (que Meta no entrene con mensajes de la gente). Cada llamada se registra con su costo. |

## La verdad contra la que verifica: datos, no opiniones

Muse no «adivina» si algo es fraude. La decisión sale de datos comprobables,
y Muse solo los explica:

| Fuente de verdad | Tipo | Quién la mantiene |
|---|---|---|
| Lista oficial MX: dominios reales de bancos, SAT, CFE, paqueterías (`paquete-mx/*-v2.json`, 79 filas, 66 verificadas) | Datos verificados **a mano**, fila por fila, con fuente y fecha | Nelli, a mano |
| Los «nunca pide» de cada institución (71 filas) | Dato oficial publicado por la institución | Nelli, copiado a mano letra por letra |
| URLhaus (abuse.ch) vía `herramientas/urlhaus.py` | Big data pública de ligas maliciosas reportadas en el mundo | Comunidad / abuse.ch |
| RDAP vía `herramientas/rdap.py` | Registro público de dominios: edad del dominio | Registros de internet |
| `check_url.py` | Sigue la liga **sin cargarla en un navegador** (solo encabezados, bloquea redes privadas) | Motor Nelli |
| Reglas MX versionadas (`reglas.py`) | Patrones de fraude de casos reales anonimizados (material de trabajo, no publicado) | Nelli |

**La frase honesta:** las reglas deciden con datos; Muse explica.
«Fraude confirmado» nunca lo dice el modelo: sale solo de prueba dura
(liga que imita un dominio oficial verificado, liga ya reportada, o pide lo
que la institución publica que nunca pide).

## Endurecimiento del motor (A1–A12)

Las doce mejoras del 2-nov-2026 se hicieron con prueba primero y la suite en verde tras cada una, a partir de pruebas de ataque escritas en `tests/test_endurecimiento.py` (inyección, SSRF, archivos trampa, topes). La inteligencia de Nelli sigue siendo solo Muse. Lo que quedó en el motor:

| Lección | Dónde vive en Nelli | Prueba |
|---|---|---|
| El contenido que lee la IA es dato, nunca orden | A1: delimitadores neutralizados en `src/nelli/leer.py` | `test_a1_delimitadores_del_mensaje_quedan_neutralizados` |
| Recortar en silencio rompe todo | A2: reglas sobre el texto completo y Spark con principio+final en `leer.py`, `servidor.py`, `nelli.py` | `test_a2_*` (4 pruebas) |
| La IA inventa evidencia | A3: texto libre de la IA saneado en `defensas.limpiar_texto_ia`, aplicado en `tarjeta.py` y `reglas.py` | `test_a3_*` (2 pruebas) |
| Spark con lo mínimo | A4: sin `tools`, esquema estricto y URL de imagen solo https pública en `muse.py` | `test_a4_*` (2 pruebas) |
| El encierro real es el sistema operativo | A5: ffmpeg con lista blanca de formatos, `-t 180` y timeout en `nelli.py` | `test_a5_*` (13 pruebas) |
| Topes de memoria, tareas y tiempo por agente | A6: semáforo de 4, timeout 30 y tope por origen en `servidor.py` | `test_a6_*` (2 pruebas) |
| El agente no puede reescribir sus propias reglas | A7: `paquete-mx/SHA256SUMS` e `integridad.verificar()` en `reglas.py` y `leer.py` | `test_a7_*` (2 pruebas) |
| Una autoprueba fija debe dar N de N | A8: `nelli autoprueba` en `__main__.py` | 15 de 15; `test_a8_autoprueba_da_15_de_15` |
| Mismo nombre no es mismo código | A9: `requirements.lock` con hashes y `ffmpeg n9.0.2` anotado en `docs/decisiones.md` | `test_a9_lock_con_hashes_y_readme_lo_usa`; venv limpio desde el lock en verde |
| El encierro real es el sistema operativo | A10: `deploy/nelli.service` y `deploy/LEEME.md` | `test_a10_*`; `systemd-analyze verify` corrido el 3-nov: unidad válida, solo avisa que `/opt/nelli` no existe en el entorno de desarrollo |
| Nada se publica sin revisar | A11: `.gitignore` completo y archivos sin rutas ni IPs de red local | `test_a11_repo_sin_archivos_en_riesgo_ni_datos_locales`; grep de secretos en lo versionado: 0 |
| Se mide, no se supone | A12: `eval/inyeccion.py`, una sola corrida contra Spark real | 6 de 6, USD 0.0257 de un tope de 0.05 (2-nov) |

El Grupo B (B1–B4) se aplicó el 3-nov-2026: `docs/decisiones.md` y `tests/test_grupo_b.py`.

## La finalidad: que Meta lo adopte

Esto está pensado para que un día Facebook y WhatsApp lo tengan dentro
(ver `docs/vision-adopcion-meta.md`): primero como contacto de WhatsApp por
la vía oficial, después como botón Verificar sobre el contenido. **Ese día**
«con los datos de Meta detrás» será verdad. Hoy es la visión que se le
presenta al jurado, no un hecho que se afirme.

## Lo que Nelli NO es (y no va a fingir)

- Nelli **no** es un producto de Meta ni está afiliada. Es un proyecto
  independiente **hecho con** la Meta Model API (Muse). El front y la piel son
  propios: sin logos, colores ni activos de Meta.
- Nelli **no** accede a datos internos de Facebook ni de WhatsApp. Cuando en
  el pitch se dice «la verdad es datos», son los datos de arriba: fuentes
  oficiales verificadas y registros públicos de internet (la extranet),
  no la big data privada de nadie.
- La piel visual es 100% Nelli (grafito, blanco, menta y ámbar). Ni el azul de
  Facebook ni el verde de WhatsApp: ver `docs/piel-nelli.md`.

## Lo manual potencia a Muse (y al revés)

Lo hecho a mano — verificar 66 instituciones, copiar los
«nunca» letra por letra, anonimizar casos reales, escribir las
plantillas — es lo que Muse no puede inventar. Muse pone la lectura y la
explicación en segundos. Esa mezcla es Nelli: **datos verdaderos, explicados
para cualquiera.**
