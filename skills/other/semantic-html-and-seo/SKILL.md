---
name: semantic-html-and-seo
description: Semantic HTML5, SEO fundamentals, alt texts, progressive enhancement, SPA considerations, device capability detection, and user context awareness. Good HTML is the foundation of accessibility, SEO, and resilient UI. Use when building any web UI, reviewing markup quality, or optimising for search and accessibility.
metadata:
  priority: 8
  pathPatterns:
    - "**/*.html"
    - "**/*.tsx"
    - "**/*.jsx"
    - "**/*.vue"
    - "**/*.svelte"
    - "app/**"
    - "pages/**"
    - "src/**"
  promptSignals:
    phrases:
      - "seo"
      - "semantic html"
      - "alt text"
      - "meta tags"
      - "progressive enhancement"
      - "spa"
      - "open graph"
      - "structured data"
      - "html5"
retrieval:
  aliases:
    - seo
    - semantic html
    - alt text
    - progressive enhancement
    - html5 best practices
    - meta tags
    - open graph
    - structured data
    - spa seo
  intents:
    - improve seo
    - add alt texts
    - write semantic html
    - optimise for search engines
    - add open graph tags
    - make spa crawlable
  examples:
    - add proper meta tags to this page
    - write semantic html for this component
    - how do I make this SPA SEO friendly
    - add alt texts to all images
---

# Semantic HTML and SEO

Good HTML is not just markup — it is the contract between your content, search engines, assistive technologies, and the browser. Semantic HTML, correct metadata, and progressive enhancement make UI resilient, findable, and accessible by default.

---

## Semantic HTML5

Use the element that describes the content's meaning, not just its appearance.

### Document structure
```html
<header>       <!-- site header, logo, primary nav -->
<nav>          <!-- navigation links -->
<main>         <!-- primary page content, one per page -->
<article>      <!-- self-contained content: blog post, product card, news item -->
<section>      <!-- thematic grouping with a heading -->
<aside>        <!-- tangentially related content: sidebar, callout -->
<footer>       <!-- site footer, secondary links, copyright -->
```

### Headings
One `<h1>` per page — the primary topic. Headings form an outline: do not skip levels (`h1` → `h3` without `h2`).

```html
<h1>Product name</h1>
  <h2>Features</h2>
    <h3>Feature detail</h3>
  <h2>Pricing</h2>
```

### Interactive elements
```html
<button>   <!-- clickable action, submits or triggers JS -->
<a href>   <!-- navigation to a URL -->
<input>    <!-- user data entry -->
<select>   <!-- option selection -->
<details> / <summary>  <!-- native disclosure/accordion -->
```

Never use `<div>` or `<span>` as interactive elements without full ARIA annotation — and even then, prefer the native element.

---

## Images and Alt Text

Every `<img>` needs an `alt` attribute. What goes in it depends on context.

| Image type | Alt text |
|---|---|
| Informative (product photo, chart) | Describe content: `alt="Red leather sofa, three-seater"` |
| Functional (icon button, logo link) | Describe function: `alt="Go to homepage"` |
| Decorative | Empty: `alt=""` — screen readers skip it |
| Complex (chart, diagram) | Short alt + longer description nearby or in `<figcaption>` |

```html
<!-- Informative -->
<img src="sofa.jpg" alt="Red leather sofa, three-seater">

<!-- Decorative -->
<img src="divider.svg" alt="">

<!-- With caption -->
<figure>
  <img src="chart.png" alt="Bar chart showing revenue growth Q1–Q4 2025">
  <figcaption>Revenue grew 42% year-on-year in Q4 2025.</figcaption>
</figure>
```

---

## SEO Fundamentals

### Title and description
```html
<title>Product Name — Short descriptor | Brand</title>
<meta name="description" content="One or two sentences. What this page is, who it is for, what they will find.">
```

- Title: 50–60 characters. Most important keyword first.
- Description: 120–160 characters. Shown in search results — write for the human, not the algorithm.

### Canonical URL
```html
<link rel="canonical" href="https://example.com/the-definitive-url">
```

Prevents duplicate content penalties when the same page is accessible via multiple URLs.

### Open Graph (social sharing)
```html
<meta property="og:title" content="Page title">
<meta property="og:description" content="Page description">
<meta property="og:image" content="https://example.com/og-image.jpg">
<meta property="og:url" content="https://example.com/page">
<meta property="og:type" content="website">

<!-- Twitter/X -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Page title">
<meta name="twitter:image" content="https://example.com/og-image.jpg">
```

