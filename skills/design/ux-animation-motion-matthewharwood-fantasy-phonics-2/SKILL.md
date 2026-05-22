---
name: ux-animation-motion
description: Animation patterns using Anime.js v4 for UI feedback, transitions, and celebrations. Use when implementing hover effects, transitions, loading animations, or gamification feedback. Includes reduced motion handling. (project)
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# UX Animation & Motion Skill

Animation system using Anime.js v4 for responsive, accessible UI motion. This skill covers animation patterns, timing, and reduced motion support.

## Related Skills

- **`animejs-v4`**: Complete Anime.js 4.0 API reference
- **`js-micro-utilities`**: Array utilities like `.at(-1)` for accessing last element
- **`ux-iconography`**: Icon animation patterns
- **`ux-accessibility`**: Reduced motion requirements

## Animation Import

```javascript
import { animate } from 'animejs';
```

Note: Project uses import maps to resolve `animejs` to local node_modules.

## Animation Utilities

The project provides reusable animations in `js/utils/animations.js`:

```javascript
import {
  shake,
  pressEffect,
  successBounce,
  glow,
  DURATION,
  EASE
} from '../../utils/animations.js';
```

### Duration Constants

```javascript
const DURATION = {
  instant: 100,    // Micro-interactions
  quick: 200,      // Button press, toggles
  normal: 300,     // Standard transitions
  slow: 500,       // Page transitions
  celebration: 600 // Success animations
};
```

### Easing Functions

```javascript
const EASE = {
  snap: 'easeOutQuad',     // Quick, snappy feel
  smooth: 'easeInOutQuad', // Gentle transitions
  bounceOut: 'easeOutBack' // Playful, overshooting
};
```

## Animation Patterns

### Press Effect (Tactile Feedback)

For button clicks and taps:

```javascript
pressEffect(element);
// or
animate(element, {
  scale: [1, 0.95, 1],
  duration: DURATION.instant,
  ease: EASE.snap
});
```

### Success Bounce

For completed actions:

```javascript
successBounce(element);
// or
animate(element, {
  scale: [1, 1.1, 1],
  duration: DURATION.normal,
  ease: EASE.bounceOut
});
```

### Shake (Error/Invalid)

For validation failures:

```javascript
shake(element, { intensity: 6 });
// or
animate(element, {
  translateX: [-6, 6, -6, 6, -3, 3, 0],
  duration: DURATION.normal,
  ease: EASE.snap
});
```

### Glow Effect

For achievements or highlights:

```javascript
glow(element, {
  color: 'rgba(74, 222, 128, 0.6)',
  intensity: 15
});
// Uses box-shadow animation
```

### Pulse (Attention)

For elements requiring attention:

```css
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.attention {
  animation: pulse 1.5s ease-in-out infinite;
}
```

## Transition Patterns

### Fade In

```javascript
animate(element, {
  opacity: [0, 1],
  duration: DURATION.normal,
  ease: EASE.smooth
});
```

### Slide In

```javascript
animate(element, {
  translateY: [20, 0],
  opacity: [0, 1],
  duration: DURATION.normal,
  ease: EASE.snap
});
```

### Scale In

```javascript
animate(element, {
  scale: [0.9, 1],
  opacity: [0, 1],
  duration: DURATION.quick,
  ease: EASE.bounceOut
});
```

### Staggered List

```javascript
animate('.list-item', {
  translateY: [20, 0],
  opacity: [0, 1],
  delay: (el, i) => i * 50,
  duration: DURATION.normal,
  ease: EASE.snap
});
```

## State Change Animations

### Attribute Change Response

```javascript
attributeChangedCallback(name, oldVal, newVal) {
  if (name === 'completed' && newVal !== null) {
    this.#animateComplete();
  }
}

#animateComplete() {
  animate(this, {
    scale: [1, 2, 1],
    duration: DURATION.normal,
    ease: EASE.bounceOut
  });
}
```

### Phase Transition

```javascript
#animatePhaseChange() {
  animate(this.#container, {
    opacity: [1, 0, 1],
    duration: DURATION.slow,
    ease: EASE.smooth
  });
}
```

## Game Feedback Animations

### Word Completion

```javascript
#celebrateWord() {
  successBounce(this.#wordElement);
  glow(this.#wordElement, { color: 'rgba(74, 222, 128, 0.6)' });
}
```

### Score Update

```javascript
#animateScore() {
  animate(this.#scoreElement, {
    scale: [1, 1.2, 1],
    duration: DURATION.quick,
    ease: EASE.bounceOut
  });
}
```

### Achievement Unlock

```javascript
#celebrateAchievement() {
  animate(this.#badge, {
    scale: [0, 1.2, 1],
    rotate: [0, -10, 10, 0],
    duration: DURATION.celebration,
    ease: EASE.bounceOut
  });
}
```

## Reduced Motion Support

### Check Preference

```javascript
const prefersReducedMotion = window.matchMedia(
  '(prefers-reduced-motion: reduce)'
).matches;

if (!prefersReducedMotion) {
  animate(element, { scale: [1, 1.1, 1] });
} else {
  // Instant state change instead
  element.classList.add('completed');
}
```

### CSS Fallback

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Safe Animation Wrapper

```javascript
function safeAnimate(element, props) {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    // Apply final state immediately
    if (props.scale) element.style.transform = `scale(${props.scale.at(-1)})`;
    if (props.opacity) element.style.opacity = props.opacity.at(-1);
    return;
  }
  return animate(element, props);
}
```

## CSS Transitions

For simple state changes, prefer CSS:

```css
.button {
  transition:
    background-color 0.15s ease,
    transform 0.1s ease,
    opacity 0.15s ease;
}

.button:hover {
  background: var(--color-hover-overlay);
}

.button:active {
  transform: scale(0.98);
}
```

## Loading Animations

### Spinner

```css
.spinner {
  width: 24px;
  height: 24px;
  border: 2px solid var(--theme-outline);
  border-top-color: var(--theme-primary);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { rotate: 360deg; }
}
```

### Dots

```css
.loading-dots span {
  animation: bounce 1s ease-in-out infinite;
}

.loading-dots span:nth-child(2) { animation-delay: 0.1s; }
.loading-dots span:nth-child(3) { animation-delay: 0.2s; }

@keyframes bounce {
  0%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-6px); }
}
```

## Performance Guidelines

### Do

- Use `transform` and `opacity` for smooth 60fps
- Keep animations under 300ms for interactions
- Use `will-change` sparingly for complex animations
- Cancel animations when element unmounts

### Don't

- Animate `width`, `height`, `margin`, `padding`
- Use long durations for frequent interactions
- Chain many sequential animations
- Animate elements off-screen

### Cleanup

```javascript
#animation = null;

disconnectedCallback() {
  if (this.#animation) {
    this.#animation.pause();
    this.#animation = null;
  }
}
```

## Animation Timing Reference

| Action | Duration | Easing |
|--------|----------|--------|
| Button press | 100ms | easeOutQuad |
| Toggle switch | 150ms | easeOutQuad |
| Dropdown open | 200ms | easeOutQuad |
| Modal appear | 200-300ms | easeOutBack |
| Page transition | 300-500ms | easeInOutQuad |
| Success celebration | 400-600ms | easeOutBack |
