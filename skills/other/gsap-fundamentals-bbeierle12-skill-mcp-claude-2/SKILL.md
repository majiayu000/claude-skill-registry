---
name: gsap-fundamentals
description: Core GSAP animation concepts including tweens, timelines, easing functions, and animation properties. Use when implementing basic animations, transitions, or learning GSAP foundations. Essential starting point for any GSAP-based animation work.
---

# GSAP Fundamentals

Core animation concepts with GreenSock Animation Platform.

## Quick Start

```bash
npm install gsap
```

```javascript
import gsap from 'gsap';

// Basic tween
gsap.to('.box', {
  x: 200,
  duration: 1,
  ease: 'power2.out'
});
```

## Core Concepts

### Tween Types

| Method | Description | Use Case |
|--------|-------------|----------|
| `gsap.to()` | Animate from current → target | Most common |
| `gsap.from()` | Animate from target → current | Entrance animations |
| `gsap.fromTo()` | Animate from defined start → end | Full control |
| `gsap.set()` | Instantly set properties | Initial state |

### Basic Tweens

```javascript
// To: current state → target
gsap.to('.element', {
  x: 100,
  y: 50,
  rotation: 360,
  duration: 1
});

// From: target → current state
gsap.from('.element', {
  opacity: 0,
  y: -50,
  duration: 0.5
});

// FromTo: explicit start and end
gsap.fromTo('.element',
  { opacity: 0, scale: 0.5 },  // from
  { opacity: 1, scale: 1, duration: 1 }  // to
);

// Set: instant property change
gsap.set('.element', { visibility: 'visible', opacity: 0 });
```

## Animation Properties

### Transform Properties

```javascript
gsap.to('.element', {
  // Position
  x: 100,           // translateX in pixels
  y: 50,            // translateY in pixels
  xPercent: 50,     // translateX as percentage of element width
  yPercent: -100,   // translateY as percentage of element height

  // Rotation
  rotation: 360,    // 2D rotation in degrees
  rotationX: 45,    // 3D rotation around X axis
  rotationY: 45,    // 3D rotation around Y axis

  // Scale
  scale: 1.5,       // Uniform scale
  scaleX: 2,        // Horizontal scale
  scaleY: 0.5,      // Vertical scale

  // Skew
  skewX: 20,        // Horizontal skew in degrees
  skewY: 10,        // Vertical skew in degrees

  // Transform origin
  transformOrigin: 'center center',
  transformPerspective: 500,

  duration: 1
});
```

### CSS Properties

```javascript
gsap.to('.element', {
  // Colors
  color: '#00F5FF',
  backgroundColor: '#FF00FF',
  borderColor: 'rgba(255, 215, 0, 0.5)',

  // Dimensions
  width: 200,
  height: '50%',
  padding: 20,
  margin: '10px 20px',

  // Display
  opacity: 0.8,
  visibility: 'visible',
  display: 'block',

  // Border
  borderRadius: '50%',
  borderWidth: 2,

  // Shadow
  boxShadow: '0 0 20px rgba(0, 245, 255, 0.5)',

  duration: 1
});
```

### SVG Properties

```javascript
gsap.to('svg path', {
  // Path morphing (requires MorphSVGPlugin)
  morphSVG: '#targetPath',

  // Draw SVG
  strokeDashoffset: 0,
  drawSVG: '100%',

  // SVG attributes
  attr: {
    cx: 100,
    cy: 100,
    r: 50,
    fill: '#00F5FF'
  },

  duration: 2
});
```

## Timing Controls

### Duration and Delay

```javascript
gsap.to('.element', {
  x: 100,
  duration: 1,      // Animation length in seconds
  delay: 0.5,       // Wait before starting
  repeat: 3,        // Repeat 3 times (4 total plays)
  repeatDelay: 0.2, // Pause between repeats
  yoyo: true        // Reverse on alternate repeats
});
```

### Infinite Repeat

```javascript
gsap.to('.spinner', {
  rotation: 360,
  duration: 1,
  repeat: -1,       // Infinite repeat
  ease: 'none'      // Linear for constant speed
});
```

### Stagger

```javascript
// Animate multiple elements with offset timing
gsap.to('.card', {
  y: 0,
  opacity: 1,
  duration: 0.5,
  stagger: 0.1      // 0.1s delay between each element
});

// Advanced stagger
gsap.to('.grid-item', {
  scale: 1,
  duration: 0.3,
  stagger: {
    each: 0.05,     // Time between each
    from: 'center', // Start from center, edges, random, etc.
    grid: [4, 4],   // Grid dimensions for 2D stagger
    axis: 'x'       // Stagger along axis
  }
});
```

## Easing Functions

### Built-in Eases

```javascript
// Power eases (1-4, higher = more pronounced)
'power1.out'    // Subtle deceleration
'power2.out'    // Smooth deceleration (default feel)
'power3.out'    // Strong deceleration
'power4.out'    // Very strong deceleration

// Directional suffixes
'power2.in'     // Accelerate
'power2.out'    // Decelerate
'power2.inOut'  // Accelerate then decelerate

// Special eases
'back.out(1.7)' // Overshoot then settle
'elastic.out'   // Springy bounce
'bounce.out'    // Ball-drop bounce
'circ.out'      // Circular motion
'expo.out'      // Exponential
'sine.out'      // Gentle sine wave
```

### Ease Comparison

```javascript
// UI Elements - snappy, responsive
gsap.to('.button', { scale: 1.1, ease: 'power2.out', duration: 0.2 });

// Entrances - smooth deceleration
gsap.from('.modal', { y: 100, opacity: 0, ease: 'power3.out', duration: 0.5 });

// Playful - bounce or elastic
gsap.to('.notification', { y: 0, ease: 'back.out(1.7)', duration: 0.6 });

// Mechanical - linear
gsap.to('.progress', { width: '100%', ease: 'none', duration: 2 });
```

