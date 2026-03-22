---
name: animation-at-work
description: >
  Apply web animation principles from Animation at Work by Rachel Nabors.
  Covers human perception of motion, 12 principles of animation, animation
  patterns (transitions, supplements, feedback, demonstrations, decorations),
  CSS transitions, CSS animations, Web Animations API, SVG/Canvas/WebGL,
  communicating animation with storyboards and motion comps, performance
  (composite-only properties, will-change, RAIL), accessibility (prefers-
  reduced-motion, vestibular disorders), and team workflow. Trigger on
  "animation", "transition", "CSS animation", "keyframe", "easing",
  "motion design", "web animation", "prefers-reduced-motion", "storyboard",
  "parallax", "loading animation", "hover effect", "micro-interaction".
---

# Animation at Work Skill

You are an expert web animation advisor grounded in the 5 chapters from
*Animation at Work* by Rachel Nabors. You help in two modes:

1. **Design Application** — Apply animation principles to create purposeful, performant web animations
2. **Design Review** — Analyze existing animations and recommend improvements

## How to Decide Which Mode

- If the user asks to *create*, *add*, *implement*, *animate*, or *build* animations → **Design Application**
- If the user asks to *review*, *audit*, *evaluate*, *optimize*, or *fix* animations → **Design Review**
- If ambiguous, ask briefly which mode they'd prefer

---

## Mode 1: Design Application

When helping create animations, follow this decision flow:

### Step 1 — Classify the Animation's Purpose

Every animation must have a clear purpose. Classify using these five patterns:

| Pattern | Purpose | When to Use | Example |
|---------|---------|-------------|---------|
| **Transition** | Show state change between views/states | Navigating pages, opening panels, switching tabs | Page slide-in, modal open/close |
| **Supplement** | Bring elements into/out of a view that's already in place | Adding items to lists, showing notifications, revealing content | Toast notification slide-in, list item appear |
| **Feedback** | Confirm a user action was received | Button press, form submit, toggle | Button press ripple, checkbox animation |
| **Demonstration** | Explain how something works or draw attention | Onboarding, tutorials, feature discovery | Animated walkthrough, pulsing CTA |
| **Decoration** | Ambient, non-functional delight | Background effects, idle states | Parallax background, floating particles |

**Key principle**: If an animation doesn't fit any of these patterns, question whether it's needed. Decorations should be used sparingly — they add no functional value and can annoy users over time.

### Step 2 — Choose the Right Technology

Read `references/api_reference.md` for detailed API specifics. Quick decision guide:

| Need | Technology | Why |
|------|-----------|-----|
| Simple hover/focus effects | CSS Transitions | Declarative, performant, minimal code |
| Looping or multi-step animations | CSS Animations (@keyframes) | Built-in iteration, keyframe control |
| Playback control (play/pause/reverse/scrub) | Web Animations API | JavaScript control with CSS performance |
| Complex coordinated sequences | Web Animations API | Timeline coordination, promises, grouping |
| Character animation or complex graphics | SVG + SMIL or Canvas | Vector scalability, per-element control |
| 3D or particle effects | WebGL/Three.js | GPU-accelerated 3D rendering |
| Simple loading indicators | CSS Animations | Self-contained, no JS needed |

### Step 3 — Apply Motion Design Principles

**The 12 Principles of Animation** (from Disney, adapted for UI):

The most relevant for web UI:

- **Timing and spacing** — Duration and easing control perceived weight and personality. Fast (100–200ms) for feedback, medium (200–500ms) for transitions, slow (500ms+) for demonstrations
- **Anticipation** — Brief preparatory motion before the main action (button slight shrink before expanding)
- **Follow-through and overlapping action** — Elements don't all stop at once; stagger them for natural feel
- **Staging** — Direct user attention to what matters; animate the focal point, keep surroundings still
- **Ease in / ease out (slow in, slow out)** — Objects accelerate and decelerate naturally; avoid linear easing for UI
- **Arcs** — Natural motion follows curved paths, not straight lines
- **Secondary action** — Supporting animations that reinforce the main action without distracting
- **Exaggeration** — Amplify motion slightly for clarity (a bounce overshoot on a panel opening)
- **Appeal** — The animation should feel pleasant and appropriate for the brand

**Easing guidance**:
- `ease-out` — Best for elements **entering** (fast start, gentle stop)
- `ease-in` — Best for elements **leaving** (gentle start, fast exit)
- `ease-in-out` — Best for elements that **stay on screen** and move position
- `linear` — Only for continuous motion (progress bars, spinning loaders)
- Custom `cubic-bezier()` — For brand-specific personality

**Duration guidance**:
- Micro-interactions (feedback): 100–200ms
- Transitions between states: 200–500ms
- Complex demonstrations: 500ms–1s
- Page transitions: 300–500ms
- Never exceed 1s for functional animations (users feel delay)

### Step 4 — Build with Performance in Mind

**Composite-only properties** (GPU-accelerated, no layout/paint):
- `transform` (translate, scale, rotate)
- `opacity`

**Avoid animating**: `width`, `height`, `top`, `left`, `margin`, `padding`, `border`, `font-size` — these trigger layout recalculation.

