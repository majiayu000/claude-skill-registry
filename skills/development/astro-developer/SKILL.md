---
name: astro-developer
description: Comprehensive Astro web framework development guidance for 2026. Use when building, configuring, or troubleshooting Astro projects; creating components; setting up routing; implementing islands architecture; working with React, Tailwind CSS, and Node.js integrations; testing; performance optimization; or deployment strategies. Includes TypeScript patterns, state management, API routes, and common pitfalls solutions.
---

# Astro Developer Skill

## Overview

Enables comprehensive Astro web development including component creation, project setup, configuration optimization, islands architecture implementation, content collections management, and deployment strategies. This skill emphasizes **Tailwind CSS-first development** for consistent, maintainable styling.

## Quick Start

Identify the task type and follow the corresponding workflow:

1. **New Project Setup** → Use "Project Initialization" workflow
2. **Component Development** → Use "Component Creation" guidelines with Tailwind CSS
3. **Testing Setup** → See [Testing Guide](references/testing-guide.md) for Vitest/Playwright
4. **Performance Optimization** → Use "Islands Architecture" patterns, see [Performance Guide](references/performance-optimization.md)
5. **State Management** → See [State Management Guide](references/state-management.md) for React islands
6. **Troubleshooting Issues** → See [Common Pitfalls Guide](references/common-pitfalls.md)
7. **Content Management** → Use "Content Collections" workflow
8. **Configuration & Deployment** → Use "Configuration" and "Deployment" sections

## Core Capabilities

### 1. Project Initialization & Setup

Create new Astro projects with optimal configurations:

```bash
# Basic Astro project
npm create astro@latest my-project

# With specific integrations
npm create astro@latest -- --add react --add tailwind --add mdx

# From template
npm create astro@latest -- --template blog
```

Essential project structure to create:

```
src/
├── components/          # Reusable Astro/UI framework components
├── layouts/            # Page layout templates
├── pages/              # File-based routing (REQUIRED)
├── styles/             # CSS/Sass files
├── content/            # Content collections (Markdown/MDX)
└── env.d.ts           # TypeScript environment types
public/                 # Static assets (robots.txt, favicon, etc)
astro.config.mjs       # Astro configuration
tsconfig.json         # TypeScript configuration
package.json          # Project dependencies and scripts
```

### 2. Component Creation

#### Astro Components (.astro)

Create server-rendered components with zero client-side JavaScript and Tailwind CSS styling:

```astro
---
// Component frontmatter - runs on server only
import { SITE_TITLE } from '@/config';
export interface Props {
  title?: string;
  published?: Date;
  variant?: 'default' | 'primary' | 'secondary';
}

const { title, published, variant = 'default' } = Astro.props;

const variantClasses = {
  default: 'bg-white dark:bg-gray-800',
  primary: 'bg-blue-500 dark:bg-blue-600 text-white',
  secondary: 'bg-gray-100 dark:bg-gray-700'
};
---

<!-- Component template - HTML with special syntax -->
<html lang="en" class="h-full">
  <head>
    <title>{title || SITE_TITLE}</title>
  </head>
  <body class="h-full m-0 font-sans leading-relaxed text-gray-900 dark:text-gray-100 bg-white dark:bg-gray-900">
    <main class={`${variantClasses[variant]} p-6 rounded-lg shadow-sm`}>
      {title && <h1 class="text-2xl font-bold mb-4">{title}</h1>}
      {published && (
        <time class="text-sm text-gray-600 dark:text-gray-400">
          {published.toLocaleDateString()}
        </time>
      )}
      <slot />  <!-- Children content -->
    </main>
  </body>
</html>
```

#### UI Framework Components (React, Vue, Svelte)

Add interactivity with client directives:

```astro
---
import ReactCounter from '@/components/ReactCounter.jsx';
import VueComponent from '@/components/VueComponent.vue';
import SvelteButton from '@/components/SvelteButton.svelte';
---

<!-- Load immediately -->
<ReactCounter client:load />

<!-- Load when visible in viewport -->
<SvelteButton client:visible />

<!-- Load when browser is idle -->
<VueComponent client:idle />

<!-- Load only on mobile -->
<ReactCounter client:load media="(max-width: 768px)" />
```

### 3. Islands Architecture

Implement optimal performance with selective hydration:

#### Client Islands Strategy

1. **Identify interactive components** - Carousels, forms, modals
2. **Choose appropriate client directive**:
   - `client:load` - Immediately (headers, critical features)
   - `client:idle` - When browser free (secondary features)
   - `client:visible` - When scrolled to (below-fold content)
   - `client:media` - Based on media query

