---
name: css
description: Modern, maintainable, and accessible CSS using latest features and best practices. Grid, Flexbox, custom properties, container queries, cascade layers. Trigger: When writing CSS styles, implementing layouts with Grid/Flexbox, or using modern CSS features.
skills:
  - conventions
  - a11y
  - humanizer
allowed-tools:
  - documentation-reader
  - web-search
  - file-reader
---

# CSS Modern Skill

## Overview

This skill provides guidance for writing modern CSS with focus on maintainability, performance, and accessibility using current CSS features and best practices.

## Objective

Enable developers to write clean, efficient CSS that leverages modern features like CSS Grid, Flexbox, custom properties, and container queries while maintaining accessibility and browser compatibility.

---

## When to Use

Use this skill when:

- Writing CSS styles for layouts and components
- Implementing responsive designs with Grid/Flexbox
- Using modern CSS features (custom properties, container queries)
- Optimizing CSS performance and maintainability
- Creating animations and transitions

Don't use this skill for:

- Tailwind utility classes (use tailwindcss skill)
- MUI sx prop styling (use mui skill)

---

## Critical Patterns

### ✅ REQUIRED: Use Custom Properties for Theming

```css
/* ✅ CORRECT: Custom properties */
:root {
  --color-primary: #0066cc;
  --spacing: 1rem;
}

.button {
  background: var(--color-primary);
  padding: var(--spacing);
}

/* ❌ WRONG: Hardcoded values */
.button {
  background: #0066cc;
  padding: 1rem;
}
```

### ✅ REQUIRED: Use Grid/Flexbox, Not Floats

```css
/* ✅ CORRECT: Flexbox for layout */
.container {
  display: flex;
  gap: 1rem;
  justify-content: space-between;
}

/* ❌ WRONG: Floats (legacy) */
.container {
  float: left;
  clear: both;
}
```

### ✅ REQUIRED: Respect prefers-reduced-motion

```css
/* ✅ CORRECT: Disable animations for accessibility */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### ✅ REQUIRED: Use Modern Responsive Patterns

```css
/* ✅ CORRECT: Fluid typography with clamp() */
h1 {
  font-size: clamp(2rem, 5vw, 4rem);
}

/* ✅ CORRECT: Container queries for component-level responsive */
@container (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 1fr 2fr;
  }
}

/* ✅ CORRECT: Modern aspect ratio */
.video-container {
  aspect-ratio: 16 / 9;
}

/* ❌ WRONG: Padding hack for aspect ratio */
.video-container {
  padding-bottom: 56.25%; /* Old technique */
}
```

### ✅ REQUIRED: Use Modern Selectors

```css
/* ✅ CORRECT: :is() for grouping selectors */
:is(h1, h2, h3) {
  color: var(--color-heading);
}

/* ✅ CORRECT: :where() for zero specificity */
:where(ul, ol) {
  padding-left: 1rem;
}

/* ✅ CORRECT: :has() for parent selection (modern browsers) */
.card:has(img) {
  display: grid;
}

/* ❌ WRONG: Verbose selector duplication */
h1,
h2,
h3 {
  color: var(--color-heading);
}
```

### ✅ REQUIRED: Use @layer for Cascade Control

```css
/* ✅ CORRECT: Define cascade layers */
@layer reset, base, components, utilities;

@layer reset {
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
}

@layer base {
  body {
    font-family: system-ui, sans-serif;
  }
}

@layer components {
  .button {
    padding: 0.5rem 1rem;
  }
}

@layer utilities {
  .text-center {
    text-align: center;
  }
}
```

---

## Conventions

Refer to conventions for:

- Code organization
- Naming patterns

Refer to a11y for:

- Color contrast
- Focus indicators
- Accessible animations

### CSS Specific

- Use CSS custom properties for theming
- Prefer Flexbox and Grid over floats
- Use logical properties (margin-inline, padding-block)
- Implement responsive design with container queries when appropriate
- Avoid !important except for utilities
- Use BEM or similar naming convention
- **Use modern selectors** (`:is()`, `:where()`, `:has()`)
- **Use `aspect-ratio`** for consistent image/video sizing
- **Use `@layer`** for cascade control (Cascade Layers)
- **Use `clamp()`, `min()`, `max()`** for fluid responsive values

---

## Decision Tree

**One-dimensional layout?** → Use Flexbox with `flex-direction`, `justify-content`, `align-items`.

**Two-dimensional layout?** → Use CSS Grid with `grid-template-columns`, `grid-template-rows`.

**Responsive sizing?** → Use `clamp()`, `min()`, `max()` for fluid typography and spacing.

**Theme values?** → Define in `:root` with custom properties, reference with `var(--name)`.

**Center element?** → Flexbox: `display: flex; justify-content: center; align-items: center;` or Grid: `place-items: center`.

**Hide element?** → Use `display: none` to remove from DOM, `visibility: hidden` to keep space, `opacity: 0` for transitions.

**Responsive breakpoints?** → Use container queries for component-level, media queries for viewport-level.

---

## Example

```css
:root {
  --color-primary: #0066cc;
  --spacing-unit: 0.5rem;
}

.card {
  display: flex;
  flex-direction: column;
  gap: calc(var(--spacing-unit) * 2);
  padding: var(--spacing-unit);
  border-radius: 0.5rem;
  background-color: var(--color-primary);
}

@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
  }
}
```

## Edge Cases

- Handle print stylesheets
- Support dark mode with prefers-color-scheme
- Test with different font sizes
- Verify with color blindness simulators

## References

- https://web.dev/learn/css/
- https://developer.mozilla.org/en-US/docs/Web/CSS
