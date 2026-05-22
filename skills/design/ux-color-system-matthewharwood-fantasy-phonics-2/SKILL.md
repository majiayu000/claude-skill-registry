---
name: ux-color-system
description: Fantasy-themed color tokens and semantic color usage. Use when applying colors, creating themes, or ensuring color accessibility. Covers surface/text relationships, state colors, and dark theme patterns. (project)
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# UX Color System Skill

Semantic color architecture for the Fantasy Phonics game. Uses CSS custom properties for maintainable, accessible theming.

## Color Philosophy

Colors in this project follow a **fantasy/medieval** aesthetic:
- Warm, parchment-like surfaces
- Gold accents for primary actions
- Earth tones for secondary elements
- Success greens and error reds for feedback

## Semantic Color Tokens

### Surface & Background

```css
/* Base surfaces */
--theme-surface: #252119;           /* Main background */
--theme-surface-variant: #2f2a21;   /* Elevated surfaces */
--theme-surface-dim: #1a1814;       /* Recessed areas */

/* Text on surfaces */
--theme-on-surface: #f5e6c8;        /* Primary text */
--theme-on-surface-variant: #9b8b72; /* Secondary/muted text */
```

### Primary & Accent

```css
/* Primary gold accent */
--theme-primary: #d4a84b;           /* Buttons, links, focus */
--theme-on-primary: #1a1814;        /* Text on primary */
--theme-primary-container: #3d3525; /* Primary backgrounds */
--theme-on-primary-container: #f5daa0;

/* Secondary/outline */
--theme-outline: #8b7355;           /* Borders */
--theme-outline-variant: #5c4d3d;   /* Subtle borders */
```

### Semantic Colors

```css
/* Feedback colors */
--color-success: #6bcf7f;           /* Completed, correct */
--color-error: #ef4444;             /* Errors, wrong */
--color-warning: #f59e0b;           /* Caution states */

/* Phase-specific colors */
--color-word: #6366f1;              /* Word phase (indigo) */
--color-collision: #ec4899;         /* Collision phase (pink) */
--color-mutation: #f59e0b;          /* Mutation phase (amber) */
--color-story: #22c55e;             /* Story phase (green) */
```

## Usage Patterns

### Surface/Text Pairing

Always pair surface and text colors correctly:

```css
.card {
  background: var(--theme-surface);
  color: var(--theme-on-surface);
}

.card-muted {
  color: var(--theme-on-surface-variant);
}

.button-primary {
  background: var(--theme-primary);
  color: var(--theme-on-primary);
}
```

### State Colors

Apply semantic colors for component states:

```css
/* Success state */
.completed {
  color: var(--color-success);
  border-color: var(--color-success);
}

/* Error state */
.error {
  color: var(--color-error);
  border-color: var(--color-error);
}

/* Active/focus state */
.focused {
  border-color: var(--theme-primary);
  box-shadow: 0 0 0 3px rgba(212, 168, 75, 0.2);
}
```

### Phase Indicators

Use phase colors consistently throughout game:

```css
[data-phase="word"] {
  --phase-color: var(--color-word);
}

[data-phase="collision"] {
  --phase-color: var(--color-collision);
}

[data-phase="mutation"] {
  --phase-color: var(--color-mutation);
}

[data-phase="story"] {
  --phase-color: var(--color-story);
}

.phase-indicator {
  background: var(--phase-color);
}
```

## Overlay Colors

For hover, active, and disabled states:

```css
:root {
  /* Overlays */
  --color-hover-overlay: rgba(212, 168, 75, 0.08);
  --color-active-overlay: rgba(212, 168, 75, 0.2);
  --color-disabled-overlay: rgba(0, 0, 0, 0.4);
}

.button:hover {
  background: var(--color-hover-overlay);
}

.button:active {
  background: var(--color-active-overlay);
}

.button:disabled {
  opacity: 0.6;
}
```

## Gradient Patterns

Fantasy-themed gradients for special elements:

```css
/* Parchment gradient */
.parchment {
  background: linear-gradient(
    180deg,
    var(--theme-surface) 0%,
    var(--theme-surface-variant) 100%
  );
}

/* Gold shimmer for achievements */
.achievement {
  background: linear-gradient(
    135deg,
    var(--theme-primary) 0%,
    var(--theme-on-primary-container) 50%,
    var(--theme-primary) 100%
  );
}

/* Vignette for immersion */
.vignette::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(
    ellipse at center,
    transparent 0%,
    rgba(0, 0, 0, 0.3) 100%
  );
  pointer-events: none;
}
```

## Color Accessibility

### Contrast Requirements

| Combination | Ratio | Pass |
|-------------|-------|------|
| --theme-on-surface on --theme-surface | 12.5:1 | AAA |
| --theme-on-surface-variant on --theme-surface | 4.8:1 | AA |
| --theme-primary on --theme-surface | 7.2:1 | AAA |
| --color-success on --theme-surface | 6.1:1 | AA |

### Never Do

```css
/* DON'T: Low contrast combinations */
.bad {
  color: var(--theme-outline);        /* Too muted for body text */
  background: var(--theme-surface);
}

/* DON'T: Colored text on colored background */
.bad {
  color: var(--color-success);
  background: var(--color-word);
}
```

### Always Do

```css
/* DO: Use semantic pairings */
.good {
  background: var(--theme-surface);
  color: var(--theme-on-surface);
}

/* DO: Use muted for large, non-critical text */
.hint {
  font-size: var(--step--1);          /* Larger text */
  color: var(--theme-on-surface-variant);
}
```

## Dark Theme (Default)

This project uses dark theme as default. If adding light theme:

```css
@media (prefers-color-scheme: light) {
  :root {
    --theme-surface: #f5e6c8;
    --theme-on-surface: #1a1814;
    --theme-surface-variant: #e8d9b8;
    /* Invert other tokens... */
  }
}
```

## Component Examples

### Card Component

```css
.card {
  background: var(--theme-surface-variant);
  border: 1px solid var(--theme-outline-variant);
  color: var(--theme-on-surface);
}

.card:hover {
  border-color: var(--theme-outline);
}

.card:focus-within {
  border-color: var(--theme-primary);
}
```

### Button Variants

```css
/* Primary */
.btn-primary {
  background: var(--theme-primary);
  color: var(--theme-on-primary);
}

/* Secondary/Ghost */
.btn-secondary {
  background: transparent;
  color: var(--theme-primary);
  border: 1px solid var(--theme-primary);
}

/* Danger */
.btn-danger {
  background: var(--color-error);
  color: white;
}
```
