---
name: utopia-fluid-scales
description: Utopia.fyi fluid typography and spacing system using clamp(), modular scales, and proportional design. Use when implementing fluid type scales, space palettes, t-shirt sizing, space pairs, or creating fluid responsive designs without breakpoints. Foundation for systematic, proportional scaling across all viewports.
allowed-tools: Read, Write, Edit, Bash
---

# Utopia Fluid Scales

*Systematic fluid typography and spacing using Utopia.fyi philosophy*

## Core Philosophy

Utopia represents a **declarative design approach** where you establish foundational rules at two poles (@min and @max viewports) and let the browser interpolate fluidly between them. This eliminates arbitrary breakpoints in favor of **proportional, mathematical harmony**.

### The Three-Step Process

1. Define type and space scales for minimum viewport (e.g., 320px)
2. Define type and space scales for maximum viewport (e.g., 1500px)
3. Browser automatically interpolates between these scales using CSS `clamp()`

**Key Insight**: You're not designing for specific devices—you're establishing a **proportional system that scales gracefully** across all viewport widths.

## When to Use This Skill

- Implementing fluid typography that scales without breakpoints
- Creating systematic space palettes with t-shirt sizing
- Establishing design-development shared vocabulary
- Building fluid responsive designs aligned with Utopia philosophy
- Generating type and space scales using Utopia calculators
- Replacing breakpoint-heavy media queries with fluid scales
- Ensuring proportional harmony across typography and spacing

## Fluid Type Scales

### Modular Scale Approach

Rather than arbitrary font sizes at breakpoints, Utopia uses **modular scales**—mathematical ratios applied repeatedly to create harmonious typography.

#### Common Scale Ratios

- `1.2` - Minor Third (subtle scaling)
- `1.25` - Major Third (balanced, recommended)
- `1.333` - Perfect Fourth (common choice)
- `1.5` - Perfect Fifth (dramatic)
- `1.618` - Golden Ratio (natural harmony)

### Type Scale Configuration

**Define @min viewport (e.g., 320px):**
- Base size: 16px
- Scale ratio: 1.2 (Minor Third)

**Define @max viewport (e.g., 1500px):**
- Base size: 20px
- Scale ratio: 1.25 (Major Third)

**Generated Scale:**
```
Step -2: 11px → 13px
Step -1: 13px → 16px
Step 0:  16px → 20px (body text)
Step 1:  19px → 25px
Step 2:  23px → 31px
Step 3:  28px → 39px
Step 4:  34px → 49px
Step 5:  40px → 61px
```

### CSS Implementation

```css
:root {
  /* Fluid type scale using clamp() */
  --step--2: clamp(0.6944rem, 0.6578rem + 0.1831vi, 0.8rem);
  --step--1: clamp(0.8333rem, 0.7813rem + 0.2604vi, 1rem);
  --step-0: clamp(1rem, 0.9286rem + 0.3571vi, 1.25rem);
  --step-1: clamp(1.2rem, 1.1036rem + 0.4821vi, 1.5625rem);
  --step-2: clamp(1.44rem, 1.3113rem + 0.6435vi, 1.9531rem);
  --step-3: clamp(1.728rem, 1.5585rem + 0.8476vi, 2.4414rem);
  --step-4: clamp(2.0736rem, 1.8517rem + 1.1094vi, 3.0518rem);
  --step-5: clamp(2.4883rem, 2.2008rem + 1.4372vi, 3.8147rem);
}

/* Usage - semantic, not arbitrary */
h1 { font-size: var(--step-5); }
h2 { font-size: var(--step-4); }
h3 { font-size: var(--step-3); }
h4 { font-size: var(--step-2); }
h5 { font-size: var(--step-1); }
body { font-size: var(--step-0); }
small { font-size: var(--step--1); }
.caption { font-size: var(--step--2); }
```

### clamp() Formula Breakdown

```css
clamp(MIN, PREFERRED, MAX)
```

**Example:**
```css
--step-0: clamp(1rem, 0.9286rem + 0.3571vi, 1.25rem);
```

- **MIN**: `1rem` - Smallest value (at @min viewport)
- **PREFERRED**: `0.9286rem + 0.3571vi` - Fluid calculation
- **MAX**: `1.25rem` - Largest value (at @max viewport)

**Preferred Calculation:**
```
base + (slope × viewport-inline-size)
```

Where `vi` = 1% of viewport inline size (horizontal in LTR languages)

### Utopia Type Calculator

**URL**: https://utopia.fyi/type/calculator/

**Inputs:**
- Min viewport width (px)
- Min font size (px)
- Min type scale ratio
- Max viewport width (px)
- Max font size (px)
- Max type scale ratio
- Number of positive/negative steps

