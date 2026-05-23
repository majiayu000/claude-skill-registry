---
name: contentful
description: Manages content with Contentful headless CMS and Content Delivery API. Use when building content-driven applications with structured content models, CDN delivery, and enterprise content management.
---

# Contentful CMS

Enterprise headless CMS with Content Delivery API, global CDN, and powerful content modeling. Separate content from presentation for any frontend.

## Quick Start

```bash
npm install contentful
```

```typescript
import { createClient } from 'contentful';

const client = createClient({
  space: 'your_space_id',
  accessToken: 'your_access_token',  // Delivery API token
});

// Fetch entries
const entries = await client.getEntries();
console.log(entries.items);
```

## API Types

| API | Purpose | Token Type |
|-----|---------|------------|
| Content Delivery | Published content | Delivery token |
| Content Preview | Draft content | Preview token |
| Content Management | Create/update content | Management token |

```typescript
// Preview API client
const previewClient = createClient({
  space: 'your_space_id',
  accessToken: 'preview_access_token',
  host: 'preview.contentful.com'
});
```

## Fetching Entries

### Get All Entries

```typescript
const entries = await client.getEntries();

entries.items.forEach((entry) => {
  console.log(entry.fields);
});
```

### Filter by Content Type

```typescript
const posts = await client.getEntries({
  content_type: 'blogPost'
});
```

### Get Single Entry

```typescript
const entry = await client.getEntry('entry_id');
console.log(entry.fields.title);
```

### Query Parameters

```typescript
const posts = await client.getEntries({
  content_type: 'blogPost',

  // Field equality
  'fields.slug': 'hello-world',

  // Comparison operators
  'fields.publishDate[lte]': new Date().toISOString(),
  'fields.rating[gt]': 4,

  // Text search
  'fields.title[match]': 'javascript',

  // Existence
  'fields.featuredImage[exists]': true,

  // Array contains
  'fields.tags[in]': 'react,typescript',

  // Ordering
  order: '-fields.publishDate',  // desc
  order: 'fields.title',          // asc

  // Pagination
  skip: 0,
  limit: 10,

  // Locale
  locale: 'en-US',

  // Include linked entries (depth 1-10)
  include: 2,

  // Select specific fields
  select: 'fields.title,fields.slug,fields.author'
});
```

### Search Operators

```typescript
// [ne] - Not equal
'fields.status[ne]': 'draft'

// [in] - In array
'fields.category[in]': 'tech,design,business'

// [nin] - Not in array
'fields.category[nin]': 'archive'

// [exists] - Field exists
'fields.image[exists]': true

// [lt], [lte], [gt], [gte] - Comparisons
'fields.price[gte]': 100,
'fields.price[lte]': 500

// [match] - Full-text search
'fields.body[match]': 'react hooks'

// [near] - Location proximity
'fields.location[near]': '40.7128,-74.0060'

// [within] - Location within bounding box
'fields.location[within]': '40.7,-74.1,40.8,-74.0'
```

## Linked Entries (References)

```typescript
// Include linked entries (default: 1)
const posts = await client.getEntries({
  content_type: 'blogPost',
  include: 3  // Follow 3 levels of references
});

// Access linked author
posts.items.forEach((post) => {
  // Linked entries are resolved automatically
  const author = post.fields.author;
  console.log(author.fields.name);
});
```

## Assets (Images & Files)

```typescript
// Get all assets
const assets = await client.getAssets();

// Get single asset
const asset = await client.getAsset('asset_id');

console.log(asset.fields.title);
console.log(asset.fields.file.url);  // URL (add https:)

// Image transformations via URL
const imageUrl = `https:${asset.fields.file.url}?w=800&h=600&fit=fill`;
```

### Image API Parameters

```typescript
const url = `https:${image.fields.file.url}`;

// Resize
`${url}?w=800&h=600`

// Fit modes
`${url}?fit=pad`      // Add padding
`${url}?fit=fill`     // Resize to fit
`${url}?fit=scale`    // Scale proportionally
`${url}?fit=crop`     // Crop to size
`${url}?fit=thumb`    // Thumbnail

// Focus area (for crop)
`${url}?f=face`       // Focus on face
`${url}?f=faces`      // Focus on faces
`${url}?f=center`     // Center focus

// Format
`${url}?fm=webp`      // WebP
`${url}?fm=jpg`       // JPEG
`${url}?fm=png`       // PNG

// Quality (1-100)
`${url}?q=80`

// Combined
`${url}?w=400&h=300&fit=fill&fm=webp&q=80`
```

## Sync API

Keep local content in sync with delta updates.

```typescript
// Initial sync
const response = await client.sync({
  initial: true
});

// Store these
const { entries, assets, nextSyncToken } = response;

// Later: Get only changes
const deltaResponse = await client.sync({
  nextSyncToken: storedNextSyncToken
});

// Contains only changed/deleted items
const { entries, deletedEntries, assets, deletedAssets } = deltaResponse;
```

## Rich Text Rendering

```bash
npm install @contentful/rich-text-react-renderer @contentful/rich-text-types
```

