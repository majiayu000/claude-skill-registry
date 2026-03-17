---
name: web-pwa-service-workers
description: Service Worker lifecycle, caching strategies, offline patterns, update handling, precaching, runtime caching
---

# Service Worker Patterns

> **Quick Guide:** Use Service Workers for offline-first applications with sophisticated caching. Implement cache-first for static assets, network-first for HTML, and stale-while-revalidate for API data. Always handle the install/activate/fetch lifecycle properly and provide user control over updates.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST call `event.waitUntil()` in install and activate handlers to signal completion)**

**(You MUST version your caches and clean up old versions during activation)**

**(You MUST implement proper update detection and give users control over when updates apply)**

**(You MUST use `clients.claim()` in activate if you need immediate control of clients)**

**(You MUST handle all fetch failures with appropriate offline fallbacks)**

</critical_requirements>

---

**Auto-detection:** Service Worker, serviceWorker, sw.js, sw.ts, navigator.serviceWorker, caches, Cache API, CacheStorage, skipWaiting, clients.claim, precache, offline-first, PWA

**When to use:**

- Building Progressive Web Apps (PWAs) with offline support
- Implementing sophisticated caching strategies beyond browser defaults
- Providing offline fallback pages or cached content
- Controlling how network requests are handled and cached

**Key patterns covered:**

- Service Worker lifecycle (install, activate, fetch)
- Caching strategies (cache-first, network-first, stale-while-revalidate)
- Precaching critical assets during installation
- Runtime caching for dynamic content
- Update detection and user-controlled updates
- Offline fallback pages

**When NOT to use:**

- Simple websites without offline requirements
- When browser HTTP caching is sufficient
- For real-time data that must always be fresh (use network-only)

**Detailed Resources:**

- For code examples, see [examples/](examples/)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

Service Workers are **programmable network proxies** that run in a separate thread, intercepting requests between your application and the network. They enable offline functionality, sophisticated caching, and background operations that weren't previously possible on the web.

**The Service Worker lifecycle is designed for safety:**

1. **Install Phase:** Download and cache critical assets. The worker is "waiting" until installation completes.

2. **Waiting Phase:** New workers wait for all tabs using the old worker to close, preventing version conflicts.

3. **Activate Phase:** Old caches are cleaned up, and the worker takes control.

4. **Fetch Phase:** The active worker intercepts all network requests within its scope.

**Core Principles:**

1. **Safety First:** The lifecycle exists to prevent running multiple versions simultaneously, which could corrupt state or cause inconsistent behavior.

2. **User Control:** Users should decide when updates apply, not be surprised by sudden behavior changes mid-session.

3. **Graceful Degradation:** Always provide fallbacks when network and cache both fail.

4. **Cache Versioning:** Version your caches to enable clean upgrades and prevent unbounded growth.

**Lifecycle Diagram:**

```
Registration → Download → Install → Waiting → Activate → Fetch
                            ↓          ↓
                     (skipWaiting)  (claim)
```

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Service Worker Registration

Register the service worker from your main application with proper error handling and update detection.