**Output**: Production-ready CSS custom properties using `clamp()`

**Workflow:**
1. Define @min and @max parameters
2. Choose scale ratios
3. Generate CSS
4. Copy to `:root` selector
5. Use semantic step names in components

## Fluid Space Palette

### T-Shirt Sizing System

Utopia applies the same fluid logic to spacing, using multipliers derived from body font size (--step-0).

#### Space Scale Structure

```
3XS: 0.25rem → 0.3125rem
2XS: 0.5rem → 0.625rem
XS:  0.75rem → 0.9375rem
S:   1rem → 1.25rem
M:   1.5rem → 1.875rem
L:   2rem → 2.5rem
XL:  3rem → 3.75rem
2XL: 4rem → 5rem
3XL: 6rem → 7.5rem
```

### Individual Space Values

```css
:root {
  /* Single-value space tokens */
  --space-3xs: clamp(0.25rem, 0.2321rem + 0.0893vi, 0.3125rem);
  --space-2xs: clamp(0.5rem, 0.4643rem + 0.1786vi, 0.625rem);
  --space-xs: clamp(0.75rem, 0.6964rem + 0.2679vi, 0.9375rem);
  --space-s: clamp(1rem, 0.9286rem + 0.3571vi, 1.25rem);
  --space-m: clamp(1.5rem, 1.3929rem + 0.5357vi, 1.875rem);
  --space-l: clamp(2rem, 1.8571rem + 0.7143vi, 2.5rem);
  --space-xl: clamp(3rem, 2.7857rem + 1.0714vi, 3.75rem);
  --space-2xl: clamp(4rem, 3.7143rem + 1.4286vi, 5rem);
  --space-3xl: clamp(6rem, 5.5714rem + 2.1429vi, 7.5rem);
}

/* Usage */
.card {
  padding: var(--space-m);
  gap: var(--space-xs);
}

.section {
  padding-block: var(--space-2xl);
}

.button {
  padding: var(--space-2xs) var(--space-s);
}
```

### Space Pairs (Dramatic Scaling)

For more dramatic fluid changes, Utopia provides **space pairs** that interpolate between two different space values.

```css
:root {
  /* S-M: 16px → 30px (more dramatic than either alone) */
  --space-s-m: clamp(1rem, 0.7143rem + 1.4286vi, 1.875rem);

  /* M-L: 24px → 40px */
  --space-m-l: clamp(1.5rem, 1.1786rem + 1.6071vi, 2.5rem);

  /* L-XL: 32px → 60px */
  --space-l-xl: clamp(2rem, 1.4286rem + 2.8571vi, 3.75rem);

  /* XL-2XL: 48px → 80px */
  --space-xl-2xl: clamp(3rem, 2.1429rem + 4.2857vi, 5rem);

  /* 2XL-3XL: 64px → 120px (very dramatic) */
  --space-2xl-3xl: clamp(4rem, 2.8571rem + 5.7143vi, 7.5rem);
}

/* Usage - Components "breathe" dramatically */
.hero {
  padding-block: var(--space-xl-2xl); /* 48px → 80px */
}

.section {
  padding-block: var(--space-m-l); /* 24px → 40px */
  gap: var(--space-s-m); /* 16px → 30px */
}

.card {
  padding: var(--space-s-m);
  gap: var(--space-xs); /* Subtle scaling */
}

.article {
  /* Combine pairs for hierarchical spacing */
  margin-block-start: var(--space-l-xl);
  margin-block-end: var(--space-m-l);
}
```

**When to Use Space Pairs:**
- Hero sections requiring dramatic spacing changes
- Section padding that needs proportional scaling
- Component spacing that should expand significantly on larger screens
- Creating visual hierarchy with intentional spacing variance

### Utopia Space Calculator

**URL**: https://utopia.fyi/space/calculator/

**Inputs:**
- Min viewport width (px)
- Max viewport width (px)
- Min base size (px) - typically matches type scale --step-0 min
- Max base size (px) - typically matches type scale --step-0 max
- Space pair selections (custom combinations)

**Output**: Individual space tokens + space pairs as CSS custom properties

**Workflow:**
1. Use same viewport widths as type scale
2. Match base sizes to --step-0 for consistency
3. Select space pairs for dramatic scaling
4. Generate CSS
5. Copy to `:root` alongside type scale

## Design-Development Alignment

### Shared Vocabulary

**Designers specify:**
- "Use Step 3 for main headings"
- "Apply L-XL space between sections"
- "Card padding is M"

**Developers implement:**
```css
.main-heading { font-size: var(--step-3); }
.section { padding-block: var(--space-l-xl); }
.card { padding: var(--space-m); }
```

