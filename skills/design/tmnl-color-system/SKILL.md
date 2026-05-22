---
name: tmnl-color-system
description: TMNL color system architecture and surface hierarchy. Invoke when implementing color schemes, glow effects, status indicators, or debugging color inconsistencies. Defines the surface progression and accent palette.
model_invoked: true
triggers:
  - "color system"
  - "surface hierarchy"
  - "background colors"
  - "glow effect"
  - "status colors"
  - "accent colors"
  - "VANTA_COLORS"
  - "color tokens"
---

# TMNL Color System

## Overview

TMNL uses a **near-black surface hierarchy** with **restrained accent colors** and **glow effects**. The system is built on two principles:

1. **Surface Progression**: Darkest to lightest creates depth through micro-gradients
2. **Accent Restraint**: Color is used sparingly for status, emphasis, and interaction

**Key Principle**: Never use raw hex/RGB values. Always reference color tokens.

## Canonical Sources

### Color Token Sets

- **VANTA_COLORS**: `src/components/portal/tokens.ts` - Vantablack design system
- **TMNL_TOKENS.colors**: `src/components/tldraw/shapes/data-grid-theme.ts` - AG-Grid palette
- **Data Grid Tokens**: `src/lib/data-grid/theme/tokens.ts` - Grid-specific colors
- **Splash Tokens**: `src/components/splash/tokens.ts` - Splash screen palette
- **Animation Tokens**: `src/lib/animation/tokens.ts` - Reticle/trail colors

### Usage Examples

- **VantaCard**: `src/components/portal/VantaCard.tsx` - Surface hierarchy, glows
- **StatusIndicator**: `src/lib/tmnl-ui/primitives/Badge.tsx` - Status color mapping
- **AG-Grid Theme**: `src/components/tldraw/shapes/data-grid-theme.ts` - Grid cell colors

## Surface Hierarchy (VANTA_COLORS)

The Vantablack system uses a **progressive lightening scale** for depth perception.

```typescript
export const VANTA_COLORS = {
  surface: {
    void: '#000000',        // True vantablack - use sparingly
    base: '#030303',        // Primary card surface
    elevated: '#0a0a0a',    // Elevated surface (hover, focus)
    raised: '#111111',      // Subtle raised element
    border: '#1a1a1a',      // Border/separator tone
  },
}
```

**Usage Pattern**:
```typescript
// Card background
background: VANTA_COLORS.surface.base

// Hover state
background: VANTA_COLORS.surface.elevated

// Border
border: `1px solid ${VANTA_COLORS.surface.border}`
```

**Canonical source**: `src/components/portal/tokens.ts`

## Text Hierarchy (VANTA_COLORS)

Text colors follow a **contrast hierarchy** for readability.

```typescript
export const VANTA_COLORS = {
  text: {
    primary: '#e5e5e5',     // High contrast - headings, primary content
    secondary: '#a3a3a3',   // Muted - body text, labels
    tertiary: '#737373',    // Subtle - metadata, timestamps
    muted: '#525252',       // Disabled/placeholder
    inverse: '#000000',     // On light surfaces (rare)
  },
}
```

**Usage Pattern**:
```typescript
// Heading
color: VANTA_COLORS.text.primary

// Body text
color: VANTA_COLORS.text.secondary

// Timestamp
color: VANTA_COLORS.text.tertiary
```

## Accent Palette (Use Sparingly)

Accents are **high-saturation colors** used for status, emphasis, and interaction.

### Cyan (Primary Accent)

```typescript
export const VANTA_COLORS = {
  accent: {
    cyan: '#22d3ee',                        // Primary accent
    cyanMuted: '#0891b2',                   // Muted variant
    cyanGlow: 'rgba(34, 211, 238, 0.15)',  // Glow effect (15% opacity)
  },
}
```

**Use Cases**:
- Primary actions
- Active states
- Interactive elements
- Terminal aesthetics

### Emerald (Success/Active)

```typescript
export const VANTA_COLORS = {
  accent: {
    emerald: '#34d399',
    emeraldMuted: '#059669',
    emeraldGlow: 'rgba(52, 211, 153, 0.15)',
  },
}
```

**Use Cases**:
- Success states
- Active status indicators
- Positive metrics

### Amber (Warning/Pending)

```typescript
export const VANTA_COLORS = {
  accent: {
    amber: '#fbbf24',
    amberMuted: '#d97706',
    amberGlow: 'rgba(251, 191, 36, 0.15)',
  },
}
```

**Use Cases**:
- Warning states
- Pending status indicators
- Cautionary feedback

### Rose (Error/Danger)

```typescript
export const VANTA_COLORS = {
  accent: {
    rose: '#fb7185',
    roseMuted: '#e11d48',
    roseGlow: 'rgba(251, 113, 133, 0.15)',
  },
}
```

**Use Cases**:
- Error states
- Inactive/failed status
- Destructive actions

**Canonical source**: `src/components/portal/tokens.ts`

## Glow Effects

Glows are **subtle box-shadows** using low-opacity accent colors.

