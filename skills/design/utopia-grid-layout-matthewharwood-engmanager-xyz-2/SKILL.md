---
name: utopia-grid-layout
description: CSS Grid, Flexbox, and Subgrid using Utopia.fyi fluid spacing for gaps and gutters. Use when creating two-dimensional grid layouts, one-dimensional flex layouts, nested subgrids, or implementing the Utopian declarative grid system. Combines layout primitives with fluid space scales for proportional, responsive layouts without breakpoints.
allowed-tools: Read, Write, Edit, Bash
---

# Utopia Grid & Layout

*CSS Grid, Flexbox, and Subgrid with Utopia.fyi fluid spacing system*

## Core Philosophy

Utopia's layout approach follows the same **declarative design principle** as its type and space scales: establish rules at @min and @max viewports, let the browser interpret contextually. Grid and Flexbox become **systematic layout primitives** powered by fluid space tokens.

**Key Insight**: "Get the gutters right, and the rest will follow." — Utopia focuses on fluid gutters/gaps that maintain proportional relationships across all viewports.

## When to Use This Skill

- Implementing CSS Grid with fluid gutters from Utopia space scale
- Creating Flexbox layouts with fluid gaps
- Using CSS Subgrid for nested grid alignment
- Building the Utopian declarative grid system
- Choosing between Grid and Flexbox for specific layouts
- Combining layout systems with Utopia fluid space tokens
- Creating proportional, systematic layouts without breakpoint-heavy media queries

## Grid vs Flexbox Decision Matrix

```
Need a layout system?
├─ One-dimensional (row OR column)?
│  └─ Use Flexbox
│     Examples: Navigation bars, button groups, card content, centered items
│     Gap: Use Utopia space tokens (var(--space-s), var(--space-m))
│
└─ Two-dimensional (rows AND columns)?
   └─ Use CSS Grid
      Examples: Page layouts, card grids, dashboards, galleries
      Gap: Use Utopia space tokens for consistent spacing
```

**Best Practice**: Combine both — Grid for overall structure, Flexbox for components within grid cells.

## CSS Grid with Utopia Spacing

### Basic Grid with Fluid Gaps

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--space-m); /* Fluid gap from Utopia space scale */
}

/* Gap scales: 24px → 30px automatically */
```

**Why This Works:**
- `gap` uses Utopia space token
- Spacing scales proportionally with viewport
- No breakpoint needed for gap adjustments
- Maintains systematic spacing relationships

### Responsive Grid Without Media Queries

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr));
  gap: var(--space-s-m); /* Dramatic scaling: 16px → 30px */
}
```

**auto-fit vs auto-fill:**
- `auto-fit`: Collapses empty tracks, stretches items
- `auto-fill`: Maintains empty tracks, items don't stretch

**Use Cases:**
- `auto-fit`: Card grids where items should fill space
- `auto-fill`: Galleries maintaining consistent item sizes

### Named Grid Areas with Utopia Gaps

```css
.page-layout {
  display: grid;
  grid-template-areas:
    "header header header"
    "sidebar main aside"
    "footer footer footer";
  grid-template-columns: 250px 1fr 200px;
  grid-template-rows: auto 1fr auto;
  gap: var(--space-m); /* Fluid gap between all areas */
  min-height: 100vh;
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.aside { grid-area: aside; }
.footer { grid-area: footer; }
```

### Asymmetric Grid with Fluid Gaps

```css
.asymmetric-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  column-gap: var(--space-l); /* Horizontal: 32px → 40px */
  row-gap: var(--space-m); /* Vertical: 24px → 30px */
}

/* Or combined */
.asymmetric-grid {
  gap: var(--space-m) var(--space-l); /* row-gap column-gap */
}
```

### Nested Grid with Inherited Gaps

```css
.outer-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-l);
}

.nested-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-s); /* Smaller gap for nested content */
}
```

**Pattern**: Outer grids use larger space tokens (L, XL), inner grids use smaller tokens (S, M) for visual hierarchy.

## Utopian Declarative Grid System

