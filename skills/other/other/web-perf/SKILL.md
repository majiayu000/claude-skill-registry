---
name: web-perf
description: Structured 5-phase web performance audit workflow with Core Web Vitals thresholds and actionable optimization recommendations. Use when auditing website performance, diagnosing slow page loads, optimizing Core Web Vitals scores, or reviewing frontend performance patterns. Covers Webpack, Vite, Next.js, and Nuxt optimization.
license: MIT
metadata:
  author: cloudflare
  version: '1.0.0'
  source: cloudflare/skills
verified: true
lastVerifiedAt: 2026-02-22T00:00:00.000Z
version: '1.0.0'
tools: []
---

# Web Performance Audit

Structured 5-phase web performance audit workflow. Diagnose performance bottlenecks, measure Core Web Vitals, and produce actionable optimization recommendations.

## When to Apply

Use this skill when:

- Auditing website performance for Core Web Vitals compliance
- Diagnosing slow page loads, high Time to Interactive, or layout shifts
- Optimizing Largest Contentful Paint (LCP), Cumulative Layout Shift (CLS), or Interaction to Next Paint (INP)
- Reviewing frontend code for performance anti-patterns
- Preparing a site for Google's page experience ranking signals
- Optimizing build output for Webpack, Vite, Next.js, or Nuxt

## Core Web Vitals Thresholds

| Metric  | Good     | Needs Improvement | Poor    | What It Measures             |
| ------- | -------- | ----------------- | ------- | ---------------------------- |
| **LCP** | <= 2.5s  | 2.5s - 4.0s       | > 4.0s  | Loading performance          |
| **CLS** | <= 0.1   | 0.1 - 0.25        | > 0.25  | Visual stability             |
| **INP** | <= 200ms | 200ms - 500ms     | > 500ms | Interactivity (replaced FID) |

### Additional Performance Metrics

| Metric          | Good     | Poor     | What It Measures              |
| --------------- | -------- | -------- | ----------------------------- |
| **FCP**         | <= 1.8s  | > 3.0s   | First content rendered        |
| **TTFB**        | <= 800ms | > 1800ms | Server response time          |
| **TBT**         | <= 200ms | > 600ms  | Main thread blocking          |
| **Speed Index** | <= 3.4s  | > 5.8s   | Visual completeness over time |

## 5-Phase Audit Workflow

### Phase 1: Performance Trace

Capture a performance trace to establish baseline metrics.

**Browser-Based (Chrome DevTools):**

1. Open Chrome DevTools (F12) > Performance tab
2. Click "Record" and reload the page
3. Stop recording after page fully loads
4. Analyze the flame chart for:
   - Long tasks (> 50ms, marked in red)
   - Layout thrashing (forced reflow cycles)
   - Render-blocking resources
   - JavaScript execution bottlenecks

**Lighthouse Audit:**

```bash
# CLI-based Lighthouse audit
npx lighthouse https://example.com --output=json --output-path=./lighthouse-report.json

# With specific categories
npx lighthouse https://example.com --only-categories=performance --output=html

# Mobile simulation (default)
npx lighthouse https://example.com --preset=perf --throttling-method=simulate
```

**Key Trace Indicators:**

- **Main thread busy time**: Should be < 4s total
- **Largest task duration**: Should be < 250ms
- **Script evaluation time**: Should be < 2s
- **Layout/style recalculation**: Should be < 500ms

### Phase 2: Core Web Vitals Analysis

Measure each Core Web Vital and identify specific causes.

#### LCP Diagnosis

LCP measures loading performance -- when the largest content element becomes visible.

**Common LCP Elements:**

- `<img>` elements (hero images)
- `<video>` poster images
- Block-level elements with background images
- Text blocks (`<h1>`, `<p>`)

**LCP Optimization Checklist:**

1. **Preload the LCP resource**

   ```html
   <link rel="preload" as="image" href="/hero.webp" fetchpriority="high" />
   ```

2. **Eliminate render-blocking resources**

   ```html
   <!-- Defer non-critical CSS -->
   <link rel="stylesheet" href="/non-critical.css" media="print" onload="this.media='all'" />

   <!-- Async non-critical JS -->
   <script src="/analytics.js" async></script>
   ```

3. **Optimize server response time (TTFB)**
   - Use CDN for static assets
   - Enable HTTP/2 or HTTP/3
   - Implement server-side caching
   - Use streaming SSR where supported

4. **Optimize image delivery**
   ```html
   <!-- Modern format with fallback -->
   <picture>
     <source srcset="/hero.avif" type="image/avif" />
     <source srcset="/hero.webp" type="image/webp" />
     <img
       src="/hero.jpg"
       alt="Hero"
       width="1200"
       height="600"
       fetchpriority="high"
       decoding="async"
     />
   </picture>
   ```

