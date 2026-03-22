---
name: design-system
description: |
  Theme-aware design system analysis and token mapping.
  Covers extracting theme tokens, mapping mock values, and gap analysis.
  CRITICAL: All values are EXAMPLES - always read actual theme globals.css.
allowed-tools: Read, Glob, Grep
version: 1.0.0
---

# Design System Skill

Patterns for analyzing design tokens and mapping between mocks and NextSpark themes.

## Fundamental Principle

**THE DESIGN SYSTEM IS THEME-DEPENDENT.**

All values in this skill are EXAMPLES from the default theme.
You MUST read the actual theme's `globals.css` to get real values.

```bash
# Determine active theme
grep "NEXT_PUBLIC_ACTIVE_THEME" .env .env.local

# Read theme tokens
cat contents/themes/{THEME}/styles/globals.css
```

## Theme Token Locations

```
contents/themes/{THEME}/
├── styles/
│   ├── globals.css      # CSS variables (:root and .dark)
│   └── components.css   # Component-specific styles
├── config/
│   └── theme.config.ts  # Theme metadata
```

## CSS Variable Structure

### Light Mode (:root)

```css
:root {
  /* Surface Colors */
  --background: oklch(1 0 0);           /* Page background */
  --foreground: oklch(0.145 0 0);       /* Primary text */
  --card: oklch(1 0 0);                 /* Card surfaces */
  --card-foreground: oklch(0.145 0 0);  /* Card text */
  --popover: oklch(1 0 0);              /* Dropdowns */
  --popover-foreground: oklch(0.145 0 0);

  /* Interactive Colors */
  --primary: oklch(0.205 0 0);          /* Primary actions */
  --primary-foreground: oklch(0.985 0 0);
  --secondary: oklch(0.97 0 0);         /* Secondary actions */
  --secondary-foreground: oklch(0.205 0 0);
  --accent: oklch(0.97 0 0);            /* Highlights */
  --accent-foreground: oklch(0.205 0 0);

  /* State Colors */
  --muted: oklch(0.97 0 0);             /* Muted backgrounds */
  --muted-foreground: oklch(0.556 0 0); /* Placeholder text */
  --destructive: oklch(0.577 0.245 27); /* Error/danger */
  --destructive-foreground: oklch(1 0 0);

  /* Border & Input */
  --border: oklch(0.922 0 0);
  --input: oklch(0.922 0 0);
  --ring: oklch(0.708 0 0);             /* Focus rings */

  /* Radius */
  --radius: 0.5rem;
}
```

### Dark Mode (.dark)

```css
.dark {
  --background: oklch(0.145 0 0);       /* Inverted */
  --foreground: oklch(0.985 0 0);
  --card: oklch(0.145 0 0);
  --card-foreground: oklch(0.985 0 0);

  --primary: oklch(0.922 0 0);          /* Adjusted for dark */
  --primary-foreground: oklch(0.205 0 0);

  --muted: oklch(0.269 0 0);
  --muted-foreground: oklch(0.708 0 0);

  --border: oklch(0.269 0 0);
  --input: oklch(0.269 0 0);
}
```

## Color Format Conversion

Mocks often use HEX/RGB, themes use OKLCH.

### HEX to OKLCH Mapping

| Mock (HEX) | Approximate OKLCH | Notes |
|------------|-------------------|-------|
| `#ffffff` | `oklch(1 0 0)` | Pure white |
| `#000000` | `oklch(0 0 0)` | Pure black |
| `#137fec` | `oklch(0.55 0.2 250)` | Blue primary |
| `#101922` | `oklch(0.15 0.02 260)` | Dark background |
| `#00d4ff` | `oklch(0.75 0.15 200)` | Cyan accent |

### Similarity Calculation

Compare colors by:
1. **Lightness** (L) - Most important, weight 0.5
2. **Chroma** (C) - Saturation, weight 0.3
3. **Hue** (H) - Color angle, weight 0.2

```
similarity = 1 - (
  0.5 * |L1 - L2| +
  0.3 * |C1 - C2| / maxChroma +
  0.2 * |H1 - H2| / 360
)
```

## Token Categories

### Background Tokens

