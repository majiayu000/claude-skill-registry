---
name: design-system
category: design
version: 1.0.0
description: Locked design tokens, 2025-2026 aesthetic enforcement
auto_load: true
priority: 1
data_source: .claude/data/design-tokens.json
---

# Design System Skill

Enforces consistent, modern visual design across all UI.

## Locked Values (Cannot Deviate)

### Colors

```css
/* Primary */
--primary: #0D9488;
--primary-light: #14B8A6;
--primary-dark: #0F766E;

/* Neutrals */
--gray-50: #F9FAFB;
--gray-900: #111827;

/* Semantic */
--success: #10B981;
--warning: #F59E0B;
--error: #EF4444;
--info: #3B82F6;
```

### Typography

```css
/* Fonts */
--font-sans: 'Inter', system-ui, sans-serif;
--font-heading: 'Cal Sans', 'Inter', sans-serif;
--font-mono: 'JetBrains Mono', monospace;

/* Sizes */
--text-sm: 0.875rem;
--text-base: 1rem;
--text-lg: 1.125rem;
--text-2xl: 1.5rem;

/* Weights */
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

### Spacing

```css
/* Base: 8px */
--space-2: 0.5rem;   /* 8px */
--space-4: 1rem;     /* 16px */
--space-6: 1.5rem;   /* 24px */
--space-8: 2rem;     /* 32px */
```

### Border Radius

```css
--radius-sm: 6px;
--radius-md: 8px;
--radius-lg: 12px;
--radius-xl: 16px;
```

### Shadows (Soft, Colored - Never Black)

```css
--shadow-md: 0 4px 6px rgba(13, 148, 136, 0.1);
--shadow-lg: 0 10px 15px rgba(13, 148, 136, 0.1);
--shadow-xl: 0 20px 25px rgba(13, 148, 136, 0.15);
```

## Modern Aesthetic (2025-2026)

### Required Elements

- Bento grids (modular, varying card sizes)
- Glassmorphism (frosted glass, backdrop blur)
- Soft colored shadows (not black)
- Gradients (subtle, purposeful)
- Micro-interactions (hover states, transitions)
- Generous whitespace

### Forbidden Elements

- Flat gray boxes
- Generic Lucide icons
- Pure black shadows
- Bootstrap aesthetic
- Static, lifeless UI
- Cramped layouts

## Layout Default: Bento Grid

```jsx
// Basic Bento structure
<div className="grid grid-cols-4 gap-4">
  <div className="col-span-2 row-span-2">Large card</div>
  <div className="col-span-1">Small card</div>
  <div className="col-span-1">Small card</div>
  <div className="col-span-2">Wide card</div>
</div>
```

## Glassmorphism Pattern

```css
.glass {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: var(--radius-lg);
}
```

## Icon Rules

- **NO Lucide icons (DEPRECATED)**
- **NO generic icon libraries**
- **USE AI-generated custom icons**
- **TWO variants**: outline (UI) + duotone (brand)

## Never

- Use Lucide icons
- Use pure black shadows
- Create flat, lifeless UI
- Ignore spacing scale
- Deviate from locked colors
