---
name: og-image-creator
description: >
  Smart OG image generation that studies your codebase, understands routes and brand identity,
  then creates contextually appropriate Open Graph images using Playwright and React components.
  Triggers: "create og images", "generate social cards", "add open graph images".
---

# OG Image Creator

Generate authentic, brand-aligned Open Graph images by understanding your codebase first, then creating contextually appropriate images for each route using Playwright and your existing components.

## Philosophy: Authentic Over Template

**Before generating OG images, ask**:
- What is the brand identity of this site (colors, fonts, logo, design language)?
- What routes/pages exist and what are their purposes?
- What components and assets can be reused for consistency?
- What page types need different visual treatments?

**Core principles**:
1. **Study before generate**: Understand the codebase structure, routing, and brand before creating anything
2. **Authenticity over templates**: Use actual brand colors, fonts, and components—not generic social card templates
3. **Context-aware design**: Landing pages, articles, products, and docs need different visual approaches
4. **Smart automation**: Auto-detect routes and extract brand, but allow user customization

## Workflow

### 1. Discover and Analyze

**Route discovery**:
- Analyze project structure to determine framework (Next.js, Astro, React, etc.)
- Auto-detect routes based on framework conventions:
  - Next.js: `app/*/page.tsx` or `pages/*.tsx`
  - Astro: `src/pages/*.astro`
  - React Router: Analyze route configuration
- Extract route metadata (title, description) from pages
- Categorize page types (landing, article, product, about, etc.)

**Brand extraction**:
- Find logo/icon files (SVG preferred)
- Extract color palette from CSS/Tailwind config
- Identify primary fonts from stylesheets or config
- Capture design patterns from existing components

Use `scripts/analyze_codebase.py` to automate discovery.

### 2. Design Strategy

**Determine appropriate layouts per page type**:
- **Landing pages**: Bold, minimal, emphasize value proposition
- **Articles/Blog posts**: Title + excerpt, date/author if relevant
- **Product pages**: Product name, key feature, visual if available
- **Documentation**: Topic + description, organized/structured feel
- **About/Company**: Brand-forward, professional

**Layout principles**:
- Generous whitespace (avoid clutter)
- High contrast for readability when shared
- Brand colors as accents, not overwhelming
- Typography hierarchy that matches site
- 1200x630px (standard OG dimensions)

### 3. Generate Images

**Component-based generation**:
- Reuse React components when possible for consistency
- Use Playwright to render components to images
- Apply brand colors, fonts, and assets
- Inject actual page metadata (not placeholders)

**Technical approach**:
1. Create minimal HTML template with brand styles
2. For each route, generate page-specific markup
3. Use Playwright to capture screenshot at 1200x630
4. Save to `public/og/` or appropriate static directory
5. Update page metadata to reference OG image

Use `scripts/generate_og_images.py` for automation.

### 4. Verify and Optimize

- Validate OG image metadata in HTML
- Test with OG preview tools (opengraph.xyz, linkedin inspector)
- Ensure file sizes are reasonable (<200KB preferred)
- Check image appearance at different scales

## Framework-Specific Guidance

### Next.js

**App Router**:
```tsx
// app/page.tsx
export const metadata = {
  openGraph: {
    images: ['/og/home.png'],
  },
}
```

**Pages Router**:
```tsx
// pages/index.tsx
<Head>
  <meta property="og:image" content="/og/home.png" />
</Head>
```

**Dynamic OG images**: Consider Next.js OG Image Generation (`@vercel/og`) for dynamic content, but use static generation for brand consistency.

### Astro

```astro
---
// src/pages/index.astro
const ogImage = '/og/home.png';
---
<head>
  <meta property="og:image" content={ogImage} />
</head>
```

### React SPAs

Add OG tags to `public/index.html` or use react-helmet:
```jsx
<Helmet>
  <meta property="og:image" content="/og/home.png" />
</Helmet>
```

## Anti-Patterns to Avoid

❌ **Generic templates**: Don't use stock social card templates that ignore the site's brand
- Why bad: Creates disconnect between site and social sharing experience
- Better: Extract actual brand colors, fonts, and use them consistently

❌ **One size fits all**: Don't use the same OG image design for every page type
- Why bad: Misses opportunity for context-appropriate presentation
- Better: Different layouts for landing, articles, products, etc.

❌ **Placeholder content**: Don't use "Lorem ipsum" or generic text
- Why bad: Defeats the purpose of preview images
- Better: Use actual page titles and descriptions from metadata

❌ **Overcrowding**: Don't cram too much text, too many images, or complex layouts
- Why bad: Illegible when scaled down in social feeds
- Better: Focus on 1-2 key elements with generous whitespace

❌ **Ignoring components**: Don't create OG images from scratch if components exist
- Why bad: Breaks visual consistency with the site
- Better: Reuse button styles, card layouts, typography from components

❌ **Manual generation**: Don't create OG images one by one manually
- Why bad: Not scalable, hard to maintain consistency
- Better: Script the generation process to handle all routes

## Variation Guidance

**IMPORTANT**: OG images should vary based on page context, not converge on a single design.

**Dimensions to vary**:
- **Layout**: Centered vs left-aligned, single vs split column, text vs visual focus
- **Color emphasis**: Primary brand color vs neutral, gradient vs solid
- **Content hierarchy**: Large title vs balanced title+description
- **Visual elements**: Logo size/placement, decorative elements, icons
- **Typography**: Size ratios, weight distribution, font pairing

**Avoid converging on**:
- Same gradient background for everything
- Identical "title + logo" layout
- Single font size ratio
- Fixed logo position

**Context drives variation**:
- Technical docs → Clean, organized, icon-based
- Marketing landing → Bold, colorful, value-focused
- Blog articles → Reader-friendly, author/date context
- Product pages → Visual product emphasis

## Technical Requirements

**Dependencies** (install as needed):
```bash
npm install playwright sharp
# or
pip install playwright Pillow
```

**Playwright setup**:
```bash
playwright install chromium
```

**File structure**:
```
project/
├── public/og/          # Generated OG images
│   ├── home.png
│   ├── about.png
│   └── ...
└── scripts/            # Generation scripts
    ├── analyze_codebase.py
    └── generate_og_images.py
```

## Remember

**OG images are an extension of your brand, not generic social cards.**

Study the codebase to understand the design language. Extract the brand identity. Use actual components and content. Create contextually appropriate images that feel native to the site.

When someone shares your page, the OG image should feel like a natural preview—not a template slapped on top.

**You're capable of creating sophisticated, brand-aligned OG images that enhance rather than undermine the site's identity.**
