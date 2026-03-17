---
name: seo-meta
description: |
  Generate complete SEO meta tags for every page. Covers title patterns, meta descriptions, Open Graph, Twitter Cards, and JSON-LD structured data (LocalBusiness, Service, FAQ, BreadcrumbList).

  Use when: building pages, adding social sharing, implementing structured data, optimizing for search engines.
license: MIT
metadata:
  keywords:
    - seo
    - meta-tags
    - open-graph
    - twitter-cards
    - structured-data
    - json-ld
    - schema-org
  last_updated: 2026-01-14
  version: 1.0.0
---

# SEO Meta Tags

**Status**: Production Ready ✅
**Last Updated**: 2026-01-14
**Source**: Schema.org, Open Graph Protocol, Twitter Developer Docs

---

## Quick Start

Every page needs:

```tsx
<head>
  {/* Basic SEO */}
  <title>Service in Location | Brand Name</title>
  <meta name="description" content="Value prop. Differentiator. Call to action." />
  <link rel="canonical" href="https://example.com/page" />

  {/* Open Graph */}
  <meta property="og:title" content="Service in Location" />
  <meta property="og:description" content="Value prop. Differentiator. CTA." />
  <meta property="og:image" content="https://example.com/og-image.jpg" />
  <meta property="og:url" content="https://example.com/page" />
  <meta property="og:type" content="website" />

  {/* Twitter Card */}
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="Service in Location" />
  <meta name="twitter:description" content="Value prop. Differentiator. CTA." />
  <meta name="twitter:image" content="https://example.com/og-image.jpg" />

  {/* JSON-LD Structured Data */}
  <script type="application/ld+json">
    {JSON.stringify({
      "@context": "https://schema.org",
      "@type": "LocalBusiness",
      "name": "Business Name",
      "description": "What we do",
      "@id": "https://example.com",
      "url": "https://example.com",
      "telephone": "+61-XXX-XXX-XXX",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "123 Main St",
        "addressLocality": "Sydney",
        "addressRegion": "NSW",
        "postalCode": "2000",
        "addressCountry": "AU"
      }
    })}
  </script>
</head>
```

---

## Title Tag Patterns

**Character Limits**:
- Google: 50-60 characters (desktop), 78 (mobile)
- Social: 60-70 characters

**Page Type Formulas**:

| Page Type | Pattern | Example |
|-----------|---------|---------|
| Home | [Brand] - [Primary Service] in [Location] | Acme Plumbing - 24/7 Emergency Plumber Sydney |
| Service | [Service] in [Location] \| [Brand] | Hot Water Repairs Sydney \| Acme Plumbing |
| Location | [Service] [Suburb] \| [Brand] | Plumber Bondi \| Acme Plumbing |
| About | About [Brand] - [Tagline/USP] | About Acme - Licensed Plumbers Since 1995 |
| Contact | Contact [Brand] - [Location] \| [Phone] | Contact Acme Plumbing - Sydney \| 1300 XXX XXX |

**Title Modifiers** (add credibility):
- 24/7 Emergency
- Licensed & Insured
- Free Quotes
- Same Day Service
- Family Owned
- Award Winning

**Anti-Patterns** (avoid):
- ❌ "Welcome to..." (wastes characters)
- ❌ Keyword stuffing (plumber plumbing plumbers)
- ❌ ALL CAPS (looks spammy)
- ❌ Special characters (★ § ¶)

---

## Meta Description Patterns

**Character Limits**:
- Desktop: 155-160 characters
- Mobile: 120-130 characters

**Formula**:
```
[Value prop] [Service] in [Location]. [Differentiator]. [CTA].
```

**Examples by Page Type**:

**Home Page**:
```
Fast, reliable plumbing services in Sydney. 24/7 emergency response, licensed plumbers, upfront pricing. Call 1300 XXX XXX for same-day service.
```

**Service Page**:
```
Expert hot water repairs in Sydney. Fix or replace electric, gas & solar systems. Licensed technicians, 1-year warranty. Book online or call 1300 XXX XXX.
```

**Location Page**:
```
Trusted plumber in Bondi. Blocked drains, leaks, hot water, gas fitting. Same-day service, upfront quotes. Call your local plumber on 1300 XXX XXX.
```

