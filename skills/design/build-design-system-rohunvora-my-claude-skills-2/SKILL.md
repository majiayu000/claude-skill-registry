---
name: build-design-system
description: Build a design system from scratch using the Design Graph methodology. Use when starting a component library, creating design tokens, establishing typography scales, or structuring a theme. Based on Brent Jackson's (jxnblk) constraint-based systems.
---

# Build a Design System

Based on the **Design Graph** methodology by Brent Jackson and mathematical typography principles.

## When This Activates

- "Create a design system"
- "Set up design tokens"
- "Build a component library"
- "Create a theme"
- "Establish a type scale"
- "Structure my styles"

## The Design Graph

A constraint-based system with **4 interconnected nodes**:

```
SCALES ──────► COMPONENTS
   │                │
   │                │
   ▼                ▼
THEMES ◄────── VARIANTS
```

### 1. Scales

Raw design values mapped to specific properties.

```typescript
const scales = {
  colors: {
    primary: '#0066cc',
    secondary: '#666',
    background: '#fff',
    text: '#1a1a1a',
    muted: '#f5f5f5',
  },

  // Powers of 2 spacing (base 4 or 8)
  space: [0, 4, 8, 16, 32, 64, 128],

  // Mathematical type scale (1.25 ratio)
  fontSizes: [12, 14, 16, 20, 24, 32, 48],

  // Limited font weights
  fontWeights: {
    normal: 400,
    medium: 500,
    bold: 700,
  },

  // Consistent radii
  radii: [0, 2, 4, 8, 16, 9999],
}
```

**Rules:**
- Use powers of 2 for spacing: 4, 8, 16, 32, 64
- Limit to 6-7 values per scale (matches heading levels)
- Name semantically where possible (primary, muted)

### 2. Components

UI elements constrained by scales.

```typescript
const Button = {
  // Base styles (always applied)
  padding: scales.space[2], // 8px
  fontSize: scales.fontSizes[2], // 16px
  fontWeight: scales.fontWeights.medium,
  borderRadius: scales.radii[2], // 4px

  // Only use values from scales - never magic numbers
}
```

**Rules:**
- Components ONLY reference scale values
- No magic numbers (no `padding: 13px`)
- Base styles define the default state

### 3. Variants

Partial styles for contextual changes.

```typescript
const variants = {
  buttons: {
    primary: {
      bg: 'primary',
      color: 'white',
    },
    secondary: {
      bg: 'transparent',
      color: 'primary',
      border: '1px solid',
      borderColor: 'primary',
    },
    ghost: {
      bg: 'transparent',
      color: 'text',
    },
  },

  text: {
    heading: {
      fontWeight: 'bold',
      lineHeight: 1.25,
    },
    body: {
      fontWeight: 'normal',
      lineHeight: 1.5,
    },
    caption: {
      fontSize: 0, // scales.fontSizes[0]
      color: 'muted',
    },
  },
}
```

**Rules:**
- Variants are additive (applied on top of base)
- Name by purpose, not appearance (primary, not blue)
- Keep variants minimal (3-5 per component)

### 4. Themes

Collections of scales that define visual language.

```typescript
const lightTheme = {
  colors: {
    text: '#1a1a1a',
    background: '#ffffff',
    primary: '#0066cc',
    muted: '#f5f5f5',
  },
}

const darkTheme = {
  colors: {
    text: '#f5f5f5',
    background: '#1a1a1a',
    primary: '#66b3ff',
    muted: '#333333',
  },
}
```

**Rules:**
- Themes swap scales, not components
- Same keys, different values
- Components automatically adapt

## Mathematical Typography

Use **powers of 2** for a mathematically coherent system:

```
BASE: 16px (2⁴) = 1rem

TYPE SCALE (1.25 ratio):
- xs:   12px  (0.75rem)
- sm:   14px  (0.875rem)
- base: 16px  (1rem)
- lg:   20px  (1.25rem)
- xl:   24px  (1.5rem)
- 2xl:  32px  (2rem)
- 3xl:  48px  (3rem)

SPACING (powers of 2):
- 4px  (0.25rem)
- 8px  (0.5rem)
- 16px (1rem)
- 32px (2rem)
- 64px (4rem)

LINE HEIGHT:
- Headings: 1.25
- Body: 1.5
- Tight: 1.125
```

**Why powers of 2:**
- Digital displays are binary
- Common screen sizes divisible by 16
- Halving/doubling always yields integers
- Creates subtle mathematical relationships

## Output Format

When building a design system, output:

```
DESIGN SYSTEM SPEC

SCALES:
  colors: [list with hex values]
  space: [array in px]
  fontSizes: [array in px]
  fontWeights: [object]
  radii: [array in px]

COMPONENTS:
  [ComponentName]:
    base: [styles referencing scales]
    variants: [list]

THEMES:
  light: [scale overrides]
  dark: [scale overrides]

IMPLEMENTATION:
  [Code for theme provider, tokens, or CSS variables]
```

## Quick Start Template

```typescript
// theme.ts
export const theme = {
  colors: {
    text: '#1a1a1a',
    background: '#ffffff',
    primary: '#0066cc',
    secondary: '#666666',
    muted: '#f5f5f5',
    border: '#e5e5e5',
  },
  space: [0, 4, 8, 16, 32, 64],
  fontSizes: [12, 14, 16, 20, 24, 32],
  fontWeights: { normal: 400, medium: 500, bold: 700 },
  lineHeights: { tight: 1.25, normal: 1.5 },
  radii: [0, 4, 8, 16, 9999],
}
```

## Anti-Patterns

| Bad | Good |
|-----|------|
| `padding: 13px` | `padding: space[3]` (16px) |
| 20+ font sizes | 6-7 font sizes max |
| Colors by name (`blue`) | Colors by purpose (`primary`) |
| Styles in components | Styles from theme |
| Per-component theming | Global theme swap |

## References

- [Design Graph](https://jxnblk.com/blog/design-graph/) - Brent Jackson
- [Mathematical Web Typography](https://jxnblk.com/blog/mathematical-web-typography/) - Brent Jackson
- [Two Steps Forward](https://jxnblk.com/blog/two-steps-forward/) - CSS methodology evolution
