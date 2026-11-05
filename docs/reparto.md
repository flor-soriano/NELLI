# Reparto de trabajo · Nelli · 26-oct → 4-nov

| Quién | Qué | Carpetas |
|---|---|---|
| **La titular de la cuenta** (única persona registrada) | Todo: motor y API de Muse (`leer.py`, lectura de imagen por `chat/completions`, Voice Transcribe), API HTTP, repo y entrega, video, arquitectura, reglas, herramientas, defensas, evaluación, seguridad, revisión final y todo lo visual (feed, tarjeta web, Blindar, insignia) | `src/nelli/`, `feed/`, `web/`, `casos/`, `paquete-mx/`, `eval/` |

## Contrato front ↔ motor

El motor devuelve **una tarjeta JSON** (ejemplo real en `web/ejemplo-tarjeta.json`). Campos que pinta el front:

| Campo | Qué es |
|---|---|
| `etiqueta` · `nivel` | Texto grande. Colores: `fraude_confirmado` rojo · `muy_probablemente_fraude` ámbar oscuro · `posible_fraude` ámbar · `sin_senales_claras` gris · `no_pude_revisar` gris. **Nunca verde, nunca porcentajes.** |
| `puntos[5]` | `{n, titulo, texto, estado}`; `estado` = `ok` (✓) · `alerta` (!) · `no_revisado` («no pude revisar», en gris) |
| `paso` | Un solo paso, destacado |
| `botones[]` | Reportar · Bloquear · Pregúntale a alguien de confianza · Ya caí, ¿qué hago? · (en rojo) Blindar mi cuenta en 7 minutos |
| `mensaje_confianza` | Texto que arma el botón «Pregúntale a alguien de confianza»; la persona lo reenvía ella misma |
| `ya_cai` | Texto del botón «Ya caí», sin regaños |
| `fuente_verificada` | Institución + dominio oficial, con insignia |
| `ligas_desactivadas` | Ligas con `[.]`: se muestran así, sin vista previa y sin ser clicables |
| `licencia` | Gris chico: contra qué versión se revisó, qué no se pudo ver, cómo repetirlo |

API HTTP (mientras, el front usa el JSON de ejemplo):

- `POST /api/verificar` con JSON `{"texto": "...", "canal": "feed|web|whatsapp|sms|email|messenger"}` → tarjeta.
- `POST /api/verificar` multipart con `imagen` o `audio` (extensiones permitidas en `src/nelli/servidor.py`) + campo `canal` → tarjeta.
- Tope por origen: cuando se pasa, el motor devuelve `nivel: no_pude_revisar` con la razón.

## Pantallas

1. **Feed (prototipo)**: reel/post real público; debajo del texto, aviso en ámbar «⚠ Oferta no verificada: verifica 5 puntos antes de comprar · Verificar». Etiqueta de estante: Información · Oferta-venta · Petición de datos · Entretenimiento.
2. **Tarjeta** (se abre encima, sin salir): etiqueta grande, 5 puntos, un paso, fuente verificada, botones, licencia en gris chico.
3. **Blindar mi cuenta en 7 minutos**: 7 pasos con liga a cada ajuste; la persona marca cada paso y el avance se guarda solo en su aparato; insignia «Cuenta blindada» (Muse Image).
4. **Tarjeta web**: cuadro para pegar texto o liga, botón para subir captura o nota de voz, la misma tarjeta. Aviso visible antes de revisar: «no se abre la liga en un navegador, no se guarda tu mensaje y nadie te va a cobrar».

Reglas de diseño: español de casa, letra grande, sin tecnicismos, sin verde, sin porcentajes.
