---
name: tmnl-design-tokens
description: TMNL design token system architecture. Invoke when implementing token-based theming, extending token hierarchies, or integrating CSS variables. Provides canonical token locations and extension patterns.
model_invoked: true
triggers:
  - "TMNL_TOKENS"
  - "VANTA_COLORS"
  - "VANTA_TYPOGRAPHY"
  - "design tokens"
  - "token hierarchy"
  - "CSS variables"
  - "theme tokens"
---

# TMNL Design Tokens

## Overview

TMNL uses a multi-layered token system where specialized token sets (VANTA, AG-Grid, Animation) all derive from or coexist with the base TMNL_TOKENS. Tokens are parameterized TypeScript constants exported as `const` objects, enabling both type safety and runtime access.

**Key Principle**: Tokens are the single source of truth for all visual properties. Components should NEVER hardcode colors, sizes, or timing values.

## Canonical Sources

### Base Token Sets

- **AG-Grid Tokens**: `src/components/tldraw/shapes/data-grid-theme.ts`
- **Data Grid Tokens**: `src/lib/data-grid/theme/tokens.ts`
- **Vanta Design System**: `src/components/portal/tokens.ts`
- **Animation Tokens**: `src/lib/animation/tokens.ts`
- **Splash Tokens**: `src/components/splash/tokens.ts`
- **TMNL UI Tokens**: `src/lib/tmnl-ui/tokens.ts`

### Token Usage Examples

- **VantaCard**: `src/components/portal/VantaCard.tsx`
- **Badge Component**: `src/lib/tmnl-ui/primitives/Badge.tsx`
- **AG-Grid Theme**: `src/components/tldraw/shapes/data-grid-theme.ts`

## Token Hierarchy

### 1. TMNL_TOKENS (Base System)

The canonical base token set for AG-Grid and data-centric UI.

```typescript
export const TMNL_TOKENS = {
  // Color palette
  colors: {
    // Backgrounds (darkest to lightest)
    black: '#000000',
    backgroundPrimary: '#0a0a0a',
    backgroundSecondary: '#0d0d0d',
    backgroundTertiary: '#141414',
    backgroundHover: '#1a1a1a',
    backgroundSelected: '#1e1e21',

    // Borders (progressive lightening)
    borderMuted: '#1a1a1a',
    borderDefault: '#262626',
    borderSubtle: '#333333',

    // Text hierarchy
    textPrimary: '#ffffff',
    textSecondary: '#a3a3a3',
    textMuted: '#737373',
    textDisabled: '#525252',

    // Accents
    accentPrimary: '#ffffff',
    accentCyan: '#00A2FF',
    accentGreen: '#22c55e',
    accentYellow: '#eab308',
    accentRed: '#ef4444',
  },

  // Typography
  typography: {
    fontFamily: ['Geo', 'ui-monospace', 'SFMono-Regular', 'monospace'],
    fontFamilyString: 'Geo, ui-monospace, SFMono-Regular, monospace',
    fontFamilyVar: 'var(--font-stats)', // CSS variable reference
    fontSizeXs: 12,  // FLOOR - never go below
    fontSizeSm: 13,
    fontSizeMd: 14,
    fontSizeLg: 16,
  },

  // Spacing (4px unit grid)
  spacing: {
    unit: 4,
    cellPadding: 0.7,
    rowPadding: 0.9,
    headerPadding: 1.0,
  },

  // Dimensions
  dimensions: {
    rowHeight: 24,
    headerHeight: 28,
    borderRadius: 0,
    borderWidth: 1,
    iconSize: 12,
  },

  // Animation
  animation: {
    durationFast: 0.1,
    durationNormal: 0.2,
    durationSlow: 0.3,
    easing: 'cubic-bezier(0.4, 0, 0.2, 1)',
  },
} as const
```

**Canonical source**: `src/components/tldraw/shapes/data-grid-theme.ts`

### 2. VANTA_COLORS (Vantablack Design System)

Near-black surface hierarchy with accent palette.

