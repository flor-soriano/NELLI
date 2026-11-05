# Diseño para todos, probado con la persona más exigente

**Nelli es seguridad para todos.** La persona de 60 a 70 años fue el ejemplo
y la prueba de fuego, no el nicho: si ella lo usa sola, lo usa cualquiera.
Nelli protege a quien menos debe pelearse con una pantalla. Si una persona de
65 años, con la vista cansada y miedo de «romper algo», no lo hace sola a la
primera, el diseño está mal — no la persona.

## Referencias revisadas (y qué se tomó)

| Referencia | Qué se tomó | Qué se descartó |
|---|---|---|
| Una plantilla web 3D pública (copia local borrada) | Degradar con elegancia (si algo falla, se ve la versión simple), una revisión final automática como idea, poster fijo en vez de invento | El 3D que gira con el scroll: distrae, marea y no verifica nada. Para este público, **cero 3D** |
| Una guía pública de movimiento y accesibilidad | Base obligatoria: foco visible 3 px, objetivos táctiles ≥44 px, un solo `h1`, etiquetas visibles, nada oculto si falla el JS, `prefers-reduced-motion` | Reveal con scroll y animaciones: aquí casi nada se mueve |
| Nelli (días anteriores) | Letra grande, nunca verde, nunca porcentajes, español de casa, sin fuentes de internet | — |

## Las 10 reglas a prueba de errores

1. **Una sola cosa por pantalla** y un solo botón principal grande. Lo demás espera.
2. **Tres caminos, con nombre de casa:** «Pegar el texto», «Subir una foto»,
   «Mandar una nota de voz». Nada de iconitos sin texto.
3. **Botones de 64 px o más**, a todo lo ancho, con verbo claro:
   «Revisar el mensaje», no «Enviar» ni «OK».
4. **Letra:** cuerpo 21 px, resultado 34 px, nada de trabajo por debajo de 16 px.
5. **Nada escondido:** sin menú hamburguesa, sin gestos, sin doble toque, sin
   pasar el dedo «de ladito». Todo lo que se puede tocar se ve.
6. **Nunca se pierde lo escrito.** «Borrar y empezar de nuevo» lo pone la
   persona, no un error ni un toque de más. Sin recargas sorpresa.
7. **Miedo fuera, por escrito:** «La liga no se abre en un navegador. Tu mensaje no
   se guarda. Nadie te va a cobrar.» — visible antes de revisar, no en letra chica.
8. **El resultado se puede escuchar:** botón «Escuchar el resultado» que lee la
   tarjeta en voz alta (voz del propio teléfono, sin servidor).
9. **Un solo paso a seguir**, primero y en grande. Y siempre a la mano:
   «Pregúntale a alguien de confianza».
10. **Errores en cristiano y junto al problema:** «Pega el mensaje o sube una
    foto para poder revisarlo», nunca códigos ni «Error 400».

## Movimiento

Nivel «sutil» de esa guía de movimiento, bajado a casi cero: sin animaciones de
entrada, sin parallax, sin objetos que se muevan solos. Si el teléfono pide
movimiento reducido, se respeta (`prefers-reduced-motion` ya está en el CSS).

## Revisión antes de entregar (checklist)

- [ ] ¿Se hace todo con el dedo gordo, sin precisión? (botones ≥64 px)
- [ ] ¿Se lee sin lentes de cerca a 40 cm? (≥21 px, contraste alto)
- [ ] ¿Hay un solo botón que manda en cada momento?
- [ ] ¿La persona puede equivocarse sin perder nada ni «romper» algo?
- [ ] ¿El resultado se entiende escuchándolo, sin leer?
