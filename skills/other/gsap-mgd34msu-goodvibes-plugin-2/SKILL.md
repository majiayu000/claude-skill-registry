---
name: gsap
description: Creates professional animations with GSAP (GreenSock Animation Platform). Use when building complex animations, scroll-triggered effects, timelines, or smooth transitions in any JavaScript framework.
---

# GSAP Animation

Professional-grade animation library for the modern web - now 100% FREE including all plugins after Webflow acquisition.

## Quick Start

```bash
npm install gsap
```

```javascript
import gsap from "gsap";

// Basic tween - animate to values
gsap.to(".box", {
  x: 100,
  rotation: 360,
  duration: 1,
  ease: "power2.out"
});
```

## Core Methods

### gsap.to() - Animate TO values
```javascript
gsap.to(".element", {
  x: 200,           // translateX
  y: 100,           // translateY
  rotation: 180,    // degrees
  scale: 1.5,
  opacity: 0.5,
  duration: 1,
  delay: 0.5,
  ease: "elastic.out(1, 0.3)"
});
```

### gsap.from() - Animate FROM values
```javascript
// Element animates FROM these values to current state
gsap.from(".element", {
  x: -200,
  opacity: 0,
  duration: 1
});
```

### gsap.fromTo() - Define both start and end
```javascript
gsap.fromTo(".element",
  { x: 0, opacity: 0 },     // from
  { x: 200, opacity: 1, duration: 1 }  // to
);
```

### gsap.set() - Immediate property set (no animation)
```javascript
gsap.set(".element", { x: 100, opacity: 0 });
```

## Timeline Sequences

Timelines group animations with precise timing control.

```javascript
const tl = gsap.timeline({
  defaults: { duration: 0.5, ease: "power2.out" }
});

tl.to(".box1", { x: 100 })
  .to(".box2", { x: 100 }, "-=0.3")  // overlap by 0.3s
  .to(".box3", { x: 100 }, "+=0.2")  // delay by 0.2s
  .to(".box4", { x: 100 }, "<")      // same start as previous
  .to(".box5", { x: 100 }, "<0.1");  // 0.1s after previous starts

// Control playback
tl.play();
tl.pause();
tl.reverse();
tl.restart();
tl.seek(1.5);  // jump to 1.5 seconds
```

### Position Parameter
```javascript
tl.to(el, {x: 100}, 2)        // absolute: 2 seconds into timeline
tl.to(el, {x: 100}, "+=1")    // relative: 1 second after previous ends
tl.to(el, {x: 100}, "-=0.5")  // overlap: 0.5s before previous ends
tl.to(el, {x: 100}, "<")      // same time as previous animation starts
tl.to(el, {x: 100}, ">")      // when previous animation ends
tl.to(el, {x: 100}, "myLabel") // at label position
```

## Special Properties

| Property | Description | Example |
|----------|-------------|---------|
| `duration` | Animation length (seconds) | `duration: 1` |
| `delay` | Wait before starting | `delay: 0.5` |
| `ease` | Timing curve | `ease: "power2.inOut"` |
| `repeat` | Times to repeat (-1 = infinite) | `repeat: 3` |
| `yoyo` | Reverse on alternate repeats | `yoyo: true` |
| `stagger` | Delay between multiple targets | `stagger: 0.1` |
| `onComplete` | Callback when done | `onComplete: () => {}` |
| `onUpdate` | Callback each frame | `onUpdate: () => {}` |
| `paused` | Start paused | `paused: true` |

## Stagger Animations

```javascript
// Simple stagger
gsap.to(".boxes", {
  x: 100,
  stagger: 0.1  // 0.1s between each
});

// Advanced stagger
gsap.to(".boxes", {
  x: 100,
  stagger: {
    each: 0.1,
    from: "center",  // start from center element
    grid: [4, 5],    // 4 rows, 5 columns
    axis: "y",       // stagger by row
    ease: "power2.in"
  }
});
```

## Easing

```javascript
// Built-in eases
"none"              // linear
"power1.out"        // subtle
"power2.out"        // moderate (default)
"power3.out"        // strong
"power4.out"        // more pronounced
"back.out(1.7)"     // overshoot
"elastic.out(1, 0.3)" // bouncy
"bounce.out"        // bounce effect
"circ.out"          // circular
"expo.out"          // exponential

// Directions: .in, .out, .inOut
"power2.in"         // slow start
"power2.out"        // slow end
"power2.inOut"      // slow both ends
```

## ScrollTrigger Plugin

Scroll-based animations - register plugin first.

```javascript
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

// Basic scroll trigger
gsap.to(".box", {
  scrollTrigger: ".box",  // trigger when .box enters viewport
  x: 500,
  rotation: 360
});

// Advanced configuration
gsap.to(".parallax", {
  scrollTrigger: {
    trigger: ".parallax",
    start: "top bottom",    // trigger start: element top, viewport bottom
    end: "bottom top",      // trigger end: element bottom, viewport top
    scrub: true,            // link animation to scroll position
    pin: true,              // pin element during animation
    markers: true,          // debug markers (remove in production)
    toggleActions: "play pause reverse reset"
  },
  y: -200,
  ease: "none"
});
```

