/* Nelli · the hand-written example cards in English, same ids and shape as web/ejemplos.js.
   Shown only when the page is in English (web/idioma.js) and the server is not running; with the server on,
   the example is sent to the engine, which still answers in Spanish. Messages are made up; the domains do not exist.
   Buttons go as {id, texto} so the front recognises them without the Spanish labels. */
(function () {
  'use strict';

  var ROJOS = [
    { id: 'reportar', texto: 'Report' }, { id: 'bloquear', texto: 'Block' },
    { id: 'confianza', texto: 'Ask someone you trust' }, { id: 'ya_cai', texto: 'I already fell for it, what now?' },
    { id: 'blindar', texto: 'Shield my account in 7 minutes' }
  ];
  var OTROS = ROJOS.slice(0, 4);
  var TITULOS = ['Who is behind it?', 'What does it ask you to do?', 'Does what it says hold up?', 'Where does the link take you?', 'What do others say?'];
  var SIN_REPORTES = ['no_revisado', "Couldn't check: no reports at hand in this version."];
  var LICENCIA = { revisado_contra: ['hand-written example for the prototype, not checked by the engine'], ia: '—', no_pude_ver: [] };

  function puntos(lista) {
    return lista.map(function (p, i) { return { n: i + 1, titulo: TITULOS[i], estado: p[0], texto: p[1] }; });
  }

  function confianza(etiqueta) {
    return 'Hey, I got this message and Nelli flagged it as “' + etiqueta + '”. What do you think? Don’t open the link.';
  }

  window.NELLI_EJEMPLOS_EN = [
    {
      id: 'multa-falsa', nombre: 'Fake traffic ticket', estante: 'Asks for data', canal: 'sms',
      mensaje: 'SSPC NOTICE: You have a pending traffic fine of $1,850. Avoid surcharges by paying TODAY at multas-sspc-mx.info/pago with your card (number and CVV).',
      tarjeta: {
        nivel: 'fraude_confirmado', etiqueta: 'Confirmed scam', tipo: 'multa_falsa', tipo_nombre: 'Fake fine or ticket',
        puntos: puntos([
          ['alerta', 'It claims to be the SSPC, but the link is not a government page.'],
          ['alerta', 'It asks for: your card details (number and CVV). In a hurry.'],
          ['alerta', 'No authority will ever ask for full bank card numbers, CVV codes, PINs, passwords or verification codes.'],
          ['alerta', 'hxxps://multas-sspc-mx[.]info/pago. Government pages end in gob.mx; this one does not.'],
          SIN_REPORTES
        ]),
        paso: "Don't pay through the link. Look up your plate on your city or state's official finance website.",
        botones: ROJOS,
        mensaje_confianza: confianza('Confirmed scam'),
        ya_cai: 'If you paid, keep the receipt and ask your bank to trace the transfer. Check the real fine on the official site.',
        fuente_verificada: { institucion: 'SSPC / Guardia Nacional (federal security ministry)', fuente: 'https://www.gob.mx/sspc/prensa/la-sspc-emite-recomendaciones-ante-mensajes-falsos-sobre-multas-de-transito' },
        ligas_desactivadas: ['multas-sspc-mx[.]info/pago'],
        licencia: LICENCIA
      }
    },
    {
      id: 'hola-mama', nombre: '“Hi Mom, I changed my number”', canal: 'whatsapp',
      mensaje: "Hi Mom, it's me, I dropped my phone and this is my new number. I need you to deposit $3,500 today, I'll explain later, please don't tell anyone.",
      tarjeta: {
        nivel: 'muy_probablemente_fraude', etiqueta: 'Very likely a scam', tipo: 'familiar_en_apuro', tipo_nombre: 'Relative in trouble / “hi mom” / virtual kidnapping',
        puntos: puntos([
          ['alerta', "It claims to be your son or daughter, but writes from a number you didn't have."],
          ['alerta', 'It asks for: a $3,500 deposit. In a hurry.'],
          ['alerta', 'Someone who changes number and asks for money in a hurry is almost always posing as your relative.'],
          ['ok', 'No link.'],
          SIN_REPORTES
        ]),
        paso: "Hang up or don't reply. Call the person at their usual number.",
        botones: ROJOS,
        mensaje_confianza: confianza('Very likely a scam'),
        ya_cai: 'Warn your family. If you deposited, ask your bank to trace the transfer and file a report.',
        fuente_verificada: null, ligas_desactivadas: [], licencia: LICENCIA
      }
    },
    {
      id: 'venta-falsa', nombre: 'Sale with a deposit by bank transfer', estante: 'Sale offer', canal: 'feed',
      mensaje: 'CLEARANCE! Brand-new iPhone 15 Pro in the box for only $3,900. 3 left. Reserve it with a $1,000 transfer and I ship it today. Message me.',
      tarjeta: {
        nivel: 'muy_probablemente_fraude', etiqueta: 'Very likely a scam', tipo: 'compra_venta', tipo_nombre: 'Sale with an up-front deposit',
        puntos: puntos([
          ['no_revisado', "It claims to be a store on social media. I couldn't confirm who posts it."],
          ['alerta', 'It asks for: a $1,000 deposit by transfer before you receive anything. In a hurry.'],
          ['alerta', 'A seller who only takes deposits and rushes you almost always disappears after the payment.'],
          ['ok', 'No link.'],
          SIN_REPORTES
        ]),
        paso: "Don't pay a deposit. Pay on delivery or through a platform with buyer protection.",
        botones: ROJOS,
        mensaje_confianza: confianza('Very likely a scam'),
        ya_cai: 'Keep screenshots and the receipt; report it on the platform and to the Cyber Police.',
        fuente_verificada: null, ligas_desactivadas: [], licencia: LICENCIA
      }
    },
    {
      id: 'paquete', nombre: 'Package notice with a link', estante: 'Information', canal: 'sms',
      mensaje: 'Your package could not be delivered due to an incomplete address. Update your details here: entrega-rapida-mx.shop/r/8812',
      tarjeta: {
        nivel: 'posible_fraude', etiqueta: 'Possible scam', tipo: 'paqueteria', tipo_nombre: 'Held package / delivery',
        puntos: puntos([
          ['no_revisado', "It claims to be a courier, without saying which. I couldn't confirm who sent it."],
          ['alerta', 'It asks for: opening a link.'],
          ['alerta', 'Couriers do not charge “customs” or “incomplete address” fees through a link in a message.'],
          ['alerta', 'hxxps://entrega-rapida-mx[.]shop/r/8812. Not from any courier on the official list.'],
          SIN_REPORTES
        ]),
        paso: "Don't pay anything through the link. If you're expecting a package, track it with your tracking number on the courier's official site.",
        botones: OTROS,
        mensaje_confianza: confianza('Possible scam'),
        ya_cai: 'If you paid by card, call the bank to block it. Keep a screenshot of the message to report it.',
        fuente_verificada: null, ligas_desactivadas: ['entrega-rapida-mx[.]shop/r/8812'], licencia: LICENCIA
      }
    },
    {
      id: 'sin-senales', nombre: 'Order notice with no links', canal: 'sms',
      mensaje: 'Your order 4471 is on its way. It arrives between November 3 and 5. Thank you for your purchase.',
      tarjeta: {
        nivel: 'sin_senales_claras', etiqueta: 'No clear signs', tipo: 'ninguno', tipo_nombre: 'No type',
        resumen: "I found nothing odd. That doesn't mean it's trustworthy.",
        puntos: puntos([
          ['no_revisado', "It claims to be a store, without saying which. I couldn't confirm who sent it."],
          ['ok', 'It asks for: nothing.'],
          ['no_revisado', "Couldn't check: no official source at hand for this case."],
          ['ok', 'No link.'],
          SIN_REPORTES
        ]),
        paso: 'If it asks for money or data, confirm another way before doing anything.',
        botones: OTROS,
        mensaje_confianza: confianza('No clear signs'),
        ya_cai: 'Keep screenshots, change passwords and tell someone you trust.',
        fuente_verificada: null, ligas_desactivadas: [], licencia: LICENCIA
      }
    },
    {
      id: 'banco-falso', nombre: 'Fake bank asking to validate data', estante: 'Bank', canal: 'whatsapp',
      mensaje: 'BBVA: Your account will be blocked today. Validate your details at bbva-clientes-mx.com/validar to avoid the block.',
      tarjeta: {
        nivel: 'fraude_confirmado', etiqueta: 'Confirmed scam', tipo: 'banco_phishing', tipo_nombre: 'Fake bank notice',
        puntos: puntos([
          ['alerta', 'It claims to be BBVA, but the link is not bbva.mx.'],
          ['alerta', 'It asks for: validating your details, in a hurry.'],
          ['alerta', 'BBVA never asks for data, PIN, password or CVV by message or link.'],
          ['alerta', 'hxxps://bbva-clientes-mx[.]com/validar imitates the brand; it is not the official domain.'],
          SIN_REPORTES
        ]),
        paso: "Don't open the link. Open your bank's app or call the number on your card.",
        botones: ROJOS, mensaje_confianza: confianza('Confirmed scam'),
        ya_cai: 'Call your bank at the number on your card, ask them to block, and change your password from the official app.',
        fuente_verificada: { institucion: 'BBVA Mexico', dominio_oficial: 'bbva.mx' },
        ligas_desactivadas: ['bbva-clientes-mx[.]com/validar'], licencia: LICENCIA
      }
    },
    {
      id: 'empleo-falso', nombre: 'Easy job that asks you to write now', estante: 'Job', canal: 'feed',
      mensaje: 'Earn $800 a day from your phone, no experience needed. Just write now to save your spot and start today.',
      tarjeta: {
        nivel: 'posible_fraude', etiqueta: 'Possible scam', tipo: 'empleo_falso', tipo_nombre: 'Too-easy job',
        puntos: puntos([
          ['no_revisado', "It claims to be a company, but doesn't say which or where."],
          ['alerta', 'It asks for: writing right now, in a hurry, for a high salary with no requirements.'],
          ['alerta', "A real job names the company, the position and the place; it doesn't rush you by message."],
          ['ok', 'No link.'],
          SIN_REPORTES
        ]),
        paso: "Don't continue the conversation or send documents. Look up the company on your own, outside the post.",
        botones: OTROS, mensaje_confianza: confianza('Possible scam'),
        ya_cai: "Stop replying and don't send money or documents; tell someone you trust.",
        fuente_verificada: null, ligas_desactivadas: [], licencia: LICENCIA
      }
    },
    {
      id: 'premio-falso', nombre: 'Prize from a raffle you never entered', estante: 'Prize', canal: 'sms',
      mensaje: 'CONGRATULATIONS! Your number was chosen and you won an iPhone 15. Claim your prize today by paying only $99 shipping here: premio-iphone-mx.lat/reclama',
      tarjeta: {
        nivel: 'muy_probablemente_fraude', etiqueta: 'Very likely a scam', tipo: 'premio', tipo_nombre: 'Fake prize',
        puntos: puntos([
          ['alerta', "It says your number “was chosen”, but doesn't say who runs the raffle or when you entered."],
          ['alerta', 'It asks for: paying $99 “shipping” through a link. In a hurry: “claim today”.'],
          ['alerta', "A real prize doesn't charge you up front to deliver it."],
          ['alerta', 'hxxps://premio-iphone-mx[.]lat/reclama. Not the site of any known store.'],
          SIN_REPORTES
        ]),
        paso: "Don't pay or give your details. Delete the message and warn your family that it's going around.",
        botones: ROJOS,
        mensaje_confianza: confianza('Very likely a scam'),
        ya_cai: 'If you paid, call your bank to trace the charge and keep a screenshot of the message to report it.',
        fuente_verificada: null, ligas_desactivadas: ['premio-iphone-mx[.]lat/reclama'], licencia: LICENCIA
      }
    },
    {
      id: 'prestamo-facil', nombre: 'Easy loan that asks for an advance', estante: 'Loan', canal: 'feed',
      mensaje: 'Need money fast? We lend you $5,000 TODAY, no credit check, no proof of income. Just deposit $250 for “processing fees” and you have your loan in 1 hour. Reply YES and we help you.',
      tarjeta: {
        nivel: 'muy_probablemente_fraude', etiqueta: 'Very likely a scam', tipo: 'montadeudas', tipo_nombre: 'Easy loan / loan-shark scam',
        puntos: puntos([
          ['no_revisado', "It claims to be a lender with “no credit check”. I couldn't confirm it is registered."],
          ['alerta', 'It asks for: a $250 deposit for “processing fees” before lending. In a hurry: “TODAY”, “in 1 hour”.'],
          ['alerta', 'No serious lender charges you up front: any fee comes out of the loan itself.'],
          ['ok', 'No link.'],
          SIN_REPORTES
        ]),
        paso: "Don't deposit anything. If you need money, go to a branch or look the lender up in the CONDUSEF registry (Mexico's financial consumer agency).",
        botones: ROJOS,
        mensaje_confianza: confianza('Very likely a scam'),
        ya_cai: "Don't pay any more “processing” or “release” fees. Keep your receipts and report it to the Cyber Police.",
        fuente_verificada: null, ligas_desactivadas: [], licencia: LICENCIA
      }
    },
    {
      id: 'no-pude', nombre: "Screenshot that can't be read", soloEjemplo: true,
      mensaje: '(a blurry screenshot)',
      tarjeta: {
        nivel: 'no_pude_revisar', etiqueta: "I couldn't check it", tipo: 'ninguno',
        resumen: "The screenshot came out too blurry and I couldn't read the message. I'd rather not guess.",
        puntos: [],
        paso: 'Send the text of the message or a clearer screenshot. If it asks for money or data, confirm another way.',
        botones: [{ id: 'confianza', texto: 'Ask someone you trust' }],
        mensaje_confianza: "Hey, I got a message and I don't know if it's real. Can you help me check it? Don't open the link.",
        licencia: LICENCIA
      }
    }
  ];

  // Marca cada tarjeta como inglesa: así «Escuchar el resultado» usa la voz en inglés del teléfono
  window.NELLI_EJEMPLOS_EN.forEach(function (e) { e.tarjeta.idioma = 'en'; });
})();
