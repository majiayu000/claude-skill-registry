---
name: frontend-design
description: "Builds distinctive, production-grade UIs that avoid generic AI aesthetics. Use whenever the user wants to build, restyle, or give visual direction to any interface — pages, dashboards, landing pages, components, onboarding flows, mobile screens, or design systems — even without an explicit 'design' request. Also triggers for: picking an aesthetic direction, improving the look of a dull/generic existing page, adding visual personality, or choosing colors/typography. Includes a bundled design intelligence database for concrete guidance across web (React, Next.js, Vue, Tailwind) and mobile (React Native, Flutter, SwiftUI)."
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

Use the bundled design search tooling when you need concrete guidance that should shape implementation rather than generic inspiration.

Reach for `.claude/skills/frontend-design/scripts/search.py` when you need any of the following:
- a style direction that fits a product category or audience
- a color system, typography pairing, or chart recommendation
- UX or accessibility guidance for a specific interface problem
- stack-specific frontend advice for React, Next.js, Vue, Tailwind, and other supported stacks
- a full design-system recommendation grounded in the bundled dataset

Skip the search when the user already gave a precise visual direction and the implementation path is obvious.

### Search Workflow

1. Start with the smallest query that captures the product or interface type.
2. Use auto-detection first; add `--domain` only when you know what kind of answer you need.
3. Add `--stack` when framework-specific implementation details matter.
4. Synthesize the retrieved guidance into one cohesive direction instead of pasting disconnected search results into the final answer.

### Quick Start

```bash
# Auto-detect the best domain from a concise query
python3 .claude/skills/frontend-design/scripts/search.py "glassmorphism dark mode"

# Ask for a specific kind of guidance
python3 .claude/skills/frontend-design/scripts/search.py "healthcare saas" --domain colors

# Add framework context when implementation details matter
python3 .claude/skills/frontend-design/scripts/search.py "responsive layout" --stack html-tailwind
```

### High-Value Defaults

Treat these as strong defaults, not blind rules:
- Prefer SVG icon systems over emoji so the UI feels product-grade and stylistically consistent.
- Keep clickable elements obviously interactive, including pointer cues where the platform expects them.
- Protect readability first; contrast and hierarchy matter more than visual gimmicks.
- In light mode, translucent surfaces need enough opacity to stay legible.
- Floating elements look more intentional when they breathe instead of touching viewport edges.
- Prefer hover treatments that preserve layout stability unless movement is a deliberate part of the concept.

### References

- `references/design-system-generation.md` — use when the user wants a full design-system or style-guide recommendation for a project type (e.g. "SaaS dashboard", "e-commerce luxury", "fintech app") assembled from multiple search domains
- `references/quality-checklist.md` — use as the final self-critique pass before delivering UI work

## Gotchas

- **Defaulting to safe choices**: Inter font + blue primary + white background is AI slop. Be distinctive.
- **Using search as decoration**: Retrieved guidance should change the design system or implementation decisions, not just add buzzwords.
- **Inconsistent design system**: Don't mix unrelated tokens or visual languages. Commit to one system throughout.
- **Ignoring contrast ratios**: WCAG AA minimum. Beautiful but unreadable is a failure.
- **Purple gradients**: The #1 AI cliché. Avoid unless specifically requested.
- **Interaction polish gaps**: Missing hover/focus states or weak affordances make even strong visuals feel unfinished.

## Data Source

Remote: [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/main/src/ui-ux-pro-max/data)

Available domains include styles, colors, typography, charts, products, landing, ux, icons, ui-reasoning, and web-interface. Supported stacks include html-tailwind, react, nextjs, astro, vue, nuxtjs, nuxt-ui, svelte, swiftui, react-native, flutter, shadcn, and jetpack-compose.

Search uses a cached BM25 ranking script over the remote dataset, so prefer concise, concrete queries over long prompt-like paragraphs.


Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.
