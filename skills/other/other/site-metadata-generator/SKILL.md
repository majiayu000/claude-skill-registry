---
name: seo-optimizer
description: >
  Comprehensive SEO optimization for web applications. Use when asked to improve
  search rankings, add meta tags, create structured data, generate sitemaps,
  optimize for Core Web Vitals, or analyze SEO issues. Works with Next.js, Astro,
  React, and static HTML sites.
---

# SEO Optimizer

Transform your web application from invisible to discoverable. This skill analyzes your codebase and implements comprehensive SEO optimizations that help search engines and social platforms understand, index, and surface your content.

## Philosophy: SEO as Semantic Communication

SEO is not about gaming algorithms—it's about **clearly communicating what your content IS** to machines (search engines, social platforms, AI crawlers) so they can properly understand and surface it.

**Before optimizing, ask**:
- What is this page actually about? (not what keywords we want to rank for)
- Who is the intended audience and what are they searching for?
- What unique value does this content provide?
- How should machines categorize and understand this content?

**Core Principles**:

1. **Accuracy Over Optimization**: Describe what IS, not what you wish would rank
2. **User Intent First**: Match content to what searchers actually want
3. **Semantic Clarity**: Use structured data to make meaning machine-readable
4. **Progressive Enhancement**: Basic SEO for all pages, rich optimization for key pages
5. **Framework-Native**: Use each framework's idioms, not generic hacks

**The SEO Hierarchy** (prioritize in order):
```
1. Content Quality      ← Foundation: Valuable, accurate, unique content
2. Technical Access     ← Can crawlers find and index your pages?
3. Semantic Structure   ← Do machines understand your content's meaning?
4. Meta Optimization    ← Are your titles/descriptions compelling?
5. Structured Data      ← JSON-LD for rich search results
6. Performance          ← Core Web Vitals affect rankings
```

---

## Codebase Analysis Workflow

**ALWAYS analyze before implementing.** Different codebases need different approaches.

### Step 1: Discover Framework and Structure

Identify the framework and routing pattern:
- **Next.js**: Look for `next.config.js`, `app/` or `pages/` directory
- **Astro**: Look for `astro.config.mjs`, `src/pages/`
- **React Router**: Look for route configuration, `react-router-dom`
- **Gatsby**: Look for `gatsby-config.js`, `gatsby-node.js`
- **Static HTML**: Look for `.html` files in root or `public/`

### Step 2: Audit Current SEO State

Check for existing implementations:
- [ ] Meta tags in `<head>` (title, description, viewport)
- [ ] Open Graph tags (`og:title`, `og:image`, etc.)
- [ ] Twitter Card tags (`twitter:card`, `twitter:image`)
- [ ] Structured data (`<script type="application/ld+json">`)
- [ ] Sitemap (`sitemap.xml` or generation config)
- [ ] Robots.txt file
- [ ] Canonical URLs
- [ ] Alt text on images

### Step 3: Identify Page Types

Different pages need different SEO approaches:

| Page Type | Priority | Key Optimizations |
|-----------|----------|-------------------|
| Landing/Home | Critical | Brand keywords, comprehensive structured data |
| Product/Service | High | Product schema, reviews, pricing |
| Blog/Article | High | Article schema, author, publish date |
| Documentation | Medium | HowTo/FAQ schema, breadcrumbs |
| About/Contact | Medium | Organization schema, local business |
| Legal/Privacy | Low | Basic meta only, often noindex |

### Step 4: Generate Implementation Plan

Based on analysis, prioritize:
1. **Quick wins**: Missing meta tags, viewport, basic structure
2. **High impact**: Structured data for key pages, sitemap
3. **Refinement**: Performance, advanced schema, social optimization

See `references/analysis-checklist.md` for detailed audit procedures.

---

## Meta Tags Implementation

### Essential Meta Tags (Every Page)

```html
<!-- Required -->
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{Page Title} | {Site Name}</title>
<meta name="description" content="{150-160 char description}">

<!-- Recommended -->
<link rel="canonical" href="{full canonical URL}">
<meta name="robots" content="index, follow">
```