### Philosophy

Rather than fixed columns, the Utopian grid uses **fluid gutters derived from the space scale** and lets columns fill remaining space.

**"Get the gutters right, and the rest will follow."**

### Implementation

```css
:root {
  /* Grid configuration */
  --grid-max-width: 77.5rem; /* Content max-width */
  --grid-gutter: var(--space-s-l); /* Fluid gutter: 16px → 40px */
  --grid-columns: 12;
}

.grid {
  display: grid;
  grid-template-columns:
    /* Outer gutter (fluid) */
    minmax(var(--grid-gutter), 1fr)
    /* 12 content columns */
    repeat(
      var(--grid-columns),
      minmax(0, calc(var(--grid-max-width) / var(--grid-columns)))
    )
    /* Outer gutter (fluid) */
    minmax(var(--grid-gutter), 1fr);
  column-gap: var(--grid-gutter);
}

/* Default: full width within gutters */
.grid > * {
  grid-column: 2 / -2;
}

/* Narrower content */
.grid-item--narrow {
  grid-column: 4 / -4;
}

/* Specific column spans */
.grid-item--span-6 {
  grid-column: auto / span 6;
}
```

### Utopia Grid Calculator

**URL**: https://utopia.fyi/grid/calculator/

**Inputs:**
- Min/max viewport widths (match type/space scale)
- Number of columns (12 recommended)
- Min/max gutter sizes (from space calculator)
- Content max-width

**Output:** CSS grid template using fluid gutters

**Why 12 Columns?**
- Divides evenly into 2, 3, 4, 6-column layouts
- Supports uneven distributions (e.g., 7/5 split)
- Industry standard, familiar to designers

### Grid Workflow

1. **Define @min and @max viewports** (match type/space scales)
2. **Choose column count** (typically 12)
3. **Select gutter space tokens** (e.g., S-L for dramatic scaling)
4. **Set content max-width** (e.g., 77.5rem for ~1240px)
5. **Generate CSS** from Utopia grid calculator
6. **Apply to layout container**

## Flexbox with Utopia Spacing

### Basic Flex with Fluid Gaps

```css
.flex-row {
  display: flex;
  gap: var(--space-m); /* Fluid gap between flex items */
}

.flex-column {
  display: flex;
  flex-direction: column;
  gap: var(--space-s); /* Vertical spacing */
}
```

### Navigation with Fluid Spacing

```css
.nav {
  display: flex;
  gap: var(--space-s-m); /* 16px → 30px between nav items */
  align-items: center;
}

.nav__item {
  padding: var(--space-2xs) var(--space-s);
}
```

### Button Group

```css
.button-group {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-xs); /* Consistent, subtle scaling */
}

.button {
  padding: var(--space-2xs) var(--space-s);
  font-size: var(--step-0);
}
```

### Flex Cards with Proportional Spacing

```css
.card-row {
  display: flex;
  gap: var(--space-m-l); /* Dramatic gap scaling: 24px → 40px */
  flex-wrap: wrap;
}

.card {
  flex: 1 1 min(300px, 100%);
  padding: var(--space-s-m);
  display: flex;
  flex-direction: column;
  gap: var(--space-xs); /* Inner card spacing */
}
```

### Centered Content with Flex

```css
.center-flex {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: var(--space-l); /* Outer spacing */
}

.center-flex__content {
  max-width: 70ch;
  display: flex;
  flex-direction: column;
  gap: var(--space-m); /* Inner spacing */
}
```

## CSS Subgrid with Utopia

### What is Subgrid?

Subgrid allows nested grids to **inherit track sizing and gap values** from parent grids, enabling perfectly aligned nested layouts.

**Browser Support (2025):** Chrome 118+, Edge 118+, Firefox 71+, Safari 16+ (Baseline ✅)

### Basic Subgrid Syntax

```css
.parent-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-l); /* Parent gap */
}

.subgrid-item {
  display: grid;
  grid-template-columns: subgrid; /* Inherits parent's columns */
  grid-column: span 2; /* Spans 2 parent columns */
  gap: inherit; /* Inherits parent's gap */
}
```

