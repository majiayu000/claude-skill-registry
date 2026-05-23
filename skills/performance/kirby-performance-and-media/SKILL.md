---
name: kirby-performance-and-media
description: Improves Kirby performance and media delivery (cache tuning, CDN, responsive images, lazy loading). Use when optimizing page speed, caching, or image handling.
---

# Kirby Performance and Media

## Quick start

- Follow the workflow below, and run a full audit checklist when performance work spans multiple templates or plugins.

## KB entry points

- `kirby://kb/scenarios/55-cdn-asset-and-media-urls`
- `kirby://kb/scenarios/56-lazy-loading-images`
- `kirby://kb/scenarios/57-responsive-images-srcset`
- `kirby://kb/scenarios/58-fine-tune-page-cache`
- `kirby://kb/scenarios/79-conditional-loading-frontend-libraries`

## Required inputs

- Target pages/templates and performance symptoms.
- Image/media volume and CDN constraints.
- Acceptable cache settings or invalidation rules.

## Audit checklist

- Identify templates that render large image sets or long listings.
- Check `kirby://config/cache` and `kirby://config/thumbs` for overrides.
- Verify media URLs, cache headers, and variant generation.

## Measurement step

- Inspect `Cache-Control` headers and confirm generated `/media` variants exist.

## CDN fallback rule

- If the CDN is unavailable, fall back to local asset/media URLs without breaking pages.

## Common pitfalls

- Generating thumbnails in loops without `srcset()` or caching.
- Routing media through a CDN without preserving variants.

## Workflow

1. Call `kirby:kirby_init` and read `kirby://config/cache` and `kirby://config/thumbs`.
2. Inspect templates/snippets that render large collections of images:
   - `kirby:kirby_templates_index`
   - `kirby:kirby_snippets_index`
3. Search the KB with `kirby:kirby_search` (examples: "cdn asset and media urls", "lazy loading images", "responsive images srcset", "fine tune page cache").
4. Apply minimal changes first:
   - use `srcset()`/`sizes` for responsive images
   - add `loading="lazy"` and `decoding="async"`
   - adjust cache ignore rules via blueprint options or fields
   - route assets/media through a CDN when required
5. Verify output and caching behavior:
   - `kirby:kirby_render_page(noCache=true)` for HTML
   - inspect generated media variants and cache headers in a browser
