---
name: nextjs-seo-optimization
description: Implement SEO best practices in Next.js applications. Includes metadata, Open Graph tags, canonical URLs, sitemap generation, schema markup, and performance optimization for search ranking.
---

# Next.js SEO Optimization Skill

## When to Use

Use this skill when:
- Building new pages requiring SEO
- Optimizing existing pages for search ranking
- Implementing dynamic metadata (products, articles)
- Adding Open Graph tags for social sharing
- Generating sitemaps and robots.txt
- Implementing structured data (Schema.org)
- Improving Core Web Vitals for ranking

## Core Concepts

### 1. Metadata (Next.js 13+)

```typescript
// app/layout.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'OfertaChina - Melhores Cupons e Ofertas',
  description: 'Encontre as melhores ofertas da AliExpress e plataformas chinesas. Cupons exclusivos, frete grátis e cashback.',
  keywords: 'ofertas AliExpress, cupons, cashback, frete grátis',
  metadataBase: new URL('https://ofertachina.com'),
  openGraph: {
    type: 'website',
    locale: 'pt_BR',
    url: 'https://ofertachina.com',
    siteName: 'OfertaChina',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'OfertaChina - Melhores ofertas online'
      }
    ]
  },
  twitter: {
    card: 'summary_large_image',
    title: 'OfertaChina',
    description: 'Melhores cupons e ofertas da AliExpress',
    images: ['/og-image.png']
  },
  robots: {
    index: true,
    follow: true,
    'max-image-preview': 'large',
    'max-snippet': -1,
    'max-video-preview': -1,
  }
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-BR">
      <head>
        {/* Additional meta tags */}
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="theme-color" content="#FF6B35" />
        
        {/* Preconnect to external domains */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      </head>
      <body>{children}</body>
    </html>
  )
}
```

### 2. Dynamic Metadata (Products)

```typescript
// app/products/[slug]/page.tsx
import type { Metadata } from 'next'
import { getProduct } from '@/lib/api'

interface Props {
  params: { slug: string }
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const product = await getProduct(params.slug)

  if (!product) {
    return {
      title: 'Produto não encontrado',
      description: 'O produto solicitado não existe'
    }
  }

  // Dynamic metadata based on product data
  return {
    title: `${product.title} | OfertaChina`,
    description: product.description.substring(0, 160),
    keywords: `${product.title}, cupom, oferta, ${product.category}`,
    openGraph: {
      type: 'product',
      url: `https://ofertachina.com/products/${product.slug}`,
      title: product.title,
      description: product.description,
      images: [
        {
          url: product.imageUrl,
          width: 1200,
          height: 630,
          alt: product.title
        }
      ]
    },
    twitter: {
      card: 'summary_large_image',
      title: product.title,
      description: product.description,
      images: [product.imageUrl]
    }
  }
}

export async function generateStaticParams() {
  // Generate static pages for most popular products
  const products = await getProduct('popular', { limit: 100 })
  
  return products.map((product) => ({
    slug: product.slug
  }))
}

export default async function ProductPage({ params }: Props) {
  const product = await getProduct(params.slug)

  if (!product) {
    return <div>Produto não encontrado</div>
  }

  return (
    <article>
      <h1>{product.title}</h1>
      <img src={product.imageUrl} alt={product.title} />
      <p>{product.description}</p>
    </article>
  )
}
```

### 3. Schema Markup (Structured Data)

```typescript
// app/products/[slug]/page.tsx
import type { Product as SchemaProduct } from 'schema-dts'
import { JsonLd } from 'react-schemaorg'

