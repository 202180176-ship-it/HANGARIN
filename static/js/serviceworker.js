self.addEventListener('install', function(e) {
    e.waitUntil(
        caches.open('projectsite-cache-v1').then(function(cache) {
        return cache.addAll([
            '/',
            '/static/css/hangarin.css',
            '/static/css/auth.css',
            '/static/images/background.png',
            ]);
        })
    );
});
self.addEventListener('fetch', function(e) {
    e.respondWith(
    caches.match(e.request).then(function(response) {
        return response || fetch(e.request);
        })
    );    
});