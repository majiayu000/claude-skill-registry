---
name: color-system
description: Master color design with color theory, accessibility, theming, and dark mode. Create harmonious color systems that work across contexts, support accessibility standards, and enable flexible theming. Includes color psychology, contrast ratios, and color-blind friendly palettes.
---

# Color System

## Overview

Color is one of the most powerful tools in design. It communicates emotion, establishes brand identity, guides attention, and conveys meaning. Yet color is also one of the most misused design elements.

This skill teaches you to think about color systematically: choosing colors with intention, ensuring accessibility, supporting theming and dark mode, and using color to guide users without overwhelming them.

## Core Methodology: Color Harmony

Rather than choosing colors randomly, use color theory to create harmonious palettes that feel intentional and professional.

### Color Harmony Techniques

**1. Monochromatic**
Use different tints, shades, and tones of a single hue.

```
Primary: #3B82F6
Tints (lighter): #93C5FD, #DBEAFE, #EFF6FF
Shades (darker): #1D4ED8, #1E40AF, #0C2340
```

**Use Case:** Minimalist, sophisticated designs. Good for focusing attention.

**2. Analogous**
Use colors that are adjacent on the color wheel (30-60 degrees apart).

```
Primary: #3B82F6 (blue)
Secondary: #8B5CF6 (purple) - 60° away
Tertiary: #06B6D4 (cyan) - 60° away
```

**Use Case:** Harmonious, pleasing designs. Good for creating unity.

**3. Complementary**
Use colors that are opposite on the color wheel (180 degrees apart).

```
Primary: #3B82F6 (blue)
Complementary: #F59E0B (amber)
```

**Use Case:** High contrast, energetic designs. Use sparingly to avoid visual chaos.

**4. Triadic**
Use three colors evenly spaced on the color wheel (120 degrees apart).

```
Primary: #3B82F6 (blue)
Secondary: #F59E0B (amber)
Tertiary: #10B981 (green)
```

**Use Case:** Vibrant, balanced designs. Good for applications with multiple categories.

### Choosing Your Primary Color

Your primary color is the foundation of your color system. Choose it based on:

1. **Brand Identity** — What emotion do you want to convey?
2. **Accessibility** — Does it have good contrast with white and black?
3. **Versatility** — Does it work well with other colors?
4. **Distinctiveness** — Is it unique enough to differentiate your brand?

**Color Psychology:**
- **Blue** — Trust, calm, professional (tech, finance)
- **Green** — Growth, health, nature (health, sustainability)
- **Red** — Energy, urgency, passion (sales, alerts)
- **Purple** — Creativity, luxury, mystery (creative, premium)
- **Orange** — Warmth, enthusiasm, friendly (consumer, social)
- **Yellow** — Optimism, attention, caution (warning, energy)

## Building a Color System

### Layer 1: Global Colors

Define your base colors:

```javascript
module.exports = {
  theme: {
    colors: {
      // Primary color with full spectrum
      primary: {
        50: '#EFF6FF',
        100: '#DBEAFE',
        200: '#BFDBFE',
        300: '#93C5FD',
        400: '#60A5FA',
        500: '#3B82F6', // Base
        600: '#2563EB',
        700: '#1D4ED8',
        800: '#1E40AF',
        900: '#1E3A8A',
        950: '#0C2340',
      },
      
      // Secondary color
      secondary: {
        50: '#F3E8FF',
        500: '#8B5CF6',
        950: '#2E1065',
      },
      
      // Semantic colors
      success: '#10B981',
      warning: '#F59E0B',
      error: '#EF4444',
      info: '#06B6D4',
      
      // Neutral colors (grayscale)
      neutral: {
        50: '#F9FAFB',
        100: '#F3F4F6',
        200: '#E5E7EB',
        300: '#D1D5DB',
        400: '#9CA3AF',
        500: '#6B7280',
        600: '#4B5563',
        700: '#374151',
        800: '#1F2937',
        900: '#111827',
        950: '#030712',
      },
    },
  },
};
```

