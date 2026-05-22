---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Frontend Design Skill

Expert in creating distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics.

## When to Use This Skill

Use this skill when:

- Building new web components, pages, or applications with a focus on unique design
- Creating landing pages or marketing pages that need to stand out
- Designing user interfaces that require bold aesthetic choices
- Avoiding generic, cookie-cutter designs

## Purpose

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. It implements real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build, potentially including context about purpose, audience, or technical constraints.

---

## Design Thinking

Before coding, understand the context and commit to a **BOLD aesthetic direction**:

- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme aesthetic direction:
  - Brutally minimal
  - Maximalist chaos
  - Retro-futuristic
  - Organic/natural
  - Luxury/refined
  - Playful/toy-like
  - Editorial/magazine
  - Brutalist/raw
  - Art deco/geometric
  - Soft/pastel
  - Industrial/utilitarian

  _Use these for inspiration but design one true to the aesthetic direction._

- **Constraints**: Technical requirements (framework, performance, accessibility)
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work—the key is **intentionality, not intensity**.

### Implementation Requirements

Code must be:

- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

---

## Frontend Aesthetics Guidelines

### Focus Areas

**Typography**

- Choose fonts that are beautiful, unique, and interesting
- Avoid generic fonts (Arial, Inter)
- Opt for distinctive, characterful choices that elevate aesthetics
- Pair distinctive display fonts with refined body fonts

**Color & Theme**

- Commit to a cohesive aesthetic
- Use CSS variables for consistency
- Dominant colors with sharp accents outperform timid, evenly-distributed palettes

**Motion**

- Use animations for effects and micro-interactions
- Prioritize CSS-only solutions for HTML
- Use Motion library for React when available
- Focus on high-impact moments: orchestrated page loads with staggered reveals (animation-delay)
- Use scroll-triggering and hover states that surprise

**Spatial Composition**

- Unexpected layouts
- Asymmetry and overlap
- Diagonal flow and grid-breaking elements
- Generous negative space OR controlled density

**Backgrounds & Visual Details**

- Create atmosphere and depth (avoid solid colors)
- Add contextual effects and textures matching the aesthetic
- Apply creative forms:
  - Gradient meshes
  - Noise textures
  - Geometric patterns
  - Layered transparencies
  - Dramatic shadows
  - Decorative borders
  - Custom cursors
  - Grain overlays

### Avoid

**NEVER use generic AI-generated aesthetics:**

- Overused font families (Inter, Roboto, Arial, system fonts)
- Clichéd color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design lacking context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed for context. No design should be the same. Vary between light/dark themes, different fonts, different aesthetics.

### Critical Implementation Note

**IMPORTANT**: Match implementation complexity to the aesthetic vision:

- Maximalist designs need elaborate code with extensive animations and effects
- Minimalist or refined designs need restraint, precision, careful spacing, typography, and subtle details
- Elegance comes from executing the vision well

---

## Integration with Project

When using this skill in the st44-home project:

1. **Follow Angular 21+ conventions** from the `frontend` skill
2. **Apply design principles** from this skill for aesthetics
3. **Maintain project standards**:
   - camelCase naming
   - Standalone components
   - Signals for state
   - OnPush change detection
4. **Test locally** before pushing (lint, format, tests, build)

---

## Philosophy

> Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

---

## Workflow

1. **Understand** the design context and user requirements
2. **Choose** a bold aesthetic direction
3. **Implement** with Angular 21+ patterns (from `frontend` skill)
4. **Apply** distinctive design choices (typography, color, motion, layout)
5. **Refine** every detail to match the aesthetic vision
6. **Test** locally with all checks
7. **Deliver** production-grade, memorable interface

## Success Criteria

Before marking work complete:

- [ ] Clear aesthetic direction chosen and executed
- [ ] Visually distinctive and memorable
- [ ] Production-grade code quality
- [ ] Follows Angular 21+ patterns
- [ ] All local checks pass (lint, format, tests, build)
- [ ] Accessibility maintained (WCAG AA)
