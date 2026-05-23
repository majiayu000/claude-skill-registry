---
name: material-symbols-v3
description: Material Symbols v3 variable icon font system. Use when adding icons to buttons, navigation, status indicators, or any UI element. Provides 2,500+ icons with fill, weight, grade, and optical size axes. Integrates with project color tokens.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Material Symbols v3

Material Design 3 icon system using variable fonts. This project uses Material Symbols Outlined loaded from Google Fonts CDN.

## Related Skills

- **`ux-iconography`**: UX patterns for icon usage, accessibility, and animations
- **`ux-accessibility`**: ARIA requirements for icon-only buttons
- **`utopia-fluid-scales`**: Type scale tokens for fluid icon sizing

## Project Setup

Location: `css/styles/icons.css`

```css
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap');
```

### Self-Hosting (Offline)

For offline/production without CDN:

1. Download from [fonts.google.com/icons](https://fonts.google.com/icons)
2. Place in `/fonts/material-symbols-outlined.woff2`
3. Replace CDN import:

```css
@font-face {
  font-family: 'Material Symbols Outlined';
  src: url('/fonts/material-symbols-outlined.woff2') format('woff2');
  font-weight: 100 700;
  font-style: normal;
}
```

---

## Basic Usage

```html
<span class="icon">home</span>
<span class="icon">settings</span>
<span class="icon">favorite</span>
```

Use the icon name from [Material Symbols](https://fonts.google.com/icons) as text content.

---

## Icon Sizes

| Class | Size | Optical Size | Use Case |
|-------|------|--------------|----------|
| `.icon--sm` | 20px | 20 | Dense UI, inline text |
| `.icon--md` | 24px | 24 | Default, buttons |
| `.icon--lg` | 40px | 40 | Emphasis, headers |
| `.icon--xl` | 48px | 48 | Hero sections |

```html
<span class="icon icon--sm">info</span>
<span class="icon icon--md">info</span>
<span class="icon icon--lg">info</span>
<span class="icon icon--xl">info</span>
```

### Fluid Sizing with Utopia

For icons that scale with typography:

```css
.icon-fluid {
  font-size: var(--step-1);
  --icon-optical-size: 24;
}
```

---

## Variable Font Axes

Material Symbols is a **variable font** with 4 axes:

| Axis | Range | Default | Purpose |
|------|-------|---------|---------|
| `FILL` | 0–1 | 0 | Outlined (0) vs filled (1) |
| `wght` | 100–700 | 400 | Stroke weight |
| `GRAD` | -25–200 | 0 | Fine thickness adjustment |
| `opsz` | 20–48 | 24 | Optical size optimization |

### Fill Styles

```html
<span class="icon icon--outlined">favorite</span>  <!-- Outline (default) -->
<span class="icon icon--filled">favorite</span>    <!-- Filled -->
```

### Weight Variants

```html
<span class="icon icon--thin">home</span>     <!-- 100 -->
<span class="icon icon--light">home</span>    <!-- 300 -->
<span class="icon icon--regular">home</span>  <!-- 400 (default) -->
<span class="icon icon--medium">home</span>   <!-- 500 -->
<span class="icon icon--bold">home</span>     <!-- 700 -->
```

### Grade Variants

```html
<span class="icon icon--grade-low">home</span>    <!-- -25: thinner on dark bg -->
<span class="icon icon--grade-normal">home</span> <!-- 0 (default) -->
<span class="icon icon--grade-high">home</span>   <!-- 200: bolder emphasis -->
```

### Custom Variation

```css
.custom-icon {
  --icon-fill: 1;
  --icon-weight: 600;
  --icon-grade: 0;
  --icon-optical-size: 24;
}
```

---

## Icon Colors

### Semantic Colors

```html
<span class="icon icon--primary">check_circle</span>
<span class="icon icon--secondary">info</span>
<span class="icon icon--disabled">block</span>
```

### Inherit from Parent

```css
.icon {
  color: inherit;  /* Default behavior */
}

.btn-primary .icon {
  color: var(--theme-on-primary);
}
```

### State Colors

```css
.icon-success { color: var(--color-success); }
.icon-error { color: var(--color-error); }
.icon-warning { color: var(--color-warning); }
```

---

## Interactive Icons

```html
<span class="icon icon--interactive">settings</span>
```

```css
.icon--interactive {
  cursor: pointer;
  transition: color 0.2s ease, transform 0.2s ease;
}

.icon--interactive:hover {
  color: var(--icon-color-primary);
  transform: scale(1.1);
}

.icon--interactive:active {
  transform: scale(0.95);
}
```

---

## Button Patterns

### Icon + Text Button

```html
<button class="btn">
  <span class="icon" aria-hidden="true">add</span>
  <span>Add Item</span>
</button>
```

```css
.btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-xs);
}
```

### Icon-Only Button

```html
<button class="btn-icon" aria-label="Settings">
  <span class="icon" aria-hidden="true">settings</span>
</button>
```

```css
.btn-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: var(--min-touch-target);
  min-height: var(--min-touch-target);
  padding: var(--space-xs);
}
```

### Trailing Icon

```html
<button class="btn">
  <span>Next</span>
  <span class="icon" aria-hidden="true">arrow_forward</span>
</button>
```

---

## Accessibility

### Decorative Icons (with visible label)

```html
<button>
  <span class="icon" aria-hidden="true">save</span>
  Save
</button>
```

### Meaningful Icons (icon-only)

```html
<button aria-label="Close dialog">
  <span class="icon" aria-hidden="true">close</span>
</button>
```

### Screen Reader Text

```html
<button class="btn-icon">
  <span class="icon" aria-hidden="true">delete</span>
  <span class="sr-only">Delete item</span>
</button>
```

### High Contrast Mode

```css
@media (forced-colors: active) {
  .icon {
    forced-color-adjust: auto;
  }
}
```

---

## Common Icons Reference

### Navigation

| Icon | Name | Usage |
|------|------|-------|
| home | `home` | Home/main |
| menu | `menu` | Hamburger menu |
| arrow_back | `arrow_back` | Back navigation |
| arrow_forward | `arrow_forward` | Forward/next |
| close | `close` | Close/dismiss |

### Actions

| Icon | Name | Usage |
|------|------|-------|
| add | `add` | Create new |
| edit | `edit` | Edit/modify |
| delete | `delete` | Remove |
| save | `save` | Save |
| search | `search` | Search |

### Status

| Icon | Name | Usage |
|------|------|-------|
| check_circle | `check_circle` | Success/complete |
| error | `error` | Error state |
| warning | `warning` | Warning |
| info | `info` | Information |
| help | `help` | Help |

### Media

| Icon | Name | Usage |
|------|------|-------|
| play_arrow | `play_arrow` | Play |
| pause | `pause` | Pause |
| volume_up | `volume_up` | Sound on |
| volume_off | `volume_off` | Sound off |

### Settings

| Icon | Name | Usage |
|------|------|-------|
| settings | `settings` | Settings |
| tune | `tune` | Adjustments |
| brightness_6 | `brightness_6` | Theme toggle |
| lock | `lock` | Locked/secure |

Browse all icons: [fonts.google.com/icons](https://fonts.google.com/icons)

---

## Animation

### With Anime.js

```javascript
import { animate } from 'animejs';

// Wiggle
animate(iconEl, {
  rotate: [0, -10, 10, -10, 10, 0],
  duration: 300,
  ease: 'easeOutQuad'
});

// Bounce
animate(iconEl, {
  scale: [1, 1.2, 1],
  duration: 200,
  ease: 'easeOutBack'
});
```

### CSS Transitions

```css
.icon {
  transition: transform 0.15s ease;
}

.btn:hover .icon {
  transform: scale(1.1);
}

.btn:active .icon {
  transform: scale(0.95);
}
```

---

## Web Component Wrapper

```javascript
class MIcon extends HTMLElement {
  static observedAttributes = ['name', 'size', 'filled'];

  connectedCallback() {
    this.render();
  }

  attributeChangedCallback() {
    this.render();
  }

  render() {
    const name = this.getAttribute('name') || 'help';
    const size = this.getAttribute('size') || 'md';
    const filled = this.hasAttribute('filled');

    this.innerHTML = `<span class="icon icon--${size}${filled ? ' icon--filled' : ''}" aria-hidden="true">${name}</span>`;
  }
}

customElements.define('m-icon', MIcon);
```

Usage:

```html
<m-icon name="home"></m-icon>
<m-icon name="favorite" filled size="lg"></m-icon>
```

---

## CSS Custom Properties

```css
:root {
  /* Font */
  --icon-font: 'Material Symbols Outlined';

  /* Sizes */
  --icon-size-sm: 20px;
  --icon-size-md: 24px;
  --icon-size-lg: 40px;
  --icon-size-xl: 48px;

  /* Variable font axes */
  --icon-fill: 0;
  --icon-weight: 400;
  --icon-grade: 0;
  --icon-optical-size: 24;

  /* Colors */
  --icon-color: var(--color-on-surface);
  --icon-color-primary: var(--color-primary);
  --icon-color-secondary: var(--color-on-surface-variant);
  --icon-color-disabled: var(--color-outline);
}
```

---

## Migration from Emoji

Replace emoji icons with Material Symbols:

| Old (Emoji) | New (Material Symbol) |
|-------------|----------------------|
| `<span aria-hidden="true">📖</span>` | `<span class="icon" aria-hidden="true">menu_book</span>` |
| `<span aria-hidden="true">⚙️</span>` | `<span class="icon" aria-hidden="true">settings</span>` |
| `<span aria-hidden="true">🏠</span>` | `<span class="icon" aria-hidden="true">home</span>` |
| `<span aria-hidden="true">⭐</span>` | `<span class="icon" aria-hidden="true">star</span>` |
| `<span aria-hidden="true">🔒</span>` | `<span class="icon" aria-hidden="true">lock</span>` |
| `<span aria-hidden="true">🔊</span>` | `<span class="icon" aria-hidden="true">volume_up</span>` |
| `<span aria-hidden="true">🔇</span>` | `<span class="icon" aria-hidden="true">volume_off</span>` |
| `<span aria-hidden="true">✓</span>` | `<span class="icon" aria-hidden="true">check</span>` |

---

## Files

- `css/styles/icons.css` - Icon system styles and CSS custom properties
