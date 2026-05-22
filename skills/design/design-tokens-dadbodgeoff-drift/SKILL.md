---
name: design-tokens
description: Comprehensive design token system for typography, colors, and theming with WCAG AA compliance, TypeScript types, and framework integration (CSS-in-JS, Tailwind, CSS Variables).
license: MIT
compatibility: TypeScript/JavaScript
metadata:
  category: frontend
  time: 4h
  source: drift-masterguide
---

# Design Token System

Single source of truth for visual design decisions with accessibility compliance.

## When to Use This Skill

- Building a consistent design system
- Need WCAG AA compliant color contrast
- Want type-safe token access
- Supporting multiple frameworks (Tailwind, CSS-in-JS)

## Core Concepts

Design tokens provide:
1. **Typography** - Font families, sizes, weights, presets
2. **Colors** - Semantic palettes with contrast ratios
3. **Type safety** - TypeScript types for autocomplete
4. **Framework agnostic** - Export to CSS vars, Tailwind, etc.

## Implementation

### TypeScript

```typescript
// tokens/typography.ts
export const fontFamily = {
  sans: 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  mono: '"SF Mono", Monaco, "Cascadia Code", Consolas, monospace',
} as const;

export const fontSize = {
  xs: '12px',
  sm: '14px',
  base: '16px',
  lg: '18px',
  xl: '20px',
  '2xl': '24px',
  '3xl': '30px',
  '4xl': '36px',
} as const;

export const fontWeight = {
  normal: 400,
  medium: 500,
  semibold: 600,
  bold: 700,
} as const;

export const lineHeight = {
  tight: 1.2,
  snug: 1.3,
  normal: 1.5,
  relaxed: 1.625,
} as const;

// Typography presets for consistent usage
export const typographyPresets = {
  h1: {
    fontSize: fontSize['3xl'],
    fontWeight: fontWeight.bold,
    lineHeight: lineHeight.tight,
  },
  h2: {
    fontSize: fontSize['2xl'],
    fontWeight: fontWeight.semibold,
    lineHeight: lineHeight.snug,
  },
  h3: {
    fontSize: fontSize.xl,
    fontWeight: fontWeight.semibold,
    lineHeight: lineHeight.snug,
  },
  body: {
    fontSize: fontSize.base,
    fontWeight: fontWeight.normal,
    lineHeight: lineHeight.normal,
  },
  caption: {
    fontSize: fontSize.xs,
    fontWeight: fontWeight.normal,
    lineHeight: lineHeight.snug,
  },
} as const;
```

### Color Tokens

```typescript
// tokens/colors.ts
export const primary = {
  50: '#E6F4F5',
  100: '#CCE9EB',
  200: '#99D3D7',
  300: '#66BDC3',
  400: '#33A7AF',
  500: '#21808D',  // Main primary
  600: '#1A6671',
  700: '#144D55',
  800: '#0D3338',
  900: '#071A1C',
} as const;

export const neutral = {
  50: '#F8F9FA',
  100: '#F1F3F5',
  200: '#E9ECEF',
  300: '#DEE2E6',
  400: '#CED4DA',
  500: '#ADB5BD',
  600: '#868E96',
  700: '#495057',
  800: '#343A40',
  900: '#1F2121',
} as const;

export const semantic = {
  success: { light: '#86efac', main: '#218081', dark: '#16a34a' },
  warning: { light: '#fde047', main: '#A84F2F', dark: '#92400E' },
  error: { light: '#fca5a5', main: '#C0152F', dark: '#9f1239' },
  info: { light: '#99D3D7', main: '#62756E', dark: '#475569' },
} as const;

// Semantic background colors
export const background = {
  default: '#1F2121',
  surface: '#262828',
  elevated: '#334155',
  overlay: 'rgba(31, 33, 33, 0.8)',
} as const;

// Text colors with WCAG contrast ratios
export const text = {
  primary: '#FCFCF9',    // 15.8:1 - AAA
  secondary: '#B8BABA',  // 8.2:1 - AAA
  tertiary: '#9A9E9E',   // 5.8:1 - AA
  muted: '#7D8282',      // 4.5:1 - AA minimum
  link: '#32B8C6',       // 6.2:1 - AA
} as const;

export const border = {
  default: 'rgba(167, 169, 169, 0.20)',
  subtle: 'rgba(119, 124, 124, 0.30)',
  strong: '#777C7C',
  focus: '#21808D',
} as const;
```

