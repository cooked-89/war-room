/* The War Room - offline shell.
   The app HTML is network-first so a new deploy lands immediately; everything
   else same-origin is cache-first; API calls are never cached, because a draft
   board served from cache is worse than no board at all. */
const VERSION = 'war-room-v2';
const SHELL = ['./', './index.html', './manifest.webmanifest', './icon-192.png', './icon-512.png'];

self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(VERSION).then(function (c) { return Promise.all(SHELL.map(function (u) {
      return fetch(u, {cache: 'no-store'}).then(function (r) { return c.put(u, r); });
    })); }).then(function () {
    return self.skipWaiting();
  }));
});

self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.filter(function (k) { return k !== VERSION; })
                           .map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});

self.addEventListener('fetch', function (e) {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;          // live data: straight to network

  const isDoc = req.mode === 'navigate' || (req.headers.get('accept') || '').indexOf('text/html') > -1;
  if (isDoc) {
    /* 'Network-first' is not enough on its own: a plain fetch() here is still allowed to
       come out of the browser HTTP cache, and GitHub Pages sends a max-age. That served a
       ten-minute-old build after a deploy. no-store forces a real round trip, so a fix
       pushed on draft morning actually arrives. */
    e.respondWith(
      fetch(req, {cache: 'no-store'}).then(function (res) {
        const copy = res.clone();
        caches.open(VERSION).then(function (c) { c.put('./index.html', copy); });
        return res;
      }).catch(function () {
        return caches.match('./index.html').then(function (r) { return r || caches.match('./'); });
      })
    );
    return;
  }
  e.respondWith(caches.match(req).then(function (hit) { return hit || fetch(req); }));
});
