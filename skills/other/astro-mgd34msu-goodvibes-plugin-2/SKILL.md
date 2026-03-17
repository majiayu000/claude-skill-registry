---
name: astro
description: Builds content-focused websites with Astro using islands architecture, content collections, and multi-framework support. Use when creating static sites, blogs, documentation, marketing pages, or content-heavy applications with minimal JavaScript.
---

# Astro

Content-focused web framework with islands architecture for building fast static and server-rendered websites with minimal JavaScript.

## Quick Start

**Create new project:**
```bash
npm create astro@latest my-site
cd my-site
npm run dev
```

**Essential file structure:**
```
src/
  pages/              # File-based routing
    index.astro       # Home page (/)
    about.astro       # /about
    blog/
      [slug].astro    # /blog/:slug
  components/         # Reusable components
  layouts/            # Page layouts
  content/            # Content collections
    blog/             # Blog posts collection
  styles/             # Global styles
public/               # Static assets
astro.config.mjs      # Astro configuration
```

## Astro Components

### Basic Syntax

```astro
---
// Component Script (runs at build time)
import Header from '../components/Header.astro';
import Button from '../components/Button.tsx';

interface Props {
  title: string;
  description?: string;
}

const { title, description = 'Default description' } = Astro.props;

// Fetch data at build time
const response = await fetch('https://api.example.com/data');
const data = await response.json();
---

<!-- Component Template -->
<html lang="en">
  <head>
    <title>{title}</title>
    <meta name="description" content={description} />
  </head>
  <body>
    <Header />
    <main>
      <h1>{title}</h1>
      <ul>
        {data.items.map((item) => (
          <li>{item.name}</li>
        ))}
      </ul>
      <!-- Interactive island -->
      <Button client:load>Click me</Button>
    </main>
  </body>
</html>

<style>
  /* Scoped CSS by default */
  h1 {
    color: navy;
    font-size: 2rem;
  }
</style>
```

### Props and Types

```astro
---
interface Props {
  title: string;
  tags: string[];
  publishDate: Date;
  featured?: boolean;
}

const { title, tags, publishDate, featured = false } = Astro.props;
---

<article class:list={['post', { featured }]}>
  <h2>{title}</h2>
  <time datetime={publishDate.toISOString()}>
    {publishDate.toLocaleDateString()}
  </time>
  <ul>
    {tags.map((tag) => <li>{tag}</li>)}
  </ul>
</article>
```

### Slots

```astro
---
// Card.astro
interface Props {
  title: string;
}
const { title } = Astro.props;
---

<div class="card">
  <header>
    <slot name="header">{title}</slot>
  </header>
  <main>
    <slot />  <!-- Default slot -->
  </main>
  <footer>
    <slot name="footer">Default footer</slot>
  </footer>
</div>
```

**Using slots:**
```astro
<Card title="My Card">
  <h3 slot="header">Custom Header</h3>
  <p>Main content goes here</p>
  <button slot="footer">Action</button>
</Card>
```

## Islands Architecture

### Client Directives

Components are static by default. Add `client:*` directives for interactivity:

| Directive | When JavaScript Loads |
|-----------|----------------------|
| `client:load` | Immediately on page load |
| `client:idle` | When browser becomes idle |
| `client:visible` | When component enters viewport |
| `client:media` | When media query matches |
| `client:only` | Skip SSR, client render only |

```astro
---
import Counter from '../components/Counter.tsx';
import Newsletter from '../components/Newsletter.vue';
import Comments from '../components/Comments.svelte';
---

<!-- Load immediately (above fold, critical) -->
<Counter client:load />

<!-- Load when idle (non-critical) -->
<Newsletter client:idle />

<!-- Load when visible (below fold) -->
<Comments client:visible />

<!-- Load on mobile only -->
<MobileMenu client:media="(max-width: 768px)" />

<!-- React-only, no SSR -->
<ReactChart client:only="react" />
```

### Framework Integrations

```bash
# Add React
npx astro add react

# Add Vue
npx astro add vue

# Add Svelte
npx astro add svelte

# Add SolidJS
npx astro add solid
```

