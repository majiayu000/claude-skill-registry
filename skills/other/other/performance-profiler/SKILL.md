---
name: profiling-performance
description: Runs performance audits and suggests optimizations using Lighthouse and Web Vitals. Use when the user asks about performance, page speed, Core Web Vitals, Lighthouse scores, or wants to optimize rendering and execution.
---

# Performance Profiler Assistant

## When to use this skill

- User asks to run a performance audit
- User mentions Lighthouse or Web Vitals
- User wants to improve page load speed
- User asks about LCP, FID, CLS, or INP
- User wants to profile CPU or memory usage
- User asks to optimize rendering performance

## Workflow

- [ ] Identify target URL or build to audit
- [ ] Run Lighthouse audit
- [ ] Collect Core Web Vitals metrics
- [ ] Analyze bundle size
- [ ] Profile runtime performance if needed
- [ ] Generate optimization recommendations
- [ ] Prioritize fixes by impact

## Instructions

### Step 1: Identify Audit Target

For deployed site:

```bash
# URL to audit
TARGET_URL="https://example.com"
```

For local development:

```bash
# Ensure dev server is running
npm run dev
TARGET_URL="http://localhost:3000"
```

For static build analysis:

```bash
npm run build
npx serve dist  # or out, build folder
```

### Step 2: Run Lighthouse Audit

**CLI audit:**

```bash
npx lighthouse $TARGET_URL --output=json --output=html --output-path=./lighthouse-report
```

**With specific categories:**

```bash
npx lighthouse $TARGET_URL --only-categories=performance,accessibility,best-practices,seo --output=json
```

**Mobile emulation (default):**

```bash
npx lighthouse $TARGET_URL --preset=desktop  # For desktop metrics
```

**Programmatic in Node.js:**

```javascript
import lighthouse from "lighthouse";
import * as chromeLauncher from "chrome-launcher";

const chrome = await chromeLauncher.launch({ chromeFlags: ["--headless"] });
const result = await lighthouse(url, { port: chrome.port });
console.log(result.lhr.categories.performance.score * 100);
await chrome.kill();
```

### Step 3: Interpret Core Web Vitals

| Metric                          | Good   | Needs Improvement | Poor   |
| ------------------------------- | ------ | ----------------- | ------ |
| LCP (Largest Contentful Paint)  | ≤2.5s  | 2.5s–4s           | >4s    |
| INP (Interaction to Next Paint) | ≤200ms | 200ms–500ms       | >500ms |
| CLS (Cumulative Layout Shift)   | ≤0.1   | 0.1–0.25          | >0.25  |
| FCP (First Contentful Paint)    | ≤1.8s  | 1.8s–3s           | >3s    |
| TTFB (Time to First Byte)       | ≤800ms | 800ms–1.8s        | >1.8s  |

### Step 4: Analyze Bundle Size

**Next.js:**

```bash
ANALYZE=true npm run build
# Or add to next.config.js:
# const withBundleAnalyzer = require('@next/bundle-analyzer')({ enabled: process.env.ANALYZE === 'true' });
```

**Vite/Nuxt:**

```bash
npx vite-bundle-visualizer
# Or
npx nuxi analyze
```

**Generic webpack:**

```bash
npx webpack-bundle-analyzer stats.json
```

**Source map explorer:**

```bash
npx source-map-explorer dist/**/*.js
```

### Step 5: Profile Runtime Performance

**Chrome DevTools Performance tab:**

1. Open DevTools → Performance
2. Click Record
3. Perform user actions
4. Stop recording
5. Analyze flame chart for long tasks

**Measure in code:**

```typescript
// Performance marks
performance.mark("start-operation");
await heavyOperation();
performance.mark("end-operation");
performance.measure("operation", "start-operation", "end-operation");

const measures = performance.getEntriesByName("operation");
console.log(`Operation took ${measures[0].duration}ms`);
```

**React Profiler:**

```tsx
import { Profiler } from "react";

<Profiler
  id="Component"
  onRender={(id, phase, actualDuration) => {
    console.log(`${id} ${phase} render: ${actualDuration}ms`);
  }}
>
  <Component />
</Profiler>;
```

