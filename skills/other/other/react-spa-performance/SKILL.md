---
name: react-spa-performance
description: React 19 + Vite 7 SPA performance optimization guide. Apply when writing, reviewing, or refactoring React components, routes, data fetching, bundle config, or performance in any Vite SPA project. Covers build optimization, code splitting, re-render prevention, context design, virtualization, media loading, bundle analysis, TanStack Query, CSS, and dev performance.
---

# React SPA Performance (Vite + React 19)

Dense performance reference for React 19 + Vite 7 SPAs. No SSR. No Next.js.

Target projects:
- **peek-stash-browser** `client/` — React 19, Vite 7, Tailwind v3, Video.js, React Router v7 declarative, React Compiler
- **stash-sense-trainer** `web/` — React 19, Vite 7, Tailwind v4, TanStack Query v5, React Router v7

---

## 1. Vite Build Optimization

**manualChunks** — group by update frequency, only node_modules:
```js
rollupOptions: {
  output: {
    manualChunks: {
      'react-vendor': ['react', 'react-dom', 'react-router-dom'],
      'query-vendor': ['@tanstack/react-query'],
      'video-vendor': ['video.js'],  // isolate heavy libs used on few routes
    },
  },
}
```
Keep chunks under 200KB gzipped. Isolate heavy libs (video.js, recharts) so they load on demand.

**optimizeDeps** — pre-bundle CJS deps for faster dev startup:
```js
optimizeDeps: {
  include: ['react', 'react-dom', 'video.js'], // CJS libs benefit most
  exclude: ['local-linked-packages'],
}
```

**CSS code splitting** — `build.cssCodeSplit: true` (default). Each lazy route gets its own CSS chunk automatically.

**Asset inlining** — `build.assetsInlineLimit: 4096` (default 4KB). Raise to 8192 for many small icons.

**Build target** — `build.target: 'es2022'` unless supporting older browsers. Smaller output, no polyfills.

**Tree shaking** — `rollupOptions.treeshake.moduleSideEffects: false` (assume modules pure). Override per-module if needed.

**Minification** — `esbuild` is 10-100x faster than `terser`. Use `terser` only when the extra 1-3% matters:
```js
build: { minify: 'terser', terserOptions: { compress: { drop_console: true, drop_debugger: true } } }
```

---

## 2. Code Splitting & Lazy Loading

**Route-level splitting** — every page component via `React.lazy`:
```jsx
const Scenes = lazy(() => import('./pages/Scenes'));
// Single Suspense wrapping Routes for route transitions
<Suspense fallback={<PageSkeleton />}><Routes>...</Routes></Suspense>
```
Never lazy-load the shell/layout. Add nested `<Suspense>` for heavy sub-components within pages.

**Dynamic imports for heavy libs** — non-component imports:
```js
async function exportData() {
  const { exportToCsv } = await import('./utils/export');
  exportToCsv(data);
}
```

**Preload on hover/focus** for perceived instant navigation:
```jsx
const preload = () => { void import('./pages/Scenes'); };
<Link to="/scenes" onMouseEnter={preload} onFocus={preload}>Scenes</Link>
```

**Barrel file avoidance** — CRITICAL (200-800ms import cost):
```jsx
// BAD: import { Check, X } from 'lucide-react';
// GOOD:
import Check from 'lucide-react/dist/esm/icons/check';
```
Affected: `lucide-react`, `react-icons`, `@radix-ui/*`, `lodash`, `date-fns`. For your own code: import from specific files, not `components/index.js`.

---

## 3. Re-render Prevention

**React.memo** — use when: component receives objects/arrays + parent re-renders frequently, or renders large subtree. Skip when: cheap component, primitive props, or React Compiler is enabled.

**React 19 Compiler** — when `babel-plugin-react-compiler` is active (peek-stash-browser), the compiler auto-memoizes components, hooks, and JSX. Remove manual `memo()`, `useMemo`, `useCallback` unless they serve a semantic purpose. Without compiler: apply manual memoization.

