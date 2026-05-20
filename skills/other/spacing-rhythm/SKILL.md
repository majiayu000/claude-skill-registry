---
name: spacing-rhythm
description: "Establish consistent spacing systems, vertical rhythm, and white space usage for visual harmony. Use for: defining spacing scales, creating vertical rhythm, establishing padding/margin rules, and achieving visual balance."
---

# Spacing Rhythm

## Description

Spacing & Rhythm creates a mathematical system for whitespace that ensures visual consistency, establishes hierarchy, and creates pleasing proportions throughout the design. Good spacing is invisible but essential.

## When to Use

- After typography scale is established
- Before component design
- When layouts feel cramped or chaotic
- Establishing design system foundations
- Ensuring responsive spacing

---

## Instructions for AI Agents

### Step 1: Establish Base Unit

**Common base units:**

| Base | Scale | Best For |
|------|-------|----------|
| 4px | Compact, dense UI | Dashboards, data |
| 8px | Balanced, standard | Most applications |
| 16px | Spacious, editorial | Marketing, content |

**Prompt for spacing decision:**
```
For [PROJECT TYPE] targeting [AUDIENCE] with [DENSITY] information density:

1. Recommended base unit: [4/8/16]px
2. Scale multiplier approach: [Linear/Fibonacci/Custom]
3. Minimum spacing: [Value]
4. Maximum practical spacing: [Value]
```

### Step 2: Create Spacing Scale

**8px base scale (most common):**

```markdown
## Spacing Scale

| Token | Value | Pixels | Usage |
|-------|-------|--------|-------|
| space-0 | 0 | 0px | Reset, collapse |
| space-0.5 | 0.125rem | 2px | Micro gaps, hairlines |
| space-1 | 0.25rem | 4px | Icon-text gap, tight |
| space-2 | 0.5rem | 8px | Related elements |
| space-3 | 0.75rem | 12px | Default component padding |
| space-4 | 1rem | 16px | Standard gap |
| space-5 | 1.25rem | 20px | Component spacing |
| space-6 | 1.5rem | 24px | Card padding, sections |
| space-8 | 2rem | 32px | Large gaps |
| space-10 | 2.5rem | 40px | Section spacing |
| space-12 | 3rem | 48px | Major sections |
| space-16 | 4rem | 64px | Page sections |
| space-20 | 5rem | 80px | Hero spacing |
| space-24 | 6rem | 96px | Maximum gaps |
```

### Step 3: Define Usage Patterns

**Spacing application guide:**

```markdown
## Spacing Applications

### Component Internal Spacing

| Component | Padding | Internal Gap |
|-----------|---------|-------------|
| Button (sm) | 8px 12px | 6px (icon-text) |
| Button (md) | 10px 16px | 8px |
| Button (lg) | 12px 24px | 10px |
| Input | 12px 16px | - |
| Card | 20px or 24px | 16px |
| Modal | 24px | 20px |
| Table cell | 12px 16px | - |
| List item | 12px 16px | - |

### Component External Spacing

| Relationship | Spacing |
|--------------|--------|
| Related items (same group) | 8px |
| Items in a list | 12px |
| Components in same section | 16-24px |
| Section title to content | 16-24px |
| Between sections | 48-64px |
| Page title to content | 32px |
| Major page sections | 64-96px |

### Text Spacing

| Element | Margin Bottom |
|---------|---------------|
| Paragraph | 16px (1rem) |
| Heading to paragraph | 8-12px |
| Paragraph to heading | 32px |
| List items | 8px |
| Between list groups | 24px |
```

### Step 4: Vertical Rhythm

**Establishing baseline grid:**

```markdown
## Vertical Rhythm

### Baseline Grid
- Base line-height unit: 24px (for 16px body text × 1.5)
- All spacing should align to 4px or 8px increments

### Element Heights

| Element | Height | Lines (24px) |
|---------|--------|-------------|
| Single line text | 24px | 1 |
| Button (md) | 40px | ~1.67 (aligned to 8px) |
| Input (md) | 44px | ~1.83 (touch-friendly) |
| Nav item | 40px | ~1.67 |
| Table row | 48px | 2 |
| Card header | 64px | ~2.67 |

### Section Rhythm

```
| 96px | <- Page top padding
|------|
| Page Title (H1)
| 32px |
|------|
| Section
| 64px |
|------|
| Section
| 64px |
|------|
| 96px | <- Page bottom padding
```
```

