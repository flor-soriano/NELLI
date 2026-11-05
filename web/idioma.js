/* Nelli · idioma de las pantallas: español de casa por defecto, inglés con el botón «English».
   Se carga en <head>, junto a tema.js. Pone lang en <html>, guarda la elección en el aparato
   (localStorage «nelli-idioma») y acepta ?idioma=en o #idioma=es en la liga, para el video y las capturas.

   Cómo se traduce:
   - En el HTML, cada texto lleva data-t="clave"; el español es lo que está escrito y el inglés sale de EN.
     Atributos: data-t-placeholder, data-t-aria (aria-label), data-t-alt, data-t-title, data-t-content.
   - En los scripts: NelliIdioma.t('clave', 'texto en español') devuelve el inglés si está activo.
   - Las tarjetas de ejemplo en inglés viven en web/ejemplos-en.js. Las del motor real siguen en español.
   Todo el texto entra como texto, nunca como HTML. */
(function () {
  'use strict';
  var raiz = document.documentElement;
  var LLAVE = 'nelli-idioma';

  var EN = {
    /* ---- común: menú, cabecera, sello, Muse ---- */
    'menu.revisar': 'Check', 'menu.feed': 'The feed', 'menu.blindar': 'Shield my account', 'menu.manual': 'Guide',
    'menu.aria': 'Prototype screens',
    'idioma.boton.es': 'English', 'idioma.boton.en': 'Español',
    'idioma.aria.es': 'Switch to English', 'idioma.aria.en': 'Cambiar a español',
    'tema.claro': 'Light mode', 'tema.oscuro': 'Dark mode',
    'tema.aria.claro': 'Switch to light mode', 'tema.aria.oscuro': 'Switch to dark mode',
    'comun.lema': 'Check before you believe, buy or reply',
    'comun.sello': 'Unaffiliated prototype',
    'comun.muse': 'POWERED BY MUSE',
    'comun.muse.sub': 'Built with the Meta Model API · Muse Spark reads, Muse Voice listens, Muse Image illustrates',
    'comun.muse.sub.feed': 'Built with the Meta Model API (Muse Spark)',
    'comun.descripcion': 'Nelli checks suspicious messages, screenshots and voice notes and tells you in plain words whether it looks like a scam. Without opening links.',
    'comun.pie': 'Built with the Meta Model API (Muse Spark). Nelli is an independent project, not a Meta product.',
    'comun.emulador': 'Test mode without a key: the AI part is a local stand-in, not Muse. Put the Meta key in .env and the real Muse takes over.',

    /* ---- Revisar (web/index.html) ---- */
    'rev.titulo': 'Nelli · Check before you believe, buy or reply',
    'rev.calma': 'Take a breath: ',
    'rev.calma.b': 'the link is not opened in a browser, your message is not stored and nobody will charge you.',
    'rev.calma.2': ' You just bring the message; Nelli reads it with the Meta AI (Muse) and does not keep it.',
    'rev.paso1': 'Step 1 · Bring the message that worries you',
    'rev.camino.texto': 'Paste the text', 'rev.camino.texto.s': 'Copy the message and paste it below',
    'rev.camino.imagen': 'Upload a photo', 'rev.camino.imagen.s': 'A screenshot from your phone',
    'rev.camino.audio': 'Send a voice note', 'rev.camino.audio.s': 'The audio they sent you',
    'rev.paso2': 'Step 2 · Paste it here and tap the big button',
    'rev.texto.label': 'Paste the message or the link here',
    'rev.texto.placeholder': 'Paste the whole message, with the link exactly as it came',
    'rev.canal': 'Where did it come from?',
    'rev.canal.sms': 'Text message (SMS)', 'rev.canal.email': 'Email', 'rev.canal.feed': 'A social media post', 'rev.canal.otro': 'Other',
    'rev.subir': 'Upload screenshot', 'rev.voz': 'Voice note',
    'rev.revisar': 'Check the message', 'rev.borrar': 'Clear and start over',
    'rev.yacai.t': 'If you already fell for it, breathe. It can be partly and quickly fixed:',
    'rev.yacai.1b': "Don't send any more money", 'rev.yacai.1': ', even if they threaten you or you feel ashamed.',
    'rev.yacai.2b': 'Call your bank at the number on your card', 'rev.yacai.2': ' (not the one in the message) and ask them to block it.',
    'rev.yacai.3b': 'Tell someone you trust today.', 'rev.yacai.3': ' Silence is what helps the scammer most.',
    'rev.ejemplos.t': 'Examples to try',
    'rev.ejemplos.p': 'They are made-up messages. Tap one and Nelli checks it.',
    'rev.js.sinServidor': "The checker is not running: this page was opened without Nelli's server, so I did not check your message.",
    'rev.js.sinServidor.2': ' Below you can see how Nelli answers with the examples.',
    'rev.js.revisando': 'Checking, hold on a moment…',
    'rev.js.chip.voz': 'VOICE NOTE', 'rev.js.chip.cap': 'SCREENSHOT',
    'rev.js.tuCaptura': 'Your screenshot: ',
    'rev.js.listaVoz': 'Ready to listen and check.', 'rev.js.listaCap': 'Ready to read and check.',
    'rev.js.falta': 'Paste the message or upload a screenshot so I can check it.',
    'rev.js.origenVoz.1': 'I listened to your voice note “', 'rev.js.origenVoz.2': '” and checked it. Note: I still cannot tell whether the voice is human or computer-made.',
    'rev.js.origenCap.1': 'I read your screenshot “', 'rev.js.origenCap.2': '” and checked it.',
    'rev.js.escuchando': 'Listening to your note…', 'rev.js.leyendo': 'Reading your screenshot…',
    'rev.js.sinLectura': 'This version cannot read screenshots or voice notes yet. Copy and paste the text of the message.',
    'rev.js.noPude': 'I could not check it: ',
    'rev.js.ejemploCaptura': 'Hand-written example: this is what you see when a screenshot cannot be read.',
    'js.ejemploSinServidor': 'Hand-written example: the checker is not running.',

    /* ---- El feed (feed/index.html) ---- */
    'feed.titulo': 'Nelli · Prototype inside the feed',
    'feed.lema': 'The feed · our own concept, not Facebook',
    'feed.intro': 'This is how Nelli would look on top of any post. It is a showcase for Nelli, not a Meta network.',
    'feed.filtros.aria': 'Filter posts',
    'feed.filtro.todas': 'All (11)', 'feed.filtro.con': 'With a warning (9)', 'feed.filtro.sin': 'No warning (2)',
    'feed.demo': "Demo feed: people, posts and messages are made up; the photos were generated with Muse Image for the demo. The Check buttons do use Nelli's real engine.",
    'feed.util': 'Useful', 'feed.avisar': 'Warn someone', 'feed.guardar': 'Save', 'feed.verificar': 'Check',
    'feed.js.revisando': 'Checking…',
    'feed.compartio': 'Shared message · made-up example', 'feed.compartio.conversacion': 'Shared conversation · made-up example',
    'feed.p1.autor': "Aunt Chela's Kitchen", 'feed.p1.cuando': '2 h ago · Sample post', 'feed.p1.estante': 'Entertainment',
    'feed.p1.texto': 'Red pozole tonight for the cold. What do you have it with?', 'feed.p1.alt': 'Pot of red pozole with steam, illustration',
    'feed.p2.autor': "Lupita's Deals MX", 'feed.p2.cuando': '35 min ago · Sponsored', 'feed.p2.estante': 'Sale offer',
    'feed.p2.alt': 'Phone in its box with a clearance sign, illustration', 'feed.p2.aviso': 'Unverified offer: check 5 points before you buy',
    'feed.p3.cuando': '1 h ago · Shared a message', 'feed.p3.estante': 'Asks for data',
    'feed.p3.texto': 'I got this by text. Anyone else? Is it real?', 'feed.p3.alt': 'Phone with a fake fine notice, illustration',
    'feed.p3.aviso': 'Unverified message: check 5 points before you reply',
    'feed.p4.autor': 'Bank — forwarded notice', 'feed.p4.cuando': '20 min ago · Shared a message', 'feed.p4.estante': 'Bank',
    'feed.p4.texto': 'My dad got this on WhatsApp. It says his account gets blocked today:', 'feed.p4.alt': 'Generic bank building with no logos, illustration',
    'feed.p4.aviso': 'Unverified bank notice: check before you open the link',
    'feed.p5.autor': 'Neighborhood group', 'feed.p5.cuando': 'Yesterday · Sample post', 'feed.p5.estante': 'Information',
    'feed.p5.texto': 'Park clean-up this Saturday. See you at 9, bring a broom if you can.', 'feed.p5.alt': 'Neighbors in a park with trees, illustration',
    'feed.p6.autor': 'Courier — forwarded notice', 'feed.p6.cuando': '3 h ago · Shared a message', 'feed.p6.estante': 'Package',
    'feed.p6.texto': "Is this normal? I'm not expecting any package:", 'feed.p6.alt': 'Courier box with a label, illustration',
    'feed.p6.aviso': "Unverified package: don't pay anything through the link",
    'feed.p7.autor': 'Family — forwarded message', 'feed.p7.cuando': '4 h ago · Shared a screenshot', 'feed.p7.estante': 'Family',
    'feed.p7.texto': 'A neighbor got this from someone posing as her son. She called his usual number instead:', 'feed.p7.alt': 'Phone with a message asking for a deposit, illustration',
    'feed.p7.aviso': 'New number asking for money: check by calling the usual one',
    'feed.p8.autor': 'Jobs Today MX', 'feed.p8.cuando': '5 h ago · Sponsored', 'feed.p8.estante': 'Job',
    'feed.p8.alt': 'Ad for an easy job with a high salary, illustration', 'feed.p8.aviso': "Unverified job: if it doesn't say which company, be wary",
    'feed.p9.autor': 'Corner Store', 'feed.p9.cuando': 'Today · Sample post', 'feed.p9.estante': 'Information',
    'feed.p9.alt': 'Order box on its way, illustration', 'feed.p9.aviso': 'No rush and no link: you can still check it in 5 points',
    'feed.p10.autor': 'Prize — forwarded notice', 'feed.p10.cuando': '2 h ago · Shared a message', 'feed.p10.estante': 'Prize',
    'feed.p10.texto': 'My aunt got this and almost paid the “shipping” to claim it:', 'feed.p10.aviso': 'Unverified prize: check 5 points before you claim',
    'feed.p11.autor': 'Easy Credit MX', 'feed.p11.cuando': '1 h ago · Sponsored', 'feed.p11.estante': 'Loan',
    'feed.p11.aviso': "Unverified loan: don't deposit anything up front",

    /* ---- Blindar mi cuenta (web/blindar.html) ---- */
    'bl.titulo': 'Nelli · Shield my account in 7 minutes',
    'bl.hero.alt': "Nelli's seal in 3D", 'bl.hero.t': 'Security check-up',
    'bl.hero.p': 'This is Shield my account: seven short steps so nobody gets into your accounts. One at a time, no rush.',
    'bl.h1': 'Shield my account in 7 minutes',
    'bl.intro': 'Tick each step once you finish it on your phone. Your progress is saved only on this device; nobody else sees it.',
    'bl.llevas': "You've done ", 'bl.de7': ' of 7',
    'bl.1.t': '1. Screen lock with a PIN or fingerprint',
    'bl.1.p': 'Why it protects you: nobody can open your phone even if it gets lost or stolen.',
    'bl.1.h': 'How: turn on auto-lock in under 1 minute. Whoever picks up your phone must not be able to open it.',
    'bl.2.t': '2. Two-step verification on WhatsApp',
    'bl.2.p': 'Why it protects you: without this PIN, someone else can take over your WhatsApp.',
    'bl.2.h': 'How: in WhatsApp go to Settings · Account · Two-step verification. Set a PIN only you know.',
    'bl.3.t': '3. Never share codes with anyone',
    'bl.3.p': 'Why it protects you: that code is the key to your account: whoever has it gets in.',
    'bl.3.h': 'How: the 6-digit code you get by SMS is yours alone. Neither your bank nor WhatsApp will ever ask for it by message or call.',
    'bl.4.t': '4. A different password for your email',
    'bl.4.p': 'Why it protects you: if they steal your email, they steal everything that can be recovered through it.',
    'bl.4.h': "How: your email is the key to everything else. Give it a long password you don't use anywhere else.",
    'bl.5.t': '5. Two-step verification on your email and your bank',
    'bl.5.p': 'Why it protects you: even if they guess your password, the second step stops them.',
    'bl.5.h': "How: turn it on in your email and in your bank's app. Look for it under Settings or Security in each app.",
    'bl.6.t': '6. Phone and apps up to date',
    'bl.6.p': 'Why it protects you: old versions have holes that are already known.',
    'bl.6.h': 'How: install the phone and WhatsApp updates. Many account thefts get in through old versions.',
    'bl.7.t': '7. A code word with your family',
    'bl.7.p': "Why it protects you: it's your family password against the “son, I changed my number” scam.",
    'bl.7.h': 'How: agree on a secret word with your family. If someone writes asking for money, ask for the word before doing anything.',
    'bl.insignia.alt': 'Shielded account badge', 'bl.insignia.t': 'Shielded account', 'bl.insignia.p': 'You finished all 7 steps.',
    'bl.nota': 'Badge generated with Muse Image (Meta Model API) on Oct 30, 2026. Unaffiliated prototype — not a Meta product.',

    /* ---- Manual (web/manual.html) ---- */
    'man.titulo': 'Nelli · Simple user guide', 'man.lema': 'Simple user guide',
    'man.descripcion': "Nelli's simple guide: how to check a suspicious message in 3 steps, what each result means and what to do if you already fell for it.",
    'man.h1': 'How to use Nelli, no computer skills needed',
    'man.intro.1': "You got a message asking for money, data or to open a link and you don't know if it's real. ",
    'man.intro.b': 'Before you do anything, ask Nelli.',
    'man.intro.2': " No account needed, it's free and your message is not stored.",
    'man.foto1.alt': 'A woman looking worriedly at her phone in her kitchen',
    'man.paso1': 'Step 1 · Bring the message',
    'man.paso1.a.b': 'Paste the text:', 'man.paso1.a': ' copy the message and paste it in the big box.',
    'man.paso1.b.b': 'Upload a photo:', 'man.paso1.b': ' send a screenshot of your screen.',
    'man.paso1.c.b': 'Send a voice note:', 'man.paso1.c': ' send the audio you received.',
    'man.paso2': 'Step 2 · Tap the big button',
    'man.paso2.1': 'Tap ', 'man.paso2.b': '“Check the message”', 'man.paso2.2': ' and wait a few seconds. The link is not opened in a browser and your message is not stored: it goes only to the Meta AI (Muse) to be read.',
    'man.paso3': 'Step 3 · Read or listen to your card',
    'man.paso3.1': 'The result goes on top in big letters. Below it, ', 'man.paso3.b': 'one single next step',
    'man.paso3.2': ': do only that. If you prefer, tap ', 'man.paso3.b2': '“Listen to the result”', 'man.paso3.3': ' and we read it out loud.',
    'man.foto2.alt': 'Hands holding a phone inside a car',
    'man.niveles': 'What each result means', 'man.th.dice': 'What it says', 'man.th.haces': 'What you do',
    'man.n1': 'Confirmed scam', 'man.n1.h': "Don't open the link. Report and block.",
    'man.n2': 'Very likely a scam', 'man.n2.h': "Don't pay. Call the person or the bank at the usual number.",
    'man.n3': 'Possible scam', 'man.n3.h': 'Confirm another way before doing anything.',
    'man.n4': 'No clear signs', 'man.n4.h': "That doesn't mean it's safe. If it asks for money or data, confirm anyway.",
    'man.n5': "I couldn't check it", 'man.n5.h': 'Send the text or a clearer screenshot.',
    'man.yacai': 'If you already fell for it, breathe',
    'man.yacai.1': "Don't send more money, even if they threaten you.",
    'man.yacai.2': 'Call your bank at the number on your card and ask them to block.',
    'man.yacai.3': 'Tell someone you trust today.',
    'man.bl': 'Shield your account in 7 minutes',
    'man.bl.1': 'In ', 'man.bl.liga': 'Shield my account',
    'man.bl.2': ' we walk you through it step by step. When you finish the 7 steps you get your Shielded account badge, made with Muse Image.',
    'man.sello.alt': "Nelli's seal in three dimensions",
    'man.nunca': 'What Nelli never does',
    'man.nunca.1': 'Never opens the link you were sent in a browser.', 'man.nunca.2': "It never tells you “it's safe”.",
    'man.nunca.3': 'It never asks for passwords, PINs or codes.', 'man.nunca.4': "It doesn't store your message.",
    'man.pie': 'Made by an independent developer in Mexico, powered by Muse (Meta Model API). Nelli is not a Meta product. Full guide in the repository: ',
    'man.ir': 'Go check a message',

    /* ---- La tarjeta (web/tarjeta.js) ---- */
    'tj.escuchar': 'Listen to the result',
    'tj.revise': 'What I checked',
    'tj.noPude': "I couldn't check this.",
    'tj.recomiendo': 'What I recommend now', 'tj.recomiendo.voz': 'What I recommend now. ',
    'tj.siPuedo': 'What I can do',
    'tj.fuente': 'Official source: ', 'tj.fuente.dominio': 'Its official site is ', 'tj.fuente.donde': 'Where it says so (',
    'tj.ligas': "Links in the message (disabled, don't open them):",
    'tj.bloquear': 'Do it yourself in the app where it arrived: open the conversation, tap the name or number at the top and choose “Block”. Then delete it.',
    'tj.reportar': 'Prototype: the report will be sent from here, without your name or number, to warn other people. For now, report it yourself in the app where it arrived.',
    'tj.confianza': 'Send this to someone you trust:',
    'tj.copia': 'Copy it and send it to them.', 'tj.copiado': 'Copied. Paste it and send it to them.',
    'tj.cerrar': 'Close',
    'tj.lic.revisado': 'Checked against: ', 'tj.lic.ia': 'AI: ', 'tj.lic.noVi': "Couldn't see: ",
    'tj.nota.motor': 'The checker answers in Spanish for now; the buttons and labels are in English.'
  };

  function guardado() {
    var m = (location.search + location.hash).match(/idioma=(es|en)/);
    if (m) { try { localStorage.setItem(LLAVE, m[1]); } catch (e) {} return m[1]; }
    try { return localStorage.getItem(LLAVE); } catch (e) { return null; }
  }

  var actual = guardado() === 'en' ? 'en' : 'es';
  raiz.setAttribute('lang', actual === 'en' ? 'en' : 'es-MX');

  // t('clave', 'texto en español'): el inglés si está activo y existe; si no, el español tal cual
  function t(clave, es) {
    if (actual === 'en' && Object.prototype.hasOwnProperty.call(EN, clave)) return EN[clave];
    return es == null ? '' : es;
  }

  function agregar(mas) { Object.keys(mas || {}).forEach(function (k) { EN[k] = mas[k]; }); }

  var ATRIBUTOS = [['data-t-placeholder', 'placeholder'], ['data-t-aria', 'aria-label'], ['data-t-alt', 'alt'], ['data-t-title', 'title'], ['data-t-content', 'content']];

  // Guarda el español la primera vez y pone el idioma activo. Solo textContent y atributos, nunca HTML.
  function traducirDom() {
    var nodos = document.querySelectorAll('[data-t]');
    for (var i = 0; i < nodos.length; i++) {
      var n = nodos[i];
      if (n.__nelliEs == null) n.__nelliEs = n.textContent;
      n.textContent = t(n.getAttribute('data-t'), n.__nelliEs);
    }
    ATRIBUTOS.forEach(function (par) {
      var lista = document.querySelectorAll('[' + par[0] + ']');
      for (var j = 0; j < lista.length; j++) {
        var el = lista[j];
        el.__nelliEsAttr = el.__nelliEsAttr || {};
        if (el.__nelliEsAttr[par[1]] == null) el.__nelliEsAttr[par[1]] = el.getAttribute(par[1]) || '';
        el.setAttribute(par[1], t(el.getAttribute(par[0]), el.__nelliEsAttr[par[1]]));
      }
    });
    pintarBotones();
  }

  function pintarBotones() {
    var en = actual === 'en';
    var botones = document.querySelectorAll('[data-idioma-boton]');
    for (var i = 0; i < botones.length; i++) {
      botones[i].textContent = en ? EN['idioma.boton.en'] : EN['idioma.boton.es'];
      botones[i].setAttribute('aria-label', en ? EN['idioma.aria.en'] : EN['idioma.aria.es']);
      botones[i].setAttribute('lang', en ? 'es' : 'en');
    }
  }

  function aplicar(idioma) {
    actual = idioma === 'en' ? 'en' : 'es';
    raiz.setAttribute('lang', actual === 'en' ? 'en' : 'es-MX');
    try { localStorage.setItem(LLAVE, actual); } catch (e) {}
    traducirDom();
    // Las páginas vuelven a pintar lo que dibujan por script (ejemplos, textos del feed, botón de modo)
    try { document.dispatchEvent(new CustomEvent('nelli-idioma', { detail: { idioma: actual } })); } catch (e) {}
  }

  document.addEventListener('DOMContentLoaded', function () {
    traducirDom();
    document.addEventListener('click', function (e) {
      var b = e.target.closest ? e.target.closest('[data-idioma-boton]') : null;
      if (!b) return;
      aplicar(actual === 'en' ? 'es' : 'en');
    });
  });

  window.NelliIdioma = { actual: function () { return actual; }, es: function () { return actual !== 'en'; }, aplicar: aplicar, t: t, agregar: agregar };
})();
