---
name: pwa-expert
description: Progressive Web App development with Service Workers, offline support, and app-like behavior. Use for caching strategies, install prompts, push notifications, background sync. Activate on "PWA", "Service Worker", "offline", "install prompt", "beforeinstallprompt", "manifest.json", "workbox", "cache-first". NOT for native app development (use React Native), general web performance (use performance docs), or server-side rendering.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
category: Design & Creative
tags:
  - pwa
  - service-worker
  - offline
  - caching
  - installable
  - workbox
  - manifest
---

# Progressive Web App Expert

Build installable, offline-capable web apps with Service Workers, smart caching, and native-like experiences.

## When to Use This Skill

- Making a web app installable on mobile/desktop
- Implementing offline functionality
- Setting up Service Worker caching strategies
- Handling install prompts (`beforeinstallprompt`)
- Background sync for offline-first apps
- Managing PWA update flows
- Creating web app manifests

## When NOT to Use This Skill

- **Native app development** → Use React Native, Flutter, or native SDKs
- **General web performance** → Use Lighthouse/performance auditing tools
- **Server-side rendering issues** → Use Next.js/framework-specific docs
- **Push notifications only** → Consider dedicated push notification services
- **Simple static sites** → PWA overhead may not be worth it

## Core Concepts

### What Makes a PWA Installable

1. **HTTPS** (or localhost for dev)
2. **Web App Manifest** with required fields
3. **Service Worker** with fetch handler
4. **Icons** (192×192 and 512×512 minimum)

### The PWA Stack

```
┌─────────────────────────────────────────┐
│           Your App (React/Next.js)      │
├─────────────────────────────────────────┤
│         Service Worker (sw.js)          │
│  ┌─────────────┐  ┌─────────────────┐   │
│  │   Cache     │  │  Network Fetch  │   │
│  │   Storage   │  │    Handling     │   │
│  └─────────────┘  └─────────────────┘   │
├─────────────────────────────────────────┤
│          manifest.json                  │
│  (App identity, icons, display mode)    │
└─────────────────────────────────────────┘
```

## Web App Manifest

### Complete manifest.json

```json
{
  "name": "Junkie Buds 4 Life",
  "short_name": "JB4L",
  "description": "Recovery support app",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "orientation": "portrait-primary",
  "background_color": "#1a1410",
  "theme_color": "#1a1410",
  "icons": [
    {
      "src": "/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/icons/icon-maskable-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "maskable"
    }
  ],
  "shortcuts": [
    {
      "name": "Find Meetings",
      "short_name": "Meetings",
      "url": "/meetings?source=shortcut",
      "icons": [{ "src": "/icons/meetings-96.png", "sizes": "96x96" }]
    }
  ]
}
```

### Display Modes

| Mode | Description |
|------|-------------|
| `fullscreen` | No browser UI, full screen |
| `standalone` | App-like, no URL bar (recommended) |
| `minimal-ui` | Some browser controls |
| `browser` | Normal browser tab |

### Link in HTML

```html
<head>
  <link rel="manifest" href="/manifest.json" />
  <meta name="theme-color" content="#1a1410" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
  <link rel="apple-touch-icon" href="/icons/apple-touch-icon.png" />
</head>
```

## Service Worker Basics

### Registration

```typescript
// lib/pwa.ts
export async function registerServiceWorker() {
  if ('serviceWorker' in navigator) {
    try {
      const registration = await navigator.serviceWorker.register('/sw.js', {
        scope: '/',
      });
      return registration;
    } catch (error) {
      console.error('SW registration failed:', error);
    }
  }
}

// Call on app mount
useEffect(() => {
  registerServiceWorker();
}, []);
```

### Basic Service Worker Structure

```javascript
// public/sw.js
const CACHE_NAME = 'myapp-v1';
const STATIC_ASSETS = ['/', '/offline', '/manifest.json'];

// Install: Cache static assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

// Activate: Clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Fetch: Handle requests (see references for strategies)
self.addEventListener('fetch', (event) => {
  event.respondWith(handleFetch(event.request));
});
```

