---
name: seo-patterns
description: Meta tag patterns, structured data (JSON-LD), Core Web Vitals optimization, and SSR/SSG strategies for search visibility.
---

# SEO Patterns

Technical SEO patterns for web applications and content sites.

## Meta Tags Template

```typescript
// Next.js App Router metadata
import { Metadata } from 'next'

export function generateMetadata({ params }): Metadata {
  const product = getProduct(params.slug)

  return {
    title: `${product.name} | Your App`,        // 50-60 chars
    description: product.summary.slice(0, 155), // 150-160 chars
    alternates: {
      canonical: `https://example.com/products/${params.slug}`,
      languages: {
        'en': `https://example.com/en/products/${params.slug}`,
        'tr': `https://example.com/tr/products/${params.slug}`,
      }
    },
    openGraph: {
      title: product.name,
      description: product.summary,
      url: `https://example.com/products/${params.slug}`,
      siteName: 'Your App',
      images: [{
        url: product.imageUrl,
        width: 1200,
        height: 630,
        alt: product.name,
      }],
      type: 'website',
      locale: 'en_US',
    },
    twitter: {
      card: 'summary_large_image',
      title: product.name,
      description: product.summary,
      images: [product.imageUrl],
    },
    robots: {
      index: true,
      follow: true,
      'max-image-preview': 'large',
      'max-snippet': -1,
    }
  }
}
```

## Structured Data (JSON-LD)

```typescript
// Product schema
function ProductJsonLd({ product }: { product: Product }) {
  const schema = {
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
      url: `https://example.com/products/${product.slug}`,
      priceCurrency: 'USD',
      price: product.price,
      availability: product.inStock
        ? 'https://schema.org/InStock'
        : 'https://schema.org/OutOfStock',
      seller: {
        '@type': 'Organization',
        name: 'Your App',
      }
    },
    aggregateRating: product.reviewCount > 0 ? {
      '@type': 'AggregateRating',
      ratingValue: product.avgRating,
      reviewCount: product.reviewCount,
    } : undefined,
  }

  return <script type="application/ld+json">{JSON.stringify(schema)}</script>
}

// FAQ schema (wins featured snippets)
function FaqJsonLd({ faqs }: { faqs: { question: string; answer: string }[] }) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faqs.map(faq => ({
      '@type': 'Question',
      name: faq.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: faq.answer,
      }
    }))
  }

  return <script type="application/ld+json">{JSON.stringify(schema)}</script>
}

// BreadcrumbList schema
function BreadcrumbJsonLd({ items }: { items: { name: string; url: string }[] }) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: item.name,
      item: item.url,
    }))
  }

  return <script type="application/ld+json">{JSON.stringify(schema)}</script>
}
```

## Core Web Vitals Optimization

```typescript
// LCP (Largest Contentful Paint) - Target: < 2.5s
// Priority: preload hero image, avoid lazy-loading above-fold content
import Image from 'next/image'

function HeroSection({ image }: { image: string }) {
  return (
    <Image
      src={image}
      alt="Hero"
      width={1200}
      height={600}
      priority           // Preload, no lazy loading
      sizes="100vw"      // Responsive sizing hints
      quality={85}       // Balance quality vs size
    />
  )
}

// CLS (Cumulative Layout Shift) - Target: < 0.1
// Always set explicit width/height on images and embeds
function VideoEmbed({ videoId }: { videoId: string }) {
  return (
    <div style={{ aspectRatio: '16/9', width: '100%' }}>
      <iframe
        src={`https://youtube.com/embed/${videoId}`}
        width="100%"
        height="100%"
        loading="lazy"
        title="Video"
      />
    </div>
  )
}

// INP (Interaction to Next Paint) - Target: < 200ms
// Defer heavy computation, use web workers
function SearchResults() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])

  // Debounce input to prevent blocking main thread
  const debouncedSearch = useMemo(
    () => debounce((q: string) => {
      startTransition(() => {
        setResults(search(q))
      })
    }, 300),
    []
  )

  return (
    <input
      type="search"
      onChange={(e) => {
        setQuery(e.target.value)
        debouncedSearch(e.target.value)
      }}
    />
  )
}
```

## SSR/SSG Strategy

```typescript
// Static Generation (SSG): content that rarely changes
// Best for: blog posts, product pages, documentation
export async function generateStaticParams() {
  const products = await getProductSlugs()
  return products.map(slug => ({ slug }))
}

export default async function ProductPage({ params }) {
  const product = await getProduct(params.slug)
  return <ProductDetail product={product} />
}

// Incremental Static Regeneration (ISR): SSG with refresh
export const revalidate = 3600  // Regenerate every hour

// Server-Side Rendering (SSR): dynamic, personalized content
// Use only when content changes per request (user-specific, real-time data)
export const dynamic = 'force-dynamic'
```

## Sitemap and Robots

```typescript
// app/sitemap.ts
export default async function sitemap(): MetadataRoute.Sitemap {
  const products = await getAllProducts()
  const posts = await getAllBlogPosts()

  return [
    { url: 'https://example.com', lastModified: new Date(), priority: 1.0 },
    ...products.map(p => ({
      url: `https://example.com/products/${p.slug}`,
      lastModified: p.updatedAt,
      changeFrequency: 'weekly' as const,
      priority: 0.8,
    })),
    ...posts.map(p => ({
      url: `https://example.com/blog/${p.slug}`,
      lastModified: p.updatedAt,
      changeFrequency: 'monthly' as const,
      priority: 0.6,
    })),
  ]
}

