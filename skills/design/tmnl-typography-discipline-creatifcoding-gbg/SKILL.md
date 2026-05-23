---
name: tmnl-typography-discipline
description: Typography rules and the 12px floor. Invoke when setting font sizes, creating text components, or debugging unreadable text. Enforces minimum readable sizes and proper token usage.
model_invoked: true
triggers:
  - "font size"
  - "typography"
  - "text size"
  - "12px floor"
  - "text-xs"
  - "readability"
  - "small text"
  - "microscopic text"
---

# TMNL Typography Discipline

## The Problem

There is a pathological tendency to make text microscopic in the name of "clean design" or "density." This creates inaccessible, unreadable interfaces that fail basic usability standards.

**This skill exists to prevent that.**

## The 12px Floor (CRITICAL)

**RULE**: Nothing goes below 12px in standard UI. Ever. Not labels, not badges, not "tiny" text.

**Exemptions** (must be explicitly justified):
- **AG-Grid ultra-density tier**: 8-10px for ops console/trading views (grid-specific)
- **Splash screen stylization**: VT323 font with CRT aesthetic (splash-specific)
- **Metadata timestamps**: 10-11px for non-critical secondary info (rare)

**Default to 12px or higher** unless you have a documented reason AND you're in an exempted context.

## Why This Matters

### The Broken Logic (Prime's Failure Modes)

| Broken Assumption | Reality |
|-------------------|---------|
| "Density is efficiency" | Unreadable text is zero efficiency |
| "Small text looks techy" | It looks like a vision test |
| "Minimalism" | Minimalism is clarity, not invisibility |
| "I can't see my output anyway" | Users CAN see it, and they're squinting |

### The Accessibility Reality

- **12px at arm's length on 1080p** - Minimum readable for most users
- **Below 12px** - Requires leaning in, excludes users with vision impairments
- **8-10px** - Only acceptable in high-density grids where scanning, not reading, is the primary task

## The Scale (Memorize This)

From `VANTA_TYPOGRAPHY.size` and `TMNL_FONT_SIZE`:

| Token | Size | Rem | Use Case | Floor? |
|-------|------|-----|----------|--------|
| `--tmnl-text-xs` / `xs` | **12px** | 0.75rem | Labels, badges, captions | **FLOOR** |
| `--tmnl-text-sm` / `sm` | **14px** | 0.875rem | Secondary text, small UI | Standard |
| `--tmnl-text-base` / `base` | **16px** | 1rem | Body text, inputs | Standard |
| `--tmnl-text-lg` / `lg` | **18px** | 1.125rem | Subheadings, emphasis | Standard |

**CSS Variable Pattern**:
```typescript
export const TMNL_FONT_SIZE = {
  xs: 'var(--tmnl-text-xs, 12px)',
  sm: 'var(--tmnl-text-sm, 14px)',
  base: 'var(--tmnl-text-base, 16px)',
  lg: 'var(--tmnl-text-lg, 18px)',
} as const
```

**Canonical source**: `src/lib/tmnl-ui/tokens.ts`

## Patterns

### Pattern 1: CSS Variables with Fallbacks

**ALWAYS** use CSS variables for font sizes.

```typescript
import { TMNL_FONT_SIZE } from '@/lib/tmnl-ui/tokens'

// CORRECT - CSS variable with fallback
<span style={{ fontSize: TMNL_FONT_SIZE.xs }}>Label</span>
// Renders: fontSize: 'var(--tmnl-text-xs, 12px)'

// CORRECT - inline with var()
<span style={{ fontSize: 'var(--tmnl-text-sm, 14px)' }}>Secondary</span>
```

**Canonical source**: `src/lib/tmnl-ui/primitives/Badge.tsx`

### Pattern 2: Typography Presets

Use preset styles from VANTA_TYPOGRAPHY for consistency.

```typescript
import { VANTA_TYPOGRAPHY } from '@/components/portal/tokens'

// Card title preset (12px, uppercase, tracked)
<h3 style={{ ...VANTA_TYPOGRAPHY.preset.cardTitle }}>
  SYSTEM STATUS
</h3>
// Applied styles:
// fontFamily: 'var(--font-heading), "Space Grotesk", sans-serif'
// fontSize: 'var(--tmnl-text-xs, 12px)' ← FLOOR
// fontWeight: '500'
// letterSpacing: '0.1em'
// textTransform: 'uppercase'

// Label preset (12px, mono, uppercase, tracked)
<span style={{ ...VANTA_TYPOGRAPHY.preset.label }}>
  STATUS
</span>
// Applied styles:
// fontFamily: 'var(--font-label), "Share Tech Mono", monospace'
// fontSize: 'var(--tmnl-text-xs, 12px)' ← FLOOR
// fontWeight: '500'
// letterSpacing: '0.15em'
// textTransform: 'uppercase'
```

