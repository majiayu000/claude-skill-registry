---
name: web-animation-view-transitions
description: View Transitions API patterns - same-document transitions, cross-document MPA transitions, shared element animations, pseudo-element styling, accessibility
---

# View Transitions API Patterns

> **Quick Guide:** Use the View Transitions API for native page/state transitions. `document.startViewTransition()` for same-document, `@view-transition { navigation: auto }` for cross-document MPA. Always feature-detect before use and respect `prefers-reduced-motion`.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST feature-detect before using startViewTransition - it is NOT available in all browsers)**

**(You MUST respect prefers-reduced-motion by providing reduced or disabled animations)**

**(You MUST ensure view-transition-name values are unique - duplicate names break transitions)**

**(You MUST clean up dynamically assigned view-transition-name values after transitions complete)**

**(You MUST use named constants for all animation timing values - NO magic numbers)**

</critical_requirements>

---

**Auto-detection:** View Transitions API, startViewTransition, view-transition-name, @view-transition, ::view-transition, pageswap, pagereveal, ViewTransition, view-transition-class

**When to use:**

- Animating state changes in single-page applications
- Creating smooth page-to-page transitions in multi-page applications
- Implementing shared element (hero) animations between views
- Providing visual continuity during navigation
- Creating custom transition effects (slide, scale, circular reveal)

**Key patterns covered:**

- Same-document transitions with startViewTransition()
- Cross-document MPA transitions with @view-transition CSS
- view-transition-name for shared element animations
- Pseudo-element styling (::view-transition-old, ::view-transition-new)
- Direction-aware transitions with :active-view-transition-type()
- Feature detection and graceful fallbacks
- prefers-reduced-motion accessibility patterns

**When NOT to use:**

- Complex physics-based animations (use animation libraries)
- Animations requiring precise timeline control
- Browsers without View Transitions support (always provide fallback)
- Simple hover/focus effects (use CSS transitions)

**Detailed Resources:**

- For code examples, see [examples/](examples/) folder
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

The View Transitions API provides a native browser mechanism for creating animated transitions between DOM states or pages. It captures "before" and "after" snapshots, overlays them as pseudo-elements, and animates between them.

**Core principles:**

1. **Native over library** - Browser-native transitions are more performant and require less JavaScript
2. **Progressive enhancement** - Always feature-detect and provide functional fallback
3. **Snapshot-based** - Old state is captured as a screenshot, new state as a live representation
4. **CSS-driven** - Customize animations through pseudo-element CSS, not JavaScript
5. **Accessibility-first** - Always respect prefers-reduced-motion user preferences

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Feature Detection with Fallback

Always check for API support before using View Transitions.

#### Basic Feature Detection

```typescript
const SUPPORTS_VIEW_TRANSITIONS =
  typeof document !== "undefined" && "startViewTransition" in document;

function updateWithTransition(updateFn: () => void | Promise<void>): void {
  if (!SUPPORTS_VIEW_TRANSITIONS) {
    updateFn();
    return;
  }

  document.startViewTransition(() => updateFn());
}
```

**Why good:** Prevents runtime errors in unsupported browsers, provides seamless fallback, named constant for reusability

```typescript
// Bad Example - No feature detection
document.startViewTransition(() => updateDOM()); // Crashes in Firefox < 144!
```

**Why bad:** Crashes in unsupported browsers, no fallback for users without support

---

### Pattern 2: Same-Document (SPA) Transitions

Animate DOM state changes within a single page using startViewTransition().

#### Basic State Transition

```typescript
const TRANSITION_DURATION_MS = 300;

type ViewTransitionCallback = () => void | Promise<void>;

async function transitionTo(updateFn: ViewTransitionCallback): Promise<void> {
  if (!document.startViewTransition) {
    await updateFn();
    return;
  }

  const transition = document.startViewTransition(async () => {
    await updateFn();
  });

  await transition.finished;
}

// Usage
function handleNavigation(page: string): void {
  transitionTo(() => {
    setCurrentPage(page);
  });
}
```

**Why good:** Wraps feature detection, handles async updates, returns promise for chaining

#### ViewTransition Object Properties

```typescript
interface ViewTransitionPromises {
  ready: Promise<void>; // Pseudo-element tree created
  updateCallbackDone: Promise<void>; // DOM update complete
  finished: Promise<void>; // Animation finished
}

async function transitionWithCustomAnimation(
  updateFn: () => void,
): Promise<void> {
  if (!document.startViewTransition) {
    updateFn();
    return;
  }

  const transition = document.startViewTransition(updateFn);

  // Wait for pseudo-elements to be ready
  await transition.ready;

  // Now safe to apply custom animations via Web Animations API
  console.log("Pseudo-elements ready for custom animation");

  await transition.finished;
  console.log("Transition complete");
}
```