**Using multiple frameworks:**
```astro
---
import ReactComponent from '../components/ReactComponent.tsx';
import VueComponent from '../components/VueComponent.vue';
import SvelteComponent from '../components/SvelteComponent.svelte';
---

<ReactComponent client:load />
<VueComponent client:visible />
<SvelteComponent client:idle />
```

## File-Based Routing

### Static Routes

```
src/pages/
  index.astro          # /
  about.astro          # /about
  contact.astro        # /contact
  blog/
    index.astro        # /blog
    first-post.astro   # /blog/first-post
```

### Dynamic Routes

```astro
---
// src/pages/blog/[slug].astro
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map((post) => ({
    params: { slug: post.slug },
    props: { post },
  }));
}

const { post } = Astro.props;
const { Content } = await post.render();
---

<article>
  <h1>{post.data.title}</h1>
  <Content />
</article>
```

### Rest Parameters

```astro
---
// src/pages/docs/[...slug].astro
// Matches /docs, /docs/intro, /docs/guides/getting-started

export function getStaticPaths() {
  return [
    { params: { slug: undefined } },  // /docs
    { params: { slug: 'intro' } },     // /docs/intro
    { params: { slug: 'guides/start' } }, // /docs/guides/start
  ];
}

const { slug } = Astro.params;
---
```

## Content Collections

### Define Collections

```typescript
// src/content.config.ts
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    heroImage: z.string().optional(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

const authors = defineCollection({
  loader: glob({ pattern: '**/*.json', base: './src/content/authors' }),
  schema: z.object({
    name: z.string(),
    bio: z.string(),
    avatar: z.string(),
    social: z.object({
      twitter: z.string().optional(),
      github: z.string().optional(),
    }),
  }),
});

export const collections = { blog, authors };
```

### Query Collections

```astro
---
import { getCollection, getEntry } from 'astro:content';

// Get all published posts
const allPosts = await getCollection('blog', ({ data }) => {
  return data.draft !== true;
});

// Sort by date
const sortedPosts = allPosts.sort(
  (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
);

// Get single entry
const featuredPost = await getEntry('blog', 'featured-post');
---

<ul>
  {sortedPosts.map((post) => (
    <li>
      <a href={`/blog/${post.slug}`}>{post.data.title}</a>
    </li>
  ))}
</ul>
```

### Render Content

```astro
---
import { getEntry } from 'astro:content';

const post = await getEntry('blog', 'my-post');
const { Content, headings } = await post.render();
---

<article>
  <h1>{post.data.title}</h1>
  <nav>
    <h2>Table of Contents</h2>
    <ul>
      {headings.map((h) => (
        <li>
          <a href={`#${h.slug}`}>{h.text}</a>
        </li>
      ))}
    </ul>
  </nav>
  <Content />
</article>
```

## Layouts

### Basic Layout

```astro
---
// src/layouts/BaseLayout.astro
interface Props {
  title: string;
  description?: string;
}

const { title, description = 'My Astro site' } = Astro.props;
---

<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width" />
    <meta name="description" content={description} />
    <title>{title}</title>
  </head>
  <body>
    <header>
      <nav><!-- Navigation --></nav>
    </header>
    <main>
      <slot />
    </main>
    <footer><!-- Footer --></footer>
  </body>
</html>
```

**Using layouts:**
```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
---

<BaseLayout title="Home">
  <h1>Welcome!</h1>
  <p>This is the home page.</p>
</BaseLayout>
```

### Markdown Layout

```astro
---
// src/layouts/BlogPost.astro
import BaseLayout from './BaseLayout.astro';
import { type CollectionEntry } from 'astro:content';

interface Props {
  post: CollectionEntry<'blog'>;
}

const { post } = Astro.props;
const { title, pubDate, heroImage } = post.data;
---

<BaseLayout title={title}>
  <article>
    {heroImage && <img src={heroImage} alt="" />}
    <h1>{title}</h1>
    <time datetime={pubDate.toISOString()}>
      {pubDate.toLocaleDateString()}
    </time>
    <slot />
  </article>
