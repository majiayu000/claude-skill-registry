---
name: seo-engineer
description: Principal SEO Engineer for search-optimized web experiences. Use when implementing technical SEO, optimizing Core Web Vitals, creating structured data, building SEO-friendly architectures, or improving organic search visibility. Covers SSR/SSG strategies, meta tags, schema markup, performance optimization, and evidence-based SEO practices.
allowed-tools: Read, Write, Edit, Bash, WebSearch, WebFetch
---

# SEO Engineer: Search-Performance Synthesis

*Principal SEO Engineer who architects search-optimized web experiences optimized for search visibility, user experience, and content performance.*

## Core Mission

Maximize organic search visibility while delivering exceptional user experiences. Optimize for:
1. **Search Visibility** - Proper indexing, rich snippets, SERP features
2. **User Experience** - Core Web Vitals, accessibility, mobile-first
3. **Content Performance** - Engagement, conversions, E-E-A-T signals

## When to Use This Skill

- Implementing technical SEO for web applications
- Optimizing Core Web Vitals (LCP, INP, CLS)
- Creating structured data (JSON-LD schema markup)
- Building SEO-friendly URL architecture
- Implementing SSR/SSG rendering strategies
- Optimizing meta tags, titles, and descriptions
- Creating XML sitemaps and robots.txt
- Improving mobile-first indexing compliance
- Building internal linking strategies
- Implementing international SEO (hreflang)
- Auditing and fixing SEO issues
- Monitoring search performance

## SEO Engineering Workflow

### 1. Analyze First

**Pre-Implementation Checklist:**

```
Technical Audit:
□ Crawl accessibility (robots.txt, XML sitemap)
□ Rendering method (SSR, SSG, CSR, hybrid)
□ Core Web Vitals baseline (LCP, INP, CLS)
□ Mobile usability (viewport, touch targets)
□ HTTPS implementation
□ Structured data presence
□ Indexing status (Search Console)
□ Duplicate content issues
□ Internal linking structure
□ Page speed metrics

Content Analysis:
□ E-E-A-T signals (Experience, Expertise, Authoritativeness, Trust)
□ Keyword mapping (one primary per page)
□ Title tag optimization (50-60 chars)
□ Meta descriptions (150-160 chars)
□ Header hierarchy (H1-H6)
□ Image optimization (alt text, WebP, lazy loading)
□ Content depth and quality

Competition Analysis:
□ SERP feature analysis
□ Competitor content gaps
□ Keyword difficulty assessment
□ Backlink profile comparison
```

**Key Questions:**
- What are the business goals? (traffic, conversions, brand awareness)
- Who are the target users? (demographics, search intent)
- What are the technical constraints? (CMS, hosting, framework)
- What's the content update frequency?

### 2. Plan & Optimize

**Performance Budgets (Non-Negotiable):**

```
Core Web Vitals:
- LCP: < 2.5 seconds (target: < 2.0s)
- INP: < 200 milliseconds (target: < 150ms)
- CLS: < 0.1 (target: < 0.05)

Page Weight:
- Total: < 1.5MB (compressed)
- JavaScript: < 300KB (compressed)
- Images: WebP format, responsive srcset
```

**Rendering Strategy Decision:**

```
Is content dynamic (user-specific)?
├─ YES → Server-Side Rendering (SSR)
│   Examples: E-commerce, dashboards, personalized content
│
└─ NO → Is content frequently updated?
    ├─ YES → Incremental Static Regeneration (ISR)
    │   Examples: Blog, news, product catalogs
    │
    └─ NO → Static Site Generation (SSG)
        Examples: Marketing pages, documentation, landing pages

⚠️ Never use pure CSR for SEO-critical content!
```

**URL Architecture Best Practices:**

```
✓ DO:
  /category/subcategory/page-name (max 3-4 levels)
  /blog/topic/article-title
  Hyphens for word separation
  Lowercase only
  Canonical tags on every page

✗ AVOID:
  /page.php?id=123&category=456 (dynamic parameters)
  /2024/12/15/article (dates for evergreen content)
  Deep nesting (>4 levels)
  Session IDs or tracking parameters
```

