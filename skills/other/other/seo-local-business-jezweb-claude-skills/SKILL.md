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

Fill placeholders in this template:

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- Primary Meta Tags -->
  <title>{{PAGE_TITLE}} | {{BUSINESS_NAME}}</title>
  <meta name="title" content="{{PAGE_TITLE}} | {{BUSINESS_NAME}}">
  <meta name="description" content="{{META_DESCRIPTION}}">

  <!-- Canonical URL -->
  <link rel="canonical" href="{{CANONICAL_URL}}">

  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="{{CANONICAL_URL}}">
  <meta property="og:title" content="{{PAGE_TITLE}} | {{BUSINESS_NAME}}">
  <meta property="og:description" content="{{META_DESCRIPTION}}">
  <meta property="og:image" content="{{OG_IMAGE_URL}}">

  <!-- Twitter -->
  <meta property="twitter:card" content="summary_large_image">
  <meta property="twitter:url" content="{{CANONICAL_URL}}">
  <meta property="twitter:title" content="{{PAGE_TITLE}} | {{BUSINESS_NAME}}">
  <meta property="twitter:description" content="{{META_DESCRIPTION}}">
  <meta property="twitter:image" content="{{OG_IMAGE_URL}}">

  <!-- Geo Tags (Local SEO) -->
  <meta name="geo.region" content="{{GEO_REGION}}">
  <meta name="geo.placename" content="{{CITY}}">
  <meta name="geo.position" content="{{LATITUDE}};{{LONGITUDE}}">
  <meta name="ICBM" content="{{LATITUDE}}, {{LONGITUDE}}">

  <!-- Favicons -->
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">

  <!-- Structured Data -->
  <script type="application/ld+json">
    {{JSON_LD_SCHEMA}}
  </script>
</head>
```

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

Use `LocalBusiness` or a more specific subtype:

| Subtype | Use for |
|---------|---------|
| `Plumber` | Plumbing services |
| `Electrician` | Electrical services |
| `RoofingContractor` | Roofing |
| `HVACBusiness` | Air conditioning/heating |
| `AutoRepair` | Mechanics |
| `BeautySalon` | Hair/beauty |
| `Dentist` | Dental practices |
| `LegalService` | Law firms |
| `AccountingService` | Accountants |
| `RealEstateAgent` | Real estate |
| `Restaurant` | Restaurants/cafes |
| `BarOrPub` | Pubs/bars |
| `Hotel` | Accommodation |
| `Store` | Retail shops |
| `ProfessionalService` | Generic professional |

LocalBusiness schema properties:

| Property | Required | Notes |
|----------|----------|-------|
| `@type` | Yes | `LocalBusiness` or subtype from above |
| `name` | Yes | Business name as shown to customers |
| `image` | Yes | Primary business image or logo |
| `description` | Yes | 1-2 sentence business description |
| `@id` | Yes | Unique ID, use `{url}/#organization` |
| `url` | Yes | Website homepage URL |
| `telephone` | Yes | International format: `+61-2-4900-1234` |
| `address` | Yes | PostalAddress (see below) |
| `email` | Recommended | Primary contact email |
| `priceRange` | Recommended | `$` to `$$$$` |
| `geo` | Recommended | GeoCoordinates: latitude/longitude |
| `openingHoursSpecification` | Recommended | See hours format below |
| `areaServed` | Recommended | Cities/suburbs served |
| `sameAs` | Recommended | Social media profile URLs |
| `taxID` | Optional | ABN for Australian businesses |
| `logo` | Optional | Business logo URL |
| `foundingDate` | Optional | ISO 8601 date |
| `paymentAccepted` | Optional | e.g. "Cash, Credit Card, EFTPOS" |
| `currenciesAccepted` | Optional | `AUD` |

PostalAddress:

| Property | Example |
|----------|---------|
| `streetAddress` | `123 Hunter Street` |
| `addressLocality` | `Newcastle` |
| `addressRegion` | `NSW` |
| `postalCode` | `2300` |
| `addressCountry` | `AU` |

Example:

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
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Saturday"],
      "opens": "08:00",
      "closes": "12:00"
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

| Property | Required | Notes |
|----------|----------|-------|
| `name` | Yes | Service name |
| `description` | Yes | What the service provides |
| `provider` | Yes | `{ "@id": "{url}/#organization" }` |
| `areaServed` | Recommended | City or region |
| `serviceType` | Recommended | Category of service |
| `offers` | Optional | Pricing/availability |

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

**robots.txt:**

```
User-agent: *
Allow: /

Sitemap: {{SITE_URL}}/sitemap.xml
```

**sitemap.xml:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{{SITE_URL}}/</loc>
    <lastmod>{{DATE}}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <!-- Add one <url> per page. Priority: 1.0 homepage, 0.8 services, 0.6 others -->
</urlset>
```

### Step 5: Validate

Test structured data at: https://validator.schema.org/

Common validation errors:
- Missing `@context` — every JSON-LD block needs it
- Wrong phone format — must be international (`+61-...`)
- Missing `@id` — needed for cross-referencing between schemas
- Empty `areaServed` — include at least one city

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

### Australian State Codes

| State | Code | Geo Region |
|-------|------|------------|
| New South Wales | NSW | AU-NSW |
| Victoria | VIC | AU-VIC |
| Queensland | QLD | AU-QLD |
| South Australia | SA | AU-SA |
| Western Australia | WA | AU-WA |
| Tasmania | TAS | AU-TAS |
| Northern Territory | NT | AU-NT |
| ACT | ACT | AU-ACT |

### Service Areas

Use `areaServed` with Australian city and suburb names (see LocalBusiness example above).
