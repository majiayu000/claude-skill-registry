---
name: motion-and-storytelling
description: Disney's 12 animation principles, cinematic storytelling techniques, and comic book conventions apply to web UI — used subtly, they make interfaces feel alive, intentional, and emotionally resonant. Use when designing transitions, micro-interactions, onboarding flows, scroll animations, or any motion in the UI.
metadata:
  priority: 6
  pathPatterns:
    - "**/*.css"
    - "**/*.scss"
    - "**/*.tsx"
    - "**/*.jsx"
    - "design-system/**"
    - "components/**"
  promptSignals:
    phrases:
      - "animation"
      - "transition"
      - "motion"
      - "micro-interaction"
      - "scroll animation"
      - "easing"
      - "storytelling"
      - "entrance"
      - "exit"
retrieval:
  aliases:
    - animation principles
    - disney principles
    - motion design
    - micro-interactions
    - transitions
    - cinematic ui
    - storytelling ui
  intents:
    - animate this component
    - design a transition
    - make the ui feel alive
    - add scroll animations
    - design micro-interactions
  examples:
    - animate this modal entrance
    - make this button feel more satisfying to click
    - add scroll-driven animations to this landing page
    - design the transition between these two states
---

# Motion and Storytelling in UI

Animation and motion are not decoration — they are communication. When applied with the same discipline as typography or colour, they tell the user what is happening, where to look, and what the product feels like to use. The source material — Disney's 12 principles, cinematic language, comic book conventions — is centuries of accumulated knowledge about how to communicate through movement and sequence.

The key word is **subtlety**. In UI, motion should be felt, not watched.

---

## Disney's 12 Principles Applied to UI

### 1. Squash and Stretch
Objects compress on impact and extend on acceleration. In UI: a button that scales down slightly on press and springs back communicates physicality and responsiveness.

```css
button:active { transform: scale(0.96); }
button { transition: transform 80ms ease-out; }
```

Use sparingly — reserved for primary CTAs and satisfying confirmations.

### 2. Anticipation
A small preparatory movement before the main action. In UI: a menu item shifting slightly before opening, or a loading indicator appearing before a transition begins, prepares the user for what is coming.

### 3. Staging
Present one idea clearly at a time. In UI: entrance animations should direct attention to the new content, not compete with existing content. When a modal opens, the rest of the page dims — that is staging.

### 4. Straight Ahead vs Pose to Pose
**Pose to pose** — defining start and end states and letting the system interpolate — is the CSS/JS approach. Define clear initial and final states; let `transition` or a spring physics library handle the in-between.

### 5. Follow-Through and Overlapping Action
Elements don't all stop at the same time. In UI: staggered list item entrances (each item enters 40–60ms after the previous) feel more natural than all items appearing simultaneously.

```css
.item:nth-child(1) { animation-delay: 0ms; }
.item:nth-child(2) { animation-delay: 50ms; }
.item:nth-child(3) { animation-delay: 100ms; }
```

### 6. Ease In and Ease Out
Nothing in nature starts or stops instantly. Use easing curves, not linear transitions.

| Easing | Use for |
|---|---|
| `ease-out` (fast start, slow end) | Elements entering the screen — feels natural arrival |
| `ease-in` (slow start, fast end) | Elements leaving the screen — feels intentional exit |
| `ease-in-out` | Elements moving between positions on screen |
| Spring physics | Interactive elements that respond to touch/drag |

Never use `linear` for UI motion — it reads as mechanical and unfinished.

### 7. Arcs
Natural movement follows arcs, not straight lines. Tooltips and popovers that scale from their origin point (rather than fading uniformly) follow this principle. `transform-origin` matters.

### 8. Secondary Action
A supporting motion that reinforces the main action. In UI: an icon inside a button that shifts slightly when the button is pressed. A checkmark that draws itself after a form submission. These details reward attention without demanding it.

### 9. Timing
Duration is meaning. Fast = responsive, energetic. Slow = weighty, important.

| Duration | Use for |
|---|---|
| 80–120ms | Micro-interactions (button press, hover) |
| 150–250ms | Component transitions (dropdown open, tooltip) |
| 250–400ms | Page-level transitions, modal entrance |
| 400–600ms | Hero animations, onboarding sequences |
| > 600ms | Almost always too long — the user is waiting |

