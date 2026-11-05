# 50 casos reales documentados (30 + 20 raros) · 31-oct-2026

Objetivo: reunir al menos 30 casos reales y luego 20 más raros. Facebook no se scrapeó: serían datos de víctimas. Estos 50 salen de
alertas de policías y de CONDUSEF, prensa y documentos públicos que ya publicaron el
patrón. Los casos 31–50 son los raros/especiales, para que nada agarre en curva.

**Cómo leerlo:** «cita» = el texto salió publicado tal cual o casi; «reconstruido» = el
texto se armó siguiendo el patrón publicado (como el caso académico). Sin
nombres, sin teléfonos, sin ligas vivas: los dominios son inventados y van desarmados.
Ningún dato personal entró al repo.

## Fuentes

| Clave | Fuente | Fecha |
|---|---|---|
| F1 | Policía Cibernética Michoacán (FGE) | alerta 28-oct-2026 |
| F2 | SSC Ciudad de México | 2026 |
| F3 | InSight Crime / PVAngels (prensa) | 2022–2023, patrón vigente |
| F4 | ABM + CONDUSEF (vía prensa) | sep-2026 |
| F5 | SSPC / Guardia Nacional en gob.mx | verificada 29-oct |
| F6 | SAT y red R3D (phishing SAT, 2,262 cuentas falsas) | 2023–2024 |
| F7 | WhatsApp / INCIBE (robo por código de 6 dígitos) | vigente |
| F8 | Reportes de usuarios MX (tareas por likes) | 2024–2026 |
| F9 | CONDUSEF, fraude «transferencia retenida» (prensa) | 2026 |
| F10 | Pruebas propias (caso académico y SMS reales, anónimos) | 30-oct-2026 |
| F11 | CONDUSEF / REDECO (cobranza prohibida) | vigente |
| F12 | Alertas a pensionados (prensa/redes) | nov-2026 |
| F13 | FTC/FBI + prensa MX (voz clonada; caso Metepec) | oct-2026 |
| F14 | FTC (QR falsos «quishing») | sep-2026 |
| F15 | FBI/IC3 (toma de cuentas, alertas falsas) | 2025–2026 |
| F16 | Prensa (SpyLoan e inversión en redes) | 2024–2026 |

## Cobranza y montadeudas (1–8)

1. **Deuda inventada** (WhatsApp) · reconstruido F1+F2 — «Descargaste nuestra app y
   tienes un préstamo vencido de $2,800. Si hoy no pagas, avisamos a todos tus
   contactos que eres un ratero y les mandamos tu foto.»
2. **Amenaza directa** (WhatsApp) · cita de prensa F3, en español — «Te vamos a
   desmembrar a la familia si no pagas en 20 minutos.» (En la nota sale en inglés,
   dicho por una víctima.)
3. **Acoso a los contactos** (WhatsApp a la familia) · reconstruido F3 — «Tu familiar
   tiene una deuda con nosotros y no paga. Es un ratero. Haz que pague o les va a ir
   mal a todos.»
4. **Amenaza de embargo** (SMS) · reconstruido, patrón prohibido F11 — «ÚLTIMO AVISO.
   Su crédito está vencido. Si hoy no liquida, se procede al embargo de bienes y al
   bloqueo de sus cuentas. Despacho Jurídico Asociado.» → candidato a `cobranza_amenazante`.
5. **Descuento con prisa** (SMS) · **real, ya probado** F10 — «Liquida con
   78% de descuento, solo hoy.» Primo del 4: mismo esqueleto, zanahoria en vez de palo.
6. **Despacho que simula juzgado** (SMS/carta) · reconstruido F11 — «Quedó radicada la
   demanda en su contra, expediente 4471. Evite el embargo presentándose a pagar hoy.»
   REDECO prohíbe documentos que parezcan de un juzgado.
7. **Llamada al familiar** (llamada) · reconstruido F3/F1 — Guion: «Habla el licenciado
   de la financiera. Su hijo debe $4,000 y si en una hora no deposita, vamos a su casa.»
