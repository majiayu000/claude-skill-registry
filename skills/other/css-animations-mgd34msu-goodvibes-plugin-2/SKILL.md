---
name: css-animations
description: Creates native CSS animations using keyframes, transitions, and modern animation properties. Use when building animations without JavaScript libraries, optimizing performance, or implementing micro-interactions.
---

# CSS Animations

Native browser animations - GPU-accelerated, no dependencies, excellent performance.

## Quick Start

```css
/* Define keyframes */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Apply animation */
.element {
  animation: fadeIn 0.5s ease-out forwards;
}
```

## Transitions vs Animations

| Transitions | Animations |
|-------------|------------|
| Two states only | Multiple keyframes |
| Triggered by state change | Can auto-play |
| Simpler syntax | More control |
| `:hover`, `:focus`, class change | Loops, delays, direction |

## CSS Transitions

For simple two-state animations.

```css
.button {
  background: blue;
  transform: scale(1);
  transition: all 0.3s ease-out;

  /* Or be specific (better performance) */
  transition:
    background 0.3s ease-out,
    transform 0.2s ease-out;
}

.button:hover {
  background: darkblue;
  transform: scale(1.05);
}
```

### Transition Properties

```css
.element {
  transition-property: transform, opacity;
  transition-duration: 0.3s;
  transition-timing-function: ease-out;
  transition-delay: 0.1s;

  /* Shorthand: property duration timing-function delay */
  transition: transform 0.3s ease-out 0.1s;
}
```

## @keyframes Syntax

```css
/* Using from/to */
@keyframes slide {
  from {
    transform: translateX(-100%);
  }
  to {
    transform: translateX(0);
  }
}

/* Using percentages */
@keyframes bounce {
  0% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-30px);
  }
  100% {
    transform: translateY(0);
  }
}

/* Multiple properties at same point */
@keyframes complex {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.8;
  }
}
```

## Animation Properties

```css
.element {
  /* Required */
  animation-name: fadeIn;
  animation-duration: 0.5s;

  /* Optional */
  animation-timing-function: ease-out;
  animation-delay: 0.2s;
  animation-iteration-count: 1;       /* or infinite */
  animation-direction: normal;
  animation-fill-mode: forwards;
  animation-play-state: running;

  /* Shorthand */
  animation: fadeIn 0.5s ease-out 0.2s 1 normal forwards running;

  /* Multiple animations */
  animation:
    fadeIn 0.5s ease-out,
    slideUp 0.5s ease-out 0.1s;
}
```

### Animation Property Values

| Property | Values |
|----------|--------|
| `animation-timing-function` | `linear`, `ease`, `ease-in`, `ease-out`, `ease-in-out`, `cubic-bezier()`, `steps()` |
| `animation-iteration-count` | `1`, `2`, `3`, `infinite` |
| `animation-direction` | `normal`, `reverse`, `alternate`, `alternate-reverse` |
| `animation-fill-mode` | `none`, `forwards`, `backwards`, `both` |
| `animation-play-state` | `running`, `paused` |

### Fill Mode Explained

```css
/* none - Returns to original state after animation */
animation-fill-mode: none;

/* forwards - Keeps final keyframe state */
animation-fill-mode: forwards;

/* backwards - Applies first keyframe during delay */
animation-fill-mode: backwards;

/* both - forwards + backwards */
animation-fill-mode: both;
```

## Timing Functions

```css
/* Built-in */
animation-timing-function: linear;
animation-timing-function: ease;        /* default */
animation-timing-function: ease-in;
animation-timing-function: ease-out;
animation-timing-function: ease-in-out;

/* Custom cubic bezier */
animation-timing-function: cubic-bezier(0.68, -0.55, 0.265, 1.55);

/* Steps (for sprite animations) */
animation-timing-function: steps(6);
animation-timing-function: steps(6, start);
animation-timing-function: steps(6, end);
```

### Common Cubic Bezier Values

```css
/* Smooth deceleration */
cubic-bezier(0, 0, 0.2, 1)

/* Smooth acceleration */
cubic-bezier(0.4, 0, 1, 1)

/* Standard ease */
cubic-bezier(0.4, 0, 0.2, 1)

/* Overshoot (bouncy) */
cubic-bezier(0.68, -0.55, 0.265, 1.55)

/* Elastic */
cubic-bezier(0.68, -0.6, 0.32, 1.6)
```

