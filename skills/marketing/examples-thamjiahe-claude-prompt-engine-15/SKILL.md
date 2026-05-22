---
name: "SEO Optimization"
description: "Implement Next.js SEO with metadata, structured data, sitemaps, Open Graph tags, and technical SEO. Apply when optimizing pages for search engines, adding social sharing, or improving discoverability."
allowed-tools: Read, Write, Edit, Bash
version: 1.1.0
compatibility: Claude Opus 4.5, Claude Code v2.x
updated: 2026-01-24
---

# SEO Optimization

Systematic SEO implementation for Next.js applications ensuring maximum search visibility and social sharing.

## Overview

This Skill enforces:
- Optimized metadata (titles, descriptions)
- Open Graph and Twitter Card tags
- JSON-LD structured data
- Sitemaps and robots.txt
- Canonical tags for duplicate prevention
- Image optimization
- Core Web Vitals optimization
- URL structure best practices

Apply when optimizing pages for search engines, adding social sharing, or improving discoverability.

## Metadata Optimization

### Static Metadata

```tsx
// app/page.tsx
export const metadata: Metadata = {
  title: 'Home | My App',
  description: 'Build amazing apps with modern technology',
  keywords: ['Next.js', 'React', 'TypeScript'],
  authors: [{ name: 'Your Name' }],
  viewport: 'width=device-width, initial-scale=1',
  robots: 'index, follow'
};

export default function HomePage() {
  return <div>Home</div>;
}
```

### Dynamic Metadata (generateMetadata)

```tsx
// app/blog/[slug]/page.tsx
import { Metadata } from 'next';

export async function generateMetadata(
  { params }: { params: { slug: string } }
): Promise<Metadata> {
  const post = await getPost(params.slug);

  return {
    title: post.title,
    description: post.excerpt,
    keywords: post.tags,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      url: `https://example.com/blog/${post.slug}`,
      siteName: 'My Blog',
      images: [
        {
          url: post.image,
          width: 1200,
          height: 630,
          alt: post.title
        }
      ],
      type: 'article',
      publishedTime: post.publishedAt,
      authors: [post.author]
    }
  };
}

export default async function BlogPost(
  { params }: { params: { slug: string } }
) {
  const post = await getPost(params.slug);

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  );
}
```

## Open Graph & Social Sharing

### Complete Open Graph Setup

```tsx
// app/layout.tsx
export const metadata: Metadata = {
  metadataBase: new URL('https://example.com'),
  title: 'My App',
  description: 'The best app ever',
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://example.com',
    siteName: 'My App',
    title: 'My App',
    description: 'The best app ever',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'My App'
      }
    ]
  },
  twitter: {
    card: 'summary_large_image',
    title: 'My App',
    description: 'The best app ever',
    images: ['/og-image.png'],
    creator: '@yourhandle'
  }
};
```

### Article Metadata (Blog Post)

```tsx
const metadata: Metadata = {
  openGraph: {
    type: 'article',
    publishedTime: '2025-01-15T10:00:00Z',
    modifiedTime: '2025-01-20T15:30:00Z',
    authors: ['John Doe'],
    tags: ['Next.js', 'SEO', 'Performance']
  }
};
```

## JSON-LD Structured Data

### Product Schema

```tsx
// app/products/[id]/page.tsx
export default function ProductPage({ params }) {
  const product = getProduct(params.id);

  const structuredData = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    description: product.description,
    image: product.image,
    brand: {
      '@type': 'Brand',
      name: 'My Store'
    },
    offers: {
      '@type': 'Offer',
      price: product.price,
      priceCurrency: 'USD',
      availability: 'https://schema.org/InStock'
    },
    aggregateRating: {
      '@type': 'AggregateRating',
      ratingValue: product.rating,
      reviewCount: product.reviews.length
    }
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
      />
      <div>
        <h1>{product.name}</h1>
        <p>{product.description}</p>
        <p>Price: ${product.price}</p>
      </div>
    </>
  );
}
```

### Organization Schema

```tsx
// app/layout.tsx
export default function RootLayout({ children }) {
  const organizationSchema = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: 'My Company',
    url: 'https://example.com',
    logo: 'https://example.com/logo.png',
    description: 'Company description',
    sameAs: [
      'https://twitter.com/mycompany',
      'https://linkedin.com/company/mycompany',
      'https://facebook.com/mycompany'
    ],
    contact: {
      '@type': 'ContactPoint',
      contactType: 'Customer Support',
      email: 'support@example.com'
    }
  };

  return (
    <html>
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationSchema) }}
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

## Sitemaps

### Static Sitemap

```ts
// app/sitemap.ts
import { MetadataRoute } from 'next';

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: 'https://example.com',
      lastModified: new Date(),
      changeFrequency: 'yearly',
      priority: 1
    },
    {
      url: 'https://example.com/about',
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.8
    },
    {
      url: 'https://example.com/contact',
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.8
    }
  ];
}
```

### Dynamic Sitemap (Blog Posts)

