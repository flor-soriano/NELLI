# Plan D6 → D10 · Cierre Nelli (31-oct → 4-nov-2026)

> Plan escrito el 31-oct; las casillas quedan como se escribieron. Lo que de verdad pasó está en `BUILD-LOG.md`: el corpus ciego de ~600 no se construyó y en su lugar se corrió la prueba sobre 50 casos documentados (README, «Resultados»).

Entrega: **4-nov 18:00 hora del Pacífico (21:00 ET)**, cuenta registrada. Todo lleva el letrero «Unaffiliated prototype — not a Meta product»; front y piel propios.

## D6 · sáb 31-oct · Corpus y demo sólida
- [ ] Corpus ciego: ~600 casos (30% ciego, nunca vistos por quien ajusta reglas), mitad fraude / mitad legítimos difíciles. Carpeta `eval/corpus/` (ignorada por git: son mensajes de personas).
- [ ] Piloto 1 con adultos: 5 personas, tarea «reenvíale esto a Nelli», anotar dónde se traban (sin guardar mensajes reales).
- [ ] Congelar reglas: desde D6 solo se corrigen errores de crash, no patrones nuevos (si no, la prueba ciega no es ciega).

## D7 · dom 1-nov · Feed completo y video (guion)
- [ ] Feed v1: 10 publicaciones (las 4 actuales + 6), cada una con aviso y botón Verificar que abre la tarjeta real.
- [ ] Guion del video cerrado (≤3 min, subtítulos EN): 0:00 problema real (mensaje falso en WhatsApp) · 0:30 tarjeta en vivo (texto) · 1:10 captura · 1:40 nota de voz · 2:10 Blindar 7 minutos con insignia Muse Image · 2:40 cifras de la prueba ciega + «reglas deciden, la IA explica» + letrero no afiliado.
- [ ] Grabar tomas de pantalla del feed y la tarjeta propios, con el letrero no afiliado.

## D8 · lun 2-nov · Prueba ciega (una sola corrida)
- [ ] Correr UNA vez, sin reintentos: Nelli completa vs reglas solas vs Spark solo vs Scamio, sobre el corpus ciego.
- [ ] Publicar en README: fraudes escapados y legítimos marcados, con Wilson 95%. Sin cifras antes de medir.
- [ ] Si algo sale mal: se reporta tal cual. No se re-corre «para que salga mejor».

## D9 · mar 3-nov · Video y seguridad
- [ ] Video final ≤3 min, subtítulos en inglés, letrero no afiliado visible en cada toma.
- [ ] Revisión de seguridad del código completa: secretos, exposición web, OWASP del servidor. Repo pasa a **público** hoy (antes de eso: revisar que no haya .env, costos ni corpus).

## D10 · mié 4-nov · Submit
- [ ] README final con resultados D8, autoría (una sola persona registrada) y «Built with the Meta Model API» en texto, sin logos.
- [ ] Submit antes de 18:00 hora del Pacífico desde la cuenta registrada. Guardar captura del envío.
