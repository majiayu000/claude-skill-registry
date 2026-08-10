---
name: seo-optimization
description: Optimize a webpage for search engines by analyzing on-page elements, improving technical performance, and implementing structured data for maximum visibility. Use when the user requests seo optimization or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# SEO Optimization

This skill enables an AI agent to perform comprehensive search engine optimization on any webpage or website. The agent audits on-page factors (title tags, meta descriptions, headings, internal links), evaluates technical SEO health (Core Web Vitals, mobile-first indexing, crawlability), and implements structured data markup. The goal is to produce actionable recommendations that improve organic search rankings and click-through rates.

## Workflow

1. **Crawl and inventory the page.** Fetch the target URL and parse the full HTML document. Extract the title tag, meta description, canonical URL, Open Graph tags, all heading elements (H1–H6), images with alt attributes, and every internal and external link. Record the HTTP status code, response time, and redirect chain if applicable.

2. **Analyze on-page SEO elements.** Evaluate the title tag for length (50–60 characters), keyword placement, and uniqueness. Check the meta description for length (150–160 characters) and compelling call-to-action language. Verify there is exactly one H1 tag that contains the primary keyword, and that H2–H4 tags form a logical content hierarchy. Flag missing alt text on images and broken internal links.

3. **Evaluate technical SEO factors.** Assess Core Web Vitals — Largest Contentful Paint (LCP < 2.5s), First Input Delay (FID < 100ms), and Cumulative Layout Shift (CLS < 0.1). Check mobile-friendliness by analyzing the viewport meta tag and responsive layout. Verify the existence and correctness of `robots.txt`, XML sitemap, canonical tags, and hreflang tags for international sites. Identify render-blocking resources and unused CSS/JS.

4. **Implement structured data markup.** Generate JSON-LD schema markup appropriate to the page type — Article, Product, FAQ, BreadcrumbList, Organization, or LocalBusiness. Validate the markup against Google's Rich Results requirements. Ensure the schema references match the visible page content to avoid structured data penalties.

5. **Audit internal linking and content depth.** Map the internal link graph to identify orphan pages and shallow content clusters. Recommend anchor text improvements and suggest new internal links that strengthen topical authority. Evaluate content length and keyword density relative to top-ranking competitors.

6. **Generate a prioritized SEO report.** Produce a structured report with findings organized by impact (critical, high, medium, low). Include before/after code snippets for recommended changes, estimated effort for each fix, and expected ranking impact. Provide a checklist format so engineers and content teams can track completion.

## Usage

Provide the agent with the URL of the webpage to optimize and, optionally, the target keyword. The agent will return a full audit report with actionable fixes.

**Prompt:** `Optimize the following page for the keyword "project management tools": https://example.com/blog/best-pm-tools`

## Examples

### Example 1: Blog Post On-Page Optimization

**Request:** Optimize `https://acme.com/blog/remote-work-tips` for the keyword "remote work tips".

**Before — HTML head:**
```html
<head>
  <title>Blog Post | Acme Co</title>
  <meta name="description" content="Read our latest blog post.">
</head>
```

**After — Optimized HTML head:**
```html
<head>
  <title>15 Remote Work Tips That Boost Productivity in 2025 | Acme Co</title>
  <meta name="description" content="Discover 15 proven remote work tips to stay productive, manage your time, and avoid burnout. Backed by research from 500+ distributed teams.">
  <link rel="canonical" href="https://acme.com/blog/remote-work-tips">
  <meta property="og:title" content="15 Remote Work Tips That Boost Productivity">
  <meta property="og:description" content="Proven strategies from 500+ distributed teams.">
  <meta property="og:type" content="article">
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "15 Remote Work Tips That Boost Productivity in 2025",
    "author": { "@type": "Person", "name": "Jane Smith" },
    "datePublished": "2025-03-10",
    "description": "Proven remote work tips backed by research from 500+ distributed teams."
  }
  </script>
</head>
```

### Example 2: Technical SEO Audit Findings

**Request:** Run a technical SEO audit on `https://acme.com`.

**Audit Report:**

| Priority | Issue | Details | Fix |
|----------|-------|---------|-----|
| Critical | Missing XML sitemap | No sitemap found at `/sitemap.xml`; 40% of pages not indexed | Generate and submit sitemap to Search Console |
| Critical | LCP = 4.8s on mobile | Hero image is 2.4 MB uncompressed PNG | Convert to WebP, add `width`/`height`, use `loading="lazy"` |
| High | Duplicate title tags | 12 pages share the title "Acme Co — Home" | Write unique, keyword-rich titles for each page |
| High | Missing canonical tags | 8 pages lack `<link rel="canonical">`, causing index bloat | Add self-referencing canonicals to every page |
| Medium | No `robots.txt` | Entire site crawlable including `/admin` and `/staging` | Create `robots.txt` disallowing private paths |
| Low | Images missing alt text | 34 of 120 images have empty `alt` attributes | Add descriptive alt text with relevant keywords |

## Best Practices

- **Write for humans first, search engines second.** Keyword stuffing degrades user experience and triggers ranking penalties. Aim for natural keyword integration at 1–2% density.
- **Prioritize Core Web Vitals.** Google uses LCP, FID, and CLS as direct ranking signals. Compress images, defer non-critical JS, and set explicit dimensions on media elements.
- **Use self-referencing canonical tags on every page.** This prevents duplicate content issues caused by URL parameters, trailing slashes, or session IDs.
- **Build topical authority through internal linking.** Link related content in clusters around pillar pages. Use descriptive anchor text instead of generic "click here" links.
- **Validate structured data with Google's Rich Results Test.** Incorrect schema can result in manual actions. Always match schema fields to visible on-page content.
- **Monitor changes in Search Console weekly.** Track impressions, clicks, average position, and coverage errors after deploying SEO fixes to measure impact.

## Edge Cases

- **Single-page applications (SPAs):** JavaScript-rendered content may not be crawled. Implement server-side rendering (SSR) or dynamic rendering, and use the URL Inspection tool to verify Google sees the full DOM.
- **Multilingual sites:** Each language version needs its own unique title, meta description, and hreflang annotations. Incorrect hreflang mappings can cause the wrong language to appear in SERPs.
- **Paywalled or gated content:** Use `<meta name="robots" content="noindex">` on pages that require login to avoid thin-content penalties, or implement structured data for paywalled content per Google's guidelines.
- **Pagination:** Use `rel="next"` and `rel="prev"` on paginated archives, and ensure the canonical points to the current page rather than page 1.
- **Rapidly changing content:** For news or e-commerce sites with frequent inventory changes, configure sitemap update frequency and use the Indexing API for time-sensitive pages.
