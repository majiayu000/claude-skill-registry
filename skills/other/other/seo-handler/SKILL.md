---
name: seo-handler
description: Manage SEO, sitemaps, and metadata for optimal search engine visibility
tools: Read, Write, Edit
model: inherit
---

# SEO Handler Skill

This skill ensures your Next.js application is optimized for search engines. It covers sitemaps, metadata (OpenGraph), server-side rendering (SSR/ISR), structured data (JSON-LD), and robots.txt configuration.

## Core Principles

1.  **Sitemap Visibility**: Every public page MUST be in `src/app/sitemap.ts`.
2.  **Metadata Inheritance**: Use `layout.tsx` for defaults; override in `page.tsx`.
3.  **Structured Data**: Use `next-seo` components (JSON-LD) on every content page.
4.  **Server-Side Data**: Fetch content-heavy data on the server (ISR) for SEO.
5.  **Robots Control**: Use `src/app/robots.ts` to guide crawlers.

## 1. Sitemap Management

**File**: `src/app/sitemap.ts`

When adding a new public route (e.g., `/features`), add it to the `staticPages` array.

```typescript
const staticPages = [
  "", // Home
  "/features", // New page
  // ...
];
```

### Splitting Sitemaps (Large Sites)

If you have >50k URLs (e.g., user profiles, products), use `generateSitemaps`.

**File**: `src/app/products/sitemap.ts`

```typescript
import { BASE_URL } from '@/lib/constants';

export async function generateSitemaps() {
  // Fetch total count and divide by batch size (e.g., 50,000)
  return [{ id: 0 }, { id: 1 }];
}

export default async function sitemap({ id }: { id: { id: number } }) {
  const start = id.id * 50000;
  const products = await getProducts(start, 50000);
  
  return products.map(product => ({
    url: `${BASE_URL}/products/${product.slug}`,
    lastModified: product.updatedAt,
  }));
}
```

## 2. Metadata & OpenGraph

**Base Layout**: `src/app/layout.tsx` (or group layout) defines the template.

```typescript
export const metadata: Metadata = {
  title: {
    template: "%s | My App",
    default: "My App - The Best SaaS",
  },
  description: "...",
  openGraph: { ... }, // Default OG
};
```

**Page Level**: `src/app/blog/[slug]/page.tsx`

```typescript
export async function generateMetadata({ params }): Promise<Metadata> {
  const post = await getPost(params.slug);
  return {
    title: post.title,
    description: post.summary,
    openGraph: {
      images: [post.coverImage], // Overrides default
    },
  };
}
```

## 3. Structured Data (JSON-LD)

### Primary: Next-SEO Components
Use `next-seo` components to inject JSON-LD structured data. This helps search engines understand your content (Articles, Products, FAQs, etc.).

**Page Component**: `src/app/blog/[slug]/page.tsx`

```tsx
import { ArticleJsonLd } from "next-seo";

export default function BlogPost({ post }) {
  return (
    <>
      <ArticleJsonLd
        useAppDir
        url={`https://myapp.com/blog/${post.slug}`}
        title={post.title}
        images={[post.image]}
        datePublished={post.date}
        authorName="My App"
        description={post.description}
      />
      <article>...</article>
    </>
  );
}
```

### Alternative: Raw JSON-LD (Script Tag)
If a specific schema isn't supported by `next-seo`, use a raw script tag. Wrap in `Suspense` if the data fetching is async.

```tsx
import { Suspense } from "react";

export default function Page() {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'CustomType',
    name: 'Custom Name',
    description: 'Description',
  };

  return (
    <section>
      <Suspense fallback={null}>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </Suspense>
      {/* Page Content */}
    </section>
  );
}
```

## 4. Incremental Static Regeneration (ISR)

For content pages (Blogs, Docs, Marketing) that rely on database content, use ISR to cache them at the edge.

**Page Component**:

```typescript
// src/app/blog/[slug]/page.tsx

// 1. Enable ISR
export const revalidate = 3600; // Revalidate every hour (in seconds)
// OR use dynamic params with generateStaticParams for full static export behavior
export const dynamicParams = true; 

export async function generateStaticParams() {
  const posts = await db.query.posts.findMany();
  return posts.map((post) => ({ slug: post.slug }));
}

export default async function BlogPost({ params }) {
  // 2. Fetch on Server (Data is cached based on revalidate config)
  const post = await getPost(params.slug); 
  
  return <article>{/* ... */}</article>;
}
```

## 5. Robots.txt configuration

**File**: `src/app/robots.ts`

Ensure you disallow private routes (`/api/`, `/app/`, `/admin/`) to save crawl budget.

```typescript
export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: "*",
      allow: "/",
      disallow: ["/api/", "/app/", "/super-admin/"],
    },
    sitemap: `${process.env.NEXT_PUBLIC_APP_URL}/sitemap.xml`,
  };
}
```
