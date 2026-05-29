---
name: mdx
description: Creates content with MDX including Markdown with JSX, custom components, and frontmatter. Use when building content-heavy sites, documentation, blogs, or mixing Markdown with interactive components.
---

# MDX

Markdown for the component era - write JSX in Markdown documents.

## Quick Start

**Install (Next.js):**
```bash
npm install @next/mdx @mdx-js/loader @mdx-js/react
```

**Configure next.config.mjs:**
```javascript
import createMDX from '@next/mdx';

const withMDX = createMDX({
  extension: /\.mdx?$/,
  options: {
    remarkPlugins: [],
    rehypePlugins: [],
  },
});

export default withMDX({
  pageExtensions: ['js', 'jsx', 'ts', 'tsx', 'md', 'mdx'],
});
```

## Basic Usage

### MDX File

```mdx
---
title: Hello World
date: 2024-01-01
---

# {frontmatter.title}

This is **Markdown** with <span style={{color: 'red'}}>JSX</span>.

import { Button } from '@/components/ui/button'

<Button>Click me</Button>

## Features

- Write Markdown naturally
- Import and use React components
- Export data and components
```

### Use in Pages

```tsx
// app/blog/[slug]/page.tsx
import { notFound } from 'next/navigation';

async function getPost(slug: string) {
  try {
    const post = await import(`@/content/blog/${slug}.mdx`);
    return post;
  } catch {
    return null;
  }
}

export default async function BlogPost({
  params,
}: {
  params: { slug: string };
}) {
  const post = await getPost(params.slug);

  if (!post) {
    notFound();
  }

  const { default: Content, frontmatter } = post;

  return (
    <article>
      <h1>{frontmatter.title}</h1>
      <time>{frontmatter.date}</time>
      <Content />
    </article>
  );
}
```

## Frontmatter

### With gray-matter

```bash
npm install gray-matter
```

```typescript
// lib/mdx.ts
import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

const postsDirectory = path.join(process.cwd(), 'content/blog');

export function getPostBySlug(slug: string) {
  const fullPath = path.join(postsDirectory, `${slug}.mdx`);
  const fileContents = fs.readFileSync(fullPath, 'utf8');
  const { data, content } = matter(fileContents);

  return {
    slug,
    frontmatter: data,
    content,
  };
}

export function getAllPosts() {
  const slugs = fs.readdirSync(postsDirectory);

  return slugs
    .map((slug) => getPostBySlug(slug.replace(/\.mdx$/, '')))
    .sort((a, b) =>
      new Date(b.frontmatter.date).getTime() -
      new Date(a.frontmatter.date).getTime()
    );
}
```

### Type-safe Frontmatter

```typescript
// lib/mdx.ts
import { z } from 'zod';

const frontmatterSchema = z.object({
  title: z.string(),
  date: z.string().transform((s) => new Date(s)),
  description: z.string().optional(),
  tags: z.array(z.string()).default([]),
  published: z.boolean().default(true),
});

export type Frontmatter = z.infer<typeof frontmatterSchema>;

export function getPostBySlug(slug: string) {
  const { data, content } = matter(fileContents);
  const frontmatter = frontmatterSchema.parse(data);

  return { slug, frontmatter, content };
}
```

## Custom Components

### MDX Components Provider

```tsx
// components/mdx-components.tsx
import Image from 'next/image';
import Link from 'next/link';
import { Callout } from '@/components/callout';
import { CodeBlock } from '@/components/code-block';

export const mdxComponents = {
  // Override HTML elements
  h1: (props: any) => (
    <h1 className="text-4xl font-bold mt-8 mb-4" {...props} />
  ),
  h2: (props: any) => (
    <h2 className="text-3xl font-semibold mt-6 mb-3" {...props} />
  ),
  p: (props: any) => (
    <p className="leading-7 mb-4" {...props} />
  ),
  a: (props: any) => (
    <Link
      className="text-blue-600 hover:underline"
      {...props}
    />
  ),
  img: (props: any) => (
    <Image
      className="rounded-lg my-4"
      width={800}
      height={400}
      {...props}
    />
  ),
  pre: (props: any) => <CodeBlock {...props} />,
  code: (props: any) => (
    <code className="bg-gray-100 px-1 rounded" {...props} />
  ),

  // Custom components
  Callout,
  Image,
};
```

### Using Provider

```tsx
// app/layout.tsx
import { MDXProvider } from '@mdx-js/react';
import { mdxComponents } from '@/components/mdx-components';

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <MDXProvider components={mdxComponents}>
      {children}
    </MDXProvider>
  );
}
```

### App Router (Next.js 14+)

```tsx
// mdx-components.tsx (root level)
import type { MDXComponents } from 'mdx/types';
import { mdxComponents } from '@/components/mdx-components';

export function useMDXComponents(components: MDXComponents): MDXComponents {
  return {
    ...components,
    ...mdxComponents,
  };
}
```

## Plugins

### Remark Plugins (Markdown)

```bash
npm install remark-gfm remark-math
```

```javascript
// next.config.mjs
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';

const withMDX = createMDX({
  options: {
    remarkPlugins: [remarkGfm, remarkMath],
  },
});
```

### Rehype Plugins (HTML)

```bash
npm install rehype-slug rehype-autolink-headings rehype-pretty-code
```

