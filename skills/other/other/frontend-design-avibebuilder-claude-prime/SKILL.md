---
name: frontend-design
description: "Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when making design decisions, building web components, choosing color palettes, selecting typography, designing charts, or researching visual patterns. Queries design database for inspiration."
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

## Design Intelligence

Query a remote design knowledge base for styles, colors, typography, charts, and framework guidelines.

### Quick Start

```bash
# Search any domain (auto-detected)
python3 scripts/search.py "glassmorphism dark mode"

# Search specific domain
python3 scripts/search.py "healthcare saas" --domain colors

# Framework-specific guidelines
python3 scripts/search.py "responsive layout" --stack html-tailwind
```

### Search Domains

| Domain | Query Examples |
|--------|----------------|
| styles | "glassmorphism", "brutalism", "bento grids" |
| colors | "healthcare", "fintech", "e-commerce" |
| typography | "modern tech", "elegant serif", "playful" |
| charts | "time series", "comparison", "distribution" |
| products | "saas dashboard", "landing page" |
| landing | "hero + features", "pricing", "funnel" |
| ux | "navigation", "forms", "accessibility" |
| icons | "navigation", "action", "status" |
| react-performance | "memo", "suspense", "waterfall" |
| ui-reasoning | "SaaS", "e-commerce", "fintech" |
| web-interface | "aria", "form control", "semantic" |

### Stacks

`--stack` options: `html-tailwind`, `react`, `nextjs`, `astro`, `vue`, `nuxtjs`, `nuxt-ui`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`

### Design System Generation

For comprehensive design system recommendations, follow the multi-domain search orchestration workflow.

> See [references/design-system-generation.md](./references/design-system-generation.md)

### Critical Rules

1. **No Emoji Icons** - Use SVG icons (Heroicons, Lucide, Simple Icons)
2. **Cursor Pointer** - All clickable elements must have `cursor-pointer`
3. **4.5:1 Contrast** - WCAG minimum for text readability
4. **Glass Cards** - Use `bg-white/80` or higher opacity in light mode
5. **Floating Navbar** - Add spacing (`top-4 left-4 right-4`), not edge-to-edge
6. **Hover Stability** - Color/opacity transitions, not scale transforms

### Pre-Delivery Checklist

> See [references/quality-checklist.md](./references/quality-checklist.md)

## References

| Reference | Content |
|-----------|---------|
| [quality-checklist.md](./references/quality-checklist.md) | Visual, interaction, accessibility checks |
| [design-system-generation.md](./references/design-system-generation.md) | Multi-domain search orchestration for design system generation |

## Data Source

Remote: [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/main/src/ui-ux-pro-max/data)

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.