#### CLS Diagnosis

CLS measures visual stability -- unexpected layout shifts during page load.

**Common CLS Causes:**

- Images without explicit dimensions
- Ads or embeds without reserved space
- Dynamically injected content above the fold
- Web fonts causing FOIT/FOUT (Flash of Invisible/Unstyled Text)

**CLS Optimization Checklist:**

1. **Always set image dimensions**

   ```html
   <img src="/photo.jpg" width="800" height="600" alt="Photo" />
   ```

   Or use CSS aspect-ratio:

   ```css
   .hero-image {
     aspect-ratio: 16 / 9;
     width: 100%;
   }
   ```

2. **Reserve space for dynamic content**

   ```css
   .ad-slot {
     min-height: 250px;
   }
   .skeleton {
     height: 200px;
     background: #f0f0f0;
   }
   ```

3. **Use `font-display: swap` with size-adjust**

   ```css
   @font-face {
     font-family: 'CustomFont';
     src: url('/font.woff2') format('woff2');
     font-display: swap;
     size-adjust: 100.5%; /* Match fallback font metrics */
   }
   ```

4. **Avoid inserting content above existing content**
   - Banners should push down from top, not shift existing content
   - Use `transform` animations instead of `top`/`left`/`width`/`height`

#### INP Diagnosis

INP measures interactivity -- the delay between user interaction and visual response.

**Common INP Causes:**

- Long JavaScript tasks blocking the main thread
- Synchronous layout/style recalculations
- Heavy event handlers
- Excessive re-renders (React, Vue)

**INP Optimization Checklist:**

1. **Break up long tasks**

   ```javascript
   // Instead of one long task
   function processAllItems(items) {
     for (const item of items) {
       /* heavy work */
     }
   }

   // Break into chunks with scheduler
   async function processAllItems(items) {
     for (const item of items) {
       processItem(item);
       // Yield to main thread between items
       await scheduler.yield();
     }
   }
   ```

2. **Debounce/throttle event handlers**

   ```javascript
   // Throttle scroll handler
   let ticking = false;
   window.addEventListener(
     'scroll',
     () => {
       if (!ticking) {
         requestAnimationFrame(() => {
           updateUI();
           ticking = false;
         });
         ticking = true;
       }
     },
     { passive: true }
   );
   ```

3. **Use `requestIdleCallback` for non-urgent work**
   ```javascript
   requestIdleCallback(() => {
     // Analytics, prefetching, non-visible updates
     sendAnalytics(data);
   });
   ```

### Phase 3: Network Analysis

Analyze network waterfall for optimization opportunities.

**Key Checks:**

1. **Resource count and total size**
   - Target: < 100 requests, < 2MB total (compressed)
   - Check: `performance.getEntriesByType('resource').length`

2. **Critical request chains**
   - Identify chains longer than 3 requests
   - Break chains with preload/prefetch hints

3. **Compression**
   - All text resources should use Brotli (br) or gzip
   - Check `Content-Encoding` header in response

4. **Caching headers**

   ```
   # Immutable assets (hashed filenames)
   Cache-Control: public, max-age=31536000, immutable

   # HTML documents
   Cache-Control: no-cache

   # API responses
   Cache-Control: private, max-age=0, must-revalidate
   ```

5. **HTTP/2+ multiplexing**
   - Verify protocol in DevTools Network tab
   - Multiple resources should load in parallel over single connection

### Phase 4: Accessibility Performance

Performance optimizations must not degrade accessibility.

**Validation Checklist:**

- [ ] Lazy-loaded images have `alt` attributes
- [ ] Deferred scripts do not break keyboard navigation
- [ ] Skeleton loaders have `aria-busy="true"` and `aria-label`
- [ ] `prefers-reduced-motion` is respected for animations
- [ ] Focus management works with dynamically loaded content

