---
name: ux-typography
description: Typography patterns using Utopia fluid type scale with cqi units. Use when setting font sizes, line heights, font families, or text styling. Covers display vs body fonts, hierarchy, and readability. (project)
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# UX Typography Skill

Fluid typography system using Utopia scale with container query inline (cqi) units. This skill covers font selection, sizing, and typographic hierarchy.

## Font Stack

### Display Font (Headings, UI)

```css
--font-display: 'Cinzel', serif;
```

Use for:
- Headings (h1-h6)
- Navigation labels
- Button text
- Phase names
- Game titles

### Body Font (Content, Paragraphs)

```css
--font-sans: 'Crimson Pro', Georgia, serif;
```

Use for:
- Body text
- Paragraphs
- Form inputs
- Hints and descriptions
- Story content

## Fluid Type Scale

The project uses Utopia fluid scale with **cqi units** (container query inline). Sizes interpolate based on container width.

**IMPORTANT**: cqi units require `container-type: inline-size` on an ancestor. The project sets this on `html`.

### Type Steps

| Token | Min (320px) | Max (1240px) | Usage |
|-------|-------------|--------------|-------|
| `--step--2` | 11.11px | 12.50px | Fine print, captions |
| `--step--1` | 13.33px | 16.67px | Secondary text, hints |
| `--step-0` | 16px | 22.22px | Body text (base) |
| `--step-1` | 19.20px | 29.63px | Large body, subheads |
| `--step-2` | 23.04px | 39.51px | Section headings |
| `--step-3` | 27.65px | 52.68px | Page headings |
| `--step-4` | 33.18px | 70.24px | Hero text |
| `--step-5` | 39.81px | 93.65px | Display, titles |

### Usage

```css
.body-text {
  font-size: var(--step-0);
  font-family: var(--font-sans);
}

.heading {
  font-size: var(--step-3);
  font-family: var(--font-display);
}

.caption {
  font-size: var(--step--2);
  font-family: var(--font-sans);
}
```

## Line Height

### Recommended Values

| Content Type | Line Height | Rationale |
|--------------|-------------|-----------|
| Headings | 1.1–1.2 | Tight for visual impact |
| Body text | 1.5–1.6 | Optimal readability |
| UI elements | 1.2–1.3 | Compact but legible |
| Long-form | 1.6–1.7 | Comfortable reading |

```css
.heading {
  line-height: 1.1;
}

.body {
  line-height: 1.5;
}

.button-text {
  line-height: 1.2;
}
```

## Letter Spacing

### Tokens

```css
:root {
  --letter-spacing-tight: -0.025em;
  --letter-spacing-normal: 0;
  --letter-spacing-wide: 0.025em;
  --letter-spacing-wider: 0.05em;
}
```

### Usage Guidelines

| Context | Spacing | Example |
|---------|---------|---------|
| Large headings | `--letter-spacing-tight` | Hero titles |
| Body text | `--letter-spacing-normal` | Paragraphs |
| Small caps | `--letter-spacing-wide` | Labels |
| All caps | `--letter-spacing-wider` | Buttons |

```css
.hero-title {
  font-size: var(--step-5);
  letter-spacing: var(--letter-spacing-tight);
}

.phase-label {
  text-transform: uppercase;
  letter-spacing: var(--letter-spacing-wider);
}
```

## Font Weight

### Available Weights

- `400` - Regular (body text)
- `600` - Semibold (emphasis, labels)
- `700` - Bold (headings, buttons)

```css
.body {
  font-weight: 400;
}

.label {
  font-weight: 600;
}

.heading {
  font-weight: 700;
}
```

## Typographic Hierarchy

### Example Structure

```css
/* Page title */
h1 {
  font-family: var(--font-display);
  font-size: var(--step-4);
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: var(--letter-spacing-tight);
}

/* Section heading */
h2 {
  font-family: var(--font-display);
  font-size: var(--step-2);
  font-weight: 600;
  line-height: 1.2;
}

/* Body text */
p {
  font-family: var(--font-sans);
  font-size: var(--step-0);
  font-weight: 400;
  line-height: 1.5;
}

/* Caption/hint */
.hint {
  font-family: var(--font-sans);
  font-size: var(--step--1);
  color: var(--theme-on-surface-variant);
}
```

## Text Styling Patterns

### Emphasis

```css
/* Strong emphasis */
strong, .strong {
  font-weight: 600;
}

/* Italic for terms */
em, .term {
  font-style: italic;
}

/* Highlighted text */
mark, .highlight {
  background: var(--theme-primary-container);
  padding-inline: 0.2em;
  border-radius: 2px;
}
```

### Links

```css
a {
  color: var(--theme-primary);
  text-decoration: underline;
  text-underline-offset: 0.15em;
}

a:hover {
  text-decoration-thickness: 2px;
}

a:focus-visible {
  outline: var(--focus-ring-width) solid var(--focus-ring-color);
  outline-offset: var(--focus-ring-offset);
}
```

### Keyboard Hints

```css
kbd {
  display: inline-block;
  padding: 0.1em 0.4em;
  font-family: inherit;
  font-size: 0.9em;
  background: var(--theme-surface);
  border: 1px solid var(--theme-outline);
  border-radius: 3px;
}
```

## Responsive Typography

The fluid scale handles most responsiveness automatically. For specific adjustments:

```css
/* Container query for constrained spaces */
@container (max-width: 200px) {
  .phase-label {
    font-size: var(--step--2);
  }
}

/* Override for very large displays */
@container (min-width: 1400px) {
  .hero {
    font-size: var(--step-5);
  }
}
```

## Accessibility

### Minimum Sizes

- Body text: `--step-0` minimum (16px at base)
- Interactive labels: `--step--1` minimum (13px at base)
- Never smaller than `--step--2` for any readable text

### Avoid

```css
/* DON'T: Fixed pixel sizes */
.bad {
  font-size: 14px;
}

/* DON'T: Viewport units for body text */
.bad {
  font-size: 2vw;
}

/* DON'T: Low contrast with small text */
.bad {
  font-size: var(--step--2);
  color: var(--theme-outline);
}
```

### Do

```css
/* DO: Use fluid tokens */
.good {
  font-size: var(--step-0);
}

/* DO: Ensure contrast for small text */
.good {
  font-size: var(--step--1);
  color: var(--theme-on-surface);
}
```