OG image: 1200×630px. Appears when the URL is shared on Slack, LinkedIn, Twitter, iMessage.

### Structured Data (JSON-LD)
Machine-readable content enables rich search results.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "description": "Product description",
  "image": "https://example.com/product.jpg",
  "offers": {
    "@type": "Offer",
    "price": "49.00",
    "priceCurrency": "EUR"
  }
}
</script>
```

Common types: `Product`, `Article`, `BreadcrumbList`, `FAQPage`, `Organization`, `SiteLinksSearchBox`.

---

## Progressive Enhancement

Build in layers. The core content and function must work without JavaScript. Enhance with CSS. Enhance further with JS.

```
Layer 1: HTML — content is readable, links work, forms submit
Layer 2: CSS  — layout, typography, visual design
Layer 3: JS   — interactivity, animations, dynamic content
```

**In practice:**
- Forms must submit via native `<form action>` without JS — JS can intercept and enhance with fetch
- Navigation links must be real `<a href>` — JS can add transitions
- Content must be in the HTML — JS can enhance with lazy-load or personalisation
- Images must have `src` — JS can add lazy loading via `loading="lazy"` (now native)

---

## SPA Considerations

Single-page applications break browser defaults that SEO and accessibility depend on. Fix them explicitly.

### Server-side rendering or static generation
Client-rendered HTML is not reliably indexed by search engines. Use SSR (Next.js, Nuxt, SvelteKit) or static generation for any content that needs to be found.

### Title and meta updates
Update `document.title` and meta tags on every route change. Use the framework's `<Head>` component or equivalent.

### Focus management
On route change, move focus to the new page's `<h1>` or `<main>` — screen readers do not detect SPA navigation automatically.

```js
// After route change
document.querySelector('h1')?.focus();
```

### Scroll restoration
Restore scroll position to top on navigation, or to the saved position on back navigation. Browser default scroll restoration is disabled in SPAs.

### History API
Use `pushState` / `replaceState` so back/forward navigation and bookmarking work correctly.

---

## Device Capabilities and User Context

Design and code should adapt to what the device and user can actually do.

### Input method detection
```css
@media (hover: hover) {
  /* hover states — mouse or trackpad */
  .btn:hover { background: var(--color-primary-hover); }
}

@media (hover: none) {
  /* touch device — no hover, larger targets */
  .btn { min-height: 44px; }
}
```

### Pointer precision
```css
@media (pointer: coarse) {
  /* fat-finger touch — increase target sizes */
  .interactive { min-height: 44px; min-width: 44px; }
}

@media (pointer: fine) {
  /* mouse — precise, can use smaller targets */
}
```

### Network conditions
```html
<!-- Lazy load images below the fold -->
<img src="product.jpg" loading="lazy" alt="...">

<!-- Serve modern formats with fallback -->
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="...">
</picture>
```

### User preferences
```css
@media (prefers-reduced-motion: reduce) { /* disable animations */ }
@media (prefers-color-scheme: dark)     { /* dark mode tokens */ }
@media (prefers-contrast: more)         { /* increase contrast */ }
@media (forced-colors: active)          { /* Windows high contrast mode */ }
```

---

## Review Checklist

- [ ] One `<h1>` per page, headings form a logical outline
- [ ] Semantic elements used: `<main>`, `<nav>`, `<header>`, `<footer>`, `<article>`, `<section>`
- [ ] Every `<img>` has a meaningful `alt` or `alt=""` for decorative images
- [ ] `<title>` is unique per page, 50–60 characters, keyword-first
- [ ] `<meta name="description">` present and 120–160 characters
- [ ] Open Graph tags present on all shareable pages
- [ ] `<link rel="canonical">` on pages accessible via multiple URLs
- [ ] Structured data (JSON-LD) on product, article, and FAQ pages
- [ ] Forms work without JavaScript
- [ ] SPA updates `document.title` and meta tags on route change
- [ ] SPA moves focus on route change
- [ ] Hover states scoped to `@media (hover: hover)`
- [ ] Touch targets ≥ 44px on `@media (pointer: coarse)`
- [ ] Images use `loading="lazy"` below the fold
- [ ] `prefers-reduced-motion` respected
