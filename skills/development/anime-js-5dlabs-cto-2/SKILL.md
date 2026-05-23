---
name: anime-js
description: Anime.js animation patterns for web interfaces including timelines, staggering, and motion design.
agents: [blaze]
triggers: [animation, motion, animate, anime, transition]
---

# Anime.js Animation Patterns

High-performance animations for web interfaces using Anime.js.

## Core Concepts

| Concept | Description |
|---------|-------------|
| Targets | CSS selectors, DOM elements, or JS objects |
| Properties | CSS, SVG, DOM, or object properties to animate |
| Timeline | Sequence and coordinate multiple animations |
| Staggering | Cascade animations across multiple targets |
| Easing | Control animation timing curves |

## Basic Animation

```typescript
import anime from 'animejs'

// Simple animation
anime({
  targets: '.element',
  translateX: 250,
  opacity: [0, 1],
  duration: 1000,
  easing: 'easeOutExpo'
})
```

## CSS Properties

```typescript
anime({
  targets: '.box',
  translateX: 250,
  translateY: 50,
  rotate: '1turn',
  scale: 1.5,
  opacity: 0.5,
  backgroundColor: '#FFF',
  borderRadius: ['0%', '50%'],
  duration: 2000
})
```

## SVG Animations

```typescript
// Line drawing
anime({
  targets: 'path',
  strokeDashoffset: [anime.setDashoffset, 0],
  easing: 'easeInOutSine',
  duration: 1500,
  delay: (el, i) => i * 250
})

// Morph path
anime({
  targets: 'path',
  d: [
    { value: 'M0 0 L100 0 L100 100 L0 100 Z' },
    { value: 'M50 0 L100 50 L50 100 L0 50 Z' }
  ],
  easing: 'easeInOutQuad',
  duration: 2000
})
```

## Timeline

```typescript
const tl = anime.timeline({
  easing: 'easeOutExpo',
  duration: 750
})

tl
  .add({ targets: '.header', translateY: [-100, 0], opacity: [0, 1] })
  .add({ targets: '.content', translateX: [-100, 0], opacity: [0, 1] }, '-=500')
  .add({ targets: '.footer', translateY: [100, 0], opacity: [0, 1] }, '-=500')
```

## Staggering

```typescript
// Basic stagger
anime({
  targets: '.grid-item',
  translateY: [100, 0],
  opacity: [0, 1],
  delay: anime.stagger(100)
})

// Grid stagger
anime({
  targets: '.grid-item',
  scale: [0, 1],
  delay: anime.stagger(50, { grid: [7, 5], from: 'center' })
})

// Stagger with easing
anime({
  targets: '.item',
  translateX: 350,
  delay: anime.stagger(100, { easing: 'easeOutQuad' })
})
```

## Easing Functions

| Category | Functions |
|----------|-----------|
| Built-in | `linear`, `easeInQuad`, `easeOutExpo`, etc. |
| Spring | `spring(mass, stiffness, damping, velocity)` |
| Steps | `steps(5)` |
| Custom | `cubicBezier(0.5, 0, 0.5, 1)` |

```typescript
anime({
  targets: '.element',
  translateX: 250,
  easing: 'spring(1, 80, 10, 0)'
})
```

## Keyframes

```typescript
anime({
  targets: '.element',
  keyframes: [
    { translateY: -40 },
    { translateX: 250 },
    { translateY: 40 },
    { translateX: 0 },
    { translateY: 0 }
  ],
  duration: 4000,
  easing: 'easeOutElastic(1, .8)'
})
```

## Callbacks

```typescript
anime({
  targets: '.element',
  translateX: 250,
  begin: (anim) => console.log('Started'),
  update: (anim) => console.log(`Progress: ${anim.progress}%`),
  complete: (anim) => console.log('Completed'),
  loopBegin: (anim) => console.log('Loop started'),
  loopComplete: (anim) => console.log('Loop completed'),
  changeBegin: (anim) => console.log('Change began'),
  changeComplete: (anim) => console.log('Change completed')
})
```

## Controls

```typescript
const animation = anime({
  targets: '.element',
  translateX: 250,
  autoplay: false
})

animation.play()
animation.pause()
animation.restart()
animation.reverse()
animation.seek(1000)  // Seek to 1000ms
```

## React Integration

```typescript
import { useEffect, useRef } from 'react'
import anime from 'animejs'

function AnimatedComponent() {
  const elementRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (elementRef.current) {
      anime({
        targets: elementRef.current,
        translateX: 250,
        opacity: [0, 1],
        duration: 1000
      })
    }
  }, [])

  return <div ref={elementRef}>Animated</div>
}
```

## Common Patterns

### Page Load Animation

```typescript
anime.timeline()
  .add({ targets: '.logo', scale: [0, 1], duration: 600 })
  .add({ targets: '.nav-item', translateY: [-20, 0], opacity: [0, 1], delay: anime.stagger(100) }, '-=400')
  .add({ targets: '.hero', translateY: [50, 0], opacity: [0, 1] }, '-=200')
```

### Hover Effect

```typescript
element.addEventListener('mouseenter', () => {
  anime({ targets: element, scale: 1.1, duration: 300 })
})

element.addEventListener('mouseleave', () => {
  anime({ targets: element, scale: 1, duration: 300 })
})
```

### Scroll Reveal

```typescript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      anime({
        targets: entry.target,
        translateY: [50, 0],
        opacity: [0, 1],
        duration: 800
      })
      observer.unobserve(entry.target)
    }
  })
})

document.querySelectorAll('.reveal').forEach(el => observer.observe(el))
```

## Performance Tips

- Prefer transform and opacity (GPU accelerated)
- Avoid animating layout properties (width, height, top, left)
- Use `will-change` sparingly for complex animations
- Batch animations with timeline
- Clean up animations on component unmount
