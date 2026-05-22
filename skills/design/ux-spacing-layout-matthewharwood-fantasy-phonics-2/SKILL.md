---
name: ux-spacing-layout
description: Utopia fluid spacing tokens and layout patterns. Use when applying margins, padding, gaps, or creating layouts. Covers space scale, container widths, and responsive spacing. (project)
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# UX Spacing & Layout Skill

Fluid spacing system using Utopia scale with container query inline (cqi) units. This skill covers spacing tokens, layout patterns, and visual rhythm.

## Space Scale

The project uses Utopia fluid spacing with **cqi units**. Sizes interpolate based on container width.

**IMPORTANT**: cqi units require `container-type: inline-size` on an ancestor.

### Space Tokens

| Token | Min (320px) | Max (1240px) | Usage |
|-------|-------------|--------------|-------|
| `--space-3xs` | 4px | 6px | Hairline gaps |
| `--space-2xs` | 8px | 11px | Tight spacing |
| `--space-xs` | 12px | 17px | Compact gaps |
| `--space-s` | 16px | 22px | Standard small |
| `--space-m` | 24px | 33px | Standard medium |
| `--space-l` | 32px | 44px | Generous spacing |
| `--space-xl` | 48px | 67px | Section breaks |
| `--space-2xl` | 64px | 89px | Major sections |
| `--space-3xl` | 96px | 133px | Page-level gaps |

### One-Up Pairs

For asymmetric spacing relationships:

| Token | Values | Usage |
|-------|--------|-------|
| `--space-3xs-2xs` | 4px → 11px | Micro to tight |
| `--space-2xs-xs` | 8px → 17px | Tight to compact |
| `--space-xs-s` | 12px → 22px | Compact to standard |
| `--space-s-m` | 16px → 33px | Standard progression |
| `--space-m-l` | 24px → 44px | Medium to generous |
| `--space-l-xl` | 32px → 67px | Section transitions |

## Usage Patterns

### Padding

```css
/* Compact element */
.chip {
  padding: var(--space-2xs) var(--space-xs);
}

/* Standard button */
.button {
  padding: var(--space-s) var(--space-m);
}

/* Card */
.card {
  padding: var(--space-m);
}

/* Modal */
.modal {
  padding: var(--space-l);
}
```

### Margins

```css
/* Between inline elements */
.inline-group > * + * {
  margin-inline-start: var(--space-xs);
}

/* Between sections */
section + section {
  margin-block-start: var(--space-xl);
}

/* Page container */
.page {
  margin-inline: auto;
  padding-inline: var(--space-m);
}
```

### Gap (Flexbox/Grid)

```css
/* Tight list */
.list-tight {
  display: flex;
  flex-direction: column;
  gap: var(--space-2xs);
}

/* Standard stack */
.stack {
  display: flex;
  flex-direction: column;
  gap: var(--space-s);
}

/* Card grid */
.grid {
  display: grid;
  gap: var(--space-m);
}

/* Icon + text */
.icon-text {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
}
```

## Layout Utilities

### u-stack (Vertical)

```css
u-stack[gap="3xs"] { gap: var(--space-3xs); }
u-stack[gap="2xs"] { gap: var(--space-2xs); }
u-stack[gap="xs"]  { gap: var(--space-xs); }
u-stack[gap="s"]   { gap: var(--space-s); }
u-stack[gap="m"]   { gap: var(--space-m); }
u-stack[gap="l"]   { gap: var(--space-l); }
u-stack[gap="xl"]  { gap: var(--space-xl); }
```

### u-row (Horizontal)

```css
u-row[gap="xs"]  { gap: var(--space-xs); }
u-row[gap="s"]   { gap: var(--space-s); }
u-row[gap="m"]   { gap: var(--space-m); }
```

### Container Widths

```css
.u-container {
  width: min(100% - var(--space-m) * 2, var(--max-width, 1200px));
  margin-inline: auto;
}

.narrow { --max-width: 600px; }
.medium { --max-width: 900px; }
.wide   { --max-width: 1200px; }
```

## Visual Rhythm

### Consistent Spacing Rules

1. **Related items**: Use `--space-2xs` to `--space-xs`
2. **Grouped elements**: Use `--space-s` to `--space-m`
3. **Sections**: Use `--space-l` to `--space-xl`
4. **Page breaks**: Use `--space-2xl` to `--space-3xl`

### Example Component

```css
.card {
  /* Card padding */
  padding: var(--space-m);

  /* Internal spacing */
  display: flex;
  flex-direction: column;
  gap: var(--space-s);
}

.card-header {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
}

.card-content {
  /* Paragraph spacing */
  display: flex;
  flex-direction: column;
  gap: var(--space-2xs);
}

.card-actions {
  /* Button group */
  display: flex;
  gap: var(--space-xs);
  margin-block-start: var(--space-s);
}
```

## Responsive Spacing

### Container Queries

```css
/* Compact on small containers */
@container (max-width: 400px) {
  .card {
    padding: var(--space-s);
    gap: var(--space-xs);
  }
}

/* Generous on large containers */
@container (min-width: 800px) {
  .card {
    padding: var(--space-l);
    gap: var(--space-m);
  }
}
```

### Asymmetric Spacing

Use one-up pairs for progressive spacing:

```css
.section {
  /* Tight top, generous bottom */
  padding-block: var(--space-s-m) var(--space-m-l);
}
```

## Common Patterns

### Form Layout

```css
.form {
  display: flex;
  flex-direction: column;
  gap: var(--space-m);
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: var(--space-2xs);
}

.form-actions {
  display: flex;
  gap: var(--space-s);
  margin-block-start: var(--space-s);
}
```

### Navigation

```css
.nav {
  display: flex;
  gap: var(--space-xs);
  padding: var(--space-2xs);
}

.nav-item {
  padding: var(--space-2xs) var(--space-s);
}
```

### Dialog/Modal

```css
.modal {
  padding: var(--space-l);
}

.modal-header {
  padding-block-end: var(--space-m);
  border-block-end: 1px solid var(--theme-outline);
}

.modal-body {
  padding-block: var(--space-m);
}

.modal-footer {
  padding-block-start: var(--space-m);
  display: flex;
  justify-content: flex-end;
  gap: var(--space-s);
}
```

## Avoid

```css
/* DON'T: Fixed pixel values */
.bad {
  padding: 16px;
  margin: 24px;
}

/* DON'T: Magic numbers */
.bad {
  gap: 13px;
}

/* DON'T: Inconsistent spacing */
.bad {
  padding: 10px 20px 15px 25px;
}
```

## Do

```css
/* DO: Use space tokens */
.good {
  padding: var(--space-s);
  margin: var(--space-m);
}

/* DO: Consistent relationships */
.good {
  padding: var(--space-s) var(--space-m);
}
```
