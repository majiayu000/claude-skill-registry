---
name: explainer-visuals
description: Create high-quality animated explainer visuals for essays and blog posts. Use when the user wants to visualize concepts, processes, data, or ideas with interactive web animations. Triggers on requests like "create a visual for", "animate this concept", "make an explainer", "visualize this idea", "diagram this process", "show this data", or when essay content would benefit from visual explanation. Handles abstract concepts (mental models, frameworks), technical processes (algorithms, systems), and data visualization (trends, comparisons). Outputs self-contained HTML/CSS/JS that embeds directly in web content.
---

# Explainer Visuals

Create animated, interactive visuals that make complex ideas intuitive.

## Philosophy

Great explainer visuals don't just illustrate—they *reveal*. They show the structure hidden in complexity, the motion implicit in static descriptions, the relationships that words struggle to convey.

**Core principles:**
- **Earned complexity**: Start simple, add layers through interaction or animation
- **Semantic motion**: Movement carries meaning, not just attention
- **Readable at rest**: The static state communicates the core idea
- **Progressive disclosure**: Let viewers control depth of exploration

## Discovery Process

Before creating any visual, conduct a brief discovery interview using AskUserQuestion. Understand not just WHAT to visualize, but WHY this idea needs visual treatment.

### Discovery Questions

Ask 1-2 focused questions from these categories:

**Understanding the idea:**
- "What's the single most important insight viewers should take away?"
- "What makes this concept hard to explain in words alone?"
- "Is there a common misconception this visual should correct?"

**Understanding the context:**
- "Where will this appear in your essay? (Opening hook, supporting evidence, climactic reveal, summary)"
- "What's the surrounding content's tone? (Academic, conversational, provocative, instructive)"

**Understanding the audience:**
- "What does your reader already know about this topic?"
- "Should this feel like a quick insight or an explorable deep-dive?"

Skip discovery only if the user has already provided rich context about their goals.

## Visual Format Selection

Choose format based on the nature of the idea:

| Concept Type | Optimal Format | Why |
|--------------|----------------|-----|
| **Transformation/Change** | Morphing animation | Shows before→after as continuous process |
| **Hierarchy/Structure** | Zoomable treemap or nested diagram | Reveals layers through interaction |
| **Process/Flow** | Stepped animation with scrubber | User controls pace of revelation |
| **Comparison** | Side-by-side with synchronized animation | Parallel structure highlights differences |
| **Accumulation/Growth** | Building animation | Each element adds to previous |
| **Relationship/Network** | Force-directed graph | Reveals emergent structure |
| **Distribution/Proportion** | Animated unit chart or waffle | Makes quantities tangible |
| **Cycle/Feedback** | Looping animation with entry points | Shows perpetual motion of systems |
| **Timeline/Sequence** | Horizontal scroll with annotations | Natural reading direction |
| **Spatial/Geographic** | Annotated map with zoom | Grounds abstract in physical |
| **Mental Model** | Metaphor-based diagram | Connects abstract to familiar |
| **Trade-off/Tension** | Slider-controlled balance | Shows interdependence |

## Design System

### Typography
```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;

--text-hero: 2rem;      /* Single key number or word */
--text-title: 1.25rem;  /* Visual title */
--text-label: 0.875rem; /* Axis labels, annotations */
--text-micro: 0.75rem;  /* Secondary details */
```

### Color Palettes

**Minimal (default):**
```css
--ink: #1a1a2e;        /* Primary elements */
--ink-light: #4a4a68;  /* Secondary elements */
--accent: #e94560;     /* Single highlight */
--ground: #fafafa;     /* Background */
--ground-alt: #f0f0f5; /* Alternate regions */
```

**Data-rich (when showing categories):**
```css
--cat-1: #4e79a7; --cat-2: #f28e2c; --cat-3: #e15759;
--cat-4: #76b7b2; --cat-5: #59a14f; --cat-6: #af7aa1;
```

**Adapt to essay context:**
- Technical/analytical → cooler palette, more contrast
- Personal/reflective → warmer palette, softer edges
- Provocative/challenging → bolder accent, higher saturation

### Motion Principles

```javascript
const EASE = {
  standard: 'cubic-bezier(0.4, 0, 0.2, 1)',  // Smooth, natural
  enter: 'cubic-bezier(0, 0, 0.2, 1)',       // Start fast, settle
  exit: 'cubic-bezier(0.4, 0, 1, 1)',        // Start slow, accelerate
  bounce: 'cubic-bezier(0.34, 1.56, 0.64, 1)' // Slight overshoot
};

const DURATION = {
  micro: 100,    // Color, opacity
  fast: 200,     // Small movements
  medium: 350,   // Standard transitions
  slow: 500,     // Large movements
  dramatic: 800  // Major reveals
};
```

**Motion semantics:**
- **Fade** = existence (appear/disappear)
- **Scale** = importance (emphasize/de-emphasize)
- **Translate** = relationship (group/separate)
- **Morph** = identity (transform)
- **Rotate** = state (toggle, cycle)

## Technology Selection

Choose the simplest tool that achieves the effect:

| Complexity | Tool | Use When |
|------------|------|----------|
| Simple | Pure CSS | State transitions, hovers, basic transforms |
| Standard | Vanilla JS + CSS | Sequenced animations, scroll triggers, simple interactions |
| Complex | GSAP | Timeline sequences, physics, SVG morphing |
| Data-driven | D3.js | Force layouts, maps, data-bound transitions |

For most explainer visuals, vanilla JS + CSS is sufficient.

## Code Structure

Every visual is a self-contained HTML file:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Visual: [Concept Name]</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root { /* Design tokens */ }
    /* Component styles */
  </style>
</head>
<body>
  <figure class="explainer-visual" role="img" aria-label="[Description]">
    <!-- Visual content -->
    <figcaption class="visually-hidden">[Accessible description]</figcaption>
  </figure>
  <script>
    // Animation and interaction logic
  </script>
</body>
</html>
```

### Accessibility Requirements

```css
.visually-hidden {
  position: absolute; width: 1px; height: 1px;
  padding: 0; margin: -1px; overflow: hidden;
  clip: rect(0, 0, 0, 0); border: 0;
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

Every visual must include:
1. `role="img" aria-label="..."` on container
2. Full text alternative in `.visually-hidden` caption
3. Respect `prefers-reduced-motion`
4. Keyboard-accessible interactions
5. Visible focus states

## Patterns Reference

See [references/patterns.md](references/patterns.md) for implementation patterns:
- Morphing shape transitions
- Scroll-driven storytelling
- Interactive slider diagrams
- Annotated step-through animations
- Force-directed relationship graphs
- Unit/waffle chart animations

## Delivery

Output as single HTML file that:
1. Is completely self-contained (inline all CSS/JS)
2. Works when opened directly in browser
3. Can be embedded via iframe
4. Includes comments explaining key decisions

For library-dependent visuals (D3, GSAP), include CDN links with integrity hashes.

## Quality Checklist

Before delivering:

- [ ] Static state communicates the core idea
- [ ] Animation reveals insight, not just decorates
- [ ] Interactions are discoverable (cursor hints, hover states)
- [ ] Works on mobile (touch-friendly, responsive)
- [ ] Reduced motion alternative exists
- [ ] Accessible description is complete
- [ ] Code is commented for future modification
- [ ] File size reasonable (<100KB simple, <500KB complex)
