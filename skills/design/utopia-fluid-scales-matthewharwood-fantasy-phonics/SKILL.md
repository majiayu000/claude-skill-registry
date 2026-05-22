---
name: utopia-fluid-scales
description: Fluid typography and spacing tokens using Utopia.fyi with cqi (container query inline) units. Reference for the exact type steps and space tokens defined in this project.
allowed-tools: Read, Write, Edit
---

# Utopia Fluid Scales

*This project's fluid typography and spacing system*

## Configuration

Generated from: https://utopia.fyi/space/calculator?c=360,18,1.2,1240,20,1.25,5,2,&s=0.75|0.5|0.25,1.5|2|3|4|6,s-l&g=s,l,xl,12

| Parameter | Value |
|-----------|-------|
| Min viewport | 360px |
| Max viewport | 1240px |
| Min base size | 18px |
| Max base size | 20px |
| Min scale ratio | 1.2 (Minor Third) |
| Max scale ratio | 1.25 (Major Third) |

**Unit**: `cqi` (container query inline) - requires a container context to function.

## Type Scale

Location: `css/styles/typography.css`

```css
:root {
  --step--2: clamp(0.7813rem, 0.7736rem + 0.0341cqi, 0.8rem);
  --step--1: clamp(0.9375rem, 0.9119rem + 0.1136cqi, 1rem);
  --step-0: clamp(1.125rem, 1.0739rem + 0.2273cqi, 1.25rem);
  --step-1: clamp(1.35rem, 1.2631rem + 0.3864cqi, 1.5625rem);
  --step-2: clamp(1.62rem, 1.4837rem + 0.6057cqi, 1.9531rem);
  --step-3: clamp(1.944rem, 1.7405rem + 0.9044cqi, 2.4414rem);
  --step-4: clamp(2.3328rem, 2.0387rem + 1.3072cqi, 3.0518rem);
  --step-5: clamp(2.7994rem, 2.384rem + 1.8461cqi, 3.8147rem);
}
```

### Type Step Reference

| Token | Min (360px) | Max (1240px) | Use Case |
|-------|-------------|--------------|----------|
| `--step--2` | 12.5px | 12.8px | Captions, fine print |
| `--step--1` | 15px | 16px | Small text, metadata |
| `--step-0` | 18px | 20px | Body text (base) |
| `--step-1` | 21.6px | 25px | Large body, lead text |
| `--step-2` | 25.9px | 31.3px | H4 equivalent |
| `--step-3` | 31.1px | 39.1px | H3 equivalent |
| `--step-4` | 37.3px | 48.8px | H2 equivalent |
| `--step-5` | 44.8px | 61px | H1 equivalent |

### Applied Styles

```css
body {
  font-family: var(--font-base);
  font-size: var(--step-0);
  line-height: 1.5;
}
```

**Note**: No heading styles (h1-h6) are currently applied. Add as needed:

```css
h1 { font-size: var(--step-5); }
h2 { font-size: var(--step-4); }
h3 { font-size: var(--step-3); }
h4 { font-size: var(--step-2); }
h5 { font-size: var(--step-1); }
h6 { font-size: var(--step-0); }
```

## Space Scale

Location: `css/styles/space.css`

### Individual Space Tokens

```css
:root {
  --space-3xs: clamp(0.3125rem, 0.3125rem + 0cqi, 0.3125rem);
  --space-2xs: clamp(0.5625rem, 0.5369rem + 0.1136cqi, 0.625rem);
  --space-xs: clamp(0.875rem, 0.8494rem + 0.1136cqi, 0.9375rem);
  --space-s: clamp(1.125rem, 1.0739rem + 0.2273cqi, 1.25rem);
  --space-m: clamp(1.6875rem, 1.6108rem + 0.3409cqi, 1.875rem);
  --space-l: clamp(2.25rem, 2.1477rem + 0.4545cqi, 2.5rem);
  --space-xl: clamp(3.375rem, 3.2216rem + 0.6818cqi, 3.75rem);
  --space-2xl: clamp(4.5rem, 4.2955rem + 0.9091cqi, 5rem);
  --space-3xl: clamp(6.75rem, 6.4432rem + 1.3636cqi, 7.5rem);
}
```

### Space Token Reference

| Token | Min (360px) | Max (1240px) |
|-------|-------------|--------------|
| `--space-3xs` | 5px | 5px |
| `--space-2xs` | 9px | 10px |
| `--space-xs` | 14px | 15px |
| `--space-s` | 18px | 20px |
| `--space-m` | 27px | 30px |
| `--space-l` | 36px | 40px |
| `--space-xl` | 54px | 60px |
| `--space-2xl` | 72px | 80px |
| `--space-3xl` | 108px | 120px |

### One-Up Space Pairs

Fluid transitions between adjacent sizes:

```css
:root {
  --space-3xs-2xs: clamp(0.3125rem, 0.1847rem + 0.5682cqi, 0.625rem);
  --space-2xs-xs: clamp(0.5625rem, 0.4091rem + 0.6818cqi, 0.9375rem);
  --space-xs-s: clamp(0.875rem, 0.7216rem + 0.6818cqi, 1.25rem);
  --space-s-m: clamp(1.125rem, 0.8182rem + 1.3636cqi, 1.875rem);
  --space-m-l: clamp(1.6875rem, 1.3551rem + 1.4773cqi, 2.5rem);
  --space-l-xl: clamp(2.25rem, 1.6364rem + 2.7273cqi, 3.75rem);
  --space-xl-2xl: clamp(3.375rem, 2.7102rem + 2.9545cqi, 5rem);
  --space-2xl-3xl: clamp(4.5rem, 3.2727rem + 5.4545cqi, 7.5rem);
}
```

### Custom Space Pair

```css
:root {
  --space-s-l: clamp(1.125rem, 0.5625rem + 2.5cqi, 2.5rem);
}
```

| Token | Min | Max | Scaling |
|-------|-----|-----|---------|
| `--space-s-l` | 18px | 40px | Dramatic (2.2x) |

## Usage Examples

```css
/* Padding with space tokens */
.card {
  padding: var(--space-m);
}

/* Fluid gap */
.stack {
  display: flex;
  flex-direction: column;
  gap: var(--space-s-m);
}

/* Typography */
.title {
  font-size: var(--step-3);
}

/* Section spacing */
.section {
  padding-block: var(--space-l-xl);
}
```

## Container Requirement

These scales use `cqi` units which require a container context. Without a parent with `container-type: inline-size`, the fluid calculation may not work as expected.

```css
/* Required for cqi units to function */
.parent {
  container-type: inline-size;
}
```

## Files

- `css/styles/typography.css` - Type scale and body styles
- `css/styles/space.css` - Space tokens and pairs