### Step 5: Responsive Spacing

**Spacing adjustments by breakpoint:**

```markdown
## Responsive Spacing

### Scale by Breakpoint

| Token | Mobile | Tablet | Desktop |
|-------|--------|--------|----------|
| Section gap | 48px | 64px | 80px |
| Container padding | 16px | 24px | 32px |
| Card padding | 16px | 20px | 24px |
| Component gap | 12px | 16px | 16px |

### Fluid Spacing (CSS)

```css
/* Section spacing that scales with viewport */
.section-gap {
  padding: clamp(48px, 8vw, 96px) 0;
}

/* Container padding */
.container {
  padding: 0 clamp(16px, 4vw, 32px);
}
```

### Touch Considerations

- Minimum touch target: 44×44px
- Minimum tap spacing: 8px between targets
- Larger spacing on mobile for fat fingers
```

---

## Example Input/Output

### Example Input

```markdown
**Project**: TaskFlow dashboard
**Type**: SaaS application, moderate density
**Typography base**: 16px
**Grid gutter**: 24px
```

### Example Output

```markdown
## Spacing System: TaskFlow

### Foundation

**Base Unit**: 8px
**Philosophy**: Balanced whitespace for productive, calm interface

---

### Spacing Scale

| Token | rem | px | Usage |
|-------|-----|-----|-------|
| `--space-0` | 0 | 0 | Reset |
| `--space-px` | 1px | 1px | Borders |
| `--space-0.5` | 0.125rem | 2px | Hairline gaps |
| `--space-1` | 0.25rem | 4px | Tight gaps, icon-text |
| `--space-1.5` | 0.375rem | 6px | Dense lists |
| `--space-2` | 0.5rem | 8px | Related elements |
| `--space-2.5` | 0.625rem | 10px | Button padding-y |
| `--space-3` | 0.75rem | 12px | Default internal |
| `--space-4` | 1rem | 16px | Standard gap |
| `--space-5` | 1.25rem | 20px | Card padding (compact) |
| `--space-6` | 1.5rem | 24px | Card padding, gutter |
| `--space-8` | 2rem | 32px | Section title gap |
| `--space-10` | 2.5rem | 40px | Component groups |
| `--space-12` | 3rem | 48px | Minor sections |
| `--space-16` | 4rem | 64px | Major sections |
| `--space-20` | 5rem | 80px | Page sections |
| `--space-24` | 6rem | 96px | Hero spacing |

---

### Application Rules

#### Components

**Buttons**
```css
.btn-sm { padding: 6px 12px; }    /* space-1.5, space-3 */
.btn-md { padding: 10px 16px; }   /* space-2.5, space-4 */
.btn-lg { padding: 12px 24px; }   /* space-3, space-6 */
```

**Cards**
```css
.card {
  padding: 20px;             /* space-5 */
}
.card-header {
  padding: 16px 20px;        /* space-4, space-5 */
  margin: -20px -20px 20px;  /* Bleed to edges */
}
.card > * + * {
  margin-top: 16px;          /* space-4 between children */
}
```

**Form Elements**
```css
.form-group {
  margin-bottom: 20px;       /* space-5 */
}
.form-group label {
  margin-bottom: 6px;        /* space-1.5 */
}
.form-row {
  gap: 16px;                 /* space-4 */
}
```

#### Layout

**Page Structure**
```css
.page {
  padding: 32px;             /* space-8 */
}
.page-header {
  margin-bottom: 32px;       /* space-8 */
}
.page-section {
  margin-bottom: 48px;       /* space-12 */
}
.page-section:last-child {
  margin-bottom: 0;
}
```

**Content Sections**
```css
.section-title {
  margin-bottom: 24px;       /* space-6 */
}
.section-content > * + * {
  margin-top: 16px;          /* space-4 */
}
```

**Sidebar**
```css
.sidebar {
  padding: 16px;             /* space-4 */
}
.sidebar-section + .sidebar-section {
  margin-top: 24px;          /* space-6 */
  padding-top: 24px;
  border-top: 1px solid var(--border);
}
.nav-item {
  padding: 10px 12px;        /* space-2.5, space-3 */
  margin-bottom: 2px;        /* space-0.5 */
}
```

---

### Vertical Rhythm

**Baseline**: 8px (tight) to 24px (relaxed)

**Text Flow**
```css
p + p {
  margin-top: 16px;          /* space-4 */
}
h2, h3, h4 {
  margin-top: 32px;          /* space-8 */
  margin-bottom: 16px;       /* space-4 */
}
ul, ol {
  margin: 16px 0;            /* space-4 */
}
li + li {
  margin-top: 8px;           /* space-2 */
}
```

**Element Heights (8px aligned)**
```
Button sm:  32px (4 × 8px)
Button md:  40px (5 × 8px)
Button lg:  48px (6 × 8px)
Input:      44px (touch-friendly)
Nav item:   40px (5 × 8px)
Table row:  48px (6 × 8px)
Avatar sm:  32px (4 × 8px)
Avatar md:  40px (5 × 8px)
Avatar lg:  48px (6 × 8px)
```

---

### Responsive Adjustments

| Spacing Type | Mobile | Tablet | Desktop |
|--------------|--------|--------|----------|
| Page padding | 16px | 24px | 32px |
| Card padding | 16px | 20px | 24px |
| Section gap | 32px | 48px | 64px |
| Component gap | 12px | 16px | 16px |
| Grid gutter | 16px | 20px | 24px |

```css
/* Responsive page padding */
.page {
  padding: 16px;
}
@media (min-width: 768px) {
  .page {
    padding: 24px;
  }
}
@media (min-width: 1024px) {
  .page {
    padding: 32px;
  }
}
```

---

### Quick Reference

**Tight (2-4px)**: Icon-to-text, stacked badges
**Compact (8-12px)**: Related elements, list items
**Standard (16-24px)**: Component gaps, card padding
**Relaxed (32-48px)**: Section titles, component groups
**Spacious (64-96px)**: Page sections, hero areas

---

### CSS Custom Properties

```css
:root {
  --space-0: 0;
  --space-1: 0.25rem;  /* 4px */
  --space-2: 0.5rem;   /* 8px */
  --space-3: 0.75rem;  /* 12px */
  --space-4: 1rem;     /* 16px */
  --space-5: 1.25rem;  /* 20px */
  --space-6: 1.5rem;   /* 24px */
  --space-8: 2rem;     /* 32px */
  --space-10: 2.5rem;  /* 40px */
  --space-12: 3rem;    /* 48px */
  --space-16: 4rem;    /* 64px */
  --space-20: 5rem;    /* 80px */
  --space-24: 6rem;    /* 96px */
  
  /* Semantic spacing */
  --space-component-padding: var(--space-4);
  --space-card-padding: var(--space-6);
  --space-section-gap: var(--space-12);
  --space-page-padding: var(--space-8);
}
```
```

---

## Prompts Library

### Spacing Scale Generation
```
Create a spacing scale for [PROJECT TYPE]:
- Base unit: [4/8/16]px
- Density: [Compact/Balanced/Spacious]
- Include: Token names, pixel values, use cases
```

### Component Spacing Audit
```
Review spacing in this component:
[COMPONENT SPEC]

Check:
1. Is internal spacing consistent?
2. Is external spacing defined?
3. Does it align to the spacing scale?
4. Touch targets adequate?
```

---

## Success Criteria

### Minimum Requirements
- [ ] Base unit established
- [ ] Complete spacing scale
- [ ] Component padding defined
- [ ] Section spacing defined
- [ ] Responsive considerations

### Quality Indicators
- [ ] Consistent spacing throughout design
- [ ] Clear hierarchy through spacing
- [ ] Comfortable, not cramped
- [ ] Touch-friendly targets
- [ ] Scale supports all use cases

---

## Related Skills

- **Previous**: `typography.md` - Line heights inform rhythm
- **Previous**: `layout_grids.md` - Grid gutters align with spacing
- **Next**: `component_design.md` - Apply spacing to components
