---
name: visual-style
description: Use when creating or modifying UI components, styling, themes, or layouts in peek-stash-browser. Follow these visual conventions exactly.
---

# Visual Style Guide

## Color System

Colors are defined as CSS custom properties, set by the theme provider. Never use hardcoded colors.

### Core Variables

```css
--bg-primary          /* Page background (#0a0a0b dark) */
--bg-secondary        /* Nav, buttons, controls (#1d1d20) */
--bg-card             /* Cards, modals (#19191b) */
--bg-tertiary         /* Skeleton loaders, subtle backgrounds */
--text-primary        /* Main text (white) */
--text-secondary      /* Secondary text (15% dimmer) */
--text-muted          /* De-emphasized text (30% dimmer) */
--accent-primary      /* Primary accent (theme-dependent) */
--accent-secondary    /* Secondary accent */
--border-color        /* Borders (#2a2a32) */
--focus-ring-color    /* Keyboard focus ring */
--focus-ring-shadow   /* Focus ring shadow */
--selection-color     /* Hover/selection outlines */
--selection-bg        /* Selection background (10% accent) */
```

### Status Colors

```css
--status-success: #0F7173    /* Teal */
--status-error: #FD6B86      /* Pink */
--status-info: #3993DD       /* Blue */
--status-warning: #FA8C2A    /* Orange */
/* Each has -bg (10% opacity) and -border (30% opacity) variants */
```

### Themes

Five built-in themes defined in `client/src/themes/themes.js`. Custom themes supported via API. All themes use the same CSS variable interface, only values change.

## Tailwind Patterns

### Breakpoints

Standard Tailwind plus custom large-screen breakpoints:

| Breakpoint | Width | Use |
|-----------|-------|-----|
| `sm` | 640px | Small tablets |
| `md` | 768px | Tablets |
| `lg` | 1024px | Desktop |
| `xl` | 1280px | Large desktop |
| `2xl` | 1536px | Wide monitors |
| `3xl` | 1920px | Full HD |
| `4xl` | 2560px | QHD/1440p |
| `5xl` | 3840px | 4K UHD |

### Common Class Patterns

```jsx
// Card container
"flex flex-col rounded-lg border p-2"
style={{ backgroundColor: "var(--bg-card)", borderColor: "var(--border-color)" }}

// Hover effects on cards
"hover:shadow-lg hover:scale-[1.02] transition-all"

// Card outlines on hover
"hover:outline hover:outline-2 hover:outline-[var(--selection-color)] hover:outline-offset-2"

// Text styling
"text-primary"  /* var(--text-primary) */
"text-secondary" /* var(--text-secondary) */
"text-muted"    /* var(--text-muted) */

// Buttons
"btn"           /* Base: p-2 px-4 rounded-lg border transition-all 0.2s */
"btn-primary"   /* Accent bg, white text, opacity hover */
```

## Grid System

### Grid Densities

Three density levels (small/medium/large) with responsive column counts. Defined in `client/src/constants/grids.js`.

**Standard grid (performers, studios, tags)** — uses `sm:` breakpoint:

| Density | base | sm | lg | xl | 2xl | 3xl | 4xl | 5xl |
|---------|------|-----|-----|-----|------|------|------|------|
| Small | 2 | 3 | 4 | 5 | 6 | 8 | 10 | 14 |
| Medium | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 12 |
| Large | 1 | 2 | 2 | 3 | 3 | 4 | 5 | 8 |

**Scene grid** (uses `md:` breakpoint, different column counts for 16:9):

| Density | base | md | lg | xl | 2xl | 3xl | 4xl | 5xl |
|---------|------|-----|-----|-----|------|------|------|------|
| Small | 2 | 3 | 4 | 5 | 6 | 7 | 9 | 12 |
| Medium | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 10 |
| Large | 1 | 2 | 2 | 3 | 3 | 4 | 5 | 6 |

Grid gap is always `gap-4` (1rem).

### Card Density Scaling

CSS custom properties scale text and spacing per density. Applied via `density-{level}` class on the grid container.