```typescript
export const VANTA_COLORS = {
  // Surface hierarchy (darkest to lightest)
  surface: {
    void: '#000000',        // True vantablack - use sparingly
    base: '#030303',        // Primary card surface
    elevated: '#0a0a0a',    // Elevated surface (hover, focus)
    raised: '#111111',      // Subtle raised element
    border: '#1a1a1a',      // Border/separator tone
  },

  // Text hierarchy
  text: {
    primary: '#e5e5e5',     // High contrast
    secondary: '#a3a3a3',   // Muted
    tertiary: '#737373',    // Subtle
    muted: '#525252',       // Disabled/placeholder
    inverse: '#000000',     // On light surfaces
  },

  // Accent palette (use sparingly)
  accent: {
    cyan: '#22d3ee',
    cyanMuted: '#0891b2',
    cyanGlow: 'rgba(34, 211, 238, 0.15)',

    emerald: '#34d399',
    emeraldMuted: '#059669',
    emeraldGlow: 'rgba(52, 211, 153, 0.15)',

    amber: '#fbbf24',
    amberMuted: '#d97706',
    amberGlow: 'rgba(251, 191, 36, 0.15)',

    rose: '#fb7185',
    roseMuted: '#e11d48',
    roseGlow: 'rgba(251, 113, 133, 0.15)',
  },

  // Gradient definitions
  gradient: {
    surface: 'linear-gradient(180deg, #050505 0%, #000000 100%)',
    depth: 'linear-gradient(180deg, rgba(255,255,255,0.02) 0%, transparent 100%)',
    borderGlow: 'linear-gradient(180deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.02) 100%)',
    scanlines: 'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.1) 2px, rgba(0,0,0,0.1) 4px)',
  },
} as const
```

**Canonical source**: `src/components/portal/tokens.ts`

### 3. VANTA_TYPOGRAPHY (Font Hierarchy)

Brutalist Geo-primary system with tactical monospace.

```typescript
export const VANTA_TYPOGRAPHY = {
  // Font families
  family: {
    mono: 'var(--font-label), "Share Tech Mono", monospace',    // Labels, technical
    grotesk: 'var(--font-heading), "Space Grotesk", sans-serif', // Headings
    sans: 'var(--font-body), "Geo", sans-serif',                // Body text
    data: 'var(--font-stats), "Geo", sans-serif',               // Tabular data
  },

  // Font sizes (rem-based for accessibility)
  size: {
    '2xs': '0.625rem',  // 10px - Micro text, metadata
    xs: '0.6875rem',    // 11px - Labels, hints
    sm: '0.75rem',      // 12px - Secondary text (FLOOR for standard UI)
    base: '0.8125rem',  // 13px - Body text
    md: '0.875rem',     // 14px - Emphasized body
    lg: '1rem',         // 16px - Subheadings
    xl: '1.125rem',     // 18px - Headings
    '2xl': '1.25rem',   // 20px - Display headings
    '3xl': '1.5rem',    // 24px - Hero text
  },

  // Preset text styles
  preset: {
    cardTitle: {
      fontFamily: 'var(--font-heading), "Space Grotesk", sans-serif',
      fontSize: 'var(--tmnl-text-xs, 12px)', // 12px - FLOOR
      fontWeight: '500',
      letterSpacing: '0.1em',
      lineHeight: '1.25',
      textTransform: 'uppercase' as const,
    },
    label: {
      fontFamily: 'var(--font-label), "Share Tech Mono", monospace',
      fontSize: 'var(--tmnl-text-xs, 12px)', // 12px - FLOOR
      fontWeight: '500',
      letterSpacing: '0.15em',
      lineHeight: '1',
      textTransform: 'uppercase' as const,
    },
    value: {
      fontFamily: 'var(--font-stats), "Geo", sans-serif',
      fontSize: 'var(--tmnl-text-sm, 14px)',
      fontWeight: '600',
      letterSpacing: '0.025em',
      lineHeight: '1.25',
    },
  },
} as const
```

**Canonical source**: `src/components/portal/tokens.ts`

### 4. Animation Tokens

Timing, easing, and geometry for animation systems.

