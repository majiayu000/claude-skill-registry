---
name: opengraph-images
description: Create dynamic OpenGraph images for social media sharing using Next.js ImageResponse API. Use when adding OG images to new pages, updating existing OG images, or implementing page-specific social previews.
allowed-tools: Read, Edit, Write, Grep, Glob
---

# OpenGraph Images Skill

This skill helps you create consistent, branded OpenGraph images for social media sharing across the web application.

## When to Use This Skill

- Creating dynamic OG images for new pages
- Updating existing OG image content/styling
- Implementing page-specific social previews
- Adding custom fonts to OG images
- Debugging OG image rendering issues

## Key Files

| File | Purpose |
|------|---------|
| `apps/web/src/app/opengraph-image.png` | Static homepage OG image |
| `apps/web/src/app/about/opengraph-image.tsx` | Dynamic About page OG image |
| `apps/web/src/app/blog/[slug]/opengraph-image.tsx` | Dynamic blog post OG images |
| `apps/web/assets/fonts/` | Geist font files for OG images |

## Standard Configuration

### Required Exports

```typescript
import { ImageResponse } from "next/og";

// Alt text for accessibility
export const alt = "Page Title - SG Cars Trends";

// Standard OG image dimensions
export const size = {
  width: 1200,
  height: 630,
};

// Image format
export const contentType = "image/png";
```

### Font Loading

Load Geist fonts from `assets/fonts/` for consistent typography:

```typescript
import { readFile } from "node:fs/promises";
import { join } from "node:path";

export default async function Image() {
  const [geistRegular, geistSemiBold, geistBold] = await Promise.all([
    readFile(join(process.cwd(), "assets/fonts/Geist-Regular.ttf")),
    readFile(join(process.cwd(), "assets/fonts/Geist-SemiBold.ttf")),
    readFile(join(process.cwd(), "assets/fonts/Geist-Bold.ttf")),
  ]);

  return new ImageResponse(
    // JSX content
    <div>...</div>,
    {
      ...size,
      fonts: [
        { name: "Geist", data: geistRegular, style: "normal", weight: 400 },
        { name: "Geist", data: geistSemiBold, style: "normal", weight: 500 },
        { name: "Geist", data: geistBold, style: "normal", weight: 700 },
      ],
    },
  );
}
```

## Design Structure

### Standard Layout Pattern

OG images follow a consistent three-part structure:

```
┌────────────────────────────────────────────┐
│  [Eyebrow Chip]  (page context indicator)  │
│                                            │
│  Main Headline                             │
│  With Gradient Text                        │
│                                            │
│  Subheadline description text that         │
│  provides additional context               │
└────────────────────────────────────────────┘
```

### Eyebrow Chip

Small pill-shaped indicator that signals page type/context:

```typescript
<div
  style={{
    display: "flex",
    alignItems: "center",
    gap: 8,
    padding: "8px 16px",
    backgroundColor: "rgba(37, 99, 235, 0.05)",
    border: "1px solid rgba(37, 99, 235, 0.2)",
    borderRadius: 9999,
    marginBottom: 32,
  }}
>
  <div
    style={{
      width: 8,
      height: 8,
      borderRadius: "50%",
      backgroundColor: "#2563eb",
    }}
  />
  <span
    style={{
      fontSize: 16,
      fontWeight: 500,
      color: "rgba(10, 10, 10, 0.9)",
      letterSpacing: "0.025em",
    }}
  >
    Behind the Data
  </span>
</div>
```

**Eyebrow Text Guidelines:**

| Page Type | Eyebrow Text |
|-----------|--------------|
| Homepage | Singapore Car Market Data |
| About | Behind the Data |
| Blog Post | Blog / Analysis / Insights |
| COE | COE Bidding Results |
| Cars | Vehicle Registrations |

### Main Headline

Two-line headline with gradient text on the second line:

```typescript
<div
  style={{
    display: "flex",
    flexDirection: "column",
    fontSize: 64,
    fontWeight: 700,
    color: "#0a0a0a",
    lineHeight: 1.1,
    letterSpacing: "-0.025em",
    marginBottom: 24,
  }}
>
  <span>First Line of</span>
  <span
    style={{
      backgroundImage: "linear-gradient(to right, #2563eb, rgba(37, 99, 235, 0.7))",
      backgroundClip: "text",
      color: "transparent",
    }}
  >
    Gradient Headline
  </span>
</div>
```

### Subheadline

Supporting description text:

```typescript
<div
  style={{
    display: "flex",
    fontSize: 24,
    color: "rgba(10, 10, 10, 0.7)",
    lineHeight: 1.5,
    maxWidth: 700,
    fontWeight: 400,
  }}
>
  Description text that provides additional context about the page content.
</div>
```

