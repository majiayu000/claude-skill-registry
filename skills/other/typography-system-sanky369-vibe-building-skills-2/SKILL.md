---
name: typography-system
description: Master typography design with font selection, type scales, hierarchy, readability, and accessibility. Create consistent, beautiful typography that works across all devices and contexts. Includes modular scales, fluid typography, variable fonts, and accessibility best practices.
---

# Typography System

## Overview

Typography is the voice of your interface. It communicates hierarchy, establishes tone, and guides users through your content. Great typography is invisible—users don't notice it because it works so well.

This skill teaches you to think about typography systematically: choosing fonts with intention, creating scales that feel natural, establishing clear hierarchy, and ensuring readability and accessibility across all contexts.

## Core Methodology: Type Scales and Hierarchy

Rather than choosing font sizes arbitrarily, use a **modular scale**—a mathematical progression of sizes that feels harmonious and intentional.

### Modular Scales

A modular scale is a sequence of sizes derived from a base size and a ratio. Common ratios:

| Ratio | Name | Use Case | Example (16px base) |
| :--- | :--- | :--- | :--- |
| 1.125 | Major Second | Subtle, minimal | 16, 18, 20, 23, 26, 29, 33, 37, 42, 47 |
| 1.25 | Major Third | Balanced, harmonious | 16, 20, 25, 31, 39, 49, 61, 76, 95 |
| 1.5 | Perfect Fifth | Bold, dramatic | 16, 24, 36, 54, 81, 122 |
| 1.618 | Golden Ratio | Natural, elegant | 16, 26, 42, 68, 110 |

**Choosing a Scale:**
- **1.125 (Major Second)** — For subtle, minimal designs
- **1.25 (Major Third)** — For balanced, harmonious designs (most common)
- **1.5 (Perfect Fifth)** — For bold, dramatic designs
- **1.618 (Golden Ratio)** — For natural, elegant designs

**Example: Major Third Scale (1.25 ratio)**
```
Base: 16px
Scale: 16, 20, 25, 31, 39, 49, 61, 76, 95

Practical sizes:
- Caption: 12px (smaller than base)
- Body: 16px (base)
- Body Large: 18px (between base and next)
- Heading 6: 20px
- Heading 5: 25px
- Heading 4: 31px
- Heading 3: 39px
- Heading 2: 49px
- Heading 1: 61px
- Display: 76px (for hero sections)
```

### Implementing Type Scales in Tailwind

```javascript
module.exports = {
  theme: {
    fontSize: {
      // Captions and small text
      'xs': ['12px', { lineHeight: '1.5' }],
      'sm': ['14px', { lineHeight: '1.5' }],
      
      // Body text
      'base': ['16px', { lineHeight: '1.6' }],
      'lg': ['18px', { lineHeight: '1.6' }],
      
      // Headings (modular scale 1.25)
      'h6': ['20px', { lineHeight: '1.3', fontWeight: '600' }],
      'h5': ['25px', { lineHeight: '1.3', fontWeight: '600' }],
      'h4': ['31px', { lineHeight: '1.2', fontWeight: '700' }],
      'h3': ['39px', { lineHeight: '1.2', fontWeight: '700' }],
      'h2': ['49px', { lineHeight: '1.1', fontWeight: '700' }],
      'h1': ['61px', { lineHeight: '1.1', fontWeight: '700' }],
      
      // Display (for hero sections)
      'display': ['76px', { lineHeight: '1', fontWeight: '800' }],
    },
  },
};
```

## Font Selection

### Choosing Fonts

**Font Pairing Principles:**
1. **Contrast** — Pair fonts with different characteristics (serif + sans-serif, or geometric + humanist)
2. **Personality Match** — Fonts should match your brand personality
3. **Readability** — Prioritize readability over style
4. **Versatility** — Fonts should work across sizes and weights

### Common Font Pairings

| Heading Font | Body Font | Personality | Use Case |
| :--- | :--- | :--- | :--- |
| Playfair Display | Inter | Elegant, sophisticated | Luxury, editorial |
| Montserrat | Open Sans | Modern, geometric | Tech, SaaS |
| Merriweather | Lato | Warm, friendly | Publishing, lifestyle |
| Space Mono | Space Grotesk | Futuristic, technical | Developer tools, tech |
| Poppins | Poppins | Contemporary, friendly | Startups, consumer apps |

