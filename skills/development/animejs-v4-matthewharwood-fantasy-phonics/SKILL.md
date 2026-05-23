---
name: animejs-v4
description: Anime.js 4.0 animations for Web Components — drag-drop, click feedback, swaps, cancelable motion. Use when adding animations, drag interactions, visual feedback, or motion to custom elements. Combines with web-components-architecture for lifecycle cleanup.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Anime.js 4.0 for Web Components

## Installation

```bash
npm i animejs
```

```javascript
import { animate, createTimeline, stagger, createSpring, createDraggable } from 'animejs';
import { createDrawable, createMotionPath, morphTo, splitText, onScroll } from 'animejs';
```

---

## Core API

### Basic Animation

```javascript
animate('.el', {
  x: 250, y: 100, rotate: 90, scale: 1.5, opacity: 0.5,
  backgroundColor: '#FFF',
  duration: 1000, delay: 200, ease: 'outQuad',
  loop: true, alternate: true
});
```

### Per-Property Control

```javascript
animate('.el', {
  x: { from: -100, to: 100, duration: 800 },
  rotate: { from: 0, to: 360, ease: 'inOutCirc' },
  scale: { to: 1.5, delay: 200 }
});
```

### Keyframes

```javascript
animate('.el', { y: [0, -50, 0], scale: [1, 1.2, 1], duration: 1000 });
```

### Stagger

```javascript
animate('.items', {
  y: -20, opacity: [0, 1],
  delay: stagger(100),                     // Sequential
  delay: stagger(100, { from: 'center' }), // From center
  delay: stagger(50, { grid: [5, 5] })     // Grid layout
});
```

### Function-Based Values

```javascript
animate('.items', {
  x: (el, i, total) => i * 50,
  rotate: (el, i) => i % 2 === 0 ? 45 : -45
});
```

---

## Playback Control

```javascript
const anim = animate('.el', { x: 100, autoplay: false });

anim.play();
anim.pause();
anim.reverse();
anim.restart();
anim.seek(500);      // Seek to 500ms
anim.seek('50%');    // Seek to 50%
```

| Method | Behavior |
|--------|----------|
| `cancel()` | Stop immediately, keep current inline styles |
| `revert()` | Stop and remove all inline styles |
| `complete()` | Jump to final values immediately |

---

## Callbacks & Promises

```javascript
animate('.el', {
  x: 100,
  onBegin: (anim) => {},
  onUpdate: (anim) => {},
  onComplete: (anim) => {}
});

await animate('.el', { x: 100 });  // Promise-based
```

---

## Timeline

```javascript
const tl = createTimeline({ loop: true, alternate: true });
tl.add('.box1', { x: 100 })
  .add('.box2', { y: 50 }, '-=200')    // 200ms before previous ends
  .add('.box3', { scale: 2 }, '+=100') // 100ms after previous
  .add('.box4', { rotate: 90 }, 500);  // At 500ms absolute

tl.label('myLabel', 1000);
tl.call(() => console.log('done'), 2000);
```

---

## Easings & Springs

**Built-in:** `linear`, `in`, `out`, `inOut`, `outIn` (with power: `out(3)`).
**Named:** `inQuad`, `outQuad`, `inOutQuad`, `inCubic`, `outExpo`, `inOutElastic`, `outBounce`, `outBack`.

```javascript
// Spring physics
animate('.el', { x: 100, ease: createSpring({ stiffness: 400, damping: 25 }) });
```

### Spring Presets

```javascript
const springs = {
  click:  createSpring({ stiffness: 600, damping: 30 }),
  move:   createSpring({ stiffness: 300, damping: 25 }),
  drop:   createSpring({ stiffness: 400, damping: 20 }),
  settle: createSpring({ stiffness: 200, damping: 25 }),
  bounce: createSpring({ stiffness: 500, damping: 10 })
};
```

---

## Web Component Integration

### Animation Manager Pattern

**Always cancel existing animations before starting new ones.** Use a WeakMap to track animations per element without memory leaks.

```javascript
class AnimationManager {
  #anims = new WeakMap();

  animate(el, props, key = 'main') {
    const map = this.#anims.get(el) || {};
    map[key]?.cancel();  // Cancel existing

    const anim = animate(el, props);
    map[key] = anim;
    this.#anims.set(el, map);
    return anim;
  }

  cancel(el, key = 'main') { this.#anims.get(el)?.[key]?.cancel(); }
  revert(el, key = 'main') { this.#anims.get(el)?.[key]?.revert(); }
}
```

