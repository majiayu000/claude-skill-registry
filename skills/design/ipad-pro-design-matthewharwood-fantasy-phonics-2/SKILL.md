---
name: ipad-pro-design
description: CSS and UX patterns for iPad Pro 12.9" development. Covers viewport configuration, touch optimization, safe areas, ProMotion animations, and child-friendly design patterns. Use when building educational apps targeting iPad Pro.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# iPad Pro 12.9" Design Skill

Comprehensive CSS and UX patterns for building educational web applications optimized for iPad Pro 12.9" (M1/M2/M4). This skill integrates with the project's Utopia fluid scales and web components architecture.

## Related Skills

- **`utopia-fluid-scales`**: Fluid typography and spacing tokens (cqi-based)
- **`utopia-container-queries`**: Container setup for fluid scales
- **`web-components`**: Component architecture patterns
- **`ux-accessibility`**: Focus management and WCAG compliance
- **`ux-animation-motion`**: Animation timing and reduced motion
- **`animejs-v4`**: Hardware-accelerated animations

---

## iPad Pro 12.9" Technical Specifications

### Display Specifications

| Property | Value |
|----------|-------|
| Screen Resolution | 2732 x 2048 pixels |
| Points Resolution | 1366 x 1024 points |
| Device Pixel Ratio | 2x (@2x Retina) |
| PPI | 264 pixels per inch |
| Display Type | Liquid Retina XDR |
| Refresh Rate | ProMotion 24-120Hz adaptive |
| Color | P3 wide color gamut |
| Peak Brightness | 1600 nits HDR, 1000 nits full-screen |

### Viewport Calculations

```
CSS Pixels (Landscape): 1366 x 1024
CSS Pixels (Portrait):  1024 x 1366
Device Pixels (Landscape): 2732 x 2048
Device Pixels (Portrait):  2048 x 2732
```

### Safe Areas

| Edge | Safe Inset (Points) |
|------|---------------------|
| Top (Portrait, no notch) | 24pt status bar |
| Top (Landscape, no notch) | 24pt status bar |
| Bottom (all orientations) | 20pt home indicator |
| Left/Right (Landscape) | 0pt (no notch on 12.9") |

---

## Viewport Configuration

### Required Meta Tag

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```

| Attribute | Purpose |
|-----------|---------|
| `width=device-width` | Match CSS viewport to device width |
| `initial-scale=1` | Prevent default zoom, 1:1 scale |
| `viewport-fit=cover` | Extend content to screen edges (enables safe area insets) |

### AVOID These Viewport Settings

```html
<!-- DON'T: Disabling zoom breaks accessibility -->
<meta name="viewport" content="... user-scalable=no">
<meta name="viewport" content="... maximum-scale=1">

<!-- DON'T: Fixed width creates horizontal scroll -->
<meta name="viewport" content="width=1024">
```

### PWA Optimizations

```html
<!-- Full-screen web app (home screen) -->
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">

<!-- Prevent text size adjustment -->
<meta name="apple-mobile-web-app-title" content="Fantasy Phonics">

<!-- Theme color for Safari UI -->
<meta name="theme-color" content="#252119">
```

---

## Safe Area Handling

### CSS Environment Variables

Safari on iPadOS provides safe area values via `env()`:

```css
:root {
  /* Safe area fallbacks for non-Safari browsers */
  --safe-area-inset-top: env(safe-area-inset-top, 0px);
  --safe-area-inset-right: env(safe-area-inset-right, 0px);
  --safe-area-inset-bottom: env(safe-area-inset-bottom, 0px);
  --safe-area-inset-left: env(safe-area-inset-left, 0px);
}
```

### Applying Safe Areas

```css
/* Full-screen layout with safe areas */
.app-container {
  padding-top: var(--safe-area-inset-top);
  padding-right: var(--safe-area-inset-right);
  padding-bottom: var(--safe-area-inset-bottom);
  padding-left: var(--safe-area-inset-left);
}

/* Fixed bottom navigation */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding-bottom: calc(var(--space-s) + var(--safe-area-inset-bottom));
}