### Card Grid with Aligned Sections

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-m-l); /* Fluid gap: 24px → 40px */
}

.card {
  display: grid;
  grid-template-rows: subgrid; /* Align card sections across all cards */
  grid-row: span 3; /* Image, content, footer */
  padding: var(--space-s);
  gap: var(--space-xs); /* Inner card spacing */
}

/* All images align horizontally across cards */
.card__image {
  grid-row: 1;
  aspect-ratio: 16 / 9;
}

/* All content sections align */
.card__content {
  grid-row: 2;
}

/* All footers align at bottom */
.card__footer {
  grid-row: 3;
  margin-block-start: auto;
}
```

**Why This Works:**
- Subgrid inherits parent's row tracks
- All `.card__footer` elements align across cards regardless of content height
- Maintains Utopia spacing with `gap: var(--space-xs)` inside cards

### Form Layout with Subgrid

```css
.form {
  display: grid;
  grid-template-columns: [labels] 150px [inputs] 1fr [help] 200px;
  gap: var(--space-s); /* Fluid gap throughout form */
}

.form-group {
  display: grid;
  grid-template-columns: subgrid; /* Inherits 3-column structure */
  grid-column: 1 / -1; /* Spans all columns */
  gap: inherit; /* Inherits parent gap */
}

.form-group label {
  grid-column: labels;
  padding-block: var(--space-3xs); /* Vertical alignment */
}

.form-group input {
  grid-column: inputs;
}

.form-group .help-text {
  grid-column: help;
  font-size: var(--step--1);
}
```

### Subgrid with Named Lines

```css
.parent {
  display: grid;
  grid-template-columns:
    [sidebar-start] 250px
    [sidebar-end main-start] 1fr
    [main-end];
  gap: var(--space-l);
}

.child {
  display: grid;
  grid-template-columns: subgrid; /* Inherits named lines */
  grid-column: sidebar-start / main-end;
  gap: inherit;
}

/* Child can reference parent's named lines */
.nested-element {
  grid-column: main-start / main-end;
  padding: var(--space-m);
}
```

### Progressive Enhancement for Subgrid

```css
.card {
  display: grid;
  grid-template-rows: auto 1fr auto; /* Fallback */
  gap: var(--space-xs);
}

@supports (grid-template-rows: subgrid) {
  .card-grid {
    display: grid;
    grid-template-rows: repeat(3, auto);
    gap: var(--space-m);
  }

  .card {
    grid-template-rows: subgrid;
    grid-row: span 3;
  }
}
```

## Combining Grid, Flex, and Utopia Spacing

### Page Layout Example

```css
/* Outer structure: Grid */
.page-layout {
  display: grid;
  grid-template-areas:
    "header"
    "main"
    "footer";
  grid-template-rows: auto 1fr auto;
  gap: var(--space-l); /* Page section spacing */
  min-height: 100vh;
}

/* Header: Flex */
.header {
  grid-area: header;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-s-m);
  gap: var(--space-m);
}

/* Main: Grid for content */
.main {
  grid-area: main;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--space-m-l); /* Card grid spacing */
  padding: var(--space-l);
}

/* Card: Flex for internal layout */
.card {
  display: flex;
  flex-direction: column;
  gap: var(--space-s); /* Internal card spacing */
  padding: var(--space-m);
}

/* Footer: Flex */
.footer {
  grid-area: footer;
  display: flex;
  justify-content: center;
  padding: var(--space-m);
}
```

**Pattern Hierarchy:**
- **Grid**: Page-level structure, card grids
- **Flexbox**: Header/footer navigation, card internals
- **Utopia Spacing**: All gaps/padding use space tokens
- **Proportional Scaling**: Everything scales together

### Article with Sidebar

```css
.article-layout {
  display: grid;
  grid-template-columns: 1fr min(65ch, 100%) 1fr; /* Center column */
  gap: var(--space-m);
}

