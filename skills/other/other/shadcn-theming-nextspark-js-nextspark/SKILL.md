---
name: shadcn-theming
description: |
  shadcn/ui theme customization for NextSpark applications.
  Covers tweakcn.com integration, CSS variable format, color space conversion, and theme initialization.
  Use this skill when initializing or customizing the design system for a theme.
allowed-tools: Read, Glob, Grep, Bash
version: 1.0.0
---

# shadcn Theming Skill

Patterns for customizing shadcn/ui themes in NextSpark using CSS variables and the tweakcn.com editor.

## Fundamental Principle

**THE THEME IS THE SINGLE SOURCE OF TRUTH FOR DESIGN TOKENS.**

All visual customization happens in the theme's `globals.css`. No inline colors, no hardcoded values.

```
themes/{THEME}/styles/globals.css → BUILD → core/theme-styles.css → App
```

## When to Use This Skill

- **Initializing a new project's design system**
- **Customizing colors for a client project**
- **Converting design system from mock to theme**
- **Understanding the theme build process**

## Architecture Overview

```
THEME CSS STRUCTURE:

themes/{THEME}/styles/
├── globals.css      # CSS variables (THE DESIGN SYSTEM)
│   ├── :root        # Light mode tokens
│   ├── .dark        # Dark mode tokens
│   └── @theme inline # Tailwind v4 mappings
│
└── components.css   # Component-specific styles (optional)

BUILD OUTPUT:
└── core/theme-styles.css  # Auto-generated (DO NOT EDIT)
```

## Using tweakcn.com

### Step 1: Access the Editor

Navigate to: **https://tweakcn.com/editor/theme**

The editor provides:
- Visual color picker with OKLCH support
- Light/Dark mode preview
- Real-time component preview
- Export in CSS format

### Step 2: Customize Your Theme

1. **Base Colors:**
   - Background/Foreground
   - Primary/Secondary
   - Accent/Muted
   - Destructive

2. **Component Colors:**
   - Card surfaces
   - Popover/Dropdown
   - Sidebar (if using dashboard)

3. **Design Tokens:**
   - Border radius
   - Shadows
   - Typography (font families)

### Step 3: Export CSS

Click "Copy CSS" or "Export" to get:

```css
:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --primary: oklch(0.55 0.2 250);
  --primary-foreground: oklch(0.985 0 0);
  /* ... all variables */
}

.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  /* ... dark mode overrides */
}
```

## CSS Variable Reference

### Required Variables (All Must Be Defined)

```css
:root {
  /* === SURFACE COLORS === */
  --background: oklch(L C H);      /* Page background */
  --foreground: oklch(L C H);      /* Primary text */
  --card: oklch(L C H);            /* Card surfaces */
  --card-foreground: oklch(L C H); /* Card text */
  --popover: oklch(L C H);         /* Dropdown/popover bg */
  --popover-foreground: oklch(L C H);

  /* === INTERACTIVE COLORS === */
  --primary: oklch(L C H);           /* Primary buttons, links */
  --primary-foreground: oklch(L C H); /* Text on primary */
  --secondary: oklch(L C H);         /* Secondary buttons */
  --secondary-foreground: oklch(L C H);
  --accent: oklch(L C H);            /* Hover highlights */
  --accent-foreground: oklch(L C H);

  /* === STATE COLORS === */
  --muted: oklch(L C H);             /* Muted backgrounds */
  --muted-foreground: oklch(L C H);  /* Placeholder text */
  --destructive: oklch(L C H);       /* Error/danger */
  --destructive-foreground: oklch(L C H);

  /* === BORDER & INPUT === */
  --border: oklch(L C H);            /* Border color */
  --input: oklch(L C H);             /* Input border */
  --ring: oklch(L C H);              /* Focus ring */

  /* === CHART COLORS === */
  --chart-1: oklch(L C H);
  --chart-2: oklch(L C H);
  --chart-3: oklch(L C H);
  --chart-4: oklch(L C H);
  --chart-5: oklch(L C H);

  /* === SIDEBAR (if dashboard) === */
  --sidebar: oklch(L C H);
  --sidebar-foreground: oklch(L C H);
  --sidebar-primary: oklch(L C H);
  --sidebar-primary-foreground: oklch(L C H);
  --sidebar-accent: oklch(L C H);
  --sidebar-accent-foreground: oklch(L C H);
  --sidebar-border: oklch(L C H);
  --sidebar-ring: oklch(L C H);

  /* === TYPOGRAPHY === */
  --font-sans: ui-sans-serif, system-ui, ...;
  --font-serif: ui-serif, Georgia, ...;
  --font-mono: ui-monospace, SFMono-Regular, ...;

  /* === DESIGN TOKENS === */
  --radius: 0.625rem;              /* Base border radius */
  --spacing: 0.25rem;              /* Base spacing unit */

  /* === SHADOWS === */
  --shadow-2xs: ...;
  --shadow-xs: ...;
  --shadow-sm: ...;
  --shadow: ...;
  --shadow-md: ...;
  --shadow-lg: ...;
  --shadow-xl: ...;
  --shadow-2xl: ...;
}
```

