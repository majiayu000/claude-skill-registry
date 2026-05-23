---
name: edge-stack
description: |
  Modern edge-native web stack: Hono + htmx + UnoCSS + Cloudflare D1. Use when: building
  server-rendered apps with interactivity, rapid prototyping, CRUD apps, landing pages,
  marketplaces. Zero cold start, global edge deployment, $0/month on CF free tier.
  TypeScript alternative to Rust/Axum + htmx stack.
---

# Edge Stack

Ultra-fast edge-native web development: **Hono + htmx + UnoCSS + D1**

## Stack Overview

| Layer | Tool | Why |
|-------|------|-----|
| Framework | Hono | Ultra-fast, TypeScript, JSX support |
| Interactivity | htmx | Server-rendered, 14kb, no build step |
| Styling | UnoCSS | Tailwind-compatible, instant builds |
| Database | Cloudflare D1 | SQLite on edge, free tier |
| Deploy | CF Workers/Pages | Global edge, zero cold start |

## Quick Start

```bash
# Create project
pnpm create hono@latest my-app
# Select: cloudflare-workers

cd my-app
pnpm add htmx.org
```

### wrangler.toml

```toml
name = "my-app"
compatibility_date = "2024-01-01"
main = "src/index.ts"

[[d1_databases]]
binding = "DB"
database_name = "my-db"
database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

### Basic App

```typescript
import { Hono } from 'hono'
import { html } from 'hono/html'

type Bindings = { DB: D1Database }

const app = new Hono<{ Bindings: Bindings }>()

// Layout with htmx
const Layout = ({ children }: { children: any }) => html`
<!DOCTYPE html>
<html>
<head>
  <script src="https://unpkg.com/htmx.org@2.0.4"></script>
  <script src="https://cdn.jsdelivr.net/npm/@unocss/runtime"></script>
</head>
<body class="bg-gray-100 p-4">
  ${children}
</body>
</html>
`

// Page with htmx interactivity
app.get('/', (c) => {
  return c.html(
    <Layout>
      <h1 class="text-2xl font-bold mb-4">My App</h1>
      <button
        hx-get="/api/items"
        hx-target="#items"
        class="px-4 py-2 bg-blue-500 text-white rounded"
      >
        Load Items
      </button>
      <div id="items"></div>
    </Layout>
  )
})

// API returns HTML fragment
app.get('/api/items', async (c) => {
  const { results } = await c.env.DB
    .prepare('SELECT * FROM items')
    .all()

  return c.html(
    <ul class="mt-4 space-y-2">
      {results.map((item: any) => (
        <li class="p-2 bg-white rounded">{item.name}</li>
      ))}
    </ul>
  )
})

export default app
```

## Commands

```bash
# Development
pnpm dev

# Create D1 database
wrangler d1 create my-db

# Run migration
wrangler d1 execute my-db --file=./schema.sql

# Deploy
wrangler deploy
```

## When to Use

**Good for:**
- Landing pages, marketing sites
- CRUD apps, admin panels
- Marketplaces, directories
- Forms, surveys
- Rapid prototyping

**Not ideal for:**
- Heavy client-side interactivity (use SPA)
- Real-time collaborative editing
- Complex state management

## References

- **[hono.md](references/hono.md)** — Routing, middleware, JSX, bindings
- **[htmx-patterns.md](references/htmx-patterns.md)** — htmx with Hono patterns
- **[unocss.md](references/unocss.md)** — UnoCSS setup, custom utilities
- **[d1-database.md](references/d1-database.md)** — D1 schema, queries, migrations
- **[deployment.md](references/deployment.md)** — wrangler.toml, CI/CD, domains
