---
name: utopia-container-queries
description: CSS Container Queries with container units (cqi, cqw, cqh, cqb) combined with Utopia.fyi fluid scales for component-level responsiveness. Use when creating truly modular components that adapt to container size, implementing component-level fluid typography with cqi units, or building context-aware design systems. Extends Utopia philosophy from viewport-based to container-based fluidity.
allowed-tools: Read, Write, Edit, Bash
---

# Utopia Container Queries

*Component-level responsiveness using container queries with Utopia.fyi fluid scales*

## Core Philosophy

Container queries extend Utopia's **declarative, fluid design approach** from the viewport level to the **component level**. Instead of components responding only to viewport width, they respond to their **container's dimensions**, enabling truly modular, context-aware design.

**Key Insight**: Combine Utopia's fluid scales (viewport-based) with container query units (container-based) for **layered responsiveness** — global scaling + component adaptation.

## When to Use This Skill

- Creating components that adapt to container size, not viewport size
- Implementing fluid typography that scales based on component width
- Building truly reusable components for design systems
- Combining Utopia fluid scales with container-level responsiveness
- Using container query units (cqi, cqw) with clamp() for component typography
- Enabling context-aware layouts (sidebar vs. main content area)
- Progressive enhancement from viewport-based to container-based fluidity

## Container Query Fundamentals

### Browser Support (2025)

**Fully supported:** Chrome 105+, Edge 105+, Firefox 110+, Safari 16+
**Baseline:** ✅ Widely available since February 2023
**Browser Compatibility:** 82/100

### Container Types

```css
/* Long form */
.container {
  container-name: card;
  container-type: inline-size; /* Queries width (horizontal) or height (vertical) */
}

/* Shorthand */
.container {
  container: card / inline-size;
}
```

**Container Types:**
- `inline-size` - Query inline dimension (width in LTR, height in vertical writing)
- `size` - Query both dimensions (use sparingly, affects layout performance)
- `normal` - Default, no containment

**Best Practice**: Use `inline-size` for most cases — queries container width without layout side effects.

### Basic Container Query Syntax

```css
/* Named container */
@container card (inline-size > 400px) {
  .card {
    display: grid;
    grid-template-columns: 150px 1fr;
  }
}

/* Unnamed (uses nearest ancestor container) */
@container (width > 500px) {
  .component {
    display: flex;
    gap: var(--space-m);
  }
}

/* Range queries (modern, readable) */
@container (400px <= inline-size <= 800px) {
  .element {
    /* Styles for containers between 400-800px */
  }
}
```

## Container Query Units

Relative sizing units based on **container dimensions**, not viewport:

### Available Units

- `cqw` - 1% of container width
- `cqh` - 1% of container height
- `cqi` - 1% of container inline size (recommended)
- `cqb` - 1% of container block size
- `cqmin` - Smaller of cqi or cqb
- `cqmax` - Larger of cqi or cqb

**Recommended**: Use `cqi` for international audiences — automatically switches to horizontal or vertical axis based on writing mode.

### Container Units with clamp()

```css
.card {
  /* Responsive padding based on container */
  padding: clamp(1rem, 4cqi, 2rem);

  /* Fluid typography */
  font-size: clamp(1rem, 3cqi, 1.6rem);

  /* Dynamic gaps */
  gap: clamp(0.5rem, 2cqw, 1.5rem);
}
```

**How This Works:**
- At small container widths: padding approaches 1rem (minimum)
- At medium widths: padding scales proportionally (4% of container inline size)
- At large widths: padding caps at 2rem (maximum)

## Integrating Container Units with Utopia Scales

### Layered Responsiveness Strategy

**Layer 1**: Viewport-based Utopia fluid scales (global)
**Layer 2**: Container query units (component-level)

```css
:root {
  /* Utopia viewport-based type scale */
  --step-0: clamp(1rem, 0.9286rem + 0.3571vi, 1.25rem);
  --step-1: clamp(1.2rem, 1.1036rem + 0.4821vi, 1.5625rem);
  --step-2: clamp(1.44rem, 1.3113rem + 0.6435vi, 1.9531rem);

  /* Utopia space scale */
  --space-s: clamp(1rem, 0.9286rem + 0.3571vi, 1.25rem);
  --space-m: clamp(1.5rem, 1.3929rem + 0.5357vi, 1.875rem);
  --space-l: clamp(2rem, 1.8571rem + 0.7143vi, 2.5rem);
}

.card-container {
  container: card / inline-size;
}

.card {
  /* Base: Utopia fluid scale (viewport-responsive) */
  padding: var(--space-m);
  font-size: var(--step-0);

  /* Additional container-based adjustments */
  gap: clamp(var(--space-s), 3cqi, var(--space-m));
}
```

