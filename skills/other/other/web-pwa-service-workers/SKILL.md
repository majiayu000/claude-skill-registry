---
name: web-pwa-service-workers
description: Service Worker lifecycle, caching strategies, offline patterns, update handling, precaching, runtime caching
---

# Service Worker Patterns

> **Quick Guide:** Use Service Workers for offline-first applications with sophisticated caching. Implement cache-first for static assets, network-first for HTML, and stale-while-revalidate for API data. Always handle the install/activate/fetch lifecycle properly, version your caches, and provide user control over updates. Clone responses before caching (body can only be consumed once).

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST call `event.waitUntil()` in install and activate handlers to signal completion)**

**(You MUST version your caches and clean up old versions during activation)**

**(You MUST clone responses before caching - `cache.put(request, response.clone())` - response body can only be consumed once)**

**(You MUST implement proper update detection and give users control over when updates apply)**

**(You MUST handle all fetch failures with appropriate offline fallbacks)**

</critical_requirements>

---

**Auto-detection:** Service Worker, serviceWorker, sw.js, sw.ts, navigator.serviceWorker, caches, Cache API, CacheStorage, skipWaiting, clients.claim, precache, offline-first, PWA

**When to use:**

- Building Progressive Web Apps (PWAs) with offline support
- Implementing sophisticated caching strategies beyond browser defaults
- Providing offline fallback pages or cached content
- Controlling how network requests are handled and cached

**When NOT to use:**

- Simple websites without offline requirements
- When browser HTTP caching is sufficient
- For real-time data that must always be fresh (use network-only)

---

<philosophy>

## Philosophy

Service Workers are **programmable network proxies** that run in a separate thread, intercepting requests between your application and the network. They enable offline functionality, sophisticated caching, and background operations.

**The Service Worker lifecycle is designed for safety:**

1. **Install Phase:** Download and cache critical assets. The worker is "waiting" until installation completes.
2. **Waiting Phase:** New workers wait for all tabs using the old worker to close, preventing version conflicts.
3. **Activate Phase:** Old caches are cleaned up, and the worker takes control.
4. **Fetch Phase:** The active worker intercepts all network requests within its scope.

```
Registration → Download → Install → Waiting → Activate → Fetch
                            ↓          ↓
                     (skipWaiting)  (claim)
```

**Core Principles:**

1. **Safety First:** The lifecycle prevents running multiple versions simultaneously, which could corrupt state.
2. **User Control:** Users should decide when updates apply, not be surprised by sudden behavior changes mid-session.
3. **Graceful Degradation:** Always provide fallbacks when network and cache both fail.
4. **Cache Versioning:** Version your caches to enable clean upgrades and prevent unbounded growth.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Service Worker Registration

Register from your main application with feature detection, update checking, and user-controlled updates.

```typescript
const SW_PATH = "/sw.js";
const UPDATE_CHECK_INTERVAL_MS = 60 * 60 * 1000;

const registration = await navigator.serviceWorker.register(SW_PATH, {
  scope: "/",
  updateViaCache: "none", // Always check server for updates
});

// Periodic update checks
setInterval(() => registration.update(), UPDATE_CHECK_INTERVAL_MS);

// Track waiting worker for user-controlled updates
registration.addEventListener("updatefound", () => {
  const installing = registration.installing;
  installing?.addEventListener("statechange", () => {
    if (
      installing.state === "installed" &&
      navigator.serviceWorker.controller
    ) {
      // New version waiting - notify user
    }
  });
});
```

See [examples/core.md](examples/core.md) Pattern 1 for complete registration with update tracking and reload handling.

---

### Pattern 2: Lifecycle Handlers (Install / Activate / Message)

The three essential lifecycle event handlers: precache in install, cleanup in activate, user-controlled skipWaiting via message.

```typescript
// Install - precache critical assets
self.addEventListener("install", (event: ExtendableEvent) => {
  event.waitUntil(
    caches.open(CACHES.static).then((cache) => cache.addAll(PRECACHE_URLS)),
  );
  // Do NOT call skipWaiting here - let user control updates
});

// Activate - cleanup old caches, claim clients
self.addEventListener("activate", (event: ExtendableEvent) => {
  event.waitUntil(
    caches
      .keys()
      .then((names) =>
        Promise.all(
          names
            .filter((n) => !currentCaches.includes(n))
            .map((n) => caches.delete(n)),
        ),
      )
      .then(() => self.clients.claim()),
  );
});

// Message - user-controlled skipWaiting
self.addEventListener("message", (event: ExtendableMessageEvent) => {
  if (event.data?.type === "SKIP_WAITING") self.skipWaiting();
});
```

See [examples/core.md](examples/core.md) Pattern 2 for complete template with constants and type safety.

---

### Pattern 3: Caching Strategies

Four strategies to match content types:

| Strategy                      | When to Use                        | Behavior                                    |
| ----------------------------- | ---------------------------------- | ------------------------------------------- |
| **Cache-first**               | Static assets, fonts, hashed files | Return cached immediately, network fallback |
| **Network-first**             | HTML pages, user-specific API data | Try network with timeout, cache fallback    |
| **Stale-while-revalidate**    | Avatars, non-critical API, feeds   | Return cached, refresh in background        |
| **Cache-only / Network-only** | Precached shells / real-time data  | Single source, no fallback                  |

Key implementation details:

- Always check `response.ok` before caching (avoid caching 404/500)
- Always `response.clone()` before `cache.put()` (body consumed once)
- Add timeout to network-first to avoid hanging on slow connections
- Limit cache size to prevent unbounded storage growth

