---
name: nextjs-pwa
description: Comprehensive guide for building Progressive Web Apps (PWA) with Next.js using modern 2025 approaches. Use when users need to implement PWA features in Next.js applications including installability, offline support, service workers, web app manifests, caching strategies, push notifications, or converting existing Next.js apps to PWA. Covers both native Next.js PWA support (zero dependencies, App Router) and Serwist package (advanced offline capabilities, service worker management). Also use when troubleshooting PWA issues, optimizing PWA performance, or migrating from deprecated packages like next-pwa.
---

# Next.js PWA Implementation Guide (2025)

Comprehensive skill for implementing Progressive Web Apps with Next.js using the most current approaches as of 2025.

## Quick Start Decision Tree

Follow this decision tree to choose the right implementation:

```
Need PWA with Next.js?
│
├─ Basic installability only?
│  └─ Use: Native Next.js PWA Support
│     ✓ Zero dependencies
│     ✓ Built-in App Router support
│     ✓ Simple manifest.ts/json
│     ✗ No offline caching
│
└─ Need offline functionality?
   └─ Use: Serwist Package
      ✓ Advanced caching strategies
      ✓ Service worker management
      ✓ Background sync
      ✓ Push notifications
      ⚠ Requires configuration
```

---

## Approach 1: Native Next.js PWA Support

### Overview
Zero-dependency PWA implementation using Next.js built-in features.

### When to Use
- ✅ Using App Router (`/app` directory)
- ✅ Basic PWA features (installability, manifest)
- ✅ Don't need complex offline caching
- ✅ Want zero external dependencies
- ✅ Following official Next.js recommendations

### Key Features
- Built-in support since Fall 2024 (official PWA guide published)
- No external packages required
- Manifest generation via `manifest.ts`, `manifest.json`, or `manifest.webmanifest`
- Works seamlessly with App Router
- TypeScript support with `MetadataRoute.Manifest` type

### Limitations
- No automatic offline support
- No service worker generation
- No advanced caching strategies
- Manual service worker implementation required for offline features

### Quick Implementation

**1. Create Manifest (`app/manifest.ts`):**
```typescript
import type { MetadataRoute } from 'next'

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: 'Your App Name',
    short_name: 'App',
    description: 'Your app description',
    start_url: '/',
    display: 'standalone',
    background_color: '#ffffff',
    theme_color: '#000000',
    icons: [
      {
        src: '/icon-192.png',
        sizes: '192x192',
        type: 'image/png',
      },
      {
        src: '/icon-512.png',
        sizes: '512x512',
        type: 'image/png',
      },
    ],
  }
}
```

**2. Add Meta Tags (`app/layout.tsx`):**
```tsx
export const metadata = {
  manifest: '/manifest.webmanifest',
  appleWebApp: {
    capable: true,
    statusBarStyle: 'default',
    title: 'Your App Name',
  },
}
```

**3. Deploy with HTTPS** (Required for production PWA)

---

## Approach 2: Serwist Package

### Overview
Advanced PWA implementation with offline support, caching strategies, and service worker management.

### When to Use
- ✅ Need offline functionality
- ✅ Advanced caching strategies required
- ✅ Background sync needed
- ✅ Push notifications
- ✅ Complex service worker logic
- ✅ Fine-grained cache control

### Version Information (Updated November 2025)
- **Serwist Latest Stable:** 9.2.1+
- **Preview Version:** 10.0.0-preview (in development)
- **Breaking Changes:** v9.0.0 introduced major API changes (March 2024)
- **Node.js Required:** 18.0.0+ (22.x recommended)
- **TypeScript:** 5.0.0+

### Key Features
- Automatic service worker generation
- Pre-caching of static assets
- Runtime caching strategies (CacheFirst, NetworkFirst, StaleWhileRevalidate)
- Background sync
- Push notifications support
- Offline fallback pages
- TypeScript support

### Turbopack Compatibility (Updated November 2025)

**Important Update:**

✅ **Production builds** (`next build`): **Fully compatible** - Works normally with Turbopack
⚠️ **Development** (`next dev --turbo`): Shows warning but **fully functional**

**Development Warning Solution:**

```bash
# Option 1: Suppress warning (Recommended for dev)
# Add to .env.local
SERWIST_SUPPRESS_TURBOPACK_WARNING="1"

# Option 2: Use webpack in development
npm run dev -- --webpack
```

