---
name: svelte-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Specialized in Svelte/SvelteKit applications with full-stack capabilities. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

This skill guides creation of distinctive, production-grade Svelte/SvelteKit interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices, leveraging Svelte's reactivity and SvelteKit's full-stack capabilities.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working Svelte/SvelteKit code that is:
- Production-grade and functional with progressive enhancement
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail
- Leverages Svelte's reactivity and SvelteKit's full-stack features

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize Svelte's built-in transitions and actions. Focus on high-impact moments: one well-orchestrated page load with staggered reveals creates more delight than scattered micro-interactions. Use scroll-triggering with Svelte actions and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

## Integration with Svelte Component Libraries

### Primary Focus: Svelte/SvelteKit Ecosystem

When working on Svelte projects, leverage these component libraries:

**Invoke `shadcn-svelte-management` skill when:**
- Need to discover available Svelte components
- Building features requiring multiple components (forms, dialogs, data tables)
- Need component installation commands
- Want component examples and implementation patterns
- Deciding between shadcn-svelte, Skeleton UI, or Melt UI

### Svelte Component Library Options

**1. shadcn-svelte**
- Svelte adaptation of shadcn/ui
- Components in `src/lib/components/ui/`
- Theme customization via `src/app.css`

**2. Skeleton UI**
- Modern, accessible Svelte components
- Built-in theming system
- Excellent for dashboards and forms

**3. Melt UI**
- Headless components for full customization
- Built with accessibility in mind
- Perfect for unique design systems

**4. Custom Components**
- Built from scratch with Tailwind CSS
- Full control over design and functionality
- Leverage Svelte's reactivity

### Svelte-Specific Design Workflow

1. **Choose component library** based on project needs
2. **Apply `frontend-design` principles** for Svelte:
   - Override theme in `src/app.css` with CSS variables
   - Extend `tailwind.config.js` with custom colors, fonts, animations
   - Add distinctive typography (replace default fonts)
   - Enhance with Svelte transitions (`fade`, `fly`, `slide`, `scale`)
   - Apply creative backgrounds, textures, spatial composition
   - Use Svelte actions for scroll-triggered animations
   - Leverage SvelteKit's progressive enhancement

3. **Leverage Svelte features:**
   - Reactive statements (`$:`) for dynamic styling
   - Component composition with `<slot>`
   - Event handling with `on:event`
   - Stores for state management
   - Actions for DOM interactions

**Key customization files:**
```
src/app.css              → CSS variables, theme imports, custom fonts
tailwind.config.js         → theme.extend: colors, fontFamily, animation, keyframes
src/lib/components/ui/*   → Component overrides and custom components
src/routes/+layout.svelte  → Global layout and theme provider
```

**Svelte Design Patterns:**
- Use `class:` directives for conditional styling
- Leverage `transition:` directives for animations
- Implement custom actions for complex interactions
- Use stores for global state management
- Build progressive enhancement with form actions

**Remember:** Svelte component libraries provide solid structure; your job is to create visually distinctive and memorable interfaces through creative theming and Svelte's unique capabilities.
