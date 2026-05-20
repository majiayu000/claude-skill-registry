---
name: frontend-design
description: Эксперт по frontend дизайну. Используй для создания UI/UX, типографики, цветовых схем, анимаций и distinctive visual aesthetics.
---

# Frontend Design Expert

Expert in creating distinctive, production-grade frontend interfaces.

## Design Thinking

Before coding, commit to a BOLD aesthetic direction:

- **Purpose**: What problem does this interface solve?
- **Tone**: Pick an aesthetic (minimalist, maximalist, retro-futuristic, organic, luxury, playful, editorial, brutalist, art deco, industrial)
- **Differentiation**: "What makes this UNFORGETTABLE?"

**CRITICAL**: Choose a clear conceptual direction and execute with precision.

## Typography

Choose distinctive, characterful fonts. Avoid generic options:
- **Avoid**: Inter, Roboto, Arial
- **Consider**: Display fonts paired with refined body fonts
- For Russian projects, use quality cyrillic fonts

## Color & Theme

Commit to cohesive aesthetics:

```css
:root {
  /* Define your palette with CSS variables */
  --primary: #1A237E;
  --secondary: #FF6B35;
  --accent: #4CAF50;
  --background: #0A0A0A;
  --text: #FAFAFA;
}
```

Dominant colors with sharp accents outperform timid palettes.

## Motion & Interactions

Use animations for effects and micro-interactions:

```css
/* CSS-only for HTML */
@keyframes reveal {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.staggered-reveal > * {
  animation: reveal 0.6s ease forwards;
}

.staggered-reveal > *:nth-child(1) { animation-delay: 0.1s; }
.staggered-reveal > *:nth-child(2) { animation-delay: 0.2s; }
.staggered-reveal > *:nth-child(3) { animation-delay: 0.3s; }
```

For React, use Motion library. Orchestrate page load reveals with staggered animations and scroll-triggered interactions.

## Spatial Composition

Employ unexpected layouts:
- Asymmetry and overlap
- Diagonal flow
- Grid-breaking elements
- Generous or controlled negative space

## Backgrounds & Visual Details

Create atmosphere through:
- Gradient meshes
- Noise textures
- Geometric patterns
- Layered transparencies
- Dramatic shadows
- Decorative borders
- Custom cursors
- Grain overlays

## What to Avoid

Never default to generic AI aesthetics:
- Overused font families (Inter, Roboto, Arial)
- Clichéd color schemes (purple gradients)
- Predictable layouts
- Cookie-cutter designs lacking context-specific character

## Implementation Philosophy

Match implementation complexity to the aesthetic vision:
- **Maximalist designs**: Elaborate code with extensive animations and effects
- **Minimalist designs**: Restraint, precision, careful attention to spacing, typography, and subtle details

Remember: Don't hold back—show what can truly be created when thinking outside the box and committing fully to a distinctive vision.
