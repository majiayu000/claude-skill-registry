---
name: faion-seo-skill
user-invocable: false
description: Comprehensive SEO and AEO (Answer Engine Optimization) skill. Technical SEO, multilingual hreflang, schema markup, llms.txt, Core Web Vitals, accessibility, social meta tags. Use for SEO audits, optimization, and AI search visibility.
---

# SEO & AEO Mastery

**Modern SEO for Search Engines AND AI Assistants (2025-2026)**

---

## Quick Reference

| Area | Key Elements |
|------|--------------|
| **Technical** | robots.txt, sitemap.xml, crawl budget, Core Web Vitals |
| **On-Page** | Semantic HTML, schema markup, headings, meta tags |
| **Multilingual** | hreflang, URL structure, x-default |
| **AI/AEO** | llms.txt, structured data, entity optimization |
| **Social** | Open Graph, Twitter Cards, LinkedIn |
| **Accessibility** | WCAG 2.2, ARIA, screen readers, semantic markup |
| **Performance** | LCP < 2.5s, INP < 200ms, CLS < 0.1 |

---

## Core Principles

### 1. Dual Optimization Strategy

```
Traditional SEO (Google, Bing)
        ↓
    Your Content
        ↓
AI Search (ChatGPT, Perplexity, Claude)
```

**Both need:** Clear structure, authoritative content, proper markup, fast loading.

### 2. E-E-A-T Framework

- **Experience** → First-hand knowledge, case studies
- **Expertise** → Author credentials, depth of content
- **Authoritativeness** → Backlinks, citations, brand mentions
- **Trustworthiness** → HTTPS, contact info, privacy policy

---

## Technical SEO Fundamentals

### robots.txt Best Practices

```txt
# robots.txt - faion.net

User-agent: *
Disallow: /admin/
Disallow: /api/internal/
Disallow: /*?sessionid=
Disallow: /*?utm_
Allow: /api/public/

# AI Crawlers (manage separately)
User-agent: GPTBot
Disallow: /premium/
Allow: /

User-agent: Claude-Web
Disallow: /premium/
Allow: /

User-agent: PerplexityBot
Allow: /

# Sitemaps
Sitemap: https://faion.net/sitemap.xml
Sitemap: https://faion.net/sitemap-articles.xml
```

**Key Rules:**
- Block admin, session URLs, internal APIs
- Manage AI crawlers separately from search crawlers
- Always include Sitemap directive
- Never block CSS/JS files
- Test in Google Search Console before deploying

### sitemap.xml Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://faion.net/guides/sdd-methodology/</loc>
    <lastmod>2026-01-18</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
    <!-- Multilingual alternates -->
    <xhtml:link rel="alternate" hreflang="en" href="https://faion.net/en/guides/sdd-methodology/" />
    <xhtml:link rel="alternate" hreflang="uk" href="https://faion.net/uk/guides/sdd-methodology/" />
    <xhtml:link rel="alternate" hreflang="x-default" href="https://faion.net/guides/sdd-methodology/" />
  </url>
</urlset>
```

**Best Practices:**
- Max 50,000 URLs per sitemap (use sitemap index for more)
- Update `lastmod` only when content changes
- Include in sitemap ONLY indexable pages
- Don't include URLs blocked in robots.txt

---

## Multilingual SEO & hreflang

### URL Structure Options

| Pattern | Example | Pros | Cons |
|---------|---------|------|------|
| **Subdirectories** (recommended) | `/uk/`, `/en/` | Easy to manage, shared domain authority | None significant |
| **Subdomains** | `uk.faion.net` | Separate hosting possible | Split domain authority |
| **ccTLDs** | `faion.ua` | Strong geo-signal | Expensive, complex management |
| **Parameters** ❌ | `?lang=uk` | Easy to implement | Poor SEO, indexing issues |

### hreflang Implementation

```html
<head>
  <!-- Self-referencing required -->
  <link rel="alternate" hreflang="en" href="https://faion.net/en/article/" />
  <link rel="alternate" hreflang="uk" href="https://faion.net/uk/article/" />
  <link rel="alternate" hreflang="de" href="https://faion.net/de/article/" />
  <link rel="alternate" hreflang="x-default" href="https://faion.net/article/" />
</head>
```

**Critical Rules:**
1. Self-referencing tag required on every page
2. Bidirectional linking (if A → B, then B → A)
3. Use ISO 639-1 language codes (en, uk, de)
4. Use ISO 3166-1 Alpha 2 for regions (en-US, en-GB)
5. x-default for language selector or global page
6. Metadata (title, description) MUST match page language
7. Never combine hreflang with noindex

---

## AI Search Optimization (AEO)

### llms.txt Standard

```txt
# llms.txt - https://faion.net/llms.txt

# Faion Network
> AI-powered framework for solopreneurs with 282 methodologies and 43 AI agents

## Core Pages
- About: https://faion.net/about/
- Pricing: https://faion.net/pricing/
- Documentation: https://faion.net/docs/

