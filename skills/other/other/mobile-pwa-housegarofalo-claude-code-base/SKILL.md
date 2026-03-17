---
name: mobile-pwa
description: Build Progressive Web Apps with offline support, push notifications, and native-like experiences. Covers service workers, Web App Manifest, caching strategies, IndexedDB, background sync, and installability. Use for mobile-first web apps, offline-capable applications, and app-like experiences.
---

# Progressive Web Apps (PWA)

Build installable, offline-capable web applications with native-like experiences.

## Instructions

1. **Start with responsive design** - PWAs must work on all screen sizes
2. **Implement offline-first** - Cache critical assets and data
3. **Add a manifest** - Enable installation on devices
4. **Use service workers** - Control network requests and caching
5. **Optimize performance** - Fast load times are critical for mobile

## Web App Manifest

```json
// public/manifest.json
{
  "name": "My Progressive Web App",
  "short_name": "MyPWA",
  "description": "An awesome PWA",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#2563eb",
  "orientation": "portrait-primary",
  "icons": [
    {
      "src": "/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ],
  "screenshots": [
    {
      "src": "/screenshots/home.png",
      "sizes": "1280x720",
      "type": "image/png",
      "form_factor": "wide"
    },
    {
      "src": "/screenshots/mobile.png",
      "sizes": "750x1334",
      "type": "image/png",
      "form_factor": "narrow"
    }
  ]
}
```

```html
<!-- index.html -->
<link rel="manifest" href="/manifest.json" />
<meta name="theme-color" content="#2563eb" />
<link rel="apple-touch-icon" href="/icons/icon-192.png" />
```

## Service Worker

### Registration

```tsx
// src/serviceWorkerRegistration.ts
export function register() {
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', async () => {
      try {
        const registration = await navigator.serviceWorker.register('/sw.js');
        console.log('SW registered:', registration.scope);

        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing;
          newWorker?.addEventListener('statechange', () => {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              // New content available
              dispatchEvent(new CustomEvent('swUpdate', { detail: registration }));
            }
          });
        });
      } catch (error) {
        console.error('SW registration failed:', error);
      }
    });
  }
}
```

### Service Worker Implementation

```js
// public/sw.js
const CACHE_NAME = 'app-v1';
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/static/js/main.js',
  '/static/css/main.css',
  '/manifest.json',
];

// Install - cache static assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS);
    })
  );
  self.skipWaiting();
});

// Activate - clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME)
          .map((name) => caches.delete(name))
      );
    })
  );
  self.clients.claim();
});

// Fetch - cache-first for static, network-first for API
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  if (url.pathname.startsWith('/api/')) {
    // Network first for API calls
    event.respondWith(networkFirst(request));
  } else {
    // Cache first for static assets
    event.respondWith(cacheFirst(request));
  }
});

async function cacheFirst(request) {
  const cached = await caches.match(request);
  if (cached) return cached;

  const response = await fetch(request);
  if (response.ok) {
    const cache = await caches.open(CACHE_NAME);
    cache.put(request, response.clone());
  }
  return response;
}

async function networkFirst(request) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    return caches.match(request);
  }
}
```

## IndexedDB for Offline Data

```tsx
// src/lib/db.ts
import { openDB, DBSchema } from 'idb';

interface MyDB extends DBSchema {
  items: {
    key: string;
    value: {
      id: string;
      title: string;
      content: string;
      synced: boolean;
      updatedAt: number;
    };
    indexes: { 'by-synced': boolean };
  };
}

const dbPromise = openDB<MyDB>('my-app-db', 1, {
  upgrade(db) {
    const store = db.createObjectStore('items', { keyPath: 'id' });
    store.createIndex('by-synced', 'synced');
  },
});

export const db = {
  async getAll() {
    return (await dbPromise).getAll('items');
  },

  async get(id: string) {
    return (await dbPromise).get('items', id);
  },

  async put(item: MyDB['items']['value']) {
    return (await dbPromise).put('items', {
      ...item,
      updatedAt: Date.now(),
    });
  },

  async delete(id: string) {
    return (await dbPromise).delete('items', id);
  },

  async getUnsynced() {
    return (await dbPromise).getAllFromIndex('items', 'by-synced', false);
  },
};
```

