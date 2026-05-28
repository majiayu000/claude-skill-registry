---
name: roier-seo
description: >
  Technical SEO auditor and fixer. Use when the user wants to:
  - Run a Lighthouse/PageSpeed audit on a website or local dev server
  - Analyze SEO, performance, accessibility, or best practices scores
  - Fix technical SEO issues in their codebase
  - Optimize meta tags, structured data, Core Web Vitals
  - Improve page speed, accessibility, or PWA compliance
  Triggers: "audit my site", "check SEO", "fix SEO", "lighthouse", "pagespeed",
  "improve performance", "meta tags", "structured data", "core web vitals"
---

# Roier SEO - Technical SEO Auditor & Fixer

An AI-powered SEO optimization skill that audits websites and automatically implements fixes.

## When to Use

- User asks to "audit my site" or "check SEO"
- User wants to "improve performance" or "fix SEO issues"
- User mentions "lighthouse", "pagespeed", or "core web vitals"
- User wants to add/fix meta tags, structured data, or accessibility
- User has a local dev server and wants SEO analysis

## Quick Start

### 1. Run an Audit

For a **live website**:
```bash
node ~/.claude/skills/roier-seo/scripts/audit.js https://example.com
```

For a **local dev server** (must be running):
```bash
node ~/.claude/skills/roier-seo/scripts/audit.js http://localhost:3000
```

### 2. Analyze Results

After running the audit, analyze the JSON output to identify issues and prioritize fixes.

### 3. Implement Fixes

Use the fix patterns in this skill to automatically implement SEO improvements in the user's codebase.

---

## Audit Categories

The audit returns scores (0-100) for five categories:

| Category | Description | Weight |
|----------|-------------|--------|
| **Performance** | Page load speed, Core Web Vitals | High |
| **Accessibility** | WCAG compliance, screen reader support | High |
| **Best Practices** | Security, modern web standards | Medium |
| **SEO** | Search engine optimization, crawlability | High |
| **PWA** | Progressive Web App compliance | Low |

---

## Technical SEO Fix Patterns

### Meta Tags (HTML Head)

#### Missing or Bad Title Tag
```html
<!-- Bad -->
<title>Home</title>

<!-- Good -->
<title>Primary Keyword - Secondary Keyword | Brand Name</title>
```

**Rules:**
- 50-60 characters max
- Include primary keyword near the beginning
- Unique per page
- Include brand name at end

#### Missing or Bad Meta Description
```html
<!-- Add to <head> -->
<meta name="description" content="Compelling description with keywords. 150-160 characters that encourages clicks from search results.">
```

**Rules:**
- 150-160 characters
- Include primary and secondary keywords naturally
- Compelling call-to-action
- Unique per page

#### Missing Viewport Meta Tag
```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

#### Missing Charset
```html
<meta charset="UTF-8">
```

#### Missing Language
```html
<html lang="en">
```

### Open Graph Tags (Social Sharing)

```html
<meta property="og:title" content="Page Title">
<meta property="og:description" content="Page description">
<meta property="og:image" content="https://example.com/image.jpg">
<meta property="og:url" content="https://example.com/page">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Brand Name">
```

### Twitter Card Tags

```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Page Title">
<meta name="twitter:description" content="Page description">
<meta name="twitter:image" content="https://example.com/image.jpg">
```

### Canonical URL

```html
<link rel="canonical" href="https://example.com/canonical-page">
```

### Robots Meta

```html
<!-- Allow indexing (default) -->
<meta name="robots" content="index, follow">

<!-- Prevent indexing (for staging, admin pages) -->
<meta name="robots" content="noindex, nofollow">
```

---

## Structured Data (JSON-LD)

### Website Schema
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Site Name",
  "url": "https://example.com",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://example.com/search?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
</script>
```

### Organization Schema
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Company Name",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://twitter.com/company",
    "https://linkedin.com/company/company"
  ]
}
</script>
```

### BreadcrumbList Schema
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com"},
    {"@type": "ListItem", "position": 2, "name": "Category", "item": "https://example.com/category"},
    {"@type": "ListItem", "position": 3, "name": "Page"}
  ]
}
</script>
```

### Article Schema (for blog posts)
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title",
  "author": {"@type": "Person", "name": "Author Name"},
  "datePublished": "2024-01-15",
  "dateModified": "2024-01-20",
  "image": "https://example.com/article-image.jpg",
  "publisher": {
    "@type": "Organization",
    "name": "Publisher Name",
    "logo": {"@type": "ImageObject", "url": "https://example.com/logo.png"}
  }
}
</script>
```

---

## Performance Optimizations

### Image Optimization

#### Add width/height attributes (prevent CLS)
```html
<!-- Bad -->
<img src="image.jpg" alt="Description">

<!-- Good -->
<img src="image.jpg" alt="Description" width="800" height="600">
```

#### Add lazy loading
```html
<img src="image.jpg" alt="Description" loading="lazy">
```

#### Use modern formats (WebP/AVIF)
```html
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="Description">
</picture>
```

### Font Optimization

#### Preload critical fonts
```html
<link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>
```

#### Use font-display: swap
```css
@font-face {
  font-family: 'Custom Font';
  src: url('/fonts/custom.woff2') format('woff2');
  font-display: swap;
}
```

### Resource Hints

```html
<!-- Preconnect to critical third-party origins -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://cdn.example.com">

<!-- DNS prefetch for non-critical origins -->
<link rel="dns-prefetch" href="https://analytics.example.com">