### Layer 2: Semantic Colors

Assign meaning to global colors based on context:

```javascript
module.exports = {
  theme: {
    colors: {
      // Semantic colors (light mode)
      'bg-primary': 'var(--color-bg-primary)', // {neutral.50}
      'bg-secondary': 'var(--color-bg-secondary)', // {neutral.100}
      'bg-tertiary': 'var(--color-bg-tertiary)', // {neutral.200}
      
      'text-primary': 'var(--color-text-primary)', // {neutral.950}
      'text-secondary': 'var(--color-text-secondary)', // {neutral.600}
      'text-tertiary': 'var(--color-text-tertiary)', // {neutral.500}
      'text-inverse': 'var(--color-text-inverse)', // {neutral.50}
      
      'border-primary': 'var(--color-border-primary)', // {neutral.200}
      'border-secondary': 'var(--color-border-secondary)', // {neutral.300}
      
      'interactive-primary': 'var(--color-interactive-primary)', // {primary.500}
      'interactive-hover': 'var(--color-interactive-hover)', // {primary.600}
      'interactive-active': 'var(--color-interactive-active)', // {primary.700}
      'interactive-disabled': 'var(--color-interactive-disabled)', // {neutral.300}
    },
  },
};
```

### Layer 3: Component Colors

Define colors for specific components:

```javascript
module.exports = {
  theme: {
    colors: {
      // Button colors
      'button-primary-bg': 'var(--color-interactive-primary)',
      'button-primary-text': 'var(--color-text-inverse)',
      'button-secondary-bg': 'var(--color-bg-secondary)',
      'button-secondary-text': 'var(--color-text-primary)',
      
      // Card colors
      'card-bg': 'var(--color-bg-primary)',
      'card-border': 'var(--color-border-primary)',
      
      // Input colors
      'input-bg': 'var(--color-bg-primary)',
      'input-border': 'var(--color-border-primary)',
      'input-text': 'var(--color-text-primary)',
    },
  },
};
```

## Accessibility and Contrast

### WCAG Contrast Requirements

| Level | Normal Text | Large Text | Graphics |
| :--- | :--- | :--- | :--- |
| AA | 4.5:1 | 3:1 | 3:1 |
| AAA | 7:1 | 4.5:1 | 3:1 |

**Large text** is defined as 18px+ (or 14px+ if bold).

### Checking Contrast

Use tools like WebAIM Contrast Checker or Polished to verify contrast:

```javascript
// Using Polished library
import { readableColor } from 'polished';

const backgroundColor = '#3B82F6';
const textColor = readableColor(backgroundColor); // Returns #FFFFFF or #000000
```

### Color-Blind Friendly Palettes

Design for color-blind users by:

1. **Not relying on color alone** — Use patterns, icons, or text labels
2. **Using sufficient contrast** — Ensures visibility regardless of color perception
3. **Testing with color-blind simulators** — Use tools like Coblis or Color Oracle

**Color-Blind Friendly Palette:**
```
Primary: #0173B2 (blue, visible to all)
Secondary: #DE8F05 (orange, visible to all)
Accent: #CC78BC (purple, visible to most)
Neutral: #CA9161 (brown, visible to all)
```

## Dark Mode

### Implementing Dark Mode

Define semantic colors that change based on color scheme:

```css
/* Light mode (default) */
:root {
  --color-bg-primary: #F9FAFB;
  --color-bg-secondary: #F3F4F6;
  --color-text-primary: #030712;
  --color-text-secondary: #4B5563;
  --color-border-primary: #E5E7EB;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg-primary: #030712;
    --color-bg-secondary: #111827;
    --color-text-primary: #F9FAFB;
    --color-text-secondary: #D1D5DB;
    --color-border-primary: #374151;
  }
}
```

### Dark Mode Best Practices

