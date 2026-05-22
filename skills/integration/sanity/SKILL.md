---
name: sanity
description: Manages structured content with Sanity headless CMS using GROQ queries and real-time collaboration. Use when building content-driven sites with customizable schemas, live previews, and flexible data modeling.
---

# Sanity CMS

Headless CMS with GROQ query language, real-time collaboration, and customizable Studio. Content as structured data with full TypeScript support.

## Quick Start

```bash
npm create sanity@latest
```

Follow prompts to create a project. This sets up:
- Sanity Studio (admin UI)
- Content schema
- API access

### Client Setup

```bash
npm install @sanity/client
```

```typescript
import { createClient } from '@sanity/client';

const client = createClient({
  projectId: 'your-project-id',
  dataset: 'production',
  apiVersion: '2024-01-01',
  useCdn: true,  // false for real-time data
});
```

## GROQ Queries

Graph-Relational Object Queries - Sanity's query language.

### Basic Query

```javascript
// Get all documents of a type
const posts = await client.fetch(`*[_type == "post"]`);

// With projection (select fields)
const posts = await client.fetch(`
  *[_type == "post"] {
    _id,
    title,
    slug,
    publishedAt
  }
`);
```

### Filtering

```groq
// Type matching
*[_type == "post"]

// Equality
*[_type == "post" && slug.current == "hello-world"]

// Comparisons
*[_type == "post" && publishedAt >= "2024-01-01"]

// Boolean operators
*[_type == "post" && (featured == true || priority > 5)]

// Text matching (with wildcard)
*[_type == "post" && title match "Next*"]

// Array membership
*[_type == "post" && "typescript" in tags]

// Field existence
*[_type == "post" && defined(featuredImage)]

// References
*[_type == "post" && references("author-id")]
```

### Projections

```groq
// Select specific fields
*[_type == "post"] {
  _id,
  title,
  "slug": slug.current
}

// Rename fields
*[_type == "post"] {
  "postTitle": title,
  "url": slug.current
}

// Include all fields plus extras
*[_type == "post"] {
  ...,
  "url": slug.current
}

// Expand references
*[_type == "post"] {
  title,
  author->  // Full author document
}

*[_type == "post"] {
  title,
  "authorName": author->name,  // Just the name
  "authorImage": author->image.asset->url
}

// Array of references
*[_type == "post"] {
  title,
  "categories": categories[]->title
}
```

### Ordering & Pagination

```groq
// Order ascending
*[_type == "post"] | order(publishedAt asc)

// Order descending
*[_type == "post"] | order(publishedAt desc)

// Multiple sort fields
*[_type == "post"] | order(featured desc, publishedAt desc)

// Pagination (0-based index)
*[_type == "post"] | order(publishedAt desc)[0...10]  // First 10

// Skip and take
*[_type == "post"] | order(publishedAt desc)[10...20]  // Next 10

// Single item
*[_type == "post" && slug.current == $slug][0]
```

### Joins & References

```groq
// Get posts with their authors
*[_type == "post"] {
  title,
  author->{
    name,
    image
  }
}

// Reverse reference (get author's posts)
*[_type == "author"] {
  name,
  "posts": *[_type == "post" && references(^._id)] {
    title,
    slug
  }
}

// Count references
*[_type == "author"] {
  name,
  "postCount": count(*[_type == "post" && references(^._id)])
}
```

### Parameters

```javascript
const post = await client.fetch(
  `*[_type == "post" && slug.current == $slug][0]`,
  { slug: 'hello-world' }
);

const posts = await client.fetch(
  `*[_type == "post" && publishedAt > $date] | order(publishedAt desc)[0...$limit]`,
  { date: '2024-01-01', limit: 10 }
);
```

## Schema Definition

Define content types in code.

```typescript
// schemas/post.ts
import { defineType, defineField } from 'sanity';

export const post = defineType({
  name: 'post',
  title: 'Post',
  type: 'document',
  fields: [
    defineField({
      name: 'title',
      title: 'Title',
      type: 'string',
      validation: (Rule) => Rule.required()
    }),
    defineField({
      name: 'slug',
      title: 'Slug',
      type: 'slug',
      options: {
        source: 'title',
        maxLength: 96
      }
    }),
    defineField({
      name: 'author',
      title: 'Author',
      type: 'reference',
      to: [{ type: 'author' }]
    }),
    defineField({
      name: 'publishedAt',
      title: 'Published at',
      type: 'datetime'
    }),
    defineField({
      name: 'body',
      title: 'Body',
      type: 'blockContent'  // Portable Text
    }),
    defineField({
      name: 'categories',
      title: 'Categories',
      type: 'array',
      of: [{ type: 'reference', to: { type: 'category' } }]
    })
  ],
  preview: {
    select: {
      title: 'title',
      author: 'author.name',
      media: 'mainImage'
    }
  }
});
```

### Register Schema

