---
name: utopia-grid-layout
description: CSS Grid utilities using Utopia fluid spacing. Reference for the grid variables and utility classes defined in this project.
allowed-tools: Read, Write, Edit
---

# Utopia Grid Layout

*This project's grid system with fluid spacing*

## Configuration

Generated from: https://utopia.fyi/grid/calculator?c=360,18,1.2,1240,20,1.25,5,2,&s=0.75|0.5|0.25,1.5|2|3|4|6,s-l&g=s,l,xl,12

## Grid Variables

Location: `css/styles/grid.css`

```css
:root {
  --grid-max-width: 77.50rem;
  --grid-gutter: var(--space-s-l, clamp(1.125rem, 0.5625rem + 2.5vw, 2.5rem));
  --grid-columns: 12;
}
```

| Variable | Value | Description |
|----------|-------|-------------|
| `--grid-max-width` | 77.50rem (1240px) | Maximum content width |
| `--grid-gutter` | var(--space-s-l) | Fluid gutter: 18px → 40px |
| `--grid-columns` | 12 | Column count |

## Utility Classes

### .u-container

Centers content with fluid horizontal padding.

```css
.u-container {
  max-width: var(--grid-max-width);
  padding-inline: var(--grid-gutter);
  margin-inline: auto;
}
```

**Usage:**
```html
<div class="u-container">
  <!-- Content constrained to 1240px max width -->
</div>
```

### .u-grid

Basic grid with fluid gap.

```css
.u-grid {
  display: grid;
  gap: var(--grid-gutter);
}
```

**Usage:**
```html
<div class="u-grid">
  <div>Grid item</div>
  <div>Grid item</div>
</div>
```

## Usage Patterns

### Combine Container and Grid

```html
<div class="u-container">
  <div class="u-grid" style="grid-template-columns: repeat(3, 1fr);">
    <div>Item 1</div>
    <div>Item 2</div>
    <div>Item 3</div>
  </div>
</div>
```

### Auto-fit Responsive Grid

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr));
  gap: var(--grid-gutter);
}
```

### Using Space Tokens for Custom Gaps

```css
.tight-grid {
  display: grid;
  gap: var(--space-s);
}

.loose-grid {
  display: grid;
  gap: var(--space-xl);
}
```

## What's NOT Defined

The following patterns are **not** currently in the CSS:

- Column span classes (e.g., `.col-span-6`)
- Named grid areas
- Subgrid utilities
- Layout primitives (stack, cluster, sidebar)

Add these as needed based on project requirements.

## Files

- `css/styles/grid.css` - Grid variables and utilities
- `css/styles/layouts.css` - Currently empty, available for layout utilities
