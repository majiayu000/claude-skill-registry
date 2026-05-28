---
name: structured-data-jsonld
description: "Implement JSON-LD structured data for Next.js applications using Schema.org vocabulary for rich results, Knowledge Graph entries, and enhanced search appearances. CRITICAL: Includes January 2026 Google Schema deprecations warning (5 types discontinued). Use when adding structured data, implementing rich results, validating Schema.org markup, or migrating deprecated schema types."
version: "2.0.0"
last_updated: "2026-01-12"
---

# Structured Data JSON-LD Skill

You are an expert in implementing JSON-LD structured data for Next.js 16 applications using Schema.org vocabulary. You help developers implement rich results, knowledge graph entries, and enhanced search appearances through proper structured data markup for maximum SEO impact.

## Core Knowledge

### What is Structured Data?

**Definition**: Machine-readable code that helps search engines understand your content.

**Format**: JSON-LD (JavaScript Object Notation for Linked Data) - recommended by Google.

**Purpose**:
- Enable **rich results** in Google Search (star ratings, images, prices, etc.)
- Populate **Knowledge Graph** panels
- Improve search result **CTR by 20-40%**
- Help search engines understand relationships between entities

**Critical Insight**: Structured data is the difference between:
```
❌ Plain search result:
   Blue Link
   yoursite.com/recipe
   2 lines of gray text...

✅ Rich result:
   ⭐⭐⭐⭐⭐ 4.8 (234 reviews)
   🕐 30 min  🍴 4 servings  🔥 320 cal
   [Large recipe image]
   Chocolate Chip Cookies Recipe
   The best chocolate chip cookies...
```

**Impact**: Pages with structured data get 20-40% higher CTR.

## ⚠️ CRITICAL: Google Schema.org Deprecations (January 2026)

**Impact**: Google discontinued support for 5 Schema.org types in January 2026. Using these types will not generate rich results and may cause validation warnings.

### Deprecated Schema Types

| Schema Type | Status | Replacement | Impact |
|-------------|--------|-------------|--------|
| **Practice Problem** | ❌ Discontinued | Use `LearningResource` or `Quiz` | No rich results for educational problems |
| **Dataset** | ⚠️ Limited Support | Limited to Google Dataset Search | Reduced visibility in general search |
| **Sitelinks Search Box** | ❌ Discontinued | Google generates automatically | No manual control over sitelinks |
| **SpecialAnnouncement** | ❌ Discontinued | Use `NewsArticle` or `Article` | No COVID/emergency announcement rich results |
| **Q&A** | ❌ Discontinued | Use `FAQPage` instead | No standalone Q&A rich results |