```astro
---
import InteractiveHeader from '@/components/InteractiveHeader.astro';
import ImageCarousel from '@/components/ImageCarousel.jsx';
import NewsletterForm from '@/components/NewsletterForm.jsx';
import SocialShare from '@/components/SocialShare.jsx';
---

<!-- Above fold, critical interactivity -->
<InteractiveHeader client:load />

<!-- Content heavy, load when visible -->
<ImageCarousel client:visible />

<!-- Secondary feature, load when idle -->
<NewsletterForm client:idle />

<!-- Mobile-only interactivity -->
<SocialShare client:load media="(max-width: 768px)" />
```

#### Server Islands for Dynamic Content

Use `server:defer` for personalized/dynamic content:

```astro
---
import UserProfile from '@/components/UserProfile.astro';
import RecommendedPosts from '@/components/RecommendedPosts.astro';
---

<!-- Static content loads immediately -->
<main>
  <h1>Welcome to our blog</h1>
  <p>Explore our latest articles...</p>
</main>

<!-- Dynamic content loads in parallel -->
<aside>
  <!-- User's profile with personalized data -->
  <UserProfile server:defer />

  <!-- Recommended posts based on history -->
  <RecommendedPosts server:defer />
</aside>
```

### 4. Routing & Pages

#### File-Based Routing

Create pages using Astro's file-based routing:

```
src/pages/
├── index.astro           # → /
├── about.astro           # → /about
├── blog/
│   ├── index.astro       # → /blog
│   ├── [slug].astro      # → /blog/post-title
│   └── [...page].astro   # → /blog/2, /blog/3
└── api/
    └── posts.json.js     # → /api/posts (API endpoint)
```

#### Dynamic Routes

Handle dynamic segments with params:

```astro
---
// src/pages/blog/[slug].astro
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map((post) => ({
    params: { slug: post.slug },
    props: post,
  }));
}

const { Content, frontmatter } = Astro.props;
---

<h1>{frontmatter.title}</h1>
<p>Published: {frontmatter.pubDate.toLocaleDateString()}</p>
<Content />
```

#### API Routes

Create server endpoints:

```javascript
// src/pages/api/posts.json.js
export async function GET() {
  return Response.json({
    posts: [
      { id: 1, title: "First post" },
      { id: 2, title: "Second post" },
    ],
  });
}

export async function POST({ request }) {
  const data = await request.json();
  // Process form submission
  return Response.json({ success: true });
}
```

### 5. Content Collections

Organize and validate content with type safety:

#### Configure Collections

```typescript
// src/content/config.ts
import { defineCollection, z } from "astro:content";

const blog = defineCollection({
  schema: z.object({
    title: z.string(),
    pubDate: z.date(),
    updatedDate: z.date().optional(),
    description: z.string(),
    heroImage: z.string().optional(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

const projects = defineCollection({
  schema: z.object({
    title: z.string(),
    description: z.string(),
    startDate: z.date(),
    endDate: z.date().optional(),
    technologies: z.array(z.string()),
    demoUrl: z.string().url().optional(),
    repoUrl: z.string().url().optional(),
  }),
});

export const collections = { blog, projects };
```

#### Use Content in Pages

```astro
---
// src/pages/blog/index.astro
import { getCollection } from 'astro:content';
import BlogLayout from '@/layouts/BlogLayout.astro';
import BlogPost from '@/components/BlogPost.astro';

const posts = await getCollection('blog', ({ data }) => !data.draft);
const sortedPosts = posts.sort((a, b) =>
  b.data.pubDate.valueOf() - a.data.pubDate.valueOf()
);
---

<BlogLayout title="Blog">
  {sortedPosts.map((post) => (
    <BlogPost post={post} />
  ))}
</BlogLayout>
```

### 6. Styling & Integrations

#### Tailwind CSS Integration (Primary Styling Approach)

This skill emphasizes Tailwind CSS as the primary styling solution for all Astro projects.

```javascript
// astro.config.mjs
import tailwind from "@astrojs/tailwind";

export default defineConfig({
  integrations: [tailwind()],
});
```

Configure Tailwind for optimal performance:

```javascript
// tailwind.config.js
export default {
  content: ["./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}"],
  darkMode: "class", // Enables dark mode with .dark class
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      colors: {
        // Define brand colors
        primary: {
          50: "#eff6ff",
          500: "#3b82f6",
          600: "#2563eb",
          900: "#1e3a8a",
        },
      },
    },
  },
  plugins: [],
};
```

Global styles setup:

```css
/* src/styles/global.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  /* Custom base styles */
}

@layer components {
  /* Custom component classes */
}
```

