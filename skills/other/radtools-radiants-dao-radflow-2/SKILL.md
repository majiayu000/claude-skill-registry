---
name: radtools-figma-sync
description: Set up or update RadTools design system from Figma. Use ONLY for initial design system import (colors, typography, spacing tokens) or when syncing design system updates from Figma. NOT for building pages or components from Figma designs - those use Figma MCP directly with existing RadTools tokens.
compatibility: Requires Figma MCP server and RadTools devtools/ directory
---

# Figma → RadTools Design System Sync

Import or update the RadTools design system from Figma. This is for **design system setup**, not everyday component building.

## When to Use This Skill

✅ **Use this skill for:**
- Initial project setup: importing colors, typography, spacing from Figma
- Design system updates: syncing new tokens after Figma design changes
- Adding new color palettes or typography scales

❌ **Do NOT use for:**
- Building individual pages from Figma (use Figma MCP + existing tokens)
- Creating components from Figma frames (use Figma MCP + component rules)
- Everyday development with Figma references

## Prerequisites

- Figma MCP connected
- RadTools installed (check for `devtools/` folder)
- Development environment (`NODE_ENV=development`)

## Critical Rule

**Never edit `app/globals.css` directly.** Use `POST /api/devtools/write-css` — this is RadTools' own persistence mechanism.

## Import Workflow

### Step 1: Extract from Figma

Use Figma MCP tools:

```
get_variable_defs(nodeId, fileKey) → colors, spacing variables
get_design_context(nodeId, fileKey) → component styles, typography
```

### Step 2: Transform to RadTools Data Structures

**Colors → BaseColor[]:**

```typescript
interface BaseColor {
  id: string;           // "primary" or "sun-yellow"
  name: string;         // CSS variable suffix: "primary" → --color-primary
  displayName: string;  // UI label: "Primary"
  value: string;        // "#3B82F6"
  category: 'brand' | 'neutral';
}
```

Map Figma variables to semantic names:
- `Brand/Primary` → `{ id: 'primary', name: 'primary', category: 'brand' }`
- `Surface/Background` → `{ id: 'surface', name: 'surface', category: 'brand' }`
- `Neutral/50` → `{ id: 'lightest', name: 'lightest', category: 'neutral' }`

**Typography → TypographyStyle[]:**

```typescript
interface TypographyStyle {
  id: string;
  element: string;        // "h1", "h2", "p", "code", etc.
  fontFamilyId: string;   // References FontDefinition.id
  fontSize: string;       // Tailwind class: "text-4xl"
  lineHeight?: string;    // Tailwind class: "leading-tight"
  fontWeight: string;     // Tailwind class: "font-bold"
  baseColorId: string;    // References BaseColor.id
  displayName: string;
  utilities?: string[];   // Additional classes: ["underline"]
}
```

Map Figma text styles:
- `Display/Large` → element: "h1"
- `Heading/Primary` → element: "h2"
- `Body/Regular` → element: "p"
- `Code/Mono` → element: "code"

**Fonts → FontDefinition[]:**

```typescript
interface FontDefinition {
  id: string;
  name: string;           // "Inter"
  family: string;         // CSS font-family value
  files: FontFile[];
  weights: number[];      // [400, 700]
  styles: string[];       // ["normal", "italic"]
}

interface FontFile {
  id: string;
  weight: number;
  style: string;
  format: 'woff2' | 'woff' | 'ttf' | 'otf';
  path: string;           // "/fonts/Inter-Regular.woff2"
}
```

### Step 3: Call RadTools API

**POST** to `/api/devtools/write-css`:

```typescript
await fetch('/api/devtools/write-css', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    baseColors: BaseColor[],      // Colors for @theme blocks
    borderRadius: {               // Border radius tokens
      sm: '0.25rem',
      md: '0.5rem',
      lg: '1rem'
    },
    fonts: FontDefinition[],      // Font definitions for @font-face
    typographyStyles: TypographyStyle[], // Typography for @layer base
    colorModes: ColorMode[]       // Optional dark mode overrides
  })
});
```

The API:
- Creates backup at `.globals.css.backup`
- Surgically updates only managed sections
- Preserves scrollbar, animations, custom CSS

### Step 4: Upload Assets

Save extracted assets to `public/assets/`:
- Icons: `public/assets/icons/`
- Images: `public/assets/images/`
- Logos: `public/assets/logos/`

