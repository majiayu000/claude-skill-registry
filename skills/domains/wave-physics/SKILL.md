---
name: wave-physics
description: Apply wave physics principles when working on simulation code. Use this skill when editing files in src/waves/, src/simulation/, or when the user mentions wave behavior, shoaling, breaking, or foam physics.
---

# Wave Physics Validation

When working on wave simulation or physics code, validate against these foundational principles.

## Core Principles (from plans/00-principles.md)

1. **Waves are energy, not water movement** - Water particles move in orbital paths, not with the wave
2. **Deep water**: Circular orbital motion, unaffected by seafloor
3. **Shallow water**: Elliptical orbits compressed by seafloor friction
4. **Shoaling**: Waves slow down, compress, and increase in height as depth decreases
5. **Breaking criteria**: Wave breaks when height > 0.78 × water depth

## Validation Checklist

When reviewing or writing physics code:
- [ ] Does the implementation treat waves as energy propagation?
- [ ] Is orbital motion correctly circular (deep) vs elliptical (shallow)?
- [ ] Does shoaling increase wave height as depth decreases?
- [ ] Is the 0.78 breaking ratio respected?
- [ ] Are foam effects tied to energy dissipation at breaking?

## Reference Files

- `plans/00-principles.md` - Foundational physics concepts
- `plans/reference/reference-wave-physics.md` - Detailed physics reference
- `plans/model/` - Implementation plans for physics systems

## When to Apply

Automatically apply this skill when:
- Editing files matching `src/**/wave*.js` or `src/**/simulation*.js`
- User mentions: shoaling, wave breaking, orbital motion, foam physics
- Creating or editing plans in `plans/model/`
