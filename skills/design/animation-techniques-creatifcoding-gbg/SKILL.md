# Animation Techniques

> Decision-tree routing for animation pattern selection

---

## Invocation Triggers

Invoke this skill when:

- User mentions "animation", "transition", "morph", "effect"
- Implementing UI state changes with visual feedback
- Choosing between animation libraries (motion.dev vs anime.js vs CSS)
- Designing multi-phase or orchestrated animations
- Text-based animations or character effects

---

## Questionnaire: Animation Type Selection

```
Q1: What is being animated?
├─[A] Text/Characters → Q2
├─[B] Layout/Position → Q4
├─[C] Color/Opacity → Q5
├─[D] Shape/SVG → Q6
└─[E] Complex orchestration → Q7

Q2: Text animation type?
├─[A] Entrance/Exit → Use motion.dev AnimatePresence
├─[B] Character-by-character → Q3
├─[C] Typewriter effect → Use anime.js irregular playback
└─[D] Content change (A→B) → TEXT MORPH TECHNIQUE
    └─► Ref: techniques/text-morph-animation.md

Q3: Character animation complexity?
├─[A] Simple stagger (fade in/out) → motion.dev + staggerChildren
├─[B] Position scramble → anime.js splitText + stagger
├─[C] Multi-phase morph → TEXT MORPH TECHNIQUE
└─[D] Continuous loop → anime.js timeline + loop:true

Q4: Layout animation type?
├─[A] Enter/Exit presence → motion.dev AnimatePresence
├─[B] Shared element → motion.dev layoutId
├─[C] Reorder list → motion.dev Reorder
├─[D] Staggered grid → anime.js stagger({ grid: [x,y] })
└─[E] Physics-based → motion.dev spring transition

Q5: Color/Opacity animation?
├─[A] Simple fade → CSS transition (prefer)
├─[B] Color interpolation → motion.dev (handles color spaces)
├─[C] Gradient animation → anime.js (better gradient support)
└─[D] Filter effects → motion.dev filter prop

Q6: Shape/SVG animation?
├─[A] Path morphing → anime.js SVG module
├─[B] Draw/stroke → anime.js strokeDashoffset
├─[C] Simple transform → motion.dev
└─[D] Complex path → Consider GSAP or anime.js

Q7: Complex orchestration?
├─[A] Sequential phases → anime.js createTimeline
├─[B] Parallel + stagger → anime.js timeline.add(..., offset)
├─[C] React-coordinated → motion.dev variants + staggerChildren
└─[D] Imperative control → anime.js (better control API)
```

---

## Decision Tree: Library Selection

```
                    ┌─────────────────────────────────┐
                    │    ANIMATION REQUIREMENT        │
                    └───────────────┬─────────────────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            │                       │                       │
            ▼                       ▼                       ▼
    ┌───────────────┐      ┌───────────────┐      ┌───────────────┐
    │ React State   │      │ DOM Direct    │      │ Complex       │
    │ Driven        │      │ Manipulation  │      │ Orchestration │
    └───────┬───────┘      └───────┬───────┘      └───────┬───────┘
            │                       │                       │
            ▼                       ▼                       ▼
    ┌───────────────┐      ┌───────────────┐      ┌───────────────┐
    │ motion.dev    │      │ anime.js v4   │      │ anime.js v4   │
    │ (motion/react)│      │ or CSS        │      │ timeline      │
    └───────────────┘      └───────────────┘      └───────────────┘
            │                       │                       │
            ▼                       ▼                       ▼
    ┌───────────────────────────────────────────────────────────┐
    │                      COMPLEXITY CHECK                      │
    └───────────────────────────────────────────────────────────┘
            │                       │                       │
    ┌───────┴───────┐       ┌───────┴───────┐       ┌───────┴───────┐
    │ Simple        │       │ Medium        │       │ High          │
    │ (1-2 props)   │       │ (3-5 props)   │       │ (6+ props or  │
    │               │       │               │       │ multi-phase)  │
    └───────┬───────┘       └───────┬───────┘       └───────┬───────┘
            │                       │                       │
            ▼                       ▼                       ▼
    ┌───────────────┐      ┌───────────────┐      ┌───────────────┐
    │ CSS transition│      │ motion.dev    │      │ anime.js      │
    │ (if possible) │      │ (default)     │      │ createTimeline│
    └───────────────┘      └───────────────┘      └───────────────┘
```

