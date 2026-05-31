---
name: loading-states-and-perceived-performance
description: Manage user expectations during wait times with appropriate loading states — from simple spinners to complex skeleton screens and staggered animations. Perceived performance is often more important than actual load time. Use when designing data-heavy components, handling API calls, building hero sections, or improving the feel of a slow interface.
metadata:
  priority: 7
  pathPatterns:
    - "components/**"
    - "src/components/**"
    - "**/*.tsx"
    - "**/*.jsx"
    - "**/*.css"
    - "**/*.scss"
    - "design-system/**"
  promptSignals:
    phrases:
      - "loading state"
      - "spinner"
      - "skeleton screen"
      - "skeleton loader"
      - "perceived performance"
      - "loading animation"
      - "shimmer effect"
      - "staggered loading"
retrieval:
  aliases:
    - loading states
    - skeleton loaders
    - spinners
    - perceived performance
    - shimmy
    - glimmer
  intents:
    - design a loading state
    - add a skeleton screen
    - improve perceived performance
    - choose between spinner and skeleton
    - handle slow data loading
    - adding delight to the wait
  examples:
    - what loading state should this card use
    - add a skeleton loader for this list
    - make the page feel faster while loading
    - design a spinner for this button
---

# Loading States and Perceived Performance

Users don't mind waiting as much if they understand *what* they are waiting for and *how much* progress is being made. Perceived performance is the design work of making a system feel faster than it actually is.

---

## Choosing the Right Loading State

| Wait Duration | Best Pattern | Use for |
|---|---|---|
| **Short (< 1s)** | **Inline Spinner / Loader** | Button actions, small updates, quick data fetches |
| **Medium (1s – 3s)** | **Skeleton Screen** | Cards, lists, dashboards, profile pages |
| **Long (> 3s)** | **Determinate Progress Bar** | File uploads, complex exports, heavy processing |
| **Full Page** | **Staggered Entry / Animated Sections** | Initial app load, hero sections, immersive transitions |

---

## Simple Cases: Spinners and Loaders

Use spinners for small, contained actions where the layout doesn't change significantly.

- **Button Spinners:** Replace button text or sit alongside it. The button should enter a `disabled` state to prevent double-submissions.
- **Micro-Loaders:** A small 16–24px circle for inline updates (e.g., saving a single field).
- **Animation Tip:** A "spring-loaded" rotation (easing in and out) feels more premium than a constant linear rotation.

```css
@keyframes spin {
  0%   { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.spinner {
  animation: spin 800ms cubic-bezier(0.4, 0, 0.2, 1) infinite;
}
```

---

## Skeleton Screens (Glimmer/Shimmer)

Skeleton screens provide a visual placeholder that mimics the layout of the final content. This reduces "layout shift" (CLS) and signals to the user exactly where the content will appear.

### The Shimmer Effect
A subtle, moving gradient that travels across the skeleton elements.

```css
.skeleton {
  background: var(--color-grey-100);
  background-image: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.5) 50%,
    rgba(255, 255, 255, 0) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0%   { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
```

### Rules for Skeletons
- **Match the shape:** If the final content is a round avatar, use a round skeleton. If it's a 2-line heading, use two bars of varying widths.
- **Stay Recessive:** Skeletons should use your most subtle grey (`--color-grey-100` or `grey-50`). They should not draw focus.
- **Fade into Reality:** When data arrives, fade the actual content in over the skeleton (150–200ms) rather than snapping.

---

## Fully Animated Sections

For major page transitions or initial loads, use a coordinated animation strategy.

### Staggered Entry (Cascading)
Instead of the whole page appearing at once, animate sections in a sequence. This guides the user's eye from the most important content (hero) down to secondary areas.

```css
.section {
  opacity: 0;
  transform: translateY(10px);
  animation: slide-up 400ms ease-out forwards;
}
/* Stagger by index */
.section:nth-child(1) { animation-delay: 100ms; }
.section:nth-child(2) { animation-delay: 200ms; }
.section:nth-child(3) { animation-delay: 300ms; }

@keyframes slide-up {
  to { opacity: 1; transform: translateY(0); }
}
```

### Hero Section "Bloom"
For hero sections, you might use a more complex animation:
1. **Background image** fades in slowly.
2. **Heading** slides in with a slight overshoot (spring).
3. **CTA button** appears last with a crisp fade-in or subtle color transition.

---

## Advanced: Optimistic UI

The fastest UI is one that doesn't wait for the server at all.
- **The Pattern:** Update the UI immediately assuming the server call will succeed. If it fails, roll back and show an error.
- **Use for:** Liking a post, toggling a switch, renaming a folder, deleting a message.
- **Benefit:** Instant gratification for the user, making the app feel "lightning fast."

---

## Adding Delight to the Wait

Loading doesn't have to be a neutral experience. For waits longer than 2 seconds, consider adding brand personality and "delight" to keep the user engaged.

### Brand-Aligned Micro-copy
Replace generic "Loading..." text with wording that reflects the brand's voice.
- **Technical:** "Compiling data...", "Syncing with cloud..."
- **Playful:** "Gathering pixels...", "Brewing your dashboard...", "Almost there!"
- **Professional:** "Preparing your report...", "Verifying details..."

### Branded Animations (Lottie/SVG)
For significant loading moments (initial app boot, complex data processing), replace the standard spinner with a small, brand-specific animation. 
- A designer's tool might show a pencil drawing a line.
- A fitness app might show a pulsing heart or a moving runner icon.
- A financial tool might show coins stacking or a chart line moving upward.

### Progressive Storytelling
If a wait is consistently long (3s+), use the loading area to tell a small story or provide value:
- **Tips & Tricks:** "Did you know you can use Ctrl+K to search?"
- **Process Transparency:** Show what the system is doing: "Checking database..." → "Optimising results..." → "Finalising view..."

### Visual Transitions (Arrival)

When transitioning from a loading state to content, use a crisp fade-in (150ms) to make the arrival feel like a reward. Avoid scaling the incoming content, as it can cause layout instability.

---

## Review Checklist

- [ ] Is the loading state appropriate for the expected wait duration (spinner vs skeleton)?
- [ ] Does the skeleton screen match the physical layout of the incoming content?
- [ ] Is there a subtle shimmer animation on skeletons to signal "active loading"?
- [ ] Are buttons disabled during loading to prevent duplicate actions?
- [ ] Does content fade in over skeletons (150–200ms) rather than blinking into existence?
- [ ] For full-page loads, is a staggered entry used to guide the eye?
- [ ] Is `prefers-reduced-motion` respected for all loading animations?
- [ ] In "Optimistic UI" moments, is there a clear rollback path if the action fails?

## Common Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| A global spinner that blocks the whole app | High frustration, user cannot browse other areas | Use contextual loaders or skeletons |
| Skeletons that don't match the final layout | Massive layout shift (CLS) when data arrives | Match shapes and sizes exactly |
| Too many spinners on one page | Visual noise, feels like the whole app is broken | Group loading states into a single container skeleton |
| Faster-than-light skeletons | Shimmer animation that is too fast or high-contrast | Keep shimmer slow (1.5s+) and very subtle |
