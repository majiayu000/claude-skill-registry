---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

The Smart Combination Approach
Use relative units as your foundation, with strategic pixel usage for specific cases:
✅ Use Relative Units For:
Typography & Spacing (rem/em)
css/* Root sizing - easy to scale entire UI */
html { font-size: 16px; } /* base */

/* Component scales automatically */
.card {
  padding: 1.5rem;        /* 24px at base, scales with root */
  font-size: 1rem;        /* 16px at base */
  margin-bottom: 2rem;    /* 32px at base */
}

/* Media query just changes root */
@media (max-width: 768px) {
  html { font-size: 14px; } /* Everything shrinks proportionally */
}
Layout widths (%, max-width)
css.container {
  width: 100%;           /* Fluid */
  max-width: 75rem;      /* 1200px cap */
  padding: 0 5%;         /* Breathing room on all screens */
}
Viewport-based (vh/vw) - use sparingly
css.hero {
  min-height: 100vh;     /* Full screen sections */
  padding: 5vw;          /* Scales with viewport */
}
🎯 Use Pixels For:

Borders & fine details: border: 1px solid (0.0625rem looks weird)
Icons with fixed dimensions: width: 24px; height: 24px;
Media query breakpoints: @media (min-width: 768px) (industry standard)
Shadows: box-shadow: 0 2px 4px rgba(0,0,0,0.1)

TailwindCSS Context (Your Stack)
Tailwind uses rem by default - perfect combo already built-in:
tsx// Tailwind's spacing scale is in rem
<div className="p-4 mb-6 text-base">  
  {/* p-4 = 1rem, mb-6 = 1.5rem, text-base = 1rem */}
</div>

// Percentage widths
<div className="w-full md:w-1/2 lg:w-1/3">
  {/* Fluid responsive columns */}
</div>

// Max-width constraints
<div className="max-w-7xl mx-auto px-4">
  {/* Centers content, caps width, fluid padding */}
</div>
Modern Mobile-First Pattern
tsx// App component example
export function AssetCard() {
  return (
    <div className="
      w-full              /* Mobile: full width */
      sm:w-[calc(50%-1rem)]  /* Tablet: 2 columns */
      lg:w-[calc(33.333%-1rem)] /* Desktop: 3 columns */
      p-6                 /* rem-based padding */
      rounded-lg          /* Fixed border radius */
      border border-gray-200 /* 1px border */
    ">
      <h3 className="text-lg font-semibold mb-2">
        {/* rem-based text sizing */}
      </h3>
    </div>
  );
}