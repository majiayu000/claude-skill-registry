---
name: html-semantic-engineering
description: 30 pragmatic rules for production HTML covering semantic markup, accessibility (WCAG 2.1 AA), performance optimization, forms, and security. Use when writing HTML, building page structures, creating forms, implementing accessibility, or optimizing for SEO and Core Web Vitals.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebFetch, WebSearch
---

# HTML Semantic Engineering

30 battle-tested principles for production HTML. Semantic correctness first, then accessibility, then performance.

## Relationship with Other Skills

- **`web-components-architecture`**: Component lifecycle and Shadow DOM patterns
- **`javascript-pragmatic-rules`**: JavaScript behavior inside components
- **`utopia-fluid-scales`**: Typography (`--step-*`) and spacing (`--space-*`) tokens
- **`utopia-grid-layout`**: Grid utilities (`.u-container`, `.u-grid`, `--grid-gutter`)
- **`utopia-container-queries`**: Container context required for `cqi` fluid units

**Example:** A `<product-card>` component should:
- Use this skill for semantic structure (article, heading hierarchy, img alt)
- Use `web-components-architecture` for Shadow DOM encapsulation
- Use `utopia-fluid-scales` for typography (`--step-2`) and spacing (`--space-m`)
- Use `javascript-pragmatic-rules` for async data fetching

## Design System Integration

This project uses Utopia's fluid scales with `cqi` (container query inline) units. **Never hardcode pixel values for typography or spacing.** Use design tokens:

```css
/* Typography - see utopia-fluid-scales */
font-size: var(--step-0);   /* Body text */
font-size: var(--step-3);   /* H3 equivalent */

/* Spacing - see utopia-fluid-scales */
padding: var(--space-m);
gap: var(--space-s-m);      /* Fluid pair */

/* Grid - see utopia-grid-layout */
gap: var(--grid-gutter);
max-width: var(--grid-max-width);
```

**Container requirement:** The `cqi` units require `container-type: inline-size` on a parent element. This is set on `html` in `css/styles/index.css`.

---

## Semantic Structure

### Rule 1: Never Skip Heading Levels

Heading hierarchy defines document outline. Screen readers use headings for navigation.

```html
<!-- ✅ Correct hierarchy -->
<article>
  <h1>Page Title</h1>
  <section>
    <h2>Section Title</h2>
    <h3>Subsection Title</h3>
  </section>
</article>

<!-- ❌ Skipped h2 -->
<article>
  <h1>Page Title</h1>
  <h3>Subsection Title</h3>
</article>
```

### Rule 2: Use Semantic Elements Over Divs

Semantic elements convey meaning to browsers, screen readers, and search engines.

```html
<!-- ✅ Semantic structure -->
<header>
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/" aria-current="page">Home</a></li>
      <li><a href="/about">About</a></li>
    </ul>
  </nav>
</header>

<main>
  <article>
    <header>
      <h1>Article Title</h1>
      <time datetime="2024-01-15">January 15, 2024</time>
    </header>
    <p>Content...</p>
    <aside>Related sidebar content</aside>
  </article>
</main>

<footer>
  <nav aria-label="Footer navigation">...</nav>
</footer>

<!-- ❌ Generic containers -->
<div class="header">
  <div class="nav">...</div>
</div>
```

### Rule 3: Landmark Regions for Navigation

Screen reader users navigate by landmarks. Every page needs clear regions.

```html
<body>
  <!-- role="banner" is implicit for header as direct child of body -->
  <header>...</header>

  <!-- role="navigation" is implicit for nav -->
  <nav aria-label="Main">...</nav>

  <!-- role="main" is implicit -->
  <main id="main-content">...</main>

  <!-- role="complementary" is implicit for aside -->
  <aside aria-label="Related content">...</aside>

  <!-- role="contentinfo" is implicit for footer as direct child of body -->
  <footer>...</footer>
</body>
```

---

## Accessibility (WCAG 2.1 AA)

### Rule 4: Always Include Alt Text

Images need descriptions for screen readers. Decorative images use empty alt.

```html
<!-- ✅ Informative image -->
<img src="chart.png" alt="Q4 sales increased 23% compared to Q3" width="600" height="400">

<!-- ✅ Decorative image -->
<img src="decorative-border.png" alt="" role="presentation">

<!-- ✅ Complex image with extended description -->
<figure>
  <img src="flowchart.png" alt="User registration process flowchart" aria-describedby="flowchart-desc">
  <figcaption id="flowchart-desc">
    The process starts with email entry, followed by verification, profile setup, and confirmation.
  </figcaption>
</figure>

<!-- ❌ Missing alt -->
<img src="important-graph.png">
```

