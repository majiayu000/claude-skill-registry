---
name: Next.js Caching Architecture
description: The 4 layers of caching (Memoization, Data Cache, Full Route, Router Cache).
metadata:
  labels: [nextjs, caching, isr, revalidation]
  triggers:
    files: ['**/page.tsx', '**/layout.tsx', '**/action.ts']
    keywords: [unstable_cache, revalidateTag, Router Cache, Data Cache]
---

# Caching Architecture

## **Priority: P1 (HIGH)**

Next.js has 4 distinct caching layers. Understanding them prevents stale data bugs.

## **Modern Standard: Cache Components (Next.js 16+)**

> [!IMPORTANT]
> Next.js 16 favors the `'use cache'` directive over `unstable_cache`. Wrap dynamic runtime data in `<Suspense>`.

### **Core Protocol**

1. **Dynamic Shell**: Keep layouts static or cached; use `<Suspense>` for user-specific data.
2. **Deterministic Cache**: Add `'use cache'` and `cacheLife()` to server functions.
3. **Invalidation**:
   - `updateTag()`: Immediate sync reflect.
   - `revalidateTag()`: Background refresh (SWR).

## **The 4 Caching Layers**

| Layer                   | Where  | Control                        |
| :---------------------- | :----- | :----------------------------- |
| **Request Memoization** | Server | React `cache()`                |
| **Data Cache**          | Server | `'use cache'`, `revalidateTag` |
| **Full Route Cache**    | Server | Static Prerendering            |
| **Router Cache**        | Client | `router.refresh()`             |

## **Implementation Details**

See [Cache Components & PPR](references/CACHE_COMPONENTS.md) for detailed key generation, closure constraints, and invalidation strategies.