</BaseLayout>
```

## Server-Side Rendering

### Enable SSR

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import node from '@astrojs/node';

export default defineConfig({
  output: 'server', // or 'hybrid'
  adapter: node({
    mode: 'standalone',
  }),
});
```

### Server Endpoints

```typescript
// src/pages/api/posts.json.ts
import type { APIRoute } from 'astro';

export const GET: APIRoute = async ({ request }) => {
  const posts = await getPosts();
  return new Response(JSON.stringify(posts), {
    headers: { 'Content-Type': 'application/json' },
  });
};

export const POST: APIRoute = async ({ request }) => {
  const data = await request.json();
  const post = await createPost(data);
  return new Response(JSON.stringify(post), {
    status: 201,
    headers: { 'Content-Type': 'application/json' },
  });
};
```

### Hybrid Rendering

```javascript
// astro.config.mjs
export default defineConfig({
  output: 'hybrid', // Static by default, opt-in to SSR
});
```

```astro
---
// This page renders on each request
export const prerender = false;

const user = await getUser(Astro.cookies.get('session'));
---
```

## Styling

### Scoped Styles

```astro
<style>
  /* Scoped to this component only */
  h1 {
    color: red;
  }
</style>
```

### Global Styles

```astro
<style is:global>
  /* Applies globally */
  body {
    font-family: sans-serif;
  }
</style>
```

### CSS Variables

```astro
---
const { color = 'blue' } = Astro.props;
---

<div class="box">Content</div>

<style define:vars={{ color }}>
  .box {
    background-color: var(--color);
  }
</style>
```

### Tailwind CSS

```bash
npx astro add tailwind
```

```astro
<div class="flex items-center justify-between p-4 bg-blue-500">
  <h1 class="text-2xl font-bold text-white">Hello</h1>
</div>
```

## View Transitions

```astro
---
import { ViewTransitions } from 'astro:transitions';
---

<html>
  <head>
    <ViewTransitions />
  </head>
  <body>
    <header transition:persist>
      <!-- Persists across page navigations -->
    </header>
    <main transition:animate="slide">
      <slot />
    </main>
  </body>
</html>
```

**Custom transitions:**
```astro
<div transition:name="hero" transition:animate="fade">
  <img src={heroImage} alt="" />
</div>
```

## Image Optimization

```astro
---
import { Image } from 'astro:assets';
import heroImage from '../assets/hero.png';
---

<!-- Optimized image -->
<Image src={heroImage} alt="Hero" />

<!-- With dimensions -->
<Image src={heroImage} alt="Hero" width={800} height={600} />

<!-- Remote image -->
<Image
  src="https://example.com/image.jpg"
  alt="Remote"
  width={400}
  height={300}
/>
```

## Environment Variables

```bash
# .env
PUBLIC_API_URL=https://api.example.com
SECRET_KEY=abc123
```

```astro
---
// Server-side (secret)
const secret = import.meta.env.SECRET_KEY;

// Client-side (public)
const apiUrl = import.meta.env.PUBLIC_API_URL;
---
```

## Best Practices

1. **Default to static** - Only add interactivity where needed
2. **Use content collections** - For any structured content
3. **Lazy load islands** - Use `client:visible` for below-fold content
4. **Colocate styles** - Use scoped styles in components
5. **Optimize images** - Use `astro:assets` for automatic optimization

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Adding `client:*` everywhere | Only for truly interactive components |
| Large client bundles | Split into smaller islands |
| Not using content collections | For blogs, docs, use collections |
| Fetching in client components | Fetch in Astro component script |
| Ignoring `getStaticPaths` | Required for dynamic routes |

## Reference Files

- [references/content-collections.md](references/content-collections.md) - Advanced collection patterns
- [references/islands.md](references/islands.md) - Islands architecture deep dive
- [references/deployment.md](references/deployment.md) - Deployment options

## Templates

- [templates/page.astro](templates/page.astro) - Page component template
- [templates/layout.astro](templates/layout.astro) - Layout component template
