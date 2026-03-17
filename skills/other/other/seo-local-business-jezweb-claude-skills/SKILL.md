---
name: seo-local-business
description: "Generate complete SEO setup for local business websites — HTML head tags, JSON-LD LocalBusiness schema, robots.txt, sitemap.xml. Australian-optimised with +61 phone, ABN, suburb patterns."
---

# SEO Local Business

Generate a complete SEO package for local business websites. Produces meta tags, structured data, robots.txt, and sitemap.xml.

## What You Produce

1. Complete `<head>` section with meta tags, Open Graph, Twitter Cards
2. JSON-LD structured data (LocalBusiness + Service + FAQ schemas)
3. `robots.txt`
4. `sitemap.xml`

## Workflow

### Step 1: Gather Business Info

Ask for (or extract from existing site):

| Required | Optional |
|----------|----------|
| Business name | ABN |
| Primary service | Opening hours |
| Location (city/suburb) | Social media URLs |
| Phone number | Price range |
| Website URL | Service areas (suburbs) |
| Business description | GPS coordinates |

### Step 2: Generate Head Tags

Use `assets/head-template.html` as your base. Fill in all placeholders.

**Title tag patterns** (50-60 chars max):

| Page | Pattern | Example |
|------|---------|---------|
| Homepage | `Brand - Tagline` | `Newcastle Plumbing - 24/7 Emergency Service` |
| Service | `Service in Location \| Brand` | `Hot Water Repairs Newcastle \| ABC Plumbing` |
| About | `About Us \| Brand` | `About Us \| ABC Plumbing Newcastle` |
| Contact | `Contact \| Brand` | `Contact Us \| ABC Plumbing Newcastle` |

**Meta description patterns** (150-160 chars):

| Page | Pattern |
|------|---------|
| Homepage | `[USP]. [Service] in [Location]. [CTA]. Call [phone].` |
| Service | `Professional [service] in [location]. [Benefit]. [Trust signal]. Get a free quote today.` |
| About | `[X] years serving [location]. [Team info]. [Credentials]. Learn about [brand].` |
| Contact | `Contact [brand] for [service] in [location]. [Hours]. Call [phone] or request a quote online.` |

### Step 3: Generate Structured Data

**LocalBusiness** (homepage — always include):

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "ABC Plumbing Newcastle",
  "image": "https://www.abcplumbing.com.au/og-image.jpg",
  "description": "Professional plumbing services in Newcastle and Lake Macquarie.",
  "@id": "https://www.abcplumbing.com.au/#organization",
  "url": "https://www.abcplumbing.com.au",
  "telephone": "+61-2-4900-1234",
  "email": "info@abcplumbing.com.au",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Hunter Street",
    "addressLocality": "Newcastle",
    "addressRegion": "NSW",
    "postalCode": "2300",
    "addressCountry": "AU"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": -32.9283,
    "longitude": 151.7817
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "07:00",
      "closes": "17:00"
    }
  ],
  "areaServed": [
    { "@type": "City", "name": "Newcastle" },
    { "@type": "City", "name": "Lake Macquarie" }
  ],
  "sameAs": [
    "https://www.facebook.com/abcplumbing",
    "https://www.instagram.com/abcplumbing"
  ]
}
```

**Service** (service pages — add per service):

```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Hot Water System Installation",
  "description": "Professional hot water system installation and replacement in Newcastle.",
  "provider": { "@id": "https://www.abcplumbing.com.au/#organization" },
  "areaServed": { "@type": "City", "name": "Newcastle" },
  "serviceType": "Plumbing",
  "offers": {
    "@type": "Offer",
    "availability": "https://schema.org/InStock",
    "priceRange": "$$"
  }
}
```

**FAQ** (pages with FAQ sections):

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How much does a plumber cost in Newcastle?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Plumber callout fees in Newcastle typically range from $80-150."
      }
    }
  ]
}
```

### Step 4: Generate robots.txt and sitemap.xml

Use `assets/robots-template.txt` and `assets/sitemap-template.xml`. Populate with all site pages.

### Step 5: Validate

Test structured data at: https://validator.schema.org/

## Australian-Specific Patterns

### Phone Numbers

```html
<!-- Link: international format. Display: local format. -->
<a href="tel:+61249001234">(02) 4900 1234</a>
```

Schema telephone: `"+61-2-4900-1234"`

| Prefix | International |
|--------|---------------|
| 02 | +612 |
| 04 | +614 |
| 1300 | Keep as-is |

### ABN

Add to LocalBusiness schema when available:

```json
{ "taxID": "12 345 678 901" }
```

### Service Areas

Use Australian city and suburb names:

```json
"areaServed": [
  { "@type": "City", "name": "Newcastle" },
  { "@type": "City", "name": "Maitland" },
  { "@type": "City", "name": "Lake Macquarie" }
]
```

### Geo Tags

Include state-specific geo meta tags:

```html
<meta name="geo.region" content="AU-NSW">
<meta name="geo.placename" content="Newcastle">
<meta name="geo.position" content="-32.9283;151.7817">
<meta name="ICBM" content="-32.9283, 151.7817">
```

See `references/schema-properties.md` for the full list of LocalBusiness and Service schema properties.
