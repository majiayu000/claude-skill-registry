---
name: react-pwa
description: Build Progressive Web Apps with React and Vite. This skill should be used when the user asks to "create a PWA", "add offline support", "make app installable", "generate service worker", "configure workbox", "add push notifications", or mentions PWA, progressive web app, or offline-first development. Keywords: PWA, progressive web app, service worker, manifest, offline, installable, workbox, vite-plugin-pwa, React.
license: MIT
compatibility: Requires Deno for scripts. Works with React 18+ and Vite 5+.
metadata:
  author: agent-skills
  version: "1.0"
---

# React PWA

Build Progressive Web Apps with React and Vite using vite-plugin-pwa. This skill covers the complete PWA lifecycle: manifest configuration, service worker strategies, offline support, installability, and push notifications.

## When to Use This Skill

**Use when**:
- Creating a new PWA from scratch with React + Vite
- Converting an existing React app to a PWA
- Adding offline capabilities to a web application
- Implementing install prompts and app-like experiences
- Setting up push notifications
- Optimizing caching strategies for performance

**Don't use when**:
- Building server-rendered apps without client-side caching needs
- Working with Next.js (use next-pwa instead)
- Simple static sites without offline requirements

## Prerequisites

- **Node.js** 18+ and npm/pnpm/yarn
- **Vite** 5+ with React template
- **Deno** runtime (for skill scripts)
- **Source icon**: 512x512 PNG or SVG for icon generation

## Quick Start

### 1. Install Dependencies

```bash
npm install -D vite-plugin-pwa workbox-window
```

### 2. Configure Vite

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.ico', 'apple-touch-icon.png', 'mask-icon.svg'],
      manifest: {
        name: 'My React PWA',
        short_name: 'ReactPWA',
        description: 'A Progressive Web App built with React',
        theme_color: '#ffffff',
        background_color: '#ffffff',
        display: 'standalone',
        icons: [
          { src: 'pwa-192x192.png', sizes: '192x192', type: 'image/png' },
          { src: 'pwa-512x512.png', sizes: '512x512', type: 'image/png' },
          { src: 'pwa-512x512.png', sizes: '512x512', type: 'image/png', purpose: 'maskable' }
        ]
      }
    })
  ]
})
```

### 3. Generate Icons

```bash
deno run --allow-read --allow-write scripts/generate-icons.ts --input logo.png --output public/
```

### 4. Add Update Prompt (Optional)

```tsx
// src/components/PWAUpdatePrompt.tsx
import { useRegisterSW } from 'virtual:pwa-register/react'

export function PWAUpdatePrompt() {
  const {
    needRefresh: [needRefresh, setNeedRefresh],
    updateServiceWorker
  } = useRegisterSW()

  if (!needRefresh) return null

  return (
    <div className="pwa-toast">
      <span>New content available!</span>
      <button onClick={() => updateServiceWorker(true)}>Reload</button>
      <button onClick={() => setNeedRefresh(false)}>Close</button>
    </div>
  )
}
```

---

## Instructions

### Phase 1: Project Setup

#### 1a. Create New Vite React Project

```bash
npm create vite@latest my-pwa -- --template react-ts
cd my-pwa
npm install
npm install -D vite-plugin-pwa workbox-window
```

#### 1b. Add to Existing Project

```bash
npm install -D vite-plugin-pwa workbox-window
```

Add TypeScript types for virtual modules:

```typescript
// src/vite-env.d.ts (add to existing file)
/// <reference types="vite-plugin-pwa/client" />
```

---

### Phase 2: Manifest Configuration

The web app manifest defines how the PWA appears when installed.

#### Required Fields

```json
{
  "name": "Full Application Name",
  "short_name": "ShortName",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#3b82f6",
  "icons": []
}
```

#### Display Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| `fullscreen` | No browser UI, fills entire screen | Games, immersive experiences |
| `standalone` | App-like, with system UI only | Most PWAs |
| `minimal-ui` | Minimal browser controls | Apps needing navigation |
| `browser` | Standard browser tab | Fallback only |

#### Generate Manifest

```bash
deno run --allow-read --allow-write scripts/generate-manifest.ts \
  --name "My App" \
  --short-name "App" \
  --theme "#3b82f6" \
  --output public/manifest.webmanifest
