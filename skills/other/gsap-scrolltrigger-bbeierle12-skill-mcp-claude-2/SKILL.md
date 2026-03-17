---
name: gsap-scrolltrigger
description: Scroll-based animations using GSAP ScrollTrigger plugin including pinning, scrubbing, snap points, and parallax effects. Use when creating scroll-driven animations, sticky sections, progress indicators, or parallax scrolling experiences.
---

# GSAP ScrollTrigger

Scroll-driven animations and interactions.

## Quick Start

```bash
npm install gsap
```

```javascript
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

gsap.to('.box', {
  x: 500,
  scrollTrigger: {
    trigger: '.box',
    start: 'top center',
    end: 'bottom center',
    scrub: true
  }
});
```

## Core Concepts

### Basic ScrollTrigger

```javascript
gsap.to('.element', {
  x: 200,
  scrollTrigger: {
    trigger: '.element',  // Element that triggers the animation
    start: 'top center',  // When trigger hits viewport center
    end: 'bottom center', // When trigger leaves viewport center
    toggleActions: 'play pause resume reset'
  }
});
```

### Start/End Positions

```javascript
// Format: "trigger-position viewport-position"
start: 'top center'      // Trigger's top hits viewport center
start: 'top 80%'         // Trigger's top hits 80% down viewport
start: 'center center'   // Trigger's center hits viewport center
start: 'bottom top'      // Trigger's bottom hits viewport top
start: 'top top+=100'    // Trigger's top hits 100px below viewport top
```

### Position Reference

| Value | Description |
|-------|-------------|
| `top` | Top edge |
| `center` | Center |
| `bottom` | Bottom edge |
| `80%` | 80% from top |
| `+=100` | Plus 100 pixels |
| `-=50` | Minus 50 pixels |

## Scrub Animations

### Basic Scrub

```javascript
// Animation progress tied to scroll position
gsap.to('.progress-bar', {
  scaleX: 1,
  scrollTrigger: {
    trigger: '.content',
    start: 'top top',
    end: 'bottom bottom',
    scrub: true  // Directly linked to scroll
  }
});
```

### Smooth Scrub

```javascript
gsap.to('.element', {
  x: 500,
  scrollTrigger: {
    trigger: '.section',
    scrub: 1,    // 1 second smoothing
    // scrub: 0.5  // 0.5 second smoothing
    // scrub: 2    // 2 second smoothing (laggy feel)
  }
});
```

### Scrub with Timeline

```javascript
const tl = gsap.timeline({
  scrollTrigger: {
    trigger: '.container',
    start: 'top top',
    end: '+=3000',  // Scroll distance
    scrub: 1,
    pin: true
  }
});

tl.to('.step1', { opacity: 1 })
  .to('.step2', { opacity: 1 })
  .to('.step3', { opacity: 1 });
```

## Pinning

### Basic Pin

```javascript
ScrollTrigger.create({
  trigger: '.panel',
  start: 'top top',
  end: '+=500',      // Pin for 500px of scroll
  pin: true
});
```

### Pin with Animation

```javascript
gsap.to('.content', {
  x: '-200%',
  ease: 'none',
  scrollTrigger: {
    trigger: '.horizontal-section',
    start: 'top top',
    end: () => '+=' + document.querySelector('.horizontal-section').offsetWidth,
    pin: true,
    scrub: 1
  }
});
```

### Pin Spacing

```javascript
ScrollTrigger.create({
  trigger: '.section',
  pin: true,
  pinSpacing: true,   // Default: adds space for pinned duration
  // pinSpacing: false  // No extra space (content overlaps)
  // pinSpacing: '500px' // Custom spacing
});
```

## Toggle Actions

### Action Syntax

```javascript
// Format: "onEnter onLeave onEnterBack onLeaveBack"
toggleActions: 'play pause resume reset'

// Common combinations:
toggleActions: 'play none none none'     // Play once
toggleActions: 'play reverse play reverse' // Toggle direction
toggleActions: 'restart none none none'  // Restart each time
toggleActions: 'play complete reverse reset'
```

### Action Values

| Action | Effect |
|--------|--------|
| `play` | Play forward |
| `pause` | Pause |
| `resume` | Resume from paused |
| `reverse` | Play backward |
| `restart` | Restart from beginning |
| `reset` | Reset to start (no animation) |
| `complete` | Jump to end |
| `none` | Do nothing |

## Snap Points

### Basic Snap

```javascript
ScrollTrigger.create({
  trigger: '.sections',
  start: 'top top',
  end: 'bottom bottom',
  snap: 1 / 4  // Snap to quarters
});
```

### Snap to Labels

```javascript
const tl = gsap.timeline({
  scrollTrigger: {
    trigger: '.container',
    scrub: 1,
    snap: {
      snapTo: 'labels',
      duration: 0.5,
      ease: 'power2.inOut'
    }
  }
});

tl.addLabel('intro')
  .to('.a', { opacity: 1 })
  .addLabel('middle')
  .to('.b', { opacity: 1 })
  .addLabel('end');
```

### Snap Configuration

```javascript
snap: {
  snapTo: [0, 0.25, 0.5, 0.75, 1],  // Snap to specific points
  duration: { min: 0.2, max: 0.6 }, // Snap duration range
  delay: 0,                          // Delay before snap
  ease: 'power1.inOut',             // Snap easing
  directional: true                  // Snap in scroll direction
}
```

## Callbacks

### ScrollTrigger Callbacks

```javascript
ScrollTrigger.create({
  trigger: '.section',
  onEnter: () => console.log('Entered'),
  onLeave: () => console.log('Left'),
  onEnterBack: () => console.log('Entered from bottom'),
  onLeaveBack: () => console.log('Left going up'),
  onUpdate: (self) => console.log('Progress:', self.progress),
  onToggle: (self) => console.log('Active:', self.isActive),
  onRefresh: () => console.log('Refreshed')
});
```