**Result**: Both reference the same systematic scale, eliminating translation errors.

### Benefits Over Traditional Approach

**Traditional (breakpoint-heavy):**
```css
.heading {
  font-size: 1.5rem;
}
@media (min-width: 640px) {
  .heading { font-size: 2rem; }
}
@media (min-width: 1024px) {
  .heading { font-size: 2.5rem; }
}
@media (min-width: 1280px) {
  .heading { font-size: 3rem; }
}
```

**Utopia (single declaration):**
```css
.heading {
  font-size: var(--step-3); /* Scales automatically */
}
```

**Advantages:**
1. **Minimal Code** - Single declaration vs. multiple breakpoints
2. **Proportional Scaling** - Maintains mathematical relationships
3. **Fluid Transitions** - Smooth scaling, not jumps
4. **Systematic** - All values derive from intentional scales
5. **Maintainable** - Change scale ratios centrally

## Proportional Harmony

All spacing and typography decisions derive from the same mathematical foundation:

```css
.component {
  /* All values maintain proportional relationships */
  font-size: var(--step-2);        /* Scales proportionally */
  line-height: 1.5;                /* Unitless multiplier */
  padding: var(--space-m);         /* Scales with type */
  gap: var(--space-xs);            /* Maintains relationship */
  margin-block: var(--space-s-m);  /* Dramatic scaling */
}

.component__title {
  font-size: var(--step-4);        /* Larger than body */
  margin-bottom: var(--space-2xs); /* Proportional to title size */
}

.component__meta {
  font-size: var(--step--1);       /* Smaller than body */
  margin-top: var(--space-3xs);    /* Proportional to meta size */
}
```

**Key Principle**: Every spacing and typography decision maintains intentional mathematical relationships rather than arbitrary pixel values.

## Implementation Workflow

### Step 1: Generate Type Scale

1. Visit https://utopia.fyi/type/calculator/
2. Configure @min viewport and font size
3. Choose @min scale ratio (e.g., 1.2)
4. Configure @max viewport and font size
5. Choose @max scale ratio (e.g., 1.25)
6. Set positive and negative steps
7. Copy generated CSS

### Step 2: Generate Space Scale

1. Visit https://utopia.fyi/space/calculator/
2. Use same viewport widths as type scale
3. Match base sizes to type scale --step-0
4. Select space pairs (S-M, M-L, L-XL, etc.)
5. Copy generated CSS

### Step 3: Combine in :root

```css
:root {
  /* Type Scale */
  --step--2: clamp(0.6944rem, 0.6578rem + 0.1831vi, 0.8rem);
  --step--1: clamp(0.8333rem, 0.7813rem + 0.2604vi, 1rem);
  --step-0: clamp(1rem, 0.9286rem + 0.3571vi, 1.25rem);
  --step-1: clamp(1.2rem, 1.1036rem + 0.4821vi, 1.5625rem);
  --step-2: clamp(1.44rem, 1.3113rem + 0.6435vi, 1.9531rem);
  --step-3: clamp(1.728rem, 1.5585rem + 0.8476vi, 2.4414rem);
  --step-4: clamp(2.0736rem, 1.8517rem + 1.1094vi, 3.0518rem);
  --step-5: clamp(2.4883rem, 2.2008rem + 1.4372vi, 3.8147rem);

  /* Space Scale - Individual Values */
  --space-3xs: clamp(0.25rem, 0.2321rem + 0.0893vi, 0.3125rem);
  --space-2xs: clamp(0.5rem, 0.4643rem + 0.1786vi, 0.625rem);
  --space-xs: clamp(0.75rem, 0.6964rem + 0.2679vi, 0.9375rem);
  --space-s: clamp(1rem, 0.9286rem + 0.3571vi, 1.25rem);
  --space-m: clamp(1.5rem, 1.3929rem + 0.5357vi, 1.875rem);
  --space-l: clamp(2rem, 1.8571rem + 0.7143vi, 2.5rem);
  --space-xl: clamp(3rem, 2.7857rem + 1.0714vi, 3.75rem);
  --space-2xl: clamp(4rem, 3.7143rem + 1.4286vi, 5rem);
  --space-3xl: clamp(6rem, 5.5714rem + 2.1429vi, 7.5rem);

  /* Space Scale - Pairs */
  --space-s-m: clamp(1rem, 0.7143rem + 1.4286vi, 1.875rem);
  --space-m-l: clamp(1.5rem, 1.1786rem + 1.6071vi, 2.5rem);
  --space-l-xl: clamp(2rem, 1.4286rem + 2.8571vi, 3.75rem);
  --space-xl-2xl: clamp(3rem, 2.1429rem + 4.2857vi, 5rem);
  --space-2xl-3xl: clamp(4rem, 2.8571rem + 5.7143vi, 7.5rem);
}
```

