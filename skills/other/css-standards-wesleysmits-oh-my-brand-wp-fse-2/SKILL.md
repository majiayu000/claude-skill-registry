---
name: css-standards
description: CSS coding standards for Oh My Brand! theme. BEM methodology, custom properties, theme.json integration, responsive design, and accessibility. Use when styling blocks, templates or components.
metadata:
  author: Wesley Smits
  version: "1.0.0"
---

# CSS Standards

CSS coding standards and patterns for the Oh My Brand! WordPress FSE theme.

---

## When to Use

- Styling block components
- Writing responsive layouts
- Defining CSS custom properties
- Implementing accessible focus states
- Working with WordPress design tokens

---

## Reference Files

| File | Purpose |
|------|---------|
| [gallery-block.css](references/gallery-block.css) | Complete block styling example |
| [theme-json-tokens.css](references/theme-json-tokens.css) | WordPress design token usage |
| [accessibility.css](references/accessibility.css) | Focus, reduced motion, contrast |

---

## BEM Naming

BEM (Block, Element, Modifier) naming convention:

```
.block                    → Component container
.block__element           → Child element
.block--modifier          → Block variation
.block__element--modifier → Element variation
```

### Block Class Prefix

| Block Type | Prefix | Example |
|------------|--------|---------|
| Native blocks | `wp-block-theme-oh-my-brand-` | `.wp-block-theme-oh-my-brand-gallery` |
| ACF blocks | `wp-block-acf-` | `.wp-block-acf-gallery` |

### BEM Examples

```css
/* Block */
.wp-block-theme-oh-my-brand-gallery { }

/* Elements */
.wp-block-theme-oh-my-brand-gallery__track { }
.wp-block-theme-oh-my-brand-gallery__slide { }
.wp-block-theme-oh-my-brand-gallery__button { }

/* Block modifiers */
.wp-block-theme-oh-my-brand-gallery--fullwidth { }

/* Element modifiers */
.wp-block-theme-oh-my-brand-gallery__button--prev { }
.wp-block-theme-oh-my-brand-gallery__slide--active { }
```

---

## Custom Properties

Define custom properties at the block root:

```css
.wp-block-theme-oh-my-brand-gallery {
    /* Layout */
    --visible-images: 3;
    --block-gap: 1rem;

    /* Animation */
    --transition-duration: 300ms;
    --transition-timing: ease-out;

    /* Colors (use theme tokens) */
    --button-bg: var(--wp--preset--color--primary);
    --button-text: var(--wp--preset--color--base);
}
```

See [gallery-block.css](references/gallery-block.css) for complete example.

---

## Theme.json Tokens

Use WordPress design tokens from `theme.json`:

| Token Type | CSS Variable Pattern |
|------------|---------------------|
| Colors | `var(--wp--preset--color--{slug})` |
| Spacing | `var(--wp--preset--spacing--{size})` |
| Font Family | `var(--wp--preset--font-family--{slug})` |
| Font Size | `var(--wp--preset--font-size--{slug})` |
| Layout | `var(--wp--style--global--content-size)` |

See [theme-json-tokens.css](references/theme-json-tokens.css) for examples.

---

## Responsive Design

Mobile-first approach using `min-width` breakpoints:

| Name | Width | Target |
|------|-------|--------|
| Mobile | < 768px | Phones (base styles) |
| Tablet | ≥ 768px | Tablets |
| Desktop | ≥ 1024px | Laptops |
| Large | ≥ 1280px | Desktops |

### Example

```css
/* Base (mobile) styles */
.wp-block-theme-oh-my-brand-gallery {
    grid-template-columns: 1fr;
}

/* Tablet */
@media (min-width: 768px) {
    .wp-block-theme-oh-my-brand-gallery {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* Desktop */
@media (min-width: 1024px) {
    .wp-block-theme-oh-my-brand-gallery {
        grid-template-columns: repeat(3, 1fr);
    }
}
```

---

## Accessibility

### Focus Styles

```css
.wp-block-theme-oh-my-brand-gallery__button:focus-visible {
    outline: 2px solid var(--wp--preset--color--primary);
    outline-offset: 2px;
}
```

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
    .wp-block-theme-oh-my-brand-gallery__track {
        transition: none;
    }
}
```

### Screen Reader Only

```css
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}
```

See [accessibility.css](references/accessibility.css) for complete patterns.

### Color Contrast (WCAG 2.1 AA)

| Content Type | Minimum Ratio |
|--------------|---------------|
| Normal text | 4.5:1 |
| Large text (18px+ bold, 24px+) | 3:1 |
| UI components | 3:1 |

---

## Stylelint Rules

This project uses Stylelint for CSS linting. Key rules to follow:

### No Empty Blocks

Stylelint disallows empty rule blocks. Never create a rule with only a comment:

```css
/* ❌ Bad - empty block causes stylelint error */
@media (prefers-reduced-motion: reduce) {
    .my-component {
        /* No styles needed */
    }
}

/* ❌ Bad - empty block */
.my-component__element {
}

/* ✅ Good - omit the rule entirely if no styles needed */
/* (Simply don't include the rule) */

/* ✅ Good - if you need the media query, include actual styles */
@media (prefers-reduced-motion: reduce) {
    .my-component {
        transition: none;
        animation: none;
    }
}
```

### No Duplicate Selectors

Stylelint disallows duplicate selectors within a stylesheet. Consolidate all styles for a selector in one place:

```css
/* ❌ Bad - duplicate selector causes stylelint error */
.my-component__number {
    font-size: 2rem;
    font-weight: 700;
}

.my-component__label {
    font-size: 1rem;
}

.my-component__number {
    order: 0;  /* This duplicates the selector above! */
}

/* ✅ Good - all styles consolidated in one selector */
.my-component__number {
    font-size: 2rem;
    font-weight: 700;
    order: 0;
}

.my-component__label {
    font-size: 1rem;
}
```

### Hex Color Length

Use shorthand hex colors when possible:

```css
/* ❌ Bad - can be shortened */
color: #0066cc;
background: #ffffff;

/* ✅ Good - use shorthand */
color: #06c;
background: #fff;
```

### Key Principles

1. If a rule block would be empty (even with just a comment), **do not include it**
2. Consolidate all styles for a selector in **one place** - no duplicate selectors
3. Use **shorthand hex colors** when all pairs are identical (e.g., `#aabbcc` → `#abc`)

---

## Validation

**Always run stylelint after making CSS changes:**

```bash
pnpm run lint:css
```

Fix any issues before committing. This ensures consistent code style and catches common errors.

---

## Related Skills

- [html-standards](../html-standards/SKILL.md) - Semantic HTML structure
- [web-components](../web-components/SKILL.md) - Frontend Web Components
- [native-block-development](../native-block-development/SKILL.md) - Block styling

---

## References

- [BEM Methodology](https://getbem.com/)
- [WordPress Global Styles](https://developer.wordpress.org/themes/global-settings-and-styles/)
- [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
- [CSS Custom Properties](https://css-tricks.com/a-complete-guide-to-custom-properties/)