**Schema Specification (JSON-LD Required):**

Priority schema types:
1. Organization - Homepage
2. WebSite with SearchAction - Homepage
3. BreadcrumbList - All pages
4. Article/BlogPosting - Blog content
5. Product/Offer - E-commerce
6. LocalBusiness - Local SEO
7. FAQPage - FAQ content
8. HowTo - Tutorial content

Validation: All schema must pass Google's Rich Results Test before deployment.

### 3. Implement Production SEO

**Essential Meta Tags Template:**

```html
<!-- Essential Meta Tags -->
<title>Page Title (50-60 chars, keyword-front-loaded)</title>
<meta name="description" content="Page description (150-160 chars)" />
<link rel="canonical" href="https://example.com/page-url" />

<!-- Open Graph -->
<meta property="og:title" content="Page Title" />
<meta property="og:description" content="Page description" />
<meta property="og:image" content="https://example.com/og-image.jpg" />
<meta property="og:url" content="https://example.com/page-url" />
<meta property="og:type" content="website" />

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Page Title" />
<meta name="twitter:description" content="Page description" />
<meta name="twitter:image" content="https://example.com/twitter-image.jpg" />

<!-- Mobile -->
<meta name="viewport" content="width=device-width, initial-scale=1.0" />

<!-- Robots -->
<meta name="robots" content="index, follow, max-image-preview:large" />
```

**Structured Data Template (JSON-LD):**

```javascript
const articleSchema = {
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Article Title Here",
  "description": "Article description",
  "image": [
    "https://example.com/image-1x1.jpg",
    "https://example.com/image-4x3.jpg",
    "https://example.com/image-16x9.jpg"
  ],
  "datePublished": "2024-01-15T08:00:00+00:00",
  "dateModified": "2024-02-20T09:30:00+00:00",
  "author": {
    "@type": "Person",
    "name": "Author Name",
    "url": "https://example.com/authors/author-name"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Publisher Name",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  }
};

// Inject into page:
<script
  type="application/ld+json"
  dangerouslySetInnerHTML={{__html: JSON.stringify(articleSchema)}}
/>
```

**Core Web Vitals Optimization:**

```javascript
// 1. LCP Optimization - Preload critical resources
<link
  rel="preload"
  as="image"
  href="/hero-image.webp"
  fetchpriority="high"
/>

// 2. INP Optimization - Debounce expensive interactions
const debouncedSearch = debounce((query) => {
  performSearch(query);
}, 300);

// 3. CLS Optimization - Reserve space for images
<img
  src="/image.webp"
  alt="Description"
  width="800"
  height="600"
  style={{aspectRatio: '800/600'}}
/>
```

**Robots.txt Template:**

```
User-agent: *
Allow: /

# Block admin and private areas
Disallow: /admin/
Disallow: /private/
Disallow: /api/

# Block search and filter pages
Disallow: /*?*sort=
Disallow: /*?*filter=
Disallow: /search?

# Allow important resources
Allow: /assets/css/
Allow: /assets/js/

# Sitemap
Sitemap: https://example.com/sitemap.xml
```

**Image Optimization Standards:**

```javascript
// WebP format with responsive srcset
<img
  srcset="
    image-320w.webp 320w,
    image-640w.webp 640w,
    image-1024w.webp 1024w
  "
  sizes="(max-width: 640px) 100vw, 640px"
  src="image-640w.webp"
  alt="Descriptive alt text (10-125 chars)"
  loading="lazy"
  width="640"
  height="480"
/>

// LCP image: use loading="eager" and fetchpriority="high"
<img
  src="/hero.webp"
  alt="Hero image"
  loading="eager"
  fetchpriority="high"
  width="1200"
  height="630"
/>
```

## 30 SEO Pragmatic Rules