**Power Words** (use sparingly):
- Trust: Licensed, Certified, Insured, Guaranteed, Trusted
- Speed: Fast, Quick, Same Day, Emergency, 24/7, Instant
- Value: Affordable, Competitive, Upfront, No Hidden Fees, Free Quote
- Local: Local, Nearby, Your Area, [Suburb Name]
- Quality: Expert, Professional, Experienced, Award Winning

---

## Open Graph Tags

**Required Tags**:

```html
<meta property="og:title" content="Service in Location" />
<meta property="og:description" content="Value prop. Differentiator. CTA." />
<meta property="og:image" content="https://example.com/og-image.jpg" />
<meta property="og:url" content="https://example.com/page" />
<meta property="og:type" content="website" />
```

**Image Requirements**:
- Dimensions: 1200x630px (1.91:1 ratio)
- Format: JPG or PNG (JPG preferred for file size)
- File size: <1MB (ideally <300KB)
- Text overlay: Keep important text center (safe zone: 1000x530)

**og:type Values by Page Type**:

| Page Type | og:type |
|-----------|---------|
| Home, Service, Location | website |
| Blog Post | article |
| Business Profile | business.business |

**Optional but Recommended**:
```html
<meta property="og:site_name" content="Brand Name" />
<meta property="og:locale" content="en_AU" />
```

---

## Twitter Cards

**Card Types**:

| Type | Use Case |
|------|----------|
| summary | Small square image (1:1), basic info |
| summary_large_image | Large image (1.91:1), most common |

**Required Tags**:

```html
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Service in Location" />
<meta name="twitter:description" content="Value prop. Differentiator. CTA." />
<meta name="twitter:image" content="https://example.com/og-image.jpg" />
```

**Optional**:
```html
<meta name="twitter:site" content="@yourbrand" />
<meta name="twitter:creator" content="@authorhandle" />
```

**Fallback Behavior**:
- If twitter:title missing, uses og:title
- If twitter:description missing, uses og:description
- If twitter:image missing, uses og:image

**Best Practice**: Define og:* tags first, only add twitter:* if values differ.

---

## JSON-LD Structured Data

### LocalBusiness Schema (Most Important)

Use for homepage and contact page:

```json
{
  "@context": "https://schema.org",
  "@type": "Plumber",
  "name": "Acme Plumbing",
  "description": "Licensed plumbing services in Sydney",
  "@id": "https://acmeplumbing.com.au",
  "url": "https://acmeplumbing.com.au",
  "logo": "https://acmeplumbing.com.au/logo.png",
  "image": "https://acmeplumbing.com.au/og-image.jpg",
  "telephone": "+61-XXX-XXX-XXX",
  "email": "info@acmeplumbing.com.au",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main Street",
    "addressLocality": "Sydney",
    "addressRegion": "NSW",
    "postalCode": "2000",
    "addressCountry": "AU"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": -33.8688,
    "longitude": 151.2093
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "07:00",
      "closes": "17:00"
    }
  ],
  "sameAs": [
    "https://facebook.com/acmeplumbing",
    "https://instagram.com/acmeplumbing"
  ]
}
```

**Specific Business Types** (instead of generic LocalBusiness):
- Plumber, Electrician, Locksmith, HVAC (HVACBusiness)
- Dentist, Attorney, Accountant
- Restaurant, Cafe, FoodEstablishment
- Store, AutoRepair, BeautySalon

### Service Schema

Use for service pages:

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Hot Water Repairs",
  "description": "Fast hot water system repairs in Sydney",
  "provider": {
    "@type": "Plumber",
    "name": "Acme Plumbing",
    "url": "https://acmeplumbing.com.au"
  },
  "areaServed": {
    "@type": "City",
    "name": "Sydney"
  },
  "availableChannel": {
    "@type": "ServiceChannel",
    "serviceUrl": "https://acmeplumbing.com.au/hot-water-repairs",
    "servicePhone": "+61-XXX-XXX-XXX"
  }
}
```

### FAQ Schema (Rich Snippets)

Use for FAQ sections:

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How much does a plumber cost in Sydney?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Plumbing rates in Sydney typically range from $100-$150 per hour for standard work. Emergency callouts may incur higher rates. We provide upfront quotes before starting work."
      }
    },
    {
      "@type": "Question",
      "name": "Do you offer same-day service?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, we offer same-day plumbing service across Sydney for urgent repairs. Call us before 2pm for same-day availability."
      }
    }
  ]
}
```

### BreadcrumbList Schema

