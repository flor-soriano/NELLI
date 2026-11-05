/* Nelli · dibuja la tarjeta del motor (src/nelli/tarjeta.py, contrato en docs/reparto.md) para web/ y feed/.
   Todo el texto entra como texto, nunca como HTML: puede venir del mensaje que escribió el estafador.
   Sin verde y sin porcentajes. */
(function () {
  'use strict';

  // Con esta ruta se arman las ligas a las otras pantallas, sirva el servidor la página o se abra con doble clic
  var AQUI = document.currentScript ? document.currentScript.src : location.href;

  // Textos fijos de la tarjeta: español aquí mismo; inglés desde web/idioma.js si la página está en «English»
  function t(clave, es) { return window.NelliIdioma ? window.NelliIdioma.t(clave, es) : es; }

  // Las tarjetas de ejemplo en el idioma activo (web/ejemplos.js o web/ejemplos-en.js)
  function ejemplos() {
    var en = window.NelliIdioma && !window.NelliIdioma.es() && window.NELLI_EJEMPLOS_EN;
    return en ? window.NELLI_EJEMPLOS_EN : (window.NELLI_EJEMPLOS || []);
  }

  var SVG = {
    alerta: '<path d="M12 3 2 21h20L12 3z"/><path d="M12 10v5"/><path d="M12 18h.01"/>',
    escudo: '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6l-8-3z"/><path d="M12 8v5"/><path d="M12 16h.01"/>',
    duda: '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.6v.6"/><path d="M12 17h.01"/>',
    insignia: '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6l-8-3z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
    bandera: '<path d="M5 21V4"/><path d="M5 4h11l-2 4 2 4H5"/>',
    bloquear: '<circle cx="12" cy="12" r="9"/><path d="m5.6 5.6 12.8 12.8"/>',
    personas: '<circle cx="9" cy="8" r="3"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><path d="M16 5.5a3 3 0 0 1 0 5"/><path d="M21 20c0-2.6-1.6-4.8-4-5.6"/>',
    salvavidas: '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="m5.6 5.6 3.6 3.6M14.8 14.8l3.6 3.6M18.4 5.6l-3.6 3.6M9.2 14.8l-3.6 3.6"/>',
    candado: '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>'
  };

  var ICONO_NIVEL = {
    fraude_confirmado: 'alerta', muy_probablemente_fraude: 'alerta', posible_fraude: 'escudo',
    sin_senales_claras: 'escudo', no_pude_revisar: 'duda', negativa: 'bloquear'
  };
  var MARCA = { ok: '✓', alerta: '!', no_revisado: '?' };
  var ICONO_BOTON = { reportar: 'bandera', bloquear: 'bloquear', confianza: 'personas', ya_cai: 'salvavidas', blindar: 'candado' };

  // El motor manda los botones como texto; el front los reconoce por su texto
  function idBoton(b) {
    if (b && typeof b === 'object') return b.id;
    var t = String(b);
    if (t.indexOf('Blindar') === 0) return 'blindar';
    if (t.indexOf('Ya caí') === 0) return 'ya_cai';
    if (t.indexOf('Pregúntale') === 0) return 'confianza';
    if (t.indexOf('Bloquear') === 0) return 'bloquear';
    if (t.indexOf('Reportar') === 0) return 'reportar';
    return '';
  }

  function icono(nombre) {
    var s = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    s.setAttribute('viewBox', '0 0 24 24'); s.setAttribute('class', 'icono'); s.setAttribute('aria-hidden', 'true');
    s.setAttribute('fill', 'none'); s.setAttribute('stroke', 'currentColor'); s.setAttribute('stroke-width', '2');
    s.setAttribute('stroke-linecap', 'round'); s.setAttribute('stroke-linejoin', 'round');
    s.innerHTML = SVG[nombre] || '';
    return s;
  }

  // h('p', {class: 'x'}, 'texto', otroNodo): crea nodos sin pasar texto por innerHTML
  function h(etiqueta, attrs) {
    var n = document.createElement(etiqueta);
    Object.keys(attrs || {}).forEach(function (k) {
      if (attrs[k] === false || attrs[k] == null) return;
      if (k === 'texto') n.textContent = attrs[k]; else n.setAttribute(k, attrs[k]);
    });
    for (var i = 2; i < arguments.length; i++) {
      var hijo = arguments[i];
      if (hijo == null) continue;
      n.appendChild(typeof hijo === 'string' ? document.createTextNode(hijo) : hijo);
    }
    return n;
  }

  // Las ligas se enseñan desarmadas aunque llegue alguna sin desarmar
  function desarmar(liga) {
    var t = String(liga).replace(/^http/i, 'hxxp');
    return t.indexOf('[.]') >= 0 ? t : t.replace(/\./g, '[.]');
  }

  // Solo se hace clicable una liga oficial que venga del paquete MX (https), nunca una del mensaje
  function ligaOficial(url) {
    return /^https:\/\//i.test(String(url || '')) ? String(url) : null;
  }

  function textoLicencia(l) {
    if (!l) return '';
    if (typeof l === 'string') return l;
    var partes = [];
    if (l.revisado_contra && l.revisado_contra.length) partes.push(t('tj.lic.revisado', 'Revisado contra: ') + l.revisado_contra.join(' · '));
    if (l.ia && l.ia !== '—') partes.push(t('tj.lic.ia', 'IA: ') + l.ia);
    if (l.no_pude_ver && l.no_pude_ver.length) partes.push(t('tj.lic.noVi', 'No pude ver: ') + l.no_pude_ver.join(', '));
    return partes.join(' · ');
  }

  function panel(id, nodos) {
    var p = h('div', { class: 'panel', id: id, hidden: 'hidden', role: 'region', tabindex: '-1' });
    nodos.forEach(function (n) { p.appendChild(n); });
    return p;
  }

  function mostrarPanel(boton, p) {
    var abierto = !p.hidden;
    p.hidden = abierto;
    boton.setAttribute('aria-expanded', String(!abierto));
    if (!abierto) p.focus();
  }

  // nota: texto gris arriba de la tarjeta, p. ej. cuando es un ejemplo escrito a mano
  function dibujar(tarjeta, nota) {
    var t_ = tarjeta;
    var raiz = h('article', { class: 'tarjeta nivel-' + t_.nivel, 'aria-labelledby': 'tarjeta-etiqueta' });
    if (nota) raiz.appendChild(h('p', { class: 'nota-ejemplo', texto: nota }));

    var sub = t_.tipo_nombre && t_.tipo !== 'ninguno' ? t_.tipo_nombre : t_.resumen;
    raiz.appendChild(h('header', { class: 'tarjeta-cabeza' }, icono(ICONO_NIVEL[t_.nivel] || 'duda'),
      h('div', {}, h('h2', { class: 'tarjeta-etiqueta', id: 'tarjeta-etiqueta', texto: t_.etiqueta }),
        sub ? h('p', { class: 'tarjeta-sub', texto: sub }) : null)));

    var SEGS = { fraude_confirmado: [4,'confirmado'], muy_probablemente_fraude: [3,'muy'], posible_fraude: [2,'posible'],
      sin_senales_claras: [1,'gris'], no_pude_revisar: [1,'gris'], negativa: [1,'gris'] };
    var seg = SEGS[t_.nivel] || [1, 'gris'];
    var med = h('div', { class: 'medidor', 'aria-hidden': 'true' });
    for (var s = 0; s < 4; s++) med.appendChild(h('i', { class: s < seg[0] ? 'on-' + seg[1] : '' }));
    raiz.appendChild(med);

    var cuerpo = h('div', { class: 'tarjeta-cuerpo' });
    raiz.appendChild(cuerpo);

    // Escuchar el resultado: lo lee la voz del propio telefono, sin servidor.
    if ('speechSynthesis' in window) {
      var btnEscuchar = h('button', { type: 'button', class: 'boton boton-escuchar' }, icono('escudo'), t('tj.escuchar', 'Escuchar el resultado'));
      btnEscuchar.addEventListener('click', function () {
        try {
          speechSynthesis.cancel();
          var partes = [tarjeta.etiqueta + '.'];
          (tarjeta.puntos || []).forEach(function (p) { partes.push(p.titulo + '. ' + (p.texto || '')); });
          if (tarjeta.paso) partes.push(t('tj.recomiendo.voz', 'Lo que te recomiendo ahora. ') + tarjeta.paso);
          var voz = new SpeechSynthesisUtterance(partes.join(' '));
          // La voz del teléfono en el idioma de la tarjeta: la del motor siempre es en español
          voz.lang = (tarjeta.idioma === 'en') ? 'en-US' : 'es-MX'; voz.rate = 0.92;
          speechSynthesis.speak(voz);
        } catch (e) { /* si la voz falla, la tarjeta escrita sigue ahi */ }
      });
      cuerpo.appendChild(btnEscuchar);
    }

    if (t_.puntos && t_.puntos.length) {
      cuerpo.appendChild(h('h3', { texto: t('tj.revise', 'Lo que revisé') }));
      var lista = h('ol', { class: 'puntos' });
      t_.puntos.forEach(function (p) {
        var texto = p.texto || (p.estado === 'no_revisado' ? t('tj.noPude', 'No pude revisarlo.') : '');
        lista.appendChild(h('li', { class: 'punto punto-' + p.estado },
          h('span', { class: 'punto-marca', 'aria-hidden': 'true', texto: MARCA[p.estado] || '·' }),
          h('span', {}, h('span', { class: 'punto-titulo', texto: p.n + '. ' + p.titulo }),
            h('span', { class: 'punto-texto', texto: texto }))));
      });
      cuerpo.appendChild(lista);
    }

    if (t_.paso) {
      cuerpo.appendChild(h('div', { class: 'paso' }, h('small', { texto: t_.nivel === 'negativa' ? t('tj.siPuedo', 'Lo que sí puedo hacer') : t('tj.recomiendo', 'Lo que te recomiendo ahora') }), t_.paso));
    }

    // El motor manda {institucion, dominio_oficial} o {institucion, fuente}
    var f = t_.fuente_verificada;
    if (f && f.institucion) {
      var url = ligaOficial(f.fuente || f.url);
      cuerpo.appendChild(h('div', { class: 'fuente' }, icono('insignia'),
        h('div', {},
          h('strong', { texto: t('tj.fuente', 'Fuente oficial: ') + f.institucion }),
          f.frase ? h('p', { class: 'fuente-cita', texto: '«' + f.frase + '»' }) : null,
          f.dominio_oficial ? h('p', { class: 'fuente-cita', texto: t('tj.fuente.dominio', 'Su página oficial es ') + f.dominio_oficial }) : null,
          url ? h('a', { href: url, rel: 'noopener noreferrer', target: '_blank', texto: t('tj.fuente.donde', 'Dónde lo publica (') + url.replace(/^https:\/\/(www\.)?/i, '').split('/')[0] + ')' }) : null,
          f.fecha ? h('span', { texto: ' · ' + f.fecha }) : null)));
    }

    if (t_.ligas_desactivadas && t_.ligas_desactivadas.length) {
      var caja = h('div', { class: 'ligas' }, h('p', { texto: t('tj.ligas', 'Ligas del mensaje (desactivadas, no las abras):') }));
      t_.ligas_desactivadas.forEach(function (l) { caja.appendChild(h('code', { texto: desarmar(l) })); });
      cuerpo.appendChild(caja);
    }

    var botones = h('div', { class: 'botones' });
    var paneles = h('div', {});
    (t_.botones || []).forEach(function (b) {
      var id = idBoton(b);
      var texto = typeof b === 'object' ? b.texto : String(b);
      if (id === 'blindar') {
        botones.appendChild(h('a', { class: 'boton boton-rojo', href: new URL('blindar.html', AQUI).href }, icono('candado'), texto));
        return;
      }
      var btn = h('button', { type: 'button', class: 'boton', 'aria-expanded': 'false' }, icono(ICONO_BOTON[id] || 'escudo'), texto);
      var p = null;
      if (id === 'ya_cai') {
        p = panel('panel-ya-cai', [h('p', { texto: t_.ya_cai || '' })]);
      } else if (id === 'bloquear') {
        p = panel('panel-bloquear', [h('p', { texto: t('tj.bloquear', 'Hazlo tú desde la app donde te llegó: abre la conversación, toca el nombre o el número de arriba y elige «Bloquear». Luego bórrala.') })]);
      } else if (id === 'reportar') {
        p = panel('panel-reportar', [h('p', { texto: t('tj.reportar', 'Prototipo: aquí se mandará el reporte, sin tu nombre ni tu número, para avisar a otras personas. Por ahora, repórtalo tú en la app donde te llegó.') })]);
      } else if (id === 'confianza') {
        btn.removeAttribute('aria-expanded');
        p = panel('panel-confianza', [h('p', { texto: t('tj.confianza', 'Mándale esto a alguien de confianza:') }),
          h('p', { texto: t_.mensaje_confianza || '' }), h('p', { class: 'aviso-copia', texto: '' })]);
        btn.addEventListener('click', function () { compartir(t_.mensaje_confianza || '', p); });
      }
      if (p && id !== 'confianza') btn.addEventListener('click', function () { mostrarPanel(btn, p); });
      if (p) btn.setAttribute('aria-controls', p.id);
      botones.appendChild(btn);
      if (p) paneles.appendChild(p);
    });
    if (botones.childNodes.length) {
      cuerpo.appendChild(botones);
      cuerpo.appendChild(paneles);
    }

    var lic = textoLicencia(t_.licencia);
    if (lic) cuerpo.appendChild(h('p', { class: 'licencia', texto: lic }));
    return raiz;
  }

  // La persona lo reenvía ella misma: compartir del teléfono o, si no se puede, copiarlo
  function compartir(texto, p) {
    p.hidden = false;
    p.focus();
    var aviso = p.querySelector('.aviso-copia');
    var COPIA = t('tj.copia', 'Cópialo y mándaselo.');
    function copiar() {
      if (!navigator.clipboard) { aviso.textContent = COPIA; return; }
      navigator.clipboard.writeText(texto).then(function () { aviso.textContent = t('tj.copiado', 'Ya lo copié. Pégalo y mándaselo.'); },
        function () { aviso.textContent = COPIA; });
    }
    if (!navigator.share) { copiar(); return; }
    navigator.share({ text: texto }).catch(function (e) { if (!e || e.name !== 'AbortError') copiar(); });
  }

  // ---------- Capa encima de la página (el feed la abre sin salir) ----------
  var capa, caja, ultimoFoco;

  function crearCapa() {
    capa = h('div', { class: 'capa', hidden: 'hidden', role: 'dialog', 'aria-modal': 'true', 'aria-labelledby': 'tarjeta-etiqueta' });
    caja = h('div', { class: 'capa-caja' });
    var cerrar = h('div', { class: 'capa-cerrar' }, h('button', { type: 'button', 'aria-label': t('tj.cerrar', 'Cerrar'), texto: '×' }));
    cerrar.firstChild.addEventListener('click', cerrarTarjeta);
    caja.appendChild(cerrar);
    capa.appendChild(caja);
    capa.addEventListener('click', function (e) { if (e.target === capa) cerrarTarjeta(); });
    document.addEventListener('keydown', function (e) {
      if (capa.hidden) return;
      if (e.key === 'Escape') cerrarTarjeta();
      if (e.key === 'Tab') atraparFoco(e);
    });
    document.body.appendChild(capa);
  }

  function atraparFoco(e) {
    var f = caja.querySelectorAll('button, a[href], [tabindex]:not([tabindex="-1"])');
    if (!f.length) return;
    var primero = f[0], ultimo = f[f.length - 1];
    if (e.shiftKey && document.activeElement === primero) { ultimo.focus(); e.preventDefault(); }
    else if (!e.shiftKey && document.activeElement === ultimo) { primero.focus(); e.preventDefault(); }
  }

  function abrirTarjeta(t, nota) {
    if (!capa) crearCapa();
    ultimoFoco = document.activeElement;
    while (caja.childNodes.length > 1) caja.removeChild(caja.lastChild);
    caja.appendChild(dibujar(t, nota));
    capa.hidden = false;
    document.body.style.overflow = 'hidden';
    caja.scrollTop = 0;
    caja.querySelector('.capa-cerrar button').focus();
  }

  function cerrarTarjeta() {
    capa.hidden = true;
    document.body.style.overflow = '';
    if (ultimoFoco) ultimoFoco.focus();
  }

  // Pide la tarjeta al motor (POST /api/verificar). Si no hay servidor, la promesa falla y la página decide qué enseñar.
  // err.respondio = true solo cuando el motor contestó con su propio error ({"error": ...}); lo demás cuenta como «sin servidor».
  // Estado del motor (GET /api/salud): null si no hay servidor. `emulador` = true cuando corre el emulador local, no Muse.
  function salud() {
    var api = (window.NELLI_API || '/api/verificar').replace(/verificar$/, 'salud');
    return fetch(api, { cache: 'no-store' }).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; });
  }

  function verificar(cuerpo) {
    var api = window.NELLI_API || '/api/verificar';
    var pedido = cuerpo instanceof FormData ? { method: 'POST', body: cuerpo }
      : { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(cuerpo) };
    return fetch(api, pedido).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (datos) {
        if (r.ok && datos.nivel) return datos;
        var e = new Error(datos.error || String(r.status));
        e.respondio = typeof datos.error === 'string';
        throw e;
      });
    });
  }

  // abierta(): true mientras la capa está encima (para volver a dibujarla si cambia el idioma)
  function abierta() { return !!capa && !capa.hidden; }

  window.Nelli = { dibujarTarjeta: dibujar, abrirTarjeta: abrirTarjeta, cerrarTarjeta: cerrarTarjeta, abierta: abierta, verificar: verificar, salud: salud, ejemplos: ejemplos, t: t, icono: icono, h: h };
  // Compatibilidad con la primera versión de las páginas: NelliTarjeta.render(contenedor, tarjeta)
  window.NelliTarjeta = { render: function (el, t) { el.textContent = ''; el.appendChild(dibujar(t)); } };
})();
