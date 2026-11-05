# web/ · tarjeta web pública y pantallas compartidas

| Archivo | Qué es |
|---|---|
| `index.html` | Revisar un mensaje: cuadro para pegar texto o liga, «¿Por dónde te llegó?», subir captura o nota de voz, y la tarjeta. Aviso visible antes de revisar: «no se abre la liga en un navegador, no se guarda tu mensaje y nadie te va a cobrar». |
| `blindar.html` | Blindar mi cuenta en 7 minutos: los 7 pasos, avance guardado solo en el aparato e insignia al terminar (hecha con Muse Image). |
| `manual.html` | Manual sencillo de uso, en una sola página, para leer o imprimir. |
| `tarjeta.js` | Dibuja la tarjeta del motor (`src/nelli/tarjeta.py`) para web/ y feed/: etiqueta, 5 puntos, un paso, fuente oficial, ligas desactivadas, botones y licencia. Todo entra como texto, nunca como HTML. Abre la tarjeta encima en el feed (`Nelli.abrirTarjeta`) y llama a `POST /api/verificar` (`Nelli.verificar`). Mantiene `NelliTarjeta.render(el, t)`. |
| `ejemplos.js` | 10 tarjetas escritas a mano con la forma del motor. Solo se enseñan si el servidor no está prendido, con la nota «Ejemplo escrito a mano». Con servidor, el ejemplo se manda al motor. |
| `ejemplos-en.js` | Las mismas 10 tarjetas en inglés, con los mismos identificadores. Se usan cuando la página está en «English». |
| `tema.js` | Modo claro (por defecto) y oscuro (automático si el teléfono lo tiene, o con el botón). Guarda la elección en el aparato; `?tema=oscuro` o `?tema=claro` fuerzan un modo. |
| `idioma.js` | Botón «English / Español». El español es lo escrito en el HTML; el inglés sale de un diccionario por clave (`data-t`, `data-t-placeholder`, `data-t-aria`, `data-t-alt`, `data-t-content`). Guarda la elección en el aparato; `?idioma=en` o `?idioma=es` fuerzan un idioma. Las tarjetas del motor real siguen en español y en inglés se avisa arriba de la tarjeta. |
| `nelli.css` | Colores y letra: grafito, blanco y el menta del logotipo como acento; rojo, ámbar oscuro, ámbar y gris por nivel. Nunca verde ni porcentajes. Letra del sistema (sin servidor de fuentes), 21 px de base y botones de 64 px. |
| `logotipo-*.png`, `icono-*.png`, `nelli-logo.svg`, `sello-3d.png`, `insignia-blindar.png` | Logotipo oficial en grafito y blanco, icono, sello en 3D e insignia (la insignia, con Muse Image). |
| `ejemplo-tarjeta.json` | Salida real del motor (demo del día 1). |

Las páginas usan rutas `../web/...` para que funcionen igual con doble clic que con `python -m nelli.servidor` (que sirve `/web/*` y `/feed/*`). Probado a 390 px de ancho, en los dos idiomas y los dos modos.
