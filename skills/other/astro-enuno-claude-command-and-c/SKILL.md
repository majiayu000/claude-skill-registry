---
name: astro
version: 1.0.0
description: Astro web framework for content-focused websites with Islands architecture, partial hydration, content collections, and multi-framework support
---

# Astro Skill

Comprehensive assistance with Astro web framework development, including components, Islands architecture, content collections, routing, SSR/SSG, and deployment.

## When to Use This Skill

This skill should be triggered when:
- Creating new Astro projects or components
- Working with Islands architecture and partial hydration
- Managing content collections and Markdown/MDX
- Implementing file-based routing and dynamic routes
- Configuring SSR adapters and deployment
- Adding integrations (React, Vue, Svelte, Tailwind)
- Optimizing images and assets
- Setting up view transitions

## Quick Start

### Create a New Project

```bash
# Interactive project creation
npm create astro@latest

# Create with template
npm create astro@latest my-project -- --template blog
npm create astro@latest my-project -- --template portfolio

# Skip prompts with defaults
npm create astro@latest my-project -- --yes
```

### CLI Commands

```bash
# Development server (hot reload)
npm run dev
# or: astro dev --port 3000 --open

# Build for production
npm run build
# or: astro build

# Preview production build
npm run preview
# or: astro preview

# Add integrations
npx astro add react
npx astro add tailwind
npx astro add netlify

# Type checking
astro check

# Generate TypeScript types
astro sync

# Environment info
astro info
```

### CLI Hotkeys

During development:
- `s + enter` - Sync content collections
- `o + enter` - Open in browser
- `q + enter` - Quit server

---

## Project Structure

```
my-astro-project/
├── src/
│   ├── pages/           # File-based routing (required)
│   │   ├── index.astro
│   │   ├── about.astro
│   │   └── blog/
│   │       ├── [slug].astro
│   │       └── index.astro
│   ├── components/      # Reusable UI components
│   │   ├── Header.astro
│   │   └── Card.astro
│   ├── layouts/         # Page templates
│   │   ├── BaseLayout.astro
│   │   └── BlogLayout.astro
│   ├── content/         # Content collections
│   │   └── blog/
│   │       └── post-1.md
│   ├── styles/          # Global styles
│   │   └── global.css
│   └── content.config.ts # Collection schemas
├── public/              # Static assets (unprocessed)
│   ├── favicon.ico
│   └── robots.txt
├── astro.config.mjs     # Astro configuration
├── tsconfig.json        # TypeScript config
└── package.json
```

**Key Directories:**
- `src/pages/` - **Required**. Each file becomes a route
- `src/components/` - Reusable Astro and framework components
- `src/layouts/` - Shared page templates with slots
- `src/content/` - Type-safe content collections
- `public/` - Static files copied as-is (no optimization)

---

## Astro Components

### Basic Component Structure

```astro
---
// Component Script (runs on server)
import Header from './Header.astro';
import { getCollection } from 'astro:content';

// Props with TypeScript
interface Props {
  title: string;
  description?: string;
}

const { title, description = "Default description" } = Astro.props;

// Fetch data
const posts = await getCollection('blog');
---

<!-- Component Template (HTML output) -->
<Header />

<main>
  <h1>{title}</h1>
  <p>{description}</p>

  <ul>
    {posts.map(post => (
      <li>
        <a href={`/blog/${post.slug}`}>{post.data.title}</a>
      </li>
    ))}
  </ul>
</main>

<style>
  /* Scoped by default */
  h1 {
    color: navy;
  }
</style>
```

### Props and Slots

```astro
---
// Card.astro
interface Props {
  title: string;
  variant?: 'default' | 'featured';
}

const { title, variant = 'default' } = Astro.props;
---

<article class:list={['card', variant]}>
  <h2>{title}</h2>

  <!-- Default slot -->
  <div class="content">
    <slot />
  </div>

  <!-- Named slots -->
  <footer>
    <slot name="footer">
      <p>Default footer content</p>
    </slot>
  </footer>
</article>

<!-- Usage -->
<Card title="My Card" variant="featured">
  <p>Card content goes here</p>
  <div slot="footer">
    <button>Learn More</button>
  </div>
</Card>
```

### Dynamic Classes and Styles

```astro
---
const isActive = true;
const theme = 'dark';
const accentColor = '#ff6600';
---

<!-- class:list for conditional classes -->
<div class:list={[
  'base-class',
  { 'is-active': isActive },
  theme === 'dark' && 'dark-mode'
]}>
  Content
</div>

<!-- CSS variables from props -->
<div class="themed">
  <slot />
</div>

<style define:vars={{ accentColor }}>
  .themed {
    border-color: var(--accentColor);
  }
</style>
```

