---
name: astro-patterns
description: Follow Astro 5 patterns for pages, components, API routes, layouts, and client-side scripts in this hybrid SSR project. Use when the user mentions "add a page", "create a component", "add an API route", "modify the layout", "SSR", "prerender", "static", "dynamic page", "script tag", or "client side".
---

# Astro Patterns

Website Foundation uses Astro 5 with hybrid rendering (`output: "server"` in `astro.config.mjs`). Pages are SSR by default — add `export const prerender = true` for static pages.

## Rendering Modes

- **Static (prerendered)**: Add `export const prerender = true` in the frontmatter. Built at deploy time. Use for content pages (blog, gallery, homepage).
- **SSR (server-rendered)**: Default mode. Rendered on every request. Use for pages that need runtime data (protected pages, dynamic responses).

## File-Based Routing

Pages live in `src/pages/`. The file path maps to the URL:
- `src/pages/index.astro` → `/`
- `src/pages/blog/index.astro` → `/blog`
- `src/pages/blog/[slug].astro` → `/blog/:slug` (dynamic route)
- `src/pages/api/contact.ts` → `/api/contact` (API endpoint)

## Dynamic Routes

Use `[slug].astro` with `getStaticPaths()` for prerendered dynamic routes:

```ts
export const prerender = true;

export async function getStaticPaths() {
  const items = await getCollection("blog");
  return items.map((item) => ({
    params: { slug: item.id },
    props: { item },
  }));
}
```

## Component Pattern

Components use PascalCase filenames in `src/components/` with typed Props:

```astro
---
interface Props {
  variant?: "primary" | "secondary";
  size?: "sm" | "md" | "lg";
}
const { variant = "primary", size = "md" } = Astro.props;
---
<div class="...">
  <slot />
</div>
```

## Layout Pattern

`Base.astro` provides the HTML shell with `<slot />` for page content:

```astro
<Base title="Page Title" description="Page description">
  <section class="mx-auto max-w-6xl px-4 pt-16 pb-20">
    <!-- page content -->
  </section>
</Base>
```

## Client Scripts

- **Bundled** (default): `<script>` tags are processed by Astro's bundler
- **Inline**: `<script is:inline>` prevents bundling — use for DOM manipulation that must run immediately (e.g., theme toggle in `<head>`)

See [pages and routing](references/pages-and-routing.md), [components](references/components.md), and [API routes](references/api-routes.md) for details.