Use on all pages except homepage:

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://acmeplumbing.com.au"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Services",
      "item": "https://acmeplumbing.com.au/services"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Hot Water Repairs",
      "item": "https://acmeplumbing.com.au/hot-water-repairs"
    }
  ]
}
```

---

## Canonical URLs

**When to Use**:
- Every page should have a self-referencing canonical
- Duplicate content (pagination, filters, print versions)
- Syndicated content
- Cross-domain duplicates

**Self-Referencing Canonical**:
```html
<!-- Always include, even if no duplicates -->
<link rel="canonical" href="https://example.com/page" />
```

**Pagination**:
```html
<!-- On page 2+ -->
<link rel="canonical" href="https://example.com/services" />
<!-- Not https://example.com/services?page=2 -->
```

**Common Mistakes**:
- ❌ Missing canonical (Google chooses for you)
- ❌ Relative URLs (use absolute URLs)
- ❌ Canonical pointing to different content
- ❌ Multiple canonicals (only one per page)

---

## Validation Tools

**Check Your Implementation**:

| Tool | Purpose | URL |
|------|---------|-----|
| Google Rich Results Test | Test structured data | search.google.com/test/rich-results |
| Schema Markup Validator | Validate JSON-LD | validator.schema.org |
| Facebook Debugger | Test Open Graph tags | developers.facebook.com/tools/debug |
| Twitter Card Validator | Test Twitter Cards | cards-dev.twitter.com/validator |
| Screaming Frog | Audit all pages | screamingfrog.co.uk/seo-spider |

**Browser Extensions**:
- SEO Meta in 1 Click (Chrome)
- META SEO inspector (Firefox)

---

## Quick Reference Checklist

For every page, include:

- [ ] `<title>` (50-60 chars, unique per page)
- [ ] `<meta name="description">` (150-160 chars, unique per page)
- [ ] `<link rel="canonical">` (absolute URL)
- [ ] Open Graph tags (og:title, og:description, og:image, og:url, og:type)
- [ ] Twitter Card tags (twitter:card, twitter:title, twitter:description, twitter:image)
- [ ] JSON-LD structured data (LocalBusiness on homepage, Service on service pages)
- [ ] BreadcrumbList schema (all pages except homepage)
- [ ] Mobile viewport meta tag
- [ ] Charset meta tag (UTF-8)

**Never**:
- ❌ Duplicate titles across pages
- ❌ Use "Welcome to..." in titles
- ❌ Omit og:image (critical for social sharing)
- ❌ Use generic @type (LocalBusiness instead of Plumber)
- ❌ Skip CTA in meta description

---

## Error Prevention

### Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| No rich snippets in search | Invalid JSON-LD | Use validator.schema.org, check commas/quotes |
| Social share shows wrong image | og:image missing or wrong size | Use 1200x630px, test with Facebook Debugger |
| Title truncated in search | Too long | Keep under 60 chars |
| Description truncated | Too long | Keep under 160 chars |
| Multiple pages rank for same keyword | Duplicate titles | Make each title unique |

### Testing Workflow

1. **Validate HTML**: Use W3C validator
2. **Test Structured Data**: Google Rich Results Test
3. **Test Social Sharing**: Facebook Debugger + Twitter Card Validator
4. **Mobile Preview**: Google Search Console URL Inspection
5. **Cross-Browser Check**: Test meta rendering in Chrome/Firefox/Safari

---

## Best Practices Summary

**Title Tags**:
- 50-60 characters maximum
- Include primary keyword + location + brand
- Unique for every page
- Use modifiers (24/7, Licensed, Free) sparingly

**Meta Descriptions**:
- 150-160 characters maximum
- Include value prop + differentiator + CTA
- Write for humans, not search engines
- Every page needs unique description

**Open Graph**:
- Always include og:image (1200x630px)
- Use absolute URLs
- Keep og:title under 60 chars
- Test with Facebook Debugger before launch

**JSON-LD**:
- Use specific @type (Plumber, not LocalBusiness)
- Include all contact info (phone, address, email)
- Add openingHoursSpecification for better display
- Validate with schema.org validator

**Canonical URLs**:
- Every page needs canonical
- Always use absolute URLs
- Self-referencing is good practice
- Only one canonical per page

---

**Production Notes**:
- Use react-helmet-async for React apps (SSR-safe)
- Generate JSON-LD dynamically from CMS/database
- Cache meta tag components for performance
- Monitor Search Console for indexing issues
- Update structured data when business details change