---

## Pages and Routing

### File-Based Routing

```
src/pages/
├── index.astro          → /
├── about.astro          → /about
├── blog/
│   ├── index.astro      → /blog
│   └── [slug].astro     → /blog/:slug
├── [category]/
│   └── [id].astro       → /:category/:id
└── [...path].astro      → /* (catch-all)
```

### Static Pages

```astro
---
// src/pages/about.astro
import Layout from '../layouts/Layout.astro';
---

<Layout title="About Us">
  <h1>About Us</h1>
  <p>Welcome to our site.</p>
</Layout>
```

### Dynamic Routes (Static Generation)

```astro
---
// src/pages/blog/[slug].astro
import { getCollection } from 'astro:content';
import BlogLayout from '../../layouts/BlogLayout.astro';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map(post => ({
    params: { slug: post.slug },
    props: { post }
  }));
}

const { post } = Astro.props;
const { Content } = await post.render();
---

<BlogLayout title={post.data.title}>
  <Content />
</BlogLayout>
```

### Dynamic Routes (SSR)

```astro
---
// src/pages/api/user/[id].ts (API endpoint)
export const prerender = false; // Enable SSR for this route

import type { APIRoute } from 'astro';

export const GET: APIRoute = async ({ params }) => {
  const { id } = params;
  const user = await fetchUser(id);

  return new Response(JSON.stringify(user), {
    headers: { 'Content-Type': 'application/json' }
  });
};
```

### Rest Parameters (Catch-All)

```astro
---
// src/pages/docs/[...path].astro
export async function getStaticPaths() {
  return [
    { params: { path: 'intro' } },           // /docs/intro
    { params: { path: 'guides/setup' } },    // /docs/guides/setup
    { params: { path: undefined } }          // /docs
  ];
}

const { path } = Astro.params;
---

<h1>Docs: {path || 'Home'}</h1>
```

### Pagination

```astro
---
// src/pages/blog/[page].astro
import { getCollection } from 'astro:content';

export async function getStaticPaths({ paginate }) {
  const posts = await getCollection('blog');
  return paginate(posts, { pageSize: 10 });
}

const { page } = Astro.props;
---

<ul>
  {page.data.map(post => (
    <li><a href={`/blog/${post.slug}`}>{post.data.title}</a></li>
  ))}
</ul>

<nav>
  {page.url.prev && <a href={page.url.prev}>Previous</a>}
  <span>Page {page.currentPage} of {page.lastPage}</span>
  {page.url.next && <a href={page.url.next}>Next</a>}
</nav>
```

---

## Layouts

### Base Layout

```astro
---
// src/layouts/BaseLayout.astro
interface Props {
  title: string;
  description?: string;
}

const { title, description = "My Astro Site" } = Astro.props;
---

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content={description}>
  <title>{title}</title>
</head>
<body>
  <header>
    <nav>
      <a href="/">Home</a>
      <a href="/about">About</a>
      <a href="/blog">Blog</a>
    </nav>
  </header>

  <main>
    <slot />
  </main>

  <footer>
    <p>&copy; 2024 My Site</p>
  </footer>
</body>
</html>
```

### Markdown Layout

```astro
---
// src/layouts/BlogLayout.astro
import type { MarkdownLayoutProps } from 'astro';
import BaseLayout from './BaseLayout.astro';

type Props = MarkdownLayoutProps<{
  title: string;
  date: string;
  author: string;
}>;

const { frontmatter, headings } = Astro.props;
---

<BaseLayout title={frontmatter.title}>
  <article>
    <h1>{frontmatter.title}</h1>
    <p class="meta">
      By {frontmatter.author} on {frontmatter.date}
    </p>

    <!-- Table of Contents -->
    <nav class="toc">
      <h2>Contents</h2>
      <ul>
        {headings.map(h => (
          <li style={`margin-left: ${(h.depth - 2) * 1}rem`}>
            <a href={`#${h.slug}`}>{h.text}</a>
          </li>
        ))}
      </ul>
    </nav>

    <!-- Rendered Markdown content -->
    <slot />
  </article>
</BaseLayout>
```

### Nested Layouts

```astro
---
// src/layouts/DocsLayout.astro
import BaseLayout from './BaseLayout.astro';

const { title } = Astro.props;
---

