---
name: aesthetic-system
description: |
  Actionable design system complementing official frontend-design plugin.
  The plugin provides philosophy; this skill provides executable patterns.

  Invoke when:
  - Building web components, pages, or applications
  - Designing UI that needs to stand out (not generic)
  - Implementing visual polish and micro-interactions
  - Choosing typography, color palettes, or spatial layouts

  CRITICAL: Avoid "AI slop" aesthetics. Make creative, unexpected choices.
  MANDATORY: Consult Gemini before any frontend work.

  See also: references/dna-codes.md, references/banned-patterns.md
---

# Aesthetic System

## Phase 0: Gemini Research (MANDATORY)

Before ANY frontend work, get design direction from Gemini:

```bash
gemini -p "I'm building [describe component/page]. Research:
1. Distinctive design approaches (avoid AI-slop aesthetics)
2. Real-world examples of excellent [component type]
3. Current typography/color/layout trends for this context
4. Unexpected alternatives to obvious solutions"
```

**Why mandatory:** Web grounding surfaces current trends, prevents convergence.

## Design Thinking

Before coding, commit to a BOLD aesthetic direction:

1. **Purpose**: What problem? Who uses it?
2. **Tone**: Pick extreme (brutalist, luxury, playful, editorial, organic...)
3. **Differentiation**: What's the ONE thing someone will remember?

**CRITICAL**: Bold maximalism and refined minimalism both work—the key is intentionality.

## Core Principles

- **Typography**: Distinctive fonts, not Inter/Roboto/Space Grotesk
- **Color**: Dominant + accent, brand-tinted neutrals, no pure grays
- **Motion**: One orchestrated moment > scattered micro-interactions
- **Layout**: Asymmetry, overlap, diagonal flow, grid-breaking
- **Backgrounds**: Gradients, noise, patterns—not solid colors

See: `references/aesthetics-guidelines.md`

## Quality Bar: Stripe-Level Excellence

Reference these as quality exemplars:
- **Stripe**: Obsessive typography, micro-interactions, developer delight
- **Linear**: Keyboard-first, performance as design, smooth motion
- **Vercel**: Minimalist clarity, dramatic contrast, confident hierarchy

**The Gasp Test**: Would users gasp at how stunning this is? If no, keep iterating.

**Quality Checkpoints:**
- [ ] Typography that makes people stop and notice
- [ ] Layout that surprises with intentionality
- [ ] Motion that feels physically satisfying
- [ ] Details that show obsessive care
- [ ] Mobile experience that doesn't "suck"

## Mobile Excellence (Separate Optimization)

Mobile is NOT just responsive—it requires separate design thinking.

### Touch Libraries to Consider
- **@use-gesture/react**: Touch, mouse, drag, pinch gestures unified
- **react-spring**: Gesture-aware animations with physical springs
- **swiper**: Touch slider with native feel
- **framer-motion**: Gesture recognition + animation
- **@capacitor/haptics**: Haptics for Capacitor/mobile apps

### Mobile-Specific Quality Checks
- Touch targets: 44x44px minimum (Apple HIG)
- Swipe gestures: Natural, discoverable, satisfying
- Haptic feedback: Confirm actions with tactile response
- Pull-to-refresh: Physical bounce, not instant
- Bottom navigation: Thumb-reachable actions
- Momentum scrolling: Physics-based scroll

See: `references/mobile-excellence.md`

## Anti-Convergence

**YOU TEND TOWARD GENERIC OUTPUTS.** Before implementing, ask:
- "Have I used this font/color/layout recently?"
- "What's a distinctive alternative?"
- "Does this feel unique to THIS project?"

**Vary every project:** light/dark, font pairings, aesthetics, color approach.

See: `references/anti-patterns.md`

## Advanced Techniques

When basic CSS isn't enough:
- **WebGL/Three.js**: Living backgrounds, gradient meshes
- **GSAP/Framer Motion**: Complex animation sequences
- **CSS Art**: Pure CSS illustrations, clip-path magic
- **ASCII**: Terminal/brutalist aesthetics
- **Iconify**: 200k+ icons when Lucide isn't enough

See: `references/advanced-techniques.md`

## Iterative Polish Pattern

For incremental refinement after initial build:

**Quick passes** (run `/polish pass` repeatedly):
- Each pass makes ONE high-impact change
- Compound improvements over 10+ passes
- Separate desktop/mobile analysis each time
- Stream Deck / macro friendly

**Full polish** (run `/polish`):
- Multi-agent Design Council critique
- 5 automated iterations with quality threshold
- Use for foundation establishment or comprehensive audit

**Overhaul mode** (say "it sucks" or "overhaul"):
- Aggressive transformation, no preservation instinct
- Forces greenfield treatment regardless of maturity
- 8 iterations max, dramatic improvements

## References

- `references/implementation-constraints.md` - **MUST/NEVER rules for implementation** (stack, components, animation, performance)
- `references/aesthetics-guidelines.md` - Typography, color, motion, spatial composition
- `references/advanced-techniques.md` - WebGL, animations, CSS art, icons, asset generation
- `references/anti-patterns.md` - AI slop to avoid, convergence traps, variation mandate
- `references/dna-codes.md` - DNA variation system for structural variety
- `references/banned-patterns.md` - Explicit banned elements (hero badges, generic fonts, etc.)
- `references/browser-helpers.md` - Browser automation for Coolors, Google Fonts, inspiration