#### Tailwind CSS Best Practices

1. **Use Custom Brand Colors**: Always use the predefined brand colors from `global.css`

   ```astro
   <!-- ✅ Use brand colors -->
   <div class="bg-mitra-blue text-warm-cream">
   <div class="border-lush-green bg-warm-orange/10">

   <!-- ❌ Avoid generic colors -->
   <div class="bg-blue-500 text-yellow-100">
   <div class="border-green-500 bg-orange-100">
   ```

   Available brand colors:
   - Primary: `mitra-blue`, `mitra-yellow`, `lush-green`, `warm-orange`
   - Text: `charcoal-grey`, `warm-cream`
   - Gradients: `bg-magic-gradient` (custom utility), `bg-linear-to-br` with brand colors

2. **Variant-based styling**: Use JavaScript objects with brand colors

   ```javascript
   const buttonVariants = {
     primary: "bg-mitra-blue hover:bg-mitra-blue-dark text-white",
     secondary: "bg-warm-cream hover:bg-grey-100 text-charcoal-grey",
     accent: "bg-warm-orange hover:bg-warm-orange-dark text-white",
   };
   ```

3. **Responsive design**: Use Tailwind's responsive prefixes

   ```astro
   <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
   ```

4. **Dark mode**: Implement with `dark:` prefix

   ```astro
   <div class="bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100">
   ```

5. **Composition**: Combine utility classes with brand colors

   ```astro
   <!-- ✅ Using brand colors -->
   <div class="flex flex-col items-center justify-center p-8 bg-linear-to-br from-mitra-blue/10 to-lush-green/10 rounded-2xl shadow-xl">
   <div class="p-6 border border-warm-orange/20 bg-magic-gradient">
   ```

6. **Custom properties**: Use CSS variables for dynamic values
   ```astro
   <div style="--delay: 100ms" class="animate-pulse [--delay:200ms]">
   ```

### 6. Tailwind CSS v4 Canonical Class Names

**IMPORTANT**: Tailwind CSS v4 uses different canonical class names. Always use these updated forms:

- `bg-gradient-to-*` → `bg-linear-to-*` (e.g., `bg-gradient-to-r` → `bg-linear-to-r`)
- `flex-shrink-0` → `shrink-0`
- `aspect-[3/2]` → `aspect-3/2` (remove brackets for simple ratios)
- `grayscale-[30%]` → `grayscale-30` (remove brackets for percentage values)

**Examples**:

```astro
<!-- Correct (Tailwind v4) -->
<div class="bg-linear-to-r from-blue-500 to-purple-600 shrink-0 aspect-3/2 grayscale-30">

<!-- Incorrect (deprecated) -->
<!-- These will trigger linter warnings: -->
<!-- bg-gradient-to-r → should be bg-linear-to-r -->
<!-- flex-shrink-0 → should be shrink-0 -->
<!-- aspect-[3/2] → should be aspect-3/2 -->
<!-- grayscale-[30%] → should be grayscale-30 -->
```

#### React Integration

```javascript
// astro.config.mjs
import react from "@astrojs/react";

export default defineConfig({
  integrations: [react()],
});
```

#### MDX Integration

```javascript
// astro.config.mjs
import mdx from "@astrojs/mdx";

export default defineConfig({
  integrations: [mdx()],
});
```

### 7. Performance Optimization

#### Image Optimization

```astro
---
import { Image } from 'astro:assets';
import heroImage from '@/images/hero.jpg';
---

<!-- Optimized, responsive images -->
<Image
  src={heroImage}
  alt="Hero section background"
  widths={[400, 800, 1200]}
  formats={['avif', 'webp', 'jpg']}
  loading="eager"
/>
```

#### View Transitions

Enable smooth page transitions:

```astro
---
// src/layouts/MainLayout.astro
import { ViewTransitions } from 'astro:transitions';
---

<html>
  <head>
    <ViewTransitions />
  </head>
  <body>
    <header>
      <nav>
        <a href="/" transition:name="home">Home</a>
        <a href="/about" transition:name="about">About</a>
      </nav>
    </header>
    <main transition:name="main-content">
      <slot />
    </main>
  </body>
</html>
```

### 8. Configuration Best Practices

#### Optimize astro.config.mjs

