---
name: ux-iconography
description: Icon usage patterns using Material Symbols v3. Use when adding icons to buttons, navigation, or status indicators. Covers sizing, accessibility, animations, and color integration with project tokens.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# UX Iconography Skill

Icon implementation patterns for UI components. This project uses **Material Symbols v3** as the primary icon system.

## Related Skills

- **`material-symbols-v3`**: Complete icon API reference, variable font axes, icon names
- **`ux-accessibility`**: ARIA requirements for icon buttons
- **`ux-animation-motion`**: Anime.js patterns for icon animations

## Icon System

Location: `css/styles/icons.css`

This project uses Material Symbols Outlined (variable font) from Google Fonts:

```html
<span class="icon">home</span>
<span class="icon">settings</span>
<span class="icon">favorite</span>
```

See **`material-symbols-v3`** skill for complete icon name reference.

## Icon Sizing

### Size Classes

```html
<span class="icon icon--sm">info</span>   <!-- 20px -->
<span class="icon icon--md">info</span>   <!-- 24px (default) -->
<span class="icon icon--lg">info</span>   <!-- 40px -->
<span class="icon icon--xl">info</span>   <!-- 48px -->
```

### Fluid Sizing with Utopia

Scale icons with typography tokens:

```css
.icon-fluid {
  font-size: var(--step-1);
}

.icon-small {
  font-size: var(--step--1);
}
```

### Fixed Container

```css
.icon-fixed {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
}
```

## Icon + Text Patterns

### Inline with Label

```html
<button class="btn-icon-text">
  <span class="icon" aria-hidden="true">menu_book</span>
  <span class="label">Word Phase</span>
</button>
```

```css
.btn-icon-text {
  display: inline-flex;
  align-items: center;
  gap: var(--space-xs);
}

.btn-icon-text .icon {
  flex-shrink: 0;
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
<a href="/next" class="link-arrow">
  Next Phase
  <span class="icon" aria-hidden="true">arrow_forward</span>
</a>
```

## Accessibility

### Always Hide Decorative Icons

```html
<!-- Decorative: has visible label -->
<button>
  <span class="icon" aria-hidden="true">settings</span>
  Settings
</button>

<!-- Meaningful: icon-only needs label -->
<button aria-label="Settings">
  <span class="icon" aria-hidden="true">settings</span>
</button>
```

### Screen Reader Text

```html
<button class="btn-icon">
  <span class="icon" aria-hidden="true">settings</span>
  <span class="sr-only">Settings</span>
</button>
```

```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  clip: rect(0, 0, 0, 0);
}
```

### Status Icons with Text

```html
<span class="status status-complete">
  <span class="icon" aria-hidden="true">check_circle</span>
  <span>Complete</span>
</span>
```

## Icon Variants

### Fill Style

```html
<span class="icon icon--outlined">favorite</span>  <!-- Outline (default) -->
<span class="icon icon--filled">favorite</span>    <!-- Solid fill -->
```

### Weight

```html
<span class="icon icon--thin">home</span>     <!-- 100 -->
<span class="icon icon--light">home</span>    <!-- 300 -->
<span class="icon icon--regular">home</span>  <!-- 400 -->
<span class="icon icon--medium">home</span>   <!-- 500 -->
<span class="icon icon--bold">home</span>     <!-- 700 -->
```

## Icon Color

### Inherit from Parent

```css
.icon {
  color: inherit;
}

.btn-primary .icon {
  color: var(--theme-on-primary);
}
```

### Semantic Colors

```css
.icon-success { color: var(--color-success); }
.icon-error { color: var(--color-error); }
.icon-warning { color: var(--color-warning); }
```

### Phase Colors

```css
[data-phase="word"] .icon { color: var(--color-word); }
[data-phase="collision"] .icon { color: var(--color-collision); }
[data-phase="mutation"] .icon { color: var(--color-mutation); }
[data-phase="story"] .icon { color: var(--color-story); }
```

## Animation

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

### Wiggle Animation (Anime.js)

```javascript
import { animate } from 'animejs';
import { DURATION, EASE } from '../../utils/animations.js';

animate(this._iconEl, {
  rotate: [0, -10, 10, -10, 10, 0],
  duration: DURATION.normal,
  ease: EASE.smooth
});
```

### Celebration Bounce

```javascript
import { successBounce } from '../../utils/animations.js';

successBounce(this._iconEl);
// Scale: 1 → 1.2 → 1
```

## Status Indicators

### Phase Status

```css
.phase-icon {
  font-size: var(--step-0);
}

[data-status="complete"] .phase-icon {
  color: var(--color-success);
}

[data-status="current"] .phase-icon {
  color: var(--theme-primary);
  animation: pulse 1.5s ease-in-out infinite;
}

[data-status="locked"] .phase-icon {
  opacity: 0.5;
  filter: grayscale(0.5);
}
```

### Progress Dots

```css
.progress-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--theme-outline-variant);
}

.progress-dot[data-completed] {
  background: var(--color-success);
}

.progress-dot[data-current] {
  background: var(--theme-primary);
}
```

## Loading Icons

### Spinner

```html
<span class="spinner" role="status">
  <span class="sr-only">Loading...</span>
</span>
```

```css
.spinner {
  display: inline-block;
  width: 1em;
  height: 1em;
  border: 2px solid var(--theme-outline);
  border-top-color: var(--theme-primary);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { rotate: 360deg; }
}
```

## Common Game Icons

| Purpose | Icon Name | Usage |
|---------|-----------|-------|
| Word phase | `menu_book` | Phase indicator |
| Collision phase | `swords` | Phase indicator |
| Mutation phase | `genetics` | Phase indicator |
| Story phase | `auto_stories` | Phase indicator |
| Complete | `check_circle` | Status indicator |
| Locked | `lock` | Unavailable item |
| Star/achievement | `star` | Rewards |
| Settings | `settings` | Configuration |
| Home | `home` | Navigation |
| Sound on | `volume_up` | Audio toggle |
| Sound off | `volume_off` | Audio toggle |

## High Contrast Mode

```css
@media (forced-colors: active) {
  .icon {
    forced-color-adjust: auto;
  }
}
```

## Best Practices

### Do

- Use `aria-hidden="true"` on decorative icons
- Provide `aria-label` for icon-only buttons
- Use semantic colors for status icons
- Ensure touch targets are 44x44px minimum
- Use `.icon--filled` for selected/active states

### Don't

- Use icons as the only indicator of meaning
- Forget to hide icons from screen readers
- Use fixed pixel sizes that don't scale
- Animate icons excessively
- Mix icon systems inconsistently