```ts
// app/sitemap.ts
import { MetadataRoute } from 'next';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await getAllPosts();

  const postUrls = posts.map(post => ({
    url: `https://example.com/blog/${post.slug}`,
    lastModified: post.updatedAt || post.publishedAt,
    changeFrequency: 'weekly' as const,
    priority: 0.7
  }));

  const staticRoutes: MetadataRoute.Sitemap = [
    {
      url: 'https://example.com',
      lastModified: new Date(),
      changeFrequency: 'yearly' as const,
      priority: 1
    },
    {
      url: 'https://example.com/blog',
      lastModified: new Date(),
      changeFrequency: 'daily' as const,
      priority: 0.8
    }
  ];

  return [...staticRoutes, ...postUrls];
}
```

## Robots.txt

```ts
// app/robots.ts
import { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/admin', '/api', '/private']
      },
      {
        userAgent: 'Googlebot',
        allow: '/',
        crawlDelay: 0
      }
    ],
    sitemap: 'https://example.com/sitemap.xml',
    host: 'https://example.com'
  };
}
```

## Canonical Tags

```tsx
export const metadata: Metadata = {
  alternates: {
    canonical: 'https://example.com/page'
  }
};

// ✅ GOOD: Prevent duplicate content
// If /blog/post and /blog?id=1 show same content
// Set canonical on both pointing to primary URL

// ❌ BAD: No canonical tag
// Search engines may index duplicate content
```

## URL Structure

### Best Practices

```
✅ GOOD: Clean, descriptive URLs
/blog/seo-best-practices
/products/laptop-15-inch
/docs/getting-started

❌ BAD: Query parameters for content
/blog?id=123&post=abc
/products?item=laptop
/page.php?section=intro

✅ GOOD: Hierarchical structure
/blog
/blog/web-development
/blog/web-development/seo-tips

❌ BAD: Deep unnecessary nesting
/content/articles/posts/blogs/my-post
/docs/guide/documentation/how-to/step-by-step
```

## Image Optimization for SEO

```tsx
import Image from 'next/image';

// ✅ GOOD: Optimized image with alt text
<Image
  src="/blog-post-image.jpg"
  alt="Complete guide to Next.js SEO optimization"
  width={1200}
  height={630}
  priority={false}
  quality={80}
  format="webp"
/>

// ❌ BAD: Missing alt text
<img src="/blog-post-image.jpg" />

// ❌ BAD: Generic alt text
<Image
  src="/image.jpg"
  alt="image"
/>
```

## Core Web Vitals Optimization

### Lighthouse Score Target

- **LCP (Largest Contentful Paint)**: < 2.5 seconds
- **FID (First Input Delay)**: < 100 milliseconds
- **CLS (Cumulative Layout Shift)**: < 0.1

### Optimization Steps

```tsx
// ✅ GOOD: Preload critical resources
export const metadata = {
  metadataBase: new URL('https://example.com'),
  preload: [
    {
      href: '/fonts/inter-var.woff2',
      as: 'font',
      type: 'font/woff2',
      crossOrigin: 'anonymous'
    }
  ]
};

// ✅ GOOD: Lazy load below-fold images
<Image
  src="/below-fold-image.jpg"
  alt="description"
  loading="lazy"
/>

// ✅ GOOD: Dynamic imports for heavy components
const HeavyChart = dynamic(() => import('@/components/Chart'), {
  loading: () => <div>Loading...</div>
});
```

## Verification Checklist

### Before Deploying

- [ ] Title tag: 50-60 characters, keyword-rich
- [ ] Meta description: 155-160 characters, compelling
- [ ] Headings: Proper hierarchy (h1 > h2 > h3)
- [ ] Canonical tags: Prevent duplicate content
- [ ] Open Graph tags: Social sharing optimized
- [ ] JSON-LD schema: Rich results enabled
- [ ] Sitemap: Generated and valid
- [ ] Robots.txt: Proper rules configured
- [ ] Images: Alt text, optimized, WebP format
- [ ] Core Web Vitals: LCP < 2.5s, FID < 100ms, CLS < 0.1
- [ ] Mobile-friendly: Responsive design verified
- [ ] No broken links: 404 redirects handled

### Testing Tools

```bash
# Google Lighthouse
# https://pagespeed.web.dev

# Google Search Console
# https://search.google.com/search-console

# Structured Data Testing
# https://schema.org/validator

# Open Graph Preview
# https://www.opengraphcheck.com
```

## Anti-Patterns

```tsx
// ❌ BAD: Duplicate titles
<title>Home</title>  // Same on every page

// ❌ BAD: Keyword stuffing
<meta name="description" content="Buy shoes, shoes, best shoes, cheap shoes, red shoes" />

// ❌ BAD: No alt text
<img src="product.jpg" />

// ❌ BAD: Blocking resources
<link rel="stylesheet" href="heavy-style.css" />
<script src="heavy-script.js"></script>

// ❌ BAD: No schema markup
// Missing rich results opportunity

// ❌ BAD: Redirects chain
// /old-page → /newer-page → /current-page
// Use direct redirect instead
```

## Integration with Project Standards

Enforces discoverability and performance:
- Improved search visibility (organic traffic)
- Better social sharing (engagement)
- Fast page loads (Core Web Vitals)
- Structured data (rich results)

## Resources

- Next.js SEO: https://nextjs.org/learn/seo/introduction-to-seo
- Google Search Central: https://developers.google.com/search
- Schema.org: https://schema.org
- Lighthouse: https://developers.google.com/web/tools/lighthouse
---

**Last Updated:** January 24, 2026
**Compatibility:** Claude Opus 4.5, Claude Code v2.x
**Status:** Production Ready

> **January 2026 Update:** This skill is compatible with Claude Opus 4.5 and Claude Code v2.x. For complex tasks, use the `effort: high` parameter for thorough analysis.