```javascript
import { defineConfig } from "astro/config";
import react from "@astrojs/react";
import sitemap from "@astrojs/sitemap";
import tailwind from "@astrojs/tailwind";

export default defineConfig({
  // Site metadata for SEO
  site: "https://yoursite.com",
  base: "/subpath", // If deploying to subdirectory

  // Integrations
  integrations: [react(), tailwind(), sitemap()],

  // Build optimizations
  build: {
    format: "directory", // Clean URLs
    assets: "_assets", // Custom assets path
  },

  // Vite configurations
  vite: {
    optimizeDeps: {
      exclude: ["some-large-package"],
    },
  },

  // Server options for SSR
  output: "hybrid", // or 'server' or 'static'

  // Security headers
  security: {
    allowedHosts: ["yoursite.com"],
  },
});
```

#### TypeScript Configuration

```json
// tsconfig.json
{
  "extends": "astro/tsconfigs/strict",
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/layouts/*": ["./src/layouts/*"]
    },
    "types": ["@astrojs/image/client"]
  },
  "include": ["src/**/*.ts", "src/**/*.d.ts"]
}
```

### 9. Deployment Strategies

#### Static Site Generation (Default)

```bash
npm run build  # Creates static files in dist/
```

Deploy to:

- Vercel, Netlify, Cloudflare Pages
- GitHub Pages, GitLab Pages
- Any static hosting

#### Hybrid Rendering

```javascript
// astro.config.mjs
export default defineConfig({
  output: 'hybrid',
});

// Individual pages can opt-in to SSR
---
export const prerender = false;
---
```

#### Server-Side Rendering

```javascript
// astro.config.mjs
export default defineConfig({
  output: "server",
  adapter: node({
    mode: "standalone",
  }),
});
```

Deploy to:

- Node.js servers
- Docker containers
- Serverless platforms (Vercel, Netlify Functions)

### 10. Testing Strategies

See [Testing Guide](references/testing-guide.md) for comprehensive testing documentation.

#### Vitest for Unit Testing

```bash
npm install -D vitest @vitest/ui jsdom
```

```typescript
// vitest.config.ts
import { getViteConfig } from 'astro/config';

export default getViteConfig({
  test: {
    environment: 'jsdom',
    include: ['src/**/*.{test,spec}.{js,ts,jsx,tsx}'],
  },
});
```

#### Playwright for E2E Testing

```bash
npm init playwright@latest
```

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  webServer: {
    command: 'npm run preview',
    url: 'http://localhost:4321/',
  },
});
```

#### Container API for Astro Components

```javascript
import { experimental_AstroContainer as AstroContainer } from 'astro/container';
import { expect, test } from 'vitest';
import Card from '../src/components/Card.astro';