```css
/* Respect reduced motion preference */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### Phase 5: Codebase Analysis

Review source code for performance anti-patterns.

#### Webpack Optimization

```javascript
// webpack.config.js
module.exports = {
  optimization: {
    splitChunks: {
      chunks: 'all',
      maxInitialRequests: 25,
      minSize: 20000,
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name(module) {
            const packageName = module.context.match(/[\\/]node_modules[\\/](.*?)([\\/]|$)/)[1];
            return `vendor.${packageName.replace('@', '')}`;
          },
        },
      },
    },
  },
};
```

#### Vite Optimization

```javascript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom'],
        },
      },
    },
    cssCodeSplit: true,
    sourcemap: false, // Disable in production
  },
});
```

#### Next.js Optimization

```typescript
// next.config.ts
const nextConfig = {
  images: {
    formats: ['image/avif', 'image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200],
  },
  experimental: {
    optimizePackageImports: ['lucide-react', '@heroicons/react'],
  },
};
```

#### Common Code Anti-Patterns

| Anti-Pattern                         | Impact            | Fix                                           |
| ------------------------------------ | ----------------- | --------------------------------------------- |
| Barrel file imports                  | Bundle bloat      | Import directly from module                   |
| Synchronous `localStorage` in render | Main thread block | Move to `useEffect` or worker                 |
| Unoptimized images                   | LCP, bandwidth    | Use `next/image` or `<picture>`               |
| Inline `<script>` in body            | Render blocking   | Use `async` or `defer`                        |
| CSS `@import` chains                 | CSSOM blocking    | Concatenate or inline critical CSS            |
| Unthrottled scroll listeners         | INP               | Use `passive: true` + `requestAnimationFrame` |
| `document.querySelectorAll` in loops | Layout thrashing  | Cache DOM references                          |

## Audit Report Template

```markdown
# Web Performance Audit Report

**URL:** [target URL]
**Date:** [audit date]
**Tool:** Lighthouse [version] / Chrome DevTools

## Core Web Vitals Summary

| Metric | Score | Rating                      | Target   |
| ------ | ----- | --------------------------- | -------- |
| LCP    | X.Xs  | GOOD/NEEDS IMPROVEMENT/POOR | <= 2.5s  |
| CLS    | X.XX  | GOOD/NEEDS IMPROVEMENT/POOR | <= 0.1   |
| INP    | Xms   | GOOD/NEEDS IMPROVEMENT/POOR | <= 200ms |
| FCP    | X.Xs  | -                           | <= 1.8s  |
| TTFB   | Xms   | -                           | <= 800ms |
| TBT    | Xms   | -                           | <= 200ms |

## Critical Findings

### P0 (Immediate Action Required)

1. [Finding] - [Impact] - [Recommended Fix]

### P1 (Address This Sprint)

1. [Finding] - [Impact] - [Recommended Fix]

### P2 (Address This Quarter)

1. [Finding] - [Impact] - [Recommended Fix]

## Optimization Recommendations (Priority Order)

1. [Recommendation with estimated impact]
2. [Recommendation with estimated impact]
3. [Recommendation with estimated impact]
```

## Anti-Patterns

- Do NOT optimize without measuring first -- always capture baseline metrics
- Do NOT lazy-load above-the-fold content -- it worsens LCP
- Do NOT remove image dimensions to "fix" CLS -- use CSS aspect-ratio instead
- Do NOT bundle all JS into a single file -- use code splitting
- Do NOT ignore mobile performance -- test with CPU/network throttling
- Do NOT use `loading="lazy"` on the LCP image -- it delays loading
- Do NOT serve images without modern formats (AVIF/WebP)

## References

- [web.dev Core Web Vitals](https://web.dev/vitals/)
- [Chrome User Experience Report](https://developer.chrome.com/docs/crux/)
- [Lighthouse Performance Scoring](https://developer.chrome.com/docs/lighthouse/performance/performance-scoring/)
- [Web Almanac Performance Chapter](https://almanac.httparchive.org/en/2024/performance)

## Iron Laws

1. **ALWAYS** measure Core Web Vitals (LCP, INP, CLS) with field data (CrUX) before proposing optimizations
2. **NEVER** optimize based on lab data alone — real user metrics determine actual user experience
3. **ALWAYS** prioritize LCP ≤2.5s, INP ≤200ms, CLS ≤0.1 as the primary performance targets
4. **NEVER** ship a performance fix without a before/after measurement proving improvement
5. **ALWAYS** address critical rendering path issues before layout or paint optimizations

## Anti-Patterns

| Anti-Pattern                            | Why It Fails                                        | Correct Approach                                |
| --------------------------------------- | --------------------------------------------------- | ----------------------------------------------- |
| Optimizing without baseline measurement | Can't prove improvement, may optimize wrong thing   | Measure CWV with Lighthouse and CrUX first      |
| Lab-only metrics (Lighthouse only)      | Doesn't reflect real user network/device conditions | Combine lab data with CrUX field data           |
| Fixing CLS before LCP is addressed      | LCP impacts far more users than CLS                 | Prioritize in order: LCP → INP → CLS            |
| Shipping without before/after metrics   | No evidence of improvement for stakeholders         | Record pre-fix and post-fix CWV scores          |
| Adding polyfills without code splitting | Bloats JS bundle for all users                      | Use dynamic `import()` with target browserslist |

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`