**Why good:** Shows the three promise stages for different timing needs

---

### Pattern 3: Cross-Document (MPA) Transitions

Enable transitions between separate pages without JavaScript.

#### CSS Opt-In

```css
/* styles.css - Include on BOTH pages */
@view-transition {
  navigation: auto;
}
```

**Why good:** No JavaScript required, works for traverse/push/replace navigations

```css
/* Bad Example - Obsolete meta tag syntax */
/* <meta name="view-transition" content="same-origin"> */

/* Good - Use CSS at-rule instead */
@view-transition {
  navigation: auto;
}
```

**Why bad:** Meta tag syntax is obsolete, CSS at-rule is the current standard

---

### Pattern 4: Shared Element Transitions

Create hero animations by giving matching elements the same view-transition-name.

#### CSS Shared Elements

```css
/* On list page */
.product-thumbnail {
  view-transition-name: product-hero;
}

/* On detail page */
.product-image {
  view-transition-name: product-hero;
}

/* Customize the transition */
::view-transition-group(product-hero) {
  animation-duration: 300ms;
  animation-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
```

**Why good:** Same name creates automatic shared element transition, custom timing via pseudo-element

#### Dynamic Name Assignment

```typescript
function setTransitionNames(elements: Array<[HTMLElement, string]>): void {
  elements.forEach(([el, name]) => {
    el.style.viewTransitionName = name;
  });
}

function clearTransitionNames(elements: HTMLElement[]): void {
  elements.forEach((el) => {
    el.style.viewTransitionName = "";
  });
}

async function transitionWithSharedElement(
  element: HTMLElement,
  name: string,
  updateFn: () => void,
): Promise<void> {
  if (!document.startViewTransition) {
    updateFn();
    return;
  }

  element.style.viewTransitionName = name;

  const transition = document.startViewTransition(updateFn);
  await transition.finished;

  // Clean up to prevent conflicts
  element.style.viewTransitionName = "";
}
```

**Why good:** Dynamic assignment allows programmatic control, cleanup prevents name conflicts

---

### Pattern 5: Custom CSS Animations

Override default cross-fade with custom animations via pseudo-elements.

#### Slide Transitions

```css
/* Named constants as CSS custom properties */
:root {
  --transition-duration: 300ms;
  --transition-easing: ease-in-out;
}

@keyframes slide-out-left {
  to {
    transform: translateX(-100%);
  }
}

@keyframes slide-in-right {
  from {
    transform: translateX(100%);
  }
}

::view-transition-old(root) {
  animation: slide-out-left var(--transition-duration) var(--transition-easing);
}

::view-transition-new(root) {
  animation: slide-in-right var(--transition-duration) var(--transition-easing);
}
```

**Why good:** CSS custom properties for timing constants, GPU-accelerated transforms

#### Scale and Fade

```css
:root {
  --scale-duration: 250ms;
  --scale-hidden: 0.95;
}

@keyframes scale-down {
  to {
    transform: scale(var(--scale-hidden));
    opacity: 0;
  }
}

@keyframes scale-up {
  from {
    transform: scale(calc(1 / var(--scale-hidden)));
    opacity: 0;
  }
}

::view-transition-old(root) {
  animation: scale-down var(--scale-duration) ease-in;
}

::view-transition-new(root) {
  animation: scale-up var(--scale-duration) ease-out;
}
```

**Why good:** Scale and opacity are GPU-accelerated, CSS variables for consistent values

---

### Pattern 6: Direction-Aware Transitions

Use different animations for forward vs backward navigation.

#### CSS with active-view-transition-type

```css
/* Forward navigation */
html:active-view-transition-type(forwards) {
  &::view-transition-old(content) {
    animation-name: slide-out-left;
  }
  &::view-transition-new(content) {
    animation-name: slide-in-right;
  }
}

/* Backward navigation */
html:active-view-transition-type(backwards) {
  &::view-transition-old(content) {
    animation-name: slide-out-right;
  }
  &::view-transition-new(content) {
    animation-name: slide-in-left;
  }
}

@keyframes slide-out-right {
  to {
    transform: translateX(100%);
  }
}

@keyframes slide-in-left {
  from {
    transform: translateX(-100%);
  }
}
```

#### Setting Navigation Types

```typescript
function setNavigationType(
  transition: ViewTransition,
  type: "forwards" | "backwards",
): void {
  if ("types" in transition) {
    (transition.types as Set<string>).add(type);
  }
}

// For MPA, use pagereveal event
window.addEventListener("pagereveal", (e) => {
  const event = e as PageRevealEvent;
  if (event.viewTransition && "activation" in navigation) {
    const navActivation = navigation.activation;
    if (navActivation) {
      const fromUrl = navActivation.from?.url;
      const toUrl = navActivation.entry?.url;

      // Determine direction based on URL structure
      if (fromUrl && toUrl) {
        const isForward = toUrl.includes("/detail");
        setNavigationType(
          event.viewTransition,
          isForward ? "forwards" : "backwards",
        );
      }
    }
  }
});
```

