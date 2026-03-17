---
name: mobile-pwa
description: Build Progressive Web Apps and mobile-first experiences. Covers service workers, offline support, push notifications, app manifest, installability, React Native basics, and mobile UX patterns.
---

# Mobile & PWA Development

Expert guidance for building Progressive Web Apps and mobile-optimized experiences that feel native.

## When to Use This Skill

- Building Progressive Web Apps (PWAs)
- Implementing offline-first functionality
- Adding push notifications to web apps
- Creating installable web applications
- Optimizing for mobile devices
- Building with React Native basics
- Implementing mobile UX patterns

## Progressive Web App Fundamentals

### Web App Manifest

```json
{
  "name": "My Progressive Web App",
  "short_name": "MyPWA",
  "description": "A fast, reliable, and engaging app",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#3b82f6",
  "orientation": "portrait-primary",
  "icons": [
    {
      "src": "/icons/icon-72x72.png",
      "sizes": "72x72",
      "type": "image/png",
      "purpose": "maskable any"
    },
    {
      "src": "/icons/icon-96x96.png",
      "sizes": "96x96",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-128x128.png",
      "sizes": "128x128",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-144x144.png",
      "sizes": "144x144",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-152x152.png",
      "sizes": "152x152",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-384x384.png",
      "sizes": "384x384",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ],
  "screenshots": [
    {
      "src": "/screenshots/mobile.png",
      "sizes": "750x1334",
      "type": "image/png",
      "form_factor": "narrow"
    },
    {
      "src": "/screenshots/desktop.png",
      "sizes": "1280x720",
      "type": "image/png",
      "form_factor": "wide"
    }
  ],
  "shortcuts": [
    {
      "name": "New Item",
      "short_name": "New",
      "url": "/new",
      "icons": [{ "src": "/icons/new.png", "sizes": "96x96" }]
    }
  ],
  "categories": ["productivity", "utilities"],
  "share_target": {
    "action": "/share",
    "method": "POST",
    "enctype": "multipart/form-data",
    "params": {
      "title": "title",
      "text": "text",
      "url": "url",
      "files": [
        {
          "name": "media",
          "accept": ["image/*", "video/*"]
        }
      ]
    }
  }
}
```

### HTML Head Configuration

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">

  <!-- PWA Meta Tags -->
  <meta name="theme-color" content="#3b82f6">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="MyPWA">

  <!-- Manifest -->
  <link rel="manifest" href="/manifest.json">

  <!-- Apple Touch Icons -->
  <link rel="apple-touch-icon" href="/icons/icon-180x180.png">
  <link rel="apple-touch-icon" sizes="152x152" href="/icons/icon-152x152.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/icons/icon-180x180.png">

  <!-- Splash Screens for iOS -->
  <link rel="apple-touch-startup-image" href="/splash/apple-splash-2048-2732.png"
        media="(device-width: 1024px) and (device-height: 1366px)">

  <title>My PWA</title>
</head>
```

## Service Workers

### Basic Service Worker Registration

```typescript
// src/registerSW.ts
export async function registerServiceWorker(): Promise<ServiceWorkerRegistration | null> {
  if (!('serviceWorker' in navigator)) {
    console.log('Service workers not supported');
    return null;
  }

  try {
    const registration = await navigator.serviceWorker.register('/sw.js', {
      scope: '/',
      updateViaCache: 'none'
    });

    // Check for updates periodically
    setInterval(() => {
      registration.update();
    }, 60 * 60 * 1000); // Every hour

    // Handle updates
    registration.addEventListener('updatefound', () => {
      const newWorker = registration.installing;
      if (!newWorker) return;

      newWorker.addEventListener('statechange', () => {
        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
          // New content available, show update prompt
          dispatchEvent(new CustomEvent('swUpdate', { detail: registration }));
        }
      });
    });

    return registration;
  } catch (error) {
    console.error('SW registration failed:', error);
    return null;
  }
}

