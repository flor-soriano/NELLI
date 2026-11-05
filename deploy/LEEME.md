# Despliegue de Nelli con systemd

Unidad: `nelli.service`, pensada para un servidor Linux con systemd. El servicio corre
como usuario `nelli`, escucha solo dentro del propio servidor (puerto 8000, en
la interfaz local que `nelli.servidor` usa por defecto) y lo expone el proxy
inverso del sitio con TLS. Las direcciones y nombres del servidor van en la
configuración del proxy, nunca en este repositorio.

- `/etc/nelli/nelli.env` es `0640 root:nelli` y lleva `MODEL_API_KEY`.
- `ProtectSystem=strict` deja `/opt/nelli` en solo lectura, así que el
  servicio no puede reescribir su propia verdad (A7).
- `IPAddressDeny` corta en el kernel las redes privadas y los metadatos de
  nube aunque engañen al chequeo del código (DNS rebinding).
- La interfaz local queda abierta a propósito, porque por ahí entra el proxy.
- Pon `NELLI_PROXY_CONFIANZA=<IP del proxy>` en `/etc/nelli/nelli.env` y haz que el proxy mande `X-Forwarded-For`; si no, el tope de consultas por origen cuenta a todos los usuarios como uno solo.
  Para esa interfaz, la única barrera es `check_url.es_privada`.

Verificación antes de instalar:

```bash
systemd-analyze verify deploy/nelli.service
```
