---
name: layout-system
description: Master responsive layout design using modern CSS (Flexbox, Grid), mobile-first approach, and breakpoint strategies. Create layouts that adapt beautifully across all devices while maintaining accessibility and performance. Includes container queries, aspect ratios, and advanced responsive patterns.
---

# Layout System

## Overview

Layout is the skeleton of your interface. It determines how content is organized, how users navigate, and how the experience adapts across devices. A well-designed layout system is invisible—users don't notice it because it works so well.

This skill teaches you to think about layout systematically, using modern CSS techniques (Flexbox, Grid, Container Queries) and a mobile-first approach that ensures your product works beautifully everywhere.

## Core Methodology: Mobile-First Responsive Design

The mobile-first approach is not just about making things smaller on mobile. It's a fundamental shift in thinking: start with the simplest, most constrained context (mobile), then progressively enhance for larger screens.

### Why Mobile-First?

1. **Constraints Drive Clarity** — Mobile forces you to prioritize. What's essential? What can wait? This clarity benefits all screen sizes.
2. **Progressive Enhancement** — Start with a solid foundation, then add complexity. This is more robust than trying to "shrink" a desktop design.
3. **Performance** — Mobile-first often results in faster, leaner code.
4. **Accessibility** — Simpler layouts are often more accessible.

### The Mobile-First Workflow

**Step 1: Design for Mobile (320px - 480px)**
- Single column layout
- Full-width content
- Touch-friendly targets (minimum 44x44px)
- Simplified navigation (hamburger menu, bottom nav)
- Prioritized content

**Step 2: Enhance for Tablet (481px - 768px)**
- Two-column layouts become possible
- Sidebar navigation
- Grid-based layouts (2-3 columns)
- Larger typography
- More whitespace

**Step 3: Optimize for Desktop (769px - 1024px)**
- Three-column layouts
- Sidebar + main content + sidebar
- Rich navigation
- Larger typography
- Generous whitespace

**Step 4: Maximize for Wide Screens (1025px+)**
- Four-column layouts
- Maximum content width (e.g., 1280px)
- Advanced grid layouts
- Optimal reading line length

## Modern Layout Techniques

### Technique 1: Flexbox for One-Dimensional Layouts

Flexbox is perfect for layouts that flow in one direction (row or column). Use it for:
- Navigation bars
- Button groups
- Card layouts
- Centering content
- Distributing space

**Key Flexbox Properties:**
- `flex-direction` — row (default) or column
- `justify-content` — Align items along the main axis (space-between, space-around, center, flex-start, flex-end)
- `align-items` — Align items along the cross axis (center, flex-start, flex-end, stretch)
- `gap` — Space between items
- `flex-wrap` — Wrap items to next line if needed
- `flex` — Shorthand for flex-grow, flex-shrink, flex-basis

**Example: Responsive Navigation**
```css
/* Mobile: Vertical stack */
nav {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Tablet and up: Horizontal */
@media (min-width: 768px) {
  nav {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
}
```

### Technique 2: CSS Grid for Two-Dimensional Layouts

Grid is perfect for layouts that need to align in both rows and columns. Use it for:
- Page layouts (header, sidebar, main, footer)
- Dashboard layouts
- Gallery layouts
- Complex component layouts

**Key Grid Properties:**
- `grid-template-columns` — Define column sizes
- `grid-template-rows` — Define row sizes
- `gap` — Space between items
- `grid-auto-flow` — How items flow (row or column)
- `grid-column` / `grid-row` — Position items in the grid
- `grid-template-areas` — Named grid areas for semantic layouts

**Example: Responsive Page Layout**
```css
/* Mobile: Single column */
body {
  display: grid;
  grid-template-columns: 1fr;
  grid-template-areas:
    "header"
    "main"
    "footer";
  gap: 1rem;
}

/* Tablet and up: Sidebar + main */
@media (min-width: 768px) {
  body {
    grid-template-columns: 250px 1fr;
    grid-template-areas:
      "header header"
      "sidebar main"
      "footer footer";
  }
}

/* Desktop: Sidebar + main + secondary */
@media (min-width: 1024px) {
  body {
    grid-template-columns: 250px 1fr 300px;
    grid-template-areas:
      "header header header"
      "sidebar main secondary"
      "footer footer footer";
  }
}
```