```tsx
import { documentToReactComponents } from '@contentful/rich-text-react-renderer';
import { BLOCKS, INLINES } from '@contentful/rich-text-types';

const options = {
  renderNode: {
    [BLOCKS.EMBEDDED_ASSET]: (node) => {
      const { file, title } = node.data.target.fields;
      return <img src={`https:${file.url}`} alt={title} />;
    },
    [BLOCKS.EMBEDDED_ENTRY]: (node) => {
      const entry = node.data.target;
      // Render embedded entry
      return <Card data={entry.fields} />;
    },
    [INLINES.HYPERLINK]: (node, children) => {
      return <a href={node.data.uri} target="_blank">{children}</a>;
    }
  }
};

function RichText({ content }) {
  return <div>{documentToReactComponents(content, options)}</div>;
}
```

## TypeScript

### Generate Types

```bash
npm install -D cf-content-types-generator
```

```bash
npx cf-content-types-generator --out src/types/contentful.d.ts
```

### Type-Safe Queries

```typescript
import { createClient, Entry, EntryCollection } from 'contentful';
import { IBlogPost, IBlogPostFields } from './types/contentful';

const client = createClient({
  space: process.env.CONTENTFUL_SPACE_ID!,
  accessToken: process.env.CONTENTFUL_ACCESS_TOKEN!
});

// Typed response
const posts: EntryCollection<IBlogPostFields> = await client.getEntries({
  content_type: 'blogPost'
});

posts.items.forEach((post: Entry<IBlogPostFields>) => {
  console.log(post.fields.title);  // TypeScript knows this exists
});
```

## Next.js Integration

```typescript
// lib/contentful.ts
import { createClient } from 'contentful';

export const client = createClient({
  space: process.env.CONTENTFUL_SPACE_ID!,
  accessToken: process.env.CONTENTFUL_ACCESS_TOKEN!
});

export const previewClient = createClient({
  space: process.env.CONTENTFUL_SPACE_ID!,
  accessToken: process.env.CONTENTFUL_PREVIEW_TOKEN!,
  host: 'preview.contentful.com'
});

export function getClient(preview = false) {
  return preview ? previewClient : client;
}
```

```typescript
// app/posts/[slug]/page.tsx
import { client } from '@/lib/contentful';
import { documentToReactComponents } from '@contentful/rich-text-react-renderer';

export async function generateStaticParams() {
  const entries = await client.getEntries({
    content_type: 'blogPost',
    select: 'fields.slug'
  });

  return entries.items.map((entry) => ({
    slug: entry.fields.slug
  }));
}

export default async function PostPage({ params }: { params: { slug: string } }) {
  const entries = await client.getEntries({
    content_type: 'blogPost',
    'fields.slug': params.slug,
    include: 2
  });

  const post = entries.items[0];

  return (
    <article>
      <h1>{post.fields.title}</h1>
      <p>By {post.fields.author.fields.name}</p>
      {documentToReactComponents(post.fields.body)}
    </article>
  );
}
```

## Preview Mode (Next.js)

```typescript
// app/api/preview/route.ts
import { draftMode } from 'next/headers';
import { redirect } from 'next/navigation';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const secret = searchParams.get('secret');
  const slug = searchParams.get('slug');

  if (secret !== process.env.CONTENTFUL_PREVIEW_SECRET) {
    return new Response('Invalid token', { status: 401 });
  }

  draftMode().enable();
  redirect(`/posts/${slug}`);
}

// In page: use preview client when draftMode is enabled
import { draftMode } from 'next/headers';
import { getClient } from '@/lib/contentful';

export default async function Page({ params }) {
  const { isEnabled } = draftMode();
  const client = getClient(isEnabled);
  // ...
}
```

## Content Management API

For creating/updating content programmatically.

```bash
npm install contentful-management
```

```typescript
import { createClient } from 'contentful-management';

const client = createClient({
  accessToken: 'management_token'
});

// Get space and environment
const space = await client.getSpace('space_id');
const environment = await space.getEnvironment('master');

// Create entry
const entry = await environment.createEntry('blogPost', {
  fields: {
    title: { 'en-US': 'New Post' },
    slug: { 'en-US': 'new-post' },
    body: { 'en-US': { /* rich text */ } }
  }
});

// Publish
await entry.publish();

// Update entry
entry.fields.title['en-US'] = 'Updated Title';
await entry.update();

// Upload asset
const asset = await environment.createAssetFromFiles({
  fields: {
    title: { 'en-US': 'My Image' },
    file: {
      'en-US': {
        contentType: 'image/jpeg',
        fileName: 'image.jpg',
        file: fs.createReadStream('image.jpg')
      }
    }
  }
});

await asset.processForAllLocales();
await asset.publish();
```

## Webhooks

Configure in Contentful dashboard to trigger on:
- Entry publish/unpublish
- Asset upload/delete
- Content type changes

```typescript
// app/api/contentful-webhook/route.ts
export async function POST(request: Request) {
  const body = await request.json();

  // Verify webhook (optional but recommended)
  const signature = request.headers.get('x-contentful-signature');

  // Handle based on event type
  const { sys } = body;

  if (sys.type === 'Entry') {
    // Revalidate specific page
    await fetch(`/api/revalidate?path=/posts/${body.fields.slug['en-US']}`);
  }

  return new Response('OK');
}
```

## Best Practices

1. **Use preview API** for draft/unpublished content
2. **Set appropriate include depth** (default 1, max 10)
3. **Select only needed fields** for performance
4. **Use sync API** for large datasets
5. **Cache responses** - content doesn't change frequently
6. **Use webhooks** for on-demand revalidation
