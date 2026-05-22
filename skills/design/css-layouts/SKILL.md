---
name: css-layout-development
description: This skill provides prescriptive guidance for writing modern CSS layouts using intrinsic design principles, container queries, and fluid responsive techniques. When implementing CSS layouts, always consult this document first.
---

# CSS Layout Development Skill

## Purpose

This skill provides prescriptive guidance for writing modern CSS layouts using intrinsic design principles, container queries, and fluid responsive techniques. When implementing CSS layouts, always consult this document first.

## Core Decision Framework

### When Starting Any Layout Task

1. **Identify the layout type needed:**

   - Stack: Vertical flow with consistent spacing
   - Cluster: Horizontal items that wrap
   - Sidebar: One intrinsic width column, one flexible
   - Grid: Multiple columns that adapt to space
   - Frame: Aspect ratio enforcement

2. **Determine responsiveness strategy:**

   - Use container queries for component-level adaptation
   - Use fluid values (clamp) for typography and spacing
   - Use quantity queries for content-aware layouts
   - Avoid fixed breakpoint media queries unless absolutely necessary

3. **Check for component reusability:**
   - Will this component appear in multiple contexts?
   - If yes, make it a container query candidate
   - If no, viewport-based queries may be acceptable

## Layout Primitives: Implementation Patterns

### Stack Pattern

**Use when:** You need consistent vertical spacing between elements.

```css
.stack {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

/* With fluid spacing */
.stack {
  display: flex;
  flex-direction: column;
  gap: clamp(1rem, 0.8rem + 1vw, 2rem);
}
```

**Key points:**

- Always use `gap` instead of margins on children
- Let the container handle all spacing
- Use custom properties for spacing values
- Scale spacing with clamp() for fluidity

### Cluster Pattern

**Use when:** You have inline items that should wrap naturally.

```css
.cluster {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-sm);
  align-items: center;
}
```

**Key points:**

- Always set `flex-wrap: wrap`
- Use `gap` for consistent spacing in both directions
- Consider `align-items` for vertical alignment
- Works for tags, buttons, inline metadata

### Sidebar Pattern

**Use when:** One element has intrinsic width, another is flexible.

```css
.sidebar {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-md);
}

.sidebar > * {
  flex-grow: 1;
}

.sidebar > :first-child {
  flex-basis: 250px;
  flex-grow: 0;
}
```

**Key points:**

- The sidebar (first child) has fixed `flex-basis`
- The content (second child) grows with `flex-grow: 1`
- Will stack when space is insufficient
- Use logical properties: `flex-basis` not widths

### Adaptive Grid Pattern

**Use when:** You need columns that adjust to available space.

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(250px, 100%), 1fr));
  gap: var(--space-md);
}

