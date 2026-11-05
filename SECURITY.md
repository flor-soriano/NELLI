# Seguridad · Security

**English:** Nelli is a hackathon prototype, not a Meta product. To report a vulnerability, email flor@eldialogo.com with the subject «Nelli · seguridad». Please do not open a public issue for security problems. You will get an answer within 7 days. Do not test against anyone else's installation and do not send real victims' messages, bank screenshots or personal data.

## Cómo reportar una falla

- Escribe a **flor@eldialogo.com** con el asunto «Nelli · seguridad». No abras un *issue* público para fallas de seguridad.
- Respuesta en un máximo de 7 días. Es un proyecto de una persona: se agradece la paciencia.
- Prueba solo contra tu propia instalación. No pruebes contra la de nadie más.
- No mandes mensajes de víctimas reales, capturas de bancos reales ni datos de personas. Si el problema necesita un ejemplo, usa uno inventado o uno de `casos/demo.jsonl`.

## Qué versión se atiende

Solo la rama `main`. No hay versiones anteriores con soporte.

## Lo que Nelli hace para protegerse (y dónde verlo)

| Riesgo | Qué hace Nelli | Dónde |
|---|---|---|
| El mensaje intenta dar órdenes a la IA | Entra como **dato** entre delimitadores, con esquema JSON estricto; si trae texto dirigido a una IA, el nivel sube, nunca baja | `src/nelli/leer.py`, `src/nelli/defensas.py` |
| Abrir ligas peligrosas | Nelli **no abre ligas en un navegador**. Solo mira el dominio: sigue las redirecciones una por una pidiendo solo encabezados (HEAD; si el sitio lo rechaza, un GET cuyo cuerpo se descarta sin leer), resuelve el DNS una vez y se conecta a esa misma IP, y bloquea redes privadas y metadatos de nube (DNS rebinding incluido) | `src/nelli/herramientas/check_url.py` |
| Que alguien cambie «la verdad» (lista oficial, reglas, prompt) | Sellado con `paquete-mx/SHA256SUMS`; el motor se niega a arrancar si algo cambió sin sellar | `src/nelli/integridad.py` |
| Gasto sin control en la API | Tope por proyecto en `costos.jsonl` (100 USD) y registro por llamada | `src/nelli/costos.py` |
| Archivos subidos (capturas, audio) | Tamaño limitado, extensión permitida (y formato comprobado con ffmpeg en el audio), borrados al terminar; nada de usuarios se guarda | `src/nelli/servidor.py`, `src/nelli/nelli.py` |
| La llave de la API | Vive solo en `.env` (fuera de git) o en `/etc/nelli/nelli.env` con permisos `0640`. Nunca en código, commits, mensajes ni pantallas | `.env.example`, `deploy/LEEME.md` |
| El servicio en producción | Unidad de systemd sin privilegios, disco de solo lectura, sin acceso a redes privadas, topes de memoria y tareas; escucha solo en la interfaz local y lo expone un proxy inverso con TLS; con `NELLI_PROXY_CONFIANZA` (IP del proxy) el tope por origen distingue a cada usuario detrás del proxy | `deploy/nelli.service` |
| Mensajes diseñados para engañar al modelo | Prompt Guard 2 (opcional, se instala aparte) y pruebas de inyección contra la API real | `eval/inyeccion.py`, `scripts/instalar-prompt-guard.sh` |

## Lo que Nelli no hace, a propósito

No abre ligas en un navegador · no guarda mensajes · no reporta ni bloquea en nombre de nadie · no manda tu mensaje a nadie salvo a la Meta Model API para leerlo (consulta el dominio de la liga sin cargar la página, el registro público RDAP y, si hay llave, URLhaus) · no analiza documentos ni apps · nunca dice «es seguro» · no redacta ni mejora mensajes · no usa el modo *contributor* de la API (nada de lo que se manda sirve para entrenar modelos).

## Qué no cubre este aviso

Nelli es un prototipo de concurso. No ha pasado una auditoría externa formal y no está pensada para operar con datos de personas sin una revisión de seguridad previa. Las revisiones hechas durante el evento y lo que falta están en `docs/validacion-auditoria-externa.md`.