<BaseLayout title={`${title} | Docs`}>
  <div class="docs-container">
    <aside class="sidebar">
      <slot name="sidebar" />
    </aside>
    <article class="content">
      <slot />
    </article>
  </div>
</BaseLayout>
```

---

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
    date: z.coerce.date(),
    author: z.string().default('Anonymous'),
    tags: z.array(z.string()).optional(),
    draft: z.boolean().default(false),
    image: z.string().optional(),
  }),
});

const authors = defineCollection({
  loader: glob({ pattern: '**/*.json', base: './src/content/authors' }),
  schema: z.object({
    name: z.string(),
    bio: z.string(),
    avatar: z.string(),
  }),
});

export const collections = { blog, authors };
```

### Content Files

```markdown
---
# src/content/blog/my-first-post.md
title: My First Post
description: Getting started with Astro
date: 2024-01-15
author: John Doe
tags: ["astro", "web"]
---

# Introduction

Welcome to my blog post about Astro!

## Why Astro?

Astro is great for content-focused websites...
```

### Query Collections

```astro
---
import { getCollection, getEntry } from 'astro:content';

// Get all posts
const allPosts = await getCollection('blog');

// Filter posts
const publishedPosts = await getCollection('blog', ({ data }) => {
  return !data.draft && data.date < new Date();
});

// Sort by date
const sortedPosts = publishedPosts.sort(
  (a, b) => b.data.date.valueOf() - a.data.date.valueOf()
);

// Get single entry
const post = await getEntry('blog', 'my-first-post');

// Render content
const { Content, headings } = await post.render();
---

<ul>
  {sortedPosts.map(post => (
    <li>
      <a href={`/blog/${post.id}`}>
        {post.data.title}
      </a>
      <time>{post.data.date.toLocaleDateString()}</time>
    </li>
  ))}
</ul>
```

---

## Islands Architecture

### Client Directives

```astro
---
import ReactCounter from './Counter.jsx';
import VueSlider from './Slider.vue';
import SvelteModal from './Modal.svelte';
---

<!-- Load immediately on page load -->
<ReactCounter client:load />

<!-- Load when browser is idle -->
<VueSlider client:idle />

<!-- Load when visible in viewport -->
<SvelteModal client:visible />

<!-- Load only on specific media query -->
<ReactCounter client:media="(max-width: 768px)" />

<!-- Load only (never hydrate) - useful for SSR-only -->
<ReactCounter client:only="react" />
```

### Directive Comparison

| Directive | Loads When | Use Case |
|-----------|------------|----------|
| `client:load` | Immediately | Critical interactivity |
| `client:idle` | Browser idle | Non-critical components |
| `client:visible` | In viewport | Below-the-fold content |
| `client:media` | Media matches | Responsive components |
| `client:only` | Client only | Skip SSR entirely |

### Framework Components

```astro
---
// Mix multiple frameworks
import ReactHeader from './Header.jsx';
import VueCard from './Card.vue';
import SvelteButton from './Button.svelte';
import SolidCounter from './Counter.tsx'; // Solid
---

<ReactHeader client:load />

<main>
  <VueCard client:visible>
    <p>Static content from Astro</p>
  </VueCard>

  <SvelteButton client:idle />
  <SolidCounter client:load initialCount={5} />
</main>
```

---

## View Transitions

### Enable View Transitions

```astro
---
// src/layouts/BaseLayout.astro
import { ClientRouter } from 'astro:transitions';
---

<html>
<head>
  <ClientRouter />
</head>
<body>
  <slot />
</body>
</html>
```

### Transition Directives

```astro
---
import { ClientRouter } from 'astro:transitions';
---

<!-- Named transitions for matching elements -->
<header transition:name="header" transition:animate="none">
  <h1 transition:name="site-title">My Site</h1>
</header>

<!-- Animation types -->
<main transition:animate="slide">
  <slot />
</main>

<!-- Persist state across navigation -->
<video transition:persist autoplay></video>
```

### Animation Options

```astro
<!-- Built-in animations -->
<div transition:animate="fade">Fade in/out</div>
<div transition:animate="slide">Slide left/right</div>
<div transition:animate="initial">Browser default</div>
<div transition:animate="none">No animation</div>

<!-- Custom animation -->
<div transition:animate={{
  old: {
    name: 'fadeOut',
    duration: '0.2s',
    easing: 'ease-out',
    fillMode: 'forwards'
  },
  new: {
    name: 'fadeIn',
    duration: '0.3s',
    easing: 'ease-in',
    fillMode: 'backwards'
  }
}}>
  Custom transition
</div>
```