```javascript
// next.config.mjs
import rehypeSlug from 'rehype-slug';
import rehypeAutolinkHeadings from 'rehype-autolink-headings';
import rehypePrettyCode from 'rehype-pretty-code';

const withMDX = createMDX({
  options: {
    rehypePlugins: [
      rehypeSlug,
      [rehypeAutolinkHeadings, { behavior: 'wrap' }],
      [rehypePrettyCode, { theme: 'github-dark' }],
    ],
  },
});
```

## Contentlayer (Recommended)

### Setup

```bash
npm install contentlayer next-contentlayer
```

```typescript
// contentlayer.config.ts
import { defineDocumentType, makeSource } from 'contentlayer/source-files';
import rehypePrettyCode from 'rehype-pretty-code';
import rehypeSlug from 'rehype-slug';
import remarkGfm from 'remark-gfm';

export const Post = defineDocumentType(() => ({
  name: 'Post',
  filePathPattern: 'blog/**/*.mdx',
  contentType: 'mdx',
  fields: {
    title: { type: 'string', required: true },
    date: { type: 'date', required: true },
    description: { type: 'string' },
    published: { type: 'boolean', default: true },
    tags: { type: 'list', of: { type: 'string' }, default: [] },
  },
  computedFields: {
    slug: {
      type: 'string',
      resolve: (post) => post._raw.sourceFileName.replace(/\.mdx$/, ''),
    },
    url: {
      type: 'string',
      resolve: (post) => `/blog/${post._raw.sourceFileName.replace(/\.mdx$/, '')}`,
    },
  },
}));

export default makeSource({
  contentDirPath: 'content',
  documentTypes: [Post],
  mdx: {
    remarkPlugins: [remarkGfm],
    rehypePlugins: [
      rehypeSlug,
      [rehypePrettyCode, { theme: 'github-dark' }],
    ],
  },
});
```

### Next.js Config

```javascript
// next.config.mjs
import { withContentlayer } from 'next-contentlayer';

export default withContentlayer({
  // Next.js config
});
```

### Usage

```tsx
// app/blog/[slug]/page.tsx
import { allPosts } from 'contentlayer/generated';
import { useMDXComponent } from 'next-contentlayer/hooks';
import { notFound } from 'next/navigation';
import { mdxComponents } from '@/components/mdx-components';

export async function generateStaticParams() {
  return allPosts.map((post) => ({
    slug: post.slug,
  }));
}

export default function PostPage({ params }: { params: { slug: string } }) {
  const post = allPosts.find((post) => post.slug === params.slug);

  if (!post) {
    notFound();
  }

  const MDXContent = useMDXComponent(post.body.code);

  return (
    <article>
      <h1>{post.title}</h1>
      <time>{post.date}</time>
      <MDXContent components={mdxComponents} />
    </article>
  );
}
```

## Remote MDX

### MDX Remote

```bash
npm install next-mdx-remote
```

```tsx
// app/blog/[slug]/page.tsx
import { MDXRemote } from 'next-mdx-remote/rsc';
import { mdxComponents } from '@/components/mdx-components';

async function getPost(slug: string) {
  const res = await fetch(`https://api.example.com/posts/${slug}`);
  return res.json();
}

export default async function PostPage({
  params,
}: {
  params: { slug: string };
}) {
  const post = await getPost(params.slug);

  return (
    <article>
      <h1>{post.title}</h1>
      <MDXRemote
        source={post.content}
        components={mdxComponents}
        options={{
          mdxOptions: {
            remarkPlugins: [],
            rehypePlugins: [],
          },
        }}
      />
    </article>
  );
}
```

## Interactive Components

### Code Playground

```mdx
import { Playground } from '@/components/playground'

<Playground
  code={`
function App() {
  const [count, setCount] = useState(0);
  return (
    <button onClick={() => setCount(c => c + 1)}>
      Count: {count}
    </button>
  );
}
`}
/>
```

### Tabs

```mdx
import { Tabs, Tab } from '@/components/tabs'

<Tabs>
  <Tab label="npm">
    ```bash
    npm install package-name
    ```
  </Tab>
  <Tab label="yarn">
    ```bash
    yarn add package-name
    ```
  </Tab>
  <Tab label="pnpm">
    ```bash
    pnpm add package-name
    ```
  </Tab>
</Tabs>
```

### Callouts

```tsx
// components/callout.tsx
interface CalloutProps {
  type?: 'info' | 'warning' | 'error';
  title?: string;
  children: React.ReactNode;
}

export function Callout({ type = 'info', title, children }: CalloutProps) {
  const styles = {
    info: 'bg-blue-50 border-blue-500',
    warning: 'bg-yellow-50 border-yellow-500',
    error: 'bg-red-50 border-red-500',
  };

  return (
    <div className={`border-l-4 p-4 my-4 ${styles[type]}`}>
      {title && <p className="font-bold">{title}</p>}
      {children}
    </div>
  );
}
```

```mdx
<Callout type="warning" title="Note">
  This is an important warning message.
</Callout>
```

## Best Practices

1. **Use type-safe frontmatter** - Validate with Zod
2. **Centralize components** - Single MDX components file
3. **Add table of contents** - Parse headings
4. **Implement syntax highlighting** - Use rehype-pretty-code
5. **Cache compiled MDX** - Contentlayer handles this

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing imports in MDX | Use components provider |
| Slow builds | Use Contentlayer |
| No syntax highlighting | Add rehype-pretty-code |
| Broken links | Use next/link component |
| Large bundle | Lazy load components |

## Reference Files

- [references/plugins.md](references/plugins.md) - Remark/Rehype plugins
- [references/components.md](references/components.md) - Custom components
- [references/contentlayer.md](references/contentlayer.md) - Contentlayer setup