### Title Tag Best Practices

**Format**: `{Primary Content} | {Brand}` or `{Primary Content} - {Brand}`

**Guidelines**:
- 50-60 characters (Google truncates at ~60)
- Front-load important keywords
- Unique for every page
- Accurately describe page content
- Include brand for recognition (usually at end)

**Title Patterns by Page Type**:
```
Homepage:     {Brand} - {Value Proposition}
Product:      {Product Name} - {Key Benefit} | {Brand}
Article:      {Article Title} | {Brand}
Category:     {Category} Products | {Brand}
Search:       Search Results for "{Query}" | {Brand}
```

### Meta Description Best Practices

**Guidelines**:
- 150-160 characters (Google may truncate at ~155)
- Include a call to action when appropriate
- Accurately summarize page content
- Unique for every page
- Include primary keyword naturally

**DO NOT**:
- Stuff keywords unnaturally
- Use the same description across pages
- Write descriptions that don't match content
- Start with "Welcome to..." or similar filler

### Open Graph Tags (Social Sharing)

```html
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical URL}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{1200x630 image URL}">
<meta property="og:site_name" content="{Site Name}">
```

### Twitter Card Tags

```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@{handle}">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{image URL}">
```

See `references/meta-tags-complete.md` for comprehensive tag reference.

---

## Structured Data (JSON-LD)

Structured data enables rich search results (star ratings, prices, FAQs, etc.).

### When to Use Which Schema

| Content Type | Schema | Rich Result |
|--------------|--------|-------------|
| Organization info | Organization | Knowledge panel |
| Products | Product | Price, availability, reviews |
| Articles/Blog | Article | Headline, image, date |
| How-to guides | HowTo | Step-by-step in search |
| FAQs | FAQPage | Expandable Q&A |
| Events | Event | Date, location, tickets |
| Recipes | Recipe | Image, time, ratings |
| Local business | LocalBusiness | Maps, hours, contact |
| Breadcrumbs | BreadcrumbList | Navigation path |

### Implementation Pattern

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

### Multiple Schemas Per Page

Use `@graph` to combine schemas:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Organization", ... },
    { "@type": "WebSite", ... },
    { "@type": "BreadcrumbList", ... }
  ]
}
```

See `references/structured-data-schemas.md` for complete schema examples.

---

## Technical SEO

### Sitemap Generation

**XML Sitemap Requirements**:
- Include all indexable pages
- Exclude noindex pages, redirects, error pages
- Update `<lastmod>` when content changes
- Submit to Google Search Console

**Framework implementations**: See `references/framework-implementations.md`

### Robots.txt

**Standard Template**:
```txt
User-agent: *
Allow: /

# Block admin/private areas
Disallow: /admin/
Disallow: /api/
Disallow: /private/

# Point to sitemap
Sitemap: https://yourdomain.com/sitemap.xml
```

### Canonical URLs

**Always set canonical URLs to**:
- Prevent duplicate content issues
- Consolidate link equity
- Specify preferred URL version

**Handle**:
- www vs non-www
- http vs https
- Trailing slashes
- Query parameters

### Performance (Core Web Vitals)

Core Web Vitals affect rankings. Monitor:

| Metric | Target | What It Measures |
|--------|--------|------------------|
| LCP | < 2.5s | Largest Contentful Paint (loading) |
| INP | < 200ms | Interaction to Next Paint (interactivity) |
| CLS | < 0.1 | Cumulative Layout Shift (visual stability) |

**Quick wins**:
- Optimize images (WebP, lazy loading, proper sizing)
- Minimize JavaScript bundles
- Use efficient fonts (display: swap)
- Implement proper caching

---

## Anti-Patterns to Avoid

❌ **Keyword Stuffing**
```html
<!-- BAD -->
<title>Best Shoes | Buy Shoes | Cheap Shoes | Shoes Online | Shoe Store</title>

