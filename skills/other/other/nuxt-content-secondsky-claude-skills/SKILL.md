---
name: nuxt-content
description: Nuxt Content v3 Git-based CMS for Markdown/MDC content sites. Use for blogs, docs, content-driven apps with type-safe queries, schema validation (Zod/Valibot), full-text search, navigation utilities. Supports Nuxt Studio production editing, Cloudflare D1/Pages deployment, Vercel deployment, SQL storage, MDC components, content collections.

  Keywords: nuxt content, @nuxt/content, content collections, git-based cms, markdown cms, mdc syntax, nuxt studio, content editing, queryCollection, cloudflare d1 deployment, vercel deployment, markdown components, prose components, content navigation, full-text search, type-safe queries, sql storage, content schema validation, zod validation, valibot, remote repositories, content queries, queryCollectionNavigation, queryCollectionSearchSections, ContentRenderer component
license: MIT
---

# Nuxt Content v3

**Status**: Production Ready
**Last Updated**: 2025-01-10
**Dependencies**: None
**Latest Versions**: @nuxt/content@^3.0.0, nuxt-studio@^0.1.0-alpha, zod@^4.1.12, valibot@^0.42.0, better-sqlite3@^11.0.0

---

## Overview

Nuxt Content v3 is a powerful Git-based CMS for Nuxt projects that manages content through Markdown, YAML, JSON, and CSV files. It transforms content files into structured data with type-safe queries, automatic validation, and SQL-based storage for optimal performance.

### What's New in v3

**Major Improvements**:
- **Content Collections**: Structured data organization with type-safe queries, automatic validation, and advanced query builder
- **SQL-Based Storage**: Production uses SQL (vs. large bundle sizes in v2) for optimized queries and universal compatibility (server/serverless/edge/static)
- **Full TypeScript Integration**: Automatic types for all collections and APIs
- **Enhanced Performance**: Ultra-fast data retrieval with adapter-based SQL system
- **Nuxt Studio Integration**: Self-hosted content editing in production with GitHub sync

### When to Use This Skill

Use this skill when:
- Building blogs, documentation sites, or content-heavy applications
- Managing content with Markdown, YAML, JSON, or CSV files
- Implementing Git-based content workflows
- Creating type-safe content queries
- Deploying to Cloudflare (Pages/Workers) or Vercel
- Setting up production content editing with Nuxt Studio
- Building searchable content with full-text search
- Creating navigation systems from content structure

---

## Quick Start (10 Minutes)

### 1. Install Nuxt Content

```bash
# Bun (recommended)
bun add @nuxt/content better-sqlite3

# npm
npm install @nuxt/content better-sqlite3

# pnpm
pnpm add @nuxt/content better-sqlite3
```

**Why this matters:**
- `@nuxt/content` is the core CMS module
- `better-sqlite3` provides SQL storage for optimal performance
- Zero configuration required for basic usage

### 2. Register Module

```ts
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@nuxt/content']
})
```

**CRITICAL:**
- Module must be added to `modules` array (not `buildModules`)
- No additional configuration needed for basic setup

### 3. Create First Collection

```ts
// content.config.ts
import { defineContentConfig, defineCollection } from '@nuxt/content'
import { z } from 'zod'

export default defineContentConfig({
  collections: {
    content: defineCollection({
      type: 'page',
      source: '**/*.md',
      schema: z.object({
        tags: z.array(z.string()).optional(),
        date: z.date().optional()
      })
    })
  }
})
```

Create content file:
```md
<!-- content/index.md -->
---
title: Hello World
description: My first Nuxt Content page
tags: ['nuxt', 'content']
---

# Welcome to Nuxt Content v3

This is my first content-driven site!
```

### 4. Query and Render Content

```vue
<!-- pages/[...slug].vue -->
<script setup>
const route = useRoute()
const { data: page } = await useAsyncData(route.path, () =>
  queryCollection('content').path(route.path).first()
)
</script>

<template>
  <ContentRenderer v-if="page" :value="page" />
</template>
```

**See Full Template**: `templates/blog-collection-setup.ts`

---

## Critical Rules

### Always Do