**Why This Works:**
- Utopia scales provide **global proportional scaling**
- Container units add **component-level adaptation**
- Double fluidity: responds to both viewport AND container

### Component Typography with cqi

```css
.card-container {
  container: card / inline-size;
}

.card {
  /* Base typography from Utopia */
  font-size: var(--step-0); /* 16px → 20px (viewport) */

  /* Container-based refinement */
  @container (inline-size > 400px) {
    font-size: clamp(var(--step-0), 2.5cqi + 0.5rem, var(--step-1));
  }
}

.card__title {
  /* Viewport-based from Utopia */
  font-size: var(--step-2);

  /* Container-based enhancement */
  @container (inline-size > 600px) {
    font-size: clamp(var(--step-2), 4cqi, var(--step-3));
  }
}
```

**Pattern:**
1. Start with Utopia step (viewport-based foundation)
2. Add container query at breakpoint
3. Use cqi with clamp() bounded by Utopia steps
4. Result: Smooth scaling within Utopia's systematic constraints

### Spacing with Container Units

```css
.card-container {
  container: card / inline-size;
}

.card {
  /* Base padding from Utopia space scale */
  padding: var(--space-s-m); /* 16px → 30px (viewport) */

  /* Container-based adjustment */
  @container (inline-size > 500px) {
    padding: clamp(var(--space-m), 5cqi, var(--space-l));
    gap: clamp(var(--space-s), 2cqi, var(--space-m));
  }
}
```

**Best Practice**: Use Utopia space tokens as min/max bounds for container-based clamp() calculations.

## Container Queries vs Media Queries

### When to Use Container Queries

**✅ Use Container Queries:**
- Component-level responsiveness
- Reusable components in varying contexts
- Design system components
- Cards, widgets, modular UI elements
- Layout flexibility within page sections

### When to Use Media Queries

**✅ Use Media Queries:**
- User preferences (`prefers-color-scheme`, `prefers-reduced-motion`)
- Page-level layouts
- Print styles
- Device characteristics (hover capability)
- Global theme switches

### Best Practice: Use Both Together

```css
/* Global: Media query for dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: #1a1a1a;
    --color-text: #f5f5f5;
  }
}

/* Component: Container query for layout */
@container card (inline-size > 400px) {
  .card {
    display: grid;
    grid-template-columns: 150px 1fr;
  }
}
```

## Practical Patterns

### Adaptive Card Component

```css
.card-container {
  container: card / inline-size;
}

.card {
  /* Base: Utopia scales */
  padding: var(--space-s);
  gap: var(--space-xs);
  font-size: var(--step-0);
  display: grid;
}

/* Small: Stacked layout */
@container card (inline-size < 400px) {
  .card {
    grid-template-columns: 1fr;
    padding: var(--space-s);
  }

  .card__image {
    aspect-ratio: 16 / 9;
  }
}

/* Medium: Horizontal layout */
@container card (inline-size >= 400px) {
  .card {
    grid-template-columns: 150px 1fr;
    padding: clamp(var(--space-s), 3cqi, var(--space-m));
    gap: clamp(var(--space-xs), 2cqi, var(--space-s));
  }
}

/* Large: Enhanced layout */
@container card (inline-size >= 600px) {
  .card {
    grid-template-columns: 200px 1fr;
    padding: clamp(var(--space-m), 4cqi, var(--space-l));
    gap: clamp(var(--space-s), 3cqi, var(--space-m));
  }

  .card__title {
    font-size: clamp(var(--step-1), 3cqi, var(--step-2));
  }

  .card__image {
    aspect-ratio: 3 / 4;
  }
}
```

**Why This Works:**
- Same component code works in sidebar (narrow) or main content (wide)
- Container queries handle layout shifts
- Utopia scales + cqi provide layered fluidity
- Systematic spacing maintained throughout

### Responsive Navigation

```css
.nav-container {
  container: nav / inline-size;
}

.nav {
  display: flex;
  gap: var(--space-s);
  padding: var(--space-s);
}

/* Narrow: Vertical stack */
@container nav (inline-size < 600px) {
  .nav {
    flex-direction: column;
    gap: var(--space-2xs);
  }

  .nav__item {
    width: 100%;
  }
}

/* Wide: Horizontal with fluid gaps */
@container nav (inline-size >= 600px) {
  .nav {
    flex-direction: row;
    gap: clamp(var(--space-s), 2cqi, var(--space-m));
  }
}
```