<!-- Preload critical resources -->
<link rel="preload" href="/critical.css" as="style">
<link rel="preload" href="/hero-image.webp" as="image">
```

---

## Accessibility Fixes

### Missing Alt Text
```html
<!-- Bad -->
<img src="photo.jpg">

<!-- Good (descriptive) -->
<img src="photo.jpg" alt="Team members collaborating in the office">

<!-- Good (decorative, intentionally empty) -->
<img src="decoration.jpg" alt="" role="presentation">
```

### Insufficient Color Contrast
Ensure text has at least:
- **4.5:1** contrast ratio for normal text
- **3:1** contrast ratio for large text (18px+ or 14px+ bold)

### Missing Form Labels
```html
<!-- Bad -->
<input type="email" placeholder="Email">

<!-- Good -->
<label for="email">Email Address</label>
<input type="email" id="email" name="email">
```

### Missing Skip Link
```html
<!-- Add as first element in body -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<!-- Style to hide visually but accessible -->
<style>
.skip-link {
  position: absolute;
  left: -9999px;
}
.skip-link:focus {
  left: 0;
  top: 0;
  z-index: 9999;
  background: #000;
  color: #fff;
  padding: 8px 16px;
}
</style>
```

### Missing Landmark Roles
```html
<header role="banner">...</header>
<nav role="navigation">...</nav>
<main role="main" id="main-content">...</main>
<footer role="contentinfo">...</footer>
```

### Button Accessibility
```html
<!-- Bad -->
<div onclick="submit()">Submit</div>

<!-- Good -->
<button type="submit">Submit</button>

<!-- Icon button needs aria-label -->
<button aria-label="Close menu">
  <svg>...</svg>
</button>
```

---

## Best Practices Fixes

### HTTPS
Ensure all resources load over HTTPS. Fix mixed content:
```html
<!-- Bad -->
<img src="http://example.com/image.jpg">

<!-- Good -->
<img src="https://example.com/image.jpg">
```

### Security Headers (via meta tags or server config)
```html
<!-- CSP via meta tag (limited) -->
<meta http-equiv="Content-Security-Policy" content="default-src 'self'">

<!-- Recommended: Set via server headers instead -->
```

### Avoid document.write
Replace with modern DOM manipulation:
```javascript
// Bad
document.write('<script src="app.js"></script>');

// Good
const script = document.createElement('script');
script.src = 'app.js';
document.head.appendChild(script);
```

---

## Framework-Specific Patterns

### Next.js

```jsx
// pages/_app.js or app/layout.js
import Head from 'next/head';

export default function MyApp({ Component, pageProps }) {
  return (
    <>
      <Head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Component {...pageProps} />
    </>
  );
}

// Per-page SEO (pages/about.js)
import Head from 'next/head';

export default function About() {
  return (
    <>
      <Head>
        <title>About Us | Brand Name</title>
        <meta name="description" content="Learn about our company..." />
        <link rel="canonical" href="https://example.com/about" />
      </Head>
      <main>...</main>
    </>
  );
}
```

### React (with react-helmet)

```jsx
import { Helmet } from 'react-helmet';

function Page() {
  return (
    <>
      <Helmet>
        <title>Page Title | Brand</title>
        <meta name="description" content="Page description" />
        <link rel="canonical" href="https://example.com/page" />
      </Helmet>
      <main>...</main>
    </>
  );
}
```

### Vue.js (with vue-meta or useHead)

```vue
<script setup>
useHead({
  title: 'Page Title | Brand',
  meta: [
    { name: 'description', content: 'Page description' }
  ],
  link: [
    { rel: 'canonical', href: 'https://example.com/page' }
  ]
})
</script>
```

### Nuxt.js

```vue
<script setup>
useSeoMeta({
  title: 'Page Title | Brand',
  description: 'Page description',
  ogTitle: 'Page Title',
  ogDescription: 'Page description',
  ogImage: 'https://example.com/og-image.jpg'
})
</script>
```

---

## Workflow

### Step 1: Audit

Run the audit script on the target URL:

```bash
node ~/.claude/skills/roier-seo/scripts/audit.js <URL>
```

This outputs a JSON file with detailed audit results.

### Step 2: Identify Framework

Check the codebase to identify the framework:
- Look for `package.json` dependencies
- Check for framework-specific files (next.config.js, nuxt.config.ts, etc.)
- Identify the HTML entry point or layout files

### Step 3: Prioritize Fixes

Focus on issues with the highest impact:
1. **Critical** (red): Fix immediately
2. **Serious** (orange): Fix soon
3. **Moderate** (yellow): Fix when possible
4. **Minor** (gray): Nice to have

### Step 4: Implement

Use the fix patterns above, adapted to the user's framework.

### Step 5: Re-audit

Run the audit again to verify improvements.

---

## Example Session

**User:** Can you audit my site at localhost:3000 and fix any SEO issues?

**Claude:**
1. Runs `node ~/.claude/skills/roier-seo/scripts/audit.js http://localhost:3000`
2. Analyzes the results
3. Identifies issues (e.g., missing meta description, images without dimensions)
4. Locates the relevant files in the codebase
5. Implements fixes using the appropriate framework pattern
6. Re-runs audit to confirm improvements

---

## Requirements

This skill requires:
- **Node.js 18+** installed
- **Chrome/Chromium** browser (for Lighthouse)
- The audit script dependencies (auto-installed on first run)

Install dependencies manually if needed:
```bash
cd ~/.claude/skills/roier-seo/scripts
npm install
```