1. **Define Collections** in `content.config.ts` before querying
2. **Use ISO 8601 Date Format**: `2024-01-15` or `2024-01-15T10:30:00Z`
3. **Restart Dev Server** after changing `content.config.ts`
4. **Use `.only()`** to select specific fields (performance)
5. **Place MDC Components** in `components/content/` directory
6. **Use Zero-Padded Prefixes** for numeric sorting: `01-`, `02-`
7. **Install Database Connector**: `better-sqlite3` required
8. **Specify Language** in code blocks for syntax highlighting
9. **Use `<!--more-->`** in content to separate excerpts
10. **D1 Binding Must Be "DB"** (case-sensitive) on Cloudflare

### Never Do

1. **Don't Query Before Defining Collection** in `content.config.ts`
2. **Don't Use Non-ISO Date Formats** (e.g., "January 15, 2024")
3. **Don't Forget to Restart** dev server after config changes
4. **Don't Query All Fields** when you only need some (use `.only()`)
5. **Don't Place Components** outside `components/content/`
6. **Don't Use Single-Digit Prefixes** (use `01-` not `1-`)
7. **Don't Skip Database Connector** installation
8. **Don't Forget Language** in code fences
9. **Don't Expect Excerpts** without `<!--more-->` divider
10. **Don't Use Different Binding Names** for D1 (must be "DB")

---

## Content Collections

### Defining Collections

Collections organize related content with shared configuration:

```ts
// content.config.ts
import { defineCollection, defineContentConfig } from '@nuxt/content'
import { z } from 'zod'

export default defineContentConfig({
  collections: {
    blog: defineCollection({
      type: 'page',
      source: 'blog/**/*.md',
      schema: z.object({
        title: z.string(),
        date: z.date(),
        tags: z.array(z.string()).default([])
      })
    }),

    authors: defineCollection({
      type: 'data',
      source: 'authors/*.yml',
      schema: z.object({
        name: z.string(),
        bio: z.string()
      })
    })
  }
})
```

---

### Collection Types

#### Page Type (`type: 'page'`)

**Use for**: Content that maps to URLs

**Features**:
- Auto-generates paths from file structure
- Built-in fields: `path`, `title`, `description`, `body`, `navigation`
- Perfect for: blogs, docs, marketing pages

**Path Mapping**:
```
content/index.md        → /
content/about.md        → /about
content/blog/hello.md   → /blog/hello
```

#### Data Type (`type: 'data'`)

**Use for**: Structured data without URLs

**Features**:
- Complete schema control
- No automatic path generation
- Perfect for: authors, products, configs

---

### Schema Validation

#### With Zod v4 (Recommended)

```bash
bun add -D zod@^4.1.12
# or: npm install -D zod@^4.1.12
```

```ts
import { z } from 'zod'

schema: z.object({
  title: z.string(),
  date: z.date(),
  published: z.boolean().default(false),
  tags: z.array(z.string()).optional(),
  category: z.enum(['news', 'tutorial', 'update'])
})
```

#### With Valibot (Alternative)

```bash
bun add -D valibot@^0.42.0
# or: npm install -D valibot@^0.42.0
```

```ts
import * as v from 'valibot'

schema: v.object({
  title: v.string(),
  date: v.date(),
  published: v.boolean(false),
  tags: v.optional(v.array(v.string()))
})
```

---

## Querying Content

### Basic Queries

```ts
// Get all posts
const posts = await queryCollection('blog').all()

// Get single post by path
const post = await queryCollection('blog').path('/blog/hello').first()

// Get post by ID
const post = await queryCollection('blog').where('_id', '=', 'hello').first()
```

---

### Field Selection

```ts
// Select specific fields (performance optimization)
const posts = await queryCollection('blog')
  .only(['title', 'description', 'date', 'path'])
  .all()

// Exclude fields
const posts = await queryCollection('blog')
  .without(['body'])
  .all()
```

---

### Where Conditions

```ts
// Single condition
const posts = await queryCollection('blog')
  .where('published', '=', true)
  .all()

// Multiple conditions
const posts = await queryCollection('blog')
  .where('published', '=', true)
  .where('category', '=', 'tutorial')
  .all()

// Operators: =, !=, <, <=, >, >=, in, not-in, like
const recent = await queryCollection('blog')
  .where('date', '>', new Date('2024-01-01'))
  .all()

const tagged = await queryCollection('blog')
  .where('tags', 'in', ['nuxt', 'vue'])
  .all()
```