```

---

### Phase 3: Service Worker Strategies

vite-plugin-pwa uses Workbox under the hood. Choose a strategy based on your needs.

#### Strategy Options

| Strategy | Behavior | Best For |
|----------|----------|----------|
| `generateSW` | Auto-generates SW from config | Most projects |
| `injectManifest` | Injects precache into custom SW | Custom caching logic |

#### Caching Strategies

**CacheFirst** - Serve from cache, fall back to network:
```typescript
runtimeCaching: [
  {
    urlPattern: /^https:\/\/fonts\.googleapis\.com\/.*/i,
    handler: 'CacheFirst',
    options: {
      cacheName: 'google-fonts-cache',
      expiration: { maxEntries: 10, maxAgeSeconds: 60 * 60 * 24 * 365 }
    }
  }
]
```

**NetworkFirst** - Try network, fall back to cache:
```typescript
{
  urlPattern: /^https:\/\/api\.example\.com\/.*/i,
  handler: 'NetworkFirst',
  options: {
    cacheName: 'api-cache',
    expiration: { maxEntries: 50, maxAgeSeconds: 60 * 60 * 24 }
  }
}
```

**StaleWhileRevalidate** - Serve cache immediately, update in background:
```typescript
{
  urlPattern: /\.(?:png|jpg|jpeg|svg|gif)$/,
  handler: 'StaleWhileRevalidate',
  options: {
    cacheName: 'images-cache',
    expiration: { maxEntries: 100, maxAgeSeconds: 60 * 60 * 24 * 30 }
  }
}
```

#### Complete Vite Config with Caching

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg,woff2}'],
        runtimeCaching: [
          {
            urlPattern: /^https:\/\/api\..*/i,
            handler: 'NetworkFirst',
            options: {
              cacheName: 'api-cache',
              expiration: { maxEntries: 100, maxAgeSeconds: 60 * 60 * 24 }
            }
          },
          {
            urlPattern: /\.(?:png|jpg|jpeg|svg|gif|webp)$/,
            handler: 'CacheFirst',
            options: {
              cacheName: 'images',
              expiration: { maxEntries: 100, maxAgeSeconds: 60 * 60 * 24 * 30 }
            }
          }
        ]
      },
      manifest: {
        name: 'My React PWA',
        short_name: 'ReactPWA',
        theme_color: '#3b82f6',
        background_color: '#ffffff',
        display: 'standalone',
        icons: [
          { src: 'pwa-192x192.png', sizes: '192x192', type: 'image/png' },
          { src: 'pwa-512x512.png', sizes: '512x512', type: 'image/png' },
          { src: 'pwa-512x512.png', sizes: '512x512', type: 'image/png', purpose: 'maskable' }
        ]
      }
    })
  ]
})
```

---

### Phase 4: Offline Support

#### 4a. Offline Fallback Page

Create an offline page that displays when network and cache both fail:

```typescript
// vite.config.ts - add to VitePWA options
workbox: {
  navigateFallback: '/offline.html',
  navigateFallbackDenylist: [/^\/api/]
}
```

Create `public/offline.html`:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Offline</title>
  <style>
    body { font-family: system-ui; display: flex; align-items: center;
           justify-content: center; min-height: 100vh; margin: 0; }
    .offline { text-align: center; }
  </style>
</head>
<body>
  <div class="offline">
    <h1>You're offline</h1>
    <p>Please check your internet connection and try again.</p>
    <button onclick="window.location.reload()">Retry</button>
  </div>
</body>
</html>
```

#### 4b. Offline Detection Hook

```tsx
// src/hooks/useOnlineStatus.ts
import { useSyncExternalStore } from 'react'

function subscribe(callback: () => void) {
  window.addEventListener('online', callback)
  window.addEventListener('offline', callback)
  return () => {
    window.removeEventListener('online', callback)
    window.removeEventListener('offline', callback)
  }
}

