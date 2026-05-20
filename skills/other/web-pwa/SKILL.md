---
name: web-pwa
cluster: web-dev
description: "PWA: service workers, Cache API, manifest, offline, background sync, push notifications"
tags: ["pwa","service-worker","offline","web"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "progressive web app service worker offline push notification cache"
---

# web-pwa

## Purpose
This skill enables building Progressive Web Apps (PWAs) by managing service workers, caching, manifests, offline functionality, background sync, and push notifications. It focuses on making web apps installable, reliable, and engaging like native apps.

## When to Use
Use this skill when developing web apps that need offline access, such as news readers or e-commerce sites; for apps requiring push notifications, like chat apps; or when enhancing user experience with background sync for data updates. Apply it in scenarios where users expect app-like behavior on mobile or desktop browsers.

## Key Capabilities
- Service Workers: Intercept network requests and cache responses using the Cache API (e.g., `caches.open('my-cache')`).
- Manifest: Define app metadata in a JSON file (e.g., `{ "name": "My PWA", "start_url": "/" }`) for installability.
- Offline Support: Enable apps to function without internet via service workers and IndexedDB.
- Background Sync: Queue tasks for later execution when online, using the Background Sync API (e.g., `registration.sync.register('my-sync')`).
- Push Notifications: Handle subscriptions and messages via the Push API and Service Worker API (e.g., `subscription.endpoint` for server communication).

## Usage Patterns
To implement a PWA, first create a service worker file (e.g., `sw.js`) and register it in your main script. For offline caching, use the Cache API to store assets. Always check for service worker support before registration. Integrate a web app manifest for installation prompts. Test patterns in a browser's dev tools under the Application tab.

## Common Commands/API
- Register a service worker: Use `if ('serviceWorker' in navigator) { navigator.serviceWorker.register('/sw.js'); }` in your JavaScript file.
- Cache assets: In `sw.js`, add `event.respondWith(caches.match(event.request).then(response => response || fetch(event.request)));` to handle requests.
- Add to home screen: Ensure manifest.json includes `"display": "standalone"` and serve it from the root.
- Handle push notifications: Subscribe with `registration.pushManager.subscribe({ userVisibleOnly: true })` and send via a server endpoint like `https://yourserver.com/push` (requires $VAPID_PUBLIC_KEY for authentication).
- Background sync: Register with `navigator.serviceWorker.ready.then(reg => reg.sync.register('sync-tag'))`; use CLI tools like `workbox-cli build` for bundling (e.g., `npx workbox generateSW workbox-config.js`).
Config format for manifest: JSON object like `{ "short_name": "App", "icons": [{ "src": "icon.png", "sizes": "192x192" }] }`.

## Integration Notes
Integrate this skill with existing web projects by adding a service worker script and manifest file. For push notifications, set up a server with the Web Push library and use env vars like `$VAPID_PRIVATE_KEY` for signing. If using frameworks, import in React via `useEffect(() => { if ('serviceWorker' in navigator) navigator.serviceWorker.register(); }, []);`. For caching, combine with Fetch API; ensure HTTPS for service workers. Avoid conflicts by checking for existing workers before registration.

## Error Handling
When registering service workers, catch errors with `.then(() => console.log('Registered')).catch(err => console.error('Registration failed:', err))`. For cache operations, handle promise rejections (e.g., `caches.open('cache-name').then(cache => cache.addAll(['/'])).catch(err => console.error(err))`). If push subscription fails, check user permissions and use `Notification.requestPermission()` first. For background sync, listen for `sync` events in the service worker and handle failures by retrying or logging with `event.tag`. Use browser-specific error codes, like DOMException for security errors, and set up global error handlers in your app.

## Concrete Usage Examples
1. **Basic PWA Setup**: Create a service worker to cache static assets. In `index.js`: `if ('serviceWorker' in navigator) { navigator.serviceWorker.register('/sw.js').then(reg => console.log('SW registered')); }`. In `sw.js`: `self.addEventListener('install', event => event.waitUntil(caches.open('static').then(cache => cache.add('/'))));`. This enables offline loading of the home page.
2. **Push Notifications Integration**: Subscribe users and handle messages. In your app: `registration.pushManager.subscribe().then(sub => fetch('/subscribe', { method: 'POST', body: JSON.stringify(sub) }));`. On the server, use an endpoint like `POST /subscribe` with $VAPID_PUBLIC_KEY to send notifications via the Push API.

## Graph Relationships
- Related to cluster: web-dev (e.g., shares dependencies with skills like web-frontend, web-backend).
- Connected via tags: pwa (links to mobile-app), service-worker (links to web-performance), offline (links to data-sync), web (links to full-stack-dev).
- Dependencies: Requires web APIs; integrates with tools like Workbox for service worker generation.