---

### Ordering and Pagination

```ts
// Sort by field
const posts = await queryCollection('blog')
  .sort('date', 'DESC')
  .all()

// Pagination
const posts = await queryCollection('blog')
  .sort('date', 'DESC')
  .limit(10)
  .offset(0)
  .all()
```

---

### Counting

```ts
// Count results
const total = await queryCollection('blog')
  .where('published', '=', true)
  .count()
```

---

### Server-Side Queries

```ts
// server/api/posts.get.ts
export default defineEventHandler(async (event) => {
  const posts = await queryCollection('blog')
    .where('published', '=', true)
    .sort('date', 'DESC')
    .all()

  return { posts }
})
```

---

## Navigation

Auto-generate navigation tree from content structure:

```ts
const navigation = await queryCollectionNavigation('blog').all()
```

**Returns hierarchical structure**:
```ts
[
  {
    title: 'Getting Started',
    path: '/docs/getting-started',
    children: [{ title: 'Installation', path: '/docs/getting-started/installation' }]
  }
]
```

**Advanced patterns** (filters, ordering, custom structures): See `references/collection-examples.md`

---

## MDC Syntax (Markdown Components)

### Basic Component Syntax

```md
<!-- Default slot -->
::my-alert
This is an alert message
::

<!-- Named slots -->
::my-card
#title
Card Title
#default
Card content here
::
```

**Component**:
```vue
<!-- components/content/MyAlert.vue -->
<template>
  <div class="alert">
    <slot />
  </div>
</template>
```

---

### Props

```md
::my-button{href="/docs" type="primary"}
Click me
::
```

**Component**:
```vue
<!-- components/content/MyButton.vue -->
<script setup>
defineProps<{
  href: string
  type: 'primary' | 'secondary'
}>()
</script>
```

---

## Full-Text Search

```ts
// Search across all content
const results = await queryCollectionSearchSections('blog', 'nuxt content')
  .where('published', '=', true)
  .all()
```

**Returns**:
```ts
[
  {
    id: 'hello',
    path: '/blog/hello',
    title: 'Hello World',
    content: '...matching text...'
  }
]
```

---

## Deployment

### Cloudflare Pages + D1

```bash
bun add -D @nuxthub/core
bunx wrangler d1 create nuxt-content
bun run build && bunx wrangler pages deploy dist
```

**wrangler.toml**:
```toml
[[d1_databases]]
binding = "DB"  # Must be exactly "DB" (case-sensitive)
database_name = "nuxt-content"
database_id = "your-database-id"
```

**CRITICAL**: D1 binding MUST be named `DB` (case-sensitive).

**See**: `references/deployment-checklists.md` for complete Cloudflare deployment guide with troubleshooting.

---

### Vercel

```ts
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@nuxt/content'],
  routeRules: {
    '/blog/**': { prerender: true }
  }
})
```

```bash
vercel deploy
```

**See**: `references/deployment-checklists.md` for complete Vercel configuration and prerender strategy.

---

## Nuxt Studio Integration

### Enable Studio

```bash
bun add -D nuxt-studio@alpha
# or: npm install -D nuxt-studio@alpha
```

```ts
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@nuxt/content', 'nuxt-studio'],
  
  studio: {
    enabled: true,
    gitInfo: {
      name: 'your-name',
      email: 'your-email@example.com'
    }
  }
})
```

### OAuth Setup

1. Create GitHub OAuth App
2. Set Authorization callback URL: `https://yourdomain.com/api/__studio/oauth/callback`
3. Add client ID and secret to environment variables

**CRITICAL**: Callback URL must match production domain exactly (including `https://`).

---

## Top 5 Critical Issues

### Issue #1: Collection Not Found

**Error**: `Collection 'xyz' not found`

**Solution**: Define collection in `content.config.ts` and restart dev server
```bash
rm -rf .nuxt && bun dev
```

---

