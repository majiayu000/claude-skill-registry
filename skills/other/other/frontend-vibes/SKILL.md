---
name: frontend-vibes
description: Create distinctive frontend interfaces with faux-ASCII aesthetic, warm dark palettes, and expressive motion. Use when user mentions ASCII art, dot matrix, scanline effects, terminal aesthetic, pixelated figures, block letterforms, "vibes", "make it vibes", "use the aesthetic from frontend-vibes", warm blacks, terracotta accents, Anthropic-adjacent design, technical romance, or wants emotionally expressive UI that balances precision with organic imperfection.
license: MIT
---

This skill guides creation of distinctive, emotionally expressive frontend interfaces that balance technical precision with organic imperfection. Build React + TypeScript + Tailwind applications with faux-ASCII aesthetics, warm dark palettes, spring-based motion, and Anthropic-adjacent design sensibility.

## Core Identity: Technical Precision Meets Organic Imperfection

The essence of this aesthetic lives in a productive tension: **technical precision meets organic imperfection**. The grid exists, but something breaks out of it. Type is clean, but rendered in dots or blocks. Palettes are restrained, but punctuated with jarring accents that make everything sing.

**Expressive by Design**: Create interfaces that make users feel something. Research shows expressive design helps users spot key elements 4x faster while inspiring emotional connection through strategic use of color, shape, size, motion, and containment. Balance emotional engagement with functional clarity—never sacrifice core usability for visual appeal.

**The Feeling**: Confidence of someone who knows what they're doing, expressed through restraint rather than excess. Technical but not cold. Modern but referencing history. Clean but with texture. Serious but with moments of play.

**When to Use**: Creative portfolios, developer tools, design systems, technical documentation, AI/LLM interfaces, anything wanting a distinctive voice. The constraint (faux-ASCII, warm palettes, spring motion) becomes the style.

## Design Elements Framework

Map Material Design's five expressive elements to this distinctive aesthetic:

**1. Color as Expression**
Strategic color use draws attention and conveys emotion. Prefer dark foundations (warm blacks with olive/brown undertones) punctuated by vibrant accents (electric orange, coral, neon green). The 90/10 rule: 90% restrained background, 10% vibrant accent doing all the emotional work.

**2. Shape as Identity**
Distinctive forms create visual memory. Employ faux-ASCII shapes (block letterforms built from rectangles, pixelated figures, geometric patterns), scanline overlays, dot matrix compositions, and technical construction lines that reveal the design process.

**3. Size as Hierarchy**
Proportional emphasis establishes importance. Use dramatic scale jumps: 48-80px bold headlines (700-900 weight) contrasted with restrained 14-16px body (400 weight). The gap between them IS the design.

**4. Motion as Guide**
Dynamic transitions direct attention. Prefer spring-based physics over easing curves—animations that bounce slightly feel alive and intentional. Reserve expressive motion for hero moments and key interactions.

**5. Containment as Organization**
Visual grouping creates clarity. Use bento grid layouts where each card has different proportions, dark sections as punctuation in light pages, generous negative space (60-120px padding), and asymmetric compositions that guide the eye.

## Color Philosophy: Restraint with Punctuation

