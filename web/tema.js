/* Nelli · modo claro y oscuro.
   Claro por defecto; oscuro solo si el telefono esta en modo oscuro; y un boton para cambiarlo a mano.
   Se carga en el <head>, antes del CSS, para que no parpadee. La eleccion se guarda solo en este aparato.
   Para el video y las capturas: ?tema=oscuro o #tema=claro fuerzan un modo y lo guardan. */
(function () {
  'use strict';
  var raiz = document.documentElement;
  var LLAVE = 'nelli-tema';
  var medio = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;

  function guardado() {
    var m = (location.search + location.hash).match(/tema=(claro|oscuro)/);
    if (m) { try { localStorage.setItem(LLAVE, m[1]); } catch (e) {} return m[1]; }
    try { return localStorage.getItem(LLAVE); } catch (e) { return null; }
  }

  function actual() {
    var t = raiz.getAttribute('data-tema');
    if (t === 'claro' || t === 'oscuro') return t;
    return medio && medio.matches ? 'oscuro' : 'claro';
  }

  function aplicar(t) {
    if (t === 'claro' || t === 'oscuro') raiz.setAttribute('data-tema', t);
    else raiz.removeAttribute('data-tema');
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', actual() === 'oscuro' ? '#15191D' : '#FFFFFF');
    pintarBotones();
  }

  // El boton dice lo que hace, no lo que hay: en claro ofrece "Modo oscuro" y al reves
  // El texto del botón pasa por web/idioma.js si está cargado (inglés con «English»)
  function tx(clave, es) { return window.NelliIdioma ? window.NelliIdioma.t(clave, es) : es; }

  function pintarBotones() {
    var oscuro = actual() === 'oscuro';
    var botones = document.querySelectorAll('[data-tema-boton]');
    for (var i = 0; i < botones.length; i++) {
      botones[i].textContent = oscuro ? tx('tema.claro', 'Modo claro') : tx('tema.oscuro', 'Modo oscuro');
      botones[i].setAttribute('aria-label', oscuro ? tx('tema.aria.claro', 'Cambiar a modo claro') : tx('tema.aria.oscuro', 'Cambiar a modo oscuro'));
      botones[i].className = 'boton-tema ' + (oscuro ? 'es-oscuro' : 'es-claro');
    }
  }

  aplicar(guardado());

  document.addEventListener('DOMContentLoaded', function () {
    pintarBotones();
    document.addEventListener('click', function (e) {
      var b = e.target.closest ? e.target.closest('[data-tema-boton]') : null;
      if (!b) return;
      var nuevo = actual() === 'oscuro' ? 'claro' : 'oscuro';
      try { localStorage.setItem(LLAVE, nuevo); } catch (err) {}
      aplicar(nuevo);
    });
  });

  // Si no hay eleccion a mano, sigue al telefono cuando cambie de modo
  if (medio && medio.addEventListener) medio.addEventListener('change', function () { aplicar(raiz.getAttribute('data-tema')); });

  // Si cambia el idioma (web/idioma.js), el botón se vuelve a escribir
  document.addEventListener('nelli-idioma', pintarBotones);
  window.NelliTema = { actual: actual, aplicar: aplicar };
})();