## Colour Palette

| Element | Colour | Value |
|---------|--------|-------|
| Background | Light gray | `#f5f5f5` |
| Primary text | Near black | `#0a0a0a` |
| Secondary text | Muted | `rgba(10, 10, 10, 0.7)` |
| Primary blue | Brand | `#2563eb` |
| Gradient end | Lighter blue | `rgba(37, 99, 235, 0.7)` |
| Chip background | Tinted | `rgba(37, 99, 235, 0.05)` |
| Chip border | Subtle | `rgba(37, 99, 235, 0.2)` |

## Static vs Dynamic OG Images

### Use Static PNG When:

- Content never changes (homepage)
- No page-specific data needed
- Maximum performance required

```
src/app/opengraph-image.png  # Just place the file
```

### Use Dynamic TSX When:

- Content varies by page/route (blog posts, about)
- Need custom fonts
- Dynamic data from database

```typescript
// src/app/[route]/opengraph-image.tsx
export default async function Image({ params }) {
  // Fetch data, generate dynamic content
}
```

## Dynamic Route OG Images

For routes with dynamic segments (e.g., blog posts):

```typescript
import { getAllPosts, getPostBySlug } from "@web/queries/posts";
import { ImageResponse } from "next/og";

interface Props {
  params: Promise<{ slug: string }>;
}

export const size = { width: 1200, height: 630 };
export const dynamic = "force-static";

export async function generateStaticParams() {
  const posts = await getAllPosts();
  return posts.map((post) => ({ slug: post.slug }));
}

const Image = async ({ params }: Props) => {
  const { slug } = await params;
  const post = await getPostBySlug(slug);

  if (!post) {
    return new Response("Not found", { status: 404 });
  }

  return new ImageResponse(
    <div style={{ /* ... */ }}>
      {post.title}
    </div>,
    {
      ...size,
      headers: {
        "Cache-Control": "public, max-age=31536000, s-maxage=31536000, immutable",
      },
    },
  );
};

export default Image;
```

## Caching Headers

For static/infrequently changing OG images:

```typescript
return new ImageResponse(content, {
  ...size,
  headers: {
    "Cache-Control": "public, max-age=31536000, s-maxage=31536000, immutable",
  },
});
```

## Important Constraints

### ImageResponse JSX Limitations

The `ImageResponse` API uses Satori for rendering, which has constraints:

- **No CSS classes** - Use inline `style` objects only
- **Limited CSS properties** - Flexbox works, Grid doesn't
- **No external images** - Must be base64 or absolute URLs
- **Font files required** - Must load `.ttf` files explicitly
- **No React hooks** - Server-side only

### Common Style Gotchas

```typescript
// ❌ Won't work
<div className="flex gap-4">

// ✅ Use inline styles
<div style={{ display: "flex", gap: 16 }}>

// ❌ CSS Grid not supported
<div style={{ display: "grid" }}>

// ✅ Use Flexbox
<div style={{ display: "flex", flexWrap: "wrap" }}>
```

## Testing OG Images

1. **Local development**: Visit `http://localhost:3000/about/opengraph-image` directly
2. **Social debuggers**:
   - [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
   - [Twitter Card Validator](https://cards-dev.twitter.com/validator)
   - [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)
3. **OG Preview tools**: [opengraph.xyz](https://www.opengraph.xyz/)

## File Organization

```
src/app/
├── opengraph-image.png           # Static homepage OG
├── about/
│   └── opengraph-image.tsx       # Dynamic About OG
├── blog/
│   └── [slug]/
│       └── opengraph-image.tsx   # Dynamic blog post OG
├── cars/
│   └── opengraph-image.tsx       # Dynamic cars section OG
└── coe/
    └── opengraph-image.tsx       # Dynamic COE section OG
```

## Validation Checklist

When creating/updating OG images:

- [ ] Exports `alt`, `size`, and `contentType`
- [ ] Uses standard 1200x630 dimensions
- [ ] Follows three-part structure (eyebrow, headline, subheadline)
- [ ] Uses brand colours from palette
- [ ] Loads Geist fonts for custom typography
- [ ] Uses inline styles only (no CSS classes)
- [ ] Eyebrow text clearly indicates page context
- [ ] Headline is concise and fits on two lines max
- [ ] Subheadline provides useful context
- [ ] Tested in social media debuggers

## Related Files

- `apps/web/CLAUDE.md` - Web app conventions
- `apps/web/assets/fonts/` - Geist font files
- `apps/web/src/config/index.ts` - Site title and URL constants