### Rule 5: Implement Skip Links

Keyboard users need to bypass repetitive navigation.

```html
<body>
  <a href="#main-content" class="skip-link">Skip to main content</a>
  <a href="#navigation" class="skip-link">Skip to navigation</a>

  <header>...</header>
  <nav id="navigation">...</nav>
  <main id="main-content">...</main>
</body>

<style>
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  padding: var(--space-2xs) var(--space-s);
  background: var(--color-background-inverse, #000);
  color: var(--color-text-inverse, #fff);
  z-index: 100;
}
.skip-link:focus {
  top: 0;
}
</style>
```

### Rule 6: Associate Labels with Inputs

Every form control needs an accessible name.

```html
<!-- ✅ Explicit label association -->
<label for="email">Email Address</label>
<input type="email" id="email" name="email" required>

<!-- ✅ Implicit label wrapping -->
<label>
  <input type="checkbox" name="subscribe">
  Subscribe to newsletter
</label>

<!-- ✅ aria-label for icon buttons -->
<button aria-label="Close dialog">
  <svg aria-hidden="true">...</svg>
</button>

<!-- ❌ Missing label -->
<input type="text" placeholder="Enter name">
```

### Rule 7: Use ARIA Correctly

ARIA supplements HTML semantics—it doesn't replace them.

```html
<!-- ✅ ARIA for custom widgets -->
<div role="tablist" aria-label="Account settings">
  <button role="tab" aria-selected="true" aria-controls="panel-1" id="tab-1">Profile</button>
  <button role="tab" aria-selected="false" aria-controls="panel-2" id="tab-2">Security</button>
</div>
<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">...</div>
<div role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>...</div>

<!-- ✅ Live regions for dynamic content -->
<div aria-live="polite" aria-atomic="true" id="status">
  <!-- Updated by JavaScript -->
</div>

<!-- ❌ Redundant ARIA -->
<button role="button">Submit</button>
<nav role="navigation">...</nav>
```

### Rule 8: Keyboard Navigation

All interactive elements must be keyboard accessible.

```html
<!-- ✅ Native focus management -->
<button>Focusable by default</button>
<a href="/page">Focusable by default</a>
<input type="text">

<!-- ✅ Custom focusable element -->
<div role="button" tabindex="0"
     onkeydown="if(event.key==='Enter'||event.key===' ')this.click()">
  Custom Button
</div>

<!-- ✅ Focus trap in modal -->
<dialog>
  <h2>Dialog Title</h2>
  <button>First focusable</button>
  <button>Last focusable</button>
</dialog>

<!-- ❌ Non-interactive element made clickable without keyboard support -->
<div onclick="doSomething()">Click me</div>
```

---

## Forms & Validation

### Rule 9: Use Appropriate Input Types

Input types provide semantic meaning, validation, and mobile keyboards.

```html
<input type="email" autocomplete="email">
<input type="tel" autocomplete="tel">
<input type="url" autocomplete="url">
<input type="date" min="2024-01-01" max="2024-12-31">
<input type="number" min="0" max="100" step="1">
<input type="search" autocomplete="off">
<input type="password" autocomplete="new-password" minlength="8">
```

### Rule 10: HTML5 Validation with Accessible Errors

Use native validation with clear error messaging.

```html
<form novalidate>
  <div class="form-group">
    <label for="username">Username <abbr title="required">*</abbr></label>
    <input
      type="text"
      id="username"
      name="username"
      required
      pattern="[a-zA-Z0-9_]{3,20}"
      minlength="3"
      maxlength="20"
      aria-describedby="username-help username-error"
    >
    <div id="username-help" class="help-text">3-20 characters, letters, numbers, underscores</div>
    <div id="username-error" class="error" role="alert" aria-live="polite"></div>
  </div>

  <button type="submit">Create Account</button>
</form>
```

### Rule 11: Group Related Form Controls

Fieldsets and legends improve form comprehension.

```html
<fieldset>
  <legend>Shipping Address</legend>
  <label for="street">Street</label>
  <input type="text" id="street" autocomplete="street-address">

  <label for="city">City</label>
  <input type="text" id="city" autocomplete="address-level2">
</fieldset>

<fieldset>
  <legend>Payment Method</legend>
  <label><input type="radio" name="payment" value="card"> Credit Card</label>
  <label><input type="radio" name="payment" value="paypal"> PayPal</label>
</fieldset>
```

