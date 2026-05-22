---
name: aesthetic
description: "Visual design intelligence and UI aesthetics. Integrates: chrome-devtools, ai-multimodal, media-processing. Capabilities: design analysis, visual hierarchy, color theory, typography, micro-interactions, animation, design systems, accessibility. Actions: analyze, design, create, capture, evaluate, implement UI aesthetics. Keywords: Dribbble, Behance, Mobbin, design inspiration, visual hierarchy, color palette, typography, spacing, animation, micro-interaction, design system, style guide, accessibility, WCAG, contrast ratio, golden ratio, whitespace, visual rhythm. Use when: building beautiful UIs, analyzing design inspiration, implementing visual hierarchy, adding animations/micro-interactions, creating design systems, evaluating aesthetic quality, capturing design screenshots."
license: Complete terms in LICENSE.txt
---

# Aesthetic

Create aesthetically beautiful interfaces by following proven design principles and systematic workflows. This skill combines design thinking, frontend implementation patterns, and comprehensive analysis techniques.

## When to Use This Skill

Use when:
- Building or designing user interfaces
- Analyzing designs from inspiration websites (Dribbble, Mobbin, Behance)
- Generating design images and evaluating aesthetic quality
- Implementing visual hierarchy, typography, color theory
- Adding micro-interactions and animations
- Creating design documentation and style guides
- Need guidance on accessibility and design systems
- Building production-grade frontend interfaces with distinctive aesthetics

## Core Philosophy

**Design Thinking First**: Before coding, understand context and commit to a BOLD aesthetic direction. Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

**Evidence-Based Aesthetics**: AI lacks aesthetic sense - standards must come from analyzing high-quality examples and aligning with market tastes. Study existing designs, identify patterns, extract principles.

**Progressive Excellence**: Start with BEAUTIFUL (aesthetics), ensure RIGHT (functionality/accessibility), add SATISFYING (micro-interactions), elevate with PEAK (storytelling).

## Quick Reference Framework

### 1. BEAUTIFUL: Understanding Aesthetics
Study existing designs, identify patterns, extract principles.

**Reference**: `references/design-principles.md` - Load for visual hierarchy, typography, color theory, white space principles.

### 2. RIGHT: Ensuring Functionality
Beautiful designs lacking usability are worthless. Study design systems, component architecture, accessibility requirements.

**Reference**: `references/design-principles.md` - Load for design systems, component libraries, WCAG accessibility standards.

### 3. SATISFYING: Micro-Interactions
Incorporate subtle animations with appropriate timing (150-300ms), easing curves (ease-out for entry, ease-in for exit), sequential delays.

**Reference**: `references/micro-interactions.md` - Load for duration guidelines, easing curves, performance optimization.

### 4. PEAK: Storytelling Through Design
Elevate with narrative elements - parallax effects, particle systems, thematic consistency. Use restraint: "too much of anything isn't good."

**Reference**: `references/storytelling-design.md` - Load for narrative elements, scroll-based storytelling, interactive techniques.

## Frontend Implementation Guidelines

### Typography
Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter. Pair a distinctive display font with a refined body font.

### Color & Theme
Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.

### Motion & Animation
Use animations for effects and micro-interactions. Prioritize CSS-only solutions. Use anime.js for complex animations.

**Reference**: `references/animejs.md` - Load when implementing anime.js v4 animations.

### Spatial Composition
Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.

### Backgrounds & Visual Details
Create atmosphere and depth. Add contextual effects and textures: gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, grain overlays.

**Reference**: `references/implementation-guide.md` - Load for detailed frontend design execution patterns.

## Workflows

### Workflow 1: Capture & Analyze Inspiration

Extract design guidelines from inspiration websites:
1. Browse inspiration sites (Dribbble, Mobbin, Behance, Awwwards)
2. Use **chrome-devtools** skill to capture full-screen screenshots
3. Use **ai-multimodal** skill to analyze and extract design patterns
4. Document findings in project design guidelines

**Reference**: `references/workflows.md` - Load for complete workflow steps and analysis checklist.

### Workflow 2: Generate & Iterate Design Images

Create aesthetically pleasing designs through iteration:
1. Define design prompt with style, colors, typography, audience
2. Use **ai-multimodal** skill to generate design images
3. Evaluate aesthetic quality (must score >= 7/10)
4. Iterate until professional standards met
5. Document final design decisions

**Reference**: `references/workflows.md` - Load for complete iteration process and quality standards.

## Design Documentation

### Create Design Guidelines
Use `assets/design-guideline-template.md` to document:
- Color patterns & psychology
- Typography system & hierarchy
- Layout principles & spacing
- Component styling standards
- Accessibility considerations
- Design highlights & rationale

Save in project `./docs/design-guideline.md`.

### Create Design Story
Use `assets/design-story-template.md` to document:
- Narrative elements & themes
- Emotional journey
- User journey & peak moments
- Design decision rationale

Save in project `./docs/design-story.md`.

## Anti-Patterns: Avoid Generic AI Aesthetics

NEVER use:
- Overused font families (Inter, Roboto, Arial, system fonts)
- Cliched color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

**Variation Principle**: No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

## Implementation Complexity Matching

Match implementation complexity to the aesthetic vision:
- **Maximalist designs**: Need elaborate code with extensive animations and effects
- **Minimalist/refined designs**: Need restraint, precision, careful attention to spacing, typography, and subtle details
- **Elegance**: Comes from executing the vision well

## Related Skills Integration

- **ai-multimodal**: Analyze documents, screenshots & videos, generate design images, evaluate aesthetic quality using Gemini API
- **chrome-devtools**: Capture screenshots from inspiration websites, navigate pages, interact with elements
- **media-processing**: Refine generated images (FFmpeg for video, ImageMagick for images)
- **ui-styling**: Implement designs with shadcn/ui components + Tailwind CSS
- **web-frameworks**: Build with Next.js, React, Vue

**Reference**: `references/design-resources.md` - Load for inspiration platforms, design systems, AI tools, MCP integrations.

## Key Principles

1. Aesthetic standards come from humans, not AI - study quality examples
2. Choose a BOLD aesthetic direction and execute with precision
3. Iterate based on analysis - never settle for first output (minimum 7/10 quality)
4. Balance beauty with functionality and accessibility
5. Document decisions for consistency across development
6. Use progressive disclosure in design - reveal complexity gradually
7. Match implementation complexity to aesthetic vision
8. Avoid generic AI aesthetics - create context-specific character

## Code Quality Standards

Implement working code that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

**Remember**: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.