/* With container queries */
.grid {
  container-type: inline-size;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(250px, 100%), 1fr));
  gap: clamp(1rem, 2cqw, 2rem);
}
```

**Key points:**

- Use `auto-fit` to collapse empty columns
- Use `minmax(min(250px, 100%), 1fr)` to prevent overflow
- The `min()` wrapper prevents the minimum from forcing overflow
- Never use fixed column counts with media queries

### Frame Pattern

**Use when:** You need to enforce aspect ratios.

```css
.frame {
  aspect-ratio: 16 / 9;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.frame > img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
```

**Key points:**

- Always use `aspect-ratio` property
- Set `object-fit` on images inside
- Use `overflow: hidden` to contain content
- Provide fallback dimensions for older browsers

## Container Queries: Implementation Guide

### Setting Up Containers

```css
/* Define container */
.card-wrapper {
  container-name: card;
  container-type: inline-size;
}

/* Or shorthand */
.card-wrapper {
  container: card / inline-size;
}
```

**Key points:**

- Always name containers for clarity
- Use `inline-size` for width-based queries
- Can have multiple named containers in a tree
- Parent containers affect child container calculations

### Size Container Queries

```css
/* Basic pattern */
@container card (min-width: 400px) {
  .card {
    flex-direction: row;
  }
}

/* With container name */
@container card (min-width: 400px) {
  .card-content {
    padding: clamp(1rem, 2cqw, 2rem);
  }
}
```

**When to use:**

- Component layout changes based on available space
- Typography scaling relative to container
- Image sizing relative to container
- Any dimensional adaptation

**Common thresholds:**

- 300px: Minimum for horizontal card layout
- 400px: Comfortable horizontal layout
- 600px: Multi-column internal layouts
- Adjust based on actual content needs

### Style Container Queries

```css
/* Set custom property on container */
.card-wrapper {
  --featured: true;
}

/* Query it */
@container style(--featured: true) {
  .card {
    grid-template-columns: 1fr 1fr;
  }

  .card-thumb {
    grid-column: 1 / -1;
  }
}
```

**When to use:**

- Component variants (featured, compact, minimal)
- Theme switching at component level
- Conditional layouts based on configuration
- State-driven styling

**Key points:**

- Use boolean values: `true` or absent
- Can combine with size queries
- Cleaner than multiple class variants
- Enables declarative component configuration

### Container Query Units

```css
/* Typography with cqw */
.title {
  font-size: clamp(1rem, 1rem + 2cqw, 1.75rem);
}

/* Spacing with cqw */
.card {
  padding: clamp(0.5rem, 1cqw, 2rem);
  gap: clamp(0.5rem, 2cqw, 1.5rem);
}

/* Dimensions with cqw */
.card-thumb {
  flex: 0 0 clamp(70px, 10cqw + 70px, 150px);
}
```

**Available units:**

- `cqw`: 1% of container width
- `cqh`: 1% of container height
- `cqi`: 1% of container inline size
- `cqb`: 1% of container block size
- `cqmin`: Smaller of `cqi` or `cqb`
- `cqmax`: Larger of `cqi` or `cqb`

**Best practices:**

- Prefer `cqw` over `vw` for component-level scaling
- Always wrap in `clamp()` with min/max bounds
- Use for typography, spacing, and flexible dimensions
- Test at extreme container sizes

## Fluid Typography and Spacing

### Fluid Type Scale Pattern

```css
:root {
  --font-size-sm: clamp(0.875rem, 0.8rem + 0.375vw, 1rem);
  --font-size-base: clamp(1rem, 0.9rem + 0.5vw, 1.25rem);
  --font-size-md: clamp(1.125rem, 1rem + 0.625vw, 1.5rem);
  --font-size-lg: clamp(1.5rem, 1.3rem + 1vw, 2rem);
  --font-size-xl: clamp(2rem, 1.6rem + 2vw, 3rem);
}
```

**How to calculate:**

- Minimum: Mobile size (typically 16px base)
- Maximum: Desktop size (typically 20px base)
- Growth factor: `(max - min) / viewport-range` as vw
- Formula: `clamp(min, min + growth-factor, max)`

**Use this calculator:**
https://min-max-calculator.9elements.com/

### Fluid Spacing Scale Pattern

```css
:root {
  --space-3xs: clamp(0.25rem, 0.2rem + 0.25vw, 0.375rem);
  --space-2xs: clamp(0.5rem, 0.4rem + 0.5vw, 0.75rem);
  --space-xs: clamp(0.75rem, 0.6rem + 0.75vw, 1.125rem);
  --space-sm: clamp(1rem, 0.8rem + 1vw, 1.5rem);
  --space-md: clamp(1.5rem, 1.2rem + 1.5vw, 2.25rem);
  --space-lg: clamp(2rem, 1.6rem + 2vw, 3rem);
  --space-xl: clamp(3rem, 2.4rem + 3vw, 4.5rem);
  --space-2xl: clamp(4rem, 3.2rem + 4vw, 6rem);
}
```

**Key points:**

- Maintain consistent ratios between steps
- Each step typically 1.5x the previous
- Use semantic names, not arbitrary numbers
- Reference these variables everywhere

### Component-Level Fluid Scaling

```css
.component {
  container-type: inline-size;
}

.component-title {
  /* Scales with container, not viewport */
  font-size: clamp(1rem, 1rem + 2cqw, 1.75rem);
}

.component-content {
  /* Spacing scales with container */
  padding: clamp(1rem, 2cqw, 2rem);
  gap: clamp(0.5rem, 1cqw, 1rem);
}
```

## Quantity Queries: Implementation Patterns

### Basic Quantity Query

```css
/* 4 or more items */
.section:has(.card:nth-last-child(n + 4)) {
  grid-template-columns: 1fr;
}

/* Exactly 3 items */
.section:has(.card:last-child:nth-child(3)) {
  grid-template-columns: repeat(3, 1fr);
}

/* Between 2 and 4 items */
.section:has(.card:nth-last-child(n + 2):nth-last-child(-n + 4)) {
  grid-template-columns: repeat(2, 1fr);
}
```

### Common Quantity Query Patterns

```css
/* Layout changes based on quantity */
.section {
  display: grid;
  gap: var(--space-md);
}

/* 1-3 items: horizontal layout */
.section:has(.card:nth-last-child(-n + 3)) {
  grid-template-columns: 200px 1fr;
}

/* 4+ items: vertical layout with compact header */
.section:has(.card:nth-last-child(n + 4)) {
  grid-template-columns: 1fr;
}

.section:has(.card:nth-last-child(n + 4)) .section-header {
  display: flex;
  flex-direction: row;
  gap: 1rem;
}
```

### Featured Items Based on Quantity

```css
/* Feature first item when 6+ items */
.section:has(.card:nth-last-child(n + 6)) .card:first-child {
  --featured: true;
  grid-column: 1 / -1;
}

/* Feature first two items when 8+ items */
.section:has(.card:nth-last-child(n + 8)) .card:nth-child(-n + 2) {
  --featured: true;
}
```

## Using :has() for Conditional Styling

### Content-Based Styling

```css
/* Card without image */
.card:not(:has(img)) {
  border-inline-start: 4px solid var(--color-accent);
  padding-inline-start: 1rem;
}

/* Card with image */
.card:has(img) {
  display: grid;
  grid-template-columns: auto 1fr;
}

/* Section with featured item */
.section:has([data-featured]) {
  grid-template-rows: auto 1fr;
}
```

### Sibling-Aware Styling

```css
/* First card when there's a second card */
.card:has(+ .card) {
  border-bottom: 1px solid var(--color-border);
}

/* Last card in a group */
.card:not(:has(+ .card)) {
  border-bottom: none;
}
```

## Grid vs Flexbox: Decision Matrix

### Use CSS Grid When:

- You need two-dimensional layout (rows AND columns)
- Items need precise positioning
- Layout areas are named and structured
- Overlapping elements are needed
- You want items to align across tracks

**Example scenarios:**

- Page layouts with header, sidebar, main, footer
- Card grids that adapt column count
- Dashboard layouts
- Magazine-style layouts

### Use Flexbox When:

- You need one-dimensional layout (row OR column)
- Items should distribute space flexibly
- Items need to wrap onto new lines
- Order of items might change
- Content size should drive layout

**Example scenarios:**

- Navigation bars
- Button groups
- Inline metadata (tags, dates, authors)
- Card internal content
- Form layouts

### Common Combinations

```css
/* Grid for overall structure, flex for content */
.card {
  display: grid;
  grid-template-rows: auto 1fr auto;
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

/* Grid for main layout, flex for header */
.page {
  display: grid;
  grid-template-columns: 250px 1fr;
}

.page-header {
  grid-column: 1 / -1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
```

## Defensive CSS Checklist

Before finalizing any CSS, verify these defensive patterns:

### ✓ Flexbox Items

```css
/* Always set min-width on flex items that could overflow */
.flex-item {
  min-width: 0;
}

/* Especially for images in flex containers */
.flex-item img {
  min-width: 0;
  max-width: 100%;
}
```

### ✓ Text Overflow

```css
/* Readable line length */
.prose {
  max-width: 65ch;
}

/* Long words */
.text {
  overflow-wrap: break-word;
  hyphens: auto;
}

/* Truncate with ellipsis when needed */
.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
```

### ✓ Images

```css
/* Prevent overflow */
img {
  max-width: 100%;
  height: auto;
}

/* Maintain aspect ratio in flex/grid */
.card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Prevent too-small images */
.thumbnail {
  min-width: 48px;
  min-height: 48px;
}
```

### ✓ Variable Content Heights

```css
/* Use min-height, not height */
.card {
  min-height: 200px;
}

/* Allow growth */
.container {
  height: auto;
  min-height: 100vh;
}

/* Set max-height for very long content */
.description {
  max-height: 200px;
  overflow: auto;
}
```

### ✓ Empty States

```css
/* Handle empty containers gracefully */
.grid:empty {
  display: none;
}

/* Minimum content for empty sections */
.section:not(:has(*)) {
  min-height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.section:not(:has(*))::after {
  content: 'No content available';
  color: var(--color-muted);
}
```

## Common Patterns and Solutions

### Card Component Pattern

```css
.card {
  container: card / inline-size;
  display: flex;
  flex-direction: column;
  gap: clamp(0.5rem, 2cqw, 1rem);
  padding: clamp(1rem, 3cqw, 1.5rem);
}

/* Switch to horizontal at sufficient width */
@container card (min-width: 400px) {
  .card {
    flex-direction: row;
    gap: clamp(1rem, 3cqw, 2rem);
  }

  .card-thumbnail {
    flex: 0 0 clamp(100px, 15cqw, 200px);
    min-width: 0;
  }
}

/* Fluid typography inside card */
.card-title {
  font-size: clamp(1rem, 0.8rem + 2cqw, 1.5rem);
}

/* Featured variant */
@container style(--featured: true) {
  .card {
    background: var(--color-featured);
  }
}

/* No image variant */
.card:not(:has(.card-thumbnail)) {
  border-inline-start: 4px solid var(--color-accent);
  padding-inline-start: 1rem;
}
```

### Section Layout Pattern

```css
.section {
  container: section / inline-size;
  display: grid;
  gap: clamp(1rem, 2cqw, 2rem);
}

/* Default: sidebar layout for 1-3 items */
.section:has(.card:nth-last-child(-n + 3)) {
  grid-template-columns: 200px 1fr;
}

/* 4+ items: stacked with compact header */
.section:has(.card:nth-last-child(n + 4)) {
  grid-template-columns: 1fr;
}

.section:has(.card:nth-last-child(n + 4)) .section-header {
  display: flex;
  flex-direction: row;
  gap: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--color-border);
}

/* Featured first item with 6+ total */
@container section (min-width: 600px) {
  .section:has(.card:nth-last-child(n + 6)) .card:first-child {
    --featured: true;
    grid-column: 1 / -1;
  }
}
```

### Responsive Grid Pattern

```css
.grid {
  container: grid / inline-size;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(250px, 100%), 1fr));
  gap: clamp(1rem, 2cqw, 2rem);
}

/* Adjust minimum width at container sizes */
@container grid (min-width: 800px) {
  .grid {
    grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr));
  }
}

