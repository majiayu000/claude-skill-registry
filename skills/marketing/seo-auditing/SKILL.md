---
name: seo-auditing
description: Audit pages for search engine optimization best practices including meta tags, structured data, performance, and content optimization. Use when checking SEO compliance, improving search rankings, adding structured data, or optimizing meta tags. Triggers on requests like "audit SEO", "improve SEO", "add meta tags", "structured data", "optimize for search", or "search engine optimization".
---

# SEO Auditing

Audit and improve SEO for better search engine visibility.

## Process

1. **Technical SEO** - Meta tags, structure, performance
2. **Content SEO** - Headings, keywords, readability
3. **Structured Data** - Schema.org markup
4. **Crawlability** - Sitemap, robots, canonical URLs
5. **Implement fixes** - Priority order

## Technical SEO Checklist

### Meta Tags

```tsx
// src/app/layout.tsx or page generateMetadata
export async function generateMetadata(): Promise<Metadata> {
  const settings = await getPublicSettings();

  return {
    title: {
      default: settings.site_name,
      template: `%s ${settings.meta_title_suffix || '| ' + settings.site_name}`,
    },
    description: settings.site_description,
    metadataBase: new URL(settings.site_url || 'https://example.com'),
    openGraph: {
      type: 'website',
      siteName: settings.site_name,
      images: settings.default_og_image_path
        ? [{ url: `/api/media/${settings.default_og_image_path}` }]
        : [],
    },
    twitter: {
      card: 'summary_large_image',
      site: settings.social_twitter,
    },
    robots: {
      index: true,
      follow: true,
    },
  };
}
```

### Page-Level Metadata

```tsx
// src/app/(public)/blog/[slug]/page.tsx
export async function generateMetadata({ params }): Promise<Metadata> {
  const article = await getArticle(params.slug);

  return {
    title: article.title,
    description: article.excerpt || article.body.slice(0, 160),
    openGraph: {
      type: 'article',
      title: article.title,
      description: article.excerpt,
      publishedTime: article.authored_on,
      authors: [article.author],
      images: article.image_path
        ? [{ url: `/api/media/${article.image_path}`, alt: article.title }]
        : [],
    },
    alternates: {
      canonical: `/blog/${article.slug}`,
    },
  };
}
```

### Canonical URLs

```tsx
// Prevent duplicate content
alternates: {
  canonical: `/blog/${slug}`,  // Always use canonical
}
```

## Content SEO

### Heading Structure
```tsx
// Single h1 per page
<h1>{article.title}</h1>

// Logical hierarchy
<h2>Section</h2>
<h3>Subsection</h3>

// Don't skip levels (h1 -> h3)
```

### Image Optimization
```tsx
// Alt text for all images
<img
  src={imageUrl}
  alt={descriptiveAltText}  // Describe the image content
  loading="lazy"            // Lazy load below-fold images
  width={800}               // Explicit dimensions prevent CLS
  height={600}
/>

// Next.js Image component
import Image from 'next/image';
<Image
  src={imageUrl}
  alt={altText}
  width={800}
  height={600}
  priority={isAboveFold}  // LCP optimization
/>
```

## Structured Data (Schema.org)

Use Next.js built-in JSON-LD support or create a dedicated component:

### JsonLd Component Pattern

```tsx
// src/components/JsonLd.tsx
interface JsonLdProps {
  data: Record<string, unknown>;
}

export function JsonLd({ data }: JsonLdProps) {
  // Create script element with JSON-LD
  // Note: Only use with trusted, sanitized data from your database
  return (
    <script
      type="application/ld+json"
      // Content must be from trusted sources only (your database)
      // Never use user-provided HTML directly
      {...{ dangerouslySetInnerHTML: { __html: JSON.stringify(data) } }}
    />
  );
}
```

### Article Schema

```tsx
// In article page
const articleSchema = {
  '@context': 'https://schema.org',
  '@type': 'Article',
  headline: article.title,
  description: article.excerpt,
  image: article.image_url,
  datePublished: article.authored_on,
  dateModified: article.updated_at,
  author: {
    '@type': 'Person',
    name: article.author,
  },
  publisher: {
    '@type': 'Organization',
    name: settings.site_name,
    logo: {
      '@type': 'ImageObject',
      url: settings.logo_url,
    },
  },
};

<JsonLd data={articleSchema} />
```

### Organization Schema

```tsx
// Add to homepage/layout
const orgSchema = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  name: settings.site_name,
  url: settings.site_url,
  logo: settings.logo_url,
  sameAs: [
    settings.social_twitter && `https://twitter.com/${settings.social_twitter}`,
    settings.social_facebook,
    settings.social_linkedin,
  ].filter(Boolean),
};
```

### Breadcrumb Schema

```tsx
const breadcrumbSchema = {
  '@context': 'https://schema.org',
  '@type': 'BreadcrumbList',
  itemListElement: [
    { '@type': 'ListItem', position: 1, name: 'Home', item: '/' },
    { '@type': 'ListItem', position: 2, name: 'Blog', item: '/blog' },
    { '@type': 'ListItem', position: 3, name: article.title },
  ],
};
```

## Crawlability

### Sitemap

```tsx
// src/app/sitemap.ts (existing file)
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const db = await getDb();
  const articles = await db.prepare(`
    SELECT slug, updated_at FROM articles WHERE published = 1
  `).all();

  return [
    { url: '/', lastModified: new Date(), changeFrequency: 'daily', priority: 1 },
    { url: '/blog', lastModified: new Date(), changeFrequency: 'daily', priority: 0.9 },
    ...articles.results.map(article => ({
      url: `/blog/${article.slug}`,
      lastModified: new Date(article.updated_at),
      changeFrequency: 'weekly' as const,
      priority: 0.8,
    })),
  ];
}
```

### Robots.txt

```tsx
// src/app/robots.ts
export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: '*',
      allow: '/',
      disallow: ['/admin/', '/api/'],
    },
    sitemap: 'https://example.com/sitemap.xml',
  };
}
```

## Performance (Core Web Vitals)

SEO ranking factors include:

| Metric | Target | How to Achieve |
|--------|--------|----------------|
| LCP | < 2.5s | Optimize images, prioritize above-fold |
| FID | < 100ms | Minimize JavaScript, defer non-critical |
| CLS | < 0.1 | Set image dimensions, avoid layout shifts |

## Output

Provide SEO audit results:
1. Meta tag completeness checklist
2. Structured data validation
3. Content optimization suggestions
4. Technical issues (sitemap, robots, canonical)
5. Priority fixes with implementation code
