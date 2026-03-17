---
name: bold-frontend-design
description: Creates visually striking, production-grade frontend interfaces that reject generic "AI slop" aesthetics through intentional design thinking. Implements bold typography, distinctive color palettes, high-impact animations (React Three Fiber, Framer Motion), and unexpected spatial compositions. Use PROACTIVELY when building landing pages, hero sections, 3D visualizations, or any interface requiring memorable visual impact. MUST BE USED when user requests "creative", "bold", "unique", "striking", "3D", "animated", or "next-level" design.
allowed-tools: ["Bash", "Read", "Write", "Edit", "Grep", "Glob"]
model: claude-sonnet-4-5-20250929
---

# Bold Frontend Design Skill

## Overview

**Philosophy**: Reject AI convergence. Claude naturally samples from high-probability design patterns (Inter fonts, purple gradients, centered layouts). This creates generic "AI slop" - safe, predictable, and forgettable designs.

**Core Principle**: "Make unexpected choices that feel genuinely designed for the context."

**Key Insight**: Steerability as a feature - Claude responds dramatically to specific guidance pushing away from convention. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Bold maximalism and refined minimalism both work - **the key is intentionality, not intensity**.

---

## Prerequisites

**Project Type**: Next.js or React application

**Dependencies** (installed as needed):
```bash
npm install @react-three/fiber @react-three/drei @react-three/postprocessing framer-motion three
```

**Verification**: `scripts/dependency_check.sh`

---

## Anti-Convergence Protocol

### NEVER Use (Explicit Rejection List)