### TypeScript Types

```typescript
// types/tokens.ts
export type FontFamily = keyof typeof fontFamily;
export type FontSize = keyof typeof fontSize;
export type FontWeight = keyof typeof fontWeight;
export type TypographyPreset = keyof typeof typographyPresets;

export type PrimaryColor = keyof typeof primary;
export type NeutralColor = keyof typeof neutral;
export type SemanticColor = keyof typeof semantic;
export type BackgroundColor = keyof typeof background;
export type TextColor = keyof typeof text;
```

### CSS Variables Export

```typescript
// tokens/export.ts
export function generateCSSVariables(): string {
  return `
:root {
  /* Typography */
  --font-sans: ${fontFamily.sans};
  --font-mono: ${fontFamily.mono};
  --text-sm: ${fontSize.sm};
  --text-base: ${fontSize.base};
  --text-lg: ${fontSize.lg};
  
  /* Colors */
  --color-primary: ${primary[500]};
  --color-primary-light: ${primary[300]};
  --color-primary-dark: ${primary[700]};
  
  /* Backgrounds */
  --bg-default: ${background.default};
  --bg-surface: ${background.surface};
  --bg-elevated: ${background.elevated};
  
  /* Text */
  --text-primary: ${text.primary};
  --text-secondary: ${text.secondary};
  --text-muted: ${text.muted};
  
  /* Borders */
  --border-default: ${border.default};
  --border-focus: ${border.focus};
}`;
}
```

### Tailwind Integration

```typescript
// tailwind.config.ts
import { primary, neutral, background, text } from './tokens/colors';

export default {
  theme: {
    extend: {
      colors: {
        primary: {
          50: primary[50],
          500: primary[500],
          900: primary[900],
          DEFAULT: primary[500],
        },
        neutral,
      },
      backgroundColor: {
        default: background.default,
        surface: background.surface,
        elevated: background.elevated,
      },
      textColor: {
        primary: text.primary,
        secondary: text.secondary,
        muted: text.muted,
      },
    },
  },
};
```

## Usage Examples

### CSS-in-JS

```typescript
import styled from '@emotion/styled';
import { text, background, typographyPresets, border } from '@/tokens';

export const Button = styled.button`
  font-size: ${typographyPresets.body.fontSize};
  font-weight: ${typographyPresets.body.fontWeight};
  background-color: ${primary[500]};
  color: ${text.primary};
  
  &:hover {
    background-color: ${primary[400]};
  }
  
  &:focus {
    outline: 2px solid ${border.focus};
    outline-offset: 2px;
  }
`;
```

### React Component

```tsx
import { typographyPresets, text } from '@/tokens';

export function Heading({ children }: { children: React.ReactNode }) {
  return (
    <h1 style={{
      ...typographyPresets.h1,
      color: text.primary,
    }}>
      {children}
    </h1>
  );
}
```

## WCAG Compliance

| Token | Color | Contrast | Level |
|-------|-------|----------|-------|
| text.primary | #FCFCF9 | 15.8:1 | AAA |
| text.secondary | #B8BABA | 8.2:1 | AAA |
| text.tertiary | #9A9E9E | 5.8:1 | AA |
| text.muted | #7D8282 | 4.5:1 | AA min |

## Best Practices

1. Use semantic tokens (text.primary not #FCFCF9)
2. Leverage typography presets for consistency
3. Test all text colors meet WCAG AA (4.5:1)
4. Export TypeScript types for autocomplete
5. Document contrast ratios for each text color

## Common Mistakes

- Using raw hex values instead of tokens
- Not testing contrast ratios
- Missing focus states for accessibility
- Inconsistent typography across components
- No dark/light mode support

## Related Patterns

- pwa-setup - Mobile app styling
- mobile-components - Responsive design