### Programmatic Navigation

```astro
<script>
  import { navigate } from 'astro:transitions/client';

  document.querySelector('#my-button').addEventListener('click', () => {
    navigate('/new-page');
  });
</script>
```

### Lifecycle Events

```astro
<script>
  document.addEventListener('astro:page-load', () => {
    console.log('Page loaded');
  });

  document.addEventListener('astro:before-swap', () => {
    console.log('About to swap content');
  });

  document.addEventListener('astro:after-swap', () => {
    console.log('Content swapped');
  });
</script>
```

---

## Styling

### Scoped Styles (Default)

```astro
<h1>Hello World</h1>

<style>
  /* Automatically scoped to this component */
  h1 {
    color: blue;
    font-size: 2rem;
  }
</style>
```

### Global Styles

```astro
<!-- Opt out of scoping -->
<style is:global>
  body {
    font-family: system-ui;
  }
</style>

<!-- Or use :global() for specific rules -->
<style>
  :global(body) {
    margin: 0;
  }

  .container :global(p) {
    line-height: 1.6;
  }
</style>
```

### Import Stylesheets

```astro
---
// Import local CSS
import '../styles/global.css';

// Import from node_modules
import 'open-props/style.css';
---
```

### Tailwind CSS

```bash
# Add Tailwind integration
npx astro add tailwind
```

```astro
---
// Works out of the box after integration
---

<div class="container mx-auto p-4">
  <h1 class="text-3xl font-bold text-blue-600">
    Hello Tailwind!
  </h1>
</div>
```

### CSS Modules

```astro
---
import styles from './Component.module.css';
---

<div class={styles.container}>
  <h1 class={styles.title}>Hello</h1>
</div>
```

---

## Images

### Image Component

```astro
---
import { Image } from 'astro:assets';
import heroImage from '../assets/hero.jpg';
---

<!-- Local images (optimized) -->
<Image
  src={heroImage}
  alt="Hero image"
  width={800}
  height={600}
/>

<!-- Remote images (need authorization) -->
<Image
  src="https://example.com/image.jpg"
  alt="Remote image"
  width={400}
  height={300}
  inferSize
/>

<!-- Responsive images -->
<Image
  src={heroImage}
  alt="Responsive hero"
  widths={[320, 640, 1280]}
  sizes="(max-width: 768px) 100vw, 50vw"
/>
```

### Picture Component

```astro
---
import { Picture } from 'astro:assets';
import myImage from '../assets/photo.jpg';
---

<Picture
  src={myImage}
  formats={['avif', 'webp']}
  alt="Multi-format image"
  width={800}
  height={600}
/>
```

### Image Configuration

```javascript
// astro.config.mjs
export default defineConfig({
  image: {
    domains: ['example.com', 'images.unsplash.com'],
    remotePatterns: [{ protocol: 'https' }],
    service: {
      entrypoint: 'astro/assets/services/sharp'
    }
  }
});
```

---

## Data Fetching

### In Components

```astro
---
// Top-level await in component script
const response = await fetch('https://api.example.com/data');
const data = await response.json();

// GraphQL
const gqlResponse = await fetch('https://api.example.com/graphql', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: `
      query {
        posts {
          title
          slug
        }
      }
    `
  })
});
const { data: gqlData } = await gqlResponse.json();
---

<ul>
  {data.items.map(item => (
    <li>{item.name}</li>
  ))}
</ul>
```

### Pass to Framework Components

```astro
---
const posts = await fetch('https://api.example.com/posts')
  .then(res => res.json());
---

<ReactPostList posts={posts} client:load />
```

---

## Integrations

### Adding Integrations

```bash
# UI Frameworks
npx astro add react
npx astro add vue
npx astro add svelte
npx astro add solid
npx astro add preact

# Styling
npx astro add tailwind

# SSR Adapters
npx astro add netlify
npx astro add vercel
npx astro add cloudflare
npx astro add node

# Other
npx astro add mdx
npx astro add sitemap
npx astro add partytown
```

### Manual Configuration

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://example.com',
  integrations: [
    react(),
    tailwind({
      applyBaseStyles: false
    }),
    sitemap()
  ]
});
```

---

## SSR and Deployment

### Enable SSR

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import netlify from '@astrojs/netlify';

export default defineConfig({
  output: 'server', // Enable SSR for all pages
  adapter: netlify()
});
```

### Hybrid Rendering

```javascript
// astro.config.mjs
export default defineConfig({
  output: 'hybrid', // SSG by default, opt-in SSR
  adapter: netlify()
});
```

