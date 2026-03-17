---
name: seo-analytics-auditor
description: Use this skill when auditing SEO, analyzing Core Web Vitals, verifying meta tags, checking structured data, or troubleshooting analytics implementations. Covers Google Search Console, Google Analytics 4, Cloudflare Web Analytics, and technical SEO best practices.
---

# SEO & Analytics Auditor

Audit SEO, verify analytics, and optimize Core Web Vitals.

## When to Use

**Use for:**

- Auditing SEO meta tags and structured data
- Verifying analytics implementations (GA4, Cloudflare)
- Checking Core Web Vitals (LCP, INP, CLS)
- Troubleshooting Search Console issues
- Validating Open Graph and Twitter Card meta tags
- Reviewing robots.txt and sitemap.xml

## Quick Audit Workflow

```bash
# 1. Run Lighthouse audit
npx lighthouse https://yoursite.com --output=html --output-path=./audit.html

# 2. Check Core Web Vitals
npx lighthouse https://yoursite.com --only-categories=performance

# 3. Validate structured data
# Open: https://search.google.com/test/rich-results
```

## SEO Checklist

### Meta Tags (Required)

```html
<title>Page Title - Brand (50-60 chars)</title>
<meta name="description" content="Description (150-160 chars)" />
<meta name="robots" content="index, follow" />
<link rel="canonical" href="https://domain.com/page/" />
```

### Open Graph (Social Sharing)

```html
<meta property="og:type" content="website" />
<meta property="og:url" content="https://domain.com/" />
<meta property="og:title" content="Title" />
<meta property="og:description" content="Description" />
<meta property="og:image" content="https://domain.com/og-image.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
```

### Twitter Card

```html
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Title" />
<meta name="twitter:description" content="Description" />
<meta name="twitter:image" content="https://domain.com/og-image.png" />
```

### Schema.org (Structured Data)

```html
<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "Name",
    "jobTitle": "Title",
    "url": "https://domain.com"
  }
</script>
```

## Analytics Implementation

### Google Analytics 4

```html
<script
  async
  src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"
></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag() {
    dataLayer.push(arguments);
  }
  gtag("js", new Date());
  gtag("config", "G-XXXXXXXXXX", {
    anonymize_ip: true,
    cookie_flags: "SameSite=None;Secure",
  });
</script>
```

### Cloudflare Web Analytics

```html
<script
  defer
  src="https://static.cloudflareinsights.com/beacon.min.js"
  data-cf-beacon='{"token": "YOUR_TOKEN"}'
></script>
```

## Core Web Vitals Targets (2025)

| Metric                          | Good    | Needs Improvement | Poor    |
| ------------------------------- | ------- | ----------------- | ------- |
| LCP (Largest Contentful Paint)  | < 2.5s  | 2.5s - 4s         | > 4s    |
| INP (Interaction to Next Paint) | < 200ms | 200ms - 500ms     | > 500ms |
| CLS (Cumulative Layout Shift)   | < 0.1   | 0.1 - 0.25        | > 0.25  |

## Testing Tools

| Tool               | URL                                         | Purpose         |
| ------------------ | ------------------------------------------- | --------------- |
| PageSpeed Insights | https://pagespeed.web.dev                   | Core Web Vitals |
| Rich Results Test  | https://search.google.com/test/rich-results | Schema.org      |
| OpenGraph.xyz      | https://www.opengraph.xyz                   | Social preview  |

## Files to Check

- `index.html` - Meta tags, analytics scripts, Schema.org
- `robots.txt` - Crawler directives, sitemap reference
- `sitemap.xml` - URL list, lastmod dates
- `manifest.json` - PWA config

## Common Issues

| Issue                      | Fix                              |
| -------------------------- | -------------------------------- |
| Meta description too short | Use 150-160 characters           |
| Missing canonical URL      | Add `<link rel="canonical">`     |
| OG image wrong size        | Use 1200x630 for best display    |
| Schema.org errors          | Test with Rich Results Test      |
| Analytics not firing       | Check browser console for errors |

## Integration Checklist

- [ ] Google Search Console verified
- [ ] Sitemap submitted to GSC
- [ ] GA4 property created and linked
- [ ] Core Web Vitals in "Good" range
- [ ] Rich Results test passing
- [ ] Social preview working

## See Also

- [Google SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [Core Web Vitals](https://web.dev/articles/vitals)
- [Schema.org](https://schema.org/docs/gs.html)