**Source**: [Schema Markup Guide 2026](https://almcorp.com/blog/schema-markup-detailed-guide-2026-serp-visibility/)

### Migration Guide

#### 1. Practice Problem → LearningResource

```typescript
// ❌ OLD: PracticeProblem (discontinued)
const oldSchema = {
  '@context': 'https://schema.org',
  '@type': 'PracticeProblem',
  name: 'Algebra Problem Set',
  educationalLevel: 'High School',
};

// ✅ NEW: LearningResource
import { LearningResource, WithContext } from 'schema-dts';

const newSchema: WithContext<LearningResource> = {
  '@context': 'https://schema.org',
  '@type': 'LearningResource',
  learningResourceType: 'Problem Set',
  name: 'Algebra Problem Set',
  educationalLevel: 'High School',
  educationalUse: 'Practice',
  about: {
    '@type': 'Thing',
    name: 'Algebra',
  },
};
```

#### 2. Q&A → FAQPage

```typescript
// ❌ OLD: QAPage (discontinued)
const oldSchema = {
  '@context': 'https://schema.org',
  '@type': 'QAPage',
  mainEntity: {
    '@type': 'Question',
    name: 'How do I reset my password?',
    acceptedAnswer: {
      '@type': 'Answer',
      text: 'Click Forgot Password...',
    },
  },
};

// ✅ NEW: FAQPage (supports multiple Q&A pairs)
import { FAQPage, WithContext } from 'schema-dts';

const newSchema: WithContext<FAQPage> = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: [
    {
      '@type': 'Question',
      name: 'How do I reset my password?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Click Forgot Password on the login page, enter your email, and follow the instructions sent to your inbox.',
      },
    },
    {
      '@type': 'Question',
      name: 'How long does password reset take?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Password reset emails are sent instantly. Check your spam folder if you don\'t see it within 5 minutes.',
      },
    },
  ],
};
```

#### 3. SpecialAnnouncement → NewsArticle

```typescript
// ❌ OLD: SpecialAnnouncement (discontinued)
const oldSchema = {
  '@context': 'https://schema.org',
  '@type': 'SpecialAnnouncement',
  name: 'Service Maintenance Update',
  text: 'Our platform will undergo maintenance on January 15th.',
  datePosted: '2026-01-10',
};

// ✅ NEW: NewsArticle or Article
import { NewsArticle, WithContext } from 'schema-dts';

const newSchema: WithContext<NewsArticle> = {
  '@context': 'https://schema.org',
  '@type': 'NewsArticle',
  headline: 'Service Maintenance Update',
  articleBody: 'Our platform will undergo maintenance on January 15th from 2-4am PST. All services will be temporarily unavailable during this time.',
  datePublished: '2026-01-10T08:00:00Z',
  dateModified: '2026-01-10T08:00:00Z',
  author: {
    '@type': 'Organization',
    name: 'Acme Engineering Team',
  },
  publisher: {
    '@type': 'Organization',
    name: 'Acme Company',
    logo: {
      '@type': 'ImageObject',
      url: 'https://acme.com/logo.png',
    },
  },
};
```

#### 4. Sitelinks Search Box → Remove

```typescript
// ❌ OLD: Sitelinks Search Box (discontinued)
const oldSchema = {
  '@context': 'https://schema.org',
  '@type': 'WebSite',
  url: 'https://acme.com',
  potentialAction: {
    '@type': 'SearchAction',
    target: {
      '@type': 'EntryPoint',
      urlTemplate: 'https://acme.com/search?q={search_term_string}',
    },
    'query-input': 'required name=search_term_string',
  },
};

// ✅ NEW: Remove SearchAction, Google generates automatically
import { WebSite, WithContext } from 'schema-dts';

const newSchema: WithContext<WebSite> = {
  '@context': 'https://schema.org',
  '@type': 'WebSite',
  name: 'Acme Company',
  url: 'https://acme.com',
  description: 'Enterprise-grade development tools',
  // Google will automatically generate sitelinks based on:
  // 1. Site structure and navigation
  // 2. Internal linking patterns
  // 3. User engagement data
  // No manual SearchAction needed
};
```

#### 5. Dataset → Use Sparingly

```typescript
// ⚠️ LIMITED: Dataset (only for Google Dataset Search)
import { Dataset, WithContext } from 'schema-dts';

const datasetSchema: WithContext<Dataset> = {
  '@context': 'https://schema.org',
  '@type': 'Dataset',
  name: 'Weather Observations 2025',
  description: 'Hourly weather data from 500+ meteorological stations across North America.',
  url: 'https://acme.com/datasets/weather-2025',

  // Dataset-specific properties
  temporalCoverage: '2025-01-01/2025-12-31',
  spatialCoverage: {
    '@type': 'Place',
    geo: {
      '@type': 'GeoShape',
      box: '18.0 -170.0 71.5 -66.0', // North America bounding box
    },
  },

  // Only appears in https://datasetsearch.research.google.com/
  // Not in general Google Search results
  // Use only if targeting dataset-specific search tools
};
```

### Audit Your Existing Schemas

**Check for deprecated types**:

```bash
# Search for deprecated schema types in your codebase
grep -r "PracticeProblem\|QAPage\|SpecialAnnouncement\|SearchAction\|'Dataset'" apps/web/app/

# Check all JSON-LD script tags
grep -r "application/ld+json" apps/web/app/ -A 20 | grep "@type"
```

**Validation checklist**:
- [ ] No `PracticeProblem` types (use `LearningResource` instead)
- [ ] No `QAPage` types (use `FAQPage` instead)
- [ ] No `SpecialAnnouncement` types (use `NewsArticle`/`Article` instead)
- [ ] No `SearchAction` in `WebSite` types (remove, Google auto-generates)
- [ ] `Dataset` only used for dataset-specific tools (not general SEO)

### When to Update

- **Immediate**: If using any of the 5 deprecated types
- **Before deployment**: Validate all new structured data against [current Google support](https://developers.google.com/search/docs/appearance/structured-data/search-gallery)
- **Monthly audit**: Check [Google Search Console](https://search.google.com/search-console) for structured data errors
- **After Schema.org updates**: Review [Schema.org releases](https://schema.org/docs/releases.html) quarterly

### Testing Deprecated Schemas

```bash
# Test with Google Rich Results Test
# URL: https://search.google.com/test/rich-results

# Deprecated types will show warnings:
# ⚠️ "This feature is no longer eligible for rich results"
# ⚠️ "Google does not support this schema type"

# Validate with Schema.org validator
# URL: https://validator.schema.org/
# Note: Schema.org validator may still pass, but Google won't use it
```

---

## JSON-LD Basics

### Basic Implementation in Next.js

```typescript
// app/page.tsx
export default function HomePage() {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: 'Acme Company',
    url: 'https://acme.com',
    logo: 'https://acme.com/logo.png',
    sameAs: [
      'https://twitter.com/acmecompany',
      'https://facebook.com/acmecompany',
      'https://linkedin.com/company/acmecompany',
    ],
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <main>{/* Page content */}</main>
    </>
  );
}
```

### XSS Security (CRITICAL)

**Problem**: JSON.stringify can create XSS vulnerabilities.

**Solution**: Sanitize `<` characters.

```typescript
// ✅ SAFE: Replace < with unicode
function sanitizeJsonLd(obj: object) {
  return JSON.stringify(obj).replace(/</g, '\\u003c');
}

// Usage:
<script
  type="application/ld+json"
  dangerouslySetInnerHTML={{ __html: sanitizeJsonLd(jsonLd) }}
/>

// Alternative: Use serialize-javascript library
import serialize from 'serialize-javascript';

<script
  type="application/ld+json"
  dangerouslySetInnerHTML={{ __html: serialize(jsonLd) }}
/>
```

### TypeScript Support (schema-dts)

**Installation**:
```bash
pnpm add schema-dts
```

**Usage**:
```typescript
import { Organization, WithContext } from 'schema-dts';

const jsonLd: WithContext<Organization> = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  name: 'Acme Company',
  url: 'https://acme.com',
  logo: 'https://acme.com/logo.png',
};
```

**Benefits**:
- Type checking for all Schema.org properties
- Autocomplete in IDE
- Prevents typos and invalid properties

## Common Schema Types

### Organization

**Use For**: Company homepage, about page.

```typescript
import { Organization, WithContext } from 'schema-dts';

const jsonLd: WithContext<Organization> = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  name: 'Acme Company',
  alternateName: 'Acme',
  url: 'https://acme.com',
  logo: 'https://acme.com/logo.png',
  description: 'Enterprise-grade development tools for modern teams.',

  // Contact info
  email: 'contact@acme.com',
  telephone: '+1-555-123-4567',

  // Address
  address: {
    '@type': 'PostalAddress',
    streetAddress: '123 Main Street',
    addressLocality: 'San Francisco',
    addressRegion: 'CA',
    postalCode: '94105',
    addressCountry: 'US',
  },

  // Social profiles
  sameAs: [
    'https://twitter.com/acmecompany',
    'https://facebook.com/acmecompany',
    'https://linkedin.com/company/acmecompany',
    'https://github.com/acmecompany',
    'https://instagram.com/acmecompany',
  ],

  // Founder
  founder: {
    '@type': 'Person',
    name: 'John Doe',
  },

  // Founding date
  foundingDate: '2020-01-15',
};
```

### Article (Blog Posts)

**Use For**: Blog posts, news articles, editorial content.

```typescript
import { Article, WithContext } from 'schema-dts';

const jsonLd: WithContext<Article> = {
  '@context': 'https://schema.org',
  '@type': 'Article',
  headline: 'How to Build a SaaS App in 2026',
  description: 'Complete guide to building scalable SaaS applications with Next.js.',

  // Images (required for rich results)
  image: [
    'https://acme.com/blog/saas-guide-1x1.jpg', // 1:1 aspect ratio
    'https://acme.com/blog/saas-guide-4x3.jpg', // 4:3 aspect ratio
    'https://acme.com/blog/saas-guide-16x9.jpg', // 16:9 aspect ratio
  ],

  // Dates
  datePublished: '2026-01-10T08:00:00+00:00',
  dateModified: '2026-01-10T12:00:00+00:00',

  // Author
  author: {
    '@type': 'Person',
    name: 'Jane Smith',
    url: 'https://acme.com/authors/jane-smith',
  },

  // Publisher (required)
  publisher: {
    '@type': 'Organization',
    name: 'Acme Blog',
    logo: {
      '@type': 'ImageObject',
      url: 'https://acme.com/logo.png',
    },
  },

  // Article body (optional, but helpful)
  articleBody: 'Full article text...',

  // Word count (optional)
  wordCount: 2500,

  // URL
  url: 'https://acme.com/blog/how-to-build-saas-app',

  // Main entity of page
  mainEntityOfPage: {
    '@type': 'WebPage',
    '@id': 'https://acme.com/blog/how-to-build-saas-app',
  },
};
```

### Product (E-commerce)

**Use For**: Product pages.

```typescript
import { Product, WithContext } from 'schema-dts';

const jsonLd: WithContext<Product> = {
  '@context': 'https://schema.org',
  '@type': 'Product',
  name: 'Premium Widget Pro',
  description: 'The best widget on the market with advanced features.',

  // Images (multiple recommended)
  image: [
    'https://acme.com/products/widget-1.jpg',
    'https://acme.com/products/widget-2.jpg',
    'https://acme.com/products/widget-3.jpg',
  ],

  // SKU & Brand
  sku: 'WIDGET-PRO-001',
  mpn: 'WP-001', // Manufacturer Part Number
  brand: {
    '@type': 'Brand',
    name: 'Acme',
  },

  // Offers (required for rich results)
  offers: {
    '@type': 'Offer',
    url: 'https://acme.com/products/premium-widget-pro',
    priceCurrency: 'USD',
    price: 99.99,
    priceValidUntil: '2026-12-31',
    availability: 'https://schema.org/InStock', // or OutOfStock, PreOrder
    seller: {
      '@type': 'Organization',
      name: 'Acme Store',
    },
  },

  // Aggregate rating (if available)
  aggregateRating: {
    '@type': 'AggregateRating',
    ratingValue: 4.8,
    reviewCount: 234,
    bestRating: 5,
    worstRating: 1,
  },

  // Reviews (optional)
  review: [
    {
      '@type': 'Review',
      reviewRating: {
        '@type': 'Rating',
        ratingValue: 5,
        bestRating: 5,
      },
      author: {
        '@type': 'Person',
        name: 'John Customer',
      },
      reviewBody: 'Amazing product! Highly recommended.',
      datePublished: '2026-01-05',
    },
  ],
};
```

### Recipe

**Use For**: Food recipes.

```typescript
import { Recipe, WithContext } from 'schema-dts';

const jsonLd: WithContext<Recipe> = {
  '@context': 'https://schema.org',
  '@type': 'Recipe',
  name: 'Chocolate Chip Cookies',
  description: 'The best chocolate chip cookies you\'ll ever make!',

  // Images (required)
  image: ['https://acme.com/recipes/cookies.jpg'],

  // Author
  author: {
    '@type': 'Person',
    name: 'Chef Jane',
  },

  // Dates
  datePublished: '2026-01-10',

  // Time
  prepTime: 'PT15M', // 15 minutes (ISO 8601 duration)
  cookTime: 'PT15M', // 15 minutes
  totalTime: 'PT30M', // 30 minutes

  // Yield
  recipeYield: '24 cookies',

  // Category & Cuisine
  recipeCategory: 'Dessert',
  recipeCuisine: 'American',

  // Keywords
  keywords: 'chocolate chip, cookies, dessert, baking',

  // Nutrition (optional)
  nutrition: {
    '@type': 'NutritionInformation',
    calories: '320 calories',
    fatContent: '16g',
    sugarContent: '24g',
  },

  // Ingredients (required)
  recipeIngredient: [
    '2 1/4 cups all-purpose flour',
    '1 tsp baking soda',
    '1 tsp salt',
    '1 cup butter, softened',
    '3/4 cup granulated sugar',
    '3/4 cup brown sugar',
    '2 large eggs',
    '2 tsp vanilla extract',
    '2 cups chocolate chips',
  ],

  // Instructions (required)
  recipeInstructions: [
    {
      '@type': 'HowToStep',
      text: 'Preheat oven to 375°F (190°C).',
    },
    {
      '@type': 'HowToStep',
      text: 'Combine flour, baking soda, and salt in a bowl.',
    },
    {
      '@type': 'HowToStep',
      text: 'Beat butter and sugars until creamy. Add eggs and vanilla.',
    },
    {
      '@type': 'HowToStep',
      text: 'Gradually mix in flour mixture. Stir in chocolate chips.',
    },
    {
      '@type': 'HowToStep',
      text: 'Drop spoonfuls onto baking sheet and bake 9-11 minutes.',
    },
  ],

  // Aggregate rating
  aggregateRating: {
    '@type': 'AggregateRating',
    ratingValue: 4.9,
    reviewCount: 156,
  },
};
```

### FAQ Page

**Use For**: FAQ sections, Q&A pages.

```typescript
import { FAQPage, WithContext } from 'schema-dts';

const jsonLd: WithContext<FAQPage> = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: [
    {
      '@type': 'Question',
      name: 'What is your return policy?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'We offer a 30-day money-back guarantee on all products. If you\'re not satisfied, contact us for a full refund.',
      },
    },
    {
      '@type': 'Question',
      name: 'How long does shipping take?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Standard shipping takes 5-7 business days. Express shipping (2-3 days) is available for an additional fee.',
      },
    },
    {
      '@type': 'Question',
      name: 'Do you ship internationally?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Yes, we ship to over 50 countries worldwide. International shipping times vary by destination.',
      },
    },
  ],
};
```

### Event

**Use For**: Events, conferences, webinars.

```typescript
import { Event, WithContext } from 'schema-dts';

const jsonLd: WithContext<Event> = {
  '@context': 'https://schema.org',
  '@type': 'Event',
  name: 'Next.js Conf 2026',
  description: 'The official Next.js conference featuring talks from the core team and community.',

  // Image
  image: ['https://acme.com/events/nextjs-conf.jpg'],

  // Start & End dates (ISO 8601 format)
  startDate: '2026-10-25T09:00:00-07:00',
  endDate: '2026-10-26T18:00:00-07:00',

  // Status
  eventStatus: 'https://schema.org/EventScheduled', // or EventCancelled, EventPostponed
  eventAttendanceMode: 'https://schema.org/OfflineEventAttendanceMode', // or OnlineEventAttendanceMode, MixedEventAttendanceMode

  // Location
  location: {
    '@type': 'Place',
    name: 'Moscone Center',
    address: {
      '@type': 'PostalAddress',
      streetAddress: '747 Howard St',
      addressLocality: 'San Francisco',
      addressRegion: 'CA',
      postalCode: '94103',
      addressCountry: 'US',
    },
  },

  // Organizer
  organizer: {
    '@type': 'Organization',
    name: 'Vercel',
    url: 'https://vercel.com',
  },

  // Offers (tickets)
  offers: {
    '@type': 'Offer',
    url: 'https://acme.com/events/nextjs-conf/tickets',
    price: 299,
    priceCurrency: 'USD',
    availability: 'https://schema.org/InStock',
    validFrom: '2026-01-10T09:00:00-08:00',
  },

  // Performer (speakers)
  performer: [
    {
      '@type': 'Person',
      name: 'Lee Robinson',
    },
    {
      '@type': 'Person',
      name: 'Guillermo Rauch',
    },
  ],
};
```

### Local Business

**Use For**: Physical business locations (restaurants, stores, offices).

```typescript
import { LocalBusiness, WithContext } from 'schema-dts';

const jsonLd: WithContext<LocalBusiness> = {
  '@context': 'https://schema.org',
  '@type': 'Restaurant', // or Store, LocalBusiness, etc.
  name: 'Acme Cafe',
  description: 'Cozy cafe serving artisan coffee and homemade pastries.',

  // Images
  image: ['https://acme.com/cafe/interior.jpg'],

  // Contact
  telephone: '+1-555-987-6543',
  email: 'info@acmecafe.com',
  url: 'https://acmecafe.com',

  // Address
  address: {
    '@type': 'PostalAddress',
    streetAddress: '456 Market Street',
    addressLocality: 'San Francisco',
    addressRegion: 'CA',
    postalCode: '94102',
    addressCountry: 'US',
  },

  // Geo coordinates (for maps)
  geo: {
    '@type': 'GeoCoordinates',
    latitude: 37.7749,
    longitude: -122.4194,
  },

  // Opening hours
  openingHoursSpecification: [
    {
      '@type': 'OpeningHoursSpecification',
      dayOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
      opens: '07:00',
      closes: '19:00',
    },
    {
      '@type': 'OpeningHoursSpecification',
      dayOfWeek: ['Saturday', 'Sunday'],
      opens: '08:00',
      closes: '20:00',
    },
  ],

  // Price range
  priceRange: '$$',

  // Cuisine (for restaurants)
  servesCuisine: ['American', 'Coffee'],

  // Aggregate rating
  aggregateRating: {
    '@type': 'AggregateRating',
    ratingValue: 4.7,
    reviewCount: 89,
  },
};
```

### Breadcrumb

**Use For**: Breadcrumb navigation.

```typescript
import { BreadcrumbList, WithContext } from 'schema-dts';

const jsonLd: WithContext<BreadcrumbList> = {
  '@context': 'https://schema.org',
  '@type': 'BreadcrumbList',
  itemListElement: [
    {
      '@type': 'ListItem',
      position: 1,
      name: 'Home',
      item: 'https://acme.com',
    },
    {
      '@type': 'ListItem',
      position: 2,
      name: 'Blog',
      item: 'https://acme.com/blog',
    },
    {
      '@type': 'ListItem',
      position: 3,
      name: 'How to Build a SaaS App',
      item: 'https://acme.com/blog/how-to-build-saas-app',
    },
  ],
};
```

## Dynamic Structured Data

### Blog Post Example

```typescript
// app/blog/[slug]/page.tsx
import { Article, WithContext } from 'schema-dts';

export default async function BlogPostPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const post = await getBlogPost(slug);

  const jsonLd: WithContext<Article> = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: post.title,
    description: post.excerpt,
    image: [post.coverImage],
    datePublished: post.publishedAt,
    dateModified: post.updatedAt,
    author: {
      '@type': 'Person',
      name: post.author.name,
      url: `https://acme.com/authors/${post.author.slug}`,
    },
    publisher: {
      '@type': 'Organization',
      name: 'Acme Blog',
      logo: {
        '@type': 'ImageObject',
        url: 'https://acme.com/logo.png',
      },
    },
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <article>{/* Post content */}</article>
    </>
  );
}
```

### Product Page Example

```typescript
// app/products/[id]/page.tsx
import { Product, WithContext } from 'schema-dts';

export default async function ProductPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const product = await getProduct(id);

  const jsonLd: WithContext<Product> = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    description: product.description,
    image: product.images,
    sku: product.sku,
    brand: {
      '@type': 'Brand',
      name: product.brand,
    },
    offers: {
      '@type': 'Offer',
      url: `https://acme.com/products/${id}`,
      priceCurrency: 'USD',
      price: product.price,
      availability: product.inStock
        ? 'https://schema.org/InStock'
        : 'https://schema.org/OutOfStock',
    },
    aggregateRating: product.reviews?.count > 0 ? {
      '@type': 'AggregateRating',
      ratingValue: product.reviews.average,
      reviewCount: product.reviews.count,
    } : undefined,
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <main>{/* Product content */}</main>
    </>
  );
}
```

## Reusable Component Pattern

### StructuredData Component

```typescript
// components/structured-data.tsx
interface StructuredDataProps {
  data: object;
}

