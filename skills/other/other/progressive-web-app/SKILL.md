---
name: progressive-web-app
description: Build progressive web apps using service workers, web manifest, offline support, and installability. Use when creating app-like web experiences.
---

# Progressive Web App

## Overview

Build progressive web applications with offline support, installability, service workers, and web app manifests to deliver app-like experiences in the browser.

## When to Use

- App-like web experiences
- Offline functionality needed
- Mobile installation required
- Push notifications
- Fast loading experiences

## Implementation Examples

### 1. **Web App Manifest**

```json
// public/manifest.json
{
  "name": "My Awesome App",
  "short_name": "AwesomeApp",
  "description": "A progressive web application",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "orientation": "portrait-primary",
  "background_color": "#ffffff",
  "theme_color": "#007bff",
  "icons": [
    {
      "src": "/images/icon-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/images/icon-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/images/icon-maskable-192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "maskable"
    },
    {
      "src": "/images/icon-maskable-512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "maskable"
    }
  ],
  "screenshots": [
    {
      "src": "/images/screenshot-1.png",
      "sizes": "540x720",
      "type": "image/png",
      "form_factor": "narrow"
    },
    {
      "src": "/images/screenshot-2.png",
      "sizes": "1280x720",
      "type": "image/png",
      "form_factor": "wide"
    }
  ],
  "categories": ["productivity", "utilities"],
  "shortcuts": [
    {
      "name": "Quick Note",
      "short_name": "Note",
      "description": "Create a quick note",
      "url": "/new-note",
      "icons": [
        {
          "src": "/images/note-icon.png",
          "sizes": "192x192"
        }
      ]
    }
  ]
}
```

```html
<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#007bff">
  <link rel="manifest" href="/manifest.json">
  <link rel="icon" href="/favicon.ico">
  <link rel="apple-touch-icon" href="/images/icon-192.png">
  <title>My Awesome App</title>
</head>
<body>
  <div id="root"></div>
</body>
</html>
```

### 2. **Service Worker Implementation**

```typescript
// public/service-worker.ts
const CACHE_NAME = 'app-v1';
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/css/main.css',
  '/js/app.js',
  '/images/icon-192.png',
  '/offline.html'
];

// Install event
self.addEventListener('install', (event: ExtendableEvent) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(STATIC_ASSETS);
    })
  );
  self.skipWaiting();
});

// Activate event
self.addEventListener('activate', (event: ExtendableEvent) => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames
          .filter(name => name !== CACHE_NAME)
          .map(name => caches.delete(name))
      );
    })
  );
  self.clients.claim();
});

// Fetch event with cache-first strategy for static assets
self.addEventListener('fetch', (event: FetchEvent) => {
  const { request } = event;

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // Cache first for static assets
  if (request.destination === 'image' || request.destination === 'font') {
    event.respondWith(
      caches.match(request).then(response => {
        return response || fetch(request).then(res => {
          if (res.ok) {
            const clone = res.clone();
            caches.open(CACHE_NAME).then(cache => {
              cache.put(request, clone);
            });
          }
          return res;
        });
      }).catch(() => {
        return caches.match('/offline.html');
      })
    );
  }

  // Network first for API calls
  if (request.url.includes('/api/')) {
    event.respondWith(
      fetch(request)
        .then(response => {
          if (response.ok) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then(cache => {
              cache.put(request, clone);
            });
          }
          return response;
        })
        .catch(() => {
          return caches.match(request);
        })
    );
  }

  // Stale while revalidate for HTML
  if (request.destination === 'document') {
    event.respondWith(
      caches.match(request).then(cachedResponse => {
        const fetchPromise = fetch(request).then(response => {
          if (response.ok) {
            caches.open(CACHE_NAME).then(cache => {
              cache.put(request, response.clone());
            });
          }
          return response;
        });

        return cachedResponse || fetchPromise;
      })
    );
  }
});

// Background Sync
self.addEventListener('sync', (event: any) => {
  if (event.tag === 'sync-notes') {
    event.waitUntil(syncNotes());
  }
});

async function syncNotes() {
  const db = await openDB('notes');
  const unsynced = await db.getAll('keyval', IDBKeyRange.bound('pending_', 'pending_\uffff'));

  for (const item of unsynced) {
    try {
      await fetch('/api/notes', {
        method: 'POST',
        body: JSON.stringify(item.value)
      });
      await db.delete('keyval', item.key);
    } catch (error) {
      console.error('Sync failed:', error);
    }
  }
}
```

### 3. **Install Prompt and App Installation**