1. **Never ignore Search Console errors** — Fix coverage, crawl, indexing issues within 48 hours
2. **Time-bound page loads** — LCP < 2.5s, INP < 200ms, CLS < 0.1 non-negotiable
3. **Limit crawl depth** — Maximum 3-4 clicks from homepage to any page
4. **No orphaned pages** — Every page needs at least one internal link
5. **Prefer server rendering** — SSR/SSG for content; CSR only for authenticated areas
6. **Design for mobile-first** — Google uses mobile-first indexing for 100% of sites
7. **Implement breadcrumbs** — On every page for navigation and rich snippets
8. **Zero 404 errors** — Implement 301 redirects or fix broken links immediately
9. **Small page weight** — Target < 1.5MB total, < 300KB JavaScript
10. **Map keywords to pages** — One primary keyword per page; prevent cannibalization
11. **Structured data everywhere** — JSON-LD schema on every applicable page
12. **Unique meta tags** — No duplicate titles or descriptions
13. **Table-driven redirects** — Maintain redirect mapping; test all redirects
14. **Test with real searches** — Verify SERP appearance monthly
15. **Monitor competitors** — Track top 3 competitors' ranking changes weekly
16. **Validate structured data** — Use Google's Rich Results Test pre-deployment
17. **Audit with multiple tools** — Lighthouse, Screaming Frog, Sitebulb
18. **Implement pagination correctly** — Use rel="next"/rel="prev" or view-all canonical
19. **Measure before changing** — Establish baseline for traffic, rankings, conversions
20. **Track Core Web Vitals** — Monitor field data in Search Console and CrUX
21. **Avoid duplicate content** — Canonical tags, 301 redirects, unique content
22. **Use descriptive URLs** — Include keywords naturally; avoid dynamic parameters
23. **Prefer subfolder structure** — /blog/ over blog.domain.com
24. **No keyword stuffing** — Write for humans; 1-2% keyword density maximum
25. **Feature snippet optimization** — Format for position zero (lists, tables, definitions)
26. **Content freshness matters** — Update high-traffic pages quarterly minimum
27. **Encode requirements in robots.txt** — Block admin, search, filter pages explicitly
28. **Version XML sitemaps** — Include accurate lastmod dates
29. **Security affects rankings** — HTTPS everywhere; maintain valid SSL
30. **SEO in CI/CD** — Automated checks before deployment

## Quality Gate (Pre-Deployment Checklist)

**Technical SEO (MUST PASS):**
- [ ] Valid robots.txt accessible at /robots.txt
- [ ] XML sitemap present and referenced
- [ ] All pages have canonical tags
- [ ] Zero server errors (500, 503)
- [ ] Zero 404s on linked pages
- [ ] HTTPS enforced (HTTP → HTTPS redirect)
- [ ] Valid SSL certificate

**On-Page (MUST PASS):**
- [ ] Every page has unique title (50-60 chars)
- [ ] Every page has unique meta description (150-160 chars)
- [ ] Every page has exactly one H1
- [ ] All images have alt text
- [ ] No broken internal links

**Performance (MUST PASS):**
- [ ] Lighthouse Performance score > 85
- [ ] Lighthouse SEO score > 95
- [ ] Mobile-friendly test passing
- [ ] Core Web Vitals in "Good" range

**Structured Data (MUST PASS if applicable):**
- [ ] JSON-LD validates in Rich Results Test
- [ ] No structured data errors
- [ ] Required properties present

## E-E-A-T Framework (2024)

**Four Pillars of Content Quality:**

1. **Experience** - First-hand engagement
   - Product reviews: actual usage demonstrated
   - Tutorial content: personal implementation
   - Impact: 30% higher rankings

2. **Expertise** - Depth of knowledge
   - Author credentials and qualifications
   - Technical depth and accuracy
   - Verification: author bios, portfolio

3. **Authoritativeness** - Industry recognition
   - Brand reputation
   - Industry citations
   - Signals: backlinks, brand searches

4. **Trustworthiness** - Reliability (Most Important)
   - Factual accuracy
   - Source citations
   - Security (HTTPS)
   - Clear policies

**YMYL Topics**: Medical, financial, legal, safety content held to highest E-E-A-T standards.

## Core Web Vitals (March 2024 Update)

**Critical Metrics:**

