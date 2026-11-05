# Piel de Nelli · Parte A — identidad propia e inconfundible

**Regla madre:** Nelli se reconoce sin decir Facebook ni WhatsApp. Si una pantalla
podría confundirse con una de Meta, está mal, aunque funcione. Sin permiso escrito
de Meta no se copia su piel: ni su azul, ni su verde, ni sus burbujas, ni su feed.

## La marca

- **Nombre:** Nelli (náhuatl: verdad, lo verificado). Solo «Nelli», nunca
  «Nelli de Meta / para WhatsApp» como nombre.
- **Logotipo:** el oficial, en grafito y blanco con el rombo menta (`web/logotipo-*.png`,
  `web/icono-*.png`). El sello en 3D (`web/sello-3d.png`) va solo en el video y la insignia.
  Es un sello de verificación, no un escudo de banco ni un logo de red social.
- **Lema:** «Verifica antes de creer, comprar o contestar.»

## Color (grafito, blanco y menta — nunca la piel de otro)

| Token | Valor | Uso |
|---|---|---|
| `--grafito` / `--tinta` | `#15191D` | Fondo del logotipo, botones, bordes fuertes, chips activos |
| `--menta` | `#4fdfa3` | El rombo del logotipo: acento, nunca fondo |
| `--fondo` | `#f2f4f7` | Fondo de página (modo claro; el modo oscuro invierte los tokens en `web/nelli.css`) |
| `--superficie` | `#ffffff` | Tarjetas y superficies |
| `--accion` | `var(--tinta)` | Botón principal (grafito, no rojo de alerta) |
| `--ambar` | `#b45309` | Avisos y detalles |
| `--nivel-*` | rojo/ámbar/gris | Solo niveles de riesgo. **Nunca verde** (verde diría «seguro») |

Prohibido: azul Facebook `#1877f2`, verde WhatsApp `#25d366`, degradados
azul-morado, burbujas de mensajes verde/beige, barra superior azul o verde.

## Letra

- Titulares y cuerpo: letra del sistema (`system-ui`), sin fuentes de internet:
  funciona sin conexión y no llama a servidores de nadie.
- Cuerpo grande (21 px) y botones de 64 px, pensados para manos y vistas cansadas.

## Forma

- Tarjeta con filete superior grueso en tinta/ámbar (como un expediente sellado),
  no tarjeta flotante genérica de app.
- El letrero de no afiliación es un **sello**, no una pastilla gris: borde
  discontinuo ámbar, mayúsculas, «Prototipo no afiliado — no es un producto
  de Meta / Unaffiliated prototype — not a Meta product». Visible siempre,
  integrado al diseño, no escondido.

## El feed es concepto Nelli

El feed no imita el de Facebook: sin «Me gusta · Comentar · Compartir» de otra
red, sin avatares de red social como identidad. Es el escaparate de Nelli:
publicaciones de ejemplo con su aviso ámbar y su botón **Verificar** en grafito.
Si mañana entra a una red real, será por la vía oficial y con su permiso.

## Crédito a Meta (sin piel de Meta)

Se nombra con texto, nunca con su logo ni sus colores:
«Hecho con la Meta Model API (Muse Spark)» / «Built with the Meta Model API».
Front y piel son propios: sin logos, colores ni activos de Meta, para no
interferir con sus términos.