### Progress-Based Updates

```javascript
ScrollTrigger.create({
  trigger: '.section',
  start: 'top bottom',
  end: 'bottom top',
  onUpdate: (self) => {
    // self.progress: 0 to 1
    // self.direction: 1 (down) or -1 (up)
    // self.velocity: scroll speed
    updateElement(self.progress);
  }
});
```

## Parallax Effects

### Basic Parallax

```javascript
// Background moves slower than scroll
gsap.to('.background', {
  yPercent: -50,
  ease: 'none',
  scrollTrigger: {
    trigger: '.section',
    scrub: true
  }
});

// Foreground moves faster
gsap.to('.foreground', {
  yPercent: 50,
  ease: 'none',
  scrollTrigger: {
    trigger: '.section',
    scrub: true
  }
});
```

### Multi-Layer Parallax

```javascript
const layers = [
  { selector: '.layer-1', speed: -20 },
  { selector: '.layer-2', speed: -40 },
  { selector: '.layer-3', speed: -60 },
  { selector: '.layer-4', speed: -80 }
];

layers.forEach(layer => {
  gsap.to(layer.selector, {
    yPercent: layer.speed,
    ease: 'none',
    scrollTrigger: {
      trigger: '.parallax-section',
      start: 'top bottom',
      end: 'bottom top',
      scrub: true
    }
  });
});
```

## Horizontal Scrolling

### Horizontal Section

```javascript
const sections = gsap.utils.toArray('.panel');

gsap.to(sections, {
  xPercent: -100 * (sections.length - 1),
  ease: 'none',
  scrollTrigger: {
    trigger: '.horizontal-container',
    pin: true,
    scrub: 1,
    snap: 1 / (sections.length - 1),
    end: () => '+=' + document.querySelector('.horizontal-container').offsetWidth
  }
});
```

## Markers (Development)

```javascript
ScrollTrigger.create({
  trigger: '.section',
  start: 'top center',
  end: 'bottom center',
  markers: true,  // Show visual markers
  // markers: { startColor: 'green', endColor: 'red', fontSize: '12px' }
});
```

## Batch Animations

### Stagger on Scroll

```javascript
ScrollTrigger.batch('.card', {
  onEnter: (elements) => {
    gsap.from(elements, {
      opacity: 0,
      y: 50,
      stagger: 0.1,
      duration: 0.5
    });
  },
  start: 'top 85%'
});
```

### Batch Configuration

```javascript
ScrollTrigger.batch('.item', {
  interval: 0.1,  // Time between batches
  batchMax: 3,    // Max items per batch
  onEnter: batch => gsap.to(batch, { opacity: 1, y: 0, stagger: 0.1 }),
  onLeave: batch => gsap.to(batch, { opacity: 0, y: 20 }),
  onEnterBack: batch => gsap.to(batch, { opacity: 1, y: 0 }),
  onLeaveBack: batch => gsap.to(batch, { opacity: 0, y: -20 })
});
```

## Common Patterns

### Reveal on Scroll

```javascript
gsap.utils.toArray('.reveal').forEach(elem => {
  gsap.from(elem, {
    opacity: 0,
    y: 50,
    duration: 0.8,
    scrollTrigger: {
      trigger: elem,
      start: 'top 80%',
      toggleActions: 'play none none none'
    }
  });
});
```

### Progress Indicator

```javascript
gsap.to('.progress-bar', {
  scaleX: 1,
  transformOrigin: 'left center',
  ease: 'none',
  scrollTrigger: {
    trigger: 'body',
    start: 'top top',
    end: 'bottom bottom',
    scrub: 0.3
  }
});
```

### Sticky Header Transform

```javascript
ScrollTrigger.create({
  start: 'top -80',
  onUpdate: (self) => {
    if (self.direction === 1) {
      gsap.to('.header', { y: -80, duration: 0.3 });
    } else {
      gsap.to('.header', { y: 0, duration: 0.3 });
    }
  }
});
```

## Temporal Collapse Patterns

### Countdown Scroll Reveal

```javascript
// Reveal countdown sections as user scrolls
const sections = ['days', 'hours', 'minutes', 'seconds'];

sections.forEach((section, i) => {
  gsap.from(`.countdown-${section}`, {
    opacity: 0,
    scale: 0.8,
    y: 50,
    duration: 0.8,
    ease: 'power3.out',
    scrollTrigger: {
      trigger: `.countdown-${section}`,
      start: 'top 80%',
      toggleActions: 'play none none none'
    }
  });
});
```

### Scroll-Based Time Dilation Effect

```javascript
gsap.timeline({
  scrollTrigger: {
    trigger: '.time-section',
    start: 'top center',
    end: 'bottom center',
    scrub: 1
  }
})
.to('.time-digit', {
  textShadow: '0 0 50px #00F5FF, 0 0 100px #00F5FF',
  scale: 1.1
})
.to('.particles', {
  opacity: 1,
  filter: 'blur(0px)'
}, '<');
```

## Performance Tips

```javascript
// Disable on mobile if needed
ScrollTrigger.matchMedia({
  '(min-width: 768px)': function() {
    // Desktop animations
  },
  '(max-width: 767px)': function() {
    // Simpler mobile animations
  }
});

// Refresh on resize
ScrollTrigger.refresh();

// Kill all ScrollTriggers
ScrollTrigger.killAll();

// Kill specific trigger
const st = ScrollTrigger.create({ ... });
st.kill();
```

## Reference

- See `gsap-fundamentals` for animation basics
- See `gsap-sequencing` for timeline composition
- See `gsap-react` for React integration with ScrollTrigger
