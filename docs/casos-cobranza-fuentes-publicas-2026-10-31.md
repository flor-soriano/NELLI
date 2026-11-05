# Casos de cobranza desde fuentes públicas · 31-oct-2026

La idea inicial era «scrapear Facebook y redes» por capturas reales de cobranza de
los últimos 3 meses. Eso **no se hizo**: Facebook lo bloquea y serían datos de víctimas
(nombres, teléfonos, deudas), que por regla del proyecto no se tocan ni entran al repo.

Lo que sí hay aquí: patrones publicados por policías y prensa (ago–oct 2026), con el
mensaje **reconstruido** al estilo del caso académico. Sin nombres, sin
teléfonos y sin ligas reales. La alerta de Michoacán publica 14 números: no se copiaron.

## Fuentes

| # | Fuente | Fecha | Qué aporta |
|---|---|---|---|
| F1 | Policía Cibernética Michoacán (FGE) vía Ministry of Cyber Affairs | Alerta 28-oct-2026 (nota 1-nov) | Llamadas montadeudas que amenazan por préstamos nunca pedidos; números de MX, Colombia y Nicaragua |
| F2 | Policía Cibernética Michoacán | feb-2026 | Aviso previo de montadeudas «dinero fácil» |
| F3 | SSC CDMX (citada en F1) | 2026 | Víctimas que solo bajaron la app, nunca recibieron dinero, y aun así las extorsionaron |
| F4 | InSight Crime / PVAngels (prensa) | 2023 (patrón vigente) | Cita textual de amenaza y mensajes a contactos etiquetando de «ratero/estafador» con fotos |
| F5 | ABM + CONDUSEF (prensa, MexExpats) | principios de sep-2026 | Ola de SMS fraudulentos de «bancos» con ligas; 42,791 quejas ene–jul 2026 |

## Casos reconstruidos para correr

### A · Montadeudas: deuda inventada (F1 + F3)
> «Descargaste nuestra app y tienes un préstamo vencido de $2,800. Si hoy no pagas,
> avisamos a todos tus contactos que eres un ratero y les mandamos tu foto.»

Señales: deuda que la persona no reconoce · amenaza con contactos/foto · prisa «hoy» ·
sin liga. Es el caso que F3 describe: ni siquiera recibieron dinero.

### B · Montadeudas: amenaza directa (F4, cita de prensa traducida)
> «Te vamos a desmembrar a la familia si no pagas en 20 minutos.»

En prensa sale en inglés («I will dismember your family if you don't pay us back in
20 minutes», dicho por una víctima a InSight Crime). Aquí va en español de casa como
circula por WhatsApp. Señales: amenaza de violencia · plazo en minutos · sin liga.

### C · Cobranza con amenaza de embargo (patrón REDECO)
> «ÚLTIMO AVISO. Su crédito está vencido. Si hoy no liquida, se procede al embargo de
> bienes y al bloqueo de sus cuentas. Despacho Jurídico Asociado.»

Reconstruido del patrón que CONDUSEF/REDECO prohíbe: la cobranza por mensaje no puede
amenazar con embargo ni hacerse pasar por autoridad judicial. Señales: amenaza legal ·
«hoy» · firma genérica de despacho · sin liga. **Este es el que merece tipo propio**
(`cobranza_amenazante`): puede venir hasta de un despacho real abusando, no es el
«fraude confirmado» clásico.

### D · Cobranza con descuento y prisa (ya cazado en las pruebas de SMS)
> «Liquida con 78% de descuento, solo hoy.»

Es el SMS real ya probado (ver `docs/pruebas-msg-directos-2026-10-30.md`); se deja
constancia porque C y D son primos: mismo esqueleto «paga hoy o te va peor», uno con
amenaza y otro con zanahoria. El tipo nuevo debería cazar los dos.

## Qué no se encontró (honesto)

- Capturas textuales recientes con el mensaje foto por foto: viven en publicaciones
  cerradas de Facebook/WhatsApp o en notas que las describen sin citarlas completas.
- Ninguna fuente oficial publica el texto íntegro; publican el patrón. Por eso todo lo
  de arriba dice «reconstruido», igual que el caso académico.

## Sugerencia

Correr A–D contra el motor y ver en qué nivel cae cada uno. Si C sale como fraude
confirmado clásico, ahí está la prueba de que `cobranza_amenazante` necesita su tipo,
como quedó anotado en las pruebas de SMS.
