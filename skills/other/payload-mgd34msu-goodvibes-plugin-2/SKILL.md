---
name: payload
description: Builds full-stack applications with Payload CMS, the Next.js-native headless CMS. Use when creating content-driven apps with TypeScript, code-first configuration, and full control over your backend.
---

# Payload CMS

Open-source, Next.js-native headless CMS with full TypeScript support. Code-first configuration, self-hosted, with REST and GraphQL APIs.

## Quick Start

```bash
npx create-payload-app@latest my-app
cd my-app
npm run dev
```

Opens admin at `http://localhost:3000/admin`.

## Project Structure

```
my-app/
  app/                    # Next.js app directory
    (payload)/           # Payload admin routes
  collections/           # Content type definitions
  payload.config.ts      # Main configuration
  payload-types.ts       # Generated types
```

## Configuration

```typescript
// payload.config.ts
import { buildConfig } from 'payload';
import { mongooseAdapter } from '@payloadcms/db-mongodb';
// or: import { postgresAdapter } from '@payloadcms/db-postgres';

import { Posts } from './collections/Posts';
import { Users } from './collections/Users';
import { Media } from './collections/Media';

export default buildConfig({
  admin: {
    user: Users.slug,
  },
  collections: [Users, Posts, Media],
  db: mongooseAdapter({
    url: process.env.MONGODB_URI!,
  }),
  typescript: {
    outputFile: 'payload-types.ts',
  },
  secret: process.env.PAYLOAD_SECRET!,
});
```

## Collections (Content Types)

```typescript
// collections/Posts.ts
import { CollectionConfig } from 'payload';

export const Posts: CollectionConfig = {
  slug: 'posts',
  admin: {
    useAsTitle: 'title',
    defaultColumns: ['title', 'status', 'publishedAt'],
  },
  access: {
    read: () => true,  // Public read
    create: ({ req }) => !!req.user,  // Authenticated only
    update: ({ req }) => !!req.user,
    delete: ({ req }) => !!req.user,
  },
  versions: {
    drafts: true,
  },
  fields: [
    {
      name: 'title',
      type: 'text',
      required: true,
    },
    {
      name: 'slug',
      type: 'text',
      unique: true,
      admin: {
        position: 'sidebar',
      },
      hooks: {
        beforeValidate: [
          ({ value, data }) => value || data?.title?.toLowerCase().replace(/\s+/g, '-'),
        ],
      },
    },
    {
      name: 'author',
      type: 'relationship',
      relationTo: 'users',
    },
    {
      name: 'publishedAt',
      type: 'date',
      admin: {
        position: 'sidebar',
      },
    },
    {
      name: 'status',
      type: 'select',
      options: [
        { label: 'Draft', value: 'draft' },
        { label: 'Published', value: 'published' },
      ],
      defaultValue: 'draft',
      admin: {
        position: 'sidebar',
      },
    },
    {
      name: 'content',
      type: 'richText',
    },
    {
      name: 'featuredImage',
      type: 'upload',
      relationTo: 'media',
    },
    {
      name: 'categories',
      type: 'relationship',
      relationTo: 'categories',
      hasMany: true,
    },
  ],
};
```

## Field Types

```typescript
// Text
{ name: 'title', type: 'text', required: true }

// Textarea
{ name: 'excerpt', type: 'textarea' }

// Rich Text (Lexical)
{ name: 'content', type: 'richText' }

// Number
{ name: 'price', type: 'number', min: 0 }

// Email
{ name: 'email', type: 'email' }

// Date
{ name: 'publishedAt', type: 'date' }

// Checkbox
{ name: 'featured', type: 'checkbox', defaultValue: false }

// Select
{
  name: 'status',
  type: 'select',
  options: [
    { label: 'Draft', value: 'draft' },
    { label: 'Published', value: 'published' },
  ],
}

// Radio
{
  name: 'type',
  type: 'radio',
  options: ['video', 'article', 'podcast'],
}

// Relationship
{
  name: 'author',
  type: 'relationship',
  relationTo: 'users',
}

// Upload
{
  name: 'image',
  type: 'upload',
  relationTo: 'media',
}

// Array (repeatable)
{
  name: 'gallery',
  type: 'array',
  fields: [
    { name: 'image', type: 'upload', relationTo: 'media' },
    { name: 'caption', type: 'text' },
  ],
}

// Group (nested object)
{
  name: 'meta',
  type: 'group',
  fields: [
    { name: 'title', type: 'text' },
    { name: 'description', type: 'textarea' },
  ],
}

// Blocks (flexible content)
{
  name: 'layout',
  type: 'blocks',
  blocks: [HeroBlock, ContentBlock, CTABlock],
}
```

