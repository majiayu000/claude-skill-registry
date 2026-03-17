---
name: gsap-sequencing
description: Complex GSAP timelines including labels, callbacks, nested timelines, and position parameters. Use when orchestrating multi-step animations, building animation sequences, or creating coordinated motion. Essential for cinematic animations and complex UI choreography.
---

# GSAP Sequencing

Complex timelines and animation orchestration.

## Quick Start

```javascript
import gsap from 'gsap';

const tl = gsap.timeline();

tl.to('.box1', { x: 100, duration: 0.5 })
  .to('.box2', { y: 50, duration: 0.5 })
  .to('.box3', { rotation: 360, duration: 0.5 });
```

## Timeline Basics

### Creating Timelines

```javascript
// Basic timeline
const tl = gsap.timeline();

// Timeline with defaults
const tl = gsap.timeline({
  defaults: {
    duration: 0.5,
    ease: 'power2.out'
  }
});

// Paused timeline (manual control)
const tl = gsap.timeline({ paused: true });
```

### Sequential Animations

```javascript
const tl = gsap.timeline();

// Each animation starts after the previous one ends
tl.to('.header', { y: 0, opacity: 1, duration: 0.5 })
  .to('.content', { y: 0, opacity: 1, duration: 0.5 })
  .to('.footer', { y: 0, opacity: 1, duration: 0.5 });
```

## Position Parameters

### Absolute Positioning

```javascript
const tl = gsap.timeline();

tl.to('.a', { x: 100 })
  .to('.b', { x: 100 }, 0)      // Start at 0 seconds (absolute)
  .to('.c', { x: 100 }, 0.5)    // Start at 0.5 seconds
  .to('.d', { x: 100 }, 2);     // Start at 2 seconds
```

### Relative Positioning

```javascript
const tl = gsap.timeline();

tl.to('.a', { x: 100, duration: 1 })
  .to('.b', { x: 100 }, '-=0.5')   // Start 0.5s before previous ends
  .to('.c', { x: 100 }, '+=0.5')   // Start 0.5s after previous ends
  .to('.d', { x: 100 }, '<')       // Start when previous starts
  .to('.e', { x: 100 }, '>')       // Start when previous ends (default)
  .to('.f', { x: 100 }, '<0.2')    // Start 0.2s after previous starts
  .to('.g', { x: 100 }, '>-0.2');  // Start 0.2s before previous ends
```

### Position Parameter Cheat Sheet

| Parameter | Meaning |
|-----------|---------|
| `0` | At 0 seconds (absolute) |
| `2` | At 2 seconds (absolute) |
| `'+=0.5'` | 0.5s after previous end |
| `'-=0.5'` | 0.5s before previous end |
| `'<'` | When previous starts |
| `'>'` | When previous ends |
| `'<0.3'` | 0.3s after previous starts |
| `'>-0.3'` | 0.3s before previous ends |
| `'myLabel'` | At label position |
| `'myLabel+=0.5'` | 0.5s after label |

## Labels

### Adding Labels

```javascript
const tl = gsap.timeline();

tl.add('intro')
  .to('.title', { opacity: 1 })
  .to('.subtitle', { opacity: 1 })
  .add('content')
  .to('.paragraph', { opacity: 1 })
  .to('.image', { scale: 1 })
  .add('outro')
  .to('.cta', { y: 0 });

// Jump to label
tl.seek('content');
tl.play('outro');
```

### Using Labels for Position

```javascript
const tl = gsap.timeline();

tl.addLabel('start')
  .to('.a', { x: 100 }, 'start')
  .to('.b', { x: 100 }, 'start')      // Same time as 'a'
  .to('.c', { x: 100 }, 'start+=0.2') // 0.2s after start label
  .addLabel('middle')
  .to('.d', { x: 100 }, 'middle')
  .to('.e', { x: 100 }, 'middle-=0.1');
```

## Nested Timelines

### Basic Nesting

```javascript
// Child timeline
function createIntro() {
  const tl = gsap.timeline();
  tl.from('.logo', { scale: 0, duration: 0.5 })
    .from('.tagline', { opacity: 0, y: 20 });
  return tl;
}

// Parent timeline
const master = gsap.timeline();
master.add(createIntro())
      .add(createContent())
      .add(createOutro());
```