### ScrollTrigger Options

```javascript
scrollTrigger: {
  trigger: ".element",      // element that triggers
  start: "top center",      // [trigger position] [scroller position]
  end: "bottom center",

  // Scrub - link to scroll
  scrub: true,              // instant scrub
  scrub: 0.5,              // smoothing (seconds to catch up)

  // Pin element
  pin: true,
  pinSpacing: true,

  // Toggle actions: onEnter onLeave onEnterBack onLeaveBack
  toggleActions: "play none none reverse",
  toggleClass: "active",

  // Callbacks
  onEnter: () => {},
  onLeave: () => {},
  onEnterBack: () => {},
  onLeaveBack: () => {},
  onUpdate: (self) => console.log(self.progress),

  // Horizontal scroll
  horizontal: true,

  // Custom scroller
  scroller: ".scroll-container",

  // Snap to sections
  snap: {
    snapTo: 1 / 4,         // snap to quarter sections
    duration: 0.5,
    ease: "power2.inOut"
  }
}
```

## React Integration

Use the official `@gsap/react` package for proper cleanup.

```bash
npm install @gsap/react
```

```jsx
import { useGSAP } from "@gsap/react";
import gsap from "gsap";

gsap.registerPlugin(useGSAP);

function Component() {
  const container = useRef();

  useGSAP(() => {
    // Animations auto-cleanup on unmount
    gsap.to(".box", { x: 360, rotation: 360 });
  }, { scope: container }); // scope animations to container

  return (
    <div ref={container}>
      <div className="box">Animate me</div>
    </div>
  );
}
```

### With Context for Manual Control

```jsx
function Component() {
  const container = useRef();

  const { contextSafe } = useGSAP({ scope: container });

  // Wrap event handlers with contextSafe
  const handleClick = contextSafe(() => {
    gsap.to(".box", { rotation: "+=360" });
  });

  return (
    <div ref={container}>
      <button onClick={handleClick}>Rotate</button>
      <div className="box" />
    </div>
  );
}
```

## Other Plugins (All FREE)

```javascript
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { Flip } from "gsap/Flip";
import { Draggable } from "gsap/Draggable";
import { MotionPathPlugin } from "gsap/MotionPathPlugin";
import { TextPlugin } from "gsap/TextPlugin";
import { SplitText } from "gsap/SplitText";
import { MorphSVGPlugin } from "gsap/MorphSVGPlugin";
import { DrawSVGPlugin } from "gsap/DrawSVGPlugin";
import { ScrollSmoother } from "gsap/ScrollSmoother";

gsap.registerPlugin(
  ScrollTrigger, Flip, Draggable, MotionPathPlugin,
  TextPlugin, SplitText, MorphSVGPlugin, DrawSVGPlugin,
  ScrollSmoother
);
```

## Performance Tips

1. **Use transforms and opacity** - GPU accelerated, no layout recalc
2. **Avoid** animating width, height, top, left, margin, padding
3. **Use will-change sparingly** - `will-change: transform`
4. **Limit concurrent animations** - batch or stagger
5. **Use `gsap.quickTo()`** for frequently updated values:

```javascript
const xTo = gsap.quickTo(".box", "x", { duration: 0.3 });
const yTo = gsap.quickTo(".box", "y", { duration: 0.3 });

window.addEventListener("mousemove", (e) => {
  xTo(e.clientX);
  yTo(e.clientY);
});
```

## Common Patterns

### Fade In on Scroll
```javascript
gsap.utils.toArray(".fade-in").forEach((el) => {
  gsap.from(el, {
    scrollTrigger: {
      trigger: el,
      start: "top 80%",
    },
    y: 50,
    opacity: 0,
    duration: 1
  });
});
```

### Horizontal Scroll Section
```javascript
const sections = gsap.utils.toArray(".panel");
gsap.to(sections, {
  xPercent: -100 * (sections.length - 1),
  ease: "none",
  scrollTrigger: {
    trigger: ".container",
    pin: true,
    scrub: 1,
    snap: 1 / (sections.length - 1),
    end: () => "+=" + document.querySelector(".container").offsetWidth
  }
});
```

### Text Reveal
```javascript
const split = new SplitText(".headline", { type: "chars, words" });
gsap.from(split.chars, {
  opacity: 0,
  y: 50,
  stagger: 0.02,
  duration: 0.5,
  ease: "back.out"
});
```

## Reference Files

- [references/scrolltrigger.md](references/scrolltrigger.md) - Complete ScrollTrigger guide
- [references/plugins.md](references/plugins.md) - All GSAP plugins overview