### Step 4: Apply Semantically

```css
/* Typography */
h1 { font-size: var(--step-5); }
h2 { font-size: var(--step-4); }
h3 { font-size: var(--step-3); }
body { font-size: var(--step-0); }

/* Spacing */
.hero { padding-block: var(--space-xl-2xl); }
.section { padding-block: var(--space-m-l); }
.card { padding: var(--space-m); gap: var(--space-s); }
.button { padding: var(--space-2xs) var(--space-s); }
```

## Integration with Framework/Utility CSS

### Tailwind CSS

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      fontSize: {
        'step--2': 'var(--step--2)',
        'step--1': 'var(--step--1)',
        'step-0': 'var(--step-0)',
        'step-1': 'var(--step-1)',
        'step-2': 'var(--step-2)',
        'step-3': 'var(--step-3)',
        'step-4': 'var(--step-4)',
        'step-5': 'var(--step-5)',
      },
      spacing: {
        '3xs': 'var(--space-3xs)',
        '2xs': 'var(--space-2xs)',
        'xs': 'var(--space-xs)',
        's': 'var(--space-s)',
        'm': 'var(--space-m)',
        'l': 'var(--space-l)',
        'xl': 'var(--space-xl)',
        '2xl': 'var(--space-2xl)',
        '3xl': 'var(--space-3xl)',
        's-m': 'var(--space-s-m)',
        'm-l': 'var(--space-m-l)',
        'l-xl': 'var(--space-l-xl)',
        'xl-2xl': 'var(--space-xl-2xl)',
      }
    }
  }
}
```

**Usage:**
```html
<h1 class="text-step-5">Main Heading</h1>
<section class="py-xl-2xl">
  <div class="card p-m gap-s">
    <h2 class="text-step-3">Card Title</h2>
    <p class="text-step-0">Body text</p>
  </div>
</section>
```

## Best Practices

1. **Start with Body Text** - --step-0 is the heart of the system; all else orbits around it
2. **Match @min and @max Intentionally** - These aren't device sizes; they're design poles
3. **Use Modular Ratios** - 1.25 (Major Third) is balanced for most use cases
4. **Maintain Relationships** - Space values should derive from type scale base
5. **Test Across Range** - View designs at @min, @max, and midpoints
6. **Prefer Semantic Names** - Use step names, not arbitrary values
7. **Document Decisions** - Save calculator URLs for future adjustments
8. **Limit Steps** - 3-5 positive steps usually sufficient for most designs
9. **Use Space Pairs Intentionally** - For dramatic scaling, not default spacing
10. **Combine with Container Queries** - Use with `utopia-container-queries` skill for component-level fluidity

## Common Patterns

### Article Typography
```css
.article {
  font-size: var(--step-0);
  line-height: 1.6;
  max-width: 70ch;
}

.article h1 {
  font-size: var(--step-4);
  margin-block: var(--space-l-xl) var(--space-m);
}

.article h2 {
  font-size: var(--step-3);
  margin-block: var(--space-l) var(--space-s);
}

.article p + p {
  margin-block-start: var(--space-m);
}
```

### Card Component
```css
.card {
  padding: var(--space-s-m);
  gap: var(--space-s);
  border-radius: 0.5rem;
}

.card__title {
  font-size: var(--step-2);
  margin-bottom: var(--space-2xs);
}

.card__meta {
  font-size: var(--step--1);
  color: var(--color-muted);
}
```

### Hero Section
```css
.hero {
  padding-block: var(--space-2xl-3xl);
  text-align: center;
}

.hero__title {
  font-size: var(--step-5);
  margin-bottom: var(--space-m);
}

.hero__subtitle {
  font-size: var(--step-1);
  margin-bottom: var(--space-l);
}
```

## Resources

- **Utopia Homepage**: https://utopia.fyi/
- **Type Calculator**: https://utopia.fyi/type/calculator/
- **Space Calculator**: https://utopia.fyi/space/calculator/
- **Blog**: https://utopia.fyi/blog/
- **Smashing Magazine Guide**: https://www.smashingmagazine.com/2021/04/designing-developing-fluid-type-space-scales/

## Next Steps

After implementing fluid scales:
1. Use `utopia-grid-layout` skill for Grid/Flexbox/Subgrid with fluid gaps
2. Use `utopia-container-queries` skill for component-level container queries with container units
3. Combine all three for comprehensive Utopia-aligned fluid design system
