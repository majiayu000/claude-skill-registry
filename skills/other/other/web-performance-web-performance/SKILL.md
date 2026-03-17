---
name: web-performance-web-performance
description: Bundle optimization, render performance
---

# Performance Standards

> **Quick Guide:** Build performance? Turborepo caching with >80% hit rate. Bundle budgets? < 200KB main bundle. Core Web Vitals? LCP < 2.5s, INP < 200ms, CLS < 0.1. React patterns? Strategic memo/useMemo (or React Compiler), lazy loading, virtualization for 100+ items. Monitoring? Real User Monitoring with web-vitals library.

---

<critical_requirements>

## CRITICAL: Before Optimizing Performance

**(You MUST set performance budgets BEFORE building features - bundle size limits, Core Web Vitals targets, build time thresholds)**

**(You MUST profile BEFORE optimizing - measure actual bottlenecks with Chrome DevTools, React Profiler, or Lighthouse)**

**(You MUST use named constants for ALL performance thresholds - no magic numbers like `< 200KB` or `< 2.5s`)**

**(You MUST monitor Core Web Vitals in production with web-vitals library - track LCP, INP, CLS for real users)**

**(You MUST lazy load route components and heavy libraries - code splitting prevents large initial bundles)**

</critical_requirements>

---

**Detailed Resources:**

- For code examples, see [examples.md](examples.md)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

**Auto-detection:** Core Web Vitals, bundle size optimization, LCP, INP, CLS, FID, lazy loading, memoization, React Compiler, performance monitoring, web-vitals library, Turborepo caching, bundle budget, virtualization

**When to use:**

- Optimizing Core Web Vitals (LCP < 2.5s, INP < 200ms, CLS < 0.1)
- Setting and enforcing bundle size budgets (< 200KB main bundle)
- Implementing React performance patterns (strategic memo, lazy loading, virtualization)
- Monitoring performance with web-vitals library in production
- Configuring Turborepo caching for build performance (> 80% cache hit rate)

**When NOT to use:**

- Before measuring (premature optimization adds complexity without benefit)
- For simple components (memoizing cheap renders adds overhead)
- Internal admin tools with < 10 users (ROI too low)
- Prototypes and MVPs (optimize after validating product-market fit)

**Key patterns covered:**

- Core Web Vitals targets (LCP < 2.5s, INP < 200ms, CLS < 0.1)
- Bundle size budgets (< 200KB main, < 500KB total initial load)
- Strategic React optimization (memo/useMemo when needed, not everywhere - profile first)
- Image optimization (WebP/AVIF, lazy loading, Next.js Image component)
- Build performance with Turborepo caching and parallel execution

---

<philosophy>

## Philosophy

Performance is a feature, not an afterthought. Fast applications improve user experience, conversion rates, and SEO rankings. Performance optimization requires measurement before action, budgets before building, and monitoring in production.

**Core performance principles:**

- **Measure first, optimize second** - Profile actual bottlenecks, don't guess
- **Set budgets early** - Define bundle size limits and Core Web Vitals targets before building
- **Monitor real users** - Lab metrics (Lighthouse) differ from real-world performance (RUM)
- **Optimize strategically** - Memoize expensive operations, not everything
- **Lazy load by default** - Load code when needed, not upfront

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Build Performance with Turborepo Caching

Use Turborepo to cache build artifacts across machines (local and CI). Target > 80% cache hit rate for optimal build performance.

#### Build Time Targets

```typescript
// constants/performance.ts
export const BUILD_TIME_TARGETS = {
  FULL_BUILD_COLD_CACHE_MINUTES: 2,
  INCREMENTAL_BUILD_WARM_CACHE_SECONDS: 30,
  DEVELOPMENT_REBUILD_HMR_SECONDS: 5,
  PRODUCTION_BUILD_MINUTES: 5,
} as const;

export const CACHE_HIT_RATE_TARGET_PERCENT = 80;
```

**Targets:**

- **Full build** (cold cache): < 2 min
- **Incremental build** (warm cache): < 30s
- **Development rebuild** (HMR): < 5s
- **Production build**: < 5 min
- **Cache hit rate**: > 80%