**Canonical source**: `src/components/portal/tokens.ts`

### Pattern 3: Tailwind Classes (Standard Sizes Only)

When using Tailwind, use semantic classes, NOT arbitraries.

```typescript
// CORRECT - semantic class
<span className="text-xs font-mono">Label</span>
// Maps to: font-size: 0.75rem (12px)

// CORRECT - semantic class
<span className="text-sm">Secondary</span>
// Maps to: font-size: 0.875rem (14px)

// BANNED - arbitrary below floor
<span className="text-[8px]">Too small</span>
<span className="text-[10px]">Still too small</span>
```

### Pattern 4: AG-Grid Exemption (Ultra Density)

Grid-specific sub-12px sizes are ONLY allowed in grid contexts.

```typescript
// AG-Grid ultra tier (ops console, trading views)
export const DIMENSIONS = {
  rowHeightUltra: 16,      // Ultra-dense rows
  rowHeightDense: 20,      // Dense rows
  rowHeightNormal: 24,     // Default - FLOOR for standard UI
}

export const TYPOGRAPHY = {
  fontSizeXs: 12,          // Standard UI FLOOR
  fontSizeSm: 13,
  fontSizeMd: 14,
  // Grid exemptions
  fontSizeUltra: 8,        // Ultra-dense grid cells
  fontSizeDense: 10,       // Dense grid cells
}

// Usage (grid context ONLY)
const ultraTheme = tmnlDataGridTheme.withParams({
  rowHeight: DIMENSIONS.rowHeightUltra,
  fontSize: TYPOGRAPHY.fontSizeUltra, // 8px - EXEMPTED
})
```

**Canonical source**: `src/lib/data-grid/theme/tokens.ts`

**Documentation**:
```typescript
/**
 * GRID EXEMPTION: Sub-12px fonts are intentionally allowed for:
 * - ultra tier: 8px (max density ops console)
 * - dense tier: 9-10px (trading views)
 *
 * Standard UI should respect 12px floor per CLAUDE.md.
 */
```

### Pattern 5: Splash Screen Exemption (Stylization)

VT323 font renders larger than typical fonts, so nominal sizes differ.

```typescript
// Splash-specific typography (VT323 font)
export const SPLASH_TYPOGRAPHY = {
  fontFamily: "var(--font-splash), 'VT323', monospace",

  size: {
    xs: '0.875rem',   // 14px - VT323 renders larger
    sm: '1rem',       // 16px
    base: '1.125rem', // 18px
    lg: '1.5rem',     // 24px
    xl: '2rem',       // 32px
  },
}

// Note: 12px floor applies to standard UI, splash is intentionally stylized
```

**Canonical source**: `src/components/splash/tokens.ts`

### Pattern 6: Token-Driven Component Sizes

Components consume typography tokens, never hardcode sizes.

```typescript
import { TMNL_FONT_SIZE, TMNL_TOKENS } from '@/lib/tmnl-ui/tokens'

export function Badge({ children }: BadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center px-2 py-0.5',
        TMNL_TOKENS.typography.label, // Font family + tracking
      )}
      style={{ fontSize: TMNL_FONT_SIZE.xs }} // 12px FLOOR
    >
      {children}
    </span>
  )
}
```

**Canonical source**: `src/lib/tmnl-ui/primitives/Badge.tsx`

## Font Family Hierarchy

TMNL uses a multi-family system for typographic contrast.

### VANTA System (Brutalist Geo-primary)

```typescript
export const VANTA_TYPOGRAPHY = {
  family: {
    // Labels, technical text - monospace precision
    mono: 'var(--font-label), "Share Tech Mono", monospace',

    // Headings - neo-grotesque brutalist
    grotesk: 'var(--font-heading), "Space Grotesk", sans-serif',

    // Body text - Geo primary workhorse
    sans: 'var(--font-body), "Geo", sans-serif',

    // Data/stats - tabular clarity
    data: 'var(--font-stats), "Geo", sans-serif',
  },
}
```

### TMNL_TOKENS System (Monospace Stack)