### Font Loading Strategy

Use system fonts first, then web fonts as fallback:

```css
/* System fonts (fast, no network request) */
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;

/* Or use web fonts (Google Fonts, Typekit, etc.) */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

body {
  font-family: 'Inter', system-ui, sans-serif;
}
```

**Font Loading Best Practices:**
- Use `font-display: swap` to avoid invisible text while fonts load
- Preload critical fonts: `<link rel="preload" as="font" href="font.woff2" crossorigin>`
- Limit to 2-3 font families and 3-4 weights
- Use variable fonts to reduce file size

## Hierarchy and Emphasis

### Creating Visual Hierarchy

Use these properties to create hierarchy:

1. **Size** — Larger text is more prominent
2. **Weight** — Bolder text is more prominent
3. **Color** — Brighter or more saturated colors are more prominent
4. **Spacing** — More space around text makes it more prominent
5. **Position** — Top-left is more prominent than bottom-right

**Example: Hierarchy in a Card**
```html
<div class="card">
  <h2 class="card-title">Card Title</h2>
  <p class="card-description">This is a description of the card content.</p>
  <p class="card-meta">Published on January 16, 2026</p>
</div>
```

```css
.card-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.card-description {
  font-size: 16px;
  font-weight: 400;
  color: var(--text-primary);
  line-height: 1.6;
  margin-bottom: 1rem;
}

.card-meta {
  font-size: 14px;
  font-weight: 400;
  color: var(--text-secondary);
  line-height: 1.5;
}
```

### Emphasis Techniques

- **Bold** — Use for emphasis, not entire paragraphs
- **Italic** — Use for citations, asides, or emphasis
- **Color** — Use to highlight important information
- **ALL CAPS** — Use sparingly for labels or buttons
- **Underline** — Use only for links (to avoid confusion)

## Readability and Accessibility

### Line Height

Line height affects readability. Tighter line heights for headings, looser for body text:

```css
h1, h2, h3 {
  line-height: 1.2; /* Tight for headings */
}

p, li {
  line-height: 1.6; /* Loose for body text */
}

.caption {
  line-height: 1.4; /* Medium for captions */
}
```

### Line Length

Optimal line length is 50-75 characters. Too long and reading becomes difficult:

```css
main {
  max-width: 65ch; /* ~65 characters */
}
```

### Letter Spacing

Adjust letter spacing for different contexts:

```css
h1 {
  letter-spacing: -0.02em; /* Tighter for large headings */
}

.label {
  letter-spacing: 0.05em; /* Looser for labels */
}

.caption {
  letter-spacing: 0; /* Normal for body text */
}
```

### Text Contrast

Ensure sufficient contrast for readability (WCAG AA: 4.5:1 for normal text, 3:1 for large text):

```css
/* Good contrast */
color: #030712; /* dark text */
background-color: #F9FAFB; /* light background */
/* Contrast ratio: 19:1 ✓ */

/* Poor contrast */
color: #9CA3AF; /* medium gray text */
background-color: #F9FAFB; /* light background */
/* Contrast ratio: 2.5:1 ✗ */
```

### Responsive Typography

Use fluid typography to scale smoothly across devices:

```css
/* Fixed sizes (old approach) */
h1 {
  font-size: 24px; /* mobile */
}

@media (min-width: 768px) {
  h1 {
    font-size: 32px; /* tablet */
  }
}

@media (min-width: 1024px) {
  h1 {
    font-size: 40px; /* desktop */
  }
}

/* Fluid typography (modern approach) */
h1 {
  font-size: clamp(24px, 5vw, 40px);
  /* min: 24px, preferred: 5% of viewport width, max: 40px */
}
```

## Advanced Typography Techniques

### Variable Fonts

Variable fonts allow multiple weights and styles in a single file:

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap');

body {
  font-family: 'Inter', sans-serif;
  font-weight: 400;
}

strong {
  font-weight: 600;
}

.light {
  font-weight: 300;
}
```

### Font Features

Use OpenType features for advanced typography:

```css
/* Ligatures (fi, fl, etc.) */
body {
  font-feature-settings: 'liga' 1;
}

/* Tabular numbers (for tables) */
.table {
  font-feature-settings: 'tnum' 1;
}