export default function ProductPage({ product }) {
  const schemaData: SchemaProduct = {
    '@type': 'Product',
    '@context': 'https://schema.org/',
    name: product.title,
    description: product.description,
    image: product.imageUrl,
    url: `https://ofertachina.com/products/${product.slug}`,
    sku: product.sku,
    brand: {
      '@type': 'Brand',
      name: product.brand
    },
    offers: {
      '@type': 'Offer',
      url: `https://ofertachina.com/products/${product.slug}`,
      priceCurrency: 'BRL',
      price: product.price.toString(),
      priceValidUntil: product.expiresAt,
      availability: product.inStock ? 'InStock' : 'OutOfStock',
      seller: {
        '@type': 'Organization',
        name: 'OfertaChina'
      }
    },
    aggregateRating: product.rating ? {
      '@type': 'AggregateRating',
      ratingValue: product.rating.score,
      ratingCount: product.rating.count
    } : undefined
  }

  return (
    <>
      <JsonLd<SchemaProduct> item={schemaData} />
      <article>
        <h1>{product.title}</h1>
        {/* Product content */}
      </article>
    </>
  )
}
```

### 4. Sitemap Generation

```typescript
// app/sitemap.ts
import { MetadataRoute } from 'next'
import { getAllProducts } from '@/lib/api'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = 'https://ofertachina.com'
  
  // Static routes
  const staticRoutes: MetadataRoute.Sitemap = [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1
    },
    {
      url: `${baseUrl}/products`,
      lastModified: new Date(),
      changeFrequency: 'hourly',
      priority: 0.9
    },
    {
      url: `${baseUrl}/categories`,
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 0.8
    },
    {
      url: `${baseUrl}/about`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.5
    }
  ]

  // Dynamic routes (products)
  const products = await getAllProducts()
  const productRoutes: MetadataRoute.Sitemap = products.map((product) => ({
    url: `${baseUrl}/products/${product.slug}`,
    lastModified: new Date(product.updatedAt),
    changeFrequency: 'weekly' as const,
    priority: 0.7
  }))

  return [...staticRoutes, ...productRoutes]
}
```

### 5. Robots.txt

```typescript
// app/robots.ts
import type { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/admin', '/api', '/*.json$'],
      },
      {
        userAgent: 'GPTBot',
        disallow: '/',
      },
    ],
    sitemap: 'https://ofertachina.com/sitemap.xml',
  }
}
```

### 6. Canonical URLs

```typescript
// components/CanonicalURL.tsx
interface CanonicalURLProps {
  path: string
  baseUrl?: string
}

export function CanonicalURL({ path, baseUrl = 'https://ofertachina.com' }: CanonicalURLProps) {
  return (
    <link
      rel="canonical"
      href={`${baseUrl}${path}`}
      key="canonical"
    />
  )
}

// Usage in page.tsx
export const metadata: Metadata = {
  // ... other metadata
  other: {
    canonical: 'https://ofertachina.com/products/smartphone-xyz'
  }
}
```

### 7. Image Optimization

```typescript
// components/OptimizedImage.tsx
import Image from 'next/image'

interface OptimizedImageProps {
  src: string
  alt: string
  title?: string
  width?: number
  height?: number
}

export function OptimizedImage({
  src,
  alt,
  title,
  width = 800,
  height = 600
}: OptimizedImageProps) {
  return (
    <Image
      src={src}
      alt={alt}
      title={title || alt}
      width={width}
      height={height}
      quality={85}
      priority={false}
      placeholder="blur"
      blurDataURL="data:image/webp;base64,..." // Placeholder
      sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
    />
  )
}
```

### 8. Open Graph Dynamic Images

```typescript
// app/products/[slug]/opengraph-image.tsx
import { ImageResponse } from 'next/og'
import { getProduct } from '@/lib/api'

export const runtime = 'nodejs'
export const alt = 'Product preview'
export const size = {
  width: 1200,
  height: 630,
}
export const contentType = 'image/png'

interface Props {
  params: { slug: string }
}

export default async function Image({ params }: Props) {
  const product = await getProduct(params.slug)

  return new ImageResponse(
    (
      <div
        style={{
          fontSize: 48,
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          width: '100%',
          height: '100%',
          display: 'flex',
          textAlign: 'center',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'white',
          padding: '40px',
        }}
      >
        <div>
          <h1>{product.title}</h1>
          <p>💰 R$ {product.price}</p>
          <p>⭐ {product.rating}/5</p>
        </div>
      </div>
    ),
    {
      ...size,
    },
  )
}
```

### 9. SEO Checklist

```typescript
// hooks/useSEOChecklist.ts
export function useSEOChecklist(page: string) {
  const checks = {
    homepage: [
      '✅ Title tag (50-60 chars)',
      '✅ Meta description (150-160 chars)',
      '✅ H1 tag (only one)',
      '✅ Open Graph image (1200x630)',
      '✅ Mobile responsive',
      '✅ Core Web Vitals score',
      '✅ Schema markup (Organization)',
      '✅ robots.txt configured',
      '✅ sitemap.xml present',
      '✅ Canonical URL set'
    ],
    productPage: [
      '✅ Product title in H1',
      '✅ Product image optimized',
      '✅ Price structured data',
      '✅ Rating schema markup',
      '✅ Dynamic meta description',
      '✅ Open Graph tags dynamic',
      '✅ Canonical URL set',
      '✅ Related products linked',
      '✅ Breadcrumb schema',
      '✅ No duplicate content'
    ]
  }

  return checks[page] || []
}
```

### 10. Performance Optimization

```typescript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'cdn.example.com',
      },
      {
        protocol: 'https',
        hostname: 'aliexpress.com',
      },
    ],
    minimumCacheSize: 50,
    formats: ['image/webp', 'image/avif'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
  },
  
  // ISR configuration
  onDemandEntries: {
    maxInactiveAge: 60 * 10 * 1000, // 10 min
    pagesBufferLength: 5,
  },
  
  // Headers for SEO
  headers: async () => [
    {
      source: '/:path*',
      headers: [
        {
          key: 'X-Content-Type-Options',
          value: 'nosniff'
        },
        {
          key: 'X-Frame-Options',
          value: 'SAMEORIGIN'
        },
        {
          key: 'X-XSS-Protection',
          value: '1; mode=block'
        }
      ]
    }
  ]
}

module.exports = nextConfig
```

## SEO Best Practices

✅ **Title**: 50-60 characters, keyword at start  
✅ **Description**: 150-160 characters, compelling CTA  
✅ **H1**: One per page, keyword relevant  
✅ **Images**: Optimized, descriptive alt text  
✅ **Links**: Internal linking strategy, no orphaned pages  
✅ **Mobile**: Fully responsive, Core Web Vitals ≥ 75  
✅ **Speed**: Images optimized, code splitting  
✅ **Schema**: Product, Organization, BreadcrumbList  
✅ **Canonicals**: Set for paginated/filtered content  
✅ **Structured Data**: Tested with Google Schema Validator  

## Testing Tools

- [Google Search Console](https://search.google.com/search-console)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [Schema Markup Validator](https://validator.schema.org/)
- [Open Graph Preview](https://www.opengraph.xyz/)
- [Mobile-Friendly Test](https://search.google.com/test/mobile-friendly)

## Related Files

- [seo-config.ts](./seo-config.ts) - SEO configuration templates
- [metadata-generator.ts](./metadata-generator.ts) - Dynamic metadata helper
- [schema-templates.ts](./schema-templates.ts) - Schema markup templates

## References

- Next.js SEO: https://nextjs.org/learn/seo/introduction-to-seo
- Google SEO Guide: https://developers.google.com/search/docs
- Schema.org: https://schema.org/
- Open Graph: https://ogp.me/