> **See:** `references/service-worker-patterns.md` for caching strategy implementations

## Caching Strategies

| Strategy | Best For | Tradeoff |
|----------|----------|----------|
| Cache-First | Static assets, fonts, images | Stale until cache updated |
| Network-First | API data, user content | Slower, needs connectivity |
| Stale-While-Revalidate | Balance freshness/speed | Background updates |
| Network-Only | Auth, real-time data | No offline support |
| Cache-Only | Versioned assets | Never updates |

> **See:** `references/service-worker-patterns.md` for full implementations

## Install Prompts

Handle the `beforeinstallprompt` event to show a custom install UI:

```typescript
// Basic pattern
const [deferredPrompt, setDeferredPrompt] = useState(null);

useEffect(() => {
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    setDeferredPrompt(e);
  });
}, []);

const handleInstall = async () => {
  if (deferredPrompt) {
    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    // outcome: 'accepted' or 'dismissed'
  }
};
```

> **See:** `references/install-prompt.md` for full `usePWAInstall` hook and component

## Offline Experience

Key patterns:
- Offline page fallback for navigation failures
- `useOnlineStatus` hook to detect connectivity
- Offline banner to inform users

> **See:** `references/offline-handling.md` for implementations

## Background Sync

Queue actions while offline, execute when connectivity returns:

```javascript
// In Service Worker
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-data') {
    event.waitUntil(syncPendingData());
  }
});

// In App - trigger sync
const registration = await navigator.serviceWorker.ready;
await registration.sync.register('sync-data');
```

> **See:** `references/background-sync.md` for full IndexedDB integration

## Update Flow

Notify users when a new version is available:

```typescript
// Basic pattern
registration.addEventListener('updatefound', () => {
  const newWorker = registration.installing;
  newWorker?.addEventListener('statechange', () => {
    if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
      // New version available - show update prompt
    }
  });
});
```

> **See:** `references/update-flow.md` for `usePWAUpdate` hook and update strategies

## Next.js Integration

Options for Next.js PWA:

1. **next-pwa** - Works with standard Next.js server
2. **Custom SW** - Required for `output: 'export'` (static sites)
3. **Workbox CLI** - Generate SW after build

> **See:** `references/nextjs-integration.md` for detailed configurations

## Quick Reference

| Task | Solution |
|------|----------|
| Check if installed | `window.matchMedia('(display-mode: standalone)').matches` |
| Force SW update | `registration.update()` |
| Clear all caches | `caches.keys().then(keys => keys.forEach(k => caches.delete(k)))` |
| Check online | `navigator.onLine` |
| Get SW registration | `navigator.serviceWorker.ready` |
| Skip waiting | `self.skipWaiting()` in SW |
| Take control | `self.clients.claim()` in SW |

## Testing PWA

### Chrome DevTools

1. **Application tab** → Manifest, Service Workers, Cache Storage
2. **Lighthouse** → PWA audit
3. **Network** → Offline checkbox to simulate

### Debug Checklist

- [ ] Manifest loads (Application → Manifest)
- [ ] SW registered (Application → Service Workers)
- [ ] Cache populated (Application → Cache Storage)
- [ ] Install prompt fires (Console for beforeinstallprompt)
- [ ] Offline page works (Network → Offline)
- [ ] Update flow works (trigger update, verify prompt)

## References

Detailed implementations in `/references/`:

- `service-worker-patterns.md` - Caching strategy implementations
- `install-prompt.md` - `usePWAInstall` hook and install component
- `offline-handling.md` - Offline page, status hooks, banners
- `background-sync.md` - Background sync with IndexedDB
- `update-flow.md` - Update detection and user prompts
- `nextjs-integration.md` - Next.js PWA configuration options
