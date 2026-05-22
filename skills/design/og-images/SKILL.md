---
name: og-images
description: Guides creation of OpenGraph and Twitter share images using next/og ImageResponse. Covers layout patterns, custom fonts, avatars, title case, and Satori rules. Use when building OG images, Twitter cards, or social previews.
---

# Creating Share Images for Next.js

Generate dynamic OpenGraph (1200x630) and Twitter (1200x600) images using `next/og` ImageResponse.

## Choosing an Approach

- **File-based route** (`app/opengraph-image.tsx`): Best for static pages with known titles at build time. Export `runtime`, `alt`, `size`, `contentType`, and a default `Image` function.
- **API route** (`app/api/og/route.tsx`): Best for dynamic content (blog posts, CMS). Accept `slug` and/or `title` as query params. Reference in metadata via `generateMetadata()`.

Use `export const runtime = "edge"` for both approaches.

## File Naming Convention

| File | Purpose | Dimensions |
|------|---------|------------|
| `opengraph-image.tsx` | Facebook, LinkedIn, iMessage | 1200x630 |
| `twitter-image.tsx` | Twitter/X cards | 1200x600 |
| `app/api/og/route.tsx` | Dynamic API route | 1200x630 |

Place file-based routes in the relevant route directory (e.g., `app/about/opengraph-image.tsx` for `/about`).

## Layout Pattern

- Use `flexDirection: "column"` with `justifyContent: "space-between"` to separate content from branding
- Title and subtitle (e.g., author name) go top-left in a stacked flex column
- Title: large, bold/medium weight, dark color
- Subtitle: same size or smaller, lighter weight, muted color (e.g., `#888`)
- Keep text left-aligned with `textWrap: "balance"` and constrain width with `maxWidth`
- Use `letterSpacing: "-0.02em"` for tight, editorial feel at large sizes
- Padding: `48px` on all sides works well at 1200x630

## Avatar / Logo (Optional)

If the project has an avatar or logo, place it in the bottom-right corner using a flex container with `justifyContent: "flex-end"`. Load images via `fetch` + `arrayBuffer`, convert to base64 data URI for the `src`. Use `borderRadius: "50%"` for circular avatars. Cache loaded assets in a `Map` to avoid refetching.

## Custom Fonts

Load `.ttf` files from `public/fonts/` using `new URL("../../../public/fonts/YourFont.ttf", import.meta.url)`. Pass the `ArrayBuffer` to `ImageResponse` via the `fonts` option. Cache the font buffer after first load. Match the `weight` in the fonts config to the actual font file weight.

## Title Case

If titles come from a CMS, apply smart title case:
- Lowercase small words (a, an, the, and, but, for, in, of, etc.) unless first or last
- Always capitalize brand names correctly (WordPress, JavaScript, GitHub, macOS, etc.)
- Uppercase known acronyms (AI, API, CSS, HTML, UI, UX)
- Handle hyphenated words by capitalizing each part independently

## Metadata Integration

Reference the OG route in `generateMetadata()`:

```tsx
export function generateMetadata({ params }) {
  return {
    openGraph: {
      images: [`/api/og?slug=${params.slug}`],
    },
  };
}
```

For static pages, pass the title directly: `/api/og?title=About`.

## Satori Rules

These are hard requirements of the `next/og` rendering engine (Satori):

1. **Every element needs `display: "flex"`** — this is the only layout mode
2. **Inline styles only** — no CSS classes, no external stylesheets, no CSS variables
3. **All text must be in elements** with explicit style props
4. **Use hex colors** — no `rgb()`, `hsl()`, or CSS variables
5. **No `gap` on older versions** — test before relying on it; fallback to margin

## Common Issues

| Issue | Solution |
|-------|----------|
| Text not rendering | Add `display: "flex"` to the text wrapper |
| Layout broken | Ensure all containers have `display: "flex"` |
| Colors wrong | Use hex colors, not CSS variables |
| Font not loading | Check the relative path from route file to `public/fonts/` |
| Image not showing | Convert to base64 data URI, don't use relative paths |

## Testing

Preview during development by visiting the route directly in the browser:

```
http://localhost:3000/api/og?title=Hello+World
```

After building, verify routes register as dynamic (`f` prefix) in the build output.
