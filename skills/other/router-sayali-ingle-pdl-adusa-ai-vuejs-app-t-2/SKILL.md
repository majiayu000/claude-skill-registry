---
name: router
description: Generates src/router/index.ts with Vue Router configuration, hash-based routing, and navigation guards for route protection.
---

# Router Skill

## Purpose
Generate the `src/router/index.ts` file with Vue Router configuration and navigation guards.

## Input Parameters
- `application_type`: "micro-frontend" or "standalone"

## Output
Create the file: `src/router/index.ts`

## Import Strategy (CRITICAL)

### Micro-Frontend Applications (`application_type: "micro-frontend"`)
**MUST use direct imports** - NO lazy loading:
```typescript
import Home from '@/views/Home/Home.vue';
import PageNotFoundView from '@/views/PageNotFoundView/PageNotFoundView.vue';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: Home,  // Direct import
    meta: { requiresAuth: true },
  },
];
```

**Why**: Micro-frontends require a single bundle file (`app.js`). Lazy loading (`() => import()`) causes code splitting into multiple chunks, breaking single-spa integration.

### Standalone Applications (`application_type: "standalone"`)
**RECOMMENDED: Use lazy loading** for better performance:
```typescript
const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home/Home.vue'),  // Lazy loading
    meta: { requiresAuth: true },
  },
];
```

**Why**: Standalone apps benefit from code splitting for faster initial load times.

## Notes
- Uses hash-based routing with `createWebHashHistory`
- Implements navigation guards for example usage
- Create 2 routes: home screen and page not found screen
- All pages except page not found should have navigation guards
- Import strategy differs based on `application_type` parameter