## Products
- Ultimate Solopreneur Guide: https://faion.net/guide/
- SDD Methodology: https://faion.net/sdd/

## Contact
- Email: hello@faion.net
- Support: https://faion.net/support/

## Exclusions
- /premium/* (subscription required)
- /admin/*
```

**Purpose:**
- Provides AI crawlers with curated site structure
- Clarifies canonical sources
- Reduces hallucination risk
- Emerging standard (like robots.txt for AI)

### Structured Data for AI

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Faion Network",
  "description": "AI-powered framework for solopreneurs",
  "url": "https://faion.net",
  "founder": {
    "@type": "Person",
    "name": "Ruslan Faion"
  },
  "sameAs": [
    "https://twitter.com/faion",
    "https://linkedin.com/company/faion"
  ]
}
```

**Key Schema Types:**
- Organization, Person (brand/author)
- Article, BlogPosting (content)
- Product, Offer (e-commerce)
- FAQPage, HowTo (rich results + AI)
- BreadcrumbList (navigation)
- LocalBusiness (local SEO)

---

## Schema Markup (JSON-LD)

### Article Schema

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "SDD Methodology: Complete Guide",
  "description": "Learn Specification-Driven Development...",
  "image": "https://faion.net/images/sdd-guide.jpg",
  "author": {
    "@type": "Person",
    "name": "Ruslan Faion",
    "url": "https://faion.net/about/"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Faion Network",
    "logo": {
      "@type": "ImageObject",
      "url": "https://faion.net/logo.png"
    }
  },
  "datePublished": "2026-01-15",
  "dateModified": "2026-01-18"
}
```

### Breadcrumb Schema

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://faion.net/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Guides",
      "item": "https://faion.net/guides/"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "SDD Methodology"
    }
  ]
}
```

### FAQ Schema

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is SDD?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "SDD (Specification-Driven Development) is..."
      }
    }
  ]
}
```

---

## Social Meta Tags

### Open Graph (Facebook, LinkedIn)

```html
<meta property="og:type" content="article" />
<meta property="og:title" content="SDD Methodology Guide" />
<meta property="og:description" content="Learn how to build products faster..." />
<meta property="og:image" content="https://faion.net/og-image.jpg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:url" content="https://faion.net/guides/sdd/" />
<meta property="og:site_name" content="Faion Network" />
<meta property="og:locale" content="en_US" />
<meta property="og:locale:alternate" content="uk_UA" />
```

### Twitter Cards

```html
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:site" content="@faion" />
<meta name="twitter:creator" content="@ruslanfaion" />
<meta name="twitter:title" content="SDD Methodology Guide" />
<meta name="twitter:description" content="Learn how to build products faster..." />
<meta name="twitter:image" content="https://faion.net/twitter-image.jpg" />
```

**Image Requirements:**
- Minimum: 1200x630px (1.91:1 ratio)
- Max file size: 8MB
- Formats: JPG, PNG, GIF, WebP
- Always use absolute URLs

---

## Core Web Vitals (2025)

### Target Metrics

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| **LCP** (Largest Contentful Paint) | ≤ 2.5s | 2.5s - 4s | > 4s |
| **INP** (Interaction to Next Paint) | ≤ 200ms | 200ms - 500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | ≤ 0.1 | 0.1 - 0.25 | > 0.25 |

### Optimization Checklist

**LCP:**
- [ ] Preload largest image: `<link rel="preload" as="image" href="...">`
- [ ] Use WebP/AVIF formats (25-35% smaller)
- [ ] Implement lazy loading for below-fold images
- [ ] Optimize server response time (TTFB < 800ms)
- [ ] Use CDN for static assets

**INP:**
- [ ] Minimize main thread blocking
- [ ] Break up long JavaScript tasks (< 50ms chunks)
- [ ] Defer non-critical JS
- [ ] Use `requestIdleCallback` for low-priority work

**CLS:**
- [ ] Always include width/height on images
- [ ] Reserve space for ads and embeds
- [ ] Avoid inserting content above existing content
- [ ] Use `font-display: swap` with font preload

---

## Semantic HTML & Accessibility

### Correct Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title | Site Name</title>
</head>
<body>
  <header role="banner">
    <nav aria-label="Main navigation">
      <ul>
        <li><a href="/">Home</a></li>
      </ul>
    </nav>
  </header>

  <main id="main-content">
    <article>
      <h1>Single H1 Per Page</h1>
      <p>Introduction...</p>

      <section aria-labelledby="section1">
        <h2 id="section1">Section Title</h2>
        <p>Content...</p>

        <h3>Subsection</h3>
        <p>More content...</p>
      </section>
    </article>

    <aside aria-label="Related content">
      <h2>Related Articles</h2>
    </aside>
  </main>

  <footer role="contentinfo">
    <p>&copy; 2026 Faion Network</p>
  </footer>
</body>
</html>
```

### Accessibility Checklist

- [ ] **Headings:** Logical hierarchy (H1 → H2 → H3), single H1
- [ ] **Images:** Descriptive alt text, decorative images: `alt=""`
- [ ] **Links:** Descriptive text (not "click here")
- [ ] **Forms:** Labels associated with inputs
- [ ] **Color:** Sufficient contrast (4.5:1 minimum)
- [ ] **Keyboard:** All interactive elements focusable
- [ ] **ARIA:** Use landmarks (banner, main, navigation, contentinfo)

---

## Internal Linking Strategy

### Pillar-Cluster Model

```
             ┌─────────────────┐
             │  Pillar Page    │
             │ (Head Keyword)  │
             └────────┬────────┘
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
   ┌─────────┐  ┌─────────┐  ┌─────────┐
   │ Cluster │  │ Cluster │  │ Cluster │
   │ (Long-  │  │ (Long-  │  │ (Long-  │
   │  tail)  │  │  tail)  │  │  tail)  │
   └─────────┘  └─────────┘  └─────────┘
```

### Avoiding Keyword Cannibalization

| Issue | Solution |
|-------|----------|
| Multiple pages targeting same keyword | Consolidate with 301 redirects |
| Similar content competing | Merge into comprehensive guide |
| Unclear primary page | Increase internal links to preferred page |
| Same anchor text for different pages | Use unique anchors per target page |

### Best Practices

1. **One primary keyword per page** → map keywords to URLs
2. **Internal links from high-authority pages** → pass link equity
3. **Contextual links within content** → better than footer/sidebar
4. **Descriptive anchor text** → tells Google what page is about
5. **Regular audits** → find orphan pages, broken links

---

## Breadcrumbs

### Implementation

```html
<nav aria-label="Breadcrumb">
  <ol itemscope itemtype="https://schema.org/BreadcrumbList">
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <a itemprop="item" href="https://faion.net/">
        <span itemprop="name">Home</span>
      </a>
      <meta itemprop="position" content="1" />
    </li>
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <a itemprop="item" href="https://faion.net/guides/">
        <span itemprop="name">Guides</span>
      </a>
      <meta itemprop="position" content="2" />
    </li>
    <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <span itemprop="name">SDD Methodology</span>
      <meta itemprop="position" content="3" />
    </li>
  </ol>
</nav>
```

**Rules:**
- 3-5 levels maximum
- Reflect actual site hierarchy
- Last item = current page (no link)
- Include JSON-LD schema
- Visible on desktop (removed from mobile SERPs Jan 2025)

---

## Quick Audits

### Technical SEO Checklist

- [ ] robots.txt configured correctly
- [ ] XML sitemap submitted to Search Console
- [ ] No duplicate content (canonical tags)
- [ ] HTTPS everywhere
- [ ] Mobile-friendly (responsive)
- [ ] Core Web Vitals passing
- [ ] No 4xx/5xx errors
- [ ] Proper redirects (301, not chains)

### On-Page SEO Checklist

- [ ] Unique title tag (50-60 chars)
- [ ] Meta description (120-160 chars)
- [ ] Single H1 with primary keyword
- [ ] Logical heading hierarchy
- [ ] Internal links to related content
- [ ] External links to authoritative sources
- [ ] Image alt text
- [ ] Schema markup

### AI/AEO Checklist

- [ ] llms.txt file created
- [ ] Organization schema
- [ ] FAQPage schema for Q&A content
- [ ] Clear, factual content structure
- [ ] Entity connections (author, organization)
- [ ] Recent publish/update dates

---

## References

- [references/technical-seo.md](references/technical-seo.md) - robots.txt, sitemaps, crawl budget
- [references/multilingual.md](references/multilingual.md) - hreflang, URL structure
- [references/schema.md](references/schema.md) - JSON-LD templates
- [references/aeo.md](references/aeo.md) - AI optimization, llms.txt
- [references/accessibility.md](references/accessibility.md) - WCAG, ARIA
- [references/performance.md](references/performance.md) - Core Web Vitals

---

## Tools

| Tool | Purpose |
|------|---------|
| [Google Search Console](https://search.google.com/search-console) | Indexing, Core Web Vitals, errors |
| [PageSpeed Insights](https://pagespeed.web.dev/) | Performance analysis |
| [Rich Results Test](https://search.google.com/test/rich-results) | Schema validation |
| [Schema Validator](https://validator.schema.org/) | Schema.org validation |
| [Ahrefs/Semrush](https://ahrefs.com) | Backlinks, keywords, audits |
| [Screaming Frog](https://www.screamingfrog.co.uk/) | Technical crawling |
| [WAVE](https://wave.webaim.org/) | Accessibility testing |

---

## Sources

- [Google Search Central](https://developers.google.com/search)
- [Schema.org](https://schema.org/)
- [Web.dev](https://web.dev/)
- [WCAG 2.2](https://www.w3.org/WAI/WCAG22/quickref/)
- [Yoast SEO Blog](https://yoast.com/seo-blog/)
- [Search Engine Land](https://searchengineland.com/)
- [Backlinko](https://backlinko.com/)