export function StructuredData({ data }: StructuredDataProps) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{
        __html: JSON.stringify(data).replace(/</g, '\\u003c'),
      }}
    />
  );
}

// Usage:
import { StructuredData } from '@/components/structured-data';

export default function Page() {
  const jsonLd = { '@context': 'https://schema.org', '@type': 'Organization', ... };

  return (
    <>
      <StructuredData data={jsonLd} />
      <main>Content</main>
    </>
  );
}
```

## Multiple Schemas on One Page

**Allowed**: One page can have multiple structured data blocks.

```typescript
export default function BlogPostPage() {
  const article = { '@context': 'https://schema.org', '@type': 'Article', ... };
  const breadcrumb = { '@context': 'https://schema.org', '@type': 'BreadcrumbList', ... };
  const faq = { '@context': 'https://schema.org', '@type': 'FAQPage', ... };

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(article) }} />
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumb) }} />
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(faq) }} />
      <article>{/* Content */}</article>
    </>
  );
}
```

## Validation & Testing

### Google Rich Results Test

**URL**: https://search.google.com/test/rich-results

**Use For**:
- Test if page is eligible for rich results
- Preview how rich results will appear
- Identify errors in structured data
- See which rich result features are detected

**How to Use**:
1. Enter URL or paste code
2. Click "Test URL" or "Test Code"
3. Review detected features
4. Fix any errors or warnings
5. Re-test after changes

### Schema Markup Validator

**URL**: https://validator.schema.org/

**Use For**:
- Validate JSON-LD syntax
- Check Schema.org compliance
- Identify property errors
- Verify schema structure

**How to Use**:
1. Paste JSON-LD code
2. Click "Run Test"
3. Review errors and warnings
4. Fix issues
5. Re-validate

### View Source Check

**Quick Validation**:
```bash
# View page source
curl https://your-site.com/page | grep 'application/ld+json'