### Nested Timeline Positioning

```javascript
const intro = gsap.timeline();
intro.to('.a', { x: 100 })
     .to('.b', { y: 100 });

const main = gsap.timeline();
main.to('.header', { opacity: 1 })
    .add(intro, '-=0.3')  // Overlap intro with header
    .to('.footer', { opacity: 1 });
```

### Modular Animation Functions

```javascript
// Reusable animation modules
const animations = {
  fadeIn: (target, duration = 0.5) => {
    return gsap.timeline()
      .from(target, { opacity: 0, y: 20, duration });
  },

  staggerIn: (targets, stagger = 0.1) => {
    return gsap.timeline()
      .from(targets, { opacity: 0, y: 30, stagger });
  },

  scaleIn: (target) => {
    return gsap.timeline()
      .from(target, { scale: 0, ease: 'back.out(1.7)' });
  }
};

// Compose master timeline
const master = gsap.timeline()
  .add(animations.fadeIn('.hero'))
  .add(animations.staggerIn('.card'), '-=0.2')
  .add(animations.scaleIn('.cta'));
```

## Timeline Callbacks

### Lifecycle Callbacks

```javascript
const tl = gsap.timeline({
  onStart: () => console.log('Timeline started'),
  onUpdate: () => console.log('Frame'),
  onComplete: () => console.log('Timeline complete'),
  onRepeat: () => console.log('Timeline repeated'),
  onReverseComplete: () => console.log('Reverse complete')
});
```

### Adding Callbacks Inline

```javascript
const tl = gsap.timeline();

tl.to('.element', { x: 100 })
  .call(() => console.log('After first animation'))
  .to('.element', { y: 100 })
  .call(updateState, ['param1', 'param2'], 'labelName');
```

### Callback with Parameters

```javascript
function logProgress(label) {
  console.log(`Reached: ${label}`);
}

const tl = gsap.timeline();
tl.to('.a', { x: 100 })
  .call(logProgress, ['step1'])
  .to('.b', { x: 100 })
  .call(logProgress, ['step2']);
```

## Timeline Control

### Playback Methods

```javascript
const tl = gsap.timeline({ paused: true });

// Build timeline...

// Control
tl.play();
tl.pause();
tl.resume();
tl.reverse();
tl.restart();

// Seeking
tl.seek(2);           // Jump to 2 seconds
tl.seek('labelName'); // Jump to label
tl.progress(0.5);     // Jump to 50%

// Speed
tl.timeScale(2);      // 2x speed
tl.timeScale(0.5);    // Half speed

// Direction
tl.reversed(true);    // Play backwards
tl.reversed(false);   // Play forwards
```

### Repeat and Yoyo

```javascript
const tl = gsap.timeline({
  repeat: 2,          // Repeat twice (3 total plays)
  repeatDelay: 0.5,   // Pause between repeats
  yoyo: true          // Reverse on alternate repeats
});

// Infinite loop
const tl = gsap.timeline({ repeat: -1 });
```

## Advanced Patterns

### Staggered Timeline Entries

```javascript
const tl = gsap.timeline();

// Add multiple at once with stagger
tl.to('.card', {
  y: 0,
  opacity: 1,
  stagger: {
    each: 0.1,
    from: 'start'
  }
}, 'cards');
```

### Timeline Scrubbing

```javascript
const tl = gsap.timeline({ paused: true });
tl.to('.progress', { scaleX: 1, duration: 1 });

// Scrub based on input
slider.addEventListener('input', (e) => {
  tl.progress(e.target.value / 100);
});
```

### Conditional Branches

```javascript
function createTimeline(options) {
  const tl = gsap.timeline();

  tl.to('.intro', { opacity: 1 });

  if (options.showDetails) {
    tl.to('.details', { height: 'auto', opacity: 1 });
  }

  if (options.animate3D) {
    tl.to('.model', { rotationY: 360 });
  }

  tl.to('.outro', { opacity: 1 });

  return tl;
}
```

## Complex Sequence Example

### Page Transition