### Pattern: Status Indicator Glow

```typescript
const statusColors: Record<IndicatorStatus, { dot: string; text: string; glow: string }> = {
  active: {
    dot: VANTA_COLORS.accent.emerald,
    text: VANTA_COLORS.accent.emerald,
    glow: VANTA_COLORS.accent.emeraldGlow, // rgba(52, 211, 153, 0.15)
  },
  error: {
    dot: VANTA_COLORS.accent.rose,
    text: VANTA_COLORS.accent.rose,
    glow: VANTA_COLORS.accent.roseGlow,
  },
}

// Apply glow
<div
  style={{
    width: '6px',
    height: '6px',
    borderRadius: '50%',
    backgroundColor: statusColors[status].dot,
    boxShadow: `0 0 8px ${statusColors[status].glow}`,
  }}
/>
```

**Canonical source**: `src/components/portal/VantaCard.tsx`

### Pattern: Hover Glow

```typescript
const glowShadows = {
  cyan: VANTA_BORDERS.shadow.glowCyan,       // '0 0 14px rgba(34, 211, 238, 0.15)'
  emerald: VANTA_BORDERS.shadow.glowEmerald, // '0 0 20px rgba(52, 211, 153, 0.15)'
  amber: VANTA_BORDERS.shadow.glowAmber,
  rose: VANTA_BORDERS.shadow.glowRose,
}

// CSS hover state
<style>{`
  .vanta-card-glow:hover {
    box-shadow: ${variantTokens.boxShadow}, ${glowShadows[glowColor]};
    border-color: ${VANTA_COLORS.accent.cyanMuted};
  }
`}</style>
```

**Canonical source**: `src/components/portal/VantaCard.tsx`

## Gradient Definitions

TMNL uses **linear gradients** for subtle depth and texture.

```typescript
export const VANTA_COLORS = {
  gradient: {
    // Card surface gradient (top to bottom)
    surface: 'linear-gradient(180deg, #050505 0%, #000000 100%)',

    // Subtle depth gradient
    depth: 'linear-gradient(180deg, rgba(255,255,255,0.02) 0%, transparent 100%)',

    // Border glow gradient
    borderGlow: 'linear-gradient(180deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.02) 100%)',

    // Scanline overlay (CRT effect)
    scanlines: 'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.1) 2px, rgba(0,0,0,0.1) 4px)',
  },
}
```

**Usage Pattern**:
```typescript
// Card with gradient background
<div
  style={{
    background: VANTA_COLORS.gradient.surface,
    border: `1px solid ${VANTA_COLORS.surface.border}`,
  }}
>
  {/* Depth overlay */}
  <div
    style={{
      position: 'absolute',
      inset: 0,
      background: VANTA_COLORS.gradient.depth,
      pointerEvents: 'none',
    }}
  />

  {/* Content */}
  <div style={{ position: 'relative', zIndex: 1 }}>
    {children}
  </div>
</div>
```

**Canonical source**: `src/components/portal/VantaCard.tsx`

## Status Color Mapping

Map semantic states to accent colors for consistency.

### Pattern: AG-Grid Status Colors

```typescript
export const STATUS_COLORS = {
  active: TMNL_TOKENS.colors.accentGreen,   // #22c55e
  pending: TMNL_TOKENS.colors.accentYellow, // #eab308
  inactive: TMNL_TOKENS.colors.accentRed,   // #ef4444
  default: TMNL_TOKENS.colors.textMuted,    // #737373
} as const
```

**Canonical source**: `src/components/tldraw/shapes/data-grid-theme.ts`

### Pattern: VantaCard Indicator

```typescript
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
  inactive: {
    dot: VANTA_COLORS.text.muted,
    text: VANTA_COLORS.text.muted,
    glow: 'transparent',
  },
  error: {
    dot: VANTA_COLORS.accent.rose,
    text: VANTA_COLORS.accent.rose,
    glow: VANTA_COLORS.accent.roseGlow,
  },
}
```

**Canonical source**: `src/components/portal/VantaCard.tsx`

## Animation Color Tokens

Animation-specific colors for reticles, trails, and feedback.

```typescript
export const COLORS = {
  // Reticle colors
  reticle: {
    primary: '#00ff88',      // Bright green - primary ring
    secondary: '#44ffaa',    // Softer green - secondary ring
    tertiary: '#88ffcc',     // Pale green - tertiary ring
    glow: 'rgba(0, 255, 136, 0.4)', // Glow effect
  },

  // Momentum trail colors
  trail: {
    ghost: 'rgba(255, 255, 255, 0.15)',
    velocity: 'rgba(0, 255, 136, 0.3)', // Speed-based tint
  },

  // Snap feedback colors
  snap: {
    indicator: '#00a2ff',    // Cyan snap line
    ripple: 'rgba(0, 162, 255, 0.5)',
    particle: '#ffffff',
  },
} as const
```

**Canonical source**: `src/lib/animation/tokens.ts`

## Patterns

### Pattern 1: Card with Surface Hierarchy