// Handle update prompt
export function promptUserToUpdate(registration: ServiceWorkerRegistration): void {
  if (confirm('New version available! Reload to update?')) {
    registration.waiting?.postMessage({ type: 'SKIP_WAITING' });
    window.location.reload();
  }
}
```

### Complete Service Worker with Caching Strategies

```typescript
// public/sw.js
const CACHE_VERSION = 'v1';
const STATIC_CACHE = `static-${CACHE_VERSION}`;
const DYNAMIC_CACHE = `dynamic-${CACHE_VERSION}`;
const IMAGE_CACHE = `images-${CACHE_VERSION}`;

// Assets to precache
const PRECACHE_ASSETS = [
  '/',
  '/index.html',
  '/styles/main.css',
  '/scripts/app.js',
  '/offline.html',
  '/icons/icon-192x192.png'
];

// Install event - precache static assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => cache.addAll(PRECACHE_ASSETS))
      .then(() => self.skipWaiting())
  );
});

// Activate event - clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys
          .filter(key => key !== STATIC_CACHE && key !== DYNAMIC_CACHE && key !== IMAGE_CACHE)
          .map(key => caches.delete(key))
      ))
      .then(() => self.clients.claim())
  );
});

// Fetch event - serve from cache with strategies
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') return;

  // Skip cross-origin requests
  if (url.origin !== location.origin) return;

  // API requests - Network First
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(networkFirst(request, DYNAMIC_CACHE));
    return;
  }

  // Images - Cache First with fallback
  if (request.destination === 'image') {
    event.respondWith(cacheFirst(request, IMAGE_CACHE));
    return;
  }

  // Static assets - Cache First
  if (PRECACHE_ASSETS.includes(url.pathname)) {
    event.respondWith(cacheFirst(request, STATIC_CACHE));
    return;
  }

  // Other requests - Stale While Revalidate
  event.respondWith(staleWhileRevalidate(request, DYNAMIC_CACHE));
});

// Caching Strategies
async function cacheFirst(request, cacheName) {
  const cached = await caches.match(request);
  if (cached) return cached;

  try {
    const response = await fetch(request);
    const cache = await caches.open(cacheName);
    cache.put(request, response.clone());
    return response;
  } catch {
    return caches.match('/offline.html');
  }
}