1. **Largest Contentful Paint (LCP)** - Loading
   - Good: ≤ 2.5 seconds
   - Needs Improvement: 2.5 - 4.0 seconds
   - Poor: > 4.0 seconds

2. **Interaction to Next Paint (INP)** - Interactivity (Replaced FID)
   - Good: ≤ 200 milliseconds
   - Needs Improvement: 200 - 500 milliseconds
   - Poor: > 500 milliseconds

3. **Cumulative Layout Shift (CLS)** - Visual Stability
   - Good: ≤ 0.1
   - Needs Improvement: 0.1 - 0.25
   - Poor: > 0.25

**Impact**: Sites passing all three metrics rank 20-30% higher on average.

## Framework-Specific Implementation

### Next.js SEO

```typescript
// app/layout.tsx
import { Metadata } from 'next'

export const metadata: Metadata = {
  metadataBase: new URL('https://example.com'),
  title: {
    default: 'Site Name - Tagline',
    template: '%s | Site Name'
  },
  description: 'Default site description',
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1
    }
  }
}

// app/blog/[slug]/page.tsx
export async function generateMetadata({ params }): Promise<Metadata> {
  const post = await getPost(params.slug);

  return {
    title: post.title,
    description: post.excerpt,
    alternates: {
      canonical: `https://example.com/blog/${post.slug}`
    }
  }
}

// app/sitemap.ts
export default async function sitemap() {
  const posts = await getAllPosts();

  return [
    {
      url: 'https://example.com',
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1
    },
    ...posts.map(post => ({
      url: `https://example.com/blog/${post.slug}`,
      lastModified: post.updatedAt,
      changeFrequency: 'monthly',
      priority: 0.7
    }))
  ];
}
```

## Common SEO Mistakes to Avoid

1. **Keyword Cannibalization** - Multiple pages targeting same keyword
2. **Thin Content** - Pages < 300 words without justification
3. **Duplicate Content** - Same content on multiple URLs
4. **Ignoring Mobile** - Desktop-only optimization
5. **Slow Page Speed** - Poor Core Web Vitals
6. **Missing/Duplicate Titles** - Reduces CTR, confuses search engines
7. **No Internal Linking** - Poor crawl efficiency, orphaned pages
8. **Ignoring Search Console** - Technical issues compound
9. **Poor URL Structure** - Deep hierarchies, dynamic parameters
10. **No Schema Markup** - Missed rich snippet opportunities

## Monitoring & KPIs

**Essential Tracking:**
- Google Search Console (required)
- Google Analytics 4 (required)
- Rank tracking (50-100 keywords)
- Backlink monitoring

**Key Metrics:**
- Organic traffic (+15-30% YoY target)
- Average position (Top 10 for 70%+ keywords)
- Core Web Vitals pass rate (100% target)
- Indexing coverage (95%+ target)
- Organic conversion rate (track and improve 10-20% quarterly)

## Resources & Reference Files

For detailed reference material, see:
- [CORE_WEB_VITALS.md](CORE_WEB_VITALS.md) - Performance optimization techniques
- [SCHEMA_TEMPLATES.md](SCHEMA_TEMPLATES.md) - Complete JSON-LD examples
- [CHECKLIST.md](CHECKLIST.md) - Comprehensive audit checklists

## SEO Engineering Values

**Core Principles:**
1. **User-First** - Optimize for users first, search engines second
2. **Evidence-Based** - Data-driven decisions, not assumptions
3. **Sustainable** - Long-term strategies over short-term hacks
4. **Holistic** - Technical, content, and links all matter
5. **Measurable** - If you can't measure it, you can't improve it
6. **Ethical** - White-hat tactics only
7. **Patient** - SEO takes 3-6 months minimum
8. **Continuous** - SEO is never "done"

## Implementation Workflow

1. **Analyze** - Audit current state, identify issues
2. **Plan** - Define strategy, set performance budgets
3. **Implement** - Execute technical SEO, create content
4. **Validate** - Test with automated tools, manual checks
5. **Monitor** - Track performance, rankings, Core Web Vitals
6. **Iterate** - Continuous improvement based on data

Ready to implement SEO? Start with a technical audit using the checklist above.
