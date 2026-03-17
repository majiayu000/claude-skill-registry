---
name: generating-seo-metadata
description: Generates SEO meta tags, Open Graph cards, and JSON-LD structured data. Use when the user asks about meta tags, og:image, schema.org markup, hreflang, or wants to improve search visibility.
---

# SEO Metadata Generator

## When to use this skill

- User asks to add meta tags to a page
- User mentions Open Graph or social sharing
- User wants JSON-LD or structured data
- User asks about hreflang or internationalization
- User wants to improve SEO or search visibility

## Workflow

- [ ] Identify page type and intent
- [ ] Generate base meta tags
- [ ] Create Open Graph tags
- [ ] Add Twitter Card meta
- [ ] Generate JSON-LD structured data
- [ ] Add hreflang if multilingual
- [ ] Validate output

## Instructions

### Step 1: Identify Page Type

Determine content type to select appropriate schema:

| Page Type    | JSON-LD Schema             | Priority Meta         |
| ------------ | -------------------------- | --------------------- |
| Homepage     | Organization, WebSite      | Brand, description    |
| Article/Blog | Article, BlogPosting       | Author, date, image   |
| Product      | Product, Offer             | Price, availability   |
| Service      | Service, LocalBusiness     | Provider, area        |
| FAQ          | FAQPage                    | Questions             |
| Event        | Event                      | Date, location, price |
| Person/About | Person, ProfilePage        | Name, role            |
| Contact      | ContactPage, LocalBusiness | Address, phone        |

### Step 2: Generate Base Meta Tags

**Essential meta tags:**

```html
<head>
  <!-- Primary Meta -->
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{Page Title} | {Site Name}</title>
  <meta name="description" content="{150-160 char description}" />

  <!-- Indexing Control -->
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://example.com/page-url" />

  <!-- Optional -->
  <meta name="author" content="{Author Name}" />
  <meta name="keywords" content="{keyword1, keyword2, keyword3}" />
</head>
```

**Title guidelines:**

- 50-60 characters max
- Primary keyword near the start
- Include brand name with separator
- Unique per page

**Description guidelines:**

- 150-160 characters
- Include primary keyword naturally
- Call to action when appropriate
- Unique per page

### Step 3: Open Graph Tags

**Core Open Graph:**

```html
<!-- Open Graph -->
<meta property="og:type" content="website" />
<meta property="og:url" content="https://example.com/page" />
<meta property="og:title" content="{Title for social sharing}" />
<meta property="og:description" content="{Description for social sharing}" />
<meta property="og:image" content="https://example.com/og-image.jpg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="{Image description}" />
<meta property="og:site_name" content="{Site Name}" />
<meta property="og:locale" content="en_US" />
```

**Article-specific:**

```html
<meta property="og:type" content="article" />
<meta property="article:published_time" content="2026-01-18T10:00:00Z" />
<meta property="article:modified_time" content="2026-01-18T12:00:00Z" />
<meta property="article:author" content="https://example.com/author" />
<meta property="article:section" content="Technology" />
<meta property="article:tag" content="JavaScript" />
```

**Product-specific:**

```html
<meta property="og:type" content="product" />
<meta property="product:price:amount" content="29.99" />
<meta property="product:price:currency" content="USD" />
<meta property="product:availability" content="in stock" />
```

### Step 4: Twitter Card Meta

```html
<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:site" content="@sitehandle" />
<meta name="twitter:creator" content="@authorhandle" />
<meta name="twitter:title" content="{Title}" />
<meta name="twitter:description" content="{Description}" />
<meta name="twitter:image" content="https://example.com/twitter-image.jpg" />
<meta name="twitter:image:alt" content="{Image description}" />
```

**Card types:**

- `summary`: Small square image
- `summary_large_image`: Large rectangular image
- `player`: Video/audio embed
- `app`: App install card

### Step 5: JSON-LD Structured Data

**Article schema:**

```html
<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Article Title Here",
    "description": "Article description",
    "image": "https://example.com/image.jpg",
    "author": {
      "@type": "Person",
      "name": "Author Name",
      "url": "https://example.com/author"
    },
    "publisher": {
      "@type": "Organization",
      "name": "Site Name",
      "logo": {
        "@type": "ImageObject",
        "url": "https://example.com/logo.png"
      }
    },
    "datePublished": "2026-01-18",
    "dateModified": "2026-01-18"
  }
</script>
```

**Product schema:**

```html
<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Product",
    "name": "Product Name",
    "description": "Product description",
    "image": "https://example.com/product.jpg",
    "brand": {
      "@type": "Brand",
      "name": "Brand Name"
    },
    "offers": {
      "@type": "Offer",
      "url": "https://example.com/product",
      "priceCurrency": "USD",
      "price": "29.99",
      "availability": "https://schema.org/InStock",
      "seller": {
        "@type": "Organization",
        "name": "Store Name"
      }
    },
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": "4.5",
      "reviewCount": "42"
    }
  }
</script>
```