| Token | Tailwind Class | Usage |
|-------|----------------|-------|
| `--background` | `bg-background` | Page background |
| `--card` | `bg-card` | Card surfaces |
| `--popover` | `bg-popover` | Dropdowns, menus |
| `--muted` | `bg-muted` | Subtle backgrounds |
| `--accent` | `bg-accent` | Hover states |
| `--primary` | `bg-primary` | Primary buttons |
| `--secondary` | `bg-secondary` | Secondary buttons |
| `--destructive` | `bg-destructive` | Error states |

### Foreground Tokens

| Token | Tailwind Class | Usage |
|-------|----------------|-------|
| `--foreground` | `text-foreground` | Primary text |
| `--card-foreground` | `text-card-foreground` | Card text |
| `--muted-foreground` | `text-muted-foreground` | Secondary text |
| `--primary-foreground` | `text-primary-foreground` | On primary bg |
| `--destructive-foreground` | `text-destructive-foreground` | On error bg |

### Border Tokens

| Token | Tailwind Class | Usage |
|-------|----------------|-------|
| `--border` | `border-border` | Default borders |
| `--input` | `border-input` | Input borders |
| `--ring` | `ring-ring` | Focus rings |

## Mapping Process

### Step 1: Extract Mock Tokens

From Tailwind config or inline styles:
```javascript
// From mock's tailwind.config
const mockTokens = {
  colors: {
    primary: '#137fec',
    'bg-dark': '#101922',
    accent: '#00d4ff'
  }
}
```

### Step 2: Read Theme Tokens

```bash
# Extract all CSS variables
grep -E "^\s*--" contents/themes/{theme}/styles/globals.css
```

### Step 3: Create Mapping

For each mock token:
1. Check exact match (hex → hex)
2. Check semantic match (primary → --primary)
3. Calculate color similarity
4. Flag gaps if no good match

### Step 4: Document Gaps

```json
{
  "gaps": [
    {
      "mockValue": "#ff5722",
      "mockUsage": "accent icons",
      "closestToken": "--destructive",
      "similarity": 0.72,
      "recommendation": "USE_CLOSEST or ADD_TOKEN"
    }
  ]
}
```

## Output Format: ds-mapping.json

```json
{
  "theme": "default",
  "themeGlobalsPath": "contents/themes/default/styles/globals.css",
  "analyzedAt": "2025-01-09T12:00:00Z",

  "themeTokens": {
    "colors": {
      "--background": "oklch(1 0 0)",
      "--foreground": "oklch(0.145 0 0)",
      "--primary": "oklch(0.205 0 0)",
      "--secondary": "oklch(0.97 0 0)",
      "--accent": "oklch(0.97 0 0)",
      "--muted": "oklch(0.97 0 0)",
      "--destructive": "oklch(0.577 0.245 27.325)"
    },
    "radius": "0.5rem",
    "fonts": {
      "sans": "var(--font-sans)",
      "mono": "var(--font-mono)"
    }
  },

  "mockTokens": {
    "colors": {
      "primary": "#137fec",
      "background-dark": "#101922",
      "accent": "#00d4ff",
      "text-light": "#ffffff",
      "text-muted": "#94a3b8"
    }
  },

  "colorMapping": [
    {
      "id": "color-1",
      "mockValue": "#137fec",
      "mockName": "primary",
      "mockUsage": ["buttons", "links", "focus rings"],
      "themeToken": "--primary",
      "themeValue": "oklch(0.205 0 0)",
      "tailwindClass": "bg-primary text-primary-foreground",
      "matchType": "semantic",
      "similarity": 0.65,
      "notes": "Theme primary is darker, mock is more vibrant blue"
    },
    {
      "id": "color-2",
      "mockValue": "#101922",
      "mockName": "background-dark",
      "mockUsage": ["hero background", "footer"],
      "themeToken": "--background",
      "themeValue": "oklch(0.145 0 0)",
      "tailwindClass": "bg-background",
      "matchType": "closest",
      "similarity": 0.88,
      "notes": "Use dark mode or bg-gray-900"
    }
  ],

  "typographyMapping": [
    {
      "mockFont": "Inter",
      "themeToken": "--font-sans",
      "tailwindClass": "font-sans",
      "matchType": "exact"
    }
  ],

  "spacingMapping": [
    {
      "mockValue": "24px",
      "tailwindClass": "p-6",
      "matchType": "exact"
    }
  ],

  "radiusMapping": [
    {
      "mockValue": "8px",
      "themeToken": "--radius",
      "themeValue": "0.5rem",
      "tailwindClass": "rounded-lg",
      "matchType": "exact"
    }
  ],

  "gaps": [
    {
      "type": "color",
      "mockValue": "#00d4ff",
      "mockName": "accent",
      "mockUsage": ["terminal prompt", "code highlights"],
      "closestToken": "--primary",
      "similarity": 0.45,
      "recommendations": [
        {
          "option": "A",
          "action": "Use --primary",
          "impact": "Loses cyan accent, uses theme primary"
        },
        {
          "option": "B",
          "action": "Add --accent-cyan to theme",
          "impact": "Requires theme modification"
        },
        {
          "option": "C",
          "action": "Use inline text-[#00d4ff]",
          "impact": "Not recommended, breaks theming"
        }
      ]
    }
  ],

  "summary": {
    "totalMockTokens": 12,
    "mapped": 10,
    "gaps": 2,
    "overallCompatibility": 0.83,
    "recommendation": "PROCEED_WITH_GAPS"
  }
}
```