```javascript
function pageTransition(currentPage, nextPage) {
  const tl = gsap.timeline();

  // Exit current page
  tl.to(currentPage, {
    opacity: 0,
    x: -50,
    duration: 0.3,
    ease: 'power2.in'
  })

  // Transition overlay
  .to('.overlay', {
    scaleY: 1,
    transformOrigin: 'bottom',
    duration: 0.4,
    ease: 'power2.inOut'
  }, '-=0.1')

  // Swap content (instant)
  .set(currentPage, { display: 'none' })
  .set(nextPage, { display: 'block', opacity: 0, x: 50 })

  // Hide overlay
  .to('.overlay', {
    scaleY: 0,
    transformOrigin: 'top',
    duration: 0.4,
    ease: 'power2.inOut'
  })

  // Enter next page
  .to(nextPage, {
    opacity: 1,
    x: 0,
    duration: 0.3,
    ease: 'power2.out'
  }, '-=0.2');

  return tl;
}
```

### Orchestrated UI Reveal

```javascript
function revealDashboard() {
  const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });

  tl.addLabel('start')

    // Header slides down
    .from('.header', { y: -100, opacity: 0, duration: 0.6 }, 'start')

    // Sidebar slides in
    .from('.sidebar', { x: -100, opacity: 0, duration: 0.6 }, 'start+=0.1')

    // Cards stagger in
    .from('.card', {
      y: 50,
      opacity: 0,
      duration: 0.5,
      stagger: 0.1
    }, 'start+=0.2')

    // Charts animate
    .from('.chart-bar', {
      scaleY: 0,
      transformOrigin: 'bottom',
      duration: 0.4,
      stagger: 0.05
    }, 'start+=0.4')

    // Final CTA pops
    .from('.cta-button', {
      scale: 0,
      ease: 'back.out(1.7)',
      duration: 0.4
    }, '-=0.2');

  return tl;
}
```

## Temporal Collapse Sequences

### Countdown Digit Change

```javascript
function digitChangeSequence(digitElement, oldValue, newValue) {
  const tl = gsap.timeline();

  tl.to(digitElement, {
    rotationX: -90,
    opacity: 0,
    textShadow: '0 0 0px #00F5FF',
    duration: 0.25,
    ease: 'power2.in'
  })
  .call(() => { digitElement.textContent = newValue; })
  .fromTo(digitElement,
    { rotationX: 90, opacity: 0 },
    {
      rotationX: 0,
      opacity: 1,
      textShadow: '0 0 30px #00F5FF',
      duration: 0.25,
      ease: 'power2.out'
    }
  )
  .to(digitElement, {
    textShadow: '0 0 10px #00F5FF',
    duration: 0.3
  });

  return tl;
}
```

### Final Countdown Sequence

```javascript
function createFinalCountdown() {
  const master = gsap.timeline({ paused: true });

  // Build intensity over last 10 seconds
  for (let i = 10; i >= 0; i--) {
    const intensity = (10 - i) / 10;

    master.addLabel(`second-${i}`)
      .to('.countdown', {
        scale: 1 + intensity * 0.2,
        textShadow: `0 0 ${20 + intensity * 40}px #00F5FF`,
        duration: 0.5
      }, `second-${i}`)
      .to('.background', {
        filter: `brightness(${1 + intensity * 0.5})`,
        duration: 0.5
      }, `second-${i}`);
  }

  // Zero moment explosion
  master.addLabel('zero')
    .to('.countdown', {
      scale: 3,
      opacity: 0,
      duration: 0.5,
      ease: 'power4.out'
    }, 'zero')
    .to('.celebration', {
      opacity: 1,
      scale: 1,
      duration: 0.8,
      ease: 'back.out(1.7)'
    }, 'zero+=0.3');

  return master;
}
```

## Debugging Timelines

```javascript
// Slow down for inspection
tl.timeScale(0.25);

// Log timeline duration
console.log('Duration:', tl.duration());

// Log all tweens
tl.getChildren().forEach((child, i) => {
  console.log(i, child.startTime(), child.duration());
});

// GSDevTools (premium plugin)
GSDevTools.create({ animation: tl });
```

## Reference

- See `gsap-fundamentals` for tween basics and easing
- See `gsap-react` for React integration
- See `gsap-scrolltrigger` for scroll-driven timelines