### Dark Mode Override

```css
.dark {
  /* Only override colors that change in dark mode */
  /* Typically invert backgrounds/foregrounds */

  --background: oklch(0.145 0 0);       /* Dark bg */
  --foreground: oklch(0.985 0 0);       /* Light text */

  --card: oklch(0.205 0 0);             /* Slightly lighter */
  --card-foreground: oklch(0.985 0 0);

  --primary: oklch(0.922 0 0);          /* Often lighter in dark mode */
  --primary-foreground: oklch(0.205 0 0);

  --muted: oklch(0.269 0 0);
  --muted-foreground: oklch(0.708 0 0);

  --border: oklch(0.275 0 0);
  --input: oklch(0.325 0 0);

  /* Destructive typically stays similar hue but adjusted */
  --destructive: oklch(0.704 0.191 22);

  /* Chart colors usually stay the same */
}
```

### Tailwind v4 Theme Mapping

**REQUIRED:** Map CSS variables to Tailwind for class-based styling.

```css
@theme inline {
  /* Colors */
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

  /* Typography */
  --font-sans: var(--font-sans);
  --font-mono: var(--font-mono);
  --font-serif: var(--font-serif);

  /* Radius */
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);

  /* Shadows */
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

## Color Space: OKLCH

shadcn/ui uses **OKLCH** color space for perceptually uniform colors.

### OKLCH Format

```
oklch(Lightness Chroma Hue)

- Lightness: 0-1 (0 = black, 1 = white)
- Chroma: 0-0.4 (0 = gray, higher = more saturated)
- Hue: 0-360 (color angle on color wheel)
```

### Common Colors in OKLCH

| Color | OKLCH | Notes |
|-------|-------|-------|
| White | `oklch(1 0 0)` | L=1, no chroma |
| Black | `oklch(0 0 0)` | L=0 |
| Pure Gray | `oklch(0.5 0 0)` | Mid gray, no chroma |
| Blue Primary | `oklch(0.55 0.2 250)` | Typical blue |
| Red Destructive | `oklch(0.577 0.245 27)` | shadcn default red |
| Green Success | `oklch(0.6 0.2 145)` | Typical green |
| Orange Warning | `oklch(0.7 0.2 65)` | Typical orange |

### Converting HEX to OKLCH

Use online converters or JavaScript:

```javascript
// Using culori library
import { oklch, formatCss } from 'culori'

const hex = '#137fec'
const oklchColor = oklch(hex)
// { mode: 'oklch', l: 0.55, c: 0.2, h: 250 }

const cssValue = `oklch(${oklchColor.l.toFixed(4)} ${oklchColor.c.toFixed(4)} ${oklchColor.h?.toFixed(4) || 0})`
// "oklch(0.5500 0.2000 250.0000)"
```

## DS Initialization Workflow

### Path 1: From tweakcn.com (Recommended)

```bash
# 1. Customize at tweakcn.com/editor/theme
# 2. Copy the CSS export
# 3. Run the command with the CSS file