/* Small caps */
.label {
  font-feature-settings: 'smcp' 1;
}
```

## Common Typography Patterns

### Pattern 1: Article Typography
```css
article {
  font-size: 18px;
  line-height: 1.7;
  max-width: 65ch;
  margin: 0 auto;
  padding: 2rem 1rem;
}

article h1 {
  font-size: 49px;
  line-height: 1.1;
  margin-bottom: 1rem;
  margin-top: 2rem;
}

article h2 {
  font-size: 39px;
  line-height: 1.2;
  margin-bottom: 0.75rem;
  margin-top: 1.5rem;
}

article p {
  margin-bottom: 1.5rem;
}

article a {
  color: var(--interactive-primary);
  text-decoration: underline;
}
```

### Pattern 2: UI Typography
```css
/* Buttons */
button {
  font-size: 16px;
  font-weight: 600;
  line-height: 1.5;
  letter-spacing: 0;
}

/* Labels */
label {
  font-size: 14px;
  font-weight: 500;
  line-height: 1.4;
  letter-spacing: 0.05em;
}

/* Captions */
.caption {
  font-size: 12px;
  font-weight: 400;
  line-height: 1.4;
  color: var(--text-secondary);
}
```

### Pattern 3: Responsive Headings
```css
h1 {
  font-size: clamp(24px, 5vw, 61px);
  line-height: 1.1;
  font-weight: 700;
}

h2 {
  font-size: clamp(20px, 4vw, 49px);
  line-height: 1.2;
  font-weight: 700;
}

h3 {
  font-size: clamp(18px, 3vw, 39px);
  line-height: 1.2;
  font-weight: 600;
}
```

## How to Use This Skill with Claude Code

### Create a Type Scale

```
"I'm using the typography-system skill. Can you create a type scale for me?
- Base font size: 16px
- Ratio: 1.25 (Major Third)
- Font family: Inter for body, Playfair Display for headings
- Include sizes for: captions, body, headings, display
- Ensure accessibility (contrast, line height, line length)"
```

### Audit Your Typography

```
"Can you audit my current typography?
- Are my font sizes following a modular scale?
- Is my line height appropriate?
- Is my line length too long?
- Are my color contrasts sufficient?
- Are my fonts accessible?
- What improvements would you suggest?"
```

### Implement Responsive Typography

```
"Can you help me implement responsive typography?
- Create fluid typography using clamp()
- Ensure readability at all breakpoints
- Test at mobile (320px), tablet (768px), desktop (1024px)
- Provide CSS code I can use"
```

### Create Typography Documentation

```
"Can you create comprehensive typography documentation?
- Type scale with all sizes
- Font pairings and usage
- Hierarchy guidelines
- Accessibility guidelines
- Code examples for each style
- Responsive behavior"
```

## Design Critique: Evaluating Your Typography

Claude Code can critique your typography:

```
"Can you evaluate my typography?
- Is my type scale harmonious?
- Is my hierarchy clear?
- Is my readability good?
- Are my color contrasts sufficient?
- Are my fonts accessible?
- What's one thing I could improve immediately?"
```

## Integration with Other Skills

- **design-foundation** — Typography tokens and scales
- **layout-system** — Responsive typography scales
- **color-system** — Text color and contrast
- **component-architecture** — Typography in components
- **accessibility-excellence** — Font sizes, contrast, line height
- **interaction-design** — Typography in animations

## Key Principles

**1. Type Scale Brings Harmony**
A modular scale feels natural and intentional. It's the foundation of great typography.

**2. Hierarchy Guides Users**
Clear hierarchy helps users understand what's important and what to read next.

**3. Readability is Non-Negotiable**
Beautiful typography that's hard to read is not beautiful. Readability comes first.

**4. Accessibility is Foundational**
Font sizes, contrast, and line height must meet accessibility standards.

**5. Consistency Builds Trust**
Consistent typography across your product builds trust and reduces cognitive load.

## Checklist: Is Your Typography System Ready?

- [ ] Type scale is defined and modular
- [ ] Font families are chosen with intention
- [ ] Font sizes are consistent across components
- [ ] Line heights are appropriate for context
- [ ] Line length is 50-75 characters for body text
- [ ] Color contrast meets WCAG AA standards
- [ ] Hierarchy is clear and intentional
- [ ] Responsive typography uses fluid scaling
- [ ] Fonts are loaded efficiently
- [ ] Typography works well on all devices
- [ ] Typography is documented and shared with the team

Great typography is the voice of your interface. Make it count.