/* Dense packing for many items */
.grid:has(.item:nth-last-child(n + 12)) {
  grid-auto-flow: dense;
}
```

## Testing Requirements

Before considering any layout complete, test these scenarios:

### Content Variations

1. **Very long text:** Titles with 100+ characters, descriptions with 500+ words
2. **Very short text:** Single word titles, one sentence descriptions
3. **Missing content:** No images, no descriptions, empty sections
4. **Many items:** 1, 2, 5, 10, 20, 50 items
5. **Mixed content:** Some items with images, some without

### Container Variations

1. Place component in narrow sidebar (200px)
2. Place component in medium container (600px)
3. Place component in wide container (1200px)
4. Place component full-width
5. Nest component inside another component

### Browser Testing

1. Test in Chrome, Firefox, Safari
2. Verify container query support (fallback if needed)
3. Test `:has()` support (fallback if needed)
4. Verify `clamp()` calculations at extremes
5. Test logical property support

## Anti-Patterns to Avoid

### ❌ Don't: Fixed Breakpoints for Components

```css
/* BAD: Component knows about viewport */
.card {
  flex-direction: column;
}

@media (min-width: 768px) {
  .card {
    flex-direction: row;
  }
}
```

```css
/* GOOD: Component responds to container */
.card {
  container-type: inline-size;
  flex-direction: column;
}

