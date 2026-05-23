---
name: Headless CMS Integration
description: Separating content management from presentation by providing content via APIs, enabling omnichannel delivery and developer flexibility with platforms like Contentful, Strapi, and Sanity.
---

# Headless CMS Integration

> **Current Level:** Intermediate  
> **Domain:** Content Management / Backend

---

## Overview

Headless CMS separates content management from presentation, providing content via APIs. This guide covers integration patterns, popular platforms, and best practices for building content-driven applications with flexibility and scalability.

---

---

## Core Concepts

### Headless CMS Concepts

```
Traditional CMS:  Content → Template → HTML
Headless CMS:     Content → API → Any Frontend
```

**Benefits:**
- Platform agnostic
- Omnichannel delivery
- Better performance
- Developer flexibility
- Scalability

## Popular Headless CMS Comparison

| CMS | Type | API | Hosting | Pricing |
|-----|------|-----|---------|---------|
| **Contentful** | SaaS | REST, GraphQL | Cloud | Free tier, paid plans |
| **Strapi** | Self-hosted | REST, GraphQL | Self/Cloud | Open source, enterprise |
| **Sanity** | SaaS | GROQ, GraphQL | Cloud | Free tier, paid plans |
| **Prismic** | SaaS | REST, GraphQL | Cloud | Free tier, paid plans |
| **Directus** | Self-hosted | REST, GraphQL | Self/Cloud | Open source |

## Content Modeling

```typescript
// Example content model
interface BlogPost {
  id: string;
  title: string;
  slug: string;
  content: RichText;
  excerpt: string;
  author: Reference<Author>;
  categories: Reference<Category>[];
  featuredImage: Asset;
  publishedAt: Date;
  metadata: SEOMetadata;
}

interface Author {
  id: string;
  name: string;
  bio: string;
  avatar: Asset;
  socialLinks: SocialLink[];
}

interface Category {
  id: string;
  name: string;
  slug: string;
  description: string;
}

interface SEOMetadata {
  title: string;
  description: string;
  keywords: string[];
  ogImage: Asset;
}

interface Asset {
  id: string;
  url: string;
  title: string;
  description: string;
  width: number;
  height: number;
  contentType: string;
}
```

## API Integration

### REST API

```typescript
// services/cms-client.service.ts
import axios, { AxiosInstance } from 'axios';

export class CMSClient {
  private client: AxiosInstance;

  constructor(baseURL: string, apiKey: string) {
    this.client = axios.create({
      baseURL,
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      }
    });
  }

  async getEntries<T>(contentType: string, query?: QueryParams): Promise<T[]> {
    const response = await this.client.get('/entries', {
      params: {
        content_type: contentType,
        ...query
      }
    });

    return response.data.items;
  }

  async getEntry<T>(id: string): Promise<T> {
    const response = await this.client.get(`/entries/${id}`);
    return response.data;
  }

  async getAsset(id: string): Promise<Asset> {
    const response = await this.client.get(`/assets/${id}`);
    return response.data;
  }
}

interface QueryParams {
  limit?: number;
  skip?: number;
  order?: string;
  locale?: string;
  include?: number;
  [key: string]: any;
}
```

### GraphQL API

```typescript
// services/cms-graphql.service.ts
import { GraphQLClient } from 'graphql-request';

export class CMSGraphQLClient {
  private client: GraphQLClient;

  constructor(endpoint: string, apiKey: string) {
    this.client = new GraphQLClient(endpoint, {
      headers: {
        'Authorization': `Bearer ${apiKey}`
      }
    });
  }

  async getBlogPosts(limit: number = 10): Promise<BlogPost[]> {
    const query = `
      query GetBlogPosts($limit: Int!) {
        blogPostCollection(limit: $limit, order: publishedAt_DESC) {
          items {
            sys { id }
            title
            slug
            excerpt
            publishedAt
            author {
              name
              avatar {
                url
              }
            }
            featuredImage {
              url
              width
              height
            }
            categoriesCollection {
              items {
                name
                slug
              }
            }
          }
        }
      }
    `;

    const data = await this.client.request(query, { limit });
    return data.blogPostCollection.items;
  }

  async getBlogPost(slug: string): Promise<BlogPost> {
    const query = `
      query GetBlogPost($slug: String!) {
        blogPostCollection(where: { slug: $slug }, limit: 1) {
          items {
            sys { id }
            title
            slug
            content {
              json
            }
            excerpt
            publishedAt
            author {
              name
              bio
              avatar {
                url
              }
            }
            featuredImage {
              url
              width
              height
            }
          }
        }
      }
    `;

    const data = await this.client.request(query, { slug });
    return data.blogPostCollection.items[0];
  }
}
```