For detailed Turborepo configuration examples, see [examples.md](examples.md#turborepo-configuration).

---

### Pattern 2: Bundle Size Budgets

Set and enforce bundle size limits to prevent bloat. Main bundle should be < 200KB gzipped for fast downloads on 3G networks.

#### Bundle Size Constants

```typescript
// constants/bundle-budgets.ts
export const BUNDLE_SIZE_BUDGETS_KB = {
  MAIN_BUNDLE_GZIPPED: 200,
  VENDOR_BUNDLE_GZIPPED: 150,
  ROUTE_BUNDLE_GZIPPED: 100,
  TOTAL_INITIAL_LOAD_GZIPPED: 500,
  MAIN_CSS_GZIPPED: 50,
  CRITICAL_CSS_INLINE: 14, // Fits in first TCP packet
} as const;

export const IMAGE_SIZE_BUDGETS_KB = {
  HERO_IMAGE: 200,
  THUMBNAIL: 50,
} as const;
```

#### Recommended Budgets

**JavaScript bundles:**

- **Main bundle**: < 200 KB (gzipped)
- **Vendor bundle**: < 150 KB (gzipped)
- **Route bundles**: < 100 KB each (gzipped)
- **Total initial load**: < 500 KB (gzipped)

**Why these limits:** 200 KB ≈ 1 second download on 3G, faster Time to Interactive (TTI), better mobile performance

**CSS bundles:**

- **Main CSS**: < 50 KB (gzipped)
- **Critical CSS**: < 14 KB (inlined, fits in first TCP packet)

**Images:**

- **Hero images**: < 200 KB (use WebP/AVIF)
- **Thumbnails**: < 50 KB
- **Icons**: Use SVG or icon fonts

For code splitting and bundle analysis examples, see [examples.md](examples.md#code-splitting-strategies).

---

### Pattern 3: Core Web Vitals Optimization

Optimize for Google's Core Web Vitals: LCP < 2.5s, INP < 200ms, CLS < 0.1. These metrics impact SEO and user experience.

**Note:** INP (Interaction to Next Paint) replaced FID (First Input Delay) as a Core Web Vital on March 12, 2024. FID is now deprecated.

#### Core Web Vitals Constants

```typescript
// constants/web-vitals.ts
export const CORE_WEB_VITALS_THRESHOLDS = {
  LCP_SECONDS: 2.5, // Largest Contentful Paint
  FID_MS: 100, // First Input Delay
  INP_MS: 200, // Interaction to Next Paint (replacing FID)
  CLS_SCORE: 0.1, // Cumulative Layout Shift
  FCP_SECONDS: 1.8, // First Contentful Paint
  TTI_SECONDS: 3.8, // Time to Interactive
  TBT_MS: 300, // Total Blocking Time
  TTFB_MS: 800, // Time to First Byte
} as const;
```

#### LCP (Largest Contentful Paint): < 2.5s

Measures loading performance. When largest element becomes visible.

**How to improve:**

- Optimize images (WebP, lazy loading)
- Minimize render-blocking resources
- Use CDN for static assets
- Server-side rendering (SSR) or Static Site Generation (SSG)

#### INP (Interaction to Next Paint): < 200ms

Measures interactivity. Time from user interaction to next visual update. INP replaced FID as a Core Web Vital on March 12, 2024.

**Why INP replaced FID:** FID only measured the first interaction and only the input delay. INP measures ALL interactions throughout the page visit, including input delay, processing time, and presentation delay.

**How to improve:**

- Minimize JavaScript execution time
- Code splitting (load less JS upfront)
- Use web workers for heavy computation
- Debounce/throttle expensive event handlers
- Break up long tasks (> 50ms) with `scheduler.yield()` or `setTimeout`

#### CLS (Cumulative Layout Shift): < 0.1

Measures visual stability. Prevents unexpected layout shifts.

**How to improve:**

- Set image/video dimensions
- Reserve space for dynamic content
- Avoid injecting content above existing content
- Use `font-display: swap` with size-adjust

For detailed Core Web Vitals examples and production monitoring setup, see [examples.md](examples.md#core-web-vitals-examples).

</patterns>

---

<critical_reminders>

## CRITICAL REMINDERS

**(You MUST set performance budgets BEFORE building features - bundle size limits, Core Web Vitals targets, build time thresholds)**

**(You MUST profile BEFORE optimizing - measure actual bottlenecks with Chrome DevTools, React Profiler, or Lighthouse)**

**(You MUST use named constants for ALL performance thresholds - no magic numbers like `< 200KB` or `< 2.5s`)**

**(You MUST monitor Core Web Vitals in production with web-vitals library - track LCP, INP, CLS for real users)**

**(You MUST lazy load route components and heavy libraries - code splitting prevents large initial bundles)**

**Failure to follow these rules will result in slow applications, poor Core Web Vitals, large bundles, and degraded user experience.**

</critical_reminders>