export function useOnlineStatus() {
  return useSyncExternalStore(
    subscribe,
    () => navigator.onLine,
    () => true // SSR fallback
  )
}
```

Usage:
```tsx
function App() {
  const isOnline = useOnlineStatus()

  return (
    <div>
      {!isOnline && <Banner>You are offline. Some features may be limited.</Banner>}
      {/* ... */}
    </div>
  )
}
```

---

### Phase 5: Install Prompt

#### 5a. Install Button Component

```tsx
// src/components/InstallButton.tsx
import { useState, useEffect } from 'react'

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>
}

export function InstallButton() {
  const [deferredPrompt, setDeferredPrompt] = useState<BeforeInstallPromptEvent | null>(null)
  const [isInstalled, setIsInstalled] = useState(false)

  useEffect(() => {
    // Check if already installed
    if (window.matchMedia('(display-mode: standalone)').matches) {
      setIsInstalled(true)
      return
    }

    const handler = (e: Event) => {
      e.preventDefault()
      setDeferredPrompt(e as BeforeInstallPromptEvent)
    }

    window.addEventListener('beforeinstallprompt', handler)
    window.addEventListener('appinstalled', () => setIsInstalled(true))

    return () => window.removeEventListener('beforeinstallprompt', handler)
  }, [])

  const handleInstall = async () => {
    if (!deferredPrompt) return

    deferredPrompt.prompt()
    const { outcome } = await deferredPrompt.userChoice

    if (outcome === 'accepted') {
      setDeferredPrompt(null)
    }
  }

  if (isInstalled || !deferredPrompt) return null

  return (
    <button onClick={handleInstall} className="install-btn">
      Install App
    </button>
  )
}
```

---

### Phase 6: Push Notifications

#### 6a. Request Permission

```typescript
async function requestNotificationPermission(): Promise<boolean> {
  if (!('Notification' in window)) {
    console.warn('Notifications not supported')
    return false
  }

  if (Notification.permission === 'granted') return true
  if (Notification.permission === 'denied') return false

  const permission = await Notification.requestPermission()
  return permission === 'granted'
}
```

#### 6b. Subscribe to Push

```typescript
async function subscribeToPush(vapidPublicKey: string): Promise<PushSubscription | null> {
  const registration = await navigator.serviceWorker.ready

  const subscription = await registration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: urlBase64ToUint8Array(vapidPublicKey)
  })

  // Send subscription to your backend
  await fetch('/api/push/subscribe', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(subscription)
  })

  return subscription
}

function urlBase64ToUint8Array(base64String: string): Uint8Array {
  const padding = '='.repeat((4 - base64String.length % 4) % 4)
  const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/')
  const rawData = window.atob(base64)
  return Uint8Array.from([...rawData].map(char => char.charCodeAt(0)))
}
```

#### 6c. Handle Push in Service Worker (injectManifest mode)

```typescript
// src/sw.ts
import { precacheAndRoute } from 'workbox-precaching'

declare const self: ServiceWorkerGlobalScope

precacheAndRoute(self.__WB_MANIFEST)

self.addEventListener('push', (event) => {
  const data = event.data?.json() ?? { title: 'Notification', body: 'New update available' }

  event.waitUntil(
    self.registration.showNotification(data.title, {
      body: data.body,
      icon: '/pwa-192x192.png',
      badge: '/badge-72x72.png'
    })
  )
})

self.addEventListener('notificationclick', (event) => {
  event.notification.close()
  event.waitUntil(
    self.clients.openWindow('/')
  )
})
```

---

## Examples

### Example 1: Basic PWA Setup

**Scenario**: Convert a Vite React app to an installable PWA with offline support.

**Steps**:
1. Install dependencies: `npm install -D vite-plugin-pwa`
2. Add VitePWA plugin to vite.config.ts
3. Generate icons from source image
4. Build and test: `npm run build && npm run preview`
5. Verify in Chrome DevTools > Application > Manifest

**Verification**:
- Lighthouse PWA audit passes
- App is installable (install icon in address bar)
- Works offline after first load

### Example 2: API-Heavy App with Smart Caching

**Scenario**: E-commerce app with product API calls that should work offline after browsing.

```typescript
VitePWA({
  workbox: {
    runtimeCaching: [
      // Cache product images aggressively
      {
        urlPattern: /\/products\/images\/.*/,
        handler: 'CacheFirst',
        options: {
          cacheName: 'product-images',
          expiration: { maxEntries: 200, maxAgeSeconds: 60 * 60 * 24 * 7 }
        }
      },
      // Cache API responses with network-first
      {
        urlPattern: /\/api\/products\/.*/,
        handler: 'NetworkFirst',
        options: {
          cacheName: 'product-api',
          expiration: { maxEntries: 100, maxAgeSeconds: 60 * 60 },
          networkTimeoutSeconds: 3
        }
      }
    ]
  }
})
```

### Example 3: Periodic Background Sync

**Scenario**: News app that syncs content in background.

```typescript
// Register periodic sync
const registration = await navigator.serviceWorker.ready
await registration.periodicSync.register('sync-articles', {
  minInterval: 60 * 60 * 1000 // 1 hour
})

