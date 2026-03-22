---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
---

# Frontend Design Skill

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

## Anti-Patterns to Avoid

NEVER use generic AI-generated aesthetics like:

- Overused font families (Inter, Roboto, Arial, system fonts)
- Cliched color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

## Implementation Principles

**IMPORTANT**: Match implementation complexity to the aesthetic vision:

- **Maximalist designs** need elaborate code with extensive animations and effects
- **Minimalist or refined designs** need restraint, precision, and careful attention to spacing, typography, and subtle details

Elegance comes from executing the vision well.

## ACR Automotive Context

**IMPORTANT**: When working on this project, you MUST follow the established UX patterns documented in the pattern guides. This ensures consistency across the entire application.

### Required Reading

Before designing ANY new features or pages for ACR Automotive, read BOTH pattern documents (located in this skill directory):

**1. `ACR_UX_PATTERNS.md` (Desktop Patterns)**

- **Established Design Language**: Professional, Coca-Cola inspired, red-as-accent
- **Color System**: Exact hex codes and usage rules for ACR brand colors
- **Typography Patterns**: Font choices, size scales, and utility classes
- **Layout Standards**: Page structure, container widths, responsive grids
- **Component Patterns**: Cards, buttons, search, forms, navigation (with code examples)
- **Loading States**: Preloader, skeletons, animations, and timing system
- **Animation System**: Entrance animations, stagger delays, hover effects
- **Error States**: When to use CardError vs InlineError vs PageError
- **Accessibility Standards**: Keyboard navigation, focus states, ARIA patterns

**2. `ACR_MOBILE_UX_PATTERNS.md` (Mobile/Tablet Patterns)**

- **Touch-First Design**: 44px minimum touch targets, active states, press feedback
- **Progressive Disclosure**: Combined vs separate components, stacked layouts
- **Mobile-Specific Components**: Admin card view, dashboard combined card, search tabs
- **Spacing & Density**: Tighter spacing on mobile (p-3 vs lg:p-4), responsive gaps
- **Typography Adaptations**: Smaller headings, truncation patterns, responsive labels
- **Layout Transformations**: Stack on mobile → horizontal on desktop patterns
- **Mobile Performance**: Touch feedback timing, lazy loading, optimization strategies
- **Touch Accessibility**: Keyboard support on tablets, screen reader patterns

### Key Constraints

- **Never invent new patterns**: Use existing ACR components and utilities
- **Red sparingly**: ACR red (#ED1C24) for CTAs and highlights only, not overwhelming
- **Professional aesthetic**: Business tool first, visual flair second
- **Performance critical**: Fast animations (300-450ms), responsive interactions
- **Consistency over creativity**: Match existing pages rather than innovating

### Common Mistakes to Avoid

- Creating custom loading spinners (use Preloader or skeleton states)
- Inventing new button styles (use AcrButton variants)
- Inconsistent card styling (use AcrCard with standard variants)
- Wrong animation timing (start at 0.7s, use stagger classes for grids)
- Overusing red (white cards with gray borders, red only for actions)
- Ignoring mobile patterns (always check responsive behavior)

### Design System Integration

- **Component Library**: `src/components/acr/` - Use existing ACR components
- **Design Tokens**: `src/app/globals.css` - Color palette, animation classes
- **Skeleton States**: `src/components/ui/skeleton.tsx` - Loading patterns
- **Error States**: `src/components/ui/error-states.tsx` - Error handling
- **Documentation**: `src/components/acr/README.md` - Architecture philosophy

## Quality Checklist

Before completing any frontend work:

- [ ] Clear aesthetic direction chosen and executed
- [ ] Typography is distinctive and appropriate
- [ ] Color palette is cohesive with sharp accents
- [ ] Motion/animations enhance (not distract from) UX
- [ ] Responsive across mobile, tablet, and desktop
- [ ] Accessible (keyboard nav, screen reader friendly)
- [ ] Production-ready code quality

---

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.
