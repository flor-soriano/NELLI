# Pruebas con un caso académico · 30-oct-2026 (anónimo)

Origen: un caso académico: presentaciones escolares sobre fraude por mensaje, hechas por alumnos para sus mamás y abuelos, que cubren todos los ámbitos (banco, préstamos, premios). Las capturas originales traían nombres de alumnos (**nunca** al repo ni al video) y sus copias locales se borraron. De ahí se extrajeron los hechos, sin nombres, y se reconstruyó el mensaje tal como le llegó a la víctima. Esto **no** es la prueba ciega D8 ni piloto con menores: es material real para probar el motor.

## Casos reconstruidos (con IA real, Spark 1.3)

| # | Hecho real (anónimo) | Mensaje reconstruido | Resultado Nelli | Decidió |
|---|---|---|---|---|
| A | Correo falso del «banco» pidió contraseña y CVV; le quitaron $1,700 de la tarjeta | «Confirma tu contraseña y el CVV» + liga falsa, por correo | **Fraude confirmado** (banco_phishing) | Reglas |
| B | Página de Facebook «pagamos todas tus deudas»: datos + $5,000 de enganche; luego amenaza de buró por $15,000 | Post de feed con datos, depósito y amenaza de buró | **Muy probablemente es fraude** (préstamo fácil / montadeudas) | Reglas |
| C | La mamá recibe mensajes que parecen de bancos/tiendas/Telcel; una vez creyó que se ganó un iPhone | SMS «Te ganaste un iPhone, reclama hoy» + liga | **Muy probablemente es fraude** (premio) | **IA subió el nivel** |

3/3 en el nivel correcto. En C se ve el diseño funcionando: las reglas vieron señales sueltas y Spark subió a «muy probablemente» explicando por qué.

## Hallazgos (deuda, para antes de congelar reglas en D6)

1. **Contenido educativo marcado «Posible fraude»:** el manual de un alumno (captura) salió `Posible fraude` por `presion: «inmediatamente»` («No abrir **inmediatamente** los enlaces») + `banco: «tarjeta»`. Las reglas no distinguen negación ni contexto educativo. No es «Fraude confirmado» (bien), pero un post educativo en el feed no debería ni llegar a «Posible». Candidato: contexto de negación en señales de presión. No se «arregla» con lista de palabras educativas: un fraude podría disfrazarse de guía.
2. **Atribución genérica de banco:** en A, punto 1 dice «la liga no es de Hey Banco» cuando el mensaje solo dice «BANCO» a secas. La marca genérica no debería atribuirse a un banco concreto.

## Qué más sirve de las presentaciones (sin copiar texto)

- Las víctimas reales son mamás y abuelos; los alumnos ya les hicieron manuales y los entendieron. Nelli habla ese mismo idioma: 5 puntos, un paso, sin tecnicismos. Validación de tono, no de motor.
- Fuentes que los alumnos verificaron: INAI, Meta (evitar estafas), Google (phishing), CONDUSEF y una secretaría de seguridad municipal. Coinciden con el paquete MX.
- El paso «pregunta la palabra clave a tu familia» de Blindar conecta con el «hola mamá» del caso C.

Costo de la sesión: USD 0.0425 acumulado de 100 (`nelli costos`).