## Push Notifications

### Request Permission

```tsx
async function requestNotificationPermission() {
  if (!('Notification' in window)) {
    return 'unsupported';
  }

  if (Notification.permission === 'granted') {
    return 'granted';
  }

  if (Notification.permission !== 'denied') {
    const permission = await Notification.requestPermission();
    return permission;
  }

  return 'denied';
}
```

### Subscribe to Push

```tsx
async function subscribeToPush() {
  const registration = await navigator.serviceWorker.ready;

  const subscription = await registration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: urlBase64ToUint8Array(VAPID_PUBLIC_KEY),
  });

  // Send subscription to backend
  await fetch('/api/push/subscribe', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(subscription),
  });

  return subscription;
}
```

### Handle Push in Service Worker

```js
// sw.js
self.addEventListener('push', (event) => {
  const data = event.data?.json() ?? {};

  const options = {
    body: data.body,
    icon: '/icons/icon-192.png',
    badge: '/icons/badge-72.png',
    vibrate: [100, 50, 100],
    data: { url: data.url },
    actions: [
      { action: 'open', title: 'Open' },
      { action: 'dismiss', title: 'Dismiss' },
    ],
  };

  event.waitUntil(
    self.registration.showNotification(data.title, options)
  );
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();

  if (event.action === 'open' || !event.action) {
    event.waitUntil(
      clients.openWindow(event.notification.data.url || '/')
    );
  }
});
```

## Install Prompt

```tsx
function useInstallPrompt() {
  const [prompt, setPrompt] = useState<BeforeInstallPromptEvent | null>(null);
  const [isInstalled, setIsInstalled] = useState(false);

  useEffect(() => {
    const handleBeforeInstall = (e: BeforeInstallPromptEvent) => {
      e.preventDefault();
      setPrompt(e);
    };

    const handleInstalled = () => {
      setIsInstalled(true);
      setPrompt(null);
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstall);
    window.addEventListener('appinstalled', handleInstalled);

    // Check if already installed
    if (window.matchMedia('(display-mode: standalone)').matches) {
      setIsInstalled(true);
    }

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstall);
      window.removeEventListener('appinstalled', handleInstalled);
    };
  }, []);

  const install = async () => {
    if (!prompt) return false;

    prompt.prompt();
    const { outcome } = await prompt.userChoice;
    setPrompt(null);

    return outcome === 'accepted';
  };

  return { canInstall: !!prompt, isInstalled, install };
}

// Usage
function InstallBanner() {
  const { canInstall, install } = useInstallPrompt();

  if (!canInstall) return null;

  return (
    <div className="fixed bottom-0 inset-x-0 p-4 bg-blue-600 text-white">
      <div className="flex items-center justify-between max-w-lg mx-auto">
        <span>Install our app for a better experience</span>
        <button onClick={install} className="px-4 py-2 bg-white text-blue-600 rounded-lg">
          Install
        </button>
      </div>
    </div>
  );
}
```

## Offline Detection

```tsx
function useOnlineStatus() {
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

function OfflineBanner() {
  const isOnline = useOnlineStatus();

  if (isOnline) return null;

  return (
    <div className="bg-yellow-100 border-b border-yellow-200 p-2 text-center text-yellow-800">
      You're offline. Some features may be unavailable.
    </div>
  );
}
```

## PWA Checklist

- [ ] Responsive on all devices
- [ ] Works offline (at minimum, shows offline page)
- [ ] Has web app manifest
- [ ] Uses HTTPS
- [ ] Loads fast (< 3s on 3G)
- [ ] Uses service worker
- [ ] Has proper icons (192x192, 512x512)
- [ ] Provides install experience
- [ ] Handles network errors gracefully

## When to Use

- Mobile-first web applications
- Apps needing offline functionality
- Content that should be installable
- Apps replacing native mobile apps
- Engagement-focused applications with push notifications

## Notes

- Test on actual mobile devices
- Lighthouse PWA audit is essential
- Safari has limited PWA support (no push, limited caching)
- Background sync requires browser support
- Keep service worker updates seamless