async function networkFirst(request, cacheName) {
  try {
    const response = await fetch(request);
    const cache = await caches.open(cacheName);
    cache.put(request, response.clone());
    return response;
  } catch {
    const cached = await caches.match(request);
    return cached || new Response(JSON.stringify({ error: 'Offline' }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

async function staleWhileRevalidate(request, cacheName) {
  const cached = await caches.match(request);

  const fetchPromise = fetch(request)
    .then(response => {
      const cache = caches.open(cacheName);
      cache.then(c => c.put(request, response.clone()));
      return response;
    })
    .catch(() => cached);

  return cached || fetchPromise;
}

// Handle skip waiting message
self.addEventListener('message', (event) => {
  if (event.data?.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
```

### Workbox Integration (Recommended)

```typescript
// sw.ts (using Workbox)
import { precacheAndRoute, cleanupOutdatedCaches } from 'workbox-precaching';
import { registerRoute, NavigationRoute } from 'workbox-routing';
import {
  CacheFirst,
  NetworkFirst,
  StaleWhileRevalidate
} from 'workbox-strategies';
import { ExpirationPlugin } from 'workbox-expiration';
import { CacheableResponsePlugin } from 'workbox-cacheable-response';

declare const self: ServiceWorkerGlobalScope;

// Precache assets from build
precacheAndRoute(self.__WB_MANIFEST);
cleanupOutdatedCaches();

// Cache Google Fonts
registerRoute(
  ({ url }) => url.origin === 'https://fonts.googleapis.com' ||
               url.origin === 'https://fonts.gstatic.com',
  new StaleWhileRevalidate({
    cacheName: 'google-fonts',
    plugins: [
      new ExpirationPlugin({ maxEntries: 30, maxAgeSeconds: 60 * 60 * 24 * 365 })
    ]
  })
);

// Cache images
registerRoute(
  ({ request }) => request.destination === 'image',
  new CacheFirst({
    cacheName: 'images',
    plugins: [
      new ExpirationPlugin({ maxEntries: 100, maxAgeSeconds: 60 * 60 * 24 * 30 }),
      new CacheableResponsePlugin({ statuses: [0, 200] })
    ]
  })
);

// API calls - Network First
registerRoute(
  ({ url }) => url.pathname.startsWith('/api/'),
  new NetworkFirst({
    cacheName: 'api-cache',
    plugins: [
      new ExpirationPlugin({ maxEntries: 50, maxAgeSeconds: 60 * 5 })
    ]
  })
);

// Navigation - Network First with offline fallback
registerRoute(
  new NavigationRoute(
    new NetworkFirst({
      cacheName: 'navigations',
      plugins: [
        new CacheableResponsePlugin({ statuses: [200] })
      ]
    }),
    {
      denylist: [/^\/_/, /\/api\//]
    }
  )
);
```

## Push Notifications

### Request Permission and Subscribe

```typescript
// src/notifications.ts
interface PushSubscriptionData {
  endpoint: string;
  keys: {
    p256dh: string;
    auth: string;
  };
}

export async function requestNotificationPermission(): Promise<NotificationPermission> {
  if (!('Notification' in window)) {
    console.log('Notifications not supported');
    return 'denied';
  }

  const permission = await Notification.requestPermission();
  return permission;
}

export async function subscribeToPush(): Promise<PushSubscriptionData | null> {
  try {
    const registration = await navigator.serviceWorker.ready;

    // Check for existing subscription
    let subscription = await registration.pushManager.getSubscription();

    if (!subscription) {
      // Create new subscription
      const vapidPublicKey = import.meta.env.VITE_VAPID_PUBLIC_KEY;
      subscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: urlBase64ToUint8Array(vapidPublicKey)
      });
    }

    // Send subscription to server
    const subscriptionData: PushSubscriptionData = {
      endpoint: subscription.endpoint,
      keys: {
        p256dh: arrayBufferToBase64(subscription.getKey('p256dh')),
        auth: arrayBufferToBase64(subscription.getKey('auth'))
      }
    };

    await fetch('/api/push/subscribe', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(subscriptionData)
    });

    return subscriptionData;
  } catch (error) {
    console.error('Push subscription failed:', error);
    return null;
  }
}

function urlBase64ToUint8Array(base64String: string): Uint8Array {
  const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
  const rawData = window.atob(base64);
  return Uint8Array.from([...rawData].map(char => char.charCodeAt(0)));
}

function arrayBufferToBase64(buffer: ArrayBuffer | null): string {
  if (!buffer) return '';
  return btoa(String.fromCharCode(...new Uint8Array(buffer)));
}
```

### Handle Push in Service Worker

```typescript
// In sw.js
self.addEventListener('push', (event) => {
  const data = event.data?.json() ?? {
    title: 'New Notification',
    body: 'You have a new message'
  };

  const options = {
    body: data.body,
    icon: '/icons/icon-192x192.png',
    badge: '/icons/badge-72x72.png',
    image: data.image,
    vibrate: [100, 50, 100],
    data: {
      url: data.url || '/',
      timestamp: Date.now()
    },
    actions: data.actions || [
      { action: 'open', title: 'Open' },
      { action: 'dismiss', title: 'Dismiss' }
    ],
    tag: data.tag || 'default',
    renotify: true,
    requireInteraction: data.requireInteraction || false
  };

  event.waitUntil(
    self.registration.showNotification(data.title, options)
  );
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();

  if (event.action === 'dismiss') return;

  const url = event.notification.data?.url || '/';

  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true })
      .then(windowClients => {
        // Focus existing window if available
        for (const client of windowClients) {
          if (client.url === url && 'focus' in client) {
            return client.focus();
          }
        }
        // Open new window
        return clients.openWindow(url);
      })
  );
});
```

## Offline Support

### IndexedDB for Offline Data

```typescript
// src/db.ts
import { openDB, DBSchema, IDBPDatabase } from 'idb';

interface MyAppDB extends DBSchema {
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
  pendingSync: {
    key: number;
    value: {
      id?: number;
      type: 'create' | 'update' | 'delete';
      collection: string;
      data: unknown;
      timestamp: number;
    };
  };
}

let dbPromise: Promise<IDBPDatabase<MyAppDB>>;

export function getDB(): Promise<IDBPDatabase<MyAppDB>> {
  if (!dbPromise) {
    dbPromise = openDB<MyAppDB>('my-app-db', 1, {
      upgrade(db) {
        // Items store
        const itemStore = db.createObjectStore('items', { keyPath: 'id' });
        itemStore.createIndex('by-synced', 'synced');

        // Pending sync store
        db.createObjectStore('pendingSync', { keyPath: 'id', autoIncrement: true });
      }
    });
  }
  return dbPromise;
}

// Save item locally
export async function saveItem(item: MyAppDB['items']['value']): Promise<void> {
  const db = await getDB();
  await db.put('items', { ...item, synced: false, updatedAt: Date.now() });

  // Queue for background sync
  await db.add('pendingSync', {
    type: item.id ? 'update' : 'create',
    collection: 'items',
    data: item,
    timestamp: Date.now()
  });

  // Request background sync
  if ('serviceWorker' in navigator && 'sync' in ServiceWorkerRegistration.prototype) {
    const registration = await navigator.serviceWorker.ready;
    await registration.sync.register('sync-items');
  }
}

// Get all items
export async function getAllItems(): Promise<MyAppDB['items']['value'][]> {
  const db = await getDB();
  return db.getAll('items');
}

// Get unsynced items
export async function getUnsyncedItems(): Promise<MyAppDB['items']['value'][]> {
  const db = await getDB();
  return db.getAllFromIndex('items', 'by-synced', false);
}
```

### Background Sync

```typescript
// In sw.js
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-items') {
    event.waitUntil(syncItems());
  }
});