<!-- GOOD -->
<title>Running Shoes for Marathon Training | SportShop</title>
```
Why bad: Search engines penalize unnatural keyword repetition. Users don't click spammy titles.

❌ **Duplicate Descriptions**
Using the same meta description across multiple pages.
Why bad: Misses opportunity for page-specific relevance. Google may ignore and auto-generate.

❌ **Description/Content Mismatch**
Writing descriptions for keywords rather than actual content.
Why bad: High bounce rates signal low quality. Users feel deceived.

❌ **Missing Alt Text**
```html
<!-- BAD -->
<img src="product.jpg">

<!-- GOOD -->
<img src="product.jpg" alt="Blue Nike Air Max running shoe, side view">
```
Why bad: Accessibility violation. Missed image search opportunity.

❌ **Blocking Crawlers Unintentionally**
```txt
# Accidentally blocking everything
User-agent: *
Disallow: /
```
Why bad: Complete deindexing. Check robots.txt carefully.

❌ **Ignoring Mobile**
Not having responsive design or mobile-specific considerations.
Why bad: Google uses mobile-first indexing. Most traffic is mobile.

❌ **Over-Optimization**
Adding structured data for content that doesn't exist.
Why bad: Schema violations can result in penalties. Trust erosion.

❌ **Generic Auto-Generated Content**
```html
<!-- BAD: Template without customization -->
<meta name="description" content="Welcome to our website. We offer great products and services.">
```
Why bad: Provides no value. Won't rank. Won't get clicks.

---

## Variation Guidance

**IMPORTANT**: SEO implementation should vary based on context.

**Vary based on**:
- **Industry**: E-commerce needs Product schema; SaaS needs Software schema
- **Content type**: Blog posts vs landing pages vs documentation
- **Audience**: B2B vs B2C affects tone and keywords
- **Competition**: Highly competitive niches need more sophisticated optimization
- **Framework**: Use native patterns (Next.js metadata API vs manual tags)

**Avoid converging on**:
- Same title format for all page types
- Generic descriptions that could apply to any site
- Identical structured data without page-specific content
- One-size-fits-all sitemap configuration

---

## Framework Quick Reference

### Next.js (App Router)

```typescript
// app/page.tsx
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Page Title | Brand',
  description: 'Page description',
  openGraph: {
    title: 'Page Title',
    description: 'Page description',
    images: ['/og-image.png'],
  },
}
```

### Next.js (Pages Router)

```typescript
// pages/index.tsx
import Head from 'next/head'

export default function Page() {
  return (
    <Head>
      <title>Page Title | Brand</title>
      <meta name="description" content="Page description" />
    </Head>
  )
}
```

### Astro

```astro
---
// src/pages/index.astro
import Layout from '../layouts/Layout.astro';
---
<Layout
  title="Page Title | Brand"
  description="Page description"
  ogImage="/og-image.png"
/>
```

### React (react-helmet)

```jsx
import { Helmet } from 'react-helmet';

function Page() {
  return (
    <Helmet>
      <title>Page Title | Brand</title>
      <meta name="description" content="Page description" />
    </Helmet>
  );
}
```

See `references/framework-implementations.md` for complete guides.

---

## Scripts

### analyze_seo.py

Analyzes a codebase for SEO issues and opportunities:

```bash
python scripts/analyze_seo.py <path-to-project>
```

**Output**:
- Current SEO state (what's implemented)
- Missing elements by priority
- Page-by-page recommendations
- Structured data opportunities

### generate_sitemap.py

Generates sitemap.xml from project routes:

```bash
python scripts/generate_sitemap.py <path-to-project> --domain https://example.com
```

---

## Remember

**SEO is semantic communication, not algorithm manipulation.**

The best SEO:
- Accurately describes what content IS
- Helps machines understand meaning through structured data
- Prioritizes user value over keyword optimization
- Uses framework-native patterns
- Implements progressively based on page importance

Focus on making your content findable and understandable. The rankings follow from genuine value clearly communicated.

**Claude is capable of comprehensive SEO analysis and implementation. These guidelines illuminate the path—they don't fence it.**