## Output Format: block-plan.json (BLOCKS workflow only)

For the BLOCKS workflow, an additional output is generated to guide block development:

```json
{
  "mockPath": "mocks/",
  "analyzedAt": "2026-01-12T12:00:00Z",
  "workflow": "BLOCKS",

  "existingBlocks": [
    {
      "name": "hero-simple",
      "similarity": 0.85,
      "matchReason": "Similar layout and components"
    },
    {
      "name": "hero-centered",
      "similarity": 0.72,
      "matchReason": "Centered text, different background"
    }
  ],

  "decision": {
    "type": "new" | "variant" | "existing",
    "blockName": "hero-terminal",
    "baseBlock": "hero-simple",
    "reasoning": "Requires custom terminal animation component not in existing blocks"
  },

  "blockSpec": {
    "name": "hero-terminal",
    "category": "hero",
    "fields": [
      {"name": "title", "type": "text", "required": true},
      {"name": "subtitle", "type": "text", "required": false},
      {"name": "primaryCta", "type": "link", "required": true},
      {"name": "secondaryCta", "type": "link", "required": false},
      {"name": "terminalContent", "type": "textarea", "required": true}
    ],
    "customComponents": ["TerminalAnimation"],
    "estimatedComplexity": "medium"
  },

  "developmentNotes": [
    "Terminal animation requires custom React component",
    "Use existing Button component for CTAs",
    "Background gradient matches theme --background token"
  ]
}
```

### Decision Types

| Type | When to Use | Action |
|------|-------------|--------|
| `existing` | Mock matches existing block 90%+ | Use existing block, no changes |
| `variant` | Mock matches but needs minor additions | Extend existing block with new variant |
| `new` | Mock requires significant new functionality | Create new block from scratch |

## Workflow Integration

| Workflow | ds-mapping.json | block-plan.json | When Generated |
|----------|-----------------|-----------------|----------------|
| **BLOCKS** | Yes | Yes | Phase 1 (Mock Analysis) |
| **TASK** | Yes (if mock) | No | Phase 0.6 (if mock selected) |
| **STORY** | Yes (if mock) | No | Phase 0.6 (if mock selected) |
| **TWEAK** | No | No | N/A |

## Reusability

This skill applies to ANY design-to-code conversion:
- Landing pages (mocks → blocks)
- Email templates (design → HTML)
- PDF templates (design → React-PDF)
- Marketing materials

---

## Generating globals.css from Mock (One-Time Setup)

Use this section when initializing a theme from a design mock. This is typically a **one-time setup task** during theme creation.

### When to Use

- New theme creation from design mock
- Theme initialization via `how-to:customize-theme` command
- Converting a purchased template to NextSpark theme

### Step 1: Convert HEX to OKLCH

For each color in mock's Tailwind config, convert from HEX to OKLCH:

```javascript
function hexToOklch(hex) {
  // Remove # if present
  hex = hex.replace('#', '')

  // Parse RGB
  const r = parseInt(hex.substr(0, 2), 16) / 255
  const g = parseInt(hex.substr(2, 2), 16) / 255
  const b = parseInt(hex.substr(4, 2), 16) / 255

  // Convert to linear RGB
  const rL = r <= 0.04045 ? r / 12.92 : Math.pow((r + 0.055) / 1.055, 2.4)
  const gL = g <= 0.04045 ? g / 12.92 : Math.pow((g + 0.055) / 1.055, 2.4)
  const bL = b <= 0.04045 ? b / 12.92 : Math.pow((b + 0.055) / 1.055, 2.4)

  // Approximate OKLCH
  const L = 0.4122 * rL + 0.5363 * gL + 0.0514 * bL
  const lightness = Math.cbrt(L)

  // Chroma and hue calculation
  const max = Math.max(r, g, b)
  const min = Math.min(r, g, b)
  const chroma = (max - min) * 0.3

  let hue = 0
  if (max !== min) {
    if (max === r) hue = 60 * (((g - b) / (max - min)) % 6)
    else if (max === g) hue = 60 * ((b - r) / (max - min) + 2)
    else hue = 60 * ((r - g) / (max - min) + 4)
    if (hue < 0) hue += 360
  }

  return `oklch(${lightness.toFixed(4)} ${chroma.toFixed(4)} ${hue.toFixed(0)})`
}
```

### Step 2: Generate Dark Mode (Invert Lightness)

For dark mode, invert the lightness (L) value:

```javascript
function invertLightnessOklch(oklchValue) {
  // Parse oklch(L C H)
  const match = oklchValue.match(/oklch\(([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\)/)
  if (!match) return oklchValue

  const L = parseFloat(match[1])
  const C = parseFloat(match[2])
  const H = parseFloat(match[3])

  // Invert lightness: L' = 1 - L
  const invertedL = 1 - L

  return `oklch(${invertedL.toFixed(4)} ${C.toFixed(4)} ${H.toFixed(0)})`
}
```

**Which tokens to invert:**
- `--background` ↔ `--foreground` (swap)
- `--card` ↔ `--card-foreground` (swap)
- `--popover` ↔ `--popover-foreground` (swap)
- `--muted` → invert
- `--muted-foreground` → invert
- `--border`, `--input` → invert
- `--primary`, `--secondary`, `--accent` → typically keep similar or slightly adjust

### Step 3: globals.css Template