8. **Anuncio de préstamo fácil** (redes) · reconstruido F1/F2 — Ya vive en el feed como
   `prestamo-facil`: «Te prestamos $5,000 HOY sin buró… deposita $250 de gestión.»

## Banco, SAT y gobierno (9–16)

9. **Banco que pide CVV** (SMS) · patrón F4 — Ya vive como `banco-falso`: cargo no
   reconocido + liga para «confirmar contraseña y CVV».
10. **Transferencia retenida** (SMS) · reconstruido F9 — «Tu transferencia de $8,500
    quedó retenida por seguridad. Valida tus datos para liberarla: banca-movil-mx[.]lat»
11. **Canje de puntos** (SMS) · reconstruido F4 — «Tus 12,400 puntos vencen HOY.
    Canjéalos antes de perderlos: puntos-banco-mx[.]lat/canje»
12. **SAT: CFDI falso** (correo) · patrón F6 — «Se detectó una irregularidad en su
    facturación. Descargue el CFDI adjunto y regularice su situación.» (El adjunto es
    el gancho; el SAT identificó 2,262 cuentas falsas con este modo.)
13. **SAT: devolución falsa** (SMS/correo) · reconstruido F6 — «Tiene un saldo a favor
    de $4,230. Registre su CLABE para recibir su devolución: sat-devolucion-mx[.]lat»
    (El SAT no pide CLABE por liga.)
14. **Multa de tránsito falsa** (SMS) · **ya probado** F5/F10 — Vive como `multa-falsa`
    con fuente oficial SSPC verificada.
15. **Depósito falso a pensionados** (SMS/llamada) · reconstruido F12 — «Ya le
    depositamos su apoyo. Para liberarlo confirme los datos de su tarjeta en la
    liga.» Oleada de alertas de noviembre contra adultos mayores.
16. **Corte de luz falso** (SMS) · reconstruido, patrón frecuente en alertas estatales —
    «Su servicio será suspendido HOY por falta de pago. Pague su recibo aquí:
    cfe-pagos-mx[.]lat» (La CFE no corta el mismo día por una liga.)

## Cuentas, familia y mensajes (17–22)

17. **Robo de WhatsApp por código** (WhatsApp) · patrón F7 — «Perdón, te mandé por
    error mi código de 6 dígitos. ¿Me lo pasas?» (Con ese código se quedan la cuenta
    y luego piden dinero a los contactos haciéndose pasar por la víctima.)
18. **«Hola mamá, cambié de número»** (WhatsApp) · **ya probado** F10 — Vive como
    `hola-mama` en ejemplos y en el feed.
19. **Secuestro virtual** (llamada) · patrón SSPC, reconstruido — Guion: gritos de
    fondo, «¡Mamá, me tienen!», un «comandante» pide depósito inmediato y prohíbe
    colgar. La SSPC lo trae en sus alertas de extorsión telefónica.
20. **Familiar detenido** (llamada) · patrón de extorsión, reconstruido — «Su hijo
    tuvo un accidente y está detenido. Mande $6,000 para la fianza o se lo llevan.»
21. **Premio de sorteo** (SMS) · patrón de prensa — Ya vive como `premio-falso`:
    iPhone «ganado» pagando $99 de envío por liga.
22. **Paquete retenido** (SMS) · **ya probado** — Vive como `paquete`: dirección
    incompleta + liga que no es de ninguna paquetería oficial.

## Ventas, empleo y otros (23–27)

23. **Venta con anticipo** (redes) · **ya probado** — Vive como `venta-falsa`: remate
    de iPhone con apartado por transferencia.
24. **Empleo de dar likes** (WhatsApp → Telegram) · patrón F8 — «Gana $600 diarios
    dando likes a videos. Empiezas hoy, sin experiencia.» Luego piden «invertir» para
    liberar las ganancias: ahí está el robo.
