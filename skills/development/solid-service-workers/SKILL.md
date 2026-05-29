---
name: solid-service-workers
description: "SolidStart service workers: registration, caching strategies, offline support, background sync, PWA features."
metadata:
  globs:
    - "public/sw.js"
    - "**/*service-worker*"
---

# SolidStart Service Workers

Complete guide to service workers in SolidStart. Enable offline support, caching, and PWA features.

## Registration

Register service worker in `entry-client.tsx`.

### Basic Registration

```tsx
// src/entry-client.tsx
import { mount, StartClient } from "@solidjs/start/client";

mount(() => <StartClient />, document.getElementById("app")!);

if ("serviceWorker" in navigator && import.meta.env.PROD) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/sw.js");
  });
}
```

**Key points:**
- Only register in production
- Wait for window load
- Service worker file in `public/` directory

### With Error Handling

```tsx
if ("serviceWorker" in navigator && import.meta.env.PROD) {
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .register("/sw.js")
      .then((registration) => {
        console.log("SW registered:", registration);
      })
      .catch((error) => {
        console.error("SW registration failed:", error);
      });
  });
}
```

## Service Worker File

Create service worker in `public/sw.js`.

### Basic Service Worker

```js
// public/sw.js
const CACHE_NAME = "my-app-v1";
const urlsToCache = [
  "/",
  "/styles.css",
  "/app.js",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(urlsToCache);
    })
  );
});

self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
```

## Caching Strategies

### Cache First

Serve from cache, fallback to network.

```js
self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      if (response) {
        return response; // Serve from cache
      }
      return fetch(event.request); // Fallback to network
    })
  );
});
```

### Network First

Try network, fallback to cache.

```js
self.addEventListener("fetch", (event) => {
  event.respondWith(
    fetch(event.request)
      .then((response) => {
        // Cache successful responses
        if (response.ok) {
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
        }
        return response;
      })
      .catch(() => {
        // Fallback to cache
        return caches.match(event.request);
      })
  );
});
```

### Stale While Revalidate

Serve cache immediately, update in background.

```js
self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.match(event.request).then((cachedResponse) => {
        const fetchPromise = fetch(event.request).then((networkResponse) => {
          cache.put(event.request, networkResponse.clone());
          return networkResponse;
        });
        return cachedResponse || fetchPromise;
      });
    })
  );
});
```

## Offline Support

### Offline Page

```js
self.addEventListener("fetch", (event) => {
  event.respondWith(
    fetch(event.request)
      .catch(() => {
        // Return offline page
        return caches.match("/offline.html");
      })
  );
});
```

### Offline Indicator

```tsx
function OfflineIndicator() {
  const [isOnline, setIsOnline] = createSignal(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);

    onCleanup(() => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    });
  });

  return (
    <Show when={!isOnline()}>
      <div class="offline-banner">You're offline</div>
    </Show>
  );
}
```

## Background Sync

Sync data when connection is restored.

```js
// Service worker
self.addEventListener("sync", (event) => {
  if (event.tag === "sync-data") {
    event.waitUntil(syncData());
  }
});

async function syncData() {
  // Sync pending data
  const pending = await getPendingData();
  for (const item of pending) {
    await syncItem(item);
  }
}
```

```tsx
// Client code
async function syncData() {
  if ("serviceWorker" in navigator && "sync" in (self as any).registration) {
    await (navigator.serviceWorker.ready as any).then((registration: any) => {
      return registration.sync.register("sync-data");
    });
  }
}
```

## Update Strategy

### Check for Updates

```tsx
function checkForUpdates() {
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.getRegistration().then((registration) => {
      if (registration) {
        registration.update();
      }
    });
  }
}
```

### Handle Updates

```js
// Service worker
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
```

## Best Practices

1. **Version your cache:**
   - Use versioned cache names
   - Clean up old caches

2. **Cache selectively:**
   - Don't cache everything
   - Cache static assets
   - Cache API responses carefully

3. **Handle updates:**
   - Check for updates periodically
   - Clean up old caches
   - Notify users of updates

4. **Test offline:**
   - Test offline functionality
   - Verify cache strategies
   - Check error handling

5. **Security:**
   - Only over HTTPS (or localhost)
   - Validate cached responses
   - Handle errors gracefully

## Summary

- **Registration**: In entry-client.tsx, production only
- **Caching**: Choose strategy (cache-first, network-first, stale-while-revalidate)
- **Offline**: Provide offline page and indicator
- **Background sync**: Sync when connection restored
- **Updates**: Version caches and handle updates

