---
name: seo
description: SEO audit and structured data patterns - meta tags, Open Graph, JSON-LD schema, Core Web Vitals. Use for marketing sites and e-commerce.
triggers:
  - seo
  - meta tags
  - schema
  - open graph
  - structured data
  - sitemap
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
model: opus
user-invocable: true
---

# SEO & Structured Data

Based on [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT). Merged from seo-audit and schema-markup skills.

## 1. Meta Tags & Open Graph

### Title Tags
- 50-60 characters, primary keyword near the beginning
- Unique per page, compelling and click-worthy
- Brand name at end: `Primary Keyword | Brand`

### Meta Descriptions
- 150-160 characters with primary keyword
- Clear value proposition and call to action
- Unique per page (never auto-generated filler)

### Open Graph & Twitter Cards

```html
<!-- Open Graph -->
<meta property="og:title" content="Page Title" />
<meta property="og:description" content="Page description" />
<meta property="og:image" content="https://example.com/og-image.jpg" />
<meta property="og:url" content="https://example.com/page" />
<meta property="og:type" content="website" />

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Page Title" />
<meta name="twitter:description" content="Page description" />
<meta name="twitter:image" content="https://example.com/twitter-image.jpg" />
```

OG images: 1200x630px. Twitter images: 1200x600px.

## 2. JSON-LD Schema Markup

Use JSON-LD format (Google recommended). Place in `<head>` or end of `<body>`.

### Common Schema Types

| Type | Use For | Required Properties |
|------|---------|-------------------|
| Organization | Company homepage | name, url |
| Product | Product pages | name, image, offers |
| Article | Blog posts | headline, image, datePublished, author |
| FAQPage | FAQ content | mainEntity (Q&A array) |
| BreadcrumbList | Any page with breadcrumbs | itemListElement |
| LocalBusiness | Local business pages | name, address |

### Product Schema (E-commerce)

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Product Name",
  "image": "https://example.com/product.jpg",
  "description": "Product description",
  "sku": "SKU-001",
  "brand": { "@type": "Brand", "name": "Brand Name" },
  "offers": {
    "@type": "Offer",
    "price": "29.99",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "url": "https://example.com/product"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "42"
  }
}
```

### Organization Schema

```json
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
```

### Multiple Types with @graph

```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Organization", "name": "...", "url": "..." },
    { "@type": "WebSite", "name": "...", "url": "..." },
    { "@type": "BreadcrumbList", "itemListElement": [...] }
  ]
}
```

## 3. Technical SEO

### Sitemap & Robots

```xml
<!-- public/sitemap.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2026-01-15</lastmod>
    <priority>1.0</priority>
  </url>
</urlset>
```

```txt
# public/robots.txt
User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin/
Sitemap: https://example.com/sitemap.xml
```

### Canonical URLs
- Every page needs a canonical tag (self-referencing for unique pages)
- Consistent www vs non-www, trailing slash, HTTP vs HTTPS
- Prevents duplicate content issues

### Redirects
- Use 301 for permanent redirects (passes SEO value)
- Fix redirect chains (A -> B -> C should be A -> C)
- Handle trailing slashes consistently

### Core Web Vitals
- **LCP** (Largest Contentful Paint): < 2.5s
- **INP** (Interaction to Next Paint): < 200ms
- **CLS** (Cumulative Layout Shift): < 0.1

## 4. Next.js SEO

### Static Metadata

```typescript
// app/page.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Page Title | Brand',
  description: 'Page description for search results',
  openGraph: {
    title: 'Page Title',
    description: 'OG description',
    images: [{ url: '/og-image.jpg', width: 1200, height: 630 }],
  },
  twitter: {
    card: 'summary_large_image',
  },
};
```

### Dynamic Metadata

```typescript
// app/products/[slug]/page.tsx
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const product = await getProduct(params.slug);
  return {
    title: `${product.name} | Brand`,
    description: product.description,
    openGraph: {
      images: [{ url: product.image }],
    },
  };
}
```

### JSON-LD in Next.js

```typescript
export default function ProductPage({ product }: Props) {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    image: product.image,
    offers: {
      '@type': 'Offer',
      price: product.price,
      priceCurrency: 'USD',
    },
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      {/* Page content */}
    </>
  );
}
```

## 5. Audit Checklist

### Before Launch
- [ ] Unique title tags on every page (50-60 chars)
- [ ] Meta descriptions on every page (150-160 chars)
- [ ] One H1 per page with primary keyword
- [ ] Open Graph tags on all shareable pages
- [ ] JSON-LD schema on key pages (Organization, Product, Article)
- [ ] Sitemap.xml generated and submitted
- [ ] Robots.txt allows important pages
- [ ] Canonical tags on all pages
- [ ] Alt text on all images
- [ ] Internal linking between related pages
- [ ] Core Web Vitals passing (LCP < 2.5s, INP < 200ms, CLS < 0.1)
- [ ] HTTPS across entire site
- [ ] Mobile-responsive design

### Validation Tools
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Schema.org Validator](https://validator.schema.org/)
- Google Search Console (Enhancements reports)
- Google PageSpeed Insights (Core Web Vitals)

### E-commerce Specifics
- [ ] Product schema on all product pages
- [ ] BreadcrumbList schema for navigation
- [ ] Category pages have unique content (not just product grids)
- [ ] Out-of-stock pages handled (not 404)
- [ ] Faceted navigation not creating duplicate URLs