```typescript
export const TIMING = {
  emanation: {
    primary: { start: 0, duration: 15 },
    secondary: { start: 15, duration: 20 },
    tertiary: { start: 35, duration: 15 },
    total: 50,
  },
  reticle: {
    expandDuration: 80,
    pulsePeriod: 800,
    collapseDuration: 120,
  },
} as const

export const EASING = {
  gsap: {
    emanationOut: 'power2.out',
    reticleExpand: 'back.out(1.7)',
    snapBounce: 'elastic.out(1, 0.3)',
  },
  css: {
    emanationOut: 'cubic-bezier(0.22, 1, 0.36, 1)',
    snapBounce: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
  },
} as const
```

**Canonical source**: `src/lib/animation/tokens.ts`

## Patterns

### Pattern 1: Consuming Tokens (Inline Styles)

Use tokens via inline styles when CSS classes aren't sufficient.

```typescript
import { VANTA_COLORS, VANTA_TYPOGRAPHY, VANTA_SPACING } from '@/components/portal/tokens'

function MyCard() {
  return (
    <div
      style={{
        background: VANTA_COLORS.gradient.surface,
        border: `1px solid ${VANTA_COLORS.surface.border}`,
        padding: VANTA_SPACING['4'],
      }}
    >
      <h3
        style={{
          color: VANTA_COLORS.text.primary,
          ...VANTA_TYPOGRAPHY.preset.cardTitle,
        }}
      >
        SYSTEM STATUS
      </h3>
    </div>
  )
}
```

**Canonical source**: `src/components/portal/VantaCard.tsx`

### Pattern 2: CSS Variable Integration

Tokens reference CSS variables for ScaleProvider integration.

```typescript
import { TMNL_FONT_SIZE } from '@/lib/tmnl-ui/tokens'

// CSS variable with fallback
export const TMNL_FONT_SIZE = {
  xs: 'var(--tmnl-text-xs, 12px)',
  sm: 'var(--tmnl-text-sm, 14px)',
  base: 'var(--tmnl-text-base, 16px)',
  lg: 'var(--tmnl-text-lg, 18px)',
} as const

// Usage
<span style={{ fontSize: TMNL_FONT_SIZE.xs }}>Label</span>
```

**Canonical source**: `src/lib/tmnl-ui/tokens.ts`

### Pattern 3: Extending Token Sets

Create domain-specific tokens that extend base tokens.

```typescript
import { TMNL_TOKENS } from '@/components/tldraw/shapes/data-grid-theme'

// STATUS_COLORS extends base palette
export const STATUS_COLORS = {
  active: TMNL_TOKENS.colors.accentGreen,
  pending: TMNL_TOKENS.colors.accentYellow,
  inactive: TMNL_TOKENS.colors.accentRed,
  default: TMNL_TOKENS.colors.textMuted,
} as const

// FLASH_COLORS adds animation-specific alpha
export const FLASH_COLORS = {
  up: 'rgba(34, 197, 94, 0.4)',
  down: 'rgba(239, 68, 68, 0.4)',
  change: 'rgba(255, 255, 255, 0.2)',
} as const
```

**Canonical source**: `src/components/tldraw/shapes/data-grid-theme.ts`

### Pattern 4: Compound Token Sets

Pre-composed variants for common use cases.

```typescript
import { VANTA_COLORS, VANTA_BORDERS, VANTA_SPACING } from './tokens'

export const VANTA_CARD_VARIANTS = {
  default: {
    background: VANTA_COLORS.gradient.surface,
    border: VANTA_BORDERS.style.subtle,
    borderRadius: VANTA_BORDERS.radius.sm,
    boxShadow: VANTA_BORDERS.shadow.card,
    padding: VANTA_SPACING.card.padding,
  },
  elevated: {
    background: VANTA_COLORS.gradient.surface,
    border: VANTA_BORDERS.style.default,
    borderRadius: VANTA_BORDERS.radius.md,
    boxShadow: VANTA_BORDERS.shadow.elevated,
    padding: VANTA_SPACING.card.padding,
  },
} as const

// Usage
const variantTokens = VANTA_CARD_VARIANTS[variant]
```