async function syncItems() {
  const db = await openDB('my-app-db', 1);
  const pendingItems = await db.getAll('pendingSync');

  for (const item of pendingItems) {
    try {
      let endpoint = `/api/${item.collection}`;
      let method = 'POST';

      if (item.type === 'update') {
        endpoint += `/${item.data.id}`;
        method = 'PUT';
      } else if (item.type === 'delete') {
        endpoint += `/${item.data.id}`;
        method = 'DELETE';
      }

      const response = await fetch(endpoint, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(item.data)
      });

      if (response.ok) {
        // Remove from pending queue
        await db.delete('pendingSync', item.id);

        // Mark item as synced
        if (item.type !== 'delete') {
          const existing = await db.get(item.collection, item.data.id);
          if (existing) {
            await db.put(item.collection, { ...existing, synced: true });
          }
        }
      }
    } catch (error) {
      console.error('Sync failed for item:', item, error);
      // Will retry on next sync
    }
  }
}
```

## Mobile UX Patterns

### Touch-Friendly Components

```tsx
// src/components/TouchButton.tsx
import { useState, useRef, type ReactNode } from 'react';

interface TouchButtonProps {
  children: ReactNode;
  onClick: () => void;
  className?: string;
  haptic?: boolean;
}

export function TouchButton({
  children,
  onClick,
  className = '',
  haptic = true
}: TouchButtonProps) {
  const [isPressed, setIsPressed] = useState(false);
  const touchStartTime = useRef(0);

  const handleTouchStart = () => {
    setIsPressed(true);
    touchStartTime.current = Date.now();

    // Haptic feedback
    if (haptic && navigator.vibrate) {
      navigator.vibrate(10);
    }
  };

  const handleTouchEnd = () => {
    setIsPressed(false);

    // Only trigger if not a long press
    if (Date.now() - touchStartTime.current < 500) {
      onClick();
    }
  };

  return (
    <button
      className={`
        min-h-[44px] min-w-[44px]
        touch-manipulation select-none
        transition-transform duration-150
        ${isPressed ? 'scale-95' : 'scale-100'}
        ${className}
      `}
      onTouchStart={handleTouchStart}
      onTouchEnd={handleTouchEnd}
      onMouseDown={() => setIsPressed(true)}
      onMouseUp={handleTouchEnd}
      onMouseLeave={() => setIsPressed(false)}
    >
      {children}
    </button>
  );
}
```

### Pull-to-Refresh

```tsx
// src/hooks/usePullToRefresh.ts
import { useState, useRef, useEffect } from 'react';