```typescript
import { VANTA_COLORS, VANTA_CARD_VARIANTS } from '@/components/portal/tokens'

function MyCard({ variant = 'default' }: CardProps) {
  const variantTokens = VANTA_CARD_VARIANTS[variant]

  return (
    <div
      style={{
        background: variantTokens.background,      // gradient.surface
        border: variantTokens.border,              // subtle border
        borderRadius: variantTokens.borderRadius,  // minimal radius
        boxShadow: variantTokens.boxShadow,        // card elevation
      }}
    >
      {/* Depth overlay */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: VANTA_COLORS.gradient.depth,
          pointerEvents: 'none',
        }}
      />

      {/* Content */}
      <div style={{ position: 'relative', zIndex: 1 }}>
        {children}
      </div>
    </div>
  )
}
```

### Pattern 2: Status Indicator with Glow

```typescript
import { VANTA_COLORS } from '@/components/portal/tokens'

function StatusIndicator({ status }: { status: 'active' | 'error' }) {
  const colors = {
    active: {
      dot: VANTA_COLORS.accent.emerald,
      glow: VANTA_COLORS.accent.emeraldGlow,
    },
    error: {
      dot: VANTA_COLORS.accent.rose,
      glow: VANTA_COLORS.accent.roseGlow,
    },
  }

  return (
    <div
      style={{
        width: '6px',
        height: '6px',
        borderRadius: '50%',
        backgroundColor: colors[status].dot,
        boxShadow: `0 0 8px ${colors[status].glow}`,
      }}
    />
  )
}
```

### Pattern 3: Hover State with Glow

```typescript
import { VANTA_COLORS, VANTA_BORDERS } from '@/components/portal/tokens'

function InteractiveCard({ glowColor = 'cyan' }: CardProps) {
  const glowShadows = {
    cyan: VANTA_BORDERS.shadow.glowCyan,
    emerald: VANTA_BORDERS.shadow.glowEmerald,
  }

  return (
    <div className="interactive-card">
      <style>{`
        .interactive-card {
          transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
        }
        .interactive-card:hover {
          box-shadow: ${VANTA_BORDERS.shadow.card}, ${glowShadows[glowColor]};
          border-color: ${VANTA_COLORS.accent.cyanMuted};
        }
      `}</style>
    </div>
  )
}
```

### Pattern 4: Text Hierarchy in Components

```typescript
import { VANTA_COLORS } from '@/components/portal/tokens'

function Card() {
  return (
    <div>
      {/* Primary text - headings */}
      <h3 style={{ color: VANTA_COLORS.text.primary }}>
        SYSTEM STATUS
      </h3>

      {/* Secondary text - body */}
      <p style={{ color: VANTA_COLORS.text.secondary }}>
        All systems operational
      </p>

      {/* Tertiary text - metadata */}
      <span style={{ color: VANTA_COLORS.text.tertiary }}>
        Last updated 2 minutes ago
      </span>
    </div>
  )
}
```

## Anti-Patterns (BANNED)

### Hardcoded Hex Colors

```typescript
// BANNED - bypasses token system
<div style={{ background: '#0a0a0a', color: '#ffffff' }} />

// CORRECT - uses surface hierarchy
<div style={{
  background: VANTA_COLORS.surface.elevated,
  color: VANTA_COLORS.text.primary
}} />
```

### Inline RGB/RGBA

```typescript
// BANNED - hardcoded glow color
boxShadow: '0 0 8px rgba(34, 211, 238, 0.15)'

// CORRECT - token reference
boxShadow: `0 0 8px ${VANTA_COLORS.accent.cyanGlow}`
```

### Arbitrary Glow Opacities

```typescript
// BANNED - arbitrary opacity, inconsistent
boxShadow: `0 0 10px rgba(52, 211, 153, 0.3)` // Not 0.15

// CORRECT - uses token opacity (0.15)
boxShadow: `0 0 8px ${VANTA_COLORS.accent.emeraldGlow}`
```

### Mixing Color Systems

```typescript
// BANNED - mixing VANTA and TMNL colors inconsistently
<div style={{
  background: VANTA_COLORS.surface.base,
  color: TMNL_TOKENS.colors.textPrimary, // Different system
}} />

// CORRECT - consistent token set
<div style={{
  background: VANTA_COLORS.surface.base,
  color: VANTA_COLORS.text.primary,
}} />
```

### Overusing Accent Colors

```typescript
// BANNED - accent color for non-status elements
<div style={{ color: VANTA_COLORS.accent.cyan }}>
  Regular body text
</div>

// CORRECT - accent only for status/emphasis
<div style={{ color: VANTA_COLORS.text.secondary }}>
  Regular body text
</div>
<StatusIndicator status="active" /> {/* Accent here */}
```

## Related Skills

- **tmnl-design-tokens** - Token hierarchy and extension patterns
- **tmnl-typography-discipline** - Text color token usage
- **tmnl-animation-tokens** - Animation-specific color tokens
- **ag-grid-patterns** - Grid cell color patterns