### Article Component

```css
.article-container {
  container: article / inline-size;
}

.article {
  /* Base typography from Utopia */
  font-size: var(--step-0);
  line-height: 1.6;
  padding: var(--space-m);
}

.article h1 {
  font-size: var(--step-3);
  margin-block-end: var(--space-m);
}

/* Container-based enhancements */
@container article (inline-size > 600px) {
  .article {
    padding: clamp(var(--space-m), 4cqi, var(--space-l));
    max-width: 70ch;
  }

  .article h1 {
    font-size: clamp(var(--step-3), 5cqi, var(--step-4));
    margin-block-end: clamp(var(--space-m), 3cqi, var(--space-l));
  }
}

@container article (inline-size > 900px) {
  .article {
    font-size: clamp(var(--step-0), 2cqi + 0.5rem, var(--step-1));
  }

  .article h1 {
    font-size: clamp(var(--step-4), 6cqi, var(--step-5));
  }
}
```

### Grid Item Adaptation

```css
/* Parent uses Utopia grid */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr));
  gap: var(--space-m-l);
}

/* Each grid item is a container */
.grid-item {
  container: item / inline-size;
}

/* Item adapts to its grid cell width */
.grid-item__content {
  padding: var(--space-s);
  font-size: var(--step-0);
}

@container item (inline-size > 350px) {
  .grid-item__content {
    padding: clamp(var(--space-s), 3cqi, var(--space-m));
    display: grid;
    grid-template-columns: auto 1fr;
    gap: var(--space-s);
  }
}

@container item (inline-size > 500px) {
  .grid-item__content {
    font-size: clamp(var(--step-0), 2.5cqi, var(--step-1));
  }
}
```

**Pattern**: Grid controls layout, container queries control item internals.

## Nested Containers

Multiple containers can coexist with independent queries:

```css
.page-container {
  container: page / inline-size;
}

.sidebar-container {
  container: sidebar / inline-size;
}

.card-container {
  container: card / inline-size;
}

/* Page-level query */
@container page (inline-size > 1200px) {
  .page {
    display: grid;
    grid-template-columns: 300px 1fr;
    gap: var(--space-l);
  }
}

/* Sidebar-level query */
@container sidebar (inline-size > 250px) {
  .sidebar-nav {
    font-size: var(--step-0);
    gap: var(--space-s);
  }
}

/* Card-level query (inside sidebar OR main) */
@container card (inline-size > 400px) {
  .card {
    display: grid;
    grid-template-columns: 150px 1fr;
  }
}
```

**Why This Works:**
- Each container queries independently
- Card responds to ITS container, not page width
- Same card component works in sidebar (narrow) or main (wide)
- True component modularity

## Accessibility Considerations

### Always Test with Browser Zoom

```css
/* ⚠️ Can cause accessibility issues */
.component {
  font-size: 3cqw; /* No min/max bounds */
}
```

**Problem**: When user zooms, container width may not change proportionally, breaking text scaling.

**Solution**: Always use clamp() with Utopia steps as bounds:

```css
/* ✅ Accessible */
.component {
  font-size: clamp(var(--step-0), 2.5cqi, var(--step-1));
}
```

**Testing Checklist:**
1. Zoom to 200% in browser
2. Verify text scales appropriately
3. Ensure minimum sizes are readable
4. Check that container-based scaling doesn't break zoom

### Keep Central rem Value Near 1

```css
/* ✅ Good - users retain zoom control */
font-size: clamp(1rem, 2cqi + 0.5rem, 1.5rem);

/* ⚠️ Problematic - reduces user control */
font-size: clamp(0.5rem, 5cqi, 3rem);
```

**Guideline**: Keep the central rem value close to 1rem and cqi value low (2-3cqi) to preserve user zoom control.

## Progressive Enhancement

### Fallback for Non-Supporting Browsers

```css
/* Base styles (all browsers) */
.card {
  padding: var(--space-m);
  font-size: var(--step-0);
}

/* Enhanced with container queries */
@supports (container-type: inline-size) {
  .card-container {
    container: card / inline-size;
  }

  @container card (inline-size > 400px) {
    .card {
      display: grid;
      grid-template-columns: 150px 1fr;
      padding: clamp(var(--space-m), 4cqi, var(--space-l));
    }
  }
}
```

