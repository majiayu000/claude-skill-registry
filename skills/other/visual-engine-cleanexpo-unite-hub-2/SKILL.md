---
name: visual-engine-skill
description: Extend and apply the Visual Experience Engine across landing pages, inspiration galleries, and demos using safe, persona-aware animations and layouts. Use when adding or modifying visual experiences.
allowed-tools: Read, Write, Search
---

# Visual Engine Skill

## Purpose
Own the Visual Experience Engine for Synthex.social, including:
- Animation presets and registries
- Inspiration gallery (/inspiration)
- Demos page (/demos)
- Visual Experience Engine page (/visual-experience-engine)

## Scope
- `src/lib/visual/animations/*`
- `src/lib/visual/animationOrchestrator.ts`
- `src/lib/visual/animationStyles.ts`
- `src/data/videoDemos.json`
- `src/app/visual-experience-engine/page.tsx`
- `src/app/demos/page.tsx`
- `src/app/wizard/animation-style/page.tsx`
- `src/components/visual/*`
- `src/components/visual/three/*`

## Responsibilities
1. Add new animation styles and presets with human-friendly names.
2. Ensure accessibility and respects `prefers-reduced-motion`.
3. Wire animations into hero sections, cards, sections, and demos.
4. Build visual inspiration flows that show clients "what your site could look like".
5. Manage 3D visual components (Three.js).

## Animation Categories
- **Beam Effects**: Light sweeps, auroras, glows
- **Clip Animations**: Iris reveals, mask transitions
- **Card Effects**: Morphs, hovers, flips
- **Flashlight**: Cursor spotlight effects
- **Transitions**: Page and section transitions
- **Background FX**: Particles, starfields, gradients

## Constraints
- No rapid flashing (epilepsy safety)
- No disorienting zoom/rotation
- All durations > 0.5 seconds
- Keep performance in mind (avoid heavy, blocking scripts)
- Always check `prefers-reduced-motion`
