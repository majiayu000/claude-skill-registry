---
name: visual-hierarchy-refactoring
description: Master visual hierarchy through size, weight, contrast, and whitespace. Learn to establish clear information hierarchy without relying solely on color. Covers Gestalt principles, the rule of excessive whitespace, and the visual weight system. Use when designing layouts, establishing visual importance, or refactoring cluttered interfaces.
---

# Visual Hierarchy & Refactoring UI

## Overview

Visual hierarchy is the principle that **design is a function of size, weight, and contrast**—not color. When done right, users instantly understand what's important and where to look next. This skill teaches you to establish clear hierarchy through systematic visual decisions.

## Core Principle: The Rule of Excessive Whitespace

The most common mistake in interface design is **density**. When interfaces feel cluttered, the instinct is to shrink text. This is wrong.

**The Solution: Start with too much space.**

When you have breathing room, users can scan the interface and identify signals amongst the noise. Generous whitespace signals confidence—it implies that the content presented is important enough to stand on its own, without competing for attention.

### Application

If a standard margin is 16px, try 32px or 48px. If you feel it's too much space, you're probably on the right track. Reduce from there, but never back to density.

```css
/* Generous whitespace creates confidence */
.card {
  padding: 48px;  /* Not 16px */
  margin-bottom: 32px;  /* Not 8px */
}

.section {
  margin-top: 64px;  /* Breathing room between sections */
  margin-bottom: 64px;
}
```

## Visual Hierarchy Through Size, Weight, and Contrast

### 1. Size Hierarchy

Size is the most powerful tool for establishing hierarchy. Larger elements draw attention first.

**Guidelines:**
- Primary information should be 1.5-2x larger than secondary
- Each level should be clearly distinguishable
- Use modular scales (Major Second, Major Third, Perfect Fifth)

```css
/* Size hierarchy */
h1 {
  font-size: 48px;  /* Primary */
}

h2 {
  font-size: 32px;  /* Secondary */
}

h3 {
  font-size: 24px;  /* Tertiary */
}

body {
  font-size: 16px;  /* Base */
}

small {
  font-size: 12px;  /* Tertiary text */
}
```

### 2. Weight Hierarchy

Font weight creates visual emphasis without changing size.

**Guidelines:**
- Use 2-3 weights maximum (e.g., 400, 600, 700)
- Bold for emphasis, not for everything
- Lighter weight for secondary information

```css
/* Weight hierarchy */
h1 {
  font-weight: 700;  /* Bold for primary */
  font-size: 48px;
}

h2 {
  font-weight: 600;  /* Semi-bold for secondary */
  font-size: 32px;
}

body {
  font-weight: 400;  /* Regular for body */
  font-size: 16px;
}

.secondary-text {
  font-weight: 400;  /* Regular, not bold */
  color: var(--text-secondary);
}
```

### 3. Contrast Hierarchy

Contrast creates visual separation and guides attention.

**Guidelines:**
- High contrast for primary information
- Medium contrast for secondary
- Low contrast for tertiary/disabled

```css
/* Contrast hierarchy */
.primary-text {
  color: var(--text-primary);  /* High contrast */
}

.secondary-text {
  color: var(--text-secondary);  /* Medium contrast */
}

.tertiary-text {
  color: var(--text-tertiary);  /* Low contrast */
}

.disabled-text {
  color: var(--text-disabled);  /* Very low contrast */
  opacity: 0.5;
}
```

## The Color Weight System

### Tinted Greys, Not True Greys