25. **Grupo de inversión** (WhatsApp) · patrón de prensa (SpyLoan/inversión) — «Grupo
    VIP de criptomonedas: deposita $1,000 y retiras $2,000 en 24 horas. Solo hoy hay
    lugares.»
26. **Renta falsa** (redes) · patrón frecuente, reconstruido — «Depa amueblado $4,500
    ya con servicios. Hay mucha gente interesada: apártalo con $500 y mañana lo ves.»
27. **Suscripción no pagada** (SMS/correo) · patrón phishing general — «No pudimos
    cobrar tu suscripción y se cancelará hoy. Actualiza tu pago: streaming-pagos[.]lat»

## Legítimos difíciles (28–30) · para que el motor no marque de más

28. **Aviso real de Telnor** (SMS) · reconstruido como lo manda un aviso real — «Tu
    recibo Telnor ya está disponible. Consúltalo en la app o en telnor.com.» Sin liga
    en el mensaje. Es el pendiente: hoy sale marcado de más.
29. **SMS real de banco** (SMS) · patrón de aviso legítimo — «Compra aprobada por
    $1,240 en tienda con tu tarjeta terminación 4471. Si no la reconoces, llama al
    número que viene en tu tarjeta.» Sin liga y sin pedir datos.
30. **Pedido en camino** (SMS) · **ya en ejemplos** como `sin-senales` — «Tu pedido
    4471 ya va en camino. Llega entre el 3 y el 5 de noviembre.» El nivel correcto:
    «No vemos señales claras», nunca «es seguro».

## Raros y especiales (31–50) · para que nada agarre en curva

31. **Voz clonada de tu hijo** (nota de voz/llamada) · patrón F13 — Se oye igual a él:
    «Mamá, tuve un accidente, deposítame ahorita.» En octubre 2026 cayó en Metepec una
    banda que clonaba voces de funcionarios (Infobae/Milenio). **Ojo:** Nelli hoy no
    distingue voz de computadora; el paso correcto es la palabra clave de la familia
    (conecta con Blindar) y colgar para llamar al número de siempre.
32. **Secuestro virtual con video** (videollamada) · evolución del 19 — Misma llamada
    de extorsión, pero enseñando un video corto del «hijo» amarrado. Es grabado o
    generado; el guion no cambia: no deposites, cuelga, verifica por otro lado.
33. **«Instala la app de seguridad del banco»** (llamada) · patrón de soporte falso —
    «Para proteger su cuenta instale esta aplicación que le mando.» Es acceso remoto:
    ven todo lo que escribes, incluidas tus claves. Ningún banco instala cosas en tu
    teléfono por llamada.
34. **«Mueva su dinero a una cuenta segura»** (llamada) · patrón F15 — «Soy de
    fraudes de su banco: su cuenta está en riesgo, mueva todo a esta cuenta segura.»
    Ningún banco pide mover dinero a otra cuenta por teléfono. Jamás.
35. **SMS falso dentro del hilo real del banco** (SMS) · bancos lo han advertido —
    El mensaje llega en la misma conversación de siempre del banco, pero trae liga.
    Ni estar en el hilo bueno lo salva: el banco no manda ligas para «validar».
36. **QR pegado encima del bueno** (calle/restaurante) · F14 — Calcomanía con QR
    falso sobre el del parquímetro o la mesa. Al escanear pagas en una página falsa.
    La liga que abre debe ser la oficial; si no la conoces, no pagues ahí.
37. **Paquete que no pediste, con QR** (entrega) · FBI lo advirtió en 2025 — Llega
    una caja sin remitente con un QR «para ver quién te lo mandó». El QR lleva a una
    página que pide tus datos o tu tarjeta.
38. **Sextorsión montadeudas** (WhatsApp a contactos) · F3 — Editan la foto de la
    víctima con letreros de «ratero» o cosas peores y la mandan a sus contactos si
    no paga. Ya hubo detenidos en CDMX por redes de apps así.