**Note:** The `--webpack` flag is **NOT required** for production builds. Serwist works natively with Turbopack in production.

### Installation

```bash
npm i @serwist/next && npm i -D serwist
# or
yarn add @serwist/next && yarn add -D serwist
# or
pnpm add @serwist/next && pnpm add -D serwist
```

### Quick Implementation

**1. Configure `next.config.js`:**

```javascript
import withSerwistInit from '@serwist/next'

const withSerwist = withSerwistInit({
  swSrc: 'app/sw.ts',
  swDest: 'public/sw.js',
  cacheOnNavigation: true,
  reloadOnOnline: true,
  disable: process.env.NODE_ENV === 'development', // Optional
})

export default withSerwist({
  // Your Next.js config
})
```

**2. Create Service Worker (`app/sw.ts`):**

```typescript
import { Serwist } from 'serwist'

const serwist = new Serwist({
  precacheEntries: self.__SW_MANIFEST,
  skipWaiting: true,
  clientsClaim: true,
  navigationPreload: true,
  runtimeCaching: [
    {
      urlPattern: /^https:\/\/fonts\.(?:googleapis|gstatic)\.com\/.*/i,
      handler: 'CacheFirst',
      options: {
        cacheName: 'google-fonts',
        expiration: {
          maxEntries: 4,
          maxAgeSeconds: 365 * 24 * 60 * 60, // 1 year
        },
      },
    },
    {
      urlPattern: /\.(?:eot|otf|ttc|ttf|woff|woff2|font.css)$/i,
      handler: 'StaleWhileRevalidate',
      options: {
        cacheName: 'static-font-assets',
        expiration: {
          maxEntries: 4,
          maxAgeSeconds: 7 * 24 * 60 * 60, // 1 week
        },
      },
    },
    {
      urlPattern: /\.(?:jpg|jpeg|gif|png|svg|ico|webp)$/i,
      handler: 'StaleWhileRevalidate',
      options: {
        cacheName: 'static-image-assets',
        expiration: {
          maxEntries: 64,
          maxAgeSeconds: 24 * 60 * 60, // 1 day
        },
      },
    },
    {
      urlPattern: /\/_next\/image\?url=.+$/i,
      handler: 'StaleWhileRevalidate',
      options: {
        cacheName: 'next-image',
        expiration: {
          maxEntries: 64,
          maxAgeSeconds: 24 * 60 * 60, // 1 day
        },
      },
    },
    {
      urlPattern: /\.(?:js)$/i,
      handler: 'StaleWhileRevalidate',
      options: {
        cacheName: 'static-js-assets',
        expiration: {
          maxEntries: 32,
          maxAgeSeconds: 24 * 60 * 60, // 1 day
        },
      },
    },
    {
      urlPattern: /\.(?:css|less)$/i,
      handler: 'StaleWhileRevalidate',
      options: {
        cacheName: 'static-style-assets',
        expiration: {
          maxEntries: 32,
          maxAgeSeconds: 24 * 60 * 60, // 1 day
        },
      },
    },
    {
      urlPattern: /\/_next\/data\/.+\/.+\.json$/i,
      handler: 'StaleWhileRevalidate',
      options: {
        cacheName: 'next-data',
        expiration: {
          maxEntries: 32,
          maxAgeSeconds: 24 * 60 * 60, // 1 day
        },
      },
    },
    {
      urlPattern: /\/api\/.*/i,
      handler: 'NetworkFirst',
      method: 'GET',
      options: {
        cacheName: 'apis',
        expiration: {
          maxEntries: 16,
          maxAgeSeconds: 24 * 60 * 60, // 1 day
        },
        networkTimeoutSeconds: 10,
      },
    },
    {
      urlPattern: /.*/i,
      handler: 'NetworkFirst',
      options: {
        cacheName: 'others',
        expiration: {
          maxEntries: 32,
          maxAgeSeconds: 24 * 60 * 60, // 1 day
        },
        networkTimeoutSeconds: 10,
      },
    },
  ],
})

serwist.addEventListeners()
```

**3. Register Service Worker (`app/layout.tsx`):**

