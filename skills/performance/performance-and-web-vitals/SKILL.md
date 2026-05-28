---
name: performance-and-web-vitals
description: Audit UI performance with Lighthouse and fix Core Web Vitals — LCP, CLS, INP. Fast UI is good UX. Use when optimising page load, fixing layout shift, reducing input delay, improving Lighthouse scores, or reviewing images, fonts, and render-blocking resources.
metadata:
  priority: 8
  docs:
    - "https://web.dev/vitals/"
    - "https://developer.chrome.com/docs/lighthouse/overview/"
  pathPatterns:
    - "**/*.html"
    - "**/*.tsx"
    - "**/*.jsx"
    - "**/*.css"
    - "**/*.scss"
    - "next.config.*"
    - "vite.config.*"
    - "app/**"
    - "pages/**"
  promptSignals:
    phrases:
      - "lighthouse"
      - "performance"
      - "web vitals"
      - "lcp"
      - "cls"
      - "inp"
      - "layout shift"
      - "slow"
      - "page speed"
      - "core web vitals"
retrieval:
  aliases:
    - lighthouse
    - web vitals
    - performance
    - LCP
    - CLS
    - INP
    - page speed
    - core web vitals
  intents:
    - run a lighthouse audit
    - fix layout shift
    - improve lcp
    - optimise images
    - fix slow page
    - improve lighthouse score
  examples:
    - run lighthouse on this page
    - my LCP is too slow
    - fix the layout shift on this page
    - optimise images for performance
    - improve the lighthouse score
---

# Performance and Web Vitals

## Run a Lighthouse Audit

```bash
# CLI audit — outputs JSON and HTML report
npx lighthouse https://example.com --output html --output-path ./lighthouse-report.html

# Headless, useful in CI
npx lighthouse https://example.com --chrome-flags="--headless" --output json --output-path ./report.json

# Audit specific categories only
npx lighthouse https://example.com --only-categories=performance,accessibility,seo
```

Or open Chrome DevTools → Lighthouse tab → Analyse page load.

**Target scores:**
| Category | Target |
|---|---|
| Performance | ≥ 90 |
| Accessibility | 100 |
| Best Practices | ≥ 95 |
| SEO | ≥ 95 |

---

## Core Web Vitals

### LCP — Largest Contentful Paint
*How fast does the main content appear?*

**Target: ≤ 2.5s**

LCP measures when the largest visible element (hero image, heading, video poster) renders. It is the user's perception of "did the page load?"

**Common causes and fixes:**

| Cause | Fix |
|---|---|
| Unoptimised hero image | Use WebP/AVIF, correct size, `fetchpriority="high"` |
| Image not preloaded | `<link rel="preload" as="image" href="hero.webp">` |
| Render-blocking CSS/JS | Defer non-critical JS, inline critical CSS |
| Slow server response | CDN, caching headers, edge delivery |
| Web font blocking render | `font-display: swap` or `optional` |

```html
<!-- Preload LCP image -->
<link rel="preload" as="image" href="hero.webp" fetchpriority="high">

<!-- LCP image: no lazy loading -->
<img src="hero.webp" alt="..." fetchpriority="high" width="1200" height="600">
```

Never use `loading="lazy"` on the LCP image — it delays the most important render.

---

### CLS — Cumulative Layout Shift
*Does content jump around while loading?*

**Target: ≤ 0.1**

CLS measures unexpected layout shifts — content moving after it has rendered. Caused by images without dimensions, late-loading ads, fonts swapping, or dynamic content injected above existing content.

**Common causes and fixes:**

| Cause | Fix |
|---|---|
| Images without width/height | Always set `width` and `height` on `<img>` |
| Web font swap | Use `font-display: optional` or preload fonts |
| Dynamic content above fold | Reserve space with `min-height` on containers |
| Late-loading ads or embeds | Reserve fixed dimensions for ad slots |
| Animations that shift layout | Animate `transform` only, never `top/left/width/height` |

```html
<!-- Always include dimensions -->
<img src="product.jpg" width="400" height="300" alt="...">
```