```typescript
export const TMNL_TOKENS = {
  typography: {
    fontFamily: [
      'Geo',
      'ui-monospace',
      'SFMono-Regular',
      '"SF Mono"',
      'Menlo',
      'Consolas',
      'monospace',
    ],
    fontFamilyString: 'Geo, ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace',
    fontFamilyVar: 'var(--font-stats)', // CSS variable
  },
}
```

## When Tempted to Shrink

**Ask**: "Can a human read this at arm's length on a 1080p monitor?"

- **Yes, easily** - Size is acceptable
- **Yes, but squinting** - Too small, bump to 12px
- **Barely** - Way too small, bump to 14px
- **No** - Unacceptable, use 16px

**Ask**: "Is this in a grid exemption context?"

- **Yes** - Sub-12px MIGHT be acceptable (document why)
- **No** - Respect the 12px floor

**Ask**: "Am I defaulting to small because I think it looks 'clean'?"

- **Yes** - Stop. That's the broken logic. Use the scale.
- **No** - Good. Validate with the monitor test.

## Debugging Unreadable Text

When you see text that's too small:

1. **Grep for arbitrary sizes**: `grep -r "text-\[([0-9]+)px\]" src/`
2. **Check inline styles**: Look for `fontSize: '8px'`, `fontSize: '10px'`
3. **Validate token usage**: Ensure `TMNL_FONT_SIZE.xs` or `var(--tmnl-text-xs, 12px)`
4. **Check context**: Is this in a grid? Splash? Standard UI?
5. **Fix systematically**: Replace with tokens, not inline fixes

## Anti-Patterns (BANNED)

### Arbitrary Tailwind Sizes Below Floor

```typescript
// BANNED - bypasses design system, unreadable
<span className="text-[7px] font-mono">Label</span>
<span className="text-[8px] uppercase">ID</span>
<span className="text-[9px]">Timestamp</span>

// CORRECT - uses semantic class at floor
<span className="text-xs font-mono">Label</span>
// Maps to: 12px
```

### Hardcoded Sub-Floor Sizes

```typescript
// BANNED - hardcoded below floor
<span style={{ fontSize: '10px' }}>Metadata</span>

// CORRECT - token at floor
<span style={{ fontSize: TMNL_FONT_SIZE.xs }}>Metadata</span>
// Renders: var(--tmnl-text-xs, 12px)
```

### "Density" Justification Without Context

```typescript
// BANNED - no grid context, just "looks dense"
<div style={{ fontSize: '8px' }}>
  High-density information display
</div>

// CORRECT - grid context with documented exemption
// In AG-Grid ultra tier ONLY
const ultraTheme = tmnlDataGridTheme.withParams({
  fontSize: TYPOGRAPHY.fontSizeUltra, // 8px - EXEMPTED for ops console
})
```

### Mixing Arbitrary and Token Sizes

```typescript
// BANNED - inconsistent sizing strategy
<div>
  <span className="text-[11px]">Label</span>
  <span style={{ fontSize: TMNL_FONT_SIZE.xs }}>Value</span>
</div>

// CORRECT - token-driven throughout
<div>
  <span style={{ fontSize: TMNL_FONT_SIZE.xs }}>Label</span>
  <span style={{ fontSize: TMNL_FONT_SIZE.xs }}>Value</span>
</div>
```

### Omitting Fallbacks

```typescript
// BANNED - no fallback if CSS variable missing
<span style={{ fontSize: 'var(--tmnl-text-xs)' }}>Label</span>

// CORRECT - fallback ensures floor even if var missing
<span style={{ fontSize: 'var(--tmnl-text-xs, 12px)' }}>Label</span>
```

## Quick Reference

| Context | Min Size | Token | Justification Required? |
|---------|----------|-------|-------------------------|
| Standard UI | 12px | `TMNL_FONT_SIZE.xs` | No |
| AG-Grid ultra | 8px | `TYPOGRAPHY.fontSizeUltra` | Yes |
| AG-Grid dense | 10px | `TYPOGRAPHY.fontSizeDense` | Yes |
| Splash screen | 14px (VT323) | `SPLASH_TYPOGRAPHY.size.xs` | No (stylization) |
| Metadata (rare) | 10-11px | `VANTA_TYPOGRAPHY.size['2xs']` | Yes |

## Related Skills

- **tmnl-design-tokens** - Typography token definitions
- **tmnl-component-tiers** - Component-level typography usage
- **ag-grid-patterns** - Grid-specific typography exemptions
