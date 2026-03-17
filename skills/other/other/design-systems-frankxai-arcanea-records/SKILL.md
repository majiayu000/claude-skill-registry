---
name: Design System Architecture
description: Build consistent, scalable design systems with proper token architecture
version: 1.0.0
license: MIT
tier: community
---

# Design System Architecture

> **Create consistent, scalable visual languages that evolve gracefully**

This skill provides frameworks for building design systems that scale from single projects to entire organizations.

## Core Principles

### 1. Tokens Are Truth
Design decisions should be encoded as tokens (variables). Nothing should be hard-coded.

### 2. Constraints Enable Creativity
A good design system provides guardrails that speed up decisions, not slow them down.

### 3. Components Over Compositions
Build primitives that compose into anything, not specific layouts that restrict.

## Token Architecture

### The Token Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                     SEMANTIC TOKENS                          │
│  (What they mean: --color-primary, --spacing-section)       │
└────────────────────────────┬────────────────────────────────┘
                             │ Reference
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                     ALIAS TOKENS                             │
│  (Design decisions: --color-brand-primary, --size-lg)       │
└────────────────────────────┬────────────────────────────────┘
                             │ Reference
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                     PRIMITIVE TOKENS                         │
│  (Raw values: --blue-500, --space-16, --font-inter)         │
└─────────────────────────────────────────────────────────────┘
```

### Primitive Tokens

Raw values with no semantic meaning.

```css
/* Colors - use naming that indicates value, not usage */
--gray-50: #fafafa;
--gray-100: #f5f5f5;
--gray-200: #e5e5e5;
--gray-300: #d4d4d4;
--gray-400: #a3a3a3;
--gray-500: #737373;
--gray-600: #525252;
--gray-700: #404040;
--gray-800: #262626;
--gray-900: #171717;

--blue-50: #eff6ff;
--blue-100: #dbeafe;
--blue-200: #bfdbfe;
--blue-300: #93c5fd;
--blue-400: #60a5fa;
--blue-500: #3b82f6;
--blue-600: #2563eb;
--blue-700: #1d4ed8;
--blue-800: #1e40af;
--blue-900: #1e3a8a;

/* Spacing - use consistent scale */
--space-0: 0;
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-20: 5rem;     /* 80px */
--space-24: 6rem;     /* 96px */

/* Typography */
--font-sans: system-ui, -apple-system, sans-serif;
--font-mono: ui-monospace, monospace;

--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
--text-5xl: 3rem;      /* 48px */

--leading-tight: 1.25;
--leading-normal: 1.5;
--leading-relaxed: 1.75;

--weight-normal: 400;
--weight-medium: 500;
--weight-semibold: 600;
--weight-bold: 700;
```

### Alias Tokens

Design decisions that reference primitives.

```css
/* Brand colors */
--color-brand-primary: var(--blue-600);
--color-brand-primary-hover: var(--blue-700);
--color-brand-secondary: var(--gray-600);

/* Size scale */
--size-xs: var(--space-2);
--size-sm: var(--space-3);
--size-md: var(--space-4);
--size-lg: var(--space-6);
--size-xl: var(--space-8);

/* Radius */
--radius-none: 0;
--radius-sm: 0.125rem;
--radius-md: 0.375rem;
--radius-lg: 0.5rem;
--radius-xl: 0.75rem;
--radius-full: 9999px;
```

### Semantic Tokens

Tokens that describe usage, not values.

```css
/* Backgrounds */
--color-bg-primary: var(--white);
--color-bg-secondary: var(--gray-50);
--color-bg-tertiary: var(--gray-100);
--color-bg-inverse: var(--gray-900);

/* Text */
--color-text-primary: var(--gray-900);
--color-text-secondary: var(--gray-600);
--color-text-tertiary: var(--gray-400);
--color-text-inverse: var(--white);
--color-text-link: var(--color-brand-primary);

/* Borders */
--color-border-default: var(--gray-200);
--color-border-strong: var(--gray-300);
--color-border-focus: var(--color-brand-primary);

/* States */
--color-success: var(--green-600);
--color-warning: var(--yellow-500);
--color-error: var(--red-600);
--color-info: var(--blue-600);

/* Component tokens */
--button-padding-x: var(--space-4);
--button-padding-y: var(--space-2);
--button-radius: var(--radius-md);
--button-font-weight: var(--weight-medium);

