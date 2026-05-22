---
name: frontend-design-fix
description: Fix generic frontend designs by applying aesthetic upgrades across the 5 design dimensions
version: 2.0.0
architecture: modular-composable
tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Frontend Design Fix Skill

## Overview

This orchestrator skill diagnoses generic design patterns and applies targeted aesthetic upgrades across five design dimensions. Fixes are tech-agnostic (principles) but reference framework-specific implementation skills.

**The 5 Dimensions**:

1. **Typography** – Replace generic fonts, fix weight hierarchies, aggressive size jumps
2. **Color & Theme** – Remove predictable palettes, introduce CSS variables, add dominant + accent strategy
3. **Motion** – Add orchestrated page loads, staggered reveals, hover surprises
4. **Spatial Composition** – Break centered layouts, introduce asymmetry, adjust spacing strategy
5. **Backgrounds & Details** – Layer gradients, add geometric patterns, create atmospheric depth

---

## Quick Diagnosis

### "What's wrong with my design?"

**It looks like a template** → See `./sub-skills/audit.md`

**Font choices feel default** → See `./sub-skills/typography-fixes.md`

**Color palette is predictable** → See `./sub-skills/color-fixes.md`

**Everything's static and boring** → See `./sub-skills/motion-fixes.md`

**Layout is centered and uniform** → See `./sub-skills/spatial-fixes.md`

**Backgrounds are flat/plain** → See `./sub-skills/background-fixes.md`

---

## 5-Phase Fix Process

### Phase 1: Audit

Identify generic elements, score anti-patterns, assess brand context
→ See `./sub-skills/audit.md`

### Phase 2: Assess Brand & Context

Understand emotional intent, target audience, competitive differentiation

### Phase 3: Apply Dimension-Based Fixes

- Typography fixes (typeface, weights, size jumps)
- Color fixes (palette strategy, CSS variables, accents)
- Motion fixes (orchestration, scroll triggers, hover)
- Spatial fixes (asymmetry, overlap, diagonal flow)
- Background fixes (gradients, patterns, depth)

→ See specific sub-skills below

### Phase 4: Validate Improvements

- Visual hierarchy strengthened?
- Brand personality evident?
- Accessibility maintained (WCAG AA+)?
- Performance acceptable?

### Phase 5: Generate Before/After Report

Document improvements, measure impact, establish design guidelines

---

## Anti-Pattern Detection Checklist

**Typography**

- [ ] Using Inter, Roboto, Open Sans, Lato, or system fonts
- [ ] Font weights in safe middle range (400, 500, 600 only)
- [ ] Size progression is linear/minimal (1.25–1.5x scale)

**Color**

- [ ] Material Design trinity (Blue, Red, Green)
- [ ] Oversaturated neon accents
- [ ] No color strategy document or CSS variable structure

**Layout**

- [ ] Everything is centered (hero, cards, sections)
- [ ] Uniform padding/margins everywhere
- [ ] Symmetric, grid-based composition only

**Motion**

- [ ] No animations at all
- [ ] Linear timing on all transitions
- [ ] Slow, sluggish animations (2s+)

**Background**

- [ ] Flat solid colors throughout
- [ ] No visual depth or layering
- [ ] No contextual details or micro-patterns

---

## Sub-Skills Reference

| Sub-Skill | Purpose | Lines |
|-----------|---------|-------|
| `audit.md` | Design audit checklist and scoring | ~100 |
| `typography-fixes.md` | Font replacement, weight hierarchy, size jumps | ~100 |
| `color-fixes.md` | Palette overhaul, CSS variables, accent strategy | ~100 |
| `motion-fixes.md` | Orchestrated animations, scroll triggers, hover | ~100 |
| `spatial-fixes.md` | Break centered layout, asymmetry, spacing | ~100 |
| `background-fixes.md` | Gradients, patterns, textures, depth | ~100 |

---

## When to Use This Skill

✅ Design audit reveals generic patterns or lack of differentiation
✅ Existing design feels "AI-generated" or template-like
✅ Need to upgrade without complete redesign
✅ Applying brand personality to standardized UI
✅ Want to improve motion, hierarchy, or visual depth
✅ Building stronger design system foundations

---

## Getting Started

1. **Run the audit** → `./sub-skills/audit.md`
2. **Identify weakest dimensions** → Anti-pattern checklist above
3. **Apply targeted fixes** → Follow relevant sub-skill(s)
4. **Validate improvements** → Phase 4 checklist
5. **Document changes** → Generate before/after report

---

## Related Skills

- **frontend-design** – Create new designs (principles-first approach)
- **frontend-design-react** – React + Vite implementation
- **frontend-design-vue** – Vue 3 implementation
- **frontend-design-svelte** – Svelte implementation
- **frontend-design-html** – Static HTML/CSS implementation