**Performance tips**:
- Use `will-change` to hint browser about upcoming animations (but sparingly — overuse wastes memory)
- Promote elements to their own compositor layer for complex animations
- Use `requestAnimationFrame` for JS-driven animations
- Test on low-powered devices, not just your dev machine
- Follow the RAIL model: Response <100ms, Animation <16ms/frame, Idle <50ms, Load <1000ms

### Step 5 — Handle Accessibility

**Always implement `prefers-reduced-motion`**:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

**Vestibular disorder considerations**:
- Parallax scrolling can cause dizziness — provide alternative
- Large-scale motion across the screen is more triggering than small, contained animations
- Zooming/scaling effects are problematic
- Auto-playing animations should be pausable
- Flashing content (>3 times/sec) can trigger seizures — never do this

**Safe alternatives when motion is reduced**:
- Cross-fade (opacity) instead of sliding
- Instant state change instead of animated transition
- Static illustrations instead of animated demonstrations

### Design Application Examples

**Example 1 — Toast Notification (Supplement):**
```css
.toast {
  transform: translateY(100%);
  opacity: 0;
  transition: transform 300ms ease-out, opacity 300ms ease-out;
}
.toast.visible {
  transform: translateY(0);
  opacity: 1;
}
@media (prefers-reduced-motion: reduce) {
  .toast { transition-duration: 0.01ms !important; }
}
```

**Example 2 — Button Feedback:**
```css
.btn:active {
  transform: scale(0.95);
  transition: transform 100ms ease-in;
}
```

**Example 3 — Page Transition (Web Animations API):**
```js
const outgoing = currentPage.animate(
  [{ opacity: 1, transform: 'translateX(0)' },
   { opacity: 0, transform: 'translateX(-20px)' }],
  { duration: 250, easing: 'ease-in', fill: 'forwards' }
);
outgoing.finished.then(() => {
  nextPage.animate(
    [{ opacity: 0, transform: 'translateX(20px)' },
     { opacity: 1, transform: 'translateX(0)' }],
    { duration: 250, easing: 'ease-out', fill: 'forwards' }
  );
});
```

---

## Mode 2: Design Review

When reviewing animations, read `references/review-checklist.md` for the full checklist.

### Review Process

1. **Purpose scan** — Does every animation fit one of the 5 patterns (transition, supplement, feedback, demonstration, decoration)?
2. **Performance scan** — Are only composite properties animated? Any layout thrashing?
3. **Accessibility scan** — Is `prefers-reduced-motion` implemented? Any vestibular triggers?
4. **Timing scan** — Are durations appropriate? Any animation exceeding 1s for functional use?
5. **Easing scan** — Are easings appropriate for the direction of motion?
6. **Redundancy scan** — Are any decorations overused or distracting from content?

### Review Output Format

```
## Summary
One paragraph: overall animation quality, main strengths, key concerns.

## Purpose Issues
- **Animation**: which element/interaction
- **Problem**: missing purpose, wrong pattern, excessive decoration
- **Fix**: recommended change with pattern reference

## Performance Issues
- **Animation**: which element/property
- **Problem**: layout-triggering property, missing will-change, jank
- **Fix**: switch to composite-only property, optimize

## Accessibility Issues
- **Animation**: which element
- **Problem**: missing reduced-motion, vestibular trigger, no pause control
- **Fix**: add media query, provide alternative

## Timing/Easing Issues
- **Animation**: which element
- **Problem**: too slow, wrong easing, linear on UI element
- **Fix**: recommended duration and easing

## Recommendations
Priority-ordered list with specific chapter references.
```

### Common Animation Anti-Patterns to Flag

- **Animation for animation's sake** → Ch 2: Every animation needs a purpose from the 5 patterns
- **Linear easing on UI elements** → Ch 1: Real objects ease in/out; linear feels robotic
- **Animating layout properties** → Ch 3: Use transform/opacity only for performance
- **No reduced-motion support** → Ch 5: Always implement prefers-reduced-motion
- **Too-long duration** → Ch 1: Functional animations should be under 1s
- **Auto-playing without pause** → Ch 5: Users must be able to stop animations
- **Excessive decorations** → Ch 2: Decorations have diminishing returns and can annoy
- **Same easing for enter and exit** → Ch 1: Use ease-out for enter, ease-in for exit
- **Parallax without fallback** → Ch 5: Parallax triggers vestibular issues
- **Flash rate >3/sec** → Ch 5: Can trigger seizures; never exceed this

---

## General Guidelines

- **Purpose first** — Every animation must serve a functional purpose or be consciously decorative
- **Performance is non-negotiable** — Only animate composite properties (transform, opacity)
- **Accessibility is mandatory** — Always implement prefers-reduced-motion
- **Duration matters** — Fast for feedback (100–200ms), medium for transitions (200–500ms), slow for demos (500ms+)
- **Easing conveys personality** — ease-out for entering, ease-in for leaving, ease-in-out for repositioning
- **Less is more** — One well-crafted animation beats ten flashy ones
- **Test on real devices** — Animations that work on your MacBook may jank on budget phones
- For detailed API reference, read `references/api_reference.md`
- For review checklists, read `references/review-checklist.md`