**Hoist default non-primitive props:**
```jsx
const EMPTY = [];  // outside component
<TagList tags={EMPTY} />  // stable reference, doesn't break memo
```

**Derived state over useEffect chains** — never `setState` in effect to transform props:
```jsx
// BAD: useEffect(() => setFull(first + ' ' + last), [first, last]);
// GOOD: const fullName = first + ' ' + last;
// GOOD (expensive): const sorted = useMemo(() => items.toSorted(compare), [items]);
```

**Don't wrap simple primitives in useMemo** — hook overhead > computation cost.

**Functional setState** for stable callbacks:
```jsx
// BAD: useCallback(() => setCount(count + 1), [count]);
// GOOD: useCallback(() => setCount(c => c + 1), []);
```

**startTransition** for non-urgent updates (filtering lists, tab switches, sorting):
```jsx
const [isPending, startTransition] = useTransition();
startTransition(() => onFilter(value));  // doesn't block typing
```

**Lifting/pushing state** — push state down to the child that owns it. Lift only to nearest common ancestor. Never store server data in React state when TanStack Query handles it.

---

## 4. Context Performance

**Split state vs dispatch** — components calling only `dispatch` never re-render on state changes:
```jsx
const StateCtx = createContext();
const DispatchCtx = createContext();
// Provide dispatch in outer, state in inner
```

**Context vs props vs TanStack Query:**
| Need | Solution |
|------|----------|
| Server data | TanStack Query (never context) |
| Auth/theme/locale (rare changes) | Context |
| 1-2 levels of props | Props directly |
| Frequent complex state | useReducer + split context, or Zustand |

**Avoid provider cascades** — compose with a utility if >4 providers deep.

**useSyncExternalStore** — subscribe to external stores (localStorage, URL params, window size) without tearing. Required `getServerSnapshot` arg can return `null` for SPAs.

---

## 5. List & Grid Performance

**Virtualize lists >100 items** — `react-window` (lightweight, fixed size) or `react-virtuoso` (dynamic heights, grouping, infinite scroll). Renders only visible items.

**Keys** — always stable unique IDs, never array index. For composite keys: `` key={`${id}-${instanceId}`} ``.

**Avoid inline objects/functions in list iterations:**
```jsx
const CARD_STYLE = { margin: 8 };  // hoist outside
items.map(item => <Card key={item.id} style={CARD_STYLE} />)
```

**Pagination vs infinite scroll** — pagination for deep content with page jumping; infinite scroll for media browsing (combine with virtualization). Cursor-based for real-time data.

---

## 6. Image & Media Loading

**Native lazy loading** — `<img loading="lazy" width={W} height={H} />`. Always set dimensions to prevent layout shift.

**srcset** — provide multiple resolutions with `sizes` attribute for responsive images.

**Placeholders** — blurhash/LQIP, dominant color background, or CSS skeleton shimmer.

**Video.js lazy init:**
- Lazy-load the entire VideoPlayer component via `React.lazy`
- Separate into its own manualChunk: `'video-vendor': ['video.js']`
- Always call `player.dispose()` on unmount (memory leak otherwise)
- Never re-create player on prop changes — use `player.src()` to update
- Initialize in `useEffect` with ref guard, dispose in cleanup

---

## 7. Bundle Analysis

**vite-plugin-visualizer:**
```js
visualizer({ filename: 'dist/stats.html', gzipSize: true, brotliSize: true })
```
Run `npm run build`, open `dist/stats.html`.

**Common offenders:**
| Library | ~Size (min+gz) | Mitigation |
|---------|---------------|------------|
| video.js | 150KB | manualChunk + lazy route |
| recharts | 120KB | dynamic import on stats page |
| lucide-react (barrel) | 80KB | direct icon imports |
| date-fns (full) | 30KB | direct function imports |

**Dynamic import boundaries** — draw at: route level, heavy feature components (video, charts, editors), admin-only features, modals with heavy content.

**CI monitoring** — track `dist/assets/*.js` sizes. Alert on >10% increase.

---