interface PullToRefreshOptions {
  onRefresh: () => Promise<void>;
  threshold?: number;
  maxPull?: number;
}

export function usePullToRefresh({
  onRefresh,
  threshold = 80,
  maxPull = 120
}: PullToRefreshOptions) {
  const [pullDistance, setPullDistance] = useState(0);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const startY = useRef(0);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const handleTouchStart = (e: TouchEvent) => {
      if (container.scrollTop === 0) {
        startY.current = e.touches[0].clientY;
      }
    };

    const handleTouchMove = (e: TouchEvent) => {
      if (container.scrollTop > 0 || isRefreshing) return;

      const currentY = e.touches[0].clientY;
      const diff = currentY - startY.current;

      if (diff > 0) {
        e.preventDefault();
        setPullDistance(Math.min(diff * 0.5, maxPull));
      }
    };

    const handleTouchEnd = async () => {
      if (pullDistance >= threshold && !isRefreshing) {
        setIsRefreshing(true);
        setPullDistance(threshold);

        try {
          await onRefresh();
        } finally {
          setIsRefreshing(false);
          setPullDistance(0);
        }
      } else {
        setPullDistance(0);
      }
    };

    container.addEventListener('touchstart', handleTouchStart, { passive: true });
    container.addEventListener('touchmove', handleTouchMove, { passive: false });
    container.addEventListener('touchend', handleTouchEnd);

    return () => {
      container.removeEventListener('touchstart', handleTouchStart);
      container.removeEventListener('touchmove', handleTouchMove);
      container.removeEventListener('touchend', handleTouchEnd);
    };
  }, [pullDistance, isRefreshing, onRefresh, threshold, maxPull]);

  return { containerRef, pullDistance, isRefreshing };
}

// Usage
function MyList() {
  const { containerRef, pullDistance, isRefreshing } = usePullToRefresh({
    onRefresh: async () => {
      await fetchData();
    }
  });

  return (
    <div ref={containerRef} className="h-full overflow-y-auto">
      {/* Pull indicator */}
      <div
        className="flex justify-center items-center transition-transform"
        style={{
          height: pullDistance,
          transform: `translateY(${pullDistance > 0 ? 0 : -50}px)`
        }}
      >
        {isRefreshing ? (
          <Spinner />
        ) : pullDistance > 60 ? (
          <span>Release to refresh</span>
        ) : (
          <span>Pull to refresh</span>
        )}
      </div>

      {/* List content */}
      {items.map(item => <ListItem key={item.id} {...item} />)}
    </div>
  );
}
```

### Swipe Actions

```tsx
// src/components/SwipeableItem.tsx
import { useState, useRef, type ReactNode } from 'react';

interface SwipeableItemProps {
  children: ReactNode;
  onSwipeLeft?: () => void;
  onSwipeRight?: () => void;
  leftAction?: ReactNode;
  rightAction?: ReactNode;
  threshold?: number;
}