```typescript
// register-service-worker.ts
const SW_PATH = "/sw.js";
const UPDATE_CHECK_INTERVAL_MS = 60 * 60 * 1000; // 1 hour

interface ServiceWorkerState {
  registration: ServiceWorkerRegistration | null;
  updateAvailable: boolean;
  applyUpdate: () => void;
}

async function registerServiceWorker(): Promise<ServiceWorkerState> {
  if (!("serviceWorker" in navigator)) {
    console.log("Service Workers not supported");
    return {
      registration: null,
      updateAvailable: false,
      applyUpdate: () => {},
    };
  }

  try {
    const registration = await navigator.serviceWorker.register(SW_PATH, {
      scope: "/",
      updateViaCache: "none", // Always check server for updates
    });

    console.log("Service Worker registered:", registration.scope);

    // Check for updates periodically
    setInterval(() => {
      registration.update();
    }, UPDATE_CHECK_INTERVAL_MS);

    // Track update availability
    let updateAvailable = false;
    let waitingWorker: ServiceWorker | null = null;

    const handleUpdate = (worker: ServiceWorker) => {
      waitingWorker = worker;
      updateAvailable = true;
      // Notify UI that update is available
      window.dispatchEvent(new CustomEvent("sw-update-available"));
    };

    // Check if already waiting
    if (registration.waiting) {
      handleUpdate(registration.waiting);
    }

    // Listen for new installations
    registration.addEventListener("updatefound", () => {
      const installing = registration.installing;
      if (!installing) return;

      installing.addEventListener("statechange", () => {
        if (
          installing.state === "installed" &&
          navigator.serviceWorker.controller
        ) {
          handleUpdate(installing);
        }
      });
    });

    // Reload when new worker takes control
    let refreshing = false;
    navigator.serviceWorker.addEventListener("controllerchange", () => {
      if (!refreshing) {
        refreshing = true;
        window.location.reload();
      }
    });

    return {
      registration,
      updateAvailable,
      applyUpdate: () => {
        if (waitingWorker) {
          waitingWorker.postMessage({ type: "SKIP_WAITING" });
        }
      },
    };
  } catch (error) {
    console.error("Service Worker registration failed:", error);
    return {
      registration: null,
      updateAvailable: false,
      applyUpdate: () => {},
    };
  }
}

export { registerServiceWorker };
export type { ServiceWorkerState };
```

**Why good:** Named constant for interval, proper feature detection, periodic update checks, tracks waiting worker for user-controlled updates, handles controller change to reload, named exports

---

### Pattern 2: Basic Service Worker Structure

The service worker file with proper lifecycle handling, cache versioning, and type safety.

#### Constants

```typescript
// sw.ts
declare const self: ServiceWorkerGlobalScope;

const CACHE_VERSION = "v1.0.0";

const CACHES = {
  static: `static-${CACHE_VERSION}`,
  pages: `pages-${CACHE_VERSION}`,
  images: `images-${CACHE_VERSION}`,
  api: `api-${CACHE_VERSION}`,
} as const;

const PRECACHE_URLS = [
  "/",
  "/offline.html",
  "/manifest.json",
  "/styles/app.css",
  "/scripts/app.js",
] as const;

const MAX_CACHE_ITEMS = {
  images: 100,
  api: 50,
} as const;

const NETWORK_TIMEOUT_MS = 3000;
```

#### Install Handler

```typescript
// Install - precache critical assets
self.addEventListener("install", (event: ExtendableEvent) => {
  console.log("[SW] Installing version:", CACHE_VERSION);

  event.waitUntil(
    (async () => {
      const cache = await caches.open(CACHES.static);
      await cache.addAll(PRECACHE_URLS);
      console.log("[SW] Precached", PRECACHE_URLS.length, "assets");
      // Do NOT call skipWaiting here - let user control updates
    })(),
  );
});
```

#### Activate Handler

```typescript
// Activate - cleanup old caches
self.addEventListener("activate", (event: ExtendableEvent) => {
  console.log("[SW] Activating version:", CACHE_VERSION);

  event.waitUntil(
    (async () => {
      // Delete old caches
      const cacheNames = await caches.keys();
      const currentCaches = Object.values(CACHES);

      await Promise.all(
        cacheNames
          .filter((name) => !currentCaches.includes(name))
          .map((name) => {
            console.log("[SW] Deleting old cache:", name);
            return caches.delete(name);
          }),
      );

      // Take control of all clients immediately
      await self.clients.claim();
      console.log("[SW] Claimed all clients");
    })(),
  );
});
```

#### Message Handler

```typescript
// Handle messages from clients
self.addEventListener("message", (event: ExtendableMessageEvent) => {
  if (event.data?.type === "SKIP_WAITING") {
    console.log("[SW] Skip waiting requested");
    self.skipWaiting();
  }
});
```

**Why good:** All constants named and typed, cache versioning for clean upgrades, waitUntil signals completion, old caches cleaned up, message handler for user-controlled skipWaiting

---

### Pattern 3: Cache-First Strategy

Return cached response immediately, fall back to network. Best for static assets that don't change often.

