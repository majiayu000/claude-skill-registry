---
name: content-collections
description: Work with the four content collections (blog, gallery, testimonials, promoted) — understand schemas, create valid frontmatter, query and render content. Use when the user mentions "content", "collections", "blog post", "gallery item", "testimonial", "promoted", "frontmatter", "markdown", "schema", or "Zod".
---

# Content Collections

Website Foundation uses Astro's Content Layer API with four collections defined in `src/content.config.ts`. Each collection uses the `glob` loader to read markdown files from `src/content/<collection>/`.

## Collections Overview

| Collection | Directory | Required Fields |
|------------|-----------|-----------------|
| **blog** | `src/content/blog/` | title, description, author, publishedAt |
| **gallery** | `src/content/gallery/` | title, description, image, category, publishedAt |
| **testimonials** | `src/content/testimonials/` | author, role, publishedAt |
| **promoted** | `src/content/promoted/` | title, description, image, link, linkText, order, publishedAt |

## File Naming

Use kebab-case `.md` files: `my-first-post.md`, `sunset-beach.md`. The filename (without extension) becomes the content ID used for slugs and routing.

## Frontmatter Format

Every markdown file starts with YAML frontmatter between `---` fences:

```markdown
---
title: "My Blog Post"
description: "A short summary"
author: "Jane Doe"
publishedAt: 2026-02-21
tags: ["astro", "tutorial"]
draft: false
---

Body content goes here in markdown.
```

Dates use `z.coerce.date()` — accepts `YYYY-MM-DD` strings or ISO 8601 format.

## Querying Content

Use `getCollection()` from `astro:content` to fetch all items, then filter and sort in JavaScript:

```ts
import { getCollection } from "astro:content";

const posts = (await getCollection("blog"))
  .filter((p) => !p.data.draft)
  .sort((a, b) => b.data.publishedAt.getTime() - a.data.publishedAt.getTime());
```

See [content queries reference](references/content-queries.md) for all query patterns and [schemas reference](references/schemas.md) for detailed field documentation.

## Rendering Content

Use `render()` to get a `<Content />` component for the markdown body:

```ts
import { render } from "astro:content";
const { Content } = await render(post);
```

Then use `<Content />` in your template inside a prose container.