```tsx
'use client'

import { useEffect } from 'react'

export default function RootLayout({ children }) {
  useEffect(() => {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker
        .register('/sw.js')
        .then((registration) => {
          console.log('Service Worker registered:', registration)
        })
        .catch((error) => {
          console.error('Service Worker registration failed:', error)
        })
    }
  }, [])

  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

**4. Update `tsconfig.json`:**

```json
{
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "esnext", "webworker"],
    "types": ["@serwist/next/typings"]
  }
}
```

**5. Create Manifest (same as Native approach)**

---

## Breaking Changes: Serwist v9.0.0+

If migrating from older versions, note these critical changes:

### 1. **Import Changes**
```typescript
// ❌ OLD (v8.x and earlier)
import { installSerwist } from '@serwist/sw'

// ✅ NEW (v9.0.0+)
import { Serwist } from 'serwist'
```

### 2. **Initialization Changes**
```typescript
// ❌ OLD
const sw = installSerwist({ /* config */ })

// ✅ NEW
const serwist = new Serwist({ /* config */ })
serwist.addEventListeners() // Required!
```

### 3. **Package Consolidation**
```bash
# ❌ OLD
npm i @serwist/precaching @serwist/routing @serwist/strategies

# ✅ NEW (all in one)
npm i -D serwist
```

---

## Comparison: Native vs Serwist

| Feature | Native Next.js | Serwist |
|---------|---------------|---------|
| **Setup Complexity** | ⭐ Simple | ⭐⭐⭐ Moderate |
| **Dependencies** | ✅ Zero | ⚠️ 2 packages |
| **Offline Support** | ❌ Manual | ✅ Automatic |
| **Caching Strategies** | ❌ None | ✅ Multiple |
| **Service Worker** | ❌ Manual | ✅ Auto-generated |
| **App Router Support** | ✅ Native | ✅ Full |
| **Pages Router Support** | ⚠️ Limited | ✅ Full |
| **TypeScript** | ✅ Built-in | ✅ Full |
| **Production Ready** | ✅ Yes | ✅ Yes |
| **Turbopack Compatible** | ✅ Yes | ✅ Yes (with env var) |

---

## Common Issues & Solutions

### Issue 1: Service Worker Not Updating
**Solution:** Add versioning to your service worker or use `skipWaiting: true`

### Issue 2: Cached Content Not Updating
**Solution:** Implement proper cache invalidation strategy or reduce `maxAgeSeconds`

### Issue 3: Turbopack Warning in Development
**Solution:** Add `SERWIST_SUPPRESS_TURBOPACK_WARNING="1"` to `.env.local`

### Issue 4: HTTPS Required Error
**Solution:** Deploy to HTTPS domain (localhost works for testing)

### Issue 5: Icons Not Showing
**Solution:** Ensure icons are in `public/` directory and manifest paths are correct

---

## Recommendations

### For New Projects:
1. **Start with Native Next.js PWA** (simple, zero dependencies)
2. **Upgrade to Serwist** only when offline features are needed

### For Existing Projects:
1. **Migrating from `next-pwa`?** → Use Serwist (direct replacement)
2. **Already have custom service worker?** → Keep it or refactor to Serwist
3. **Using Pages Router?** → Serwist recommended (better support)

### For Production:
1. ✅ Always use HTTPS
2. ✅ Test offline functionality thoroughly
3. ✅ Implement proper error handling
4. ✅ Monitor service worker updates
5. ✅ Use appropriate cache strategies for different assets

---

## Resources

- **Next.js PWA Docs:** https://nextjs.org/docs/app/api-reference/file-conventions/metadata/manifest
- **Serwist Docs:** https://serwist.pages.dev
- **Serwist GitHub:** https://github.com/serwist/serwist
- **Web App Manifest Spec:** https://www.w3.org/TR/appmanifest/
- **Service Worker API:** https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API

---

## Version History

- **November 2025:** Updated Serwist version info, Turbopack compatibility clarifications
- **Fall 2024:** Native Next.js PWA support officially documented
- **March 2024:** Serwist v9.0.0 released with breaking changes
- **2023:** Serwist created as modern alternative to Workbox

---

## Consulte os seguintes arquivos para obter informações completas e atualizadas:

C:\Users\tetu_\.claude\skills\nextjs-pwa\references\serwist-implementation.md
C:\Users\tetu_\.claude\skills\nextjs-pwa\references\native-nextjs-implementation.md
C:\Users\tetu_\.claude\skills\nextjs-pwa\references\implementation-approaches.md

**Last Updated:** November 13, 2025