--input-padding: var(--space-3);
--input-border-width: 1px;
--input-radius: var(--radius-md);

--card-padding: var(--space-6);
--card-radius: var(--radius-lg);
--card-shadow: 0 1px 3px rgba(0,0,0,0.1);
```

## Color System

### Building a Color Palette

```yaml
Color Palette Structure:

  Neutrals:
    Purpose: Text, backgrounds, borders
    Scale: 50-900 (10 shades minimum)
    Key values:
      - 50: Subtle backgrounds
      - 100-200: Secondary backgrounds
      - 400-500: Placeholder text
      - 600-700: Secondary text
      - 800-900: Primary text

  Brand Primary:
    Purpose: CTAs, links, key actions
    Scale: 50-900
    Key values:
      - 500-600: Main brand color
      - 600-700: Hover states
      - 100-200: Light backgrounds

  Brand Secondary:
    Purpose: Accents, secondary actions
    Scale: 50-900 (can be smaller)

  Semantic Colors:
    Success: Typically green family
    Warning: Typically yellow/amber family
    Error: Typically red family
    Info: Typically blue family
```

### Dark Mode Strategy

```css
/* Light theme (default) */
:root {
  --color-bg-primary: var(--white);
  --color-bg-secondary: var(--gray-50);
  --color-text-primary: var(--gray-900);
  --color-text-secondary: var(--gray-600);
  --color-border-default: var(--gray-200);
}

/* Dark theme */
[data-theme="dark"] {
  --color-bg-primary: var(--gray-900);
  --color-bg-secondary: var(--gray-800);
  --color-text-primary: var(--gray-50);
  --color-text-secondary: var(--gray-400);
  --color-border-default: var(--gray-700);
}

/* System preference */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --color-bg-primary: var(--gray-900);
    /* ... dark values ... */
  }
}
```

## Typography System

### Type Scale

```yaml
Typography Scale:

  Display:
    - display-2xl: 4.5rem/1.1 (72px) - Hero headlines
    - display-xl: 3.75rem/1.1 (60px) - Major headings
    - display-lg: 3rem/1.1 (48px) - Section headlines

  Headings:
    - heading-xl: 2.25rem/1.25 (36px) - Page titles
    - heading-lg: 1.875rem/1.3 (30px) - Section titles
    - heading-md: 1.5rem/1.35 (24px) - Subsections
    - heading-sm: 1.25rem/1.4 (20px) - Card titles
    - heading-xs: 1.125rem/1.4 (18px) - Small headings

  Body:
    - body-lg: 1.125rem/1.6 (18px) - Lead paragraphs
    - body-md: 1rem/1.6 (16px) - Default body
    - body-sm: 0.875rem/1.5 (14px) - Secondary text

  Utility:
    - caption: 0.75rem/1.4 (12px) - Labels, captions
    - overline: 0.75rem/1.4 uppercase tracked - Categories
```

### Implementing Type Scale

```css
/* Type scale implementation */
.text-display-2xl {
  font-size: var(--text-5xl);
  line-height: 1.1;
  font-weight: var(--weight-bold);
  letter-spacing: -0.02em;
}

.text-heading-xl {
  font-size: var(--text-4xl);
  line-height: 1.25;
  font-weight: var(--weight-semibold);
  letter-spacing: -0.01em;
}

.text-body-md {
  font-size: var(--text-base);
  line-height: 1.6;
  font-weight: var(--weight-normal);
}
```

## Spacing System

### Spacing Scale Philosophy

```yaml
Spacing Philosophy:

  Base Unit: 4px (0.25rem)

  Scale Type: Geometric with adjustments

  Common uses:
    - 4px (space-1): Icon gaps, tight spacing
    - 8px (space-2): Inline elements, button padding (y)
    - 12px (space-3): Form inputs padding
    - 16px (space-4): Component padding, button padding (x)
    - 24px (space-6): Card padding, section gaps
    - 32px (space-8): Related section spacing
    - 48px (space-12): Unrelated section spacing
    - 64px (space-16): Major page sections
    - 96px (space-24): Hero/footer spacing
```

### Spacing Usage Guidelines

```yaml
Component Spacing:

  Buttons:
    Padding: space-2 space-4 (8px 16px)
    Gap between: space-2 (8px)

  Cards:
    Padding: space-6 (24px)
    Gap between: space-6 (24px)
    Internal gaps: space-4 (16px)

  Forms:
    Input padding: space-3 (12px)
    Label to input: space-2 (8px)
    Between fields: space-6 (24px)

  Lists:
    Item padding: space-3 space-4
    Between items: space-1 or space-2