/* Fixed header */
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  padding-top: calc(var(--space-s) + var(--safe-area-inset-top));
}
```

### Home Indicator Avoidance

The home indicator appears at the bottom of screen. Avoid placing interactive elements in this zone:

```css
.interactive-bottom-zone {
  /* Ensure 20pt clearance from bottom */
  margin-bottom: max(20px, var(--safe-area-inset-bottom));
}
```

---

## Touch Target Optimization

### Apple Human Interface Guidelines

| Guideline | Value | Project Token |
|-----------|-------|---------------|
| Minimum touch target | 44pt x 44pt | `--min-touch-target` |
| Recommended touch target | 48pt x 48pt | Use `--space-xl` |
| Child-friendly target | 56pt+ | Use `--space-2xl` |
| Spacing between targets | 8pt minimum | Use `--space-2xs` |

### Touch Target Patterns

```css
/* Standard touch target (adults) */
.touch-target {
  min-width: var(--min-touch-target);
  min-height: var(--min-touch-target);
}

/* Large touch target (children 3-8 years) */
.touch-target-child {
  min-width: var(--space-2xl);   /* 72-80px */
  min-height: var(--space-2xl);
}

/* Extra-large target (toddlers/accessibility) */
.touch-target-xl {
  min-width: var(--space-3xl);   /* 108-120px */
  min-height: var(--space-3xl);
}

/* Expanded hit area for small visual elements */
.touch-expand::before {
  content: '';
  position: absolute;
  inset: -8px;
  /* Or for child-friendly: */
  inset: calc(-1 * var(--space-s));
}
```

### Button Sizing for Children

```css
/* Primary game button - child-friendly */
.game-button {
  min-width: var(--space-3xl);
  min-height: var(--space-2xl);
  padding: var(--space-m) var(--space-xl);
  font-size: var(--step-1);
  border-radius: var(--space-s);
}

/* Card selection - large tap area */
.word-card {
  min-width: 120px;
  min-height: 120px;
  padding: var(--space-m);
}
```

---

## Media Queries for iPad Pro

### Device-Specific Targeting

```css
/* iPad Pro 12.9" Landscape */
@media screen and (min-width: 1024px) and (max-width: 1366px) and (orientation: landscape) {
  /* Landscape-specific styles */
}

/* iPad Pro 12.9" Portrait */
@media screen and (min-width: 1024px) and (max-width: 1366px) and (orientation: portrait) {
  /* Portrait-specific styles */
}

/* iPad Pro 12.9" - Any orientation */
@media screen and (min-width: 1024px) and (max-width: 1366px) {
  /* Tablet-specific styles */
}

/* High-DPI screens (Retina) */
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
  /* High-DPI assets and adjustments */
}
```

### Pointer and Hover Detection

iPadOS supports both touch and Apple Pencil/trackpad. Detect input type:

```css
/* Touch-only devices */
@media (hover: none) and (pointer: coarse) {
  .tooltip-trigger:hover .tooltip {
    /* Don't show hover tooltips on touch */
    display: none;
  }
}

/* Devices with fine pointer (trackpad/mouse) */
@media (hover: hover) and (pointer: fine) {
  .interactive:hover {
    /* Show hover states */
    background: var(--color-hover-overlay);
  }
}

/* Devices with coarse pointer (finger/stylus) */
@media (pointer: coarse) {
  .interactive {
    /* Larger touch targets */
    min-height: var(--min-touch-target);
    min-width: var(--min-touch-target);
  }
}
```

### Container Queries (Preferred)

Container queries are preferred over viewport queries for component responsiveness:

```css
/* Set container on parent */
.game-board {
  container-type: inline-size;
}

/* Component responds to container, not viewport */
@container (inline-size > 800px) {
  .word-card {
    flex-direction: row;
    padding: var(--space-l);
  }
}

@container (inline-size <= 600px) {
  .word-card {
    flex-direction: column;
    padding: var(--space-m);
  }
}
```

---

## ProMotion (120Hz) Animation Optimization

### Hardware Acceleration

Safari on iPadOS uses hardware acceleration for specific CSS properties. **Always animate these properties for smooth 120Hz performance:**

| Property | Hardware Accelerated |
|----------|---------------------|
| `transform` | Yes - always use |
| `opacity` | Yes - always use |
| `filter` | Yes (simple filters) |
| `backdrop-filter` | Yes |
| `will-change` | Promotes to GPU layer |

| Property | NOT Hardware Accelerated |
|----------|-------------------------|
| `width`, `height` | Triggers layout |
| `margin`, `padding` | Triggers layout |
| `top`, `left`, `right`, `bottom` | Triggers layout |
| `border-width` | Triggers layout |
| `font-size` | Triggers layout |
| `box-shadow` | CPU intensive |

### Animation Timing for 120Hz

At 120Hz, each frame is 8.33ms. Animation timing feels different:

```css
:root {
  /* Snappy micro-interactions */
  --duration-instant: 100ms;  /* 12 frames at 120Hz */
  --duration-quick: 150ms;    /* 18 frames at 120Hz */
  --duration-normal: 200ms;   /* 24 frames at 120Hz */
  --duration-slow: 350ms;     /* 42 frames at 120Hz */

  /* Ease curves for natural feel */
  --ease-out: cubic-bezier(0.0, 0.0, 0.2, 1);     /* Decelerate */
  --ease-in-out: cubic-bezier(0.4, 0.0, 0.2, 1); /* Standard */
  --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275); /* Overshoot */
}
```

### CSS Transitions (ProMotion Optimized)

```css
.card {
  /* Use transform instead of position */
  transform: translateY(0) scale(1);
  opacity: 1;
  transition:
    transform var(--duration-normal) var(--ease-out),
    opacity var(--duration-quick) var(--ease-out);
}

