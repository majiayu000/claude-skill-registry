---
name: astro-images
description: Use astro:assets for all images. This enables automatic optimization
  (resizing, WebP/AVIF conversion, lazy loading).
---

# Astro Image Optimization

Use `astro:assets` for all images. This enables automatic optimization (resizing, WebP/AVIF conversion, lazy loading).

## When to Use This Skill

Use this skill when:
- Adding images to `.astro` or `.mdx` files
- Moving images from `/public` to optimized assets
- Debugging 404s or unoptimized images in production

## Rules

- **Never use raw `<img>` tags** in `.astro` or `.mdx` files
- **Never reference images from `/public`** — bypasses optimization
- **Always import images** from `src/assets/`

## Correct Pattern

```astro
---
import { Image } from "astro:assets";
import photo from "../assets/photo.png";
---

<Image src={photo} alt="Description" width={800} />
```

## In MDX

```mdx
---
import { Image } from "astro:assets";
import diagram from "../../assets/diagram.png";
---

<Image src={diagram} alt="Diagram" width={600} />
```

## Linting

Run `npm run lint:assets` to catch violations. The linter flags:

- Raw `<img>` tags in `.astro` and `.mdx` files (error)
- Markdown images from `/public` like `![](/image.png)` (warning)
- Direct `/src/` paths in link/script tags (error)