### Rule 12: Autocomplete for User Data

Autocomplete speeds form filling and improves security.

```html
<input type="text" name="name" autocomplete="name">
<input type="email" name="email" autocomplete="email">
<input type="tel" name="phone" autocomplete="tel">
<input type="text" name="address" autocomplete="street-address">
<input type="text" name="city" autocomplete="address-level2">
<input type="text" name="state" autocomplete="address-level1">
<input type="text" name="zip" autocomplete="postal-code">
<input type="text" name="country" autocomplete="country-name">
<input type="text" name="cc-number" autocomplete="cc-number">
<input type="password" name="password" autocomplete="new-password">
<input type="password" name="current-password" autocomplete="current-password">
```

---

## Performance

### Rule 13: Lazy Load Below-Fold Images

Images below the viewport should load on demand.

```html
<!-- ✅ Lazy load below-fold images -->
<img src="below-fold.jpg" loading="lazy" alt="..." width="800" height="600">

<!-- ✅ Eager load above-fold images -->
<img src="hero.jpg" loading="eager" fetchpriority="high" alt="..." width="1200" height="600">

<!-- ✅ Responsive images with lazy loading -->
<img
  srcset="small.jpg 400w, medium.jpg 800w, large.jpg 1200w"
  sizes="(max-width: 600px) 100vw, 50vw"
  src="medium.jpg"
  loading="lazy"
  alt="..."
  width="800"
  height="600"
>
```

### Rule 14: Resource Hints for Critical Assets

Preconnect, preload, and prefetch optimize loading.

```html
<head>
  <!-- DNS prefetch for third-party domains -->
  <link rel="dns-prefetch" href="//fonts.googleapis.com">
  <link rel="dns-prefetch" href="//api.example.com">

  <!-- Preconnect for critical third-party -->
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

  <!-- Preload critical assets -->
  <link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/css/critical.css" as="style">

  <!-- Prefetch non-critical resources -->
  <link rel="prefetch" href="/js/non-critical.js">
</head>
```

### Rule 15: Specify Image Dimensions

Width and height prevent layout shift (CLS).

```html
<!-- ✅ Explicit dimensions prevent CLS -->
<img src="photo.jpg" width="800" height="600" alt="...">

<!-- ✅ Aspect ratio maintained with CSS (no inline styles in production) -->
<img src="photo.jpg" width="800" height="600" alt="..." class="img-fluid">

<!-- ✅ Picture element with dimensions -->
<picture>
  <source media="(min-width: 800px)" srcset="large.webp" width="1200" height="800">
  <img src="small.jpg" width="400" height="300" alt="...">
</picture>
```

### Rule 16: Defer Non-Critical Scripts

Blocking scripts delay rendering.

```html
<!-- ✅ Defer non-critical scripts -->
<script src="/js/main.js" defer></script>

<!-- ✅ Async for independent scripts -->
<script src="/js/analytics.js" async></script>

<!-- ✅ Module scripts are deferred by default -->
<script type="module" src="/js/app.js"></script>

<!-- ✅ Legacy fallback -->
<script nomodule src="/js/legacy.js" defer></script>

<!-- ❌ Blocking script in head -->
<head>
  <script src="/js/heavy.js"></script>
</head>
```

### Rule 16a: Modulepreload for Critical Components

Use `modulepreload` for above-the-fold web components to prevent FOUC (Flash of Unstyled Content).

```html
<head>
  <!-- Styles first -->
  <link rel="stylesheet" href="/css/styles/index.css">

  <!-- Modulepreload critical above-the-fold components -->
  <link rel="modulepreload" href="/js/components/site-nav.js">
  <link rel="modulepreload" href="/js/components/nav-link-item.js">
  <link rel="modulepreload" href="/js/components/page-transition.js">

  <!-- Import maps (after modulepreload) -->
  <script type="importmap">
    {
      "imports": {
        "animejs": "/node_modules/animejs/dist/modules/index.js"
      }
    }
  </script>
</head>
```

**Why modulepreload?**
- Browser starts downloading modules in parallel with HTML parsing
- Reduces time between HTML render and component definition
- Prevents unstyled custom element flash
- Works only with ES modules (`type="module"` scripts)