## 8. Data Fetching Performance (TanStack Query)

**staleTime / gcTime defaults:**
```js
defaultOptions: { queries: { staleTime: 5 * 60_000, gcTime: 30 * 60_000, refetchOnWindowFocus: false } }
```
Static data (tags, studios): `staleTime: Infinity`. User data (ratings): `60_000`. Real-time: `0`.

**Prefetch on hover:**
```jsx
const prefetch = () => queryClient.prefetchQuery({ queryKey: ['scene', id], queryFn: ... });
<Link onMouseEnter={prefetch}>...</Link>
```

**Query key factories** — hierarchical keys for targeted invalidation:
```js
export const sceneKeys = {
  all: ['scenes'], lists: () => [...sceneKeys.all, 'list'],
  list: (filters) => [...sceneKeys.lists(), filters],
  detail: (id) => [...sceneKeys.all, 'detail', id],
};
```

**Parallel queries** — `useQueries` for dynamic lists of queries. TanStack auto-deduplicates identical queryKeys across components.

**Eliminate waterfalls** — never chain dependent queries when you can combine in a single queryFn with `Promise.all`:
```jsx
queryFn: async () => {
  const scene = await fetchScene(id);
  const [performers, tags] = await Promise.all([fetchPerformers(scene.pIds), fetchTags(scene.tIds)]);
  return { scene, performers, tags };
}
```

---

## 9. CSS Performance

**Tailwind purge** — v3: verify `content` covers all templates. v4: automatic detection, no manual config needed.

**No runtime CSS-in-JS** — never use styled-components/emotion in Tailwind projects. Tailwind is build-time static CSS.

**CSS containment** for independent sections:
```css
.card-grid-item { contain: layout style paint; }
.below-fold { content-visibility: auto; contain-intrinsic-size: 0 500px; }
```
`content-visibility: auto` skips rendering off-screen elements — major win for long lists without virtualization.

**will-change** — only on elements that WILL animate, remove after animation. Never apply broadly.

**Layout thrash** — batch reads then batch writes. Prefer CSS classes over inline style manipulation. Use `requestAnimationFrame` for DOM mutations after measurement.

---

## 10. Dev Performance

**HMR** — keep fast by: avoiding top-level side effects, one component per file, separate context providers from consumers.

**Pre-bundling** — clear cache with `rm -rf node_modules/.vite` if HMR breaks. Add CJS deps to `optimizeDeps.include`.

**Env variables** — only `VITE_` prefixed vars exposed to client. Never put secrets in `VITE_` vars. Use `import.meta.env.DEV` / `import.meta.env.PROD` for conditional code (tree-shaken).

**Docker watch** — use `usePolling` only on Windows (WSL2). Linux native inotify works without polling.

---

## Universal Rules (from Vercel React Best Practices, adapted for SPA)

| Rule | Impact | Action |
|------|--------|--------|
| Eliminate waterfalls | CRITICAL | `Promise.all()` for independent fetches, start promises early |
| Barrel import avoidance | CRITICAL | Import from specific file paths, not index re-exports |
| Dynamic imports | CRITICAL | `React.lazy` + `Suspense` for routes; `import()` for heavy libs |
| Derived state | MEDIUM | Compute during render, never setState-in-useEffect to sync |
| Memo hygiene | MEDIUM | `memo()` for expensive subtrees, skip for trivial components |
| Transitions | MEDIUM | `startTransition` for filtering, sorting, non-urgent updates |
| Functional setState | MEDIUM | `setX(prev => ...)` for dep-free stable callbacks |
| Passive listeners | MEDIUM | `{ passive: true }` for scroll/touch/wheel handlers |
| Hoist statics | LOW-MEDIUM | Constants, RegExp, default props outside component body |
| Early returns | LOW-MEDIUM | Exit functions early, defer expensive work to branches that need it |
| Lazy state init | LOW | `useState(() => expensive())` not `useState(expensive())` |
| useRef for transients | LOW | Ref for frequently-changing values not used in render (mouse pos, timers) |