```css
/**
 * Theme: {theme}
 * Generated from mock: {mockPath}
 * Date: {timestamp}
 *
 * NOTE: Dark mode was auto-generated by inverting lightness values.
 * Review and adjust .dark {} section as needed for your brand.
 */

:root {
  /* Surface Colors */
  --background: {oklch from mock};
  --foreground: {oklch from mock};
  --card: {oklch from mock or default};
  --card-foreground: {oklch from mock or default};
  --popover: {oklch from mock or default};
  --popover-foreground: {oklch from mock or default};

  /* Interactive Colors */
  --primary: {oklch from mock};
  --primary-foreground: {calculated contrast};
  --secondary: {oklch from mock or default};
  --secondary-foreground: {calculated contrast};
  --accent: {oklch from mock or default};
  --accent-foreground: {calculated contrast};

  /* State Colors */
  --muted: {oklch from mock or default};
  --muted-foreground: {oklch from mock or default};
  --destructive: oklch(0.577 0.245 27.325);
  --destructive-foreground: oklch(1 0 0);

  /* Border & Input */
  --border: {oklch from mock or default};
  --input: {oklch from mock or default};
  --ring: {oklch from mock or default};

  /* Chart Colors */
  --chart-1: oklch(0.81 0.1 252);
  --chart-2: oklch(0.62 0.19 260);
  --chart-3: oklch(0.55 0.22 263);
  --chart-4: oklch(0.49 0.22 264);
  --chart-5: oklch(0.42 0.18 266);

  /* Sidebar */
  --sidebar: {based on background};
  --sidebar-foreground: {based on foreground};
  --sidebar-primary: {based on primary};
  --sidebar-primary-foreground: {based on primary-foreground};
  --sidebar-accent: {based on accent};
  --sidebar-accent-foreground: {based on accent-foreground};
  --sidebar-border: {based on border};
  --sidebar-ring: {based on ring};

  /* Typography */
  --font-sans: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  --font-serif: ui-serif, Georgia, Cambria, "Times New Roman", Times, serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;

  /* Design Tokens */
  --radius: 0.625rem;
  --spacing: 0.25rem;

  /* Shadows */
  --shadow-2xs: 0 1px 3px 0px hsl(0 0% 0% / 0.05);
  --shadow-xs: 0 1px 3px 0px hsl(0 0% 0% / 0.05);
  --shadow-sm: 0 1px 3px 0px hsl(0 0% 0% / 0.10), 0 1px 2px -1px hsl(0 0% 0% / 0.10);
  --shadow: 0 1px 3px 0px hsl(0 0% 0% / 0.10), 0 1px 2px -1px hsl(0 0% 0% / 0.10);
  --shadow-md: 0 1px 3px 0px hsl(0 0% 0% / 0.10), 0 2px 4px -1px hsl(0 0% 0% / 0.10);
  --shadow-lg: 0 1px 3px 0px hsl(0 0% 0% / 0.10), 0 4px 6px -1px hsl(0 0% 0% / 0.10);
  --shadow-xl: 0 1px 3px 0px hsl(0 0% 0% / 0.10), 0 8px 10px -1px hsl(0 0% 0% / 0.10);
  --shadow-2xl: 0 1px 3px 0px hsl(0 0% 0% / 0.25);
}

/* =============================================
   DARK MODE (Auto-generated by inverting lightness)
   Review and adjust as needed for your brand
   ============================================= */

.dark {
  --background: {inverted};
  --foreground: {inverted};
  --card: {inverted};
  --card-foreground: {inverted};
  --popover: {inverted};
  --popover-foreground: {inverted};
  --primary: {adjusted for dark};
  --primary-foreground: {adjusted for dark};
  --secondary: {inverted};
  --secondary-foreground: {inverted};
  --muted: {inverted};
  --muted-foreground: {inverted};
  --accent: {inverted};
  --accent-foreground: {inverted};
  --destructive: oklch(0.704 0.191 22.216);
  --destructive-foreground: oklch(0.985 0 0);
  --border: {inverted};
  --input: {inverted};
  --ring: {inverted};
  --sidebar: {inverted};
  --sidebar-foreground: {inverted};
  --sidebar-primary: {adjusted};
  --sidebar-primary-foreground: {adjusted};
  --sidebar-accent: {inverted};
  --sidebar-accent-foreground: {inverted};
  --sidebar-border: {inverted};
  --sidebar-ring: {inverted};
}

/* =============================================
   TAILWIND v4 THEME MAPPING
   ============================================= */

@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-card-foreground: var(--card-foreground);
  --color-popover: var(--popover);
  --color-popover-foreground: var(--popover-foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-destructive: var(--destructive);
  --color-destructive-foreground: var(--destructive-foreground);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);
  --color-chart-1: var(--chart-1);
  --color-chart-2: var(--chart-2);
  --color-chart-3: var(--chart-3);
  --color-chart-4: var(--chart-4);
  --color-chart-5: var(--chart-5);
  --color-sidebar: var(--sidebar);
  --color-sidebar-foreground: var(--sidebar-foreground);
  --color-sidebar-primary: var(--sidebar-primary);
  --color-sidebar-primary-foreground: var(--sidebar-primary-foreground);
  --color-sidebar-accent: var(--sidebar-accent);
  --color-sidebar-accent-foreground: var(--sidebar-accent-foreground);
  --color-sidebar-border: var(--sidebar-border);
  --color-sidebar-ring: var(--sidebar-ring);

  --font-sans: var(--font-sans);
  --font-mono: var(--font-mono);
  --font-serif: var(--font-serif);

  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);

  --shadow-2xs: var(--shadow-2xs);
  --shadow-xs: var(--shadow-xs);
  --shadow-sm: var(--shadow-sm);
  --shadow: var(--shadow);
  --shadow-md: var(--shadow-md);
  --shadow-lg: var(--shadow-lg);
  --shadow-xl: var(--shadow-xl);
  --shadow-2xl: var(--shadow-2xl);
}
```

### Generation Checklist

- [ ] All mock colors converted to OKLCH
- [ ] Dark mode generated with inverted lightness
- [ ] Complete @theme inline section included
- [ ] Font stacks included
- [ ] Shadow definitions included
- [ ] Clear comment indicating dark mode was auto-generated
- [ ] Complete, valid CSS output

---

## Related Skills

- `tailwind-theming` - Detailed Tailwind CSS patterns
- `shadcn-theming` - shadcn/ui theme customization
- `mock-analysis` - For extracting mock tokens
- `page-builder-blocks` - For applying tokens to blocks
- `block-decision-matrix` - For block new/variant/existing decisions