**When to use:**
- Navigation components (always visible)
- Hero/above-the-fold components
- Critical interactive elements

**When NOT to use:**
- Below-the-fold components (let browser lazy-load)
- Large dependency trees (can block other resources)

### Rule 16b: FOUC Prevention CSS

Custom elements need CSS rules to prevent Flash of Unstyled Content:

```css
/* Hide custom elements until JavaScript defines them */
site-nav:not(:defined),
nav-link-item:not(:defined) {
  opacity: 0;
}

/* Reserve layout space for fixed elements to prevent CLS */
site-nav:not(:defined) {
  display: block;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  min-height: 56px;
  background: var(--theme-surface);
}
```

See `web-components` skill for complete FOUC prevention patterns.

---

## SEO & Metadata

### Rule 17: Essential Meta Tags

Every page needs proper metadata.

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Page Title - Site Name</title>
  <meta name="description" content="150-160 character description">
  <link rel="canonical" href="https://example.com/page">

  <!-- Open Graph -->
  <meta property="og:title" content="Page Title">
  <meta property="og:description" content="Page description">
  <meta property="og:image" content="https://example.com/og-image.jpg">
  <meta property="og:url" content="https://example.com/page">
  <meta property="og:type" content="website">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Page Title">
  <meta name="twitter:description" content="Page description">
  <meta name="twitter:image" content="https://example.com/twitter-image.jpg">
</head>
```

### Rule 18: Structured Data

Schema.org markup improves search result appearance.

```html
<!-- Article Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "author": { "@type": "Person", "name": "Author Name" },
  "datePublished": "2024-01-15",
  "image": "https://example.com/image.jpg"
}
</script>

<!-- Product Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "offers": {
    "@type": "Offer",
    "price": "29.99",
    "priceCurrency": "USD"
  }
}
</script>
```

---

## Security

### Rule 19: Content Security Policy

CSP prevents XSS attacks.

```html
<meta http-equiv="Content-Security-Policy" content="
  default-src 'self';
  script-src 'self';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  font-src 'self';
  frame-ancestors 'none';
">
```

### Rule 20: Secure External Resources

Use SRI and crossorigin for external scripts.

```html
<script
  src="https://cdn.example.com/lib.js"
  integrity="sha384-abc123..."
  crossorigin="anonymous"
></script>

<link
  rel="stylesheet"
  href="https://cdn.example.com/style.css"
  integrity="sha384-def456..."
  crossorigin="anonymous"
>
```

### Rule 21: CSRF Protection in Forms

Include CSRF tokens in form submissions.

```html
<form action="/submit" method="POST">
  <input type="hidden" name="csrf_token" value="{{csrf_token}}">
  <!-- form fields -->
  <button type="submit">Submit</button>
</form>
```

---

## Tables

### Rule 22: Accessible Data Tables

Tables need proper headers and captions.

```html
<table>
  <caption>Q4 2024 Sales by Region</caption>
  <thead>
    <tr>
      <th scope="col">Region</th>
      <th scope="col">Sales</th>
      <th scope="col">Growth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">North</th>
      <td>$50,000</td>
      <td>+15%</td>
    </tr>
    <tr>
      <th scope="row">South</th>
      <td>$42,000</td>
      <td>+8%</td>
    </tr>
  </tbody>
</table>
```

---

## Interactive Components

### Rule 23: Accessible Modal Dialogs

Modals need focus trapping and proper ARIA.

```html
<button aria-haspopup="dialog" aria-controls="dialog-1">Open Dialog</button>

<dialog id="dialog-1" aria-labelledby="dialog-title" aria-describedby="dialog-desc">
  <h2 id="dialog-title">Confirm Action</h2>
  <p id="dialog-desc">Are you sure you want to proceed?</p>
  <button autofocus>Cancel</button>
  <button>Confirm</button>
</dialog>
```

### Rule 24: Expandable Content

Use details/summary or ARIA for collapsible content.

```html
<!-- ✅ Native disclosure widget -->
<details>
  <summary>Show more information</summary>
  <p>Additional content revealed when expanded.</p>
</details>

<!-- ✅ Custom accordion with ARIA -->
<h3>
  <button aria-expanded="false" aria-controls="panel-1">
    FAQ Question
  </button>
</h3>
<div id="panel-1" hidden>
  <p>FAQ Answer content.</p>
</div>
```

---

## Progressive Enhancement

### Rule 25: Design for No JavaScript

Core functionality must work without JavaScript.

```html
<!-- ✅ Form works without JS -->
<form action="/search" method="GET">
  <input type="search" name="q" required>
  <button type="submit">Search</button>