.card:active {
  /* Press feedback - instant response */
  transform: scale(0.97);
  transition-duration: var(--duration-instant);
}

.card.selected {
  transform: translateY(-8px) scale(1.02);
}
```

### Anime.js 4.0 for Complex Animations

Use Anime.js for multi-property animations:

```javascript
import { animate, createSpring } from 'animejs';

// Check reduced motion preference first
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

function cardSelectAnimation(element) {
  if (prefersReducedMotion) {
    element.classList.add('selected');
    return;
  }

  return animate(element, {
    scale: [1, 1.05, 1],
    translateY: [0, -8, -4],
    duration: 250,
    ease: 'outBack'
  });
}

// Spring physics for natural feel
function dragDropAnimation(element) {
  return animate(element, {
    x: 0,
    y: 0,
    ease: createSpring({ stiffness: 400, damping: 25 }),
  });
}
```

### will-change Usage

Use `will-change` sparingly - only on elements that will animate:

```css
/* Apply before animation starts */
.card {
  will-change: transform;
}

/* Remove after animation completes (via JavaScript) */
.card.animation-complete {
  will-change: auto;
}
```

```javascript
// Anime.js lifecycle hooks
animate(element, {
  scale: [1, 1.1, 1],
  onBegin: () => {
    element.style.willChange = 'transform';
  },
  onComplete: () => {
    element.style.willChange = 'auto';
  }
});
```

---

## Touch Interaction Patterns

### Pointer Events (Unified API)

Use Pointer Events API for unified touch/mouse/stylus handling:

```javascript
class DraggableCard extends HTMLElement {
  #isDragging = false;
  #startX = 0;
  #startY = 0;

  connectedCallback() {
    this.addEventListener('pointerdown', this);
    this.addEventListener('pointermove', this);
    this.addEventListener('pointerup', this);
    this.addEventListener('pointercancel', this);

    // Prevent default touch behaviors
    this.style.touchAction = 'none';
  }

  disconnectedCallback() {
    this.removeEventListener('pointerdown', this);
    this.removeEventListener('pointermove', this);
    this.removeEventListener('pointerup', this);
    this.removeEventListener('pointercancel', this);
  }

  handleEvent(e) {
    switch (e.type) {
      case 'pointerdown':
        this.#handlePointerDown(e);
        break;
      case 'pointermove':
        this.#handlePointerMove(e);
        break;
      case 'pointerup':
      case 'pointercancel':
        this.#handlePointerUp(e);
        break;
    }
  }

  #handlePointerDown(e) {
    this.#isDragging = true;
    this.#startX = e.clientX;
    this.#startY = e.clientY;

    // Capture pointer for reliable tracking
    this.setPointerCapture(e.pointerId);

    // Visual feedback
    this.setAttribute('aria-grabbed', 'true');
  }

  #handlePointerMove(e) {
    if (!this.#isDragging) return;

    const deltaX = e.clientX - this.#startX;
    const deltaY = e.clientY - this.#startY;

    // Direct transform for 120Hz smoothness - no animate() during drag
    this.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
  }

  #handlePointerUp(e) {
    if (!this.#isDragging) return;

    this.#isDragging = false;
    this.releasePointerCapture(e.pointerId);
    this.removeAttribute('aria-grabbed');

    // Animate back with physics
    this.#animateDrop();
  }

  #animateDrop() {
    animate(this, {
      x: 0,
      y: 0,
      duration: 300,
      ease: 'outBack'
    });
  }
}
```

### CSS touch-action Control

```css
/* Allow vertical scroll only */
.scrollable-list {
  touch-action: pan-y;
}

