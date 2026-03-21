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
    title: `${product.name} | MyStore`,        // 50-60 chars
    description: product.summary.slice(0, 155), // 150-160 chars
    alternates: {
      canonical: `https://mystore.com/products/${params.slug}`,
      languages: {
        'en': `https://mystore.com/en/products/${params.slug}`,
        'tr': `https://mystore.com/tr/products/${params.slug}`,
      }
    },
    openGraph: {
      title: product.name,
      description: product.summary,
      url: `https://mystore.com/products/${params.slug}`,
      siteName: 'MyStore',
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
      url: `https://mystore.com/products/${product.slug}`,
      priceCurrency: 'USD',
      price: product.price,
      availability: product.inStock
        ? 'https://schema.org/InStock'
        : 'https://schema.org/OutOfStock',
      seller: {
        '@type': 'Organization',
        name: 'MyStore',
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
    { url: 'https://mystore.com', lastModified: new Date(), priority: 1.0 },
    ...products.map(p => ({
      url: `https://mystore.com/products/${p.slug}`,
      lastModified: p.updatedAt,
      changeFrequency: 'weekly' as const,
      priority: 0.8,
    })),
    ...posts.map(p => ({
      url: `https://mystore.com/blog/${p.slug}`,
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
    sitemap: 'https://mystore.com/sitemap.xml',
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

## Anti-Patterns

- Client-side only rendering: search engines may not execute JS
- Duplicate content without canonical: pages compete against themselves
- Missing alt text on images: accessibility and image search penalty
- Blocking CSS/JS in robots.txt: prevents proper rendering by crawlers
- Infinite scroll without pagination URLs: content invisible to crawlers
- Meta description over 160 chars: truncated in search results
