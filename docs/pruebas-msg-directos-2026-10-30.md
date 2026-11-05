# Pruebas con SMS reales al número personal · 30-oct-2026 (anónimo)

Origen: 6 capturas de Mensajes de Google de un teléfono personal (SMS marcados como spam por Google). Traen números personales y un nombre propio: las copias locales se borraron; **nunca** al repo ni al video. Aquí solo va el patrón, sin números ni nombres. No es la prueba ciega D8.

## Resultados (captura directa, con IA real)

| # | Patrón del SMS | Antes del arreglo | Enfoque correcto |
|---|---|---|---|
| D1 | «Falabella»: liquida tu deuda con 78% de descuento, carta finiquito, por wa.link | Fraude confirmado con razón falsa | **Muy probablemente**, montadeudas |
| D2 | «Liverpool»: un solo día para liquidar, «castigo financiero», expediente, wa.link | Fraude confirmado, tipo equivocado | Cobranza amenazante, muy probablemente |
| D3 | «TELNOR»: paga tu línea en una liga corta; el recibo en la app | Muy probablemente (IA subió) | **Legítimo difícil**: la liga resuelve al dominio oficial de Telnor con campaña de cobranza; Nelli debe bajar a «posible» o «sin señales» cuando el destino final es oficial (ver hallazgo 2) |
| D4 | «Liverpool»: tu cuenta pasó a despacho de cobranza, liga `pws.mx` con puerto raro | Muy probablemente (IA) | Muy probablemente, correcto |
| D5 | «Telce» (sic): tienes 8360 «punts», canjéalos en acortador → página en vercel.app | Muy probablemente (IA), premio | Muy probablemente, correcto |
| D6 | Bandeja: 8 buzones de voz en un día, «gana $400 con tu primer invitado», cobranza Liverpool | — (solo inventario) | Material para corpus: buzón de voz masivo = señal de contexto, no mensaje único |

## Hallazgo 1 · CRÍTICO (ya corregido): la marca «link» confirmaba fraudes

La fila de Spin by OXXO traía `marca: ["link", "spinbyoxxo"]` (de `link.spinbyoxxo.com.mx`). Como `wa.link` contiene «link», **todo SMS con wa.link «imitaba a Spin by OXXO»**, y como esa fila está verificada, Nelli daba **Fraude confirmado** con la razón falsa «la liga no es de Spin by OXXO» — aunque el destino final era `api.whatsapp.com`, dominio oficial de Meta.

Arreglo (en código, no solo en datos, porque el paquete se regenera):
- `lista_oficial.buscar()`: las palabras genéricas de subdominio (`link`, `blog`, `ayuda`, `help`, `mail`, `group`, `citas`, `data`, `banco`, …) nunca cuentan como marca.
- `reglas.senales_ligas()`: si el destino final es un dominio oficial, no hay imitación posible.
- Regresión en `tests/test_reglas.py::test_marca_generica_no_imita` (wa.link, api.whatsapp.com, valida-tu-banco.com no imitan; bbva-clientes-mx.com sí imita a BBVA).

Re-corrido D1 tras el arreglo: **Muy probablemente es fraude**, tipo préstamo/montadeudas, «la liga sí es la oficial de Meta» — veredicto honesto: el engaño es el mensaje y el paso a otra app de mensajes, no la liga.

Esto también explica la atribución rara del caso A del caso académico («la liga no es de Hey Banco» por la marca genérica «banco»): ya no ocurre.

## Hallazgo 2 · Legítimo difícil de Telnor (pendiente, antes de congelar reglas D6)

Telnor no tiene fila en la lista oficial (79 filas, sin Telnor ni Falabella) y su liga corta resuelve al dominio oficial con UTM de cobranza. Aun así la IA subió a «Muy probablemente». Pendientes:
- Agregar fila de Telnor (y revisar carriers regionales) con fuente y fecha, como el resto del paquete.
- Regla de sentido común para la IA/reglas: si el destino final verificado es el dominio oficial de quien dice ser, el nivel no debería pasar de «Posible» solo por pedir un pago.

## Hallazgo 3 · Cobranza amenazante es su propio patrón

D1/D2/D4 son cobranza (real o falsa) con descuento enorme, «solo hoy», «castigo financiero» y paso a WhatsApp. Hoy caen en montadeudas/compra-venta. Candidato a tipo `cobranza_amenazante` con su plantilla: «una deuda real se puede verificar en la app o sucursal; nadie te liquida 78% por WhatsApp». Decisión pendiente antes de congelar.

Costo acumulado del proyecto: USD 0.094 de 100 (`nelli costos`).
