# Inspiración de interfaz (método, no copia)

Se leyeron 5 referencias el 1-nov-2026. Se toma el **método**; no se copia
ningún logo, color de marca ni texto de ellos. Nelli sigue con su piel
(tinta, papel, ladrillo, ámbar y su sello).

| Referencia | Qué hacen bien | Cómo entra en Nelli |
|---|---|---|
| [Google Safety · Autenticación](https://safety.google/intl/es_ALL/safety/authentication/) | Escudo amable al frente, secciones con icono + título + una frase, «más seguro desde el diseño» | Blindar se vuelve «Revisión de seguridad»: sello grande, cada paso con icono y una frase de por qué te cuida |
| [Microsoft Support · Códigos de verificación](https://support.microsoft.com/es-es/accounts-billing/manage/microsoft-account-security-info-verification-codes) | Pasos numerados, encabezados en lenguaje llano, avisos claros de qué nunca te pedirán | Cada paso de Blindar trae «Hazlo así» en 1-2 líneas numeradas; la regla «nadie te pide códigos» va primero |
| [INCIBE · Cuentas comprometidas](https://www.incibe.es/ciudadania/blog/cuentas-comprometidas-compruebalo) | Tono ciudadano, «compruébalo», casos reales, ayuda visible | Caja «Si ya caíste, respira»: 3 pasos inmediatos y sin culpa, en Revisar y al cerrar Blindar |
| [Bitwarden · Password strength](https://bitwarden.com/es-la/password-strength/) | Un medidor visual que responde al instante y se entiende sin saber de seguridad | La tarjeta gana un medidor por **segmentos** del nivel (sin porcentajes, como manda Nelli): se ve antes de leer |
| [Yahoo Ayuda · Verificación](https://es-us.ayuda.yahoo.com/kb/mobile-mail/Verificaci%C3%B3n-de-seguridad-en-un-dispositivo-m%C3%B3vil-sln26418.html) | Instrucciones por dispositivo, un toque por paso | Blindar dice dónde tocar en cada app («En WhatsApp: Ajustes · Cuenta · …») y cada paso se marca con un solo toque |

## Qué hace falta para estas mejoras (respuesta corta)

Nada que no exista ya en el proyecto:

- Iconos: dibujo de línea propio en SVG (ya vive en `web/tarjeta.js`), cero
  bancos de iconos de pago y cero logos de Google/Microsoft/Bitwarden/Yahoo.
- El sello en 3D ya renderizado (`video/3d/sello-3d.png`) como imagen fija y
  amable en Blindar. En la interfaz no se mueve: ilustra, no distrae.
- Colores: los de la piel. Lo «amigable» sale de radios más suaves, sombras
  cálidas, más aire y frases cortas — no de pintar Nelli de azul Google.
- Fuentes del sistema (sin internet), botones de 64 px y letra de 21 px:
  lo de `docs/diseno-mayores.md` no se negocia por «verse moderno».