### Custom Easing

```javascript
import { CustomEase } from 'gsap/CustomEase';
gsap.registerPlugin(CustomEase);

// Create custom ease from SVG path
CustomEase.create('custom', 'M0,0 C0.25,0.1 0.25,1 1,1');

gsap.to('.element', {
  x: 200,
  ease: 'custom',
  duration: 1
});
```

## Controlling Tweens

### Tween Instance Methods

```javascript
const tween = gsap.to('.element', {
  x: 200,
  duration: 2,
  paused: true  // Start paused
});

// Playback control
tween.play();
tween.pause();
tween.resume();
tween.reverse();
tween.restart();

// Seeking
tween.seek(0.5);        // Jump to 0.5 seconds
tween.progress(0.5);    // Jump to 50%
tween.time(1);          // Jump to 1 second

// Speed control
tween.timeScale(2);     // Double speed
tween.timeScale(0.5);   // Half speed

// State
tween.isActive();       // Currently animating?
tween.progress();       // Get current progress (0-1)

// Cleanup
tween.kill();           // Stop and remove
```

### Callbacks

```javascript
gsap.to('.element', {
  x: 200,
  duration: 1,

  // Lifecycle callbacks
  onStart: () => console.log('Started'),
  onUpdate: () => console.log('Frame update'),
  onComplete: () => console.log('Finished'),
  onRepeat: () => console.log('Repeated'),
  onReverseComplete: () => console.log('Reverse finished'),

  // With parameters
  onComplete: (param) => console.log('Done:', param),
  onCompleteParams: ['myValue'],

  // Access tween in callback
  onUpdate: function() {
    console.log('Progress:', this.progress());
  }
});
```

## Targeting Elements

### Selector Strings

```javascript
// CSS selectors
gsap.to('.class', { x: 100 });
gsap.to('#id', { x: 100 });
gsap.to('div', { x: 100 });
gsap.to('[data-animate]', { x: 100 });
gsap.to('.parent .child', { x: 100 });
```

### DOM References

```javascript
// Direct element reference
const element = document.querySelector('.box');
gsap.to(element, { x: 100 });

// NodeList / Array
const elements = document.querySelectorAll('.item');
gsap.to(elements, { x: 100, stagger: 0.1 });

// Array of mixed targets
gsap.to(['.box', '#circle', element], { opacity: 0.5 });
```

### Object Properties

```javascript
// Animate any object property
const obj = { value: 0, x: 100, y: 200 };

gsap.to(obj, {
  value: 100,
  x: 500,
  duration: 2,
  onUpdate: () => {
    console.log(obj.value);  // Interpolated value
    // Update Three.js, Canvas, etc.
  }
});
```

## Common Patterns

### Fade In/Out

```javascript
// Fade in
gsap.from('.element', {
  opacity: 0,
  duration: 0.5
});

// Fade out and remove
gsap.to('.element', {
  opacity: 0,
  duration: 0.5,
  onComplete: () => element.remove()
});
```

### Slide Animations

```javascript
// Slide in from left
gsap.from('.panel', {
  x: -100,
  opacity: 0,
  duration: 0.5,
  ease: 'power2.out'
});

// Slide in from bottom
gsap.from('.notification', {
  y: 50,
  opacity: 0,
  duration: 0.4,
  ease: 'power3.out'
});
```

### Scale Animations

```javascript
// Pop in
gsap.from('.modal', {
  scale: 0.8,
  opacity: 0,
  duration: 0.3,
  ease: 'back.out(1.7)'
});

// Pulse
gsap.to('.heart', {
  scale: 1.2,
  duration: 0.3,
  repeat: -1,
  yoyo: true,
  ease: 'power1.inOut'
});
```

## Temporal Collapse Patterns

Countdown-specific animations:

```javascript
// Digit flip animation
function flipDigit(element, newValue) {
  gsap.to(element, {
    rotationX: -90,
    opacity: 0,
    duration: 0.3,
    ease: 'power2.in',
    onComplete: () => {
      element.textContent = newValue;
      gsap.fromTo(element,
        { rotationX: 90, opacity: 0 },
        { rotationX: 0, opacity: 1, duration: 0.3, ease: 'power2.out' }
      );
    }
  });
}

// Time dilation pulse (cyan glow)
gsap.to('.countdown-digit', {
  textShadow: '0 0 30px #00F5FF, 0 0 60px #00F5FF',
  duration: 0.5,
  repeat: -1,
  yoyo: true,
  ease: 'sine.inOut'
});

// Final countdown intensity ramp
function intensifyCountdown(secondsRemaining) {
  const intensity = 1 - (secondsRemaining / 60);
  gsap.to('.glow-element', {
    filter: `brightness(${1 + intensity})`,
    duration: 0.5
  });
}
```

## Performance Tips

```javascript
// Use transforms over layout properties
// GOOD
gsap.to('.element', { x: 100, y: 50, scale: 1.2 });

// AVOID (triggers layout)
gsap.to('.element', { left: 100, top: 50, width: 200 });

// Force GPU acceleration
gsap.set('.element', { force3D: true });

// Kill tweens when component unmounts
const tween = gsap.to('.element', { x: 100 });
// Later...
tween.kill();

// Or kill all tweens on a target
gsap.killTweensOf('.element');
```

## Reference

- See `gsap-sequencing` for timelines and complex sequences
- See `gsap-react` for React integration patterns
- See `gsap-scrolltrigger` for scroll-based animations