### Feature Detection in JavaScript

```javascript
if (CSS.supports('container-type: inline-size')) {
  document.documentElement.classList.add('supports-container-queries');
}
```

```css
/* Default */
.component {
  padding: var(--space-m);
}

/* Enhanced when supported */
.supports-container-queries .component-container {
  container: component / inline-size;
}

.supports-container-queries .component {
  @container (inline-size > 500px) {
    padding: clamp(var(--space-m), 4cqi, var(--space-l));
  }
}
```

## Best Practices

1. **Utopia as Foundation** - Start with Utopia fluid scales (viewport-based)
2. **Layer Container Queries** - Add container-level responsiveness on top
3. **Use cqi for Typography** - Better internationalization than cqw
4. **Clamp with Utopia Bounds** - Use Utopia steps as min/max in clamp()
5. **Name Containers** - Use descriptive container names for clarity
6. **Test with Zoom** - Always verify 200% browser zoom works
7. **Avoid Deep Nesting** - Limit container query nesting to 2-3 levels
8. **Single Responsibility** - One container type per component
9. **Progressive Enhancement** - Provide fallbacks for older browsers
10. **Combine with Grid/Flex** - Use with `utopia-grid-layout` for complete system

## Common Patterns

### Modular Card

```css
.card-container {
  container: card / inline-size;
}

.card {
  padding: var(--space-s);
  gap: var(--space-xs);
  font-size: var(--step-0);
}

@container card (inline-size > 400px) {
  .card {
    display: grid;
    grid-template-columns: auto 1fr;
    padding: clamp(var(--space-s), 3cqi, var(--space-m));
  }
}
```

### Responsive Widget

```css
.widget-container {
  container: widget / inline-size;
}

.widget {
  padding: var(--space-m);
}

.widget__title {
  font-size: var(--step-2);
}

@container widget (inline-size < 300px) {
  .widget {
    padding: var(--space-s);
  }

  .widget__title {
    font-size: var(--step-1);
  }
}

@container widget (inline-size > 600px) {
  .widget {
    padding: clamp(var(--space-m), 4cqi, var(--space-l));
  }

  .widget__title {
    font-size: clamp(var(--step-2), 4cqi, var(--step-3));
  }
}
```

### Context-Aware Component

```css
/* Same component, different contexts */
.component-container {
  container: component / inline-size;
}

.component {
  /* Base: Works everywhere */
  padding: var(--space-s);
  font-size: var(--step-0);
}

/* In sidebar (narrow) */
@container component (inline-size < 400px) {
  .component {
    /* Compact vertical layout */
    display: flex;
    flex-direction: column;
    gap: var(--space-2xs);
  }
}

/* In main content (wide) */
@container component (inline-size >= 400px) {
  .component {
    /* Spacious horizontal layout */
    display: grid;
    grid-template-columns: auto 1fr;
    gap: clamp(var(--space-s), 2cqi, var(--space-m));
  }
}
```

## Integration with Other Skills

**Prerequisites:**
- Use `utopia-fluid-scales` first to generate type and space scales
- Use `utopia-grid-layout` for page-level layouts with fluid gaps

**Workflow:**
1. Generate Utopia scales (`utopia-fluid-scales`)
2. Implement page layouts with Grid/Flex (`utopia-grid-layout`)
3. Add container queries for component adaptation (`utopia-container-queries`)

**Result**: Complete Utopia-aligned responsive system with layered fluidity:
- **Viewport-based**: Global Utopia scales
- **Layout-based**: Grid/Flex with fluid gaps
- **Component-based**: Container queries with cqi units

## Resources

- **MDN Container Queries**: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries
- **Chrome Guide**: https://developer.chrome.com/blog/cq-polyfill
- **Container Query Units**: https://developer.mozilla.org/en-US/docs/Web/CSS/length#container_query_length_units
- **Modern CSS Solutions**: https://moderncss.dev/container-query-units-and-fluid-typography/
- **Can I Use**: https://caniuse.com/css-container-queries

## Next Steps

After implementing container queries:
1. Test components in multiple contexts (sidebar, main, grid cells)
2. Verify browser zoom works correctly (200% test)
3. Ensure accessibility with min/max bounds using Utopia steps
4. Document container query breakpoints for team reference
5. Build component library with container-aware components
6. Integrate with design system using Utopia shared vocabulary