// Handle in service worker
self.addEventListener('periodicsync', (event) => {
  if (event.tag === 'sync-articles') {
    event.waitUntil(syncArticles())
  }
})
```

---

## Script Reference

| Script | Purpose | Permissions |
|--------|---------|-------------|
| `generate-manifest.ts` | Create manifest.webmanifest | `--allow-read --allow-write` |
| `generate-icons.ts` | Generate icon set from source | `--allow-read --allow-write --allow-run` |
| `generate-sw-config.ts` | Create service worker config | `--allow-read --allow-write` |
| `audit-pwa.ts` | Validate PWA compliance | `--allow-read --allow-net` |

### Generate Manifest

```bash
deno run --allow-read --allow-write scripts/generate-manifest.ts \
  --name "My Application" \
  --short-name "MyApp" \
  --description "A great PWA" \
  --theme "#3b82f6" \
  --background "#ffffff" \
  --display standalone \
  --output public/manifest.webmanifest
```

### Generate Icons

```bash
deno run --allow-read --allow-write --allow-run scripts/generate-icons.ts \
  --input logo.svg \
  --output public/ \
  --sizes 192,512 \
  --maskable
```

### Audit PWA

```bash
deno run --allow-read --allow-net scripts/audit-pwa.ts \
  --url http://localhost:5173 \
  --format summary
```

---

## Common Issues

### Issue: Service Worker Not Updating

**Symptoms**: Old content served after deployment.

**Solution**:
1. Ensure `registerType: 'autoUpdate'` is set
2. Add update prompt component to notify users
3. For immediate updates in development: Chrome DevTools > Application > Service Workers > Update on reload

### Issue: App Not Installable

**Symptoms**: No install prompt, Lighthouse fails installability.

**Solution**:
1. Verify manifest has all required fields (name, short_name, icons, start_url, display)
2. Ensure icons are at least 192x192 and 512x512
3. Serve over HTTPS (or localhost for development)
4. Check for service worker registration errors in console

### Issue: Caching API Responses Causes Stale Data

**Symptoms**: Users see outdated data.

**Solution**:
1. Use `NetworkFirst` strategy for dynamic API endpoints
2. Add `networkTimeoutSeconds` for faster fallback
3. Implement cache versioning with expiration

### Issue: Push Notifications Not Working

**Symptoms**: Subscription succeeds but notifications don't arrive.

**Solution**:
1. Verify VAPID keys match between frontend and backend
2. Check service worker is active (not waiting)
3. Ensure `userVisibleOnly: true` in subscription
4. Test push delivery with web-push CLI tool

---

## Additional Resources

### Reference Files
- **`references/caching-strategies.md`** - Deep dive into Workbox caching patterns
- **`references/push-notifications.md`** - Complete push notification backend setup
- **`references/testing-pwas.md`** - Testing strategies for PWA features

### Assets
- **`assets/manifest-template.json`** - Complete manifest with all optional fields
- **`assets/sw-template.ts`** - Custom service worker template for injectManifest

---

## Limitations

- Push notifications require a backend server with web-push
- Background sync has limited browser support (Chrome/Edge)
- iOS Safari has PWA limitations (no push notifications, limited storage)
- Service worker debugging can be complex

## Related Skills

- **frontend-design** - Design systems and component styling
- **web-search** - Research PWA best practices and browser support