```typescript
// hooks/useInstallPrompt.ts
import { useState, useEffect } from 'react';

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
}

export const useInstallPrompt = () => {
  const [promptEvent, setPromptEvent] = useState<BeforeInstallPromptEvent | null>(null);
  const [isInstalled, setIsInstalled] = useState(false);
  const [isIOSInstalled, setIsIOSInstalled] = useState(false);

  useEffect(() => {
    const handleBeforeInstallPrompt = (e: Event) => {
      e.preventDefault();
      setPromptEvent(e as BeforeInstallPromptEvent);
    };

    const handleAppInstalled = () => {
      setIsInstalled(true);
      setPromptEvent(null);
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    window.addEventListener('appinstalled', handleAppInstalled);

    // Check if running as installed app
    if (window.matchMedia('(display-mode: standalone)').matches) {
      setIsInstalled(true);
    }

    // Check iOS
    const isIOSDevice = /iPad|iPhone|iPod/.test(navigator.userAgent);
    const isIOSApp = navigator.standalone === true;
    if (isIOSDevice && !isIOSApp) {
      setIsIOSInstalled(false);
    }

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
      window.removeEventListener('appinstalled', handleAppInstalled);
    };
  }, []);

  const installApp = async () => {
    if (promptEvent) {
      await promptEvent.prompt();
      const { outcome } = await promptEvent.userChoice;
      if (outcome === 'accepted') {
        setIsInstalled(true);
      }
      setPromptEvent(null);
    }
  };

  return {
    promptEvent,
    canInstall: promptEvent !== null,
    isInstalled,
    isIOSInstalled,
    installApp
  };
};

// components/InstallPrompt.tsx
export const InstallPrompt: React.FC = () => {
  const { canInstall, isInstalled, installApp } = useInstallPrompt();

  if (isInstalled || !canInstall) return null;

  return (
    <div className="install-prompt">
      <h2>Install App</h2>
      <p>Install our app for quick access and offline support</p>
      <button onClick={installApp}>Install</button>
    </div>
  );
};
```

### 4. **Offline Support with IndexedDB**

```typescript
// db/notesDB.ts
import { openDB, DBSchema, IDBPDatabase } from 'idb';

interface Note {
  id: string;
  title: string;
  content: string;
  timestamp: number;
  synced: boolean;
}

interface NotesDB extends DBSchema {
  notes: {
    key: string;
    value: Note;
    indexes: { 'by-timestamp': number; 'by-synced': boolean };
  };
}

let db: IDBPDatabase<NotesDB>;

export async function initDB() {
  db = await openDB<NotesDB>('notes-db', 1, {
    upgrade(db) {
      const store = db.createObjectStore('notes', { keyPath: 'id' });
      store.createIndex('by-timestamp', 'timestamp');
      store.createIndex('by-synced', 'synced');
    }
  });
  return db;
}

export async function addNote(note: Omit<Note, 'timestamp'>) {
  return db.add('notes', {
    ...note,
    timestamp: Date.now(),
    synced: false
  });
}

export async function getNotes(): Promise<Note[]> {
  return db.getAll('notes');
}

export async function getUnsyncedNotes(): Promise<Note[]> {
  return db.getAllFromIndex('notes', 'by-synced', false);
}

export async function updateNote(id: string, updates: Partial<Note>) {
  const note = await db.get('notes', id);
  if (note) {
    await db.put('notes', { ...note, ...updates });
  }
}

export async function markAsSynced(id: string) {
  await updateNote(id, { synced: true });
}
```

### 5. **Push Notifications**

```typescript
// services/pushNotification.ts
export async function subscribeToPushNotifications() {
  if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
    console.log('Push notifications not supported');
    return;
  }

  try {
    const registration = await navigator.serviceWorker.ready;
    const subscription = await registration.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: process.env.REACT_APP_VAPID_PUBLIC_KEY
    });

    // Send subscription to server
    await fetch('/api/push-subscription', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(subscription)
    });

    return subscription;
  } catch (error) {
    console.error('Push subscription failed:', error);
  }
}

// service-worker.ts
self.addEventListener('push', (event: PushEvent) => {
  const data = event.data?.json() ?? {};
  const options: NotificationOptions = {
    title: data.title || 'New Notification',
    body: data.message || '',
    icon: '/images/icon-192.png',
    badge: '/images/badge-72.png',
    tag: data.tag || 'notification'
  };

  event.waitUntil(
    self.registration.showNotification(options.title, options)
  );
});

self.addEventListener('notificationclick', (event: NotificationEvent) => {
  event.notification.close();
  event.waitUntil(
    self.clients.matchAll({ type: 'window' }).then(clients => {
      if (clients.length > 0) {
        return clients[0].focus();
      }
      return self.clients.openWindow('/');
    })
  );
});
```

## Best Practices

- Implement service workers for offline support
- Create comprehensive web app manifest
- Use cache strategies appropriate for content type
- Provide offline fallback pages
- Test on various network conditions
- Optimize for slow 3G networks
- Include installation prompts
- Use IndexedDB for local storage
- Monitor sync status and connectivity
- Handle update notifications gracefully

## Resources

- [Web.dev Progressive Web Apps](https://web.dev/progressive-web-apps/)
- [Service Workers API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [Web App Manifest](https://developer.mozilla.org/en-US/docs/Web/Manifest)
- [IndexedDB API](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API)
- [Push API](https://developer.mozilla.org/en-US/docs/Web/API/Push_API)
