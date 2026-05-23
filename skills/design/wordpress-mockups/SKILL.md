# WordPress Mockups Skill

Build accurate WordPress/Gutenberg UI mockups using pre-extracted design tokens, icons, and components.

## When to Use

Use this skill when building HTML/CSS mockups of WordPress admin UI, the Site Editor, or any Gutenberg-based interface.

## Directory Structure

```
skill/
├── SKILL.md                    # This file
├── base.css                    # Reset + base typography
├── tokens/
│   ├── TOKENS.md               # Token documentation
│   └── wordpress-tokens.css    # CSS custom properties
├── icons/
│   ├── ICONS.md                # Icon documentation + full list
│   └── svg/                    # 321 SVG icon files
├── components/
│   ├── COMPONENTS.md           # Component documentation
│   └── *.html                  # 12 component files
└── patterns/
    ├── PATTERNS.md             # Pattern documentation + composition rules
    └── *.html                  # Layout patterns (Site Editor header, etc.)
```

## Workflow

### 0. Check for Patterns First

Before building from scratch, check `patterns/` for a pre-built layout:

- Building a Site Editor mockup? Start with `patterns/site-editor-header.html`
- Building a modal? Start with `components/modal.html`

**Patterns > Components > Custom CSS**

Patterns are complete, correct layouts. Components are building blocks. Only write custom CSS for things not covered by either.

### 1. Start a New Mockup

Create an HTML file with the basic structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mockup Name</title>
  <style>
    /* Paste tokens, base, and component CSS here */
  </style>
</head>
<body>
  <!-- Mockup content -->
</body>
</html>
```

### 2. Add Design Tokens

Copy the contents of `tokens/wordpress-tokens.css` into your `<style>` block. This gives you all the CSS custom properties:

- Colors: `var(--wp-gray-900)`, `var(--wp-admin-theme-color)`
- Spacing: `var(--wp-grid-unit-20)`, `var(--wp-grid-unit-05)`
- Typography: `var(--wp-font-size-medium)`, `var(--wp-font-weight-medium)`
- Dimensions: `var(--wp-button-size)`, `var(--wp-header-height)`
- Shadows: `var(--wp-elevation-medium)`
- Radii: `var(--wp-radius-small)`

### 3. Add Base Styles

Copy the contents of `base.css` after the tokens. This sets up:

- Box-sizing reset
- Default font family and size
- Focus styles
- Link styles

### 4. Add Components

For each UI element you need:

1. Open the relevant component file (e.g., `components/button.html`)
2. Copy the CSS from the `<style>` block
3. Copy the HTML markup you need from the examples
4. Customize the content

### 5. Add Icons

To include an icon:

1. Check `icons/ICONS.md` for the icon name
2. Read the SVG: `cat skill/icons/svg/{name}.svg`
3. Paste the SVG inline in your markup

Example:
```html
<button class="components-button has-icon" aria-label="Settings">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
    <path d="..."/>
  </svg>
</button>
```

### 6. Build Layout

Compose components into your mockup layout. Add custom CSS for:

- Page structure
- Component arrangement
- Mockup-specific styling

## Key References

### Patterns
- See `patterns/PATTERNS.md` for available layouts and **composition rules**
- Composition rules tell you how WordPress UIs are assembled (what goes where, which buttons are primary, etc.)
- **Always check patterns before building a layout from scratch**

### Tokens
- See `tokens/TOKENS.md` for where values come from
- All spacing is based on 8px grid (`--wp-grid-unit`)
- Use `--wp-admin-theme-color` for accent/interactive elements

### Icons
- 321 icons available in `icons/svg/`
- All use `viewBox="0 0 24 24"`
- Add `fill="currentColor"` to inherit text color

### Components
- See `components/COMPONENTS.md` for available components
- Class naming: `.components-{name}`, `.components-{name}__{element}`
- Modifiers: `.is-primary`, `.is-compact`, `.is-pressed`, etc.

## Common Patterns

### Button with Icon
```html
<button class="components-button has-icon has-text">
  <svg>...</svg>
  Button Text
</button>
```

### Input with Label
```html
<div class="components-input-control">
  <label class="components-input-control__label">Label</label>
  <div class="components-input-control__container">
    <input type="text" class="components-input-control__input">
    <div class="components-input-control__backdrop"></div>
  </div>
</div>
```

### Collapsible Panel
```html
<div class="components-panel__body is-opened">
  <button class="components-panel__body-toggle">
    Section Title
    <svg class="components-panel__arrow">...</svg>
  </button>
  <div>Panel content...</div>
</div>
```

## Tips

1. **Always use tokens** — Don't hardcode colors or spacing
2. **Copy, don't reference** — Each mockup should be self-contained
3. **Check component variants** — Most components have multiple states/sizes
4. **Use semantic modifiers** — `.is-primary`, not custom color classes

## Source

Design tokens, icons, and component styles extracted from:
- [Gutenberg](https://github.com/WordPress/gutenberg/tree/trunk) — `packages/base-styles/` and `packages/components/`