/* Disable all touch behaviors (for custom drag) */
.draggable {
  touch-action: none;
}

/* Allow pinch-zoom but not pan */
.zoomable-image {
  touch-action: pinch-zoom;
}

/* Default - allow all */
.interactive {
  touch-action: manipulation; /* Disables double-tap zoom delay */
}
```

### Tap vs Long-Press

```javascript
class TappableElement extends HTMLElement {
  #longPressTimeout = null;
  #longPressTriggered = false;
  static LONG_PRESS_DURATION = 500; // ms

  connectedCallback() {
    this.addEventListener('pointerdown', this);
    this.addEventListener('pointerup', this);
    this.addEventListener('pointercancel', this);
  }

  handleEvent(e) {
    switch (e.type) {
      case 'pointerdown':
        this.#longPressTriggered = false;
        this.#longPressTimeout = setTimeout(() => {
          this.#longPressTriggered = true;
          this.#handleLongPress(e);
        }, TappableElement.LONG_PRESS_DURATION);
        break;

      case 'pointerup':
        clearTimeout(this.#longPressTimeout);
        if (!this.#longPressTriggered) {
          this.#handleTap(e);
        }
        break;

      case 'pointercancel':
        clearTimeout(this.#longPressTimeout);
        break;
    }
  }

  #handleTap(e) {
    this.dispatchEvent(new CustomEvent('tap', {
      bubbles: true,
      detail: { x: e.clientX, y: e.clientY }
    }));
  }

  #handleLongPress(e) {
    // Haptic feedback if available
    if (navigator.vibrate) navigator.vibrate(10);

    this.dispatchEvent(new CustomEvent('longpress', {
      bubbles: true,
      detail: { x: e.clientX, y: e.clientY }
    }));
  }
}
```

### Hover State Handling

iPadOS triggers `:hover` on first tap, then `:active` on second. Handle this:

```css
/* Default: no hover effects for touch */
@media (hover: none) {
  .button:hover {
    /* Reset hover styles for touch devices */
    background: var(--button-bg);
  }
}

/* Only apply hover for devices that support it */
@media (hover: hover) {
  .button:hover {
    background: var(--color-hover-overlay);
    transform: translateY(-1px);
  }
}

/* Active state works on both */
.button:active {
  background: var(--color-active-overlay);
  transform: scale(0.98);
}
```

---

## Layout Patterns for 12.9" Display

### Grid for Large Tablets

```css
/* Game board - uses full width */
.game-board {
  container-type: inline-size;
  display: grid;
  gap: var(--grid-gutter);
  padding: var(--space-m);
}