**FAQ schema:**

```html
<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "What is the question?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "This is the answer."
        }
      }
    ]
  }
</script>
```

**LocalBusiness schema:**

```html
<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "Business Name",
    "image": "https://example.com/photo.jpg",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "123 Main St",
      "addressLocality": "City",
      "addressRegion": "State",
      "postalCode": "12345",
      "addressCountry": "US"
    },
    "telephone": "+1-555-555-5555",
    "openingHoursSpecification": {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "09:00",
      "closes": "17:00"
    }
  }
</script>
```

**BreadcrumbList schema:**

```html
<script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {
        "@type": "ListItem",
        "position": 1,
        "name": "Home",
        "item": "https://example.com"
      },
      {
        "@type": "ListItem",
        "position": 2,
        "name": "Category",
        "item": "https://example.com/category"
      },
      {
        "@type": "ListItem",
        "position": 3,
        "name": "Current Page"
      }
    ]
  }
</script>
```

### Step 6: Hreflang for Multilingual Sites

```html
<!-- Language alternates -->
<link rel="alternate" hreflang="en" href="https://example.com/page" />
<link rel="alternate" hreflang="nl" href="https://example.nl/pagina" />
<link rel="alternate" hreflang="de" href="https://example.de/seite" />
<link rel="alternate" hreflang="x-default" href="https://example.com/page" />
```

**Common hreflang codes:**
| Language | Code | With Region |
|----------|------|-------------|
| English | `en` | `en-US`, `en-GB` |
| Dutch | `nl` | `nl-NL`, `nl-BE` |
| German | `de` | `de-DE`, `de-AT` |
| French | `fr` | `fr-FR`, `fr-CA` |
| Spanish | `es` | `es-ES`, `es-MX` |

### Framework Integration

**Next.js (App Router):**

```tsx
// app/page.tsx
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Page Title | Site Name",
  description: "Page description here",
  openGraph: {
    title: "OG Title",
    description: "OG Description",
    url: "https://example.com/page",
    siteName: "Site Name",
    images: [
      {
        url: "https://example.com/og.jpg",
        width: 1200,
        height: 630,
        alt: "Image alt",
      },
    ],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Twitter Title",
    description: "Twitter description",
    images: ["https://example.com/twitter.jpg"],
  },
  alternates: {
    canonical: "https://example.com/page",
    languages: {
      en: "https://example.com/page",
      nl: "https://example.nl/pagina",
    },
  },
};
```

**Next.js JSON-LD:**

```tsx
// app/page.tsx
export default function Page() {
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: "Article Title",
    // ... rest of schema
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

**Nuxt 3:**

```vue
<script setup lang="ts">
  useSeoMeta({
    title: "Page Title",
    description: "Page description",
    ogTitle: "OG Title",
    ogDescription: "OG Description",
    ogImage: "https://example.com/og.jpg",
    ogUrl: "https://example.com/page",
    twitterCard: "summary_large_image",
  });

  useHead({
    link: [{ rel: "canonical", href: "https://example.com/page" }],
    script: [
      {
        type: "application/ld+json",
        children: JSON.stringify({
          "@context": "https://schema.org",
          "@type": "Article",
          // ... schema
        }),
      },
    ],
  });
</script>
```

## Validation

Before completing:

- [ ] Title under 60 characters
- [ ] Description 150-160 characters
- [ ] Canonical URL set
- [ ] OG image is 1200x630px
- [ ] JSON-LD validates at schema.org validator
- [ ] All URLs are absolute
- [ ] Hreflang includes x-default

**Validation tools:**

```bash
# Test JSON-LD locally
curl -s "https://validator.schema.org/" # Use web interface

# Check meta tags
curl -s https://example.com | grep -E '<meta|<title|<link rel="canonical"'
```

## Error Handling

- **Missing required fields**: JSON-LD requires certain fields per type; validate against schema.org.
- **Image dimensions wrong**: OG images must be at least 200x200, recommended 1200x630.
- **Duplicate canonical**: Only one canonical URL per page.
- **Hreflang loops**: Each language version must link to all others including itself.
- **Invalid dates**: Use ISO 8601 format (YYYY-MM-DD or full datetime).

## Resources

- [Schema.org Full Hierarchy](https://schema.org/docs/full.html)
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Open Graph Protocol](https://ogp.me/)
- [Twitter Cards Documentation](https://developer.twitter.com/en/docs/twitter-for-websites/cards)