test('Card renders with props', async () => {
  const container = await AstroContainer.create();
  const result = await container.renderToString(Card, {
    props: { title: 'Test' },
  });
  expect(result).toContain('Test');
});
```

### 11. TypeScript Best Practices

See [Common Pitfalls Guide](references/common-pitfalls.md) for TypeScript-specific issues.

#### Strict Mode Configuration

```json
// tsconfig.json
{
  "extends": "astro/tsconfigs/strict",
  "compilerOptions": {
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/layouts/*": ["./src/layouts/*"]
    }
  }
}
```

#### Type-Safe Props

```astro
---
export interface Props {
  title: string;
  count: number;
  isActive?: boolean;
  tags: string[];
}

const { title, count, isActive = false, tags } = Astro.props;
---
```

### 12. State Management for React Islands

See [State Management Guide](references/state-management.md) for comprehensive patterns.

#### Zustand (Recommended)

```typescript
// src/store/useStore.ts
import { create } from 'zustand';

export const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}));
```

#### Usage Across Islands

```jsx
// Component 1
import { useStore } from '@/store/useStore';

function Counter() {
  const { increment } = useStore();
  return <button onClick={increment}>+</button>;
}

// Component 2
import { useStore } from '@/store/useStore';

function Display() {
  const count = useStore((state) => state.count);
  return <div>{count}</div>;
}
```

## Common Patterns & Solutions

### Environment Variables

```typescript
// Create .env file
PUBLIC_API_URL=https://api.example.com
SECRET_KEY=your-secret-key

// Use in components
const apiUrl = import.meta.env.PUBLIC_API_URL;
```

### SEO Best Practices

```astro
---
// src/layouts/BaseLayout.astro
interface Props {
  title: string;
  description: string;
  image?: string;
  url?: string;
}

const { title, description, image, url } = Astro.props;
const siteUrl = Astro.site;
const canonicalUrl = url ? new URL(url, siteUrl) : siteUrl;
---

<html>
  <head>
    <title>{title}</title>
    <meta name="description" content={description} />
    <link rel="canonical" href={canonicalUrl} />

    {image && (
      <meta property="og:image" content={new URL(image, siteUrl)} />
    )}

    <meta property="og:title" content={title} />
    <meta property="og:description" content={description} />
    <meta property="og:url" content={canonicalUrl} />
    <meta name="twitter:card" content="summary_large_image" />
  </head>
</html>
```

### Error Handling

```astro
---
// src/pages/404.astro
import Layout from '@/layouts/Layout.astro';
---

<Layout title="Not Found">
  <h1>404 - Page not found</h1>
  <p>Sorry, we couldn't find that page.</p>
</Layout>
```

```javascript
// src/pages/error/[...code].astro
export function getStaticPaths() {
  return [{ params: { code: "403" } }, { params: { code: "500" } }];
}

const { code } = Astro.params;
const errorMessages = {
  403: "Forbidden",
  500: "Internal Server Error",
};
```

## Common Issues & Solutions

### Component Not Interactive

**Problem**: React/Vue components render but don't respond to user interaction.

**Solution**: Add `client:*` directive. By default, Astro strips all client-side JavaScript.

```astro
---
import ReactComponent from '@/components/ReactComponent.jsx';
---

<!-- ❌ Wrong: No client directive -->
<ReactComponent />

<!-- ✅ Correct: Add appropriate client directive -->
<ReactComponent client:load />
```

### Context API Not Working Across Islands

**Problem**: React Context providers don't share state between different component islands.

**Solution**: Each Astro island hydrates in isolation. Use external state management (Zustand, Redux, MobX) for cross-island state sharing.

See [State Management Guide](references/state-management.md) for detailed patterns.

### `document` or `window` is Not Defined

**Problem**: Error accessing browser APIs during server-side rendering.

**Solution**: Move browser-only code to `<script>` tags or use lifecycle methods in framework components.

```astro
---
// ❌ Wrong: Browser API in frontmatter
const width = window.innerWidth;
---

<!-- ✅ Correct: Move to script tag -->
<script>
  const width = window.innerWidth;
</script>
```

### TypeScript Ref Callback Errors

When using React refs with arrays in TypeScript, avoid this common error:

```tsx
// ❌ Incorrect - TypeScript error
<div ref={(el) => (cardsRef.current[index] = el)}>

// ✅ Correct - Wrap the assignment
<div ref={(el) => {
  cardsRef.current[index] = el;
}}>
```

### Tailwind CSS v4 Migration

Common issues when migrating from Tailwind CSS v3 to v4:

1. **Gradient classes**: Always use `bg-linear-to-*` instead of `bg-gradient-to-*`
2. **Aspect ratios**: Use `aspect-3/2` instead of `aspect-[3/2]` for simple ratios
3. **Flexbox**: Use `shrink-0` instead of `flex-shrink-0`
4. **Filters**: Use `grayscale-30` instead of `grayscale-[30%]` for percentage values

### File Path Resolution

If you encounter errors about missing files that should exist:

1. Check if the file exists at the expected path
2. The error might be from an outdated diagnostic cache
3. Files may have been renamed or moved

## Resources

### scripts/

The scripts/ directory contains automation utilities:

- `create-component.js` - Generates component boilerplate
- `optimize-images.js` - Batch image optimization
- `generate-sitemap.js` - Custom sitemap generation

Execute scripts without loading into context:

```bash
node scripts/create-component.js --name MyComponent --type astro
```

### references/

Reference materials for detailed information:

- `component-patterns.md` - Common Astro component patterns
- `integration-guide.md` - Detailed integration setup guides (React, Vue, Tailwind, MDX, etc.)
- `testing-guide.md` - **NEW**: Comprehensive testing strategies with Vitest, Playwright, and Container API
- `common-pitfalls.md` - **NEW**: Common mistakes and solutions for islands architecture, client directives, SSR vs static rendering
- `performance-optimization.md` - **NEW**: Build optimization, image optimization, code splitting, deployment strategies
- `state-management.md` - **NEW**: State management patterns for React islands (Zustand, Redux Toolkit, Jotai, TanStack Query)

Load reference materials when specific detailed information is needed:

```
Read references/testing-guide.md when setting up testing infrastructure
Read references/common-pitfalls.md when troubleshooting hydration or directive issues
Read references/performance-optimization.md when optimizing build size or load times
Read references/state-management.md when implementing cross-island state sharing
```

### assets/

Templates and boilerplate code:

- `component-templates/` - Starting templates for different component types
- `layout-templates/` - Common layout patterns
- `page-templates/` - Page boilerplate for different use cases

Use assets as starting points:

- Copy component templates for new components
- Reference layout templates for consistent structure
- Adapt page templates for common page types

---

This skill provides comprehensive Astro development guidance from project setup through deployment optimization.
