---
name: extract-design
description: Extract a complete design system — colors, typography, spacing, components, shadows, and W3C design tokens — from any live website using Dembrandt. Runs a headless browser against the URL and returns real computed values from the DOM. Use when you need a site's actual design tokens, want to reverse-engineer a visual design, or need to seed a design system from an existing product.
metadata:
  priority: 9
  pathPatterns:
    - "**/tokens/**"
    - "**/theme/**"
    - "tailwind.config.*"
    - "**/design-system/**"
    - "**/*.css"
    - "**/*.scss"
    - "**/styles/**"
  promptSignals:
    phrases:
      - "extract design"
      - "design tokens"
      - "reverse engineer"
      - "copy design"
      - "extract colors"
      - "extract typography"
      - "brand tokens"
      - "design system from"
      - "extract from website"
      - "dembrandt"
      - "what colors does"
      - "what fonts does"
      - "design of this site"
retrieval:
  aliases:
    - extract design tokens
    - reverse engineer design
    - get colors from website
    - extract brand
    - design system extraction
    - dembrandt
    - copy design system
  intents:
    - extract design tokens from a live site
    - reverse engineer a website's visual design
    - seed a new design system from an existing product
    - get exact colors, fonts, and spacing from a URL
    - analyze a competitor's design system
    - generate tailwind config from a real site
    - generate shadcn theme from a real site
  examples:
    - extract the design system from stripe.com
    - what colors and fonts does linear.app use
    - reverse engineer vercel.com's design tokens
    - get the tailwind config for this site
    - copy the design system from this URL
    - what is the primary color of this website
---

# Extract Design — Dembrandt

Dembrandt runs a headless Chromium browser against any URL, walks up to thousands of DOM elements, reads computed CSS, and returns a structured design system: colors with confidence scoring, typography styles, spacing scale, border radius, borders, shadows, and interactive component styles.

## How to Run

```bash
# Install once (global)
npm i -g dembrandt

# Basic extraction — outputs to terminal
dembrandt https://stripe.com

# JSON output — pipe into files or other tools
dembrandt https://stripe.com --json-only > stripe-tokens.json

# W3C DTCG format (design-tokens.org standard)
dembrandt https://stripe.com --dtcg --save-output

# Generate DESIGN.md (human + AI readable brand doc)
dembrandt https://stripe.com --design-md

# Multi-page crawl (follows internal links)
dembrandt https://stripe.com --pages 5

# Dark mode colors
dembrandt https://stripe.com --dark-mode

# Mobile viewport
dembrandt https://stripe.com --mobile

# Everything saved to output/
dembrandt https://stripe.com --save-output
```

## Output Structure

Dembrandt returns a structured object. The key sections:

```
colors.palette        — Deduplicated colors with confidence (high/medium/low)
colors.semantic       — Primary, secondary color detection
colors.cssVariables   — Named CSS custom properties with LCH + OKLCH values
typography.styles     — Font family, size, weight, line-height per context
typography.sources    — Google Fonts, Adobe Fonts, variable font detection
spacing.commonValues  — Margin/padding scale with rem equivalents
spacing.scaleType     — 4px, 8px, or custom grid
borderRadius.values   — Border radius tokens with element context
borders.combinations  — Width + style + color combinations
shadows               — Box shadow elevation system
components.buttons    — Button variants with hover/active/focus states
components.inputs     — Input styles with focus states
components.links      — Link colors and hover states
components.badges     — Badge/tag/chip variants
breakpoints           — Responsive breakpoints from CSS media queries
frameworks            — Detected CSS framework (Tailwind, shadcn, MUI, etc.)
iconSystem            — Detected icon library (Heroicons, FA, Material, etc.)
```

## Working with Extracted Tokens

### Seeding a Tailwind config

After extraction, map the output to `tailwind.config.js`:

```js
// tailwind.config.js
export default {
  theme: {
    colors: {
      primary: '#hex-from-colors.palette[0]',
      // ...
    },
    fontFamily: {
      sans: ['Family from typography.styles', 'system-ui'],
    },
    spacing: {
      // Map spacing.commonValues px → rem
    },
    borderRadius: {
      // Map borderRadius.values
    },
    boxShadow: {
      // Map shadows
    },
  }
}
```

### Seeding a shadcn/ui theme

Map semantic colors to shadcn CSS variables in HSL:

```css
:root {
  --background: /* from colors.palette — lightest neutral */;
  --foreground: /* from colors.palette — darkest neutral */;
  --primary: /* from colors.semantic.primary */;
  --primary-foreground: /* contrasting color */;
  --muted: /* mid-tone neutral */;
  --border: /* from borders.combinations[0].color */;
  --radius: /* from borderRadius.values[0].value */;
}
```

### Reading confidence levels

Dembrandt scores every color by semantic context:

| Confidence | Meaning |
|---|---|
| **high** | Appears on semantically labeled elements (buttons, CTAs, headers with brand classes). Almost certainly a brand color. |
| **medium** | Moderate frequency or moderate context. Likely a brand color. |
| **low** | Rare, low semantic context. May be a one-off or component-specific color. |

Start with `high` confidence colors when building a palette. Include `medium` for full coverage. Treat `low` as reference only.

## Flags Reference

| Flag | What it does |
|---|---|
| `--json-only` | Clean JSON to stdout — pipe into files or tools |
| `--save-output` | Save JSON to `output/<domain>/<timestamp>.json` |
| `--dtcg` | W3C Design Tokens Community Group format |
| `--design-md` | Generate `DESIGN.md` — prose-first brand doc |
| `--brand-guide` | Generate a PDF brand guide |
| `--dark-mode` | Extract dark color scheme and merge into palette |
| `--mobile` | Extract at 390px mobile viewport |
| `--pages <n>` | Crawl up to N pages and merge tokens |
| `--sitemap` | Discover pages from sitemap.xml |
| `--slow` | 3× timeouts — use on slow-loading or JS-heavy sites |
| `--screenshot <path>` | Save a full-page screenshot |
| `--raw-colors` | Include pre-filter raw colors in JSON output |
| `--browser firefox` | Use Firefox instead of Chromium |

## Anti-Bot and SPA Handling

Dembrandt handles common extraction challenges automatically:

- **SPA hydration** — waits 8s for React/Vue/Svelte to render before extracting
- **Bot detection** — spoofs hardware concurrency, device memory, removes webdriver traces
- **Lazy content** — scrolls the full page to trigger lazy-loaded components
- **Cloudflare / bot walls** — auto-retries with a visible browser if headless is blocked
- **Slow sites** — use `--slow` for 3× timeouts on heavy JS bundles

## Checklist After Extraction

- [ ] Identify the 3–5 high-confidence colors — these are the core brand palette
- [ ] Check `colors.semantic.primary` — is it correct?
- [ ] Look at `typography.styles` — what are the heading and body fonts?
- [ ] Check `spacing.scaleType` — 4px or 8px grid?
- [ ] Review `components.buttons` — how many variants exist?
- [ ] Check `frameworks` — is Tailwind, shadcn, or MUI detected? This shapes how you apply the tokens.
- [ ] Use `--dark-mode` if the site has a dark theme
- [ ] Use `--pages 3` if the site has a multi-section design system spread across routes