.article-layout > * {
  grid-column: 2; /* All content in center column */
}

.article__hero {
  grid-column: 1 / -1; /* Full width */
  min-height: 50vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-xl-2xl);
}

.article__content {
  display: flex;
  flex-direction: column;
  gap: var(--space-m); /* Paragraph spacing */
}

.article__content h2 {
  font-size: var(--step-3);
  margin-block-start: var(--space-l);
  margin-block-end: var(--space-s);
}

.article__content p {
  font-size: var(--step-0);
  line-height: 1.6;
}
```

## Best Practices

1. **Grid for Structure** - Use Grid for two-dimensional layouts (page structure, card grids)
2. **Flex for Flow** - Use Flexbox for one-dimensional layouts (nav bars, button groups)
3. **Utopia Gaps Always** - Use space tokens for all `gap` values
4. **Proportional Hierarchy** - Outer containers use larger gaps (L, XL), inner use smaller (S, M)
5. **Space Pairs for Drama** - Use space pairs (S-M, M-L) for significant scaling
6. **Subgrid for Alignment** - Use subgrid when nested items must align across parent grid
7. **Inherit Gaps** - Use `gap: inherit` in subgrids to maintain parent spacing
8. **Named Areas for Clarity** - Use `grid-template-areas` for readable, semantic layouts
9. **Progressive Enhancement** - Provide fallbacks for subgrid with `@supports`
10. **Test at Poles** - View layouts at @min and @max viewports to ensure fluid behavior

## Common Patterns

### Hero Section
```css
.hero {
  display: grid;
  place-items: center;
  min-height: 80vh;
  padding: var(--space-xl-2xl); /* Dramatic scaling */
  text-align: center;
}

.hero__content {
  display: flex;
  flex-direction: column;
  gap: var(--space-m);
  max-width: 60ch;
}
```

### Card Grid
```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr));
  gap: var(--space-m-l); /* 24px → 40px */
}

.card {
  display: flex;
  flex-direction: column;
  gap: var(--space-s);
  padding: var(--space-m);
  border: 1px solid var(--color-border);
}
```

### Dashboard Layout
```css
.dashboard {
  display: grid;
  grid-template-areas:
    "header header header"
    "sidebar main aside"
    "footer footer footer";
  grid-template-columns: 250px 1fr 300px;
  grid-template-rows: auto 1fr auto;
  gap: var(--space-m);
  min-height: 100vh;
}

.widget-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--space-s-m);
}
```

### Gallery with Masonry-Style
```css
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  grid-auto-flow: dense; /* Fill gaps with smaller items */
  gap: var(--space-s);
}

.gallery__item--large {
  grid-column: span 2;
  grid-row: span 2;
}
```

## Integration with Other Skills

**Prerequisites:**
- Use `utopia-fluid-scales` skill first to generate space tokens
- Space tokens (--space-s, --space-m, etc.) must exist in `:root`

**Complementary:**
- Use `utopia-container-queries` skill for component-level responsiveness
- Combine Grid/Flex layouts with container queries for adaptive components

**Workflow:**
1. Generate Utopia type and space scales (`utopia-fluid-scales`)
2. Implement grid/flex layouts with space token gaps (`utopia-grid-layout`)
3. Add container queries for component adaptation (`utopia-container-queries`)

## Resources

- **Utopia Grid Calculator**: https://utopia.fyi/grid/calculator/
- **Utopia Blog - Grid Design**: https://utopia.fyi/blog/designing-a-utopian-layout-grid/
- **MDN CSS Grid**: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout
- **MDN Subgrid**: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout/Subgrid
- **web.dev Subgrid**: https://web.dev/articles/css-subgrid

## Next Steps

After implementing grid layouts:
1. Combine with `utopia-container-queries` for component-level fluid behavior
2. Use both Grid and Flexbox together (Grid for structure, Flex for components)
3. Test layouts at @min, @max, and midpoint viewports to verify fluid scaling
4. Iterate on gutter sizes using Utopia space calculator for optimal spacing hierarchy
