/* Nelli · tarjetas de ejemplo escritas a mano, con la misma forma que devuelve el motor (src/nelli/tarjeta.py).
   Se enseñan solo cuando el servidor no está prendido (página abierta con doble clic, o sin conexión), y siempre con
   la nota «ejemplo escrito a mano». Con servidor, el ejemplo se manda al motor y se pinta su tarjeta real.
   Los mensajes son inventados y sus dominios no existen (revisado el 29-oct-2026). Paso, prueba y «ya caí» salen de
   paquete-mx/plantillas-v2.json; la frase de la SSPC sale de paquete-mx/nunca-v2.json (fila sspc-datos, verificada). */
(function () {
  'use strict';

  var ROJOS = ['Reportar', 'Bloquear', 'Pregúntale a alguien de confianza', 'Ya caí, ¿qué hago?', 'Blindar mi cuenta en 7 minutos'];
  var OTROS = ROJOS.slice(0, 4);
  var TITULOS = ['¿Quién está detrás?', '¿Qué te pide hacer?', '¿Se sostiene lo que dice?', '¿A dónde te lleva la liga?', '¿Qué dicen los demás?'];
  var SIN_REPORTES = ['no_revisado', 'No pude revisar: sin reportes a la mano en esta versión.'];
  var LICENCIA = { revisado_contra: ['ejemplo escrito a mano para el prototipo, no lo revisó el motor'], ia: '—', no_pude_ver: [] };

  function puntos(lista) {
    return lista.map(function (p, i) { return { n: i + 1, titulo: TITULOS[i], estado: p[0], texto: p[1] }; });
  }

  function confianza(etiqueta) {
    return 'Oye, me llegó este mensaje y Nelli lo marcó como «' + etiqueta + '». ¿Tú qué opinas? No abras la liga.';
  }

  window.NELLI_EJEMPLOS = [
    {
      id: 'multa-falsa', nombre: 'Multa de tránsito falsa', estante: 'Petición de datos', canal: 'sms',
      mensaje: 'SSPC AVISO: Tiene una multa de tránsito pendiente por $1,850. Evite recargos pagando HOY en multas-sspc-mx.info/pago con su tarjeta (número y CVV).',
      tarjeta: {
        nivel: 'fraude_confirmado', etiqueta: 'Fraude confirmado', tipo: 'multa_falsa', tipo_nombre: 'Multa o infracción falsa',
        puntos: puntos([
          ['alerta', 'Dice ser la SSPC, pero la liga no es una página del gobierno.'],
          ['alerta', 'Te pide: datos de tu tarjeta (número y CVV). Con prisa.'],
          ['alerta', 'Ninguna autoridad solicitará números completos de tarjetas bancarias, códigos CVV, NIP, contraseñas o códigos de verificación.'],
          ['alerta', 'hxxps://multas-sspc-mx[.]info/pago. Las páginas del gobierno terminan en gob.mx; esta no.'],
          SIN_REPORTES
        ]),
        paso: 'No pagues por la liga. Consulta tu placa en la página oficial de finanzas de tu ciudad o estado.',
        botones: ROJOS,
        mensaje_confianza: confianza('Fraude confirmado'),
        ya_cai: 'Si pagaste, guarda el comprobante y pide a tu banco rastrear la transferencia. Consulta la multa real en la página oficial.',
        fuente_verificada: { institucion: 'SSPC / Guardia Nacional', fuente: 'https://www.gob.mx/sspc/prensa/la-sspc-emite-recomendaciones-ante-mensajes-falsos-sobre-multas-de-transito' },
        ligas_desactivadas: ['multas-sspc-mx[.]info/pago'],
        licencia: LICENCIA
      }
    },
    {
      id: 'hola-mama', nombre: '«Hola mamá, cambié de número»', canal: 'whatsapp',
      mensaje: 'Hola mamá, soy yo, se me cayó el cel y este es mi número nuevo. Necesito que me hagas un depósito de $3,500 hoy, luego te explico, porfa no le digas a nadie.',
      tarjeta: {
        nivel: 'muy_probablemente_fraude', etiqueta: 'Muy probablemente es fraude', tipo: 'familiar_en_apuro', tipo_nombre: 'Familiar en apuro / «hola mamá» / secuestro virtual',
        puntos: puntos([
          ['alerta', 'Dice ser tu hijo o tu hija, pero escribe desde un número que no tenías.'],
          ['alerta', 'Te pide: un depósito de $3,500. Con prisa.'],
          ['alerta', 'Quien cambia de número y pide dinero con prisa casi siempre es alguien que se hace pasar por tu familiar.'],
          ['ok', 'No trae liga.'],
          SIN_REPORTES
        ]),
        paso: 'Cuelga o no contestes. Llama a la persona a su número de siempre.',
        botones: ROJOS,
        mensaje_confianza: confianza('Muy probablemente es fraude'),
        ya_cai: 'Avisa a tu familia. Si depositaste, pide a tu banco rastrear la transferencia y denuncia.',
        fuente_verificada: null, ligas_desactivadas: [], licencia: LICENCIA
      }
    },
    {
      id: 'venta-falsa', nombre: 'Venta con apartado por transferencia', estante: 'Oferta-venta', canal: 'feed',
      mensaje: '¡REMATE! iPhone 15 Pro nuevo en caja a solo $3,900. Quedan 3. Apártalo con $1,000 por transferencia y te lo mando hoy mismo. Mándame mensaje.',
      tarjeta: {
        nivel: 'muy_probablemente_fraude', etiqueta: 'Muy probablemente es fraude', tipo: 'compra_venta', tipo_nombre: 'Compra-venta con anticipo',
        puntos: puntos([
          ['no_revisado', 'Dice ser una tienda en redes. No pude confirmar quién lo publica.'],
          ['alerta', 'Te pide: un anticipo de $1,000 por transferencia antes de recibir nada. Con prisa.'],
          ['alerta', 'Un vendedor que solo acepta anticipo y mete prisa casi siempre desaparece después del pago.'],
          ['ok', 'No trae liga.'],
          SIN_REPORTES
        ]),
        paso: 'No des anticipo. Paga contra entrega o por una plataforma con protección al comprador.',
        botones: ROJOS,
        mensaje_confianza: confianza('Muy probablemente es fraude'),
        ya_cai: 'Guarda capturas y comprobante; repórtalo en la plataforma y en la Policía Cibernética.',
        fuente_verificada: null, ligas_desactivadas: [], licencia: LICENCIA
      }
    },
    {
      id: 'paquete', nombre: 'Aviso de paquete con liga', estante: 'Información', canal: 'sms',
      mensaje: 'Tu paquete no pudo ser entregado por dirección incompleta. Actualiza tus datos aquí: entrega-rapida-mx.shop/r/8812',
      tarjeta: {
        nivel: 'posible_fraude', etiqueta: 'Posible fraude', tipo: 'paqueteria', tipo_nombre: 'Paquete retenido / envío',
        puntos: puntos([
          ['no_revisado', 'Dice ser una paquetería, sin decir cuál. No pude confirmar quién lo mandó.'],
          ['alerta', 'Te pide: abrir una liga.'],
          ['alerta', 'Las paqueterías no cobran «aduana» ni «dirección incompleta» por una liga en un mensaje.'],
          ['alerta', 'hxxps://entrega-rapida-mx[.]shop/r/8812. No es de ninguna paquetería de la lista oficial.'],
          SIN_REPORTES
        ]),
        paso: 'No pagues nada por la liga. Si esperas un paquete, rastrea con tu número de guía en la página oficial de la paquetería.',
        botones: OTROS,
        mensaje_confianza: confianza('Posible fraude'),
        ya_cai: 'Si pagaste con tarjeta, llama al banco para bloquearla. Guarda la captura del mensaje para reportar.',
        fuente_verificada: null, ligas_desactivadas: ['entrega-rapida-mx[.]shop/r/8812'], licencia: LICENCIA
      }
    },
    {
      id: 'sin-senales', nombre: 'Aviso de pedido sin ligas', canal: 'sms',
      mensaje: 'Tu pedido 4471 ya va en camino. Llega entre el 3 y el 5 de noviembre. Gracias por tu compra.',
      tarjeta: {
        nivel: 'sin_senales_claras', etiqueta: 'No vemos señales claras', tipo: 'ninguno', tipo_nombre: 'Sin tipo',
        resumen: 'No encontré nada raro. Eso no quiere decir que sea de confianza.',
        puntos: puntos([
          ['no_revisado', 'Dice ser una tienda, sin decir cuál. No pude confirmar quién lo mandó.'],
          ['ok', 'Te pide: no pide nada.'],
          ['no_revisado', 'No pude revisar: sin una fuente oficial a la mano para este caso.'],
          ['ok', 'No trae liga.'],
          SIN_REPORTES
        ]),
        paso: 'Si te pide dinero o datos, confirma por otro lado antes de hacer nada.',
        botones: OTROS,
        mensaje_confianza: confianza('No vemos señales claras'),
        ya_cai: 'Guarda capturas, cambia contraseñas y avisa a alguien de confianza.',
        fuente_verificada: null, ligas_desactivadas: [], licencia: LICENCIA
      }
    },
    {
      id: 'banco-falso', nombre: 'Banco falso que pide validar datos', estante: 'Banco', canal: 'whatsapp',
      mensaje: 'BBVA: Tu cuenta sera bloqueada hoy. Valida tus datos en bbva-clientes-mx.com/validar para evitar el bloqueo.',
      tarjeta: {
        nivel: 'fraude_confirmado', etiqueta: 'Fraude confirmado', tipo: 'banco_phishing', tipo_nombre: 'Aviso falso de banco',
        puntos: puntos([
          ['alerta', 'Dice ser BBVA, pero la liga no es bbva.mx.'],
          ['alerta', 'Te pide: validar datos con prisa.'],
          ['alerta', 'BBVA nunca solicita datos, NIP, contrasena o CVV por mensaje o liga.'],
          ['alerta', 'hxxps://bbva-clientes-mx[.]com/validar imita la marca, no es el dominio oficial.'],
          SIN_REPORTES
        ]),
        paso: 'No entres a la liga. Abre tu app del banco o llama al numero de tu tarjeta.',
        botones: ROJOS, mensaje_confianza: confianza('Fraude confirmado'),
        ya_cai: 'Llama a tu banco desde tu tarjeta, pide bloqueo y cambia tu contrasena desde la app oficial.',
        fuente_verificada: { institucion: 'BBVA Mexico', dominio_oficial: 'bbva.mx' },
        ligas_desactivadas: ['bbva-clientes-mx[.]com/validar'], licencia: LICENCIA
      }
    },
    {
      id: 'empleo-falso', nombre: 'Trabajo facil que pide escribir ya', estante: 'Empleo', canal: 'feed',
      mensaje: 'Gana $800 al dia desde tu celular, sin experiencia. Solo escribe ahora para apartar tu lugar y empezar hoy mismo.',
      tarjeta: {
        nivel: 'posible_fraude', etiqueta: 'Posible fraude', tipo: 'empleo_falso', tipo_nombre: 'Empleo demasiado facil',
        puntos: puntos([
          ['no_revisado', 'Dice ser una empresa, pero no dice cual ni donde esta.'],
          ['alerta', 'Te pide: escribir ya, con prisa, por un sueldo alto sin requisitos.'],
          ['alerta', 'Un empleo real dice la empresa, el puesto y el lugar; no apura por mensaje.'],
          ['ok', 'No trae liga.'],
          SIN_REPORTES
        ]),
        paso: 'No sigas la conversacion ni mandes documentos. Busca la empresa por tu cuenta fuera de la publicacion.',
        botones: OTROS, mensaje_confianza: confianza('Posible fraude'),
        ya_cai: 'Deja de contestar y no mandes dinero ni documentos; avisa a alguien de confianza.',
        fuente_verificada: null, ligas_desactivadas: [], licencia: LICENCIA
      }
    },
    {
      id: 'premio-falso', nombre: 'Premio de un sorteo que no jugaste', estante: 'Premio', canal: 'sms',
      mensaje: '¡FELICIDADES! Tu número fue elegido y te ganaste un iPhone 15. Reclama hoy tu premio pagando solo $99 de envío aquí: premio-iphone-mx.lat/reclama',
      tarjeta: {
        nivel: 'muy_probablemente_fraude', etiqueta: 'Muy probablemente es fraude', tipo: 'premio', tipo_nombre: 'Premio falso',
        puntos: puntos([
          ['alerta', 'Dice que tu número «fue elegido», pero no dice quién hace el sorteo ni cuándo participaste.'],
          ['alerta', 'Te pide: pagar $99 de «envío» entrando a una liga. Con prisa: «reclama hoy».'],
          ['alerta', 'Un premio de verdad no te cobra por adelantado para entregártelo.'],
          ['alerta', 'hxxps://premio-iphone-mx[.]lat/reclama. No es la página de ninguna tienda conocida.'],
          SIN_REPORTES
        ]),
        paso: 'No pagues ni des tus datos. Borra el mensaje y avisa a tu familia que anda circulando.',
        botones: ROJOS,
        mensaje_confianza: confianza('Muy probablemente es fraude'),
        ya_cai: 'Si pagaste, llama a tu banco para rastrear el cargo y guarda la captura del mensaje para reportar.',
        fuente_verificada: null, ligas_desactivadas: ['premio-iphone-mx[.]lat/reclama'], licencia: LICENCIA
      }
    },
    {
      id: 'prestamo-facil', nombre: 'Préstamo fácil que pide anticipo', estante: 'Préstamo', canal: 'feed',
      mensaje: '¿Te urge dinero? Te prestamos $5,000 HOY sin buró y sin comprobar ingresos. Solo deposita $250 de «gastos de gestión» y en 1 hora tienes tu préstamo. Responde SÍ y te atendemos.',
      tarjeta: {
        nivel: 'muy_probablemente_fraude', etiqueta: 'Muy probablemente es fraude', tipo: 'montadeudas', tipo_nombre: 'Préstamo fácil / montadeudas',
        puntos: puntos([
          ['no_revisado', 'Dice ser una financiera que presta «sin buró». No pude confirmar que exista registrada.'],
          ['alerta', 'Te pide: depositar $250 de «gastos de gestión» antes de prestarte. Con prisa: «HOY», «en 1 hora».'],
          ['alerta', 'Nadie serio te cobra por adelantado para prestarte: cualquier gasto se descuenta del mismo préstamo.'],
          ['ok', 'No trae liga.'],
          SIN_REPORTES
        ]),
        paso: 'No deposites nada. Si necesitas dinero, acude a una sucursal o busca la financiera en el registro de CONDUSEF.',
        botones: ROJOS,
        mensaje_confianza: confianza('Muy probablemente es fraude'),
        ya_cai: 'No pagues más «gestorías» ni «liberaciones». Guarda tus comprobantes y denuncia en la Policía Cibernética.',
        fuente_verificada: null, ligas_desactivadas: [], licencia: LICENCIA
      }
    },
    {
      id: 'no-pude', nombre: 'Captura que no se lee', soloEjemplo: true,
      mensaje: '(una captura borrosa)',
      tarjeta: {
        nivel: 'no_pude_revisar', etiqueta: 'No pude revisarlo', tipo: 'ninguno',
        resumen: 'La captura salió muy borrosa y no pude leer el mensaje. Prefiero no adivinar.',
        puntos: [],
        paso: 'Manda el texto del mensaje o una captura más clara. Si te pide dinero o datos, confirma por otro lado.',
        botones: ['Pregúntale a alguien de confianza'],
        mensaje_confianza: 'Oye, me llegó un mensaje que no sé si es de verdad. ¿Me ayudas a revisarlo? No abras la liga.',
        licencia: LICENCIA
      }
    }
  ];
})();