```typescript
// Cache-first: Check cache, fall back to network
async function cacheFirst(
  request: Request,
  cacheName: string,
): Promise<Response> {
  const cache = await caches.open(cacheName);
  const cachedResponse = await cache.match(request);

  if (cachedResponse) {
    console.log("[SW] Cache hit:", request.url);
    return cachedResponse;
  }

  console.log("[SW] Cache miss, fetching:", request.url);

  try {
    const networkResponse = await fetch(request);

    // Only cache successful responses
    if (networkResponse.ok) {
      // Clone before caching (response can only be consumed once)
      cache.put(request, networkResponse.clone());
    }

    return networkResponse;
  } catch (error) {
    console.error("[SW] Fetch failed:", request.url, error);
    // Return offline fallback for navigation requests
    if (request.mode === "navigate") {
      const offlinePage = await caches.match("/offline.html");
      if (offlinePage) return offlinePage;
    }
    throw error;
  }
}
```

**When to use:** Static assets (CSS, JS, images), fonts, versioned resources with cache-busting hashes

**Why good:** Checks cache first for speed, caches network responses, clones before put, handles failures with offline fallback

---

### Pattern 4: Network-First Strategy

Try network first, fall back to cache if offline. Best for content that should be fresh but work offline.

```typescript
// Network-first: Try network, fall back to cache
async function networkFirst(
  request: Request,
  cacheName: string,
  timeoutMs: number = NETWORK_TIMEOUT_MS,
): Promise<Response> {
  const cache = await caches.open(cacheName);

  try {
    // Race network request against timeout
    const networkResponse = await Promise.race([
      fetch(request),
      new Promise<never>((_, reject) =>
        setTimeout(() => reject(new Error("Network timeout")), timeoutMs),
      ),
    ]);

    // Cache successful responses
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone());
    }

    return networkResponse;
  } catch (error) {
    console.log("[SW] Network failed, trying cache:", request.url);

    const cachedResponse = await cache.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }

    // Return offline page for navigation requests
    if (request.mode === "navigate") {
      const offlinePage = await caches.match("/offline.html");
      if (offlinePage) return offlinePage;
    }

    throw error;
  }
}
```

**When to use:** HTML pages, API requests that need fresh data but should work offline, frequently updated content

**Why good:** Timeout prevents hanging on slow connections, caches successful responses for offline, proper fallback chain

---

### Pattern 5: Stale-While-Revalidate Strategy

Return cached response immediately, update cache in background. Best for content where speed matters but staleness is acceptable.

```typescript
// Stale-while-revalidate: Return cache, update in background
async function staleWhileRevalidate(
  request: Request,
  cacheName: string,
): Promise<Response> {
  const cache = await caches.open(cacheName);
  const cachedResponse = await cache.match(request);

  // Background revalidation (don't await)
  const fetchPromise = fetch(request)
    .then(async (networkResponse) => {
      if (networkResponse.ok) {
        await cache.put(request, networkResponse.clone());
        console.log("[SW] Cache updated:", request.url);
      }
      return networkResponse;
    })
    .catch((error) => {
      console.error("[SW] Background fetch failed:", request.url, error);
      return null;
    });

  // Return cached immediately if available, otherwise wait for network
  if (cachedResponse) {
    console.log("[SW] Returning stale:", request.url);
    return cachedResponse;
  }

  console.log("[SW] No cache, waiting for network:", request.url);
  const networkResponse = await fetchPromise;
  if (networkResponse) {
    return networkResponse;
  }

  throw new Error("No cached or network response available");
}
```

**When to use:** User avatars, non-critical API data, content that should be fast but eventually consistent

**Why good:** Returns immediately for cached content, background fetch doesn't block, handles both cache-hit and cache-miss scenarios

---

### Pattern 6: Fetch Event Router

Route requests to appropriate caching strategies based on request type and URL.