## Performance Best Practices

### GPU-Accelerated Properties (Composite Only)

```css
/* GOOD - GPU accelerated, no layout/paint */
transform: translateX(100px);
transform: scale(1.5);
transform: rotate(45deg);
opacity: 0.5;

/* Hint for GPU acceleration */
will-change: transform, opacity;
```

### Avoid Animating (Cause Reflow/Repaint)

```css
/* BAD - triggers layout recalculation */
width, height, top, left, right, bottom,
margin, padding, border-width,
font-size, line-height
```

### Use Transform Instead

```css
/* Instead of: left: 100px */
transform: translateX(100px);

/* Instead of: width: 200px */
transform: scaleX(2);
```

## Common Animation Patterns

### Fade In
```css
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.fade-in {
  animation: fadeIn 0.3s ease-out forwards;
}
```

### Slide In From Bottom
```css
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.slide-up {
  animation: slideUp 0.5s ease-out forwards;
}
```

### Scale In
```css
@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
```

### Pulse
```css
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.pulse {
  animation: pulse 2s ease-in-out infinite;
}
```

### Shake
```css
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
  20%, 40%, 60%, 80% { transform: translateX(5px); }
}

.shake {
  animation: shake 0.5s ease-in-out;
}
```

### Spin
```css
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.spinner {
  animation: spin 1s linear infinite;
}
```

### Bounce
```css
@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
    animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
  }
  50% {
    transform: translateY(-25%);
    animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
  }
}

.bounce {
  animation: bounce 1s infinite;
}
```

### Skeleton Loading
```css
@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.skeleton {
  background: linear-gradient(
    90deg,
    #f0f0f0 25%,
    #e0e0e0 50%,
    #f0f0f0 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}
```

## Accessibility

### Respect Reduced Motion

```css
/* Define full animation */
.element {
  animation: fadeIn 0.5s ease-out forwards;
}

/* Reduce or remove for users who prefer reduced motion */
@media (prefers-reduced-motion: reduce) {
  .element {
    animation: none;
    opacity: 1;
  }

  /* Or use simpler animation */
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Pause on Hover (for continuous animations)

```css
.element {
  animation: spin 2s linear infinite;
}

.element:hover {
  animation-play-state: paused;
}
```

## JavaScript Control

```javascript
// Add animation class
element.classList.add('animate-in');

// Remove after animation ends
element.addEventListener('animationend', () => {
  element.classList.remove('animate-in');
});

// Restart animation
function restartAnimation(element) {
  element.style.animation = 'none';
  element.offsetHeight; // Trigger reflow
  element.style.animation = null;
}

// Pause/resume
element.style.animationPlayState = 'paused';
element.style.animationPlayState = 'running';
```

### Animation Events

```javascript
element.addEventListener('animationstart', (e) => {
  console.log('Started:', e.animationName);
});

element.addEventListener('animationiteration', (e) => {
  console.log('Iteration:', e.elapsedTime);
});

element.addEventListener('animationend', (e) => {
  console.log('Ended:', e.animationName);
});

element.addEventListener('animationcancel', (e) => {
  console.log('Cancelled');
});
```

## Staggered Animations

```css
.item { animation: fadeIn 0.5s ease-out forwards; opacity: 0; }
.item:nth-child(1) { animation-delay: 0.1s; }
.item:nth-child(2) { animation-delay: 0.2s; }
.item:nth-child(3) { animation-delay: 0.3s; }
.item:nth-child(4) { animation-delay: 0.4s; }
.item:nth-child(5) { animation-delay: 0.5s; }

/* With CSS custom properties */
.item {
  animation: fadeIn 0.5s ease-out forwards;
  animation-delay: calc(var(--index) * 0.1s);
  opacity: 0;
}
```

```html
<div class="item" style="--index: 0">Item 1</div>
<div class="item" style="--index: 1">Item 2</div>
<div class="item" style="--index: 2">Item 3</div>
```

## CSS Custom Properties for Dynamic Animations

```css
:root {
  --animation-duration: 0.3s;
  --animation-easing: cubic-bezier(0.4, 0, 0.2, 1);
}

.element {
  transition: transform var(--animation-duration) var(--animation-easing);
}

/* Override per component */
.modal {
  --animation-duration: 0.5s;
}
```

## Reference Files

- [references/keyframe-patterns.md](references/keyframe-patterns.md) - Common animation patterns library