</form>

<!-- ✅ Navigation works without JS -->
<nav>
  <a href="/page-1">Page 1</a>
  <a href="/page-2">Page 2</a>
</nav>

<!-- ✅ CSS-only toggle -->
<input type="checkbox" id="menu-toggle" hidden>
<label for="menu-toggle">Menu</label>
<nav><!-- Toggle visibility with CSS --></nav>

<!-- ✅ Noscript fallback -->
<noscript>
  <p>JavaScript is required for full functionality.</p>
</noscript>
```

---

## Document Template

### Rule 26: Complete HTML5 Boilerplate

This project's entry point is `css/styles/index.css` which imports all design tokens.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">

  <title>Page Title - Site Name</title>
  <meta name="description" content="Page description">
  <link rel="canonical" href="https://example.com/page">

  <!-- Preconnect for fonts -->
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

  <!-- Design system styles (includes Utopia scales, grid, themes) -->
  <link rel="stylesheet" href="/css/styles/index.css">

  <!-- Favicon -->
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
</head>
<body>
  <a href="#main" class="skip-link">Skip to main content</a>

  <header>
    <nav aria-label="Main navigation">...</nav>
  </header>

  <main id="main" class="u-container">
    <h1>Page Title</h1>
    <!-- Content uses --step-* for type, --space-* for spacing -->
  </main>

  <footer>...</footer>

  <script type="module" src="/js/main.js"></script>
</body>
</html>
```

---

## Quick Reference

### Semantic Elements
```
<header>     Page/section header with nav
<nav>        Navigation links
<main>       Primary page content (one per page)
<article>    Self-contained content
<section>    Thematic grouping with heading
<aside>      Tangentially related content
<footer>     Page/section footer
<figure>     Self-contained media with caption
<time>       Machine-readable date/time
<address>    Contact information
```

### ARIA Landmarks
```
role="banner"        Header (implicit)
role="navigation"    Nav (implicit)
role="main"          Main (implicit)
role="complementary" Aside (implicit)
role="contentinfo"   Footer (implicit)
role="search"        Search form
role="form"          Named form region
```

### Form Input Types
```
text, email, tel, url, search, password
number, range, date, time, datetime-local
checkbox, radio, file, color
submit, reset, button, hidden
```

### Loading Strategies
```
loading="lazy"       Defer until near viewport
loading="eager"      Load immediately
fetchpriority="high" Prioritize resource
async                Load in parallel, execute when ready
defer                Load in parallel, execute after parse
modulepreload        Preload ES modules for web components
```

### FOUC Prevention for Web Components
```
:not(:defined)       Target undefined custom elements
opacity: 0           Hide without layout shift (preserve space)
modulepreload        Preload critical component scripts
```

### Common Mistakes

```html
<!-- ❌ Don't -->
<div onclick="...">Clickable div</div>
<img src="image.jpg">
<h1>Title</h1><h3>Subtitle</h3>
<input placeholder="Email">
<button role="button">Submit</button>

<!-- ✅ Do -->
<button onclick="...">Clickable button</button>
<img src="image.jpg" alt="Description" width="800" height="600">
<h1>Title</h1><h2>Subtitle</h2>
<label for="email">Email</label><input id="email" type="email">
<button>Submit</button>
```

### Design Tokens (This Project)

```
/* Typography - see utopia-fluid-scales */
--step--2 to --step-5    Font sizes (body: --step-0)

/* Spacing - see utopia-fluid-scales */
--space-3xs to --space-3xl   Fixed steps
--space-s-m, --space-s-l     Fluid pairs

/* Grid - see utopia-grid-layout */
--grid-max-width             1240px
--grid-gutter                var(--space-s-l)
.u-container                 Max-width + padding
.u-grid                      Grid with gutter gap
```

### Validation Checklist

- [ ] W3C HTML validation: 0 errors
- [ ] Heading hierarchy: h1 → h2 → h3 (no skips)
- [ ] All images have alt text
- [ ] All form inputs have labels
- [ ] Skip links present
- [ ] Landmark regions defined
- [ ] Image dimensions specified
- [ ] Lazy loading on below-fold images
- [ ] Uses design tokens (no hardcoded px for type/spacing)
- [ ] Scripts use `type="module"` or `defer`
- [ ] Meta description present
- [ ] Canonical URL specified