# Or in browser: view-source:https://your-site.com/page
# Look for <script type="application/ld+json">
```

## Common Issues

### Issue: Rich Results Not Showing

**Possible Causes**:
1. Structured data has errors
2. Missing required properties
3. Google hasn't re-crawled page
4. Page doesn't meet quality guidelines

**Solution**:
- Use Rich Results Test to validate
- Fix all errors and warnings
- Request re-indexing in Google Search Console
- Ensure content quality meets Google standards
- Wait (rich results can take days/weeks to appear)

### Issue: Invalid JSON-LD Syntax

**Problem**: JSON-LD contains syntax errors.

**Common Mistakes**:
```typescript
// ❌ Missing quotes on property names
{ @context: 'https://schema.org' }

// ✅ Correct
{ '@context': 'https://schema.org' }

// ❌ Trailing comma
{ name: 'Acme', url: 'https://acme.com', }

// ✅ Correct
{ name: 'Acme', url: 'https://acme.com' }
```

### Issue: XSS Vulnerability

**Problem**: User-generated content in JSON-LD creates XSS risk.

**Solution**: Sanitize `<` characters.

```typescript
// ✅ Safe
function sanitizeJsonLd(obj: object) {
  return JSON.stringify(obj).replace(/</g, '\\u003c');
}
```

## Best Practices

### Design Best Practices

- [ ] Use most specific schema type (Article > CreativeWork)
- [ ] Include all required properties for rich results
- [ ] Add images (1200x630 px, multiple aspect ratios)
- [ ] Use absolute URLs (not relative)
- [ ] Include dates in ISO 8601 format (2026-01-10T08:00:00Z)
- [ ] Nest related entities (Author within Article)
- [ ] Match structured data to visible content (no hidden data)

### Content Best Practices

- [ ] Structured data must reflect actual page content
- [ ] Don't mark up content that isn't visible on page
- [ ] Keep descriptions accurate and concise
- [ ] Use proper date formats (ISO 8601)
- [ ] Include multiple images when available
- [ ] Set appropriate availability status (InStock/OutOfStock)
- [ ] Update dates when content changes (dateModified)

### Code Best Practices

- [ ] Use TypeScript with schema-dts for type safety
- [ ] Sanitize JSON-LD to prevent XSS
- [ ] Place `<script>` tag in body (not head required)
- [ ] Use reusable StructuredData component
- [ ] Generate dynamically for dynamic pages
- [ ] Test with validators before deploying
- [ ] Monitor Search Console for structured data errors

## Related Skills

- `nextjs-seo-metadata` - Core Next.js metadata API
- `open-graph-twitter` - Social media metadata
- `seo-validation-testing` - Testing and validation tools

## Sources & References

### Official Documentation

- [Guides: JSON-LD | Next.js](https://nextjs.org/docs/app/guides/json-ld)
- [Schema.org](https://schema.org/) - Official schema vocabulary
- [Google Search Central: Structured Data](https://developers.google.com/search/docs/appearance/structured-data)

### Implementation Guides

- [Implementing JSON-LD in Next.js for SEO](https://www.wisp.blog/blog/implementing-json-ld-in-nextjs-for-seo)
- [Add Structured Data with JSON-LD for better SEO](https://mikebifulco.com/posts/structured-data-json-ld-for-next-js-sites)
- [How to add Schema.org to a Next.js 13+ website](https://medium.com/@lucarestagno/how-to-add-schema-org-to-a-next-js-13-website-5aa37f8795b3)
- [Implementing JSON-LD in Next.js 13/14 with TypeScript](https://steplevelup.com/blogs/add-json-ld-nextjs-1314-project-typescript)

### Validation Tools

- [Rich Results Test - Google](https://search.google.com/test/rich-results)
- [Schema Markup Validator](https://validator.schema.org/)
- [Google Search Console](https://search.google.com/search-console) - Monitor structured data errors

### Libraries

- [schema-dts](https://github.com/google/schema-dts) - TypeScript types for Schema.org
- [serialize-javascript](https://github.com/yahoo/serialize-javascript) - Safe JSON serialization

---

## Changelog

### v2.0.0 (2026-01-12)
- **CRITICAL: Added Google Schema.org deprecations warning (January 2026)**
  - Google discontinued support for 5 Schema.org types in January 2026
  - Added deprecation table with status, replacements, and impact
  - Documented all 5 deprecated types:
    1. **Practice Problem** → Use `LearningResource` or `Quiz`
    2. **Dataset** → Limited to Google Dataset Search only
    3. **Sitelinks Search Box** → Google generates automatically (remove manual implementation)
    4. **SpecialAnnouncement** → Use `NewsArticle` or `Article`
    5. **Q&A (QAPage)** → Use `FAQPage` instead
  - **Added comprehensive migration guides** with TypeScript examples for each deprecated type
  - **Added audit section**: Bash commands to check for deprecated types in codebase
  - **Added validation checklist**: 5-point checklist for deprecated schemas
  - **Added testing section**: How deprecated types show warnings in Google Rich Results Test
- **Added "When to Update" section**: Timeline for removing deprecated schemas
- Updated skill description with deprecation warnings
- **Impact**: Prevents using discontinued schema types that won't generate rich results, ensures compatibility with Google Search

### v1.0.0 (Initial)
- Core JSON-LD implementation patterns
- Common schema types (Organization, Article, Product, Recipe, FAQ, Event, LocalBusiness, Breadcrumb)
- TypeScript support with schema-dts
- XSS security patterns
- Dynamic structured data for Next.js
- Validation and testing tools

---

**Last Updated**: January 12, 2026
**Version**: 2.0.0
**Knowledge Base**: Schema.org vocabulary + Next.js 16 JSON-LD patterns + January 2026 Google deprecations
**Confidence Level**: High (based on official Schema.org and Google documentation)