## Blocks

```typescript
// blocks/Hero.ts
import { Block } from 'payload';

export const HeroBlock: Block = {
  slug: 'hero',
  labels: {
    singular: 'Hero',
    plural: 'Heroes',
  },
  fields: [
    { name: 'heading', type: 'text', required: true },
    { name: 'subheading', type: 'text' },
    { name: 'image', type: 'upload', relationTo: 'media' },
    {
      name: 'cta',
      type: 'group',
      fields: [
        { name: 'label', type: 'text' },
        { name: 'link', type: 'text' },
      ],
    },
  ],
};
```

## Access Control

```typescript
export const Posts: CollectionConfig = {
  slug: 'posts',
  access: {
    // Function-based access
    read: ({ req }) => {
      // Published posts are public
      if (!req.user) {
        return { status: { equals: 'published' } };
      }
      // Logged in users see all
      return true;
    },

    create: ({ req }) => !!req.user,

    update: ({ req }) => {
      if (!req.user) return false;
      // Admins can update all
      if (req.user.role === 'admin') return true;
      // Authors can only update own posts
      return {
        author: { equals: req.user.id },
      };
    },

    delete: ({ req }) => req.user?.role === 'admin',
  },
};
```

## Hooks

```typescript
export const Posts: CollectionConfig = {
  slug: 'posts',
  hooks: {
    beforeChange: [
      async ({ data, req, operation }) => {
        if (operation === 'create') {
          data.author = req.user?.id;
        }
        return data;
      },
    ],

    afterChange: [
      async ({ doc, operation }) => {
        if (operation === 'create') {
          // Send notification, revalidate cache, etc.
          await revalidatePath('/posts');
        }
      },
    ],

    beforeRead: [
      async ({ doc, req }) => {
        // Transform document before returning
        return doc;
      },
    ],
  },
  fields: [/* ... */],
};
```

## REST API

Auto-generated at `/api/{collection}`.

```typescript
// Get all posts
const response = await fetch('/api/posts');
const { docs, totalDocs, page, limit } = await response.json();

// Get single post
const post = await fetch('/api/posts/123').then(r => r.json());

// Query with parameters
const params = new URLSearchParams({
  where: JSON.stringify({
    status: { equals: 'published' },
    publishedAt: { less_than: new Date().toISOString() },
  }),
  sort: '-publishedAt',
  limit: '10',
  page: '1',
  depth: '2',
});

const filtered = await fetch(`/api/posts?${params}`).then(r => r.json());
```

### Query Operators

```typescript
// Equals
{ field: { equals: 'value' } }

// Not equals
{ field: { not_equals: 'value' } }

// Greater/less than
{ field: { greater_than: 100 } }
{ field: { less_than: 100 } }
{ field: { greater_than_equal: 100 } }
{ field: { less_than_equal: 100 } }

// Contains (string)
{ field: { contains: 'text' } }

// In array
{ field: { in: ['a', 'b', 'c'] } }

// Not in array
{ field: { not_in: ['x', 'y'] } }

// Exists
{ field: { exists: true } }

// Logical operators
{
  or: [
    { status: { equals: 'published' } },
    { featured: { equals: true } },
  ],
}

{
  and: [
    { status: { equals: 'published' } },
    { category: { equals: 'tech' } },
  ],
}
```

## GraphQL API

Available at `/api/graphql`.

```graphql
query {
  Posts(
    where: { status: { equals: published } }
    sort: "-publishedAt"
    limit: 10
  ) {
    docs {
      id
      title
      slug
      author {
        name
      }
    }
    totalDocs
  }
}
```

## Local API (Server-Side)

Use in Server Components, API routes, or hooks.

