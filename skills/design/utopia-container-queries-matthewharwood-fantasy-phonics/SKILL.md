---
name: utopia-container-queries
description: Container query setup required for this project's cqi-based fluid scales. The type and space tokens use cqi units which need container-type declarations to function.
allowed-tools: Read, Write, Edit
---

# Utopia Container Queries

*Container setup required for this project's fluid scales*

## Critical: cqi Units Require Container Context

This project's type and space scales use `cqi` (container query inline) units:

```css
/* From typography.css */
--step-0: clamp(1.125rem, 1.0739rem + 0.2273cqi, 1.25rem);

/* From space.css */
--space-m: clamp(1.6875rem, 1.6108rem + 0.3409cqi, 1.875rem);
```

**Without a container context, the `cqi` portion evaluates to 0**, meaning values stay at their minimum.

## Required Setup

For fluid scaling to work, you must establish a container context:

### Option 1: Root Container (Recommended)

Apply to html or body for global container context:

```css
html {
  container-type: inline-size;
}
```

Or in your component:

```css
body {
  container-type: inline-size;
}
```

### Option 2: Component-Level Containers

For component-specific containers:

```css
.card-container {
  container-type: inline-size;
}

/* Optional: name the container */
.card-container {
  container: card / inline-size;
}
```

## Current State

**No container-type declarations exist in the CSS files.** The fluid scales are defined but will not scale fluidly until container context is added.

### Files That Need Container Context

| File | Has cqi Units | Has container-type |
|------|---------------|-------------------|
| `typography.css` | Yes | No |
| `space.css` | Yes | No |
| `grid.css` | No (uses vw fallback) | No |

## Adding Container Support

### Minimal Setup

Add to `css/styles/index.css`:

```css
html {
  container-type: inline-size;
}
```

### Per-Component Setup

For isolated components:

```css
.my-component {
  container-type: inline-size;
}
```

## Container Query Syntax

Once containers are established, you can use container queries:

```css
@container (inline-size > 400px) {
  .card {
    display: grid;
    grid-template-columns: 150px 1fr;
  }
}

/* Named container query */
@container card (inline-size > 600px) {
  .card__title {
    font-size: var(--step-3);
  }
}
```

## Container Units Available

| Unit | Description |
|------|-------------|
| `cqi` | 1% of container inline size (width in LTR) |
| `cqb` | 1% of container block size (height in LTR) |
| `cqw` | 1% of container width |
| `cqh` | 1% of container height |
| `cqmin` | Smaller of cqi/cqb |
| `cqmax` | Larger of cqi/cqb |

## What's NOT Defined

The following are **not** currently in the CSS:

- Any `container-type` declarations
- Any `@container` queries
- Named containers

The infrastructure (cqi-based tokens) exists, but the container context to make it functional does not.

## Next Steps

1. Add `container-type: inline-size` to html or body
2. Verify fluid scaling works by resizing viewport
3. Add component-level containers as needed
4. Add `@container` queries for component-level responsiveness

## Files

- `css/styles/index.css` - Recommended location for root container setup
- `css/styles/layouts.css` - Empty, available for container utilities