Page Spacing:

  Section padding: space-16 to space-24 (64-96px)
  Content width: max 80ch for prose
  Grid gaps: space-6 to space-8
```

## Component Architecture

### Component Anatomy

```yaml
Component Anatomy:

  Button Example:

    Container:
      - Background color (semantic)
      - Border radius (from scale)
      - Border (optional)
      - Padding (from scale)
      - Min height/width

    Content:
      - Text color (semantic)
      - Font size (from scale)
      - Font weight (from scale)
      - Line height
      - Letter spacing

    Icon (optional):
      - Size (proportional)
      - Color (inherit or specific)
      - Spacing from text

    States:
      - Default
      - Hover
      - Active/Pressed
      - Focus (keyboard)
      - Disabled
      - Loading
```

### Component Variants Pattern

```css
/* Base component */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  padding: var(--button-padding-y) var(--button-padding-x);
  border-radius: var(--button-radius);
  font-weight: var(--button-font-weight);
  transition: all 150ms ease;
}

/* Variants */
.btn-primary {
  background: var(--color-brand-primary);
  color: var(--color-text-inverse);
}

.btn-primary:hover {
  background: var(--color-brand-primary-hover);
}

.btn-secondary {
  background: transparent;
  border: 1px solid var(--color-border-default);
  color: var(--color-text-primary);
}

.btn-ghost {
  background: transparent;
  color: var(--color-text-primary);
}

/* Sizes */
.btn-sm {
  padding: var(--space-1) var(--space-3);
  font-size: var(--text-sm);
}

.btn-lg {
  padding: var(--space-3) var(--space-6);
  font-size: var(--text-lg);
}
```

## Tailwind Integration

### Custom Tailwind Config

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    colors: {
      // Map to your tokens
      transparent: 'transparent',
      current: 'currentColor',

      // Primitives
      gray: {
        50: 'var(--gray-50)',
        100: 'var(--gray-100)',
        // ... etc
      },

      // Semantic (recommended approach)
      bg: {
        primary: 'var(--color-bg-primary)',
        secondary: 'var(--color-bg-secondary)',
        tertiary: 'var(--color-bg-tertiary)',
      },
      text: {
        primary: 'var(--color-text-primary)',
        secondary: 'var(--color-text-secondary)',
      },
      border: {
        DEFAULT: 'var(--color-border-default)',
        strong: 'var(--color-border-strong)',
      },
    },

    spacing: {
      0: 'var(--space-0)',
      1: 'var(--space-1)',
      2: 'var(--space-2)',
      // ... etc
    },

    borderRadius: {
      none: 'var(--radius-none)',
      sm: 'var(--radius-sm)',
      DEFAULT: 'var(--radius-md)',
      lg: 'var(--radius-lg)',
      full: 'var(--radius-full)',
    },

    fontSize: {
      xs: ['var(--text-xs)', { lineHeight: '1.4' }],
      sm: ['var(--text-sm)', { lineHeight: '1.5' }],
      base: ['var(--text-base)', { lineHeight: '1.6' }],
      // ... etc
    },
  },
}
```

## Animation System

### Animation Tokens

```css
/* Duration */
--duration-instant: 0ms;
--duration-fast: 100ms;
--duration-normal: 200ms;
--duration-slow: 300ms;
--duration-slower: 500ms;

/* Easing */
--ease-linear: linear;
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
```

### Common Animation Patterns

```css
/* Fade in */
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Slide up */
@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Scale in */
@keyframes scale-in {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* Usage */
.animate-fade-in {
  animation: fade-in var(--duration-normal) var(--ease-out);
}

.animate-slide-up {
  animation: slide-up var(--duration-normal) var(--ease-out);
}
```

## Quality Checklist

### Design System Audit

- [ ] All colors use tokens (no hex values in components)
- [ ] All spacing uses scale values
- [ ] Typography uses defined scale
- [ ] Components have all states defined
- [ ] Dark mode tested
- [ ] Accessibility contrast ratios met (4.5:1 body, 3:1 large)
- [ ] Focus states visible
- [ ] Motion respects prefers-reduced-motion
- [ ] Tokens documented
- [ ] Component API documented

---

*"A design system is not a project. It's a product, serving products."*