export function SwipeableItem({
  children,
  onSwipeLeft,
  onSwipeRight,
  leftAction,
  rightAction,
  threshold = 100
}: SwipeableItemProps) {
  const [offset, setOffset] = useState(0);
  const [isAnimating, setIsAnimating] = useState(false);
  const startX = useRef(0);
  const currentX = useRef(0);

  const handleTouchStart = (e: React.TouchEvent) => {
    startX.current = e.touches[0].clientX;
    currentX.current = startX.current;
    setIsAnimating(false);
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    currentX.current = e.touches[0].clientX;
    const diff = currentX.current - startX.current;

    // Limit swipe distance
    const maxOffset = 150;
    const limitedOffset = Math.sign(diff) * Math.min(Math.abs(diff), maxOffset);

    // Only allow swipe if action exists
    if ((diff > 0 && rightAction) || (diff < 0 && leftAction)) {
      setOffset(limitedOffset);
    }
  };

  const handleTouchEnd = () => {
    setIsAnimating(true);

    if (offset > threshold && onSwipeRight) {
      onSwipeRight();
    } else if (offset < -threshold && onSwipeLeft) {
      onSwipeLeft();
    }

    setOffset(0);
  };

  return (
    <div className="relative overflow-hidden">
      {/* Background actions */}
      <div className="absolute inset-0 flex">
        {rightAction && (
          <div className="flex-1 bg-green-500 flex items-center px-4">
            {rightAction}
          </div>
        )}
        {leftAction && (
          <div className="flex-1 bg-red-500 flex items-center justify-end px-4">
            {leftAction}
          </div>
        )}
      </div>

      {/* Swipeable content */}
      <div
        className={`relative bg-white ${isAnimating ? 'transition-transform duration-200' : ''}`}
        style={{ transform: `translateX(${offset}px)` }}
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
      >
        {children}
      </div>
    </div>
  );
}
```

## React Native Basics

### Setup and Structure

```bash
# Create new React Native project with Expo
npx create-expo-app@latest my-app --template blank-typescript
cd my-app

# Install common dependencies
npx expo install react-native-gesture-handler react-native-reanimated
npx expo install @react-navigation/native @react-navigation/stack
npx expo install expo-status-bar expo-constants
```

### Basic Navigation

```tsx
// App.tsx
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { StatusBar } from 'expo-status-bar';
import HomeScreen from './screens/HomeScreen';
import DetailsScreen from './screens/DetailsScreen';

export type RootStackParamList = {
  Home: undefined;
  Details: { itemId: string };
};

const Stack = createStackNavigator<RootStackParamList>();