1. **Don't use pure black** — Use dark grays (#111827 instead of #000000)
2. **Reduce saturation** — Colors feel too bright in dark mode
3. **Increase contrast** — Text needs more contrast on dark backgrounds
4. **Test readability** — Dark mode can hide readability issues
5. **Respect user preference** — Use `prefers-color-scheme` media query

## Common Color Patterns

### Pattern 1: Status Colors
```javascript
colors: {
  'status-success': '#10B981',
  'status-warning': '#F59E0B',
  'status-error': '#EF4444',
  'status-info': '#06B6D4',
}
```

### Pattern 2: Interactive States
```javascript
colors: {
  'interactive-default': '#3B82F6',
  'interactive-hover': '#2563EB',
  'interactive-active': '#1D4ED8',
  'interactive-disabled': '#D1D5DB',
  'interactive-focus': '#3B82F6', // with outline
}
```

### Pattern 3: Elevation
```javascript
colors: {
  'elevation-1': '#FFFFFF', // Highest
  'elevation-2': '#F9FAFB',
  'elevation-3': '#F3F4F6',
  'elevation-4': '#E5E7EB', // Lowest
}
```

## How to Use This Skill with Claude Code

### Create a Color System

```
"I'm using the color-system skill. Can you create a color system for me?
- Primary color: #3B82F6 (blue)
- Brand personality: Modern, professional, trustworthy
- Include: primary, secondary, semantic, and component colors
- Ensure WCAG AA contrast compliance
- Support both light and dark modes
- Provide Tailwind config"
```

### Audit Your Color System

```
"Can you audit my current color system?
- Are my colors harmonious?
- Do all text/background combinations meet WCAG AA?
- Are my colors used consistently?
- Is my dark mode accessible?
- Are my colors color-blind friendly?
- What improvements would you suggest?"
```

### Create Color-Blind Friendly Palette

```
"Can you create a color-blind friendly palette?
- Primary color: blue
- Secondary color: orange
- Accent color: purple
- Ensure all combinations are visible to color-blind users
- Provide contrast ratios for verification"
```

### Implement Dark Mode

```
"Can you help me implement dark mode?
- Define semantic color tokens for light and dark modes
- Ensure contrast is sufficient in both modes
- Provide CSS variables and Tailwind config
- Test readability in both modes"
```

## Design Critique: Evaluating Your Color System

Claude Code can critique your colors:

```
"Can you evaluate my color system?
- Are my colors harmonious?
- Do they support my brand personality?
- Are all contrast ratios sufficient?
- Is my dark mode accessible?
- Are my colors color-blind friendly?
- What's one thing I could improve immediately?"
```

## Integration with Other Skills

- **design-foundation** — Color tokens and system
- **typography-system** — Text color and contrast
- **component-architecture** — Component colors
- **accessibility-excellence** — Contrast ratios, color-blind friendly
- **interaction-design** — Color in animations and states

## Key Principles

**1. Color Harmony Matters**
Use color theory to create palettes that feel intentional and professional.

**2. Accessibility is Non-Negotiable**
All text/background combinations must meet WCAG AA contrast requirements.

**3. Semantic Colors Enable Flexibility**
By separating global, semantic, and component colors, you can support theming and dark mode.

**4. Consistency Builds Trust**
Use colors consistently across your product to build trust and reduce cognitive load.

**5. Color-Blind Friendly Design Benefits Everyone**
Designing for color-blind users results in better designs for everyone.

## Checklist: Is Your Color System Ready?

- [ ] Primary color is chosen with intention
- [ ] Color palette is harmonious (monochromatic, analogous, complementary, or triadic)
- [ ] Global colors are defined with full spectrum
- [ ] Semantic colors are defined for common contexts
- [ ] Component colors are defined for specific components
- [ ] All text/background combinations meet WCAG AA contrast
- [ ] Dark mode is supported with appropriate colors
- [ ] Colors are color-blind friendly
- [ ] Colors are used consistently across the product
- [ ] Color system is documented and shared with the team
- [ ] Color tokens are centralized in Tailwind config or CSS variables

A well-designed color system is both beautiful and functional. Make it count.