@container (min-width: 400px) {
  .card {
    flex-direction: row;
  }
}
```

### ❌ Don't: Magic Numbers

```css
/* BAD: Arbitrary value with no system */
.element {
  margin-top: 23px;
  padding: 17px;
}
```

```css
/* GOOD: System-based spacing */
.element {
  margin-top: var(--space-md);
  padding: var(--space-sm);
}
```

### ❌ Don't: Fixed Typography

```css
/* BAD: Jumps at breakpoints */
.title {
  font-size: 18px;
}

@media (min-width: 768px) {
  .title {
    font-size: 24px;
  }
}
```

```css
/* GOOD: Fluid scaling */
.title {
  font-size: clamp(1.125rem, 1rem + 0.5vw, 1.5rem);
}
```

### ❌ Don't: Class Variants for State

```css
/* BAD: Multiple classes for variants */
.card {
  /* base */
}
.card--featured {
  /* featured variant */
}
.card--compact {
  /* compact variant */
}
.card--featured-compact {
  /* combined variant */
}
```

```css
/* GOOD: Style queries with custom properties */
.card {
  /* base styles */
}

@container style(--featured: true) {
  .card {
    /* featured styles */
  }
}

@container style(--compact: true) {
  .card {
    /* compact styles */
  }
}
```

### ❌ Don't: Viewport Units Without Boundaries

```css
/* BAD: Unbounded growth */
.title {
  font-size: 2vw; /* Too small on mobile, too large on desktop */
}
```

```css
/* GOOD: Bounded with clamp */
.title {
  font-size: clamp(1.5rem, 2vw, 3rem);
}
```

## Quick Reference: Common Values

### Fluid Typography Scale

```css
--font-size-sm: clamp(0.875rem, 0.8rem + 0.375vw, 1rem);
--font-size-base: clamp(1rem, 0.9rem + 0.5vw, 1.25rem);
--font-size-md: clamp(1.125rem, 1rem + 0.625vw, 1.5rem);
--font-size-lg: clamp(1.5rem, 1.3rem + 1vw, 2rem);
--font-size-xl: clamp(2rem, 1.6rem + 2vw, 3rem);
--font-size-2xl: clamp(2.5rem, 2rem + 2.5vw, 4rem);
```

### Fluid Spacing Scale

```css
--space-3xs: clamp(0.25rem, 0.2rem + 0.25vw, 0.375rem);
--space-2xs: clamp(0.5rem, 0.4rem + 0.5vw, 0.75rem);
--space-xs: clamp(0.75rem, 0.6rem + 0.75vw, 1.125rem);
--space-sm: clamp(1rem, 0.8rem + 1vw, 1.5rem);
--space-md: clamp(1.5rem, 1.2rem + 1.5vw, 2.25rem);
--space-lg: clamp(2rem, 1.6rem + 2vw, 3rem);
--space-xl: clamp(3rem, 2.4rem + 3vw, 4.5rem);
--space-2xl: clamp(4rem, 3.2rem + 4vw, 6rem);
--space-3xl: clamp(6rem, 4.8rem + 6vw, 9rem);
```

### Container Query Breakpoints

```css
/* Typical component breakpoints */
@container (min-width: 300px) {
  /* Minimum for horizontal layout */
}
@container (min-width: 400px) {
  /* Comfortable horizontal */
}
@container (min-width: 600px) {
  /* Multi-column internal */
}
@container (min-width: 800px) {
  /* Full-featured layout */
}
```

### Common Grid Patterns

```css
/* Auto-fit responsive grid */
grid-template-columns: repeat(auto-fit, minmax(min(250px, 100%), 1fr));

/* Two-column with flexible sidebar */
grid-template-columns: minmax(200px, 250px) 1fr;

/* Holy grail layout */
grid-template-areas:
  'header header header'
  'sidebar main aside'
  'footer footer footer';
```

## Resources

- Clamp Calculator: https://min-max-calculator.9elements.com/
- Quantity Query Tool: https://css-tip.com/quantity-queries/
- Container Query Support: https://caniuse.com/css-container-queries
- Every Layout: https://every-layout.dev/
- Utopia Fluid Responsive Design: https://utopia.fyi/

## Summary

When writing CSS:

1. Start with the appropriate layout primitive
2. Make components container-aware, not viewport-aware
3. Use fluid values with clamp() for typography and spacing
4. Leverage quantity queries for content-aware layouts
5. Apply defensive techniques for variable content
6. Test across content and container variations
7. Avoid magic numbers and arbitrary breakpoints

The goal is resilient, adaptive layouts that work across infinite contexts without brittle overrides or complex media query chains.