### Issue #2: Date Validation Failure

**Error**: `Validation error: Expected date, received string`

**Solution**: Use ISO 8601 format:
```md
---
date: 2024-01-15  # ✅ Correct
# NOT: "January 15, 2024"  # ❌ Wrong
---
```

---

### Issue #3: D1 Binding Not Found (Cloudflare)

**Error**: `DB is not defined`

**Solution**: D1 binding name must be exactly `DB` (case-sensitive) in Cloudflare dashboard.

---

### Issue #4: MDC Components Not Rendering

**Error**: Components show as raw text

**Solution**: Place components in `components/content/` with exact name matching:
```vue
<!-- components/content/MyAlert.vue -->
```

```md
::my-alert
Content
::
```

---

### Issue #5: Navigation Not Updating

**Error**: New content doesn't appear in navigation

**Solution**: Clear `.nuxt` cache:
```bash
rm -rf .nuxt && bun dev
```

---

**See All 18 Issues**: `references/error-catalog.md`

---

## When to Load References

**Load `references/error-catalog.md` when:**
- User encounters error beyond Top 5 shown above
- Debugging collection validation, schema errors, or deployment issues
- Need complete error catalog with all 18 documented solutions and sources

**Load `references/collection-examples.md` when:**
- Setting up advanced collection types (data vs page)
- Implementing complex schema validation patterns
- Need examples for Zod v4 or Valibot schemas
- Working with multiple collection configurations

**Load `references/query-operators.md` when:**
- Building complex queries beyond basic examples
- Need full reference of all operators (=, !=, <, >, <=, >=, in, not-in, like)
- Implementing pagination, sorting, or field selection
- Troubleshooting query syntax errors

**Load `references/deployment-checklists.md` when:**
- Deploying to specific platform (Cloudflare Pages, Cloudflare Workers D1, Vercel)
- Setting up production environment configurations
- Troubleshooting deployment-specific errors (D1 binding, prerender routes)
- Need platform-specific wrangler.toml or vercel.json examples

**Load `references/mdc-syntax-reference.md` when:**
- Implementing custom MDC (Markdown Components)
- Debugging component rendering issues
- Need complete syntax reference for props, slots, nesting
- Creating advanced content components

**Load `references/studio-setup-guide.md` when:**
- Setting up Nuxt Studio for production content editing
- Configuring GitHub OAuth authentication
- Enabling self-hosted content editing with GitHub sync
- Troubleshooting Studio authentication or Git sync issues

**Templates** (`templates/`):
- `blog-collection-setup.ts` - Complete blog setup with collections, queries, navigation, search, and deployment (334 lines)

---

## Performance Tips

1. **Use `.only()`** to select specific fields
2. **Enable Caching** for production
3. **Use Pagination** for large collections
4. **Prerender Static Routes** on Vercel
5. **Use SQL Storage** (better-sqlite3) for optimal performance

---

## Best Practices

1. Always define collections before querying
2. Use TypeScript for type-safe queries
3. Validate schemas with Zod or Valibot
4. Place MDC components in `components/content/`
5. Use ISO 8601 date format
6. Add `<!--more-->` for excerpts
7. Specify language in code blocks
8. Clear `.nuxt` after config changes
9. For Cloudflare: D1 binding must be "DB"
10. Use pagination for large datasets

---

## Integration with Other Skills

This skill composes well with:

- **nuxt-v4** → Core Nuxt framework
- **nuxt-ui-v4** → UI component library
- **cloudflare-worker-base** → Cloudflare deployment
- **tailwind-v4-shadcn** → Styling
- **drizzle-orm-d1** → Additional database queries
- **cloudflare-d1** → Database integration

---

## Additional Resources

**Official Documentation**:
- Nuxt Content Docs: https://content.nuxt.com
- GitHub: https://github.com/nuxt/content
- Nuxt Studio: https://nuxt.studio

**Examples**:
- Official Examples: https://github.com/nuxt/content/tree/main/examples
- Starter Templates: https://github.com/nuxt-themes

---

**Production Tested**: Documentation sites, blogs, content platforms
**Last Updated**: 2025-01-27
**Token Savings**: ~60% (reduces content + error documentation)