// app/robots.ts
export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      { userAgent: '*', allow: '/', disallow: ['/api/', '/admin/', '/checkout/'] },
    ],
    sitemap: 'https://example.com/sitemap.xml',
  }
}
```

## Checklist

- [ ] Unique title (50-60 chars) and description (150-160 chars) per page
- [ ] Canonical URL set on every page (avoid duplicate content)
- [ ] JSON-LD structured data for products, FAQs, breadcrumbs, articles
- [ ] Open Graph + Twitter Card meta tags for social sharing
- [ ] LCP < 2.5s: preload hero images, inline critical CSS
- [ ] CLS < 0.1: explicit dimensions on all images/embeds
- [ ] INP < 200ms: debounce inputs, defer heavy JS
- [ ] Dynamic sitemap.xml updated with all crawlable pages
- [ ] robots.txt blocks API, admin, and auth routes from crawling
- [ ] hreflang tags for multi-language sites

## SaaS Landing Page Anatomy

```
┌──────────────────────────────────────┐
│  Nav: Logo | Features | Pricing | CTA │ ← Sticky, minimal
├──────────────────────────────────────┤
│  HERO SECTION                        │
│  H1: Value proposition (6-12 words)  │
│  Subtitle: How it works (1 sentence) │
│  CTA button + social proof line      │
│  Hero image/screenshot               │
├──────────────────────────────────────┤
│  SOCIAL PROOF BAR                    │
│  "Trusted by X teams" + logos        │
├──────────────────────────────────────┤
│  FEATURES (3-4 cards)                │
│  Icon + Title + 1 sentence each      │
├──────────────────────────────────────┤
│  HOW IT WORKS (3 steps)              │
│  Step 1 → Step 2 → Step 3           │
├──────────────────────────────────────┤
│  TESTIMONIALS (2-3 quotes)           │
│  Photo + Name + Role + Quote         │
├──────────────────────────────────────┤
│  PRICING (3 tiers)                   │
│  Free | Pro (highlighted) | Enterprise│
├──────────────────────────────────────┤
│  FAQ (5-8 questions, JSON-LD)        │
├──────────────────────────────────────┤
│  FINAL CTA                           │
│  Repeat hero CTA with urgency        │
├──────────────────────────────────────┤
│  FOOTER                              │
│  Legal links + sitemap links         │
└──────────────────────────────────────┘
```

### Hero Section Formulas

```
Formula 1 — Problem-Solution:
  H1: "Stop [pain point]. Start [desired outcome]."
  Example: "Stop losing leads. Start converting visitors."

Formula 2 — Before-After:
  H1: "[Tool] turns [bad state] into [good state]."
  Example: "[Product] turns messy spreadsheets into real-time dashboards."

Formula 3 — Social Proof Lead:
  H1: "[N]+ teams use [tool] to [outcome]."
  Example: "2,000+ teams use [Product] to ship 3x faster."
```

### Pricing Page SEO

```typescript
// Pricing page structured data
function PricingJsonLd({ plans }: { plans: Plan[] }) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    name: 'Pricing',
    description: 'Plans and pricing for Your App',
    mainEntity: plans.map(plan => ({
      '@type': 'Offer',
      name: plan.name,
      price: plan.price,
      priceCurrency: 'USD',
      description: plan.description,
      eligibleDuration: { '@type': 'QuantitativeValue', value: 1, unitCode: 'MON' }
    }))
  }

  return <script type="application/ld+json">{JSON.stringify(schema)}</script>
}

// SEO tips for pricing pages:
// - Title: "[Product] Pricing — Free, Pro & Enterprise Plans"
// - Include pricing in meta description (Google shows it in snippets)
// - Use comparison table with feature checkmarks
// - FAQ section below pricing (common objections → JSON-LD)
// - "Free tier" callout improves CTR from search results
```

### SaaS-Specific Structured Data

```typescript
// SoftwareApplication schema (rich results for SaaS)
function SoftwareAppJsonLd({ app }: { app: SaaSApp }) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    name: app.name,
    applicationCategory: app.category,  // 'BusinessApplication', 'DeveloperApplication'
    operatingSystem: 'Web',
    offers: {
      '@type': 'AggregateOffer',
      lowPrice: app.freeTier ? '0' : app.lowestPrice,
      highPrice: app.highestPrice,
      priceCurrency: 'USD',
      offerCount: app.planCount
    },
    aggregateRating: app.reviewCount > 0 ? {
      '@type': 'AggregateRating',
      ratingValue: app.avgRating,
      ratingCount: app.reviewCount,
      bestRating: 5,
      worstRating: 1
    } : undefined,
    screenshot: app.screenshotUrl,
    featureList: app.features.join(', ')
  }

  return <script type="application/ld+json">{JSON.stringify(schema)}</script>
}
```

## Anti-Patterns

- Client-side only rendering: search engines may not execute JS
- Duplicate content without canonical: pages compete against themselves
- Missing alt text on images: accessibility and image search penalty
- Blocking CSS/JS in robots.txt: prevents proper rendering by crawlers
- Infinite scroll without pagination URLs: content invisible to crawlers
- Meta description over 160 chars: truncated in search results
- Pricing page without structured data: misses rich snippet opportunity
- Landing page H1 focused on brand, not value: low click-through from SERPs