## Content Preview

```typescript
// lib/preview.ts
export class ContentPreview {
  async enablePreview(req: any, res: any): Promise<void> {
    // Check secret
    if (req.query.secret !== process.env.PREVIEW_SECRET) {
      return res.status(401).json({ message: 'Invalid token' });
    }

    // Enable preview mode
    res.setPreviewData({});

    // Redirect to the path
    res.redirect(req.query.slug || '/');
  }

  async disablePreview(req: any, res: any): Promise<void> {
    res.clearPreviewData();
    res.redirect('/');
  }

  async getPreviewContent(id: string, preview: boolean): Promise<any> {
    const client = new CMSClient(
      process.env.CMS_API_URL!,
      preview ? process.env.CMS_PREVIEW_KEY! : process.env.CMS_API_KEY!
    );

    return client.getEntry(id);
  }
}

// pages/api/preview.ts
export default async function handler(req: any, res: any) {
  const preview = new ContentPreview();
  await preview.enablePreview(req, res);
}

// pages/api/exit-preview.ts
export default async function handler(req: any, res: any) {
  const preview = new ContentPreview();
  await preview.disablePreview(req, res);
}
```

## Webhooks

```typescript
// pages/api/webhooks/cms.ts
import crypto from 'crypto';

export default async function handler(req: any, res: any) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  // Verify webhook signature
  if (!verifyWebhookSignature(req)) {
    return res.status(401).json({ message: 'Invalid signature' });
  }

  const event = req.body;

  switch (event.type) {
    case 'Entry.publish':
      await handleEntryPublished(event);
      break;

    case 'Entry.unpublish':
      await handleEntryUnpublished(event);
      break;

    case 'Entry.delete':
      await handleEntryDeleted(event);
      break;

    case 'Asset.publish':
      await handleAssetPublished(event);
      break;
  }

  res.json({ received: true });
}

function verifyWebhookSignature(req: any): boolean {
  const signature = req.headers['x-webhook-signature'];
  const secret = process.env.WEBHOOK_SECRET!;

  const hash = crypto
    .createHmac('sha256', secret)
    .update(JSON.stringify(req.body))
    .digest('hex');

  return hash === signature;
}

async function handleEntryPublished(event: any): Promise<void> {
  const { entryId, contentType } = event;

  // Revalidate pages
  await fetch(`${process.env.APP_URL}/api/revalidate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      contentType,
      entryId
    })
  });
}

async function handleEntryUnpublished(event: any): Promise<void> {
  // Implementation
}

async function handleEntryDeleted(event: any): Promise<void> {
  // Implementation
}

async function handleAssetPublished(event: any): Promise<void> {
  // Implementation
}
```

## Image Optimization

```typescript
// components/OptimizedImage.tsx
import Image from 'next/image';

interface OptimizedImageProps {
  src: string;
  alt: string;
  width: number;
  height: number;
  quality?: number;
  priority?: boolean;
}

export function OptimizedImage({
  src,
  alt,
  width,
  height,
  quality = 75,
  priority = false
}: OptimizedImageProps) {
  // Transform CMS image URL
  const optimizedSrc = transformImageUrl(src, { width, quality });

  return (
    <Image
      src={optimizedSrc}
      alt={alt}
      width={width}
      height={height}
      quality={quality}
      priority={priority}
      placeholder="blur"
      blurDataURL={generateBlurDataUrl(src)}
    />
  );
}

function transformImageUrl(url: string, options: ImageOptions): string {
  const params = new URLSearchParams({
    w: options.width?.toString() || '',
    q: options.quality?.toString() || '75',
    fm: options.format || 'webp'
  });

  return `${url}?${params}`;
}

function generateBlurDataUrl(url: string): string {
  // Generate low-quality placeholder
  return transformImageUrl(url, { width: 10, quality: 10 });
}

interface ImageOptions {
  width?: number;
  height?: number;
  quality?: number;
  format?: 'webp' | 'jpg' | 'png';
}
```

## Multi-language Content

```typescript
// lib/i18n.ts
export class I18nContent {
  async getLocalizedContent<T>(
    id: string,
    locale: string
  ): Promise<T> {
    const client = new CMSClient(
      process.env.CMS_API_URL!,
      process.env.CMS_API_KEY!
    );

    return client.getEntry<T>(id, { locale });
  }

