---
name: clone-website
description: |
  Clone/replicate websites into production-ready Next.js 16 code using Firecrawl MCP.
  Use when user asks to: clone website, vibe clone, replicate landing page, copy website design,
  rebuild this site, recreate this page, clone specific sections (hero, pricing, footer, etc).
  Triggers: "clone this website", "vibe clone [url]", "replicate this landing page",
  "rebuild this site in Next.js", "clone the hero section from [url]", "copy this design".
---

# Clone Website Skill

Transform any website into production-ready Next.js 16 code using Firecrawl MCP.

## Workflow

Execute these 3 phases in order. **Never skip Phase 2.**

### Phase 1: Scrape

1. Extract URL from user request
2. Identify section filter if specified (e.g., "hero only", "just the pricing")
3. Scrape using Firecrawl:

```
firecrawl-mcp___firecrawl_scrape:
  url: [TARGET_URL]
  formats: ["markdown", "html"]
  onlyMainContent: true
```

4. If scrape fails, fallback to `firecrawl-mcp___firecrawl_crawl`

### Phase 2: Analysis (MANDATORY)

**STOP. Present analysis to user before ANY code generation.**

Read [references/analysis-template.md](references/analysis-template.md) and fill out the template with:
- Detected sections and component breakdown
- Extracted design tokens (colors, typography, spacing)
- Image inventory with download/fallback status
- Proposed file structure

Ask user: "Ready to proceed? (y/n or request modifications)"

**Do not generate code until user confirms.**

### Phase 3: Code Generation

After user confirmation, generate files in this order:

1. `app/globals.css` - Design tokens as CSS variables
2. `app/layout.tsx` - Root layout with SEO metadata
3. `components/landing/[Section].tsx` - Each component
4. `app/page.tsx` - Main page composing components
5. Download images to `public/images/`

Reference [references/tech-stack.md](references/tech-stack.md) for Next.js 16 conventions.
Reference [references/component-patterns.md](references/component-patterns.md) for component structure.

## Tech Stack (Fixed)

| Layer | Technology |
|-------|------------|
| Framework | Next.js 16 (App Router) |
| Language | TypeScript (strict) |
| Styling | Tailwind CSS v4 |
| Components | Shadcn UI |
| Icons | Lucide React |
| Font | Geist Sans (default) or extracted |

## Image Handling

1. Extract all image URLs from scraped content
2. Attempt download via fetch
3. On failure, use Unsplash fallback:
   - Hero: `https://images.unsplash.com/photo-[id]?w=1920&h=1080`
   - Avatars: `https://images.unsplash.com/photo-[id]?w=100&h=100`
   - Features: Prefer Lucide icons over images
4. Save to `public/images/` with descriptive kebab-case names

## Partial Cloning

Parse user request for section filters:

| Request | Action |
|---------|--------|
| "clone the hero from X" | Generate only Hero.tsx |
| "clone pricing and footer" | Generate Pricing.tsx + Footer.tsx |
| "clone X" (no filter) | Full page clone |

## Code Standards

- Mobile-first responsive design
- Use Tailwind arbitrary values for pixel-perfection: `w-[347px]`
- Extract repeated colors to CSS variables
- Use `cn()` utility for conditional classes
- Add brief comments only for non-obvious patterns
- Prefer `gap-*` over margins for flex/grid spacing
- Use `size-*` over `w-* h-*` when values match