### Technique 3: Container Queries for Component-Level Responsiveness

Container queries allow components to respond to their container's size, not the viewport size. This is powerful for reusable components.

**Example: Responsive Card**
```css
/* Define a container context */
.card-container {
  container-type: inline-size;
}

/* Card responds to its container, not the viewport */
.card {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

/* When container is wider than 400px, use 2 columns */
@container (min-width: 400px) {
  .card {
    grid-template-columns: 1fr 1fr;
  }
}
```

### Technique 4: Aspect Ratio for Maintaining Proportions

Use `aspect-ratio` to maintain consistent proportions for images, videos, and other media.

```css
/* 16:9 aspect ratio (video) */
.video-container {
  aspect-ratio: 16 / 9;
  width: 100%;
}

/* 1:1 aspect ratio (square) */
.image-square {
  aspect-ratio: 1;
  width: 100%;
  object-fit: cover;
}

/* 4:3 aspect ratio (photo) */
.image-photo {
  aspect-ratio: 4 / 3;
  width: 100%;
  object-fit: cover;
}
```

## Responsive Breakpoint Strategy

Define breakpoints based on your content, not device sizes. Common breakpoints:

| Breakpoint | Size | Context | Use Case |
| :--- | :--- | :--- | :--- |
| xs | 320px - 480px | Small mobile | Single column, simplified |
| sm | 481px - 640px | Large mobile | Still mostly single column |
| md | 641px - 768px | Tablet (portrait) | Two columns possible |
| lg | 769px - 1024px | Tablet (landscape) / Small desktop | Three columns possible |
| xl | 1025px - 1280px | Desktop | Full layout |
| 2xl | 1281px+ | Large desktop | Maximum width containers |

**Tailwind CSS Breakpoints:**
```javascript
module.exports = {
  theme: {
    screens: {
      'xs': '320px',
      'sm': '640px',
      'md': '768px',
      'lg': '1024px',
      'xl': '1280px',
      '2xl': '1536px',
    },
  },
};
```

## Common Responsive Patterns

### Pattern 1: Hero Section
```html
<section class="hero">
  <div class="hero-content">
    <h1>Welcome</h1>
    <p>Your tagline here</p>
    <button>Get Started</button>
  </div>
  <div class="hero-image">
    <img src="hero.jpg" alt="Hero" />
  </div>
</section>
```

```css
/* Mobile: Single column, image below text */
.hero {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
  padding: 2rem 1rem;
}

/* Tablet and up: Two columns, image beside text */
@media (min-width: 768px) {
  .hero {
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    padding: 4rem 2rem;
    align-items: center;
  }
}
```

### Pattern 2: Card Grid
```html
<div class="card-grid">
  <div class="card"><!-- content --></div>
  <div class="card"><!-- content --></div>
  <div class="card"><!-- content --></div>
</div>
```

```css
/* Mobile: 1 column */
.card-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

/* Tablet: 2 columns */
@media (min-width: 768px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop: 3 columns */
@media (min-width: 1024px) {
  .card-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### Pattern 3: Sidebar + Main
```html
<div class="layout">
  <aside class="sidebar"><!-- navigation --></aside>
  <main class="main"><!-- content --></main>
</div>
```

```css
/* Mobile: Stacked */
.layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

/* Tablet and up: Sidebar beside main */
@media (min-width: 768px) {
  .layout {
    grid-template-columns: 250px 1fr;
    gap: 2rem;
  }
  
  .sidebar {
    position: sticky;
    top: 0;
    height: fit-content;
  }
}
```

### Pattern 4: Responsive Typography
```css
/* Mobile: Smaller text */
h1 {
  font-size: 24px;
  line-height: 1.2;
}

/* Tablet: Medium text */
@media (min-width: 768px) {
  h1 {
    font-size: 32px;
  }
}

/* Desktop: Larger text */
@media (min-width: 1024px) {
  h1 {
    font-size: 40px;
  }
}