---

## Decision Tree: Text Animation

```
                    ┌─────────────────────────────────┐
                    │      TEXT ANIMATION NEED        │
                    └───────────────┬─────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
            ┌───────────┐   ┌───────────┐   ┌───────────┐
            │ Entrance/ │   │ Content   │   │ Continuous│
            │ Exit      │   │ Change    │   │ Effect    │
            └─────┬─────┘   └─────┬─────┘   └─────┬─────┘
                  │               │               │
          ┌───────┴───────┐       │       ┌───────┴───────┐
          │               │       │       │               │
          ▼               ▼       │       ▼               ▼
    ┌───────────┐   ┌───────────┐ │ ┌───────────┐   ┌───────────┐
    │ Whole     │   │ Per-char  │ │ │ Typewriter│   │ Scramble/ │
    │ element   │   │ stagger   │ │ │ reveal    │   │ glitch    │
    └─────┬─────┘   └─────┬─────┘ │ └─────┬─────┘   └─────┬─────┘
          │               │       │       │               │
          ▼               ▼       │       ▼               ▼
    ┌───────────┐   ┌───────────┐ │ ┌───────────┐   ┌───────────┐
    │motion.dev │   │ anime.js  │ │ │ anime.js  │   │ anime.js  │
    │Animate    │   │ splitText │ │ │ irregular │   │ timeline  │
    │Presence   │   │ + stagger │ │ │ playback  │   │ + random  │
    └───────────┘   └───────────┘ │ └───────────┘   └───────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────────┐
                    │     SAME LENGTH OR DIFFERENT?   │
                    └───────────────┬─────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
            ┌───────────┐   ┌───────────┐   ┌───────────┐
            │ Same      │   │ Growing   │   │ Shrinking │
            │ length    │   │ (+chars)  │   │ (-chars)  │
            └─────┬─────┘   └─────┬─────┘   └─────┬─────┘
                  │               │               │
                  └───────────────┼───────────────┘
                                  │
                                  ▼
                    ┌─────────────────────────────────┐
                    │       TEXT MORPH TECHNIQUE      │
                    │                                 │
                    │  Phase 1: Fade out unmapped     │
                    │  Phase 2: Compress remaining    │
                    │  Phase 3: Scramble to target    │
                    │  Phase 4: Fade in new chars     │
                    │                                 │
                    │  ► techniques/text-morph-       │
                    │    animation.md                 │
                    └─────────────────────────────────┘
```

---

## Quick Reference: Library Capabilities

| Capability | motion.dev | anime.js v4 | CSS |
|------------|------------|-------------|-----|
| React integration | Native | Manual | Native |
| AnimatePresence | ✓ | - | - |
| Layout animations | ✓ | - | - |
| Shared elements | ✓ | - | - |
| Text splitting | - | ✓ splitText | - |
| Timeline | - | ✓ createTimeline | - |
| Grid stagger | - | ✓ stagger({grid}) | - |
| SVG morphing | - | ✓ | - |
| Spring physics | ✓ | ✓ | - |
| Reduced motion | ✓ useReducedMotion | Manual | ✓ prefers-reduced-motion |

---

## Technique Index

| Technique | When to Use | Reference |
|-----------|-------------|-----------|
| Text Morph | Transitioning between different text content | `techniques/text-morph-animation.md` |
| Stagger Grid | Animating grid items with wave effect | anime.js docs |
| Layout Shared | Elements moving between containers | motion.dev layoutId |
| Presence | Elements entering/exiting DOM | motion.dev AnimatePresence |

**Full catalog**: See `techniques/INDEX.md` for all documented techniques.

---

## Integration Checklist

When implementing animations:

- [ ] Check `prefers-reduced-motion` - skip or simplify
- [ ] Consider mobile performance - reduce particle counts
- [ ] Use hardware acceleration - `transform` over `top/left`
- [ ] Clean up on unmount - cancel pending animations
- [ ] Test with DevTools → Performance → 6x slowdown

---

## Related

- **Navigation:** `AGENTS.md` (agent instructions for this skill)
- **Techniques:** `techniques/INDEX.md` (full technique catalog)
- **Beads:** tmnl-ypwpb (Text Morph feature)
- **Skills:** `/effect-atom-integration` (for animation state)
- **Submodules:** `../../submodules/anime/` (anime.js v4 source)
