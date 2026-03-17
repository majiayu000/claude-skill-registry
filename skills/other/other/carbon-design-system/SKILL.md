---
name: carbon-design-system
description: Build UIs using IBM's Carbon Design System. Use when the user requests Carbon-styled interfaces, IBM-style dashboards, enterprise UIs following Carbon conventions, or explicitly mentions Carbon, IBM design, or @carbon/react. Covers component usage, design tokens (color, typography, spacing, motion), theming (White, Gray 10, Gray 90, Gray 100), grid layout, and accessibility. Supports both artifact/HTML output (CDN-based) and full React project output (@carbon/react). Triggers include "Carbon", "IBM design system", "enterprise dashboard", "@carbon/react", "carbon components", or requests for IBM-style professional interfaces.
---

# Carbon Design System

Build UIs conforming to IBM's Carbon Design System v11. Carbon provides a token-based, accessible, enterprise-grade component library.

## Rendering Context

Determine the output target before writing code.

### HTML Artifacts (no build pipeline)

Use pre-built CSS via CDN. Add to `<head>`:

```html
<link rel="stylesheet" href="https://unpkg.com/@carbon/styles/css/styles.css" />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;600&family=IBM+Plex+Mono:wght@400;600&display=swap" />
```

Apply Carbon classes to HTML elements. See `references/html-classes.md`.

### React Artifacts

`@carbon/react` is not in Claude's default artifact environment. For React artifacts, load the CDN CSS above and apply Carbon class names to standard HTML/JSX elements. The visual output is identical.

### Full Projects (file creation)

```bash
npm install @carbon/react sass
```

```jsx
import { Button } from '@carbon/react';
// Styles: @use '@carbon/react'; in root SCSS
```

Requires Dart Sass. All styles, components, icons ship in the single `@carbon/react` package.

## Design Foundations

### Typography

Always use **IBM Plex**. Never substitute.

| Role | Family | Weights |
|------|--------|---------|
| Body, UI | IBM Plex Sans | 300, 400, 600 |
| Code | IBM Plex Mono | 400, 600 |
| Editorial | IBM Plex Serif | 300, 400, 600 |

### Color Themes

| Theme | Background | Context |
|-------|-----------|---------|
| White | `#ffffff` | Default light |
| g10 | `#f4f4f4` | Subtle light |
| g90 | `#262626` | Dark |
| g100 | `#161616` | High-contrast dark |

Primary action: Blue 60 `#0f62fe`. See `references/tokens.md` for full palette.

### Spacing

8px base grid, 2px mini-unit. Component spacing: 2, 4, 8, 12, 16, 24, 32, 40, 48 px. Layout spacing: 16, 24, 32, 48, 64, 96, 160 px.

### 2x Grid

| Breakpoint | Width | Columns | Margin |
|-----------|-------|---------|--------|
| sm | 320px | 4 | 0 |
| md | 672px | 8 | 16px |
| lg | 1056px | 16 | 16px |
| xlg | 1312px | 16 | 16px |
| max | 1584px | 16 | 24px |

Grid classes: `cds--grid`, `cds--row`, `cds--col`, `cds--col-sm-N`, `cds--col-md-N`, `cds--col-lg-N`.

### Motion

| Token | Duration | Use |
|-------|----------|-----|
| fast-01 | 70ms | Micro-interactions |
| fast-02 | 110ms | Toggle, expand |
| moderate-01 | 150ms | Buttons, fields |
| moderate-02 | 240ms | Modal, dropdown |
| slow-01 | 400ms | Page transitions |
| slow-02 | 700ms | Complex choreography |

Standard easing: `cubic-bezier(0.2, 0, 0.38, 0.9)`. Entrance: `cubic-bezier(0, 0, 0.38, 0.9)`. Exit: `cubic-bezier(0.2, 0, 1, 0.9)`.

## References

- **Component HTML classes and usage**: `references/html-classes.md`
- **Full design token values**: `references/tokens.md`

Read the appropriate reference when building specific components or when exact token values are needed.

## Implementation Checklist

1. IBM Plex loaded (Sans minimum; Mono for code)
2. Theme class applied: `cds--white`, `cds--g10`, `cds--g90`, or `cds--g100`
3. Correct prefix: `cds--` (v11). Never `bx--` (v10 legacy)
4. Grid layout: `cds--grid` > `cds--row` > `cds--col-*`
5. Spacing from scale only — no arbitrary pixel values
6. Focus states preserved — 2px blue outline
7. Color by role via tokens, not raw hex
8. Icons at Carbon sizes: 16, 20, 24, 32px

## Common Patterns

### Page Shell

```html
<div class="cds--white" style="min-height:100vh">
  <header class="cds--header" role="banner">
    <a class="cds--header__name" href="#">[App Name]</a>
  </header>
  <div class="cds--grid" style="padding-top:3rem">
    <div class="cds--row">
      <div class="cds--col-lg-3"><!-- Side nav --></div>
      <div class="cds--col-lg-13"><!-- Content --></div>
    </div>
  </div>
</div>
```

### Theme Nesting

```html
<div class="cds--g100"><!-- dark header --></div>
<div class="cds--white"><!-- light body --></div>
```

### Data Dashboard

Combine `cds--tile` containers for metric cards with `cds--data-table` for tabular data, all within the 2x grid.

## Anti-Patterns

- Non-IBM Plex fonts
- `bx--` prefix (v10; use `cds--` for v11)
- Arbitrary border-radius (Carbon: 0px default, 4px for tags/pills only)
- Drop shadows on components that lack them in spec
- Overriding focus ring styles
- Colors outside the Carbon palette
- Spacing values not on the scale