| Property | Small | Medium | Large |
|----------|-------|--------|-------|
| `--card-title-size` | 13px | 15px | 16px |
| `--card-subtitle-size` | 12px | 13px | 14px |
| `--card-padding` | 6px | 8px | 10px |
| `--card-image-margin` | 8px | 12px | 14px |
| `--card-rating-icon-size` | 14px | 18px | 20px |

## Card Component Architecture

Cards use a composable primitive system defined in `client/src/components/ui/CardComponents.jsx`:

```
CardContainer          - Outer wrapper (border, bg, hover effects)
  CardImage            - Aspect-ratio image with lazy loading
  CardTitle            - MarqueeText with auto-scroll on overflow
  CardSubtitle         - Secondary text line
  CardDescription      - ExpandableDescription (3-line clamp default)
  CardIndicators       - Relationship counts (performers, tags, etc.)
  CardRatingRow        - Rating + O-counter + favorite + menu
  CardMenuRow          - Entity-specific action buttons
```

`BaseCard` in `client/src/components/ui/BaseCard.jsx` composes these primitives via render slots. Entity-specific cards (SceneCard, PerformerCard, etc.) pass their content to BaseCard.

### Aspect Ratios by Entity

| Entity | Ratio | CSS |
|--------|-------|-----|
| Scene | 16:9 | `aspect-[16/9]` |
| Performer | 2:3 | `aspect-[2/3]` |
| Gallery | 3:4 | `aspect-[3/4]` |
| Studio | 16:9 | `aspect-[16/9]` |
| Tag | 16:9 | `aspect-[16/9]` |

## Animation & Transitions

### Standard Transitions

- Card hover: `transition-all 0.2s ease`
- Button states: `transition-all 0.15s ease`

### Keyboard Focus

```css
.keyboard-focus {
  outline: 3px solid var(--focus-ring-color);
  box-shadow: var(--focus-ring-shadow), 0 8px 24px rgba(0,0,0,0.4);
  transform: scale(1.05);
  z-index: 10;
}
```

Pulse animation on focused card (2s infinite, subtle scale 1.0-1.02).

### Mouse vs Keyboard

```css
.mouse-user *:focus {
  outline: none !important;
  box-shadow: none !important;
}
```

Focus rings only show for keyboard/TV navigation, not mouse clicks.

### MarqueeText

Card titles auto-scroll when text overflows on hover. Implementation in `client/src/components/ui/MarqueeText.jsx`:
- Speed: ~30px/second
- Pauses at start (15%) and end (25%)
- Respects `prefers-reduced-motion`
- GPU-accelerated via `translate3d`

### Loading Skeletons

```jsx
<div className="animate-pulse rounded-lg" style={{
  backgroundColor: "var(--bg-tertiary)",
  height: "20rem"  // scene cards, 24rem for standard
}} />
```

## Keyboard Navigation

The app supports full TV/remote navigation with spatial awareness:

- **Zones**: search, topPagination, grid, bottomPagination, mainNav
- **Focus class**: `keyboard-focus` on the active element
- **tabIndex**: 0 for focused element, -1 for all others
- **Arrow keys**: Spatial navigation within grid
- **Enter/Space**: Select/navigate
- **Escape**: Move between zones

## Layout Patterns

### Page Structure

```jsx
<PageLayout>
  <PageHeader />           {/* Title, search, filter controls */}
  <GridLayout>             {/* Or BaseGrid */}
    <EntityCard />          {/* Repeated per item */}
  </GridLayout>
  <Pagination />
</PageLayout>
```

### Containers

| Class | Behavior |
|-------|----------|
| `.layout-container` | Full viewport width |
| `.container` | 0.25rem padding mobile, 1rem desktop |
| `.container-fluid` | Full width + responsive padding |
| `.container-constrained` | Max 1400px + responsive padding |

## Rules

1. **Never hardcode colors** — always use CSS custom properties
2. **Never skip breakpoints** — always include 3xl/4xl/5xl for large displays
3. **Use density variables** for text sizing — never hardcode font sizes in cards
4. **Respect focus patterns** — keyboard-focus class, not custom focus styles
5. **Use CardComponents primitives** — don't create new card layouts from scratch
6. **Images lazy load** via IntersectionObserver — never eager-load grid images
7. **Transitions are 0.2s ease** — don't use longer or different easing
8. **Status colors are fixed** — success=teal, error=pink, info=blue, warning=orange