### Component Lifecycle

Follows `web-components-architecture` skill — use `disconnectedCallback` for cleanup:

```javascript
class AnimatedCard extends HTMLElement {
  #anim = null;

  animate(props) {
    this.#anim?.cancel();
    this.#anim = animate(this, props);
    return this.#anim;
  }

  disconnectedCallback() {
    this.#anim?.revert();  // Clean up inline styles
  }
}
```

---

## Drag-and-Drop Animations

### Drag Start (Lift)

```javascript
function animateDragStart(card) {
  return animate(card, {
    scale: 1.12, rotate: 8,
    boxShadow: '0 20px 50px rgba(0,0,0,0.3)',
    duration: 150, ease: 'out(3)'
  });
}
```

### During Drag — Direct Transform (60fps)

**Do NOT use `animate()` for pointer tracking.** Set transform directly for smooth motion:

```javascript
function updateDragPosition(el, x, y) {
  el.style.transform = `translate(${x}px, ${y}px) scale(1.12) rotate(8deg)`;
}
```

### Drop Animation

```javascript
function animateDrop(card) {
  return animate(card, {
    x: 0, y: 0,
    scale: [1.12, 0.95, 1],
    rotate: [8, -2, 0],
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    duration: 350, ease: 'outBack'
  });
}
```

### Return to Origin

```javascript
function animateReturn(card) {
  return animate(card, {
    x: 0, y: 0, scale: 1, rotate: 0,
    duration: 400, ease: 'outBack'
  });
}
```

### Card Swap (FLIP Pattern)

```javascript
async function animateSwap(cardA, cardB, slotA, slotB) {
  const rectA = cardA.getBoundingClientRect();
  const rectB = cardB.getBoundingClientRect();

  // DOM swap first
  slotA.appendChild(cardB);
  slotB.appendChild(cardA);

  const newRectA = cardA.getBoundingClientRect();
  const newRectB = cardB.getBoundingClientRect();

  // Animate from old positions
  await Promise.all([
    animate(cardA, {
      x: [rectA.left - newRectA.left, 0],
      y: [rectA.top - newRectA.top, 0],
      scale: [1.1, 0.95, 1],
      duration: 400, ease: 'outBack'
    }),
    animate(cardB, {
      x: [rectB.left - newRectB.left, 0],
      y: [rectB.top - newRectB.top, 0],
      scale: [1, 1.05, 1],
      duration: 400, ease: 'outBack'
    })
  ]);
}
```

### Slot Hover Feedback

```javascript
function animateSlotHover(slot, isOver) {
  animate(slot, {
    scale: isOver ? 1.03 : 1,
    borderColor: isOver ? '#4CAF50' : '#999',
    duration: 150, ease: 'out(2)'
  });
}
```

---

## Click Animations

```javascript
// Bounce feedback
animate(card, {
  scale: [1, 1.15, 1],
  rotate: [0, 5, -5, 0],
  duration: 400, ease: 'outElastic(1, 0.5)'
});

// Disabled shake
animate(card, { x: [0, -8, 8, -6, 6, 0], duration: 300, ease: 'linear' });
```

---

## Scroll-Driven Animation

```javascript
animate('.el', {
  x: 300,
  autoplay: onScroll({ target: '.el', enter: 'bottom', leave: 'top', sync: true })
});
```

---

## SVG Animations

```javascript
animate(createDrawable('path'), { draw: '0 1' });           // Draw path
animate('.el', { ...createMotionPath('.path') });           // Motion path
animate('.shape1', { d: morphTo('.shape2') });              // Morph shapes
```

---

## Text Splitting

```javascript
const { chars } = splitText('.text', { chars: true });
animate(chars, { y: [20, 0], opacity: [0, 1], delay: stagger(30) });
```

---

## Built-in Draggable

```javascript
createDraggable('.el', {
  x: true, y: true, snap: 50, container: '.bounds',
  releaseEase: createSpring({ stiffness: 120, damping: 6 }),
  onDrag: (d) => {}, onRelease: (d) => {}
});
```

---

## V3 to V4 Migration

| V3 | V4 |
|----|-----|
| `anime({ targets: '.el' })` | `animate('.el', {...})` |
| `easing: 'easeOutQuad'` | `ease: 'outQuad'` |
| `direction: 'alternate'` | `alternate: true` |
| `translateX: 100` | `x: 100` |
| `anime.stagger(100)` | `stagger(100)` |
| `.finished` | `.then()` or `await` |