```typescript
import { getPayload } from 'payload';
import config from '@payload-config';

const payload = await getPayload({ config });

// Find many
const posts = await payload.find({
  collection: 'posts',
  where: {
    status: { equals: 'published' },
  },
  sort: '-publishedAt',
  limit: 10,
  depth: 2,
});

// Find one
const post = await payload.findByID({
  collection: 'posts',
  id: '123',
  depth: 2,
});

// Create
const newPost = await payload.create({
  collection: 'posts',
  data: {
    title: 'New Post',
    content: '...',
  },
});

// Update
const updated = await payload.update({
  collection: 'posts',
  id: '123',
  data: {
    title: 'Updated Title',
  },
});

// Delete
await payload.delete({
  collection: 'posts',
  id: '123',
});
```

## TypeScript

Types are auto-generated to `payload-types.ts`.

```typescript
import { Post, User } from './payload-types';

// Fully typed
const posts: Post[] = await payload.find({
  collection: 'posts',
});

posts.forEach((post: Post) => {
  console.log(post.title);  // TypeScript knows this exists
});
```

## Next.js Integration

```typescript
// app/posts/page.tsx
import { getPayload } from 'payload';
import config from '@payload-config';

export default async function PostsPage() {
  const payload = await getPayload({ config });

  const { docs: posts } = await payload.find({
    collection: 'posts',
    where: { status: { equals: 'published' } },
    sort: '-publishedAt',
  });

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>
          <a href={`/posts/${post.slug}`}>{post.title}</a>
        </li>
      ))}
    </ul>
  );
}
```

```typescript
// app/posts/[slug]/page.tsx
import { getPayload } from 'payload';
import config from '@payload-config';
import { notFound } from 'next/navigation';

export async function generateStaticParams() {
  const payload = await getPayload({ config });
  const { docs } = await payload.find({ collection: 'posts' });

  return docs.map((post) => ({ slug: post.slug }));
}

export default async function PostPage({ params }: { params: { slug: string } }) {
  const payload = await getPayload({ config });

  const { docs } = await payload.find({
    collection: 'posts',
    where: { slug: { equals: params.slug } },
    depth: 2,
  });

  if (!docs[0]) notFound();

  const post = docs[0];

  return (
    <article>
      <h1>{post.title}</h1>
      {/* Render content */}
    </article>
  );
}
```

## Media Collection

```typescript
// collections/Media.ts
import { CollectionConfig } from 'payload';

export const Media: CollectionConfig = {
  slug: 'media',
  upload: {
    staticDir: 'public/media',
    imageSizes: [
      {
        name: 'thumbnail',
        width: 400,
        height: 300,
        position: 'centre',
      },
      {
        name: 'card',
        width: 768,
        height: 1024,
        position: 'centre',
      },
    ],
    mimeTypes: ['image/*'],
  },
  fields: [
    { name: 'alt', type: 'text', required: true },
    { name: 'caption', type: 'text' },
  ],
};
```

## Globals (Singletons)

```typescript
// globals/Settings.ts
import { GlobalConfig } from 'payload';

export const Settings: GlobalConfig = {
  slug: 'settings',
  access: {
    read: () => true,
  },
  fields: [
    { name: 'siteName', type: 'text', required: true },
    { name: 'siteDescription', type: 'textarea' },
    {
      name: 'navigation',
      type: 'array',
      fields: [
        { name: 'label', type: 'text' },
        { name: 'link', type: 'text' },
      ],
    },
  ],
};

// Usage
const settings = await payload.findGlobal({ slug: 'settings' });
```

## Authentication

```typescript
// Login
const user = await payload.login({
  collection: 'users',
  data: {
    email: 'user@example.com',
    password: 'password',
  },
});

// Current user (in hooks/access control)
const user = req.user;

// Logout
await payload.logout({
  collection: 'users',
});
```

## Deployment

```bash
# Build
npm run build

# Start production
npm run start
```

Deploy to:
- **Vercel**: One-click with Neon database
- **Cloudflare**: Workers + D1 + R2
- **Self-hosted**: Any Node.js host

## Best Practices

1. **Use Local API** in Server Components for performance
2. **Define access control** for each collection
3. **Use hooks** for side effects (revalidation, notifications)
4. **Generate types** after schema changes: `npm run generate:types`
5. **Use drafts** for preview functionality
6. **Configure image sizes** to match your frontend needs