A definitive marker of amateur design is using "True Grey" (#808080) or "True Black" (#000000) on colored backgrounds.

**The Principle:** Always use tinted greys. If your brand is blue, your "grey" should be a deeply desaturated blue. If your brand is warm/orange, your grey should be warm.

```css
/* Bad - True Grey */
.text-on-blue {
  color: #808080;  /* True grey - looks wrong */
}

/* Good - Tinted Grey */
.text-on-blue {
  color: #4B5563;  /* Deeply desaturated blue - feels right */
}

/* Bad - True Black */
.text {
  color: #000000;  /* True black - harsh */
}

/* Good - Tinted Black */
.text {
  color: #030712;  /* Deeply desaturated blue-black - softer */
}
```

### Building a Color Weight System

Create 8-10 shades per hue before writing any code. This prevents "hex code drift" where a codebase accumulates 50 slightly different versions of the same color.

```css
/* Color weight system - 10 shades per hue */
:root {
  /* Primary Blue */
  --blue-50:   #F0F9FF;
  --blue-100:  #E0F2FE;
  --blue-200:  #BAE6FD;
  --blue-300:  #7DD3FC;
  --blue-400:  #38BDF8;
  --blue-500:  #0EA5E9;
  --blue-600:  #0284C7;
  --blue-700:  #0369A1;
  --blue-800:  #075985;
  --blue-900:  #0C3D66;

  /* Tinted Greys (desaturated blue) */
  --gray-50:   #F8FAFC;
  --gray-100:  #F1F5F9;
  --gray-200:  #E2E8F0;
  --gray-300:  #CBD5E1;
  --gray-400:  #94A3B8;
  --gray-500:  #64748B;
  --gray-600:  #475569;
  --gray-700:  #334155;
  --gray-800:  #1E293B;
  --gray-900:  #0F172A;
}
```

### Contrast Hierarchy with Color Weight

Use color sparingly. Text hierarchy should be handled first by lightness (size/weight), then by color.

```css
/* Contrast hierarchy - color reserved for interactive elements */
.heading {
  color: var(--gray-900);  /* Darkest - highest contrast */
  font-weight: 700;
  font-size: 32px;
}

.body-text {
  color: var(--gray-700);  /* Dark - good contrast */
  font-weight: 400;
  font-size: 16px;
}

.secondary-text {
  color: var(--gray-500);  /* Medium - reduced contrast */
  font-weight: 400;
  font-size: 14px;
}

.button-primary {
  background-color: var(--blue-600);  /* Color for interactive elements */
  color: white;
}

.button-secondary {
  background-color: var(--gray-100);  /* Subtle background */
  color: var(--gray-900);
}
```

## Gestalt Principles: How Humans Perceive Visual Groups

Gestalt principles explain how humans naturally group visual elements. Use these to create clear hierarchy and organization.

### 1. Proximity

Elements that are close together are perceived as related.

**Application:**
- Group related items together
- Increase space between unrelated groups
- Use spacing to show relationships

```css
/* Proximity - group related items */
.form-group {
  margin-bottom: 24px;  /* Space between groups */
}

.form-group label {
  display: block;
  margin-bottom: 8px;  /* Close to input */
}

.form-group input {
  width: 100%;
}
```

### 2. Similarity

Elements that look similar are perceived as related.

**Application:**
- Use consistent styling for related items
- Vary styling to show differences
- Buttons of the same type should look identical

```css
/* Similarity - consistent styling for related items */
.button-primary {
  background: var(--blue-600);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
}

.button-primary:hover {
  background: var(--blue-700);
}

/* All primary buttons look the same */
.button-primary.small {
  padding: 8px 16px;
  font-size: 14px;
}
```

### 3. Figure/Ground

Humans naturally distinguish foreground from background.

**Application:**
- Use contrast to separate foreground from background
- Active states should stand out from inactive
- Modals should have clear distinction from background

```css
/* Figure/Ground - clear foreground/background separation */
.modal-overlay {
  background: rgba(0, 0, 0, 0.5);  /* Darkened background */
}

.modal {
  background: white;  /* Clear foreground */
  box-shadow: 0 20px 25px rgba(0, 0, 0, 0.1);
}

.button.active {
  background: var(--blue-600);  /* Foreground */
  color: white;
}

.button.inactive {
  background: var(--gray-100);  /* Background */
  color: var(--gray-600);
}
```

### 4. Closure

Humans complete incomplete shapes. Minimalist designs work because of this principle.

**Application:**
- Use negative space to imply forms
- Incomplete shapes are still perceived as complete
- Reduces visual clutter while maintaining clarity

```css
/* Closure - incomplete shapes are still perceived */
.icon-incomplete {
  width: 24px;
  height: 24px;
  border: 2px solid currentColor;
  border-right: none;
  border-bottom: none;
  /* Brain completes the square */
}
```

### 5. Symmetry & Order

Balanced layouts feel stable. Asymmetry draws attention.

**Application:**
- Use grids for stable, organized layouts
- Intentional asymmetry draws attention to important elements
- Symmetry creates trust and predictability

```css
/* Symmetry - stable, organized layout */
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

/* Asymmetry - draws attention */
.hero {
  display: grid;
  grid-template-columns: 1fr 1.5fr;  /* Unequal columns */
  gap: 48px;
  align-items: center;
}
```

### 6. Common Region

Boundaries create groupings. Enclosed areas are perceived as related.

**Application:**
- Use cards to group related content
- Use backgrounds or borders to define regions
- Sections with backgrounds feel grouped

```css
/* Common Region - boundaries create groupings */
.card {
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  padding: 24px;
  background: white;
  /* Everything inside is perceived as grouped */
}

.section-with-background {
  background: var(--gray-50);
  padding: 48px;
  border-radius: 12px;
  /* Content inside is grouped */
}
```

## Practical Refactoring: From Cluttered to Clear

### Before: Cluttered Interface

```css
/* Dense, hard to scan */
.old-interface {
  padding: 8px;
  margin: 4px;
}

.old-interface h2 {
  font-size: 16px;
  font-weight: 400;  /* Not bold */
  color: #666;  /* Medium grey */
  margin-bottom: 4px;
}

.old-interface p {
  font-size: 14px;
  color: #999;  /* Light grey */
  line-height: 1.3;
  margin-bottom: 4px;
}
```

### After: Clear Hierarchy

```css
/* Spacious, easy to scan */
.new-interface {
  padding: 48px;
  margin: 32px;
}

.new-interface h2 {
  font-size: 32px;
  font-weight: 700;  /* Bold */
  color: var(--gray-900);  /* Dark */
  margin-bottom: 16px;
}

.new-interface p {
  font-size: 16px;
  color: var(--gray-700);  /* Darker grey */
  line-height: 1.6;
  margin-bottom: 16px;
}
```

## How to Use This Skill with Claude Code

### Audit Visual Hierarchy

```
"I'm using the visual-hierarchy-refactoring skill. Can you audit my interface?
- Is my whitespace generous or cramped?
- Are my size differences clear?
- Am I using tinted greys or true greys?
- Do I apply Gestalt principles effectively?
- What's one thing I could improve immediately?"
```

### Refactor Cluttered Interfaces

```
"Can you help me refactor this cluttered interface using visual hierarchy principles?
- Increase whitespace
- Establish clear size hierarchy
- Use tinted greys instead of true greys
- Apply Gestalt principles for grouping
- Show me before/after comparison"
```

### Build a Color Weight System

```
"Can you help me build a color weight system?
- Create 8-10 shades for my brand color
- Create tinted greys for my brand
- Show me how to use them for hierarchy
- Provide CSS variables"
```

## Integration with Other Skills

- **design-foundation** — Design tokens for spacing and color
- **typography-system** — Size and weight hierarchy
- **color-system** — Color weight system and tinted greys
- **component-architecture** — Hierarchy in components
- **accessibility-excellence** — Contrast and readability

## Key Principles

**1. Size, Weight, Contrast First**
Establish hierarchy through these before using color.

**2. Whitespace is Active**
Generous spacing signals confidence and improves scannability.

**3. Tinted Greys, Not True Greys**
Colors should feel cohesive with your brand.

**4. Gestalt Principles Guide Perception**
Use proximity, similarity, and grouping to organize information.

**5. Hierarchy Should Be Obvious**
If you have to explain it, it's not clear enough.

## Checklist: Is Your Visual Hierarchy Ready?

- [ ] Whitespace is generous (not cramped)
- [ ] Size differences are clear (1.5-2x between levels)
- [ ] Weight hierarchy is consistent (2-3 weights max)
- [ ] Contrast hierarchy is clear (dark for primary, lighter for secondary)
- [ ] Greys are tinted to your brand (not true grey)
- [ ] Color is used sparingly (interactive elements only)
- [ ] Gestalt principles are applied (proximity, similarity, grouping)
- [ ] Information is easy to scan
- [ ] Hierarchy is obvious without explanation
- [ ] Interfaces feel spacious, not cramped

Clear visual hierarchy transforms interfaces from confusing to intuitive.