```css
/* Reserve space for dynamic content */
.ad-slot { min-height: 250px; }

/* Animate transform, not layout properties */
.slide-in { transform: translateY(0); transition: transform 300ms; }
```

---

### INP — Interaction to Next Paint
*How quickly does the page respond to user input?*

**Target: ≤ 200ms**

INP measures the delay between a user interaction (click, tap, keyboard) and the next visual update. High INP makes the UI feel sluggish or frozen.

**Common causes and fixes:**

| Cause | Fix |
|---|---|
| Heavy JS on main thread | Break into smaller tasks, use `requestIdleCallback` |
| Large event handlers | Debounce/throttle scroll and resize handlers |
| Synchronous DOM updates | Batch DOM writes with `requestAnimationFrame` |
| Third-party scripts blocking | Load third-party scripts with `async` or `defer` |
| React re-renders | Memoize with `useMemo`, `useCallback`, `React.memo` |

---

## Images

Images are the single biggest performance lever on most pages.

```html
<!-- Modern formats with fallback -->
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" width="800" height="600" alt="..." loading="lazy">
</picture>

<!-- Responsive images -->
<img
  srcset="image-400.webp 400w, image-800.webp 800w, image-1200.webp 1200w"
  sizes="(max-width: 600px) 100vw, 50vw"
  src="image-800.webp"
  alt="..."
  width="800"
  height="600"
  loading="lazy"
>
```

**Rules:**
- Always set `width` and `height` — prevents CLS
- Use `loading="lazy"` below the fold, never on LCP image
- Serve WebP or AVIF — typically 30–50% smaller than JPEG
- Size images to their display size — do not serve 2000px image for a 400px slot
- Use a CDN with automatic format conversion where possible

---

## Fonts

Web fonts block rendering if not handled correctly.

```html
<!-- Preconnect to font origin -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- Preload critical font file -->
<link rel="preload" href="/fonts/brand.woff2" as="font" type="font/woff2" crossorigin>
```

```css
@font-face {
  font-family: 'Brand';
  src: url('/fonts/brand.woff2') format('woff2');
  font-display: swap;     /* show fallback immediately, swap when loaded */
  /* font-display: optional; — never swap, use fallback if not cached */
}
```

- `font-display: swap` — good for headings, acceptable CLS
- `font-display: optional` — zero CLS, font only used if cached (best for body text)
- Subset fonts to the characters actually used — reduces file size by 60–80%

---

## JavaScript

```html
<!-- Defer non-critical scripts -->
<script src="analytics.js" defer></script>
<script src="chat-widget.js" async></script>

<!-- Module scripts are deferred by default -->
<script type="module" src="app.js"></script>
```

- `defer`: executes after HTML parsed, in order — use for most scripts
- `async`: executes as soon as downloaded, out of order — use for independent scripts (analytics)
- Never block the main thread with synchronous `<script>` in `<head>`

---

## Lighthouse CI (automated audits)

Run Lighthouse in CI to catch regressions before deployment.

```bash
# Install
npm install -g @lhci/cli

# Run
lhci autorun --upload.target=temporary-public-storage
```

```yaml
# .lighthouserc.json
{
  "ci": {
    "assert": {
      "assertions": {
        "categories:performance": ["warn", { "minScore": 0.9 }],
        "categories:accessibility": ["error", { "minScore": 1.0 }],
        "categories:seo": ["warn", { "minScore": 0.95 }]
      }
    }
  }
}
```

---

## Review Checklist

- [ ] Lighthouse performance score ≥ 90
- [ ] Lighthouse accessibility score = 100
- [ ] LCP ≤ 2.5s — LCP image preloaded, no `loading="lazy"` on it
- [ ] CLS ≤ 0.1 — all images have `width` and `height`, no layout-shifting animations
- [ ] INP ≤ 200ms — no heavy synchronous JS on main thread
- [ ] Images served as WebP or AVIF with correct dimensions
- [ ] `loading="lazy"` on all below-fold images
- [ ] Web fonts use `font-display: swap` or `optional`
- [ ] Non-critical JS loaded with `defer` or `async`
- [ ] Lighthouse CI configured to catch regressions in deployment pipeline