39. **Tareas que suben de nivel** (Telegram) · evolución del caso 24 — «Ya ganaste
    $300. Para retirarlos sube a nivel VIP depositando $500.» Cada nivel pide más;
    las «ganancias» nunca salen.
40. **Romance que termina en inversión** (redes/WhatsApp) · patrón de prensa —
    Semanas de plática con «pareja» del extranjero y luego: «invierte conmigo en
    criptomonedas, yo te enseño». La plataforma es falsa; el dinero no vuelve.
41. **Familiar varado en el extranjero** (WhatsApp) · patrón clásico — «Soy tu tía,
    estoy en España, perdí mi pasaporte y mi bolsa. Mándame para el boleto, no le
    digas a nadie.» Número nuevo, prisa y secreto: las tres juntas.
42. **Herencia del extranjero** (correo/carta) · patrón clásico — «Su pariente
    falleció y le dejó una herencia. Para liberarla pague impuestos y gastos.»
    Nadie hereda de desconocidos ni paga por recibir una herencia.
43. **Plazas de gobierno** (redes) · patrón frecuente — «Hay plazas en el IMSS y en
    la SEP. Aparta la otra versión pagando tu examen y tu curso.» Las plazas no se venden
    por mensaje ni se apartan con depósito.
44. **«Tu familiar está en el quirófano»** (llamada) · variante del 20 — «Chocó y
    está en cirugía. Deposite $9,000 a esta cuenta para operarlo ya.» Hospitales de
    urgencia no cobran así por teléfono a la familia.
45. **«Su paquete trae droga, habla la aduana»** (llamada) · extorsión — «Retenido
    un paquete a su nombre con droga. Pague la multa o se gira orden en su contra.»
    Ninguna aduana cobra multas por teléfono.
46. **«Su computadora tiene virus»** (llamada/ventana en pantalla) · soporte falso —
    «Hable a soporte para limpiarla.» Termina en acceso remoto (caso 33) o en cobro
    por un «antivirus» que no existe.
47. **Portabilidad que no pediste** (SMS) · patrón SIM — «Tu número pasará a otra
    compañía hoy. Si no fuiste tú, confirma tu identidad aquí.» Con tus datos y un
    código se quedan tu línea y luego tus cuentas.
48. **Llamada desde el número real del banco** (llamada) · el más difícil — El
    identificador enseña el número oficial del banco, pero es suplantado. Ni el
    número salva: cuelga y marca tú el de tu tarjeta.
49. **LEGÍTIMO difícil: la paquetería sí manda liga** (SMS) — Las paqueterías reales
    avisan con liga a su dominio oficial. La revisión correcta es el dominio, no
    nomás «trae liga»: si es el oficial y no pide pagos raros, es de los buenos.
50. **LEGÍTIMO difícil: el banco sí pregunta por SMS** (SMS) — «¿Reconoces la compra
    de $1,240? Responde SI o NO.» Los bancos sí confirman así. Lo que nunca hace el
    banco real: mandar liga o pedir claves en ese mismo mensaje.

## Resumen honesto

- **Con texto citado o ya probado:** 2, 5, 14, 18, 22, 23, 30 (y 9, 21,
  8 ya viven en el feed y en `web/ejemplos.js`).
- **Reconstruidos según patrón publicado:** el resto. Ninguno trae nombres,
  teléfonos ni ligas vivas.
- Los 50 cubren los tipos que el motor ya clasifica más los huecos anotados:
  `cobranza_amenazante` (4–7), el legítimo de Telnor (28) y los legítimos con liga o
  pregunta real (49–50), donde «trae liga» o «pide responder» no basta para marcar.
- El caso 31 (voz clonada) cae en el pendiente abierto: Nelli aún no distingue voz
  humana de computadora; mientras tanto el paso es palabra clave + llamar al número
  de siempre.
- Si se corren los 50, los que caigan en nivel equivocado son candidatos a
  ajuste **antes** de congelar reglas; la prueba ciega del lunes ya no se toca.