**Dark Foundations**
Prefer warm blacks with subtle olive or brown undertones over pure black (#000000). Think #131313 to #1a1a1a with slight warmth. Avoid cold, blue-tinted blacks—they read sterile. The background should feel like comfortable night.

When going light, avoid pure white (#ffffff). Use cream, warm gray, or paper tones (#faf8f6, #faf9f5, #f5f4ed). Pure white reads clinical; warm white reads considered.

**The Accent That Cuts Through**
Almost every composition needs ONE color doing all the work:
- Electric orange / coral family (Anthropic-adjacent: terracotta, burnt orange, rust, sienna)
- Neon green / lime (technical energy)
- Hot coral / salmon (approachable warmth)
- Cyan / teal scanlines (retrofuture)

**Anthropic-Adjacent Palette Harmony**
Rhyme with Anthropic's design language without copying:
- Their terracotta (#d97757) → Use burnt orange, rust, sienna tones
- Their olive-tinted darks (#252523, #30302e) → Use similar warm blacks with green/brown undertones
- Their parchment whites (#faf9f5, #f5f4ed) → Use same cream/warm white family
- Their soft lavender (#827dbd) → Use sparingly or skip

**The Formula**
```
Dark mode:  90% warm dark background + 10% vibrant accent
Light mode: Warm off-white + strategic dark type + one accent
```

Prefer limited palettes. Single color family with variations, or 2-3 deliberately chosen colors. Reduces cognitive load and creates premium, focused appearance.

Avoid rainbow palettes, gradients for gradient's sake, or default "startup blue". Commit to a cohesive position: bold and saturated, moody and restrained, or high-contrast and minimal.

## Typography & Display Type: Constraint as Style

**Display Type Treatments**
Typography carries the design's voice. Prefer interesting personality over default thinking—avoid Arial, Inter, Roboto, system stacks. Display type should be expressive, even risky. Font choices should be inseparable from the aesthetic direction.

**Faux-ASCII Rendering Techniques:**
- **Block/Pixel Construction**: Characters built from rectangles and squares. Chunky, pixelated display type with weight and presence (like digital brutalism)
- **Scanline Effects**: Horizontal lines through letterforms, as if reading through a CRT monitor or venetian blind
- **Dot Matrix Rendering**: Type as halftone or stippled dots. The constraint makes it handmade even when digital
- **Outline with Filled Interior**: Layered technical feel showing construction

**Figlet for Big Headers**
Use the figlet npm package (https://www.npmjs.com/package/figlet) to render large ASCII art text. Creates impactful headers with retro terminal aesthetic. Works well for hero sections, section dividers, and page titles.

**Scale & Hierarchy**
- Headlines: 48-80px, weight 700-900, tight line-height (1.2-1.3)
- Subheadings: 32-44px, weight 600-700
- Body: 14-16px, weight 400, restrained
- Small text: 12-13px, weight 400-500

The gap between display and body creates visual tension. Let dramatic scale jumps establish hierarchy—one well-proportioned headline does more than scattered emphasis.

**Body Type Philosophy**
Clean, legible, stays out of the way. Display type talks; body type listens. Maintain clear visual distinction between content levels through weight contrast (700-900 headlines vs 400 body).

## Shape & Form: Distinctive Forms as Identity

**Geometric Technical Forms**
Embrace shapes that reference early computing and technical drawing:
- Pixelated figures and imagery (running figures, robots, portraits rendered through halftone)
- Block letterforms with visible construction
- Isometric perspectives and connected systems
- Abstract data visualizations as landscape
- Construction lines and guides that remain visible (showing the design process)

**Illustration Style: Technical Romance**
Illustrations should live in the space between technical precision and human warmth—smart enough to feel credible, warm enough to feel approachable.

Prefer line art with intention (single-weight strokes, isometric views, connected systems), dot/pixel compositions (constraint as style), geometric construction visible (circles and guides that built the form), and abstract data visualizations (not charts, but visual data as landscape).

Avoid blob people, generic SaaS illustrations, overly detailed 3D renders, and stock photography (almost never).

## Layout & Containment: Confident Space

**Breathing Room as Feature**
Interfaces should not fear emptiness. Generous spacing creates premium feel and improves scanability.

- Section padding: 60-120px top/bottom
- Max-width content containers: 1200-1400px, centered on large screens
- Horizontal padding: 20-40px on sides for small screens
- Vertical rhythm: Consistent spacing intervals (multiples of 8px or 16px)
- Margin below headings: 20-40px
- Margin below body blocks: 16-24px

**Bento Grid Layouts**
Feature grids where each card is different size and proportion. Creates visual interest through asymmetry while maintaining organizational clarity. Not everything needs to be the same height.

**See also:** `examples/bento-grid-layout.tsx` for complete implementation with varied card sizes, spring animations, and warm accents.

**Asymmetry with Purpose**
The 50/50 split is fine, but 60/40 is more interesting. Text heavy on left with visual on right (or vice versa). Let content weight create natural pull.

**Full-Bleed Moments**
Some sections should extend edge-to-edge. Creates rhythm through alternation. A dark section in a light page (or light in dark) creates natural hierarchy without needing explicit headers.

**The Layout Pattern**
```
Hero (full-bleed) → Feature cards (contained) →
Dark section (full-bleed) → Content grid (contained) →
Call-to-action (full-bleed)
```

Alternate between contained and full-bleed to create visual rhythm and guide attention.

## Expressive Motion System: Physics Over Duration

**Spring-Based Physics**
Replace traditional easing curves and durations with spring physics. Animations feel more fluid, natural, and alive when defined by physical properties rather than fixed timings.

**Core Properties:**
- **Stiffness**: How quickly animation resolves to final state. Higher stiffness = faster, more energetic motion
- **Damping Ratio**: How quickly bounce/oscillation decays. Ratio of 1 = critically damped (no bounce). Lower values = more overshoot

**Two Motion Schemes:**

**Expressive Motion (Recommended Default)**
Use springs with lower damping, creating noticeable overshoot and bounce. Well-suited for:
- Hero moments and key interactions
- Creative portfolio work
- Design tool interfaces
- Page transitions
- Playful, spirited feel

**Standard Motion (Functional Restraint)**
Use higher damping for subdued motion with minimal bounce. Appropriate for:
- Utilitarian applications
- Financial/banking interfaces
- Technical dashboards
- Data-heavy applications
- Calmer, functional feel

**Implementation with Framer Motion**
Prefer Framer Motion for React animations with spring physics:

```typescript
import { motion } from "framer-motion";

// Expressive spring
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{
    type: "spring",
    stiffness: 260,
    damping: 20  // Lower damping = more bounce
  }}
>

// Standard spring
<motion.div
  transition={{
    type: "spring",
    stiffness: 300,
    damping: 30  // Higher damping = less bounce
  }}
>
```

**When to Use Motion:**
Prioritize high-impact moments over scattered micro-interactions. One well-orchestrated page load with staggered reveals (using animation-delay) creates more delight than everything bouncing. Use scroll-triggering and hover states that surprise.

Focus on entrance animations, state transitions, and user feedback. Reserve expressive bounce for moments that deserve attention.

**See also:** `references/motion-physics-guide.md` for comprehensive spring parameter tuning, advanced patterns, debugging, and performance optimization.

## Animated ASCII Art: 2D Video/Image to ASCII Grid

**Conceptual Approach**
For performant 2D ASCII animation from video or images, use **PixiJS** (2D WebGL renderer) rather than DOM manipulation. Rendering individual characters as DOM elements won't perform at scale.

**High-Level Implementation Pattern:**

```typescript
// 1. Create custom Pixi Filter (fragment shader)
// Samples video/image texture, computes luminance,
// quantizes to grid, picks glyph from sprite-sheet atlas

const asciiFilter = new Filter(
  undefined,
  fragmentShaderCode,  // GLSL shader
  {
    resolution: { x: width, y: height },
    cellSize: 8,  // ASCII cell size in pixels
    time: 0       // For animation
  }
);

// 2. Render with @pixi/react
import { Stage, Sprite } from "@pixi/react";

<Stage width={800} height={450}>
  <Sprite
    texture={videoTexture}
    filters={[asciiFilter]}
  />
</Stage>

// 3. Animate by updating uniforms each frame
useTick((delta) => {
  asciiFilter.uniforms.time += delta * 0.05;
});
```

**Key Concepts:**
- Fragment shader computes luminance and quantizes to ASCII grid
- Sprite-sheet atlas technique for glyph rendering (classic approach)
- Update shader uniforms (time, resolution, cellSize, palette) per frame via Pixi ticker
- Layer GSAP on top for orchestrated transitions (palette fades, zoom, glitches)

**Resources:**
- PixiJS: https://pixijs.com
- @pixi/react: https://react.pixijs.io
- For raw WebGL approach: regl (https://regl-project.github.io/regl) + react-regl

This technique scales to video-rate performance where DOM-based approaches fail.

**See also:**
- `references/advanced-ascii-animation.md` for complete implementations with Three.js and regl, advanced effects (scanlines, dithering), performance optimization, and troubleshooting
- `examples/ascii-text-effect.tsx` for figlet-based ASCII text components with typewriter and glitch effects

## Backgrounds & Visual Details: Atmosphere and Depth

**Textured Backgrounds**
Avoid defaulting to solid colors. Create atmosphere through contextual effects:

- Gradient meshes (smooth color transitions)
- Noise and grain overlays (print-inspired texture)
- Geometric patterns (dots, grids, lines)
- Layered transparencies and glassmorphism
- Dramatic or soft shadows and glows
- Parallax depth between layers
- Decorative borders and clip-path shapes
- Print-inspired textures (halftone, duotone, stipple)
- Knockout typography (text revealing background)
- Custom cursors for interactive moments

**Component Libraries for Effects**
Reference these Aceternity UI and Magic UI components for modern background and interaction patterns:

**Backgrounds:**
- https://ui.aceternity.com/components/dotted-glow-background
- https://ui.aceternity.com/components/background-ripple-effect
- https://ui.aceternity.com/components/background-boxes
- https://ui.aceternity.com/components/background-beams
- https://ui.aceternity.com/components/glowing-stars-effect
- https://ui.aceternity.com/components/grid-and-dot-backgrounds
- https://magicui.design/docs/components/flickering-grid
- https://magicui.design/docs/components/retro-grid
- https://magicui.design/docs/components/light-rays
- https://magicui.design/docs/components/warp-background

**Borders & Effects:**
- https://ui.aceternity.com/components/glowing-effect
- https://ui.aceternity.com/components/hover-border-gradient
- https://magicui.design/docs/components/border-beam
- https://magicui.design/docs/components/shine-border

**Text Animation:**
- https://ui.aceternity.com/components/text-generate-effect
- https://ui.aceternity.com/components/typewriter-effect
- https://magicui.design/docs/components/aurora-text
- https://magicui.design/docs/components/hyper-text

Don't use all of them—select contextually appropriate effects that enhance rather than overwhelm.

**See also:** `references/component-libraries.md` for detailed catalog with descriptions, use cases, aesthetic fit ratings, integration guidance, and performance considerations for all Aceternity UI and Magic UI components.

## React + TypeScript + Tailwind Specifics

**Tailwind v4 Patterns**
Use CSS variables for theme consistency:

```typescript
// Define in globals.css
:root {
  --color-bg-dark: #131313;
  --color-bg-light: #faf9f5;
  --color-accent: #d97757;
  --spacing-section: 6rem;  /* 96px */
}

// Use in Tailwind classes
<div className="bg-[var(--color-bg-dark)] py-[var(--spacing-section)]">
```

Prefer Tailwind's built-in spacing scale (multiples of 4px) but override with CSS variables when you need specific brand values.

**Component Composition**
Follow container/presenter pattern:
- Container components handle state and data
- Presenter components handle UI and styling
- Keep presenters pure and composable

Use composition over configuration. Small, focused components that combine are more flexible than large components with many props.

**Motion Integration**
Integrate Framer Motion at component level:

```typescript
import { motion } from "framer-motion";

const Card = ({ children }: { children: React.ReactNode }) => (
  <motion.div
    whileHover={{ scale: 1.02 }}
    transition={{ type: "spring", stiffness: 300, damping: 25 }}
    className="p-6 rounded-lg bg-[var(--color-bg-light)]"
  >
    {children}
  </motion.div>
);
```

**TypeScript Rigor**
Prefer explicit types over `any`. Use discriminated unions for component variants. Define strict prop interfaces with JSDoc comments for developer experience.

## Context & Appropriateness: When to Be Expressive

**Not all projects deserve maximum expressiveness.** Context determines intensity.

**Go Full Expressive:**
- Creative portfolios and personal sites
- Design tools and creative software
- Developer tools and technical documentation
- AI/LLM interfaces and chat applications
- Marketing sites for design/creative services
- Conference and event sites

These contexts allow flourish—users expect personality and distinctive voice. Faux-ASCII treatments, bold motion, dramatic scale all work here.

**Apply Restraint:**
- Banking and financial interfaces
- Healthcare and medical applications
- Enterprise dashboards (unless specifically creative)
- E-commerce checkout flows
- Government and civic services

These contexts need calm, clear, functional design. Use subtle versions of the aesthetic: warm color palette without extreme contrasts, gentle spring motion instead of bounce, generous spacing without dramatic scale jumps.

**The Dial System:**
Think of expressiveness as a dial from 1-10, not a binary switch:
- **1-3 (Restrained)**: Warm colors, subtle spacing, minimal motion, clean type
- **4-7 (Balanced)**: One or two expressive elements (color OR motion OR type treatment), not all three
- **8-10 (Full)**: Faux-ASCII type, expressive springs, bold color punctuation, dramatic scale

Match the dial to user needs and project goals. Respect established UI patterns. Never sacrifice core functionality for visual appeal—expressive design enhances usability, doesn't replace it.

## The Anti-Vibes: What to Avoid and Alternatives

**Generic AI-Generated Aesthetics → Context-Specific Character**

Avoid overused font families that signal default thinking. **Instead of** Inter, Roboto, Arial, Space Grotesk, or system fonts, **choose** fonts with interesting personality matched to the project context. Display type should be expressive; body type should be refined.

Avoid cliched color schemes, particularly purple gradients on white backgrounds. **Instead,** commit to a cohesive position: bold and saturated, moody and restrained, or high-contrast and minimal. Use the 90/10 rule—one vibrant accent does more work than rainbow palettes.

Avoid predictable layouts and cookie-cutter component patterns. **Instead,** use asymmetry, unexpected scale jumps, bento grids with varied proportions, and full-bleed moments that create rhythm.

**Decoration Without Purpose → Intentional Details**

Avoid shapes that exist only to fill space or scattered visual elements with no function. **Instead,** every decorative element should serve the aesthetic direction: faux-ASCII patterns reference technical history, scanlines create retrofuture tension, dot matrices add warmth through constraint.

Avoid pure minimalism where empty isn't interesting. **Instead,** use intentional emptiness—generous negative space that creates breathing room and guides attention, not just absence of content.

**Over-Animation → High-Impact Moments**

Avoid parallax everything, scroll-jacking, and things constantly flying in from all directions. **Instead,** one well-orchestrated page load with staggered spring animations creates more delight than scattered micro-interactions.

Avoid traditional easing curves and fixed durations when spring physics would feel more alive. **Instead,** use Framer Motion springs with appropriate damping—expressive bounce for hero moments, standard springs for functional UI.

**Maximalist Chaos → Controlled Density**

Avoid "more is more" without consideration. **Instead,** match implementation complexity to aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist designs need restraint, elegance, and precision in spacing and typography.

**Default Backgrounds → Atmospheric Depth**

Avoid pure solid colors (especially #ffffff white or #000000 black). **Instead,** use textured backgrounds that match the overall aesthetic: warm blacks (#131313) with subtle olive tones, cream whites (#faf9f5), noise overlays, gradient meshes, or geometric patterns.

**Pure Black and White → Warm Tones**

Avoid pure black (#000000) and pure white (#ffffff). **Instead,** prefer warm blacks with olive/brown undertones (#131313-#1a1a1a) and cream/parchment whites (#faf9f5, #f5f4ed). The subtle warmth creates cohesion and prevents clinical feeling.

**AI-Generated Imagery → Deliberate Visual Choices**

Avoid AI-generated imagery unless used as deliberate aesthetic choice (glitchy, weird, intentionally artificial). **Instead,** use technical romance illustrations (line art, isometric views, pixel compositions), real product screenshots, or no imagery at all—let typography and color do the work.

## References & Resources

**Motion & Animation:**
- Framer Motion: https://www.framer.com/motion
- Material Design Expressive Motion: https://m3.material.io/blog/m3-expressive-motion-theming
- Google Expressive Design Research: https://design.google/library/expressive-material-design-google-research

**ASCII Art & Display Type:**
- Figlet (ASCII text): https://www.npmjs.com/package/figlet
- PixiJS (2D WebGL): https://pixijs.com
- @pixi/react: https://react.pixijs.io

**Component Libraries:**
- Aceternity UI: https://ui.aceternity.com
- Magic UI: https://magicui.design

**Color Reference:**
- Anthropic's terracotta family: #d97757 and warm earth tones
- Warm blacks: #131313 to #1a1a1a with olive/brown undertones
- Warm whites: #faf9f5, #f5f4ed, #faf8f6

Remember: Claude is capable of extraordinary, award-worthy creative work. Commit relentlessly to a distinctive and unforgettable vision. The constraint (faux-ASCII, warm palette, spring physics) becomes the signature style.

---

## Working Examples

Complete, production-ready React + TypeScript examples demonstrating the aesthetic in practice:

**Hero Sections:**
- `examples/hero-section.tsx` - Complete hero with figlet ASCII art, spring animations, warm palette, technical grid background, and scroll indicators

**Layout Patterns:**
- `examples/bento-grid-layout.tsx` - Asymmetric grid with varied card sizes, spring animations on hover, glassmorphism effects, and warm accents

**Typography Components:**
- `examples/ascii-text-effect.tsx` - Reusable ASCII text components with multiple fonts, typewriter effects, glitch animations, and scanline overlays

Each example includes:
- Full TypeScript types and interfaces
- Framer Motion spring configurations
- Warm color palette implementation (#131313, #d97757, #faf9f5)
- Responsive design patterns
- Accessibility considerations

Copy and adapt these examples as starting points for implementing the aesthetic in your projects.