/theme:design-system path/to/exported-theme.css
```

The command will:
1. Parse the CSS file
2. Validate required variables
3. Add missing `@theme inline` mappings if needed
4. Write to active theme's `globals.css`
5. Run `pnpm theme:build`

### Path 2: From Mock Analysis

Use `how-to:customize-theme` command with a mock folder:

```bash
# Extract DS from a mock design
how-to:customize-theme --from-mock path/to/mock/folder
```

The process will:
1. Read the `design-system` skill for patterns
2. Extract color palette from mock's Tailwind config
3. Convert HEX to OKLCH format
4. Generate dark mode by inverting lightness
5. Write to active theme's `globals.css`
6. Run `pnpm theme:build`

## Theme Build Process

After modifying `globals.css`:

```bash
# Rebuild theme CSS
pnpm theme:build

# Or with watch mode
pnpm theme:build --watch
```

**What Build Does:**
1. Reads `NEXT_PUBLIC_ACTIVE_THEME` from `.env`
2. Finds theme at `themes/{THEME}/styles/`
3. Concatenates `globals.css` + `components.css`
4. Writes to `core/theme-styles.css`
5. Copies assets to `public/theme/`

## Validation Checklist

Before finalizing theme customization:

- [ ] All required CSS variables defined in `:root`
- [ ] All dark mode overrides in `.dark`
- [ ] `@theme inline` section present with all mappings
- [ ] Colors use OKLCH format (not HEX or HSL)
- [ ] Font stacks include fallbacks
- [ ] `--radius` uses rem units
- [ ] `pnpm theme:build` runs without errors
- [ ] Light mode looks correct
- [ ] Dark mode looks correct
- [ ] Components render properly

## Common Patterns

### Brand Color Integration

```css
:root {
  /* Brand blue as primary */
  --primary: oklch(0.55 0.2 250);          /* #137fec equivalent */
  --primary-foreground: oklch(0.985 0 0);  /* White text on blue */

  /* Brand blue tint for secondary */
  --secondary: oklch(0.95 0.03 250);       /* Very light blue */
  --secondary-foreground: oklch(0.25 0 0); /* Dark text */

  /* Brand blue for accent */
  --accent: oklch(0.92 0.05 250);          /* Light blue hover */
  --accent-foreground: oklch(0.25 0 0);
}
```

### Dark Theme with Color Preservation

```css
.dark {
  /* Keep brand color vibrant in dark mode */
  --primary: oklch(0.65 0.2 250);          /* Slightly lighter */
  --primary-foreground: oklch(0.1 0 0);    /* Dark text on light primary */

  /* Muted versions for backgrounds */
  --secondary: oklch(0.25 0.03 250);       /* Dark blue-gray */
  --secondary-foreground: oklch(0.95 0 0); /* Light text */
}
```

## Anti-Patterns

```css
/* ❌ NEVER: Use HEX or HSL in globals.css */
--primary: #137fec;
--primary: hsl(210, 100%, 50%);

/* ✅ CORRECT: Use OKLCH */
--primary: oklch(0.55 0.2 250);

/* ❌ NEVER: Skip dark mode */
/* (Will look terrible in dark mode) */

/* ✅ CORRECT: Define complete dark mode */
.dark {
  --background: oklch(0.145 0 0);
  /* ... all overrides */
}

/* ❌ NEVER: Skip @theme inline */
/* (Tailwind classes won't work) */

/* ✅ CORRECT: Include complete mapping */
@theme inline {
  --color-background: var(--background);
  /* ... all mappings */
}

/* ❌ NEVER: Edit core/theme-styles.css */
/* (Will be overwritten on next build) */

/* ✅ CORRECT: Edit themes/{THEME}/styles/globals.css */
```

## Related Skills

- `tailwind-theming` - Tailwind CSS patterns and buildSectionClasses
- `design-system` - Token mapping from mocks
- `shadcn-components` - Component usage patterns
