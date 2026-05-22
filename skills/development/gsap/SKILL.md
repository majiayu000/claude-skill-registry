---
name: gsap
description: Use when implementing web animations, timeline sequencing, scroll-triggered animations, SVG animations, layout transitions, or using GSAP, ScrollTrigger, ScrollSmoother, SplitText, Flip, DrawSVG, MorphSVG, MotionPath, or @gsap/react useGSAP hook.
---

# GSAP Best Practices

Professional-grade JavaScript animation library for the modern web. Provides high-performance tweening with powerful sequencing, scroll-based animations, and extensive plugin ecosystem.

## Installation

```bash
# Core library
npm install gsap

# React hook
npm install @gsap/react

# Register plugins (do once at app entry)
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
gsap.registerPlugin(ScrollTrigger)
```

## Quick Start

```javascript
import gsap from 'gsap'

// Basic tween
gsap.to('.box', { x: 200, duration: 1 })

// From animation
gsap.from('.box', { opacity: 0, y: 50, duration: 0.5 })

// Timeline sequence
const tl = gsap.timeline()
tl.to('.box1', { x: 100 })
  .to('.box2', { x: 100 }, '-=0.5')  // overlap by 0.5s
  .to('.box3', { x: 100 }, '<')       // same start as previous
```

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Tween** | Single animation that changes properties over time |
| **Timeline** | Container for sequencing tweens with precise control |
| **Ease** | Controls animation velocity curve (default: `power1.out`) |
| **ScrollTrigger** | Links animations to scroll position |
| **Plugin** | Extends GSAP with specialized capabilities |

## Reference Index

| Reference | Use When |
|-----------|----------|
| `references/00-cheatsheet.md` | Quick reference, common operations at a glance |
| `references/01-core.md` | Basic tweens, special properties, callbacks, quickTo, ticker |
| `references/02-easing.md` | Easing functions, custom eases |
| `references/03-timeline.md` | Sequencing, positioning, labels, nesting |
| `references/04-stagger.md` | Staggered animations, grid distributions |
| `references/05-utilities.md` | Helper functions (toArray, clamp, interpolate) |
| `references/06-scrolltrigger.md` | Scroll-based animations, pin, scrub, snap |
| `references/07-scrollsmoother.md` | Smooth scrolling, parallax effects |
| `references/08-splittext.md` | Text splitting and animation |
| `references/09-svg-plugins.md` | DrawSVG, MorphSVG, MotionPath |
| `references/10-flip.md` | Layout animations (FLIP technique) |
| `references/11-react.md` | useGSAP hook, cleanup, React patterns |
| `references/12-observer-draggable.md` | Gesture detection, draggable elements |
| `references/13-text-plugins.md` | TextPlugin, ScrambleTextPlugin |

## Common Patterns

### Fade In on Load

```javascript
gsap.from('.hero', {
  opacity: 0,
  y: 30,
  duration: 1,
  ease: 'power2.out'
})
```

### Staggered List Animation

```javascript
gsap.from('.list-item', {
  opacity: 0,
  y: 20,
  stagger: 0.1,
  duration: 0.5
})
```

### Scroll-Triggered Animation

```javascript
gsap.registerPlugin(ScrollTrigger)

gsap.to('.box', {
  x: 500,
  scrollTrigger: {
    trigger: '.box',
    start: 'top 80%',
    end: 'top 20%',
    scrub: true
  }
})
```

### Timeline with Controls

```javascript
const tl = gsap.timeline({ paused: true })
tl.to('.modal', { opacity: 1, scale: 1, duration: 0.3 })
  .from('.modal-content', { y: 20, opacity: 0 }, '-=0.1')

// Control playback
tl.play()
tl.reverse()
tl.progress(0.5)
```

## Critical Mistakes to Avoid

### 1. Missing Plugin Registration

```javascript
// ❌ Plugin won't work
import { ScrollTrigger } from 'gsap/ScrollTrigger'
gsap.to('.box', { scrollTrigger: { ... } })

// ✅ Register plugins first
gsap.registerPlugin(ScrollTrigger)
gsap.to('.box', { scrollTrigger: { ... } })
```

### 2. React Cleanup Issues

```javascript
// ❌ Memory leaks, zombie animations
useEffect(() => {
  gsap.to('.box', { x: 100 })
}, [])

// ✅ Use useGSAP hook for automatic cleanup
import { useGSAP } from '@gsap/react'
useGSAP(() => {
  gsap.to('.box', { x: 100 })
}, { scope: containerRef })
```

### 3. Conflicting Tweens

```javascript
// ❌ Two tweens fighting for same property
gsap.to('.box', { x: 100, duration: 2 })
gsap.to('.box', { x: 200, duration: 1 })

// ✅ Use overwrite or kill previous
gsap.to('.box', { x: 100, duration: 2, overwrite: true })
// or
gsap.killTweensOf('.box')
gsap.to('.box', { x: 200, duration: 1 })
```

### 4. ScrollTrigger Not Refreshing

```javascript
// ❌ Layout changes but ScrollTrigger uses old positions
dynamicallyAddContent()

// ✅ Refresh after DOM/layout changes
dynamicallyAddContent()
ScrollTrigger.refresh()
```

### 5. Animating Non-Existent Elements

```javascript
// ❌ Element not in DOM yet
gsap.to('.dynamic-element', { x: 100 })

// ✅ Wait for element or use immediateRender: false
gsap.to('.dynamic-element', {
  x: 100,
  immediateRender: false,
  scrollTrigger: { ... }
})
```

### 6. Wrong from() Behavior

```javascript
// ❌ from() renders immediately, causing flash
gsap.from('.box', { opacity: 0 })

// ✅ Set initial state in CSS or use fromTo
// CSS: .box { opacity: 0; }
gsap.to('.box', { opacity: 1 })

// or use fromTo for explicit control
gsap.fromTo('.box', { opacity: 0 }, { opacity: 1 })
```

### 7. Forgetting Selector Scope

```javascript
// ❌ Affects ALL .box elements on page
gsap.to('.box', { x: 100 })

// ✅ Scope to container
gsap.to('.box', { x: 100 }, { scope: containerRef })
// or use gsap.utils.selector
const q = gsap.utils.selector(container)
gsap.to(q('.box'), { x: 100 })
```

## Quick Reference

| Task | Solution |
|------|----------|
| Animate to values | `gsap.to(target, { props })` |
| Animate from values | `gsap.from(target, { props })` |
| Animate both directions | `gsap.fromTo(target, { from }, { to })` |
| Set instantly | `gsap.set(target, { props })` |
| Create timeline | `gsap.timeline({ options })` |
| Kill all tweens | `gsap.killTweensOf(target)` |
| Global defaults | `gsap.defaults({ ease, duration })` |
| Register plugin | `gsap.registerPlugin(Plugin)` |
| Get by ID | `gsap.getById('myTween')` |
| Match media | `gsap.matchMedia()` |

## Plugin Availability

| Plugin | License | Description |
|--------|---------|-------------|
| ScrollTrigger | Free | Scroll-based animations |
| Observer | Free | Gesture/scroll detection |
| Draggable | Free | Drag interactions |
| Flip | Free | Layout animations |
| TextPlugin | Free | Text content animation |
| ScrollSmoother | Club | Smooth scrolling |
| SplitText | Club | Text splitting |
| DrawSVG | Club | SVG stroke animation |
| MorphSVG | Club | SVG morphing |
| MotionPath | Club | Path-based motion |
| ScrollTo | Free | Scroll to position |