```typescript
// Fetch event handler - routes to strategies
self.addEventListener("fetch", (event: FetchEvent) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== "GET") {
    return;
  }

  // Skip cross-origin requests
  if (url.origin !== location.origin) {
    return;
  }

  // Route based on request type
  if (request.mode === "navigate") {
    // HTML pages: Network-first
    event.respondWith(networkFirst(request, CACHES.pages));
  } else if (request.destination === "image") {
    // Images: Cache-first with size limit
    event.respondWith(
      cacheFirstWithLimit(request, CACHES.images, MAX_CACHE_ITEMS.images),
    );
  } else if (url.pathname.startsWith("/api/")) {
    // API requests: Stale-while-revalidate
    event.respondWith(staleWhileRevalidate(request, CACHES.api));
  } else {
    // Static assets: Cache-first
    event.respondWith(cacheFirst(request, CACHES.static));
  }
});
```

**Why good:** Clear routing logic, skips non-cacheable requests, uses appropriate strategy per content type, named constants for cache names

---

### Pattern 7: Cache Size Management

Limit cache size to prevent unbounded storage growth.

```typescript
// Limit cache size by removing oldest entries
async function limitCacheSize(cache: Cache, maxItems: number): Promise<void> {
  const keys = await cache.keys();

  if (keys.length > maxItems) {
    // Delete oldest entries (FIFO)
    const deleteCount = keys.length - maxItems;
    const toDelete = keys.slice(0, deleteCount);

    await Promise.all(
      toDelete.map((request) => {
        console.log("[SW] Evicting from cache:", request.url);
        return cache.delete(request);
      }),
    );
  }
}

// Cache-first with size limit
async function cacheFirstWithLimit(
  request: Request,
  cacheName: string,
  maxItems: number,
): Promise<Response> {
  const cache = await caches.open(cacheName);
  const cachedResponse = await cache.match(request);

  if (cachedResponse) {
    return cachedResponse;
  }

  try {
    const networkResponse = await fetch(request);

    if (networkResponse.ok) {
      // Limit cache size before adding
      await limitCacheSize(cache, maxItems - 1);
      cache.put(request, networkResponse.clone());
    }

    return networkResponse;
  } catch (error) {
    console.error("[SW] Fetch failed:", request.url);
    throw error;
  }
}
```

**Why good:** Prevents storage quota issues, FIFO eviction is predictable, limits checked before adding new entries

---

### Pattern 8: Offline Fallback Page

Create a meaningful offline experience when both cache and network fail.

```typescript
// offline.html should be precached during install
// Return it for navigation requests that fail

async function handleNavigationFailure(request: Request): Promise<Response> {
  // Try the cache first
  const cachedPage = await caches.match(request);
  if (cachedPage) {
    return cachedPage;
  }

  // Return offline page
  const offlinePage = await caches.match("/offline.html");
  if (offlinePage) {
    return offlinePage;
  }

  // Last resort: return a basic offline response
  return new Response(
    `<!DOCTYPE html>
    <html>
      <head><title>Offline</title></head>
      <body>
        <h1>You are offline</h1>
        <p>Please check your internet connection and try again.</p>
      </body>
    </html>`,
    {
      status: 503,
      headers: { "Content-Type": "text/html" },
    },
  );
}
```

**Why good:** Graceful degradation chain, always returns something meaningful, inline fallback as last resort

</patterns>

---

<integration>

## Integration Guide

**Service Workers are framework-agnostic.** This skill covers the native Service Worker API only. Integration with specific build tools or libraries is handled by their respective documentation.

**Works with:**

- Your build tool for precache manifest generation
- Your web app manifest for PWA installability
- Your offline page design for user experience

**Defers to:**

- Background Sync API (for queuing failed requests)
- Push API (for push notifications)
- IndexedDB (for offline data storage beyond cache)
- Navigation Preload API (for parallel navigation fetching during SW bootup)

**Recommended Tools:**

- **Workbox** - Google's production-ready library for service workers. Provides pre-built caching strategies, precaching with revision management, background sync plugins, and navigation preload support. Use Workbox for production applications instead of hand-rolling all patterns.

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST call `event.waitUntil()` in install and activate handlers to signal completion)**

**(You MUST version your caches and clean up old versions during activation)**

**(You MUST implement proper update detection and give users control over when updates apply)**

**(You MUST use `clients.claim()` in activate if you need immediate control of clients)**

**(You MUST handle all fetch failures with appropriate offline fallbacks)**

**Failure to follow these rules will result in broken updates, unbounded cache growth, and poor offline experience.**

</critical_reminders>