### Step 6: Generate Recommendations

**Report template:**

```markdown
## Performance Audit Report

**URL**: https://example.com
**Date**: 2026-01-18
**Device**: Mobile (Moto G Power)

### Scores

| Category       | Score |
| -------------- | ----- |
| Performance    | 72    |
| Accessibility  | 95    |
| Best Practices | 92    |
| SEO            | 100   |

### Core Web Vitals

| Metric | Value | Status               |
| ------ | ----- | -------------------- |
| LCP    | 3.2s  | ⚠️ Needs Improvement |
| INP    | 150ms | ✅ Good              |
| CLS    | 0.05  | ✅ Good              |

### Top Issues

#### 1. Large Contentful Paint (3.2s)

**Impact**: High
**Cause**: Hero image not optimized
**Fix**:

- Add `priority` to Next.js Image
- Use responsive srcset
- Preload LCP image

#### 2. Render-blocking resources

**Impact**: Medium
**Cause**: 3 CSS files blocking render
**Fix**:

- Inline critical CSS
- Defer non-critical styles
- Use `media` attribute for print styles

#### 3. Unused JavaScript (245KB)

**Impact**: Medium
**Cause**: Large vendor bundle
**Fix**:

- Enable tree shaking
- Dynamic import heavy components
- Remove unused dependencies
```

## Common Optimizations

### Images

```tsx
// Next.js - Use Image component with priority for LCP
import Image from "next/image";

<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority // Preloads LCP image
  sizes="(max-width: 768px) 100vw, 1200px"
/>;
```

### Code Splitting

```tsx
// React - Lazy load heavy components
import { lazy, Suspense } from "react";

const HeavyChart = lazy(() => import("./HeavyChart"));

<Suspense fallback={<Loading />}>
  <HeavyChart />
</Suspense>;
```

```typescript
// Dynamic import for conditional features
const module = await import("./heavy-module");
```

### Font Optimization

```tsx
// Next.js - Use next/font
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"], display: "swap" });
```

```css
/* Self-hosted with font-display */
@font-face {
  font-family: "Custom";
  src: url("/fonts/custom.woff2") format("woff2");
  font-display: swap;
}
```

### Preloading Critical Resources

```html
<!-- Preload LCP image -->
<link rel="preload" as="image" href="/hero.webp" />

<!-- Preconnect to CDN -->
<link rel="preconnect" href="https://cdn.example.com" />

<!-- DNS prefetch for third parties -->
<link rel="dns-prefetch" href="https://analytics.example.com" />
```

### Reducing Layout Shift

```css
/* Reserve space for images */
img {
  aspect-ratio: 16 / 9;
  width: 100%;
  height: auto;
}

/* Reserve space for ads/embeds */
.ad-slot {
  min-height: 250px;
}
```

```tsx
// Always provide width/height
<Image width={800} height={450} ... />
```

### Caching

```javascript
// next.config.js - Cache static assets
module.exports = {
  async headers() {
    return [
      {
        source: "/_next/static/:path*",
        headers: [
          {
            key: "Cache-Control",
            value: "public, max-age=31536000, immutable",
          },
        ],
      },
    ];
  },
};
```

## Validation

Before completing:

- [ ] Lighthouse performance score ≥90
- [ ] All Core Web Vitals in "Good" range
- [ ] No render-blocking resources
- [ ] Bundle size within budget
- [ ] No layout shifts from loading content

## Error Handling

- **Lighthouse fails to run**: Ensure Chrome is installed and no conflicting flags.
- **Metrics vary wildly**: Run multiple times and average; use `--throttling.cpuSlowdownMultiplier`.
- **Can't reproduce field data**: Lab data differs from real users; use CrUX for field data.
- **Build analysis fails**: Ensure source maps are generated (`devtool: 'source-map'`).

## Resources

- [web.dev Performance](https://web.dev/performance/)
- [Lighthouse Documentation](https://developer.chrome.com/docs/lighthouse/)
- [Core Web Vitals](https://web.dev/vitals/)
- [Chrome UX Report](https://developer.chrome.com/docs/crux/)