  async getAllLocales(): Promise<string[]> {
    return ['en-US', 'th-TH', 'ja-JP'];
  }

  async getLocalizedPaths(contentType: string): Promise<LocalizedPath[]> {
    const locales = await this.getAllLocales();
    const paths: LocalizedPath[] = [];

    for (const locale of locales) {
      const entries = await this.getEntries(contentType, { locale });
      
      entries.forEach(entry => {
        paths.push({
          params: { slug: entry.slug },
          locale
        });
      });
    }

    return paths;
  }
}

interface LocalizedPath {
  params: { slug: string };
  locale: string;
}

// pages/[slug].tsx
export async function getStaticPaths() {
  const i18n = new I18nContent();
  const paths = await i18n.getLocalizedPaths('blogPost');

  return {
    paths,
    fallback: 'blocking'
  };
}

export async function getStaticProps({ params, locale }: any) {
  const i18n = new I18nContent();
  const post = await i18n.getLocalizedContent(params.slug, locale);

  return {
    props: { post },
    revalidate: 60
  };
}
```

## Content Versioning

```typescript
// lib/versioning.ts
export class ContentVersioning {
  async getVersionHistory(entryId: string): Promise<Version[]> {
    const response = await fetch(
      `${process.env.CMS_API_URL}/entries/${entryId}/versions`,
      {
        headers: {
          'Authorization': `Bearer ${process.env.CMS_API_KEY}`
        }
      }
    );

    return response.json();
  }

  async getVersion(entryId: string, versionId: string): Promise<any> {
    const response = await fetch(
      `${process.env.CMS_API_URL}/entries/${entryId}/versions/${versionId}`,
      {
        headers: {
          'Authorization': `Bearer ${process.env.CMS_API_KEY}`
        }
      }
    );

    return response.json();
  }

  async compareVersions(
    entryId: string,
    version1: string,
    version2: string
  ): Promise<VersionDiff> {
    const [v1, v2] = await Promise.all([
      this.getVersion(entryId, version1),
      this.getVersion(entryId, version2)
    ]);

    return this.diff(v1, v2);
  }

  private diff(v1: any, v2: any): VersionDiff {
    // Implementation
    return {
      added: [],
      removed: [],
      modified: []
    };
  }
}

interface Version {
  id: string;
  createdAt: Date;
  createdBy: string;
  changes: string;
}

interface VersionDiff {
  added: string[];
  removed: string[];
  modified: Array<{ field: string; old: any; new: any }>;
}
```

## Caching Strategies

```typescript
// lib/cache.ts
import { Redis } from 'ioredis';

export class CMSCache {
  private redis: Redis;

  constructor() {
    this.redis = new Redis(process.env.REDIS_URL!);
  }

  async getCachedContent<T>(key: string): Promise<T | null> {
    const cached = await this.redis.get(key);
    return cached ? JSON.parse(cached) : null;
  }

  async setCachedContent(key: string, data: any, ttl: number = 3600): Promise<void> {
    await this.redis.setex(key, ttl, JSON.stringify(data));
  }

  async invalidateCache(pattern: string): Promise<void> {
    const keys = await this.redis.keys(pattern);
    if (keys.length > 0) {
      await this.redis.del(...keys);
    }
  }

  async getOrFetch<T>(
    key: string,
    fetcher: () => Promise<T>,
    ttl: number = 3600
  ): Promise<T> {
    const cached = await this.getCachedContent<T>(key);
    
    if (cached) {
      return cached;
    }

    const data = await fetcher();
    await this.setCachedContent(key, data, ttl);
    
    return data;
  }
}

// Usage
const cache = new CMSCache();

export async function getBlogPost(slug: string): Promise<BlogPost> {
  return cache.getOrFetch(
    `blog:${slug}`,
    () => cmsClient.getBlogPost(slug),
    3600 // 1 hour
  );
}
```

## Next.js Integration

```typescript
// lib/cms.ts
import { CMSGraphQLClient } from './cms-graphql';

const client = new CMSGraphQLClient(
  process.env.CMS_GRAPHQL_URL!,
  process.env.CMS_API_KEY!
);

export async function getAllPosts(): Promise<BlogPost[]> {
  return client.getBlogPosts(100);
}

export async function getPost(slug: string): Promise<BlogPost> {
  return client.getBlogPost(slug);
}

// pages/blog/[slug].tsx
import { GetStaticProps, GetStaticPaths } from 'next';

