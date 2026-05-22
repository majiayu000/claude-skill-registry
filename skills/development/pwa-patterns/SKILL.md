---
name: pwa-patterns
description: Progressive Web App patterns with Workbox 7.x, service worker lifecycle, offline-first strategies, and installability. Use when building PWAs, service workers, or offline support.
tags: [pwa, service-worker, workbox, offline-first, cache-api, push-notifications, manifest, installable]
context: fork
agent: frontend-ui-developer
version: 1.0.0
author: SkillForge
user-invocable: false
---

# PWA Patterns

Progressive Web App patterns using Workbox 7.x for service worker management, offline-first strategies, and app-like experiences.

## Service Worker Lifecycle

```
Installing -> Waiting -> Active
     │           │           │
  install    activated    fetch events
 (precache)  when old SW  (runtime cache)
              is gone
```

## Workbox: Generate Service Worker

```javascript
// build-sw.js (Node.js)
const { generateSW } = require('workbox-build');

async function buildServiceWorker() {
  await generateSW({
    globDirectory: 'dist/',
    globPatterns: ['**/*.{html,js,css,png,jpg,json,woff2}'],
    swDest: 'dist/sw.js',
    clientsClaim: true,
    skipWaiting: true,
    navigateFallback: '/index.html',
    navigateFallbackDenylist: [/^\/api\//],
    runtimeCaching: [
      {
        urlPattern: /^https:\/\/api\.example\.com\//,
        handler: 'NetworkFirst',
        options: { cacheName: 'api-cache', networkTimeoutSeconds: 10 },
      },
      {
        urlPattern: /\.(?:png|jpg|jpeg|svg|gif|webp)$/,
        handler: 'CacheFirst',
        options: { cacheName: 'images', expiration: { maxEntries: 60, maxAgeSeconds: 30 * 24 * 60 * 60 } },
      },
    ],
  });
}
```

## Caching Strategies

```javascript
// CacheFirst: Static assets that rarely change
registerRoute(/\.(?:js|css|woff2)$/, new CacheFirst({
  cacheName: 'static-v1',
  plugins: [new ExpirationPlugin({ maxEntries: 100, maxAgeSeconds: 365 * 24 * 60 * 60 })],
}));

// NetworkFirst: API calls (fresh data preferred)
registerRoute(/\/api\//, new NetworkFirst({
  cacheName: 'api-cache',
  networkTimeoutSeconds: 10,
  plugins: [new CacheableResponsePlugin({ statuses: [0, 200] })],
}));

// StaleWhileRevalidate: User avatars, non-critical images
registerRoute(/\/avatars\//, new StaleWhileRevalidate({ cacheName: 'avatars' }));

// NetworkOnly: Auth endpoints
registerRoute(/\/auth\//, new NetworkOnly());
```

## VitePWA Integration

```typescript
// vite.config.ts
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [
    VitePWA({
      registerType: 'autoUpdate',
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg,woff2}'],
        runtimeCaching: [{ urlPattern: /^https:\/\/api\./, handler: 'NetworkFirst' }],
      },
      manifest: {
        name: 'My PWA App',
        short_name: 'MyPWA',
        theme_color: '#4f46e5',
        icons: [
          { src: '/icon-192.png', sizes: '192x192', type: 'image/png' },
          { src: '/icon-512.png', sizes: '512x512', type: 'image/png' },
        ],
      },
    }),
  ],
});
```

## Web App Manifest

```json
{
  "name": "My Progressive Web App",
  "short_name": "MyPWA",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#4f46e5",
  "icons": [
    { "src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "maskable" },
    { "src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

## React Hooks

### Install Prompt Hook

```tsx
import { useState, useEffect } from 'react';

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
}

export function useInstallPrompt() {
  const [installPrompt, setInstallPrompt] = useState<BeforeInstallPromptEvent | null>(null);
  const [isInstalled, setIsInstalled] = useState(false);

  useEffect(() => {
    const handler = (e: BeforeInstallPromptEvent) => { e.preventDefault(); setInstallPrompt(e); };
    window.addEventListener('beforeinstallprompt', handler as EventListener);
    if (window.matchMedia('(display-mode: standalone)').matches) setIsInstalled(true);
    return () => window.removeEventListener('beforeinstallprompt', handler as EventListener);
  }, []);

  const promptInstall = async () => {
    if (!installPrompt) return false;
    await installPrompt.prompt();
    const { outcome } = await installPrompt.userChoice;
    setInstallPrompt(null);
    if (outcome === 'accepted') { setIsInstalled(true); return true; }
    return false;
  };

  return { canInstall: !!installPrompt, isInstalled, promptInstall };
}
```

### Offline Status Hook

```tsx
export function useOnlineStatus() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return isOnline;
}
```

## Background Sync

```javascript
// sw.js
import { BackgroundSyncPlugin } from 'workbox-background-sync';
import { registerRoute } from 'workbox-routing';
import { NetworkOnly } from 'workbox-strategies';

registerRoute(
  /\/api\/forms/,
  new NetworkOnly({ plugins: [new BackgroundSyncPlugin('formQueue', { maxRetentionTime: 24 * 60 })] }),
  'POST'
);
```

## Anti-Patterns (FORBIDDEN)

```javascript
// NEVER: Cache everything with no expiration (storage bloat)
// NEVER: Skip clientsClaim (old tabs stay on old SW)
// NEVER: Cache authentication tokens (security risk)
// NEVER: Precache dynamic content (changes frequently)
// NEVER: Forget offline fallback for navigation
// NEVER: Cache POST responses
```

## PWA Checklist

- [ ] Service worker registered
- [ ] Manifest with icons (192px + 512px maskable)
- [ ] HTTPS enabled
- [ ] Offline page works
- [ ] Responsive design
- [ ] Fast First Contentful Paint (< 1.8s)

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| SW generator | **generateSW** for simple, **injectManifest** for custom |
| API caching | **NetworkFirst** for critical data |
| Static assets | **CacheFirst** with versioned filenames |
| Update strategy | **Prompt** user for major changes |

## Related Skills

- `caching-strategies` - Backend caching patterns
- `core-web-vitals` - Performance metrics
- `streaming-api-patterns` - Real-time updates