### Step 5: Create Components

For component creation, use the **radtools-component-create** skill which covers:
- Default export requirements
- Default prop values (visual editor requirement)
- TypeScript props interface
- Preview file setup for visual editing

Quick reference — components must use imported tokens:
```tsx
// ✅ Uses tokens from @theme block
<button className="bg-sun-yellow text-black border-black rounded-md">

// ❌ Hardcoded colors
<button className="bg-[#FCE184] text-gray-900">
```

## Tailwind v4 Token Generation

RadTools uses Tailwind CSS v4's `@theme` block for automatic utility class generation:

```css
@theme {
  --color-{name}: {value};  /* → bg-{name}, text-{name}, border-{name} */
  --radius-{name}: {value}; /* → rounded-{name} */
  --shadow-{name}: {value}; /* → shadow-{name} */
}
```

**Example:** `--color-sun-yellow: #FCE184` automatically generates:
- `bg-sun-yellow`
- `text-sun-yellow`  
- `border-sun-yellow`

## Semantic Token Naming

Map Figma variables to meaningful token names. Tailwind v4 generates utilities from whatever names you choose:

| Figma Name | RadTools Token Name | Generated Classes |
|------------|---------------------|-------------------|
| Brand/Yellow | `sun-yellow` | `bg-sun-yellow`, `text-sun-yellow`, `border-sun-yellow` |
| Brand/Blue | `sky-blue` | `bg-sky-blue`, `text-sky-blue`, `border-sky-blue` |
| Surface/Background | `cream` or `warm-cloud` | `bg-cream`, `bg-warm-cloud` |
| Neutral/Dark | `black` | `bg-black`, `text-black`, `border-black` |
| Status/Error | `sun-red` | `bg-sun-red`, `text-sun-red` |

**Note:** Token names become both the CSS variable suffix (`--color-{name}`) and the generated utility classes. The `id` field is used for internal references (e.g., `baseColorId` in typography), while `name` determines the CSS output.

## Validation

After import:
1. Open RadTools (`Shift+Cmd+K`)
2. Check Variables tab for colors
3. Check Typography tab for text styles
4. Check Components tab for component discovery

RadTools reads from `globals.css` on mount and should reflect all API-written changes.

## Error Handling & Rollback

### If Import Fails

The write-css API creates a backup before writing. To rollback:

```bash
# Check for backup
ls -la app/.globals.css.backup

# Restore from backup
cp app/.globals.css.backup app/globals.css
```

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `403 Forbidden` | Not in development mode | Ensure `NODE_ENV=development` |
| `Invalid baseColors` | Malformed color data | Check all required fields: `id`, `name`, `displayName`, `value`, `category` |
| `Font file not found` | Missing font files | Upload fonts to `public/fonts/` before import |
| CSS not updating | Write succeeded but no visual change | Hard refresh browser, check DevTools console |

### Partial Import Recovery

If import partially succeeds (e.g., colors work but typography fails):

1. **Don't re-run full import** — this overwrites working data
2. **Fix the failing section** in the request payload
3. **Re-run with only the fixed section**:

```typescript
// Only update typography, keep existing colors
await fetch('/api/devtools/write-css', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    typographyStyles: [...],  // Only the fixed data
    // Omit baseColors, fonts, etc. to preserve existing
  })
});
```

**Note:** All fields are optional. The API only updates sections you provide:
- `baseColors` — updates `@theme` color variables
- `fonts` — updates `@font-face` declarations
- `typographyStyles` — updates `@layer base` element styles
- `borderRadius` — updates `@theme` radius variables
- `colorModes` — updates dark mode overrides

Typography can reference `fontFamilyId` values even if `fonts` array is omitted — existing font definitions are preserved.

### Font File Workflow

Before importing fonts, ensure files exist:

1. **Extract from Figma** using `get_design_context` to identify font families
2. **Obtain font files** (`.woff2` preferred):
   - Google Fonts: [google-webfonts-helper](https://gwfh.mranftl.com/fonts)
   - Licensed fonts: Export from font management tool
3. **Upload to `public/fonts/`**
4. **Then run import** with `FontDefinition[]` pointing to those paths

## Reference Files

See [references/data-structures.md](references/data-structures.md) for complete type definitions and examples.