**Canonical source**: `src/components/portal/tokens.ts`

### Pattern 5: Runtime Theme Variation

Generate theme variants at runtime using token overrides.

```typescript
import { TMNL_TOKENS } from '@/components/tldraw/shapes/data-grid-theme'
import { themeQuartz } from 'ag-grid-community'

export function createAnimatedTheme(overrides: Partial<typeof TMNL_TOKENS.colors>) {
  const mergedColors = { ...TMNL_TOKENS.colors, ...overrides }

  return themeQuartz.withParams({
    backgroundColor: mergedColors.backgroundPrimary,
    foregroundColor: mergedColors.textPrimary,
    accentColor: mergedColors.accentPrimary,
    // ... other params
  })
}

// Usage
const pulseTheme = createAnimatedTheme({
  backgroundPrimary: '#1a0a0a', // Warmer background
  accentPrimary: '#ff6600',     // Orange accent
})
```

**Canonical source**: `src/components/tldraw/shapes/data-grid-theme.ts`

### Pattern 6: Token-Driven Status Colors

Map status states to token colors for consistency.

```typescript
import { VANTA_COLORS } from '@/components/portal/tokens'

type IndicatorStatus = 'active' | 'pending' | 'inactive' | 'idle' | 'error'

const statusColors: Record<IndicatorStatus, { dot: string; text: string; glow: string }> = {
  active: {
    dot: VANTA_COLORS.accent.emerald,
    text: VANTA_COLORS.accent.emerald,
    glow: VANTA_COLORS.accent.emeraldGlow,
  },
  pending: {
    dot: VANTA_COLORS.accent.amber,
    text: VANTA_COLORS.accent.amber,
    glow: VANTA_COLORS.accent.amberGlow,
  },
  error: {
    dot: VANTA_COLORS.accent.rose,
    text: VANTA_COLORS.accent.rose,
    glow: VANTA_COLORS.accent.roseGlow,
  },
}
```

**Canonical source**: `src/components/portal/VantaCard.tsx`

## Token Extension Protocol

When adding new tokens:

1. **Choose the right token set** - Base TMNL_TOKENS, VANTA, or domain-specific
2. **Follow naming conventions** - `backgroundPrimary`, `textSecondary`, `accentCyan`
3. **Export as const** - `export const TOKENS = { ... } as const`
4. **Document usage** - Add JSDoc comments for non-obvious tokens
5. **Update this skill** - Add pattern with canonical source reference

## Anti-Patterns (BANNED)

### Hardcoded Colors

```typescript
// BANNED - bypasses token system
<div style={{ color: '#ffffff', background: '#0a0a0a' }} />

// CORRECT - uses tokens
<div style={{ color: VANTA_COLORS.text.primary, background: VANTA_COLORS.surface.base }} />
```

### Magic Numbers

```typescript
// BANNED - unexplained spacing value
<div style={{ padding: '16px' }} />

// CORRECT - semantic token
<div style={{ padding: VANTA_SPACING.card.padding }} />
```

### Inline RGB/Hex

```typescript
// BANNED - inline color definitions
boxShadow: '0 0 8px rgba(34, 211, 238, 0.15)'

// CORRECT - token reference
boxShadow: `0 0 8px ${VANTA_COLORS.accent.cyanGlow}`
```

### Duplicated Token Definitions

```typescript
// BANNED - redefining existing tokens
const MY_COLORS = {
  cyan: '#22d3ee', // Already in VANTA_COLORS.accent.cyan
}

// CORRECT - import and extend
import { VANTA_COLORS } from '@/components/portal/tokens'
const MY_COLORS = {
  specialCyan: VANTA_COLORS.accent.cyan,
}
```

## Related Skills

- **tmnl-typography-discipline** - Typography token usage and the 12px floor
- **tmnl-color-system** - Color token hierarchy and glow effects
- **tmnl-animation-tokens** - Animation timing and easing tokens
- **ag-grid-patterns** - AG-Grid theme integration with TMNL_TOKENS