```typescript
// sanity.config.ts
import { defineConfig } from 'sanity';
import { deskTool } from 'sanity/desk';
import { post } from './schemas/post';
import { author } from './schemas/author';

export default defineConfig({
  name: 'default',
  title: 'My CMS',
  projectId: 'your-project-id',
  dataset: 'production',
  plugins: [deskTool()],
  schema: {
    types: [post, author]
  }
});
```

## Portable Text (Rich Text)

```typescript
// schemas/blockContent.ts
import { defineType, defineArrayMember } from 'sanity';

export const blockContent = defineType({
  name: 'blockContent',
  title: 'Block Content',
  type: 'array',
  of: [
    defineArrayMember({
      type: 'block',
      styles: [
        { title: 'Normal', value: 'normal' },
        { title: 'H2', value: 'h2' },
        { title: 'H3', value: 'h3' },
        { title: 'Quote', value: 'blockquote' }
      ],
      marks: {
        decorators: [
          { title: 'Bold', value: 'strong' },
          { title: 'Italic', value: 'em' },
          { title: 'Code', value: 'code' }
        ],
        annotations: [
          {
            name: 'link',
            type: 'object',
            fields: [{ name: 'href', type: 'url' }]
          }
        ]
      }
    }),
    defineArrayMember({
      type: 'image',
      options: { hotspot: true }
    })
  ]
});
```

### Render Portable Text

```bash
npm install @portabletext/react
```

```tsx
import { PortableText } from '@portabletext/react';

const components = {
  types: {
    image: ({ value }) => (
      <img src={urlFor(value).url()} alt={value.alt} />
    )
  },
  marks: {
    link: ({ children, value }) => (
      <a href={value.href}>{children}</a>
    )
  }
};

function PostBody({ body }) {
  return <PortableText value={body} components={components} />;
}
```

## Image Handling

```bash
npm install @sanity/image-url
```

```typescript
import imageUrlBuilder from '@sanity/image-url';

const builder = imageUrlBuilder(client);

function urlFor(source) {
  return builder.image(source);
}

// Usage
const imageUrl = urlFor(post.mainImage)
  .width(800)
  .height(600)
  .fit('crop')
  .url();

// Responsive images
const srcSet = [400, 800, 1200].map(
  (w) => `${urlFor(post.mainImage).width(w).url()} ${w}w`
).join(', ');
```

## TypeScript + Type Generation

```bash
npm install -D sanity-typegen
```

```bash
# Generate types from schema
npx sanity typegen generate
```

```typescript
import { defineQuery } from 'groq';
import type { Post } from './sanity.types';

const POSTS_QUERY = defineQuery(`*[_type == "post"] {
  _id,
  title,
  slug,
  author->
}`);

// Fully typed response
const posts = await client.fetch<Post[]>(POSTS_QUERY);
```

## Real-Time Updates

```javascript
// Listen to changes
const subscription = client
  .listen(`*[_type == "post"]`)
  .subscribe((update) => {
    console.log('Change:', update);
    // { transition: 'update', documentId: '...', result: {...} }
  });

// Stop listening
subscription.unsubscribe();
```

## Next.js Integration

```typescript
// lib/sanity.ts
import { createClient } from 'next-sanity';

export const client = createClient({
  projectId: process.env.NEXT_PUBLIC_SANITY_PROJECT_ID!,
  dataset: process.env.NEXT_PUBLIC_SANITY_DATASET!,
  apiVersion: '2024-01-01',
  useCdn: process.env.NODE_ENV === 'production',
});

// app/posts/[slug]/page.tsx
import { client } from '@/lib/sanity';

export async function generateStaticParams() {
  const slugs = await client.fetch(`*[_type == "post"].slug.current`);
  return slugs.map((slug: string) => ({ slug }));
}

export default async function PostPage({ params }: { params: { slug: string } }) {
  const post = await client.fetch(
    `*[_type == "post" && slug.current == $slug][0] {
      title,
      body,
      author->{ name }
    }`,
    { slug: params.slug }
  );

  return (
    <article>
      <h1>{post.title}</h1>
      <p>By {post.author.name}</p>
      <PortableText value={post.body} />
    </article>
  );
}
```

## Live Preview

```typescript
// Enable preview mode
import { definePreview } from 'next-sanity/preview';

const usePreview = definePreview({
  projectId: 'your-project-id',
  dataset: 'production',
});

// In component
function PostPreview({ slug }) {
  const post = usePreview(null, QUERY, { slug });
  return <Post post={post} />;
}
```

## Common GROQ Patterns

### Get by Slug
```groq
*[_type == "post" && slug.current == $slug][0]
```

### Paginated List
```groq
{
  "items": *[_type == "post"] | order(publishedAt desc)[$start...$end],
  "total": count(*[_type == "post"])
}
```

### Related Posts
```groq
*[_type == "post" && _id != $currentId && count((categories[]._ref)[@ in $categoryIds]) > 0][0...4]
```

### Full-Text Search
```groq
*[_type == "post" && [title, body[].children[].text] match $query]
```
