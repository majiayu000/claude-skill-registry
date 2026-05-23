---
name: nextjs-frontend-design
description: |
  This skill should be used when the user asks to 'build a Next.js app', 'create a dashboard',
  'design a landing page', 'build a SaaS frontend', 'create React components', 'style my app',
  'design system', 'UI components', or needs distinctive frontend design. Covers App Router,
  React Server Components, type-safe APIs, Server Actions, and modern styling. Avoids generic
  'AI slop' aesthetics (Inter fonts, purple gradients, predictable layouts) - creates memorable,
  intentional interfaces instead. Triggers on: Next.js projects, e-commerce sites, admin panels,
  marketing pages, or any frontend needing both architectural excellence and visual distinction.
---

# Next.js Frontend Design Skill

Create distinctive, production-grade Next.js applications combining expert TypeScript architecture with exceptional visual design.

<frontend_aesthetics>
You tend to converge toward generic, "on distribution" outputs. In frontend design, this creates what users call the "AI slop" aesthetic. Avoid this: make creative, distinctive frontends that surprise and delight.

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Draw from IDE themes and cultural aesthetics for inspiration.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density—not the safe middle ground.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Layer CSS gradients, use geometric patterns, noise textures, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

Avoid generic AI-generated aesthetics:
- Overused font families (Inter, Roboto, Arial, system fonts)
- Clichéd color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Perfectly centered everything with equal padding
- Cookie-cutter design that lacks context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed for the context. Vary between light and dark themes, different fonts, different aesthetics. You still tend to converge on common choices (Space Grotesk, for example) across generations. Avoid this: it is critical that you think outside the box!
</frontend_aesthetics>

---

## Design Philosophy

Before writing ANY code, commit to a **BOLD aesthetic direction**:

1. **Purpose**: What problem does this interface solve? Who uses it?
2. **Tone**: Pick an extreme and commit fully:
   - Brutally minimal, maximalist chaos, retro-futuristic, organic/natural
   - Luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw
   - Art deco/geometric, soft/pastel, industrial/utilitarian, terminal/code
   - Japanese minimalism, cyberpunk neon, Miami Vice pastels
3. **Differentiation**: What's the ONE thing someone will remember?

**CRITICAL**: Bold maximalism and refined minimalism both work—the key is intentionality, not intensity. Half-measures produce mediocrity.

**For comprehensive design guidance, see:** `references/design-philosophy.md`

---

## Typography Quick Reference

**NEVER use**: Inter, Roboto, Open Sans, Lato, Arial, system fonts

**DO use**:
- Code aesthetic: JetBrains Mono, Fira Code, IBM Plex Mono
- Editorial: Playfair Display, Crimson Pro, Newsreader, Fraunces
- Technical: IBM Plex Sans, Source Sans 3, Source Serif 4
- Distinctive: Bricolage Grotesque, Syne, Outfit, DM Serif Display

**Pairing principle**: High contrast = interesting. Display + monospace, serif + geometric sans.

**Use extremes**: Weight 100/200 vs 800/900 (not 400 vs 600). Size jumps of 3x+ (not 1.5x).

```tsx
// app/layout.tsx - Font setup
import { Bricolage_Grotesque, JetBrains_Mono } from 'next/font/google';

const fontDisplay = Bricolage_Grotesque({
  subsets: ['latin'],
  variable: '--font-display',
  weight: ['200', '400', '800'],
});

const fontMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-mono',
});
```

---

## Styling Quick Reference

### CSS Variables Setup

```css
/* globals.css */
:root {
  /* Typography */
  --font-display: 'Bricolage Grotesque', sans-serif;
  --font-body: 'Source Sans 3', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* Colors - Commit to an aesthetic */
  --color-bg: #0a0a0a;
  --color-surface: #141414;
  --color-text: #e8e8e8;
  --color-muted: #6b6b6b;
  --color-accent: #ff3e00;
  --color-border: #2a2a2a;

  /* Animation easings - NEVER use default ease */
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-out-back: cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

### Page Load Animation

```css
/* Staggered reveal - high impact */
.animate-stagger > * {
  opacity: 0;
  transform: translateY(20px);
  animation: fadeUp 0.6s var(--ease-out-expo) forwards;
}

.animate-stagger > *:nth-child(1) { animation-delay: 0ms; }
.animate-stagger > *:nth-child(2) { animation-delay: 100ms; }
.animate-stagger > *:nth-child(3) { animation-delay: 200ms; }
.animate-stagger > *:nth-child(4) { animation-delay: 300ms; }

@keyframes fadeUp {
  to { opacity: 1; transform: translateY(0); }
}
```

### Background Atmosphere

```css
/* Gradient mesh - creates depth */
.hero-bg {
  background:
    radial-gradient(ellipse at 20% 50%, rgba(120, 119, 198, 0.3), transparent 50%),
    radial-gradient(ellipse at 80% 50%, rgba(255, 62, 0, 0.2), transparent 50%),
    linear-gradient(180deg, var(--color-bg) 0%, var(--color-surface) 100%);
}

/* Noise texture overlay */
.textured::after {
  content: '';
  position: absolute;
  inset: 0;
  background: url('/noise.svg');
  opacity: 0.03;
  pointer-events: none;
}
```

---

## Anti-Patterns Checklist

Before shipping, verify you have NOT:

**Typography:**
- [ ] Used Inter, Roboto, Arial, or system fonts
- [ ] Font weights only differ by 200 (e.g., 400 vs 600)
- [ ] Size hierarchy less than 2x between levels

**Color:**
- [ ] Purple gradient on white background
- [ ] Blue-purple-pink gradient (the AI classic)
- [ ] Evenly distributed pastel palette

**Layout:**
- [ ] Perfectly centered everything
- [ ] Equal padding everywhere
- [ ] Standard Bootstrap-like grid with no variation
- [ ] Cards in a perfect 3-column grid

**Animation:**
- [ ] Default `ease` timing function
- [ ] No page load orchestration
- [ ] Hover effects that just change color

**Backgrounds:**
- [ ] Solid white or #f5f5f5
- [ ] No texture, depth, or atmosphere

---

## Reference Files

**Design & Aesthetics:**
- `references/design-philosophy.md` — Complete aesthetics guide, theme recipes, spatial composition, anti-patterns

**Technical Patterns:**
- `references/nextjs-patterns.md` — App Router, Server Components, Server Actions, Caching, Streaming, Accessibility
- `references/typescript-patterns.md` — Advanced TypeScript patterns, API types, hooks
- `references/component-library.md` — Production component implementations
- `references/animation-recipes.md` — Motion design patterns, scroll effects, Framer Motion

---

## Final Reminder

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

**Remember**: Claude is capable of extraordinary creative work. Don't hold back—show what can truly be created when thinking outside the box and committing fully to a distinctive vision.
