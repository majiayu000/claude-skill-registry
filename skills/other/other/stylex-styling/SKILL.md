---
name: stylex-styling
description: StyleX styling patterns using design tokens, breakpoints, and custom css prop. Use when working with styles, CSS, design tokens, breakpoints, responsive design, themes, styling components, css prop, stylex.create, or when the user mentions StyleX, tokens.stylex, controlSize, color tokens, or breakpoints.
---

# StyleX Styling

## Overview

This project uses StyleX for styling with design tokens, responsive breakpoints, and theme-aware colors.

## Key Patterns

### Design Tokens

- **Import tokens from**: `@/tokens.stylex.ts`
- **Available token categories**:
  - `color` - Theme-aware colors (textMain, backgroundRaised, controlActive, etc.)
  - `controlSize` - Spacing and sizing values (\_1 through \_9)
  - `font` - Typography values (weight_5, etc.)

### Breakpoints

- **Import from**: `@/breakpoints`
- **Defined via**: Babel plugin in `.babelrc.js` with typing in `src/babel.d.ts`
- **Usage**: `{ default: value, [breakpoints.md]: largeScreenValue }`

### Custom CSS Prop

- Use `css={styles.someStyle}` prop instead of `{...stylex.props(styles.someStyle)}`
- Transpiled by custom Babel plugin
- Supports arrays: `css={[styles.base, isActive && styles.active]}`

## Complete Example

```tsx
import * as stylex from "@stylexjs/stylex";
import { breakpoints } from "@/breakpoints";
import { color, controlSize, font } from "@/tokens.stylex";

function Button({ children, isActive, hideLabelOnMobile, ...props }) {
  return (
    <button
      {...props}
      css={[
        styles.button,
        isActive && styles.active,
        hideLabelOnMobile && styles.hideLabelOnMobile,
      ]}
    >
      {children}
    </button>
  );
}

const styles = stylex.create({
  button: {
    // Use design tokens
    fontSize: controlSize._4,
    fontWeight: font.weight_5,
    minHeight: controlSize._9,
    paddingBlock: controlSize._1,
    paddingInline: controlSize._3,

    // Responsive design with breakpoints
    display: { default: "none", [breakpoints.md]: "inline-flex" },

    // Theme-aware colors
    color: color.textMain,
    backgroundColor: {
      default: color.backgroundRaised,
      ":hover": color.backgroundHover,
    },
  },
  active: {
    backgroundColor: color.controlActive,
    color: color.textOnActive,
  },
  hideLabelOnMobile: {
    paddingLeft: {
      default: controlSize._3,
      [breakpoints.md]: controlSize._2,
    },
  },
});
```

## Best Practices

1. **Always use design tokens** - Never hardcode colors, spacing, or font values
2. **Use the css prop** - Don't use `{...stylex.props()}` directly
3. **Conditional styles with arrays** - `css={[base, condition && conditional]}`
4. **Responsive by default** - Consider mobile-first with breakpoint overrides
5. **Theme-aware colors** - Use color tokens that adapt to light/dark themes
6. **Pseudo-selectors in objects** - `{ default: value, ":hover": hoverValue }`

## Common Patterns

### Responsive Display

```tsx
display: { default: "none", [breakpoints.md]: "flex" }
```

### Conditional Styles

```tsx
css={[styles.base, isActive && styles.active, hasError && styles.error]}
```

### Hover States

```tsx
backgroundColor: {
  default: color.backgroundRaised,
  ":hover": color.backgroundHover,
}
```

### Mobile-First Padding

```tsx
padding: {
  default: controlSize._2,
  [breakpoints.md]: controlSize._4,
  [breakpoints.lg]: controlSize._6,
}
```