```astro
---
// src/pages/dynamic.astro
export const prerender = false; // This page uses SSR
---
```

### Server Features

```astro
---
// Access request data
const { headers, method, url } = Astro.request;

// Access cookies
const sessionId = Astro.cookies.get('session');
Astro.cookies.set('visited', 'true', {
  httpOnly: true,
  secure: true
});

// Redirect
if (!sessionId) {
  return Astro.redirect('/login', 302);
}

// Custom response
Astro.response.headers.set('Cache-Control', 'max-age=3600');
---
```

### API Endpoints

```typescript
// src/pages/api/hello.ts
import type { APIRoute } from 'astro';

export const GET: APIRoute = async ({ request }) => {
  return new Response(JSON.stringify({ message: 'Hello!' }), {
    headers: { 'Content-Type': 'application/json' }
  });
};

export const POST: APIRoute = async ({ request }) => {
  const body = await request.json();
  return new Response(JSON.stringify({ received: body }), {
    status: 201,
    headers: { 'Content-Type': 'application/json' }
  });
};
```

### Deployment

```bash
# Build for production
npm run build

# Deploy to various platforms
# Netlify
netlify deploy --prod --dir=dist

# Vercel
vercel --prod

# Cloudflare Pages
wrangler pages deploy dist
```

---

## Configuration

### astro.config.mjs

```javascript
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';
import netlify from '@astrojs/netlify';

export default defineConfig({
  // Site URL for sitemap, canonical URLs
  site: 'https://example.com',

  // Base path for subdirectory hosting
  base: '/my-app',

  // Output mode
  output: 'hybrid', // 'static' | 'server' | 'hybrid'

  // SSR adapter
  adapter: netlify(),

  // Integrations
  integrations: [react(), tailwind()],

  // Build options
  build: {
    inlineStylesheets: 'auto'
  },

  // Dev server
  server: {
    port: 3000,
    host: true
  },

  // Vite options
  vite: {
    plugins: []
  },

  // Markdown options
  markdown: {
    shikiConfig: {
      theme: 'github-dark'
    }
  },

  // Image service
  image: {
    domains: ['images.unsplash.com']
  },

  // Redirects
  redirects: {
    '/old-page': '/new-page',
    '/blog/[...slug]': '/articles/[...slug]'
  }
});
```

---

## Common Patterns

### Error Pages

```astro
---
// src/pages/404.astro
import Layout from '../layouts/Layout.astro';
---

<Layout title="Page Not Found">
  <h1>404 - Page Not Found</h1>
  <p>The page you're looking for doesn't exist.</p>
  <a href="/">Go Home</a>
</Layout>
```

```astro
---
// src/pages/500.astro (SSR only)
import Layout from '../layouts/Layout.astro';

const error = Astro.props.error;
---

<Layout title="Server Error">
  <h1>500 - Server Error</h1>
  <p>Something went wrong.</p>
  {import.meta.env.DEV && <pre>{error.message}</pre>}
</Layout>
```

### Environment Variables

```bash
# .env
PUBLIC_API_URL=https://api.example.com
SECRET_KEY=private_value
```

```astro
---
// Access in component script
const apiUrl = import.meta.env.PUBLIC_API_URL;
const secret = import.meta.env.SECRET_KEY; // Server-only
---

<!-- Only PUBLIC_ prefixed vars available in templates -->
<p>API: {import.meta.env.PUBLIC_API_URL}</p>
```

### RSS Feed

```typescript
// src/pages/rss.xml.ts
import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const posts = await getCollection('blog');

  return rss({
    title: 'My Blog',
    description: 'A blog about stuff',
    site: context.site,
    items: posts.map(post => ({
      title: post.data.title,
      pubDate: post.data.date,
      description: post.data.description,
      link: `/blog/${post.slug}/`
    }))
  });
}
```

---

## Resources

- [Astro Documentation](https://docs.astro.build/)
- [Astro Integrations](https://astro.build/integrations/)
- [Astro Themes](https://astro.build/themes/)
- [Astro GitHub](https://github.com/withastro/astro)
- [Astro Discord](https://astro.build/chat)

---

## Notes

- Components render to static HTML by default (zero JS)
- Use `client:*` directives for interactive components
- Content collections provide type-safe Markdown/MDX
- View transitions enable SPA-like navigation
- Supports React, Vue, Svelte, Solid, Preact simultaneously
- File-based routing with dynamic route support
- Built-in image optimization for `src/` assets
