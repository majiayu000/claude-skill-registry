---
name: contentful
description: >-
  You are an expert in Contentful, the API-first content platform for
  enterprise teams. You help developers integrate Contentful's Content
  Delivery API (CDN-backed, read), Content Management API (write), and Content
  Preview API (draft content) into websites and apps — using typed content
  models, localization, rich text rendering, image transformations, and
  webhooks for build triggers.
license: Apache-2.0
compatibility: ''
metadata:
  author: terminal-skills
  version: 1.0.0
  category: Content Management
  tags:
    - headless-cms
    - saas
    - content-api
    - cdn
    - enterprise
    - graphql
---

# Contentful — Enterprise Headless CMS

You are an expert in Contentful, the API-first content platform for enterprise teams. You help developers integrate Contentful's Content Delivery API (CDN-backed, read), Content Management API (write), and Content Preview API (draft content) into websites and apps — using typed content models, localization, rich text rendering, image transformations, and webhooks for build triggers.

## Core Capabilities

### Content Delivery API

```typescript
// src/lib/contentful.ts — Contentful client setup
import { createClient, type Entry, type Asset } from "contentful";

const client = createClient({
  space: process.env.CONTENTFUL_SPACE_ID!,
  accessToken: process.env.CONTENTFUL_DELIVERY_TOKEN!,
  // For draft preview:
  // accessToken: process.env.CONTENTFUL_PREVIEW_TOKEN,
  // host: "preview.contentful.com",
});

// TypeScript interfaces matching content model
interface BlogPostFields {
  title: string;
  slug: string;
  excerpt: string;
  body: Document;                         // Rich Text
  featuredImage: Asset;
  author: Entry<AuthorFields>;
  tags: string[];
  publishDate: string;
}

// Fetch entries with type safety
async function getBlogPosts(limit = 10): Promise<Entry<BlogPostFields>[]> {
  const response = await client.getEntries<BlogPostFields>({
    content_type: "blogPost",
    order: ["-fields.publishDate"],
    limit,
    include: 2,                           // Resolve 2 levels of linked entries
    "fields.slug[exists]": true,          // Only entries with slug
  });
  return response.items;
}

async function getBlogPostBySlug(slug: string) {
  const response = await client.getEntries<BlogPostFields>({
    content_type: "blogPost",
    "fields.slug": slug,
    include: 3,
    limit: 1,
  });
  return response.items[0] || null;
}
```

### Rich Text Rendering

```tsx
// src/components/RichTextRenderer.tsx — Render Contentful rich text
import { documentToReactComponents, Options } from "@contentful/rich-text-react-renderer";
import { BLOCKS, INLINES, Document } from "@contentful/rich-text-types";
import Image from "next/image";

const renderOptions: Options = {
  renderNode: {
    [BLOCKS.EMBEDDED_ASSET]: (node) => {
      const { title, file } = node.data.target.fields;
      return (
        <Image
          src={`https:${file.url}`}
          alt={title}
          width={file.details.image.width}
          height={file.details.image.height}
          className="rounded-lg my-6"
        />
      );
    },
    [BLOCKS.EMBEDDED_ENTRY]: (node) => {
      const entry = node.data.target;
      if (entry.sys.contentType.sys.id === "codeBlock") {
        return (
          <pre className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
            <code className={`language-${entry.fields.language}`}>
              {entry.fields.code}
            </code>
          </pre>
        );
      }
      return null;
    },
    [INLINES.HYPERLINK]: (node, children) => (
      <a href={node.data.uri} className="text-blue-600 underline" target="_blank" rel="noopener">
        {children}
      </a>
    ),
  },
};

export function RichText({ document }: { document: Document }) {
  return <div className="prose max-w-none">{documentToReactComponents(document, renderOptions)}</div>;
}
```

### Image Transformations

```tsx
// Contentful Images API — resize, crop, format on the fly
function contentfulImageUrl(asset: Asset, options?: {
  width?: number;
  height?: number;
  quality?: number;
  format?: "webp" | "avif" | "jpg" | "png";
  fit?: "pad" | "fill" | "scale" | "crop" | "thumb";
  focus?: "face" | "center" | "top" | "bottom";
}) {
  const url = new URL(`https:${asset.fields.file.url}`);
  if (options?.width) url.searchParams.set("w", String(options.width));
  if (options?.height) url.searchParams.set("h", String(options.height));
  if (options?.quality) url.searchParams.set("q", String(options.quality));
  if (options?.format) url.searchParams.set("fm", options.format);
  if (options?.fit) url.searchParams.set("fit", options.fit);
  if (options?.focus) url.searchParams.set("f", options.focus);
  return url.toString();
}

// Usage: auto-optimize for web
<Image
  src={contentfulImageUrl(post.fields.featuredImage, {
    width: 800,
    format: "webp",
    quality: 80,
  })}
  alt={post.fields.title}
/>
```

## Installation

```bash
npm install contentful                     # Delivery SDK
npm install @contentful/rich-text-react-renderer  # Rich text → React
npm install contentful-management          # Management API (write)
```

## Best Practices

1. **Delivery API for reads** — Use CDN-backed Delivery API for production; Preview API only for draft preview
2. **Type generation** — Use `contentful-typescript-codegen` to generate TypeScript types from your content model
3. **Rich text renderer** — Always use `@contentful/rich-text-react-renderer` with custom renderers for embedded assets and entries
4. **Image API** — Transform images on the fly with URL params; serve WebP with quality 80 for 70% size reduction
5. **Webhooks for builds** — Configure webhooks to trigger Vercel/Netlify builds on publish; ISR for immediate updates
6. **Localization** — Set up locales in Contentful; fetch with `locale: "de"` or `locale: "*"` for all locales
7. **Include depth** — Set `include: 2-3` to resolve linked entries; avoids N+1 queries for related content
8. **Environment branching** — Use Contentful Environments (like Git branches) for content model changes; merge to master when ready
