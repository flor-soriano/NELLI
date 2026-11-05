# Sello de integridad (A7) truena en Windows · 31-oct-2026

Al bajar `main` en una PC con Windows, la suite quedó **29 failed, 37 passed**.
Esto es la evidencia para decidir el arreglo.

## Síntoma

Casi todo cae con lo mismo:

```
nelli.integridad.IntegridadRota: El paquete cambió sin sellar: paquete-mx/dominios-v1.json.
Revisa el diff y corre «nelli sellar».
```

`reglas.cargar()` llama `integridad.verificar()` y ahí muere, así que en Windows el motor
también se negaría a verificar mensajes, no solo las pruebas.

## Causa comprobada

Se recalculó el SHA-256 de los 14 archivos de `paquete-mx/SHA256SUMS` tal como quedaron en
disco y otra vez quitándoles el `\r` (saltos LF):

- **14 de 14 coinciden solo con LF.** Con el CRLF que mete git en Windows, ninguno.
- O sea: el paquete está intacto; el sello se selló con LF y aquí se bajó con CRLF.
  En el entorno Linux donde se selló va verde.

## Arreglos posibles

1. `.gitattributes` con `paquete-mx/*.json text eol=lf` (y lo mismo para `skills/*.md` y
   `src/nelli/esquema/*.json`) + renormalizar. Es el que menos toca.
2. Que `integridad.verificar()` normalice saltos de línea antes de hashear.
3. Sellar sobre el contenido ya normalizado en `nelli sellar`, para que el sello no
   dependa del sistema donde se baja.

Verificación: script que compara hash crudo vs hash con LF contra `SHA256SUMS`
(14/14 solo-LF). La suite en Windows no puede quedar verde hasta que esto se decida.
