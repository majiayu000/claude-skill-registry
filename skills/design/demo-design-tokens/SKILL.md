---
name: demo-design-tokens
description: Default design tokens for demo applications. Use when building demos without a formal design system. Provides colors, typography, spacing, shadows, and transitions.
---

# Demo Design Tokens

## Overview
Pre-configured design tokens for graceful demo UI without a formal design system.

## Color System

### Brand Colors
```css
--brand-primary: #2563EB;    /* Blue-600 */
--brand-secondary: #1E40AF;  /* Blue-800 */
--brand-accent: #7C3AED;     /* Violet-600 */
```

### Neutral Colors
```css
--neutral-50: #F8FAFC;   /* Background */
--neutral-100: #F1F5F9;  /* Surface alt */
--neutral-200: #E2E8F0;  /* Border */
--neutral-300: #CBD5E1;  /* Border hover */
--neutral-500: #64748B;  /* Text secondary */
--neutral-700: #334155;  /* Text primary */
--neutral-900: #0F172A;  /* Text emphasis */
```

### Semantic Colors
```css
/* Status */
--success: #22C55E;      /* Green-500 */
--warning: #EAB308;      /* Yellow-500 */
--error: #EF4444;        /* Red-500 */
--info: #3B82F6;         /* Blue-500 */

/* Severity (for data visualization) */
--severity-critical: #DC2626;  /* Red-600 */
--severity-high: #F97316;      /* Orange-500 */
--severity-medium: #EAB308;    /* Yellow-500 */
--severity-low: #3B82F6;       /* Blue-500 */
--severity-info: #6B7280;      /* Gray-500 */

/* Condition */
--condition-excellent: #22C55E;  /* Green-500 */
--condition-good: #84CC16;       /* Lime-500 */
--condition-fair: #EAB308;       /* Yellow-500 */
--condition-poor: #F97316;       /* Orange-500 */
```

## Typography

### Font Stack
```css
--font-sans: 'Inter', system-ui, -apple-system, sans-serif;
--font-mono: 'JetBrains Mono', 'SF Mono', monospace;
```

### Type Scale
| Token | Size | Line Height | Weight | Use |
|-------|------|-------------|--------|-----|
| --text-xs | 12px | 16px | 400 | Labels, captions |
| --text-sm | 14px | 20px | 400 | Secondary text |
| --text-base | 16px | 24px | 400 | Body |
| --text-lg | 18px | 28px | 500 | Emphasis |
| --text-xl | 20px | 28px | 600 | Card titles |
| --text-2xl | 24px | 32px | 600 | Section headers |
| --text-3xl | 30px | 36px | 700 | Page titles |
| --text-4xl | 36px | 40px | 700 | Hero text |

## Spacing Scale

Based on 4px grid:

| Token | Value | Tailwind |
|-------|-------|----------|
| --space-1 | 4px | p-1 |
| --space-2 | 8px | p-2 |
| --space-3 | 12px | p-3 |
| --space-4 | 16px | p-4 |
| --space-5 | 20px | p-5 |
| --space-6 | 24px | p-6 |
| --space-8 | 32px | p-8 |
| --space-10 | 40px | p-10 |
| --space-12 | 48px | p-12 |

## Shadows

| Token | Value | Use |
|-------|-------|-----|
| --shadow-sm | 0 1px 2px rgba(0,0,0,0.05) | Subtle elevation |
| --shadow-md | 0 4px 6px rgba(0,0,0,0.1) | Cards |
| --shadow-lg | 0 10px 15px rgba(0,0,0,0.1) | Modals, dropdowns |
| --shadow-xl | 0 20px 25px rgba(0,0,0,0.15) | Popovers |

## Border Radius

| Token | Value | Use |
|-------|-------|-----|
| --radius-sm | 4px | Buttons, inputs |
| --radius-md | 8px | Cards |
| --radius-lg | 12px | Modals |
| --radius-xl | 16px | Large containers |
| --radius-full | 9999px | Pills, avatars |

## Transitions

| Token | Value | Use |
|-------|-------|-----|
| --duration-fast | 150ms | Micro-interactions |
| --duration-normal | 300ms | Default |
| --duration-slow | 500ms | Page transitions |
| --ease-out | cubic-bezier(0, 0, 0.2, 1) | Entrances |
| --ease-in-out | cubic-bezier(0.4, 0, 0.2, 1) | Transitions |

## Tailwind Config Extension

```typescript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        brand: {
          primary: '#2563EB',
          secondary: '#1E40AF',
          accent: '#7C3AED',
        },
        severity: {
          critical: '#DC2626',
          high: '#F97316',
          medium: '#EAB308',
          low: '#3B82F6',
          info: '#6B7280',
        },
        condition: {
          excellent: '#22C55E',
          good: '#84CC16',
          fair: '#EAB308',
          poor: '#F97316',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'SF Mono', 'monospace'],
      },
    },
  },
};
```

## Best Practices

- Use semantic tokens over raw values
- Maintain consistent spacing rhythm
- Pair shadows with border radius
- Test colors for WCAG contrast

## Anti-Patterns

- NO hardcoded hex values in components
- NO inconsistent spacing values
- NO mixing design systems