export default function App() {
  return (
    <NavigationContainer>
      <StatusBar style="auto" />
      <Stack.Navigator
        initialRouteName="Home"
        screenOptions={{
          headerStyle: { backgroundColor: '#3b82f6' },
          headerTintColor: '#fff',
          headerTitleStyle: { fontWeight: 'bold' }
        }}
      >
        <Stack.Screen
          name="Home"
          component={HomeScreen}
          options={{ title: 'My App' }}
        />
        <Stack.Screen
          name="Details"
          component={DetailsScreen}
          options={({ route }) => ({ title: `Item ${route.params.itemId}` })}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

### Platform-Specific Code

```tsx
// src/components/Button.tsx
import { Platform, TouchableOpacity, TouchableNativeFeedback, View, Text } from 'react-native';

interface ButtonProps {
  title: string;
  onPress: () => void;
}

export function Button({ title, onPress }: ButtonProps) {
  const buttonContent = (
    <View style={{
      backgroundColor: '#3b82f6',
      paddingVertical: 12,
      paddingHorizontal: 24,
      borderRadius: 8
    }}>
      <Text style={{ color: 'white', fontWeight: 'bold', textAlign: 'center' }}>
        {title}
      </Text>
    </View>
  );

  if (Platform.OS === 'android') {
    return (
      <TouchableNativeFeedback onPress={onPress}>
        {buttonContent}
      </TouchableNativeFeedback>
    );
  }

  return (
    <TouchableOpacity onPress={onPress} activeOpacity={0.7}>
      {buttonContent}
    </TouchableOpacity>
  );
}
```

## Install Prompt

### Custom Install Prompt

```tsx
// src/components/InstallPrompt.tsx
import { useState, useEffect } from 'react';

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
}

export function InstallPrompt() {
  const [installPrompt, setInstallPrompt] = useState<BeforeInstallPromptEvent | null>(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const handler = (e: Event) => {
      e.preventDefault();
      setInstallPrompt(e as BeforeInstallPromptEvent);
      setIsVisible(true);
    };

    window.addEventListener('beforeinstallprompt', handler);

    // Check if already installed
    if (window.matchMedia('(display-mode: standalone)').matches) {
      setIsVisible(false);
    }

    return () => window.removeEventListener('beforeinstallprompt', handler);
  }, []);

  const handleInstall = async () => {
    if (!installPrompt) return;

    await installPrompt.prompt();
    const { outcome } = await installPrompt.userChoice;

    if (outcome === 'accepted') {
      setIsVisible(false);
      setInstallPrompt(null);
    }
  };

  const handleDismiss = () => {
    setIsVisible(false);
    // Remember dismissal
    localStorage.setItem('installPromptDismissed', Date.now().toString());
  };

  if (!isVisible) return null;

  return (
    <div className="fixed bottom-4 left-4 right-4 bg-white rounded-lg shadow-lg p-4 flex items-center gap-4 z-50 animate-slide-up">
      <img src="/icons/icon-72x72.png" alt="App icon" className="w-12 h-12 rounded" />
      <div className="flex-1">
        <h3 className="font-semibold">Install Our App</h3>
        <p className="text-sm text-gray-600">Get quick access from your home screen</p>
      </div>
      <button onClick={handleDismiss} className="text-gray-400 p-2">
        Not now
      </button>
      <button
        onClick={handleInstall}
        className="bg-blue-500 text-white px-4 py-2 rounded-lg font-medium"
      >
        Install
      </button>
    </div>
  );
}
```

## Best Practices

### Performance

1. **Optimize First Paint**
   - Inline critical CSS
   - Defer non-critical JavaScript
   - Use skeleton screens

2. **Touch Targets**
   - Minimum 44x44px touch targets
   - Adequate spacing between targets
   - Visual feedback on touch

3. **Reduce Network Requests**
   - Bundle and minify assets
   - Use service worker caching
   - Lazy load images and routes

### Accessibility

1. **Zoom Support**
   - Never disable zoom
   - Use relative units (rem, em)
   - Test at 200% zoom

2. **Reduced Motion**
   ```css
   @media (prefers-reduced-motion: reduce) {
     * {
       animation-duration: 0.01ms !important;
       transition-duration: 0.01ms !important;
     }
   }
   ```

3. **Color Contrast**
   - 4.5:1 minimum for normal text
   - 3:1 minimum for large text
   - Don't rely on color alone

### Testing PWAs

1. **Lighthouse Audit**
   ```bash
   npx lighthouse https://your-app.com --view
   ```

2. **PWA Checklist**
   - [ ] HTTPS enabled
   - [ ] Valid manifest.json
   - [ ] Service worker registered
   - [ ] Offline page works
   - [ ] Install prompt shows
   - [ ] Push notifications work

## Resources

- [web.dev PWA Guide](https://web.dev/progressive-web-apps/)
- [Workbox Documentation](https://developer.chrome.com/docs/workbox/)
- [React Native Documentation](https://reactnative.dev/)
- [Expo Documentation](https://docs.expo.dev/)