/* Landscape: 4 columns */
@container (inline-size >= 1024px) {
  .card-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

/* Portrait: 3 columns */
@container (inline-size >= 768px) and (inline-size < 1024px) {
  .card-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Small containers: 2 columns */
@container (inline-size < 768px) {
  .card-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
```

### Avoiding "Blown-Up Phone" Layouts

```css
/* DON'T: Single column on large screens */
.page-content {
  max-width: 100%; /* Content stretches uncomfortably */
}

/* DO: Constrain content width, use whitespace */
.page-content {
  max-width: var(--grid-max-width); /* 1240px */
  margin-inline: auto;
  padding-inline: var(--space-l);
}

/* DO: Multi-column layouts on large screens */
.main-layout {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr; /* Sidebar | Main | Aside */
  gap: var(--grid-gutter);
}
```

### Orientation Change Handling

```css
/* Landscape-specific adjustments */
@media (orientation: landscape) {
  .game-ui {
    flex-direction: row;

    .sidebar {
      width: 280px;
      flex-shrink: 0;
    }

    .main-content {
      flex: 1;
    }
  }
}

/* Portrait-specific adjustments */
@media (orientation: portrait) {
  .game-ui {
    flex-direction: column;

    .sidebar {
      width: 100%;
      height: auto;
    }

    .main-content {
      flex: 1;
    }
  }
}
```

### JavaScript Orientation Detection

```javascript
class OrientationAware extends HTMLElement {
  #mediaQuery = window.matchMedia('(orientation: landscape)');

  connectedCallback() {
    this.#mediaQuery.addEventListener('change', this);
    this.#updateOrientation();
  }

  disconnectedCallback() {
    this.#mediaQuery.removeEventListener('change', this);
  }

  handleEvent(e) {
    if (e.type === 'change') {
      this.#updateOrientation();
    }
  }

  #updateOrientation() {
    const isLandscape = this.#mediaQuery.matches;
    this.setAttribute('data-orientation', isLandscape ? 'landscape' : 'portrait');

    this.dispatchEvent(new CustomEvent('orientation-change', {
      bubbles: true,
      detail: { isLandscape }
    }));
  }
}
```

---

## Child-Friendly UX Patterns

### Design Principles for Children (Ages 3-8)

| Principle | Implementation |
|-----------|----------------|
| Large tap targets | Minimum 56pt (prefer 72pt+) |
| Clear visual feedback | Immediate bounce/glow on tap |
| Simple navigation | Max 2-3 choices visible |
| Forgiving interactions | Accept imprecise taps, allow undo |
| Consistent layout | Same button positions across screens |
| No time pressure | Avoid timers for young children |
| Positive reinforcement | Celebrate success, gentle error handling |

### Visual Feedback for Children

```javascript
// Immediate, exaggerated feedback
function childFriendlyTapFeedback(element) {
  // Instant scale down
  animate(element, {
    scale: 0.9,
    duration: 80,
    ease: 'linear'
  }).then(() => {
    // Bouncy return
    animate(element, {
      scale: [0.9, 1.15, 1],
      duration: 300,
      ease: 'outBack'
    });
  });
}

// Success celebration
function celebrateSuccess(element) {
  return animate(element, {
    scale: [1, 1.3, 1],
    rotate: [0, -8, 8, -4, 4, 0],
    duration: 500,
    ease: 'outElastic(1, 0.5)'
  });
}

// Gentle error shake (not scary)
function gentleErrorShake(element) {
  return animate(element, {
    x: [0, -4, 4, -2, 2, 0],
    duration: 300,
    ease: 'linear'
  });
}
```

### Progressive Disclosure

```html
<!-- Show only essential options initially -->
<nav class="game-nav" aria-label="Game navigation">
  <button class="nav-item nav-item--current" aria-current="page">
    <span class="icon" aria-hidden="true">play_arrow</span>
    <span class="label">Play</span>
  </button>

  <!-- Advanced options hidden until needed -->
  <button class="nav-item" hidden data-requires-progress="5">
    <span class="icon" aria-hidden="true">settings</span>
    <span class="label">Settings</span>
  </button>
</nav>
```

### Forgiving Touch Zones

```css
/* Extra-large interactive cards for children */
.word-card-child {
  min-width: 140px;
  min-height: 140px;
  padding: var(--space-l);

  /* Expanded hit area beyond visual bounds */
  position: relative;
}

.word-card-child::before {
  content: '';
  position: absolute;
  inset: calc(-1 * var(--space-m)); /* 27-30px expansion */
}

/* Wide spacing between cards to prevent mis-taps */
.card-grid-child {
  gap: var(--space-l); /* 36-40px */
}
```

### Audio Feedback (Optional)

```javascript
class AudioFeedback {
  #audioContext = null;
  #enabled = true;

  constructor() {
    // Initialize on first user interaction
    document.addEventListener('pointerdown', () => {
      if (!this.#audioContext) {
        this.#audioContext = new AudioContext();
      }
    }, { once: true });
  }

  playTap() {
    if (!this.#enabled || !this.#audioContext) return;
    this.#playTone(800, 50); // Short, high beep
  }

  playSuccess() {
    if (!this.#enabled || !this.#audioContext) return;
    this.#playMelody([523, 659, 784], 100); // C-E-G chord
  }

  playError() {
    if (!this.#enabled || !this.#audioContext) return;
    this.#playTone(200, 150); // Low, longer tone
  }

  #playTone(frequency, duration) {
    const oscillator = this.#audioContext.createOscillator();
    const gainNode = this.#audioContext.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(this.#audioContext.destination);

    oscillator.frequency.value = frequency;
    gainNode.gain.setValueAtTime(0.1, this.#audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, this.#audioContext.currentTime + duration / 1000);

    oscillator.start();
    oscillator.stop(this.#audioContext.currentTime + duration / 1000);
  }

  #playMelody(frequencies, noteDuration) {
    frequencies.forEach((freq, i) => {
      setTimeout(() => this.#playTone(freq, noteDuration), i * noteDuration);
    });
  }

  toggle(enabled) {
    this.#enabled = enabled;
  }
}
```

---

## Safari/WebKit Considerations

### Supported CSS Features (iPadOS 17+)

| Feature | Support | Notes |
|---------|---------|-------|
| Container Queries | Full | Use `cqi` units |
| `:has()` selector | Full | Use for complex states |
| Subgrid | Full | Use for nested grids |
| `view-transitions` | Partial | Same-document only |
| `field-sizing` | Yes | Auto-sizing textareas |
| `@layer` | Full | CSS cascade layers |
| `color-mix()` | Full | Dynamic color blending |
| Backdrop filter | Full | With `-webkit-` prefix |

### Safari-Specific CSS

```css
/* Backdrop blur - requires prefix */
.modal-backdrop {
  -webkit-backdrop-filter: blur(10px);
  backdrop-filter: blur(10px);
}

/* Prevent iOS font boosting */
body {
  -webkit-text-size-adjust: 100%;
  text-size-adjust: 100%;
}

/* Smooth scrolling with momentum */
.scrollable {
  -webkit-overflow-scrolling: touch;
  overflow-y: auto;
}

/* Hide scrollbar but keep functionality */
.scrollable::-webkit-scrollbar {
  display: none;
}
```

### Known Safari Limitations

| Issue | Workaround |
|-------|------------|
| No `popover` attribute | Use `<dialog>` or custom implementation |
| Limited Fullscreen API | Works in standalone PWA mode only |
| No Web MIDI | Use Web Audio API instead |
| IndexedDB storage limits | 1GB quota, request via Storage API |
| No `beforeinstallprompt` | Manual PWA install instructions |

### PWA Capabilities

```json
// manifest.json
{
  "name": "Fantasy Phonics",
  "short_name": "Phonics",
  "display": "standalone",
  "orientation": "any",
  "background_color": "#252119",
  "theme_color": "#252119",
  "icons": [
    { "src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ],
  "start_url": "/",
  "scope": "/"
}
```

---

## Performance Checklist

### Rendering Performance

- [ ] Use `transform` and `opacity` for animations (GPU accelerated)
- [ ] Apply `will-change` before animations, remove after
- [ ] Use `contain: layout` on fixed-size containers
- [ ] Avoid animating during scroll (use `scroll-behavior: smooth` instead)
- [ ] Batch DOM reads and writes (avoid layout thrashing)

### Touch Performance

- [ ] Use `touch-action: manipulation` to remove 300ms tap delay
- [ ] Apply `pointer-events: none` to elements during drag
- [ ] Use `pointerdown`/`pointermove`/`pointerup` (not touch events)
- [ ] Set `passive: true` on scroll/touch listeners when not preventing default

### Memory Management

- [ ] Clean up event listeners in `disconnectedCallback`
- [ ] Cancel animations when component unmounts
- [ ] Use `AbortController` for cancellable fetch requests
- [ ] Avoid creating objects in animation loops

### Asset Optimization

- [ ] Use `srcset` for images at 1x and 2x resolutions
- [ ] Lazy load images below the fold with `loading="lazy"`
- [ ] Preload critical fonts with `<link rel="preload">`
- [ ] Use WebP/AVIF images where supported

---

## Quick Reference

### Viewport & Safe Areas

```css
/* Essential meta tag */
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">

/* Safe area padding */
padding: env(safe-area-inset-top) env(safe-area-inset-right)
         env(safe-area-inset-bottom) env(safe-area-inset-left);
```

### Touch Targets

```css
/* Adults */ min-width: 44px; min-height: 44px;
/* Children */ min-width: 72px; min-height: 72px;
```

### Media Queries

```css
/* iPad Pro 12.9" specific */
@media (min-width: 1024px) and (max-width: 1366px) { }

/* Touch-only */
@media (hover: none) and (pointer: coarse) { }

/* Orientation */
@media (orientation: landscape) { }
```

### Animation Timing (120Hz)

```css
--duration-instant: 100ms;  /* Tap feedback */
--duration-quick: 150ms;    /* State changes */
--duration-normal: 200ms;   /* Transitions */
```

### Integration with Project Tokens

```css
/* Use Utopia space tokens for consistent sizing */
.touch-target-child {
  min-width: var(--space-2xl);   /* 72-80px */
  min-height: var(--space-2xl);
  padding: var(--space-m);       /* 27-30px */
  gap: var(--space-s);           /* 18-20px */
}

/* Use Utopia type tokens for readable text */
.game-label {
  font-size: var(--step-1);      /* 21.6-25px */
}
```

---

## Files

This skill references and integrates with:
- `css/styles/accessibility.css` - Touch target tokens, focus rings
- `css/styles/space.css` - Utopia spacing scale
- `css/styles/typography.css` - Utopia type scale
- `css/styles/transitions.css` - Animation timing tokens