### 10. Exaggeration
A small, deliberate overstatement makes an action feel satisfying. In UI: a success checkmark that overshoots slightly before settling, or a notification badge that pops just slightly larger than its final size. The exaggeration is 10–15%, not theatrical.

### 11. Solid Drawing (Solid Design)
Respect the 3D space of the interface. Elements should move in ways consistent with their perceived layer — a bottom sheet slides up from below because it lives below the content, not from the side. A tooltip appears near its trigger, not across the screen.

### 12. Appeal
The overall motion should feel right for the brand. A playful consumer app can use bouncier, springier motion. A financial tool uses precise, controlled transitions. Appeal is not decoration — it is brand personality expressed through time.

---

## Cinematic Techniques

### Reveal and Entrance
Content that enters the viewport has more impact when it arrives, rather than simply existing. Scroll-triggered entrance animations — a section fading up as the user scrolls into it — borrow from cinematic reveals. The key: **the content drives in from a meaningful direction** (below, because that's where the user is scrolling from).

```css
@keyframes fade-up {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

### Parallax
Background elements moving slower than foreground elements creates depth. In web: a hero background image moving at 50% scroll speed while content moves at 100% creates a sense of layers. Use subtly — aggressive parallax causes motion sickness.

### Cut vs Dissolve
- **Hard cut** (instant state change): fast, decisive, efficient. Use for navigation between pages, closing modals.
- **Dissolve / crossfade**: gradual, considered, connected. Use when two states are related — a tab switching, an image gallery transitioning.

### Scene Setting
The first frame of a section sets the scene before detail appears. A hero with a strong image and large type, followed by supporting details appearing after a brief delay, is a cinematic opening. The user's eye is directed to the subject before reading begins.

---

## Comic Book Conventions

### Panel Sequence
Comics tell stories through a sequence of static frames that imply motion between them. In UI: step indicators, onboarding carousels, and progress flows use the same logic — each "panel" is a moment in a sequence, and the user's eye moves between them.

### Speed Lines and Energy
Emphasis lines, radial gradients, and directional blur suggest motion and energy without actual animation. A button with a subtle directional gradient implies it is pointing somewhere. A loading indicator with trailing opacity implies direction.

### Typography as Tone
In comics, the size, weight, and style of lettering communicates emotion — a shout is set in large bold caps, a whisper in thin small italics. In UI: oversized display type for a hero carries energy; small muted caption text recedes. This is micro-typography as emotional register, not just hierarchy.

### The Gutter
In comics, the reader's imagination fills the space between panels. In UI, transitions are the gutter — what happens between states. A smooth transition lets the user's brain construct a coherent mental model. A jarring jump forces them to re-orient.

---

## Practical Rules

1. **Respect `prefers-reduced-motion`** — always. Users with vestibular disorders or motion sensitivity must be able to use the product without animation.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

2. **Motion should serve the user, not entertain them.** Every animation should answer: does this help the user understand what happened, where something came from, or where to look next?

3. **Duration under 400ms for almost everything.** If an animation takes longer, it is slowing the user down.

4. **Never animate layout properties** (`width`, `height`, `padding`, `top`, `left`) — they cause reflow. Animate `transform` and `opacity` only — they run on the GPU.

5. **One motion at a time per region.** Simultaneous competing animations create visual noise. Stage them.

## Review Checklist

- [ ] Does `prefers-reduced-motion` disable or reduce all animations?
- [ ] Are all transitions using `ease-out` (enter), `ease-in` (exit), or `ease-in-out` (reposition)?
- [ ] Is linear easing avoided?
- [ ] Are durations under 400ms for component-level transitions?
- [ ] Are only `transform` and `opacity` animated (not layout properties)?
- [ ] Do entrance animations move from a meaningful direction (bottom for scroll-reveal, origin for scale)?
- [ ] Does motion match brand tone (bouncy for playful, precise for enterprise)?
- [ ] Are staggered entrances used for list items rather than simultaneous appearance?