```typescript
// The clone pattern - response body can only be consumed once
const networkResponse = await fetch(request);
if (networkResponse.ok) {
  cache.put(request, networkResponse.clone()); // Clone for cache
}
return networkResponse; // Original for client
```

See [examples/core.md](examples/core.md) Pattern 2 for all strategy implementations in the complete template, and [examples/caching.md](examples/caching.md) for advanced patterns (expiration, selective API caching, storage cleanup).

---

### Pattern 4: Fetch Event Routing

Route requests to appropriate caching strategies based on request type and URL.

```typescript
self.addEventListener("fetch", (event: FetchEvent) => {
  const { request } = event;
  const url = new URL(request.url);

  if (request.method !== "GET") return; // Skip non-GET
  if (url.origin !== location.origin) return; // Skip cross-origin

  if (request.mode === "navigate") {
    event.respondWith(networkFirst(request, CACHES.pages));
  } else if (request.destination === "image") {
    event.respondWith(
      cacheFirstWithLimit(request, CACHES.images, MAX_CACHE_ITEMS.images),
    );
  } else if (url.pathname.startsWith("/api/")) {
    event.respondWith(staleWhileRevalidate(request, CACHES.api));
  } else {
    event.respondWith(cacheFirst(request, CACHES.static));
  }
});
```

---

### Pattern 5: Offline Fallback

Always precache an offline.html page and return it when both cache and network fail for navigation requests.

```typescript
// In install handler: precache offline.html
// In fetch error handling:
if (request.mode === "navigate") {
  const offlinePage = await caches.match("/offline.html");
  if (offlinePage) return offlinePage;
}

// Last resort: inline response
return new Response(
  "<html><body><h1>Offline</h1><p>Check your connection.</p></body></html>",
  { status: 503, headers: { "Content-Type": "text/html" } },
);
```

---

### Pattern 6: Navigation Preload

Fetch navigation requests in parallel with service worker bootup, reducing latency for network-first HTML. Enable in activate, consume via `event.preloadResponse` in fetch.

```typescript
// Activate: enable navigation preload
if (self.registration.navigationPreload) {
  await self.registration.navigationPreload.enable();
}

// Fetch: use preloaded response (avoids double fetch)
const preloadResponse = await event.preloadResponse;
if (preloadResponse) {
  cache.put(event.request, preloadResponse.clone());
  return preloadResponse;
}
```

**Warning:** If you enable navigation preload, you MUST use `event.preloadResponse`. Using `fetch(event.request)` instead results in two network requests for the same resource.

**When to use:** Network-first HTML pages with dynamic/authenticated content. Not needed for precached app shells.

See [examples/caching.md](examples/caching.md) Pattern 8 for complete implementation.

---

### Pattern 7: Update Handling

Users should control when updates apply. Detect waiting workers, notify users, and let them trigger `skipWaiting`.

```typescript
// Client: detect and apply updates
if (registration.waiting) {
  showUpdateBanner();
}

function applyUpdate() {
  registration.waiting?.postMessage({ type: "SKIP_WAITING" });
}

// Reload when new worker takes control
navigator.serviceWorker.addEventListener("controllerchange", () => {
  window.location.reload();
});
```

See [examples/updates.md](examples/updates.md) for version tracking, aggressive updates, deferred updates, idle-time updates, progressive rollout, and data migration patterns.

</patterns>

---

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Registration, lifecycle template, caching strategy implementations, types
- [examples/caching.md](examples/caching.md) - Advanced caching (expiration, selective API, storage cleanup, navigation preload)
- [examples/updates.md](examples/updates.md) - Version tracking, update strategies (aggressive, deferred, idle, rollout, migration)
- [reference.md](reference.md) - Decision frameworks, anti-patterns, lifecycle reference, checklists

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- No `event.waitUntil()` in install/activate - browser may terminate SW before async operations complete
- Calling `skipWaiting()` unconditionally in install - users experience unexpected behavior changes mid-session
- No cache versioning - old cached content persists forever, storage grows unbounded
- Not cleaning up old caches in activate - storage quota eventually exceeded
- Missing offline fallback - users see browser error page instead of helpful message
- Not checking `response.ok` before caching - error responses (404, 500) get cached and served

**Medium Priority Issues:**

- No timeout on network requests in network-first strategy - fetch hangs indefinitely on slow connections
- Not cloning response before caching - response body consumed, client gets empty response
- No cache size limits - unbounded growth leads to quota issues
- Attempting to cache POST requests - only GET requests are cacheable

**Gotchas & Edge Cases:**

- Service workers only work over HTTPS (exception: localhost for development)
- Scope determined by SW file location - `/sw.js` controls `/`, but `/scripts/sw.js` only controls `/scripts/`
- Browser may terminate idle service workers - do not rely on in-memory state
- `clients.claim()` does not trigger reload - clients keep running old page with new SW
- Chrome DevTools "Update on reload" bypasses waiting - useful for dev, not representative of production
- Web app manifest changes do not trigger SW update - only byte changes to SW file itself
- IndexedDB transactions cannot span `await` - complete DB work in single transaction
- Opaque responses (cross-origin without CORS) count against storage quota at inflated cost
- Service worker bootup varies: ~50ms desktop, ~250ms mobile, 500ms+ slow devices - navigation preload mitigates this

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST call `event.waitUntil()` in install and activate handlers to signal completion)**

**(You MUST version your caches and clean up old versions during activation)**

**(You MUST clone responses before caching - `cache.put(request, response.clone())` - response body can only be consumed once)**

**(You MUST implement proper update detection and give users control over when updates apply)**

**(You MUST handle all fetch failures with appropriate offline fallbacks)**

**Failure to follow these rules will result in broken updates, unbounded cache growth, and poor offline experience.**

</critical_reminders>