**Why good:** Different animations for different navigation directions improve UX

---

### Pattern 7: Accessibility - Reduced Motion

Always respect user preferences for reduced motion.

#### CSS Approach

```css
@media (prefers-reduced-motion: reduce) {
  ::view-transition-old(root),
  ::view-transition-new(root) {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
  }

  /* Or disable entirely */
  ::view-transition-group(*),
  ::view-transition-old(*),
  ::view-transition-new(*) {
    animation: none !important;
  }
}

/* Provide subtle alternative feedback */
@media (prefers-reduced-motion: reduce) {
  ::view-transition-old(root) {
    animation: fade-out 150ms ease-out;
  }
  ::view-transition-new(root) {
    animation: fade-in 150ms ease-in;
  }
}

@keyframes fade-out {
  to {
    opacity: 0;
  }
}

@keyframes fade-in {
  from {
    opacity: 0;
  }
}
```

**Why good:** Respects user preferences, provides subtle alternative instead of nothing

#### JavaScript Approach

```typescript
const REDUCED_MOTION_QUERY = "(prefers-reduced-motion: reduce)";

function shouldEnableTransitions(): boolean {
  // Check reduced motion preference
  if (window.matchMedia(REDUCED_MOTION_QUERY).matches) {
    return false;
  }

  // Check for API support
  return "startViewTransition" in document;
}

function transitionWithAccessibility(updateFn: () => void): void {
  if (!shouldEnableTransitions()) {
    updateFn();
    return;
  }

  document.startViewTransition(updateFn);
}

// Hook for monitoring preference changes
function useReducedMotion(): boolean {
  const query = window.matchMedia(REDUCED_MOTION_QUERY);
  let prefersReduced = query.matches;

  query.addEventListener("change", (e) => {
    prefersReduced = e.matches;
  });

  return prefersReduced;
}
```

**Why good:** Checks preference before initiating transition, reactive to preference changes

---

### Pattern 8: Circular Reveal Effect

Advanced custom animation using Web Animations API.

```typescript
interface ClickPosition {
  x: number;
  y: number;
}

let lastClickPosition: ClickPosition = { x: 0, y: 0 };

document.addEventListener("click", (e: MouseEvent) => {
  lastClickPosition = { x: e.clientX, y: e.clientY };
});

const REVEAL_DURATION_MS = 500;
const REVEAL_EASING = "ease-in-out";

async function circularRevealTransition(updateFn: () => void): Promise<void> {
  if (!document.startViewTransition) {
    updateFn();
    return;
  }

  const { x, y } = lastClickPosition;
  const endRadius = Math.hypot(
    Math.max(x, window.innerWidth - x),
    Math.max(y, window.innerHeight - y),
  );

  const transition = document.startViewTransition(updateFn);

  await transition.ready;

  document.documentElement.animate(
    {
      clipPath: [
        `circle(0 at ${x}px ${y}px)`,
        `circle(${endRadius}px at ${x}px ${y}px)`,
      ],
    },
    {
      duration: REVEAL_DURATION_MS,
      easing: REVEAL_EASING,
      pseudoElement: "::view-transition-new(root)",
    },
  );
}
```

**Supporting CSS:**

```css
::view-transition-image-pair(root) {
  isolation: auto;
}

::view-transition-old(root),
::view-transition-new(root) {
  animation: none;
  mix-blend-mode: normal;
  display: block;
}
```

**Why good:** Creates engaging circular reveal from click point, uses Web Animations API for precise control

</patterns>

---

<integration>

## Integration Guide

**View Transitions is a browser-native API.** It works with any JavaScript approach and styling solution.

**Works with:**

- **Any DOM manipulation**: Updates via direct DOM, signals, or virtual DOM all work
- **Any routing solution**: Wrap route changes in startViewTransition()
- **Any styling approach**: Customize via CSS pseudo-elements

**Key integration points:**

- Call `document.startViewTransition()` before DOM updates
- Use CSS `@view-transition` for cross-document navigation
- Set `view-transition-name` via CSS or JavaScript for shared elements

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST feature-detect before using startViewTransition - it is NOT available in all browsers)**

**(You MUST respect prefers-reduced-motion by providing reduced or disabled animations)**

**(You MUST ensure view-transition-name values are unique - duplicate names break transitions)**

**(You MUST clean up dynamically assigned view-transition-name values after transitions complete)**

**(You MUST use named constants for all animation timing values - NO magic numbers)**

**Failure to follow these rules will break transitions in unsupported browsers and create inaccessible experiences.**

</critical_reminders>