| Category | Rejected Patterns |
|----------|-------------------|
| **Fonts** | Inter, Roboto, Arial, Helvetica, system-ui |
| **Colors** | Purple gradients (#6366f1, #8b5cf6, #a78bfa on light backgrounds) |
| **Layouts** | Centered hero with symmetric two-column grid |
| **Animations** | Simple fade-ins without choreography |

### ALWAYS Verify (4 Questions)

Before implementing ANY design element:

1. **Have I seen this pattern in 100 other websites?** → If yes, choose differently
2. **Is this choice safe or bold?** → If safe, push further
3. **Does this reflect the specific context, or is it generic?** → Must be context-specific
4. **Am I converging on a local maximum of safety?** → Continuous pushback required

**If answers are Yes/Safe/Generic/Converging → STOP and choose differently**

**Full anti-pattern checklist**: [reference/anti-patterns.md](reference/anti-patterns.md)

---

## Workflow Phases

### Phase 1: Design Thinking (10-15 min) - PRE-CODE

**Objective**: Establish intentional creative direction before writing code.

1. **Define Purpose and Audience**
   - What problem does this interface solve?
   - Who is the target user?
   - What emotion/action should it inspire?

2. **Select Extreme Aesthetic Tone** (choose ONE, commit fully):
   - **Brutalist**: Raw, unstyled, stark contrasts, bold typography
   - **Maximalist**: Layered complexity, rich textures, abundant visuals
   - **Retro-Futuristic**: 80s neon, synthwave, chrome, grid perspectives
   - **Organic**: Flowing curves, natural movements, soft gradients
   - **Luxury**: Elegant restraint, premium materials (gold, marble)
   - **Playful**: Vibrant colors, unexpected interactions, whimsical
   - **Editorial**: Magazine-inspired, bold typography hierarchy

3. **Identify One Memorable Differentiator**
   - Interactive 3D visualization with bloom effects
   - Diagonal scroll-triggered reveals
   - Variable font weight animation on scroll
   - Asymmetric overlapping sections with parallax

4. **Document Constraints** (framework, performance, accessibility)

**Full guide**: [reference/design-philosophy.md](reference/design-philosophy.md)

---

### Phase 2: Rejection of Generic Patterns (5-10 min)

1. **Choose Distinctive Typography**
   - Display: Space Grotesk, Clash Display, Cabinet Grotesk, Syne
   - Body: Instrument Sans, Manrope, DM Sans, Outfit

2. **Define Dominant Color Palette** (60-30-10 Rule)
   - 60% Dominant: Deep background (e.g., #0a0e27)
   - 30% Secondary: Gradients (e.g., #06b6d4 → #3b82f6)
   - 10% Accent: Sharp highlights (#ffffff, #ef4444)

3. **Plan Unexpected Spatial Composition**
   - Asymmetry: 60/40 split instead of 50/50
   - Overlap: Sections bleed into each other
   - Diagonal: Elements on rotated grids (-3deg, 5deg)
   - Viewport Units: Full-height sections with scroll-snap

**Full checklist**: [reference/anti-patterns.md](reference/anti-patterns.md)

---

### Phase 3: Implementation (30-60 min)

1. **Install dependencies**
2. **Set up typography system** (next/font/google or @font-face)
3. **Build color system** (Tailwind config or CSS variables)
4. **Create spatial composition** (asymmetric grids, overlapping sections)
5. **Implement high-impact animations** (orchestrated entrance, scroll parallax, 3D elements)

**Full animation patterns**: [reference/animation-techniques.md](reference/animation-techniques.md)

---

### Phase 4: Refinement (15-20 min)

1. **Run Design Validation**
   ```bash
   python .claude/skills/bold-frontend-design/scripts/validate_design.py frontend/
   ```

2. **Check Performance**: 60fps in Chrome DevTools

3. **Verify Accessibility**: WCAG AA color contrast, keyboard navigation, `prefers-reduced-motion`

4. **USER CONFIRMATION - CRITICAL**
   ```
   Can you confirm you see the design at http://localhost:3000?
   Does this feel bold and distinctive (not generic)?
   ```
   **NEVER claim success without explicit user verification**

---

## Tool Selection Guide

### When to Use React Three Fiber

- 3D objects (spheres, molecules, abstract shapes)
- Glass/metallic materials (MeshTransmissionMaterial)
- Bloom post-processing effects
- Floating/rotating 3D elements

**Example**: Hero section with molecular visualization

### When to Use Framer Motion

- Orchestrated page entrance animations
- Scroll-triggered effects (useScroll, useTransform)
- Parallax compositions
- Gesture interactions (hover, tap, drag)

**Example**: Staggered text reveals on load

### Decision Tree

```
Is the element 3D?
├─ Yes → React Three Fiber
│   └─ Need glow/glass? → MeshTransmissionMaterial + Bloom
│
└─ No → Framer Motion
    └─ Triggered by scroll?
        ├─ Yes → useScroll + useTransform
        └─ No → animate prop
```

### Combining Both

```tsx
<section className="relative">
  {/* 3D Background */}
  <div className="absolute inset-0 z-0">
    <Canvas><Molecule /><Bloom /></Canvas>
  </div>

  {/* 2D Content Overlay */}
  <motion.div className="relative z-10" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
    <h1>Overlaid Content</h1>
  </motion.div>
</section>
```

**Full patterns**: [reference/animation-techniques.md](reference/animation-techniques.md)

---

## Success Criteria

### Functional Requirements
- [ ] Design philosophy documented (purpose, aesthetic, differentiator)
- [ ] Typography system implemented (distinctive fonts)
- [ ] Color palette defined (dominant hues, 60-30-10)
- [ ] Spatial composition intentional (not default grid)
- [ ] High-impact animations implemented

### Quality Requirements
- [ ] `validate_design.py` passes with **zero warnings**
- [ ] No generic fonts (Inter, Roboto, Arial)
- [ ] No generic colors (purple gradients)
- [ ] **60fps** animation performance
- [ ] WCAG AA accessibility

### MANDATORY
- [ ] **USER CONFIRMATION RECEIVED** - User has seen design and confirmed visual impact

---

## Troubleshooting

### Design Feels Generic

1. Run `validate_design.py` to detect convergent patterns
2. Check typography: `grep -r "font-family.*Inter" frontend/`
3. Check colors: `grep -r "#6366f1" frontend/`
4. Verify dominant color has 60%+ visual weight
5. Add spatial break (asymmetry, overlap, rotation)

### Animations Feel Scattered

- **Consolidate to high-impact moments** (not scattered micro-interactions)
- Page load: One orchestrated entrance sequence
- Scroll: One parallax effect with depth layers
- Hover: Dramatic state changes on key CTAs only

**Full troubleshooting**: [reference/design-philosophy.md](reference/design-philosophy.md)

---

## Resources

### Reference Materials
- [reference/design-philosophy.md](reference/design-philosophy.md) - Anti-convergence principles, aesthetic tones, case studies
- [reference/animation-techniques.md](reference/animation-techniques.md) - R3F + Framer Motion patterns (11 patterns)
- [reference/anti-patterns.md](reference/anti-patterns.md) - Explicit rejection checklist, detection scripts

### Validation Scripts
- `scripts/validate_design.py` - Detect generic fonts, colors, patterns
- `scripts/dependency_check.sh` - Verify R3F, Framer Motion installed

### Template
- [templates/hero-3d-parallax.tsx](templates/hero-3d-parallax.tsx) - Molecule hero section example

### External
- React Three Fiber: https://docs.pmnd.rs/react-three-fiber
- Drei Components: https://github.com/pmndrs/drei
- Framer Motion: https://www.framer.com/motion/

---

## Final Checklist

Before completing this skill invocation:

1. [ ] Design philosophy documented
2. [ ] Anti-pattern checklist complete
3. [ ] Typography distinctive (NO Inter/Roboto)
4. [ ] Color palette dominant (NO purple gradients)
5. [ ] Spatial composition intentional
6. [ ] Animations high-impact (orchestrated)
7. [ ] `validate_design.py` passes
8. [ ] Performance: 60fps verified
9. [ ] Accessibility: WCAG AA checked
10. [ ] **USER CONFIRMATION RECEIVED**

---

**The Ultimate Test**: If shown without branding, would 100 people remember this or think it's generic?

**Remember**: Bold design requires continuous resistance against ANY convergence toward safety. **Think outside the box** at every decision point.