/* Or use fluid typography */
h1 {
  font-size: clamp(24px, 5vw, 40px);
}
```

## Accessibility Considerations

### 1. Touch Targets
Ensure interactive elements are at least 44x44px (WCAG 2.5.5 Level AAA):

```css
button, a, input {
  min-width: 44px;
  min-height: 44px;
  padding: 0.75rem 1rem; /* Adjust as needed */
}
```

### 2. Reading Line Length
Optimal line length is 50-75 characters. Use max-width to constrain text:

```css
main {
  max-width: 65ch; /* ~65 characters */
  margin: 0 auto;
  padding: 0 1rem;
}
```

### 3. Whitespace and Breathing Room
Generous whitespace improves readability and reduces cognitive load:

```css
section {
  padding: 2rem 1rem; /* Mobile */
}

@media (min-width: 768px) {
  section {
    padding: 4rem 2rem; /* Tablet */
  }
}

@media (min-width: 1024px) {
  section {
    padding: 6rem 4rem; /* Desktop */
  }
}
```

### 4. Logical Tab Order
Ensure keyboard navigation follows a logical order:

```css
/* Use flexbox or grid order property to reorder visually without affecting tab order */
.item {
  order: 1; /* Visual order, doesn't affect tab order */
}

/* For tab order, use HTML source order or tabindex (use sparingly) */
```

## How to Use This Skill with Claude Code

### Audit Your Current Layout

```
"I'm using the layout-system skill. Can you audit my current layouts?
- Analyze my responsive behavior
- Check for accessibility issues (touch targets, line length, whitespace)
- Identify layouts that don't work well on mobile
- Suggest improvements"
```

### Create Responsive Layouts

```
"Can you create responsive layouts for:
- Hero section (mobile-first)
- Card grid (1 column mobile, 2 tablet, 3 desktop)
- Sidebar + main content
- Navigation bar (hamburger on mobile, horizontal on desktop)
- Footer"
```

### Implement Container Queries

```
"Can you help me implement container queries for my card component?
- Define container context
- Create responsive card layout based on container width
- Ensure accessibility"
```

### Test Responsive Behavior

```
"Can you create a responsive testing checklist?
- Mobile (320px, 480px)
- Tablet (768px)
- Desktop (1024px, 1280px)
- What to check at each breakpoint"
```

## Design Critique: Evaluating Your Layouts

Claude Code can critique your layouts:

```
"Can you evaluate my layouts?
- Are they truly mobile-first?
- Are touch targets large enough?
- Is the reading line length appropriate?
- Is there enough whitespace?
- Do they work well at all breakpoints?
- Are there any accessibility issues?"
```

## Integration with Other Skills

- **design-foundation** — Uses tokens for spacing and breakpoints
- **typography-system** — Responsive typography scales
- **component-architecture** — Responsive component layouts
- **accessibility-excellence** — Touch targets, reading line length, whitespace
- **interaction-design** — Responsive animations and transitions

## Key Principles

**1. Mobile-First is a Mindset**
Start simple, progressively enhance. This results in better products for everyone.

**2. Content Determines Breakpoints**
Don't use arbitrary breakpoints. Use breakpoints where your content needs them.

**3. Whitespace is Content**
Generous whitespace improves readability and reduces cognitive load.

**4. Flexibility Over Rigidity**
Use flexible units (%, em, rem) instead of fixed pixels. This allows your layout to adapt.

**5. Test on Real Devices**
Emulators are helpful, but test on real devices. Real network conditions, real touch, real performance.

## Checklist: Is Your Layout System Ready?

- [ ] All layouts are mobile-first
- [ ] Responsive breakpoints are defined and consistent
- [ ] Touch targets are at least 44x44px
- [ ] Reading line length is 50-75 characters
- [ ] Whitespace is generous and intentional
- [ ] Layouts work well at all breakpoints (test on real devices)
- [ ] Container queries are used for component-level responsiveness
- [ ] Aspect ratios are used for media
- [ ] Keyboard navigation works well
- [ ] Layouts are tested with screen readers
- [ ] Performance is good on slow networks and devices

A well-designed layout system is the foundation of a great experience across all devices.