export const getStaticPaths: GetStaticPaths = async () => {
  const posts = await getAllPosts();

  return {
    paths: posts.map(post => ({
      params: { slug: post.slug }
    })),
    fallback: 'blocking'
  };
};

export const getStaticProps: GetStaticProps = async ({ params, preview = false }) => {
  const post = await getPost(params!.slug as string);

  if (!post) {
    return { notFound: true };
  }

  return {
    props: { post },
    revalidate: 60 // ISR: Revalidate every 60 seconds
  };
};

// pages/api/revalidate.ts
export default async function handler(req: any, res: any) {
  if (req.query.secret !== process.env.REVALIDATE_SECRET) {
    return res.status(401).json({ message: 'Invalid token' });
  }

  try {
    await res.revalidate(`/blog/${req.body.slug}`);
    return res.json({ revalidated: true });
  } catch (err) {
    return res.status(500).send('Error revalidating');
  }
}
```

## Best Practices

1. **Content Modeling** - Design flexible content models
2. **API Optimization** - Use GraphQL for precise data fetching
3. **Caching** - Implement multi-layer caching
4. **Image Optimization** - Use CDN and image transformations
5. **Preview Mode** - Enable content preview for editors
6. **Webhooks** - Use webhooks for real-time updates
7. **ISR** - Use Incremental Static Regeneration
8. **Localization** - Support multi-language content
9. **Versioning** - Track content versions
10. **Security** - Secure API keys and webhooks

---

## Quick Start

### Contentful Integration

```javascript
const contentful = require('contentful')

const client = contentful.createClient({
  space: process.env.CONTENTFUL_SPACE_ID,
  accessToken: process.env.CONTENTFUL_ACCESS_TOKEN
})

// Fetch entries
const entries = await client.getEntries({
  content_type: 'blogPost'
})
```

### Strapi Integration

```javascript
// Fetch from Strapi API
const response = await fetch('http://localhost:1337/api/posts', {
  headers: {
    'Authorization': `Bearer ${process.env.STRAPI_API_TOKEN}`
  }
})

const posts = await response.json()
```

---

## Production Checklist

- [ ] **Content Model**: Design flexible content models
- [ ] **API Keys**: Secure API keys and tokens
- [ ] **Caching**: Cache content appropriately
- [ ] **Webhooks**: Set up webhooks for content updates
- [ ] **Preview**: Preview mode for draft content
- [ ] **Localization**: Multi-language content support
- [ ] **Versioning**: Content versioning if needed
- [ ] **Media**: Media asset management
- [ ] **Performance**: Optimize API calls
- [ ] **Error Handling**: Handle API failures
- [ ] **Testing**: Test content fetching
- [ ] **Documentation**: Document content structure

---

## Anti-patterns

### ❌ Don't: Fetch on Every Render

```tsx
// ❌ Bad - Fetches every render
function BlogPost({ id }) {
  const [post, setPost] = useState(null)
  
  useEffect(() => {
    fetchPost(id).then(setPost)  // Fetches every time
  })
}
```

```tsx
// ✅ Good - Cache and memoize
const postCache = new Map()

function BlogPost({ id }) {
  const [post, setPost] = useState(postCache.get(id))
  
  useEffect(() => {
    if (!post) {
      fetchPost(id).then(p => {
        postCache.set(id, p)
        setPost(p)
      })
    }
  }, [id])
}
```

### ❌ Don't: Expose API Keys

```javascript
// ❌ Bad - API key in client code
const client = contentful.createClient({
  space: 'public-space-id',
  accessToken: 'secret-token'  // Exposed!
})
```

```javascript
// ✅ Good - Use backend proxy
// Frontend
fetch('/api/contentful/posts')

// Backend
app.get('/api/contentful/posts', async (req, res) => {
  const client = contentful.createClient({
    space: process.env.CONTENTFUL_SPACE_ID,
    accessToken: process.env.CONTENTFUL_ACCESS_TOKEN
  })
  const posts = await client.getEntries()
  res.json(posts)
})
```

---

## Integration Points

- **API Design** (`01-foundations/api-design/`) - API patterns
- **Caching** (`04-database/redis-caching/`) - Content caching
- **Contentful Integration** (`33-content-management/contentful-integration/`) - Specific platform

---

## Further Reading

- [Contentful](https://www.contentful.com/developers/docs/)
- [Strapi](https://docs.strapi.io/)
- [Sanity](https://www.sanity.io/docs)
- [Prismic](https://prismic.io/docs)
- [Next.js CMS](https://nextjs.org/docs/basic-features/data-fetching)
