---
name: gsap-react
description: GSAP integration with React including useGSAP hook, ref handling, cleanup patterns, and context management. Use when implementing GSAP animations in React components, handling component lifecycle, or building reusable animation hooks.
---

# GSAP React Integration

React-specific patterns for GSAP animations.

## Quick Start

```bash
npm install gsap @gsap/react
```

```tsx
import { useGSAP } from '@gsap/react';
import gsap from 'gsap';

function Component() {
  const containerRef = useRef(null);

  useGSAP(() => {
    gsap.to('.box', { x: 200, duration: 1 });
  }, { scope: containerRef });

  return (
    <div ref={containerRef}>
      <div className="box">Animated</div>
    </div>
  );
}
```

## useGSAP Hook

### Basic Usage

```tsx
import { useGSAP } from '@gsap/react';
import gsap from 'gsap';

function AnimatedComponent() {
  const container = useRef(null);

  useGSAP(() => {
    // All GSAP animations here
    gsap.from('.item', {
      opacity: 0,
      y: 50,
      stagger: 0.1
    });
  }, { scope: container }); // Scope limits selector queries

  return (
    <div ref={container}>
      <div className="item">Item 1</div>
      <div className="item">Item 2</div>
      <div className="item">Item 3</div>
    </div>
  );
}
```

### With Dependencies

```tsx
function AnimatedComponent({ isOpen }) {
  const container = useRef(null);

  useGSAP(() => {
    gsap.to('.drawer', {
      height: isOpen ? 'auto' : 0,
      duration: 0.3
    });
  }, { scope: container, dependencies: [isOpen] });

  return (
    <div ref={container}>
      <div className="drawer">Content</div>
    </div>
  );
}
```

### Returning Context

```tsx
function Component() {
  const container = useRef(null);

  const { context, contextSafe } = useGSAP(() => {
    gsap.to('.box', { x: 200 });
  }, { scope: container });

  // Use contextSafe for event handlers
  const handleClick = contextSafe(() => {
    gsap.to('.box', { rotation: 360 });
  });

  return (
    <div ref={container}>
      <div className="box" onClick={handleClick}>Click me</div>
    </div>
  );
}
```

## Ref Patterns

### Single Element Ref

```tsx
function SingleElement() {
  const boxRef = useRef(null);

  useGSAP(() => {
    gsap.to(boxRef.current, {
      x: 200,
      rotation: 360,
      duration: 1
    });
  });

  return <div ref={boxRef}>Box</div>;
}
```

### Multiple Element Refs

```tsx
function MultipleElements() {
  const itemsRef = useRef([]);

  useGSAP(() => {
    gsap.from(itemsRef.current, {
      opacity: 0,
      y: 30,
      stagger: 0.1
    });
  });

  return (
    <div>
      {[1, 2, 3].map((item, i) => (
        <div
          key={item}
          ref={el => itemsRef.current[i] = el}
        >
          Item {item}
        </div>
      ))}
    </div>
  );
}
```

### Dynamic Refs

```tsx
function DynamicList({ items }) {
  const itemsRef = useRef(new Map());

  useGSAP(() => {
    gsap.from(Array.from(itemsRef.current.values()), {
      opacity: 0,
      y: 20,
      stagger: 0.05
    });
  }, { dependencies: [items.length] });

  return (
    <div>
      {items.map(item => (
        <div
          key={item.id}
          ref={el => {
            if (el) itemsRef.current.set(item.id, el);
            else itemsRef.current.delete(item.id);
          }}
        >
          {item.name}
        </div>
      ))}
    </div>
  );
}
```

## Context and Cleanup

### Automatic Cleanup

```tsx
// useGSAP automatically cleans up animations on unmount
function Component() {
  useGSAP(() => {
    // This timeline is automatically killed on unmount
    gsap.timeline()
      .to('.a', { x: 100 })
      .to('.b', { x: 100 });
  });
}
```

### Manual Context (Without useGSAP)

```tsx
import gsap from 'gsap';

function Component() {
  useEffect(() => {
    const ctx = gsap.context(() => {
      gsap.to('.box', { x: 200 });
      gsap.to('.circle', { rotation: 360 });
    });

    return () => ctx.revert(); // Cleanup
  }, []);
}
```

### Scoped Context

```tsx
function Component() {
  const containerRef = useRef(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      // Selectors only query within containerRef
      gsap.to('.item', { opacity: 1 });
    }, containerRef);

    return () => ctx.revert();
  }, []);
}
```

## Event Handlers

### contextSafe for Events

```tsx
function InteractiveComponent() {
  const container = useRef(null);

  const { contextSafe } = useGSAP(() => {
    // Initial animation
    gsap.set('.box', { scale: 1 });
  }, { scope: container });

  const handleMouseEnter = contextSafe(() => {
    gsap.to('.box', { scale: 1.1, duration: 0.2 });
  });

  const handleMouseLeave = contextSafe(() => {
    gsap.to('.box', { scale: 1, duration: 0.2 });
  });

  return (
    <div ref={container}>
      <div
        className="box"
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
      >
        Hover me
      </div>
    </div>
  );
}
```

### useCallback Alternative

```tsx
function Component() {
  const boxRef = useRef(null);
  const tweenRef = useRef(null);

  const animateBox = useCallback(() => {
    tweenRef.current?.kill();
    tweenRef.current = gsap.to(boxRef.current, {
      x: '+=50',
      duration: 0.3
    });
  }, []);

  useEffect(() => {
    return () => tweenRef.current?.kill();
  }, []);

  return <div ref={boxRef} onClick={animateBox}>Click</div>;
}
```

## Timeline Management

### Timeline Ref Pattern

```tsx
function TimelineComponent() {
  const container = useRef(null);
  const tl = useRef(null);

  useGSAP(() => {
    tl.current = gsap.timeline({ paused: true })
      .to('.box', { x: 200 })
      .to('.box', { y: 100 })
      .to('.box', { rotation: 360 });
  }, { scope: container });

  const play = () => tl.current?.play();
  const reverse = () => tl.current?.reverse();
  const restart = () => tl.current?.restart();

  return (
    <div ref={container}>
      <div className="box">Animated</div>
      <button onClick={play}>Play</button>
      <button onClick={reverse}>Reverse</button>
      <button onClick={restart}>Restart</button>
    </div>
  );
}
```

### Controlled Timeline

```tsx
function ControlledAnimation({ progress }) {
  const container = useRef(null);
  const tl = useRef(null);

  useGSAP(() => {
    tl.current = gsap.timeline({ paused: true })
      .to('.element', { x: 500 })
      .to('.element', { y: 200 });
  }, { scope: container });

  // Update timeline progress when prop changes
  useEffect(() => {
    if (tl.current) {
      tl.current.progress(progress);
    }
  }, [progress]);

  return (
    <div ref={container}>
      <div className="element">Controlled</div>
    </div>
  );
}
```

## ScrollTrigger in React

### Basic ScrollTrigger

```tsx
import { useGSAP } from '@gsap/react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

function ScrollComponent() {
  const container = useRef(null);

  useGSAP(() => {
    gsap.from('.section', {
      opacity: 0,
      y: 100,
      scrollTrigger: {
        trigger: '.section',
        start: 'top 80%',
        toggleActions: 'play none none none'
      }
    });
  }, { scope: container });

  return (
    <div ref={container}>
      <div className="section">Scroll to reveal</div>
    </div>
  );
}
```

### ScrollTrigger Cleanup

```tsx
function ScrollComponent() {
  const container = useRef(null);

  useGSAP(() => {
    const triggers = [];

    gsap.utils.toArray('.item').forEach(item => {
      const trigger = ScrollTrigger.create({
        trigger: item,
        start: 'top 80%',
        onEnter: () => gsap.to(item, { opacity: 1 })
      });
      triggers.push(trigger);
    });

    // Return cleanup function
    return () => triggers.forEach(t => t.kill());
  }, { scope: container });
}
```

## Custom Hooks

### useAnimation Hook

```tsx
function useAnimation(animation, deps = []) {
  const elementRef = useRef(null);
  const tweenRef = useRef(null);

  useGSAP(() => {
    if (elementRef.current) {
      tweenRef.current = animation(elementRef.current);
    }
    return () => tweenRef.current?.kill();
  }, { dependencies: deps });

  return elementRef;
}

// Usage
function Component() {
  const boxRef = useAnimation((el) =>
    gsap.from(el, { opacity: 0, y: 50, duration: 0.5 })
  );

  return <div ref={boxRef}>Animated</div>;
}
```

### useFadeIn Hook

```tsx
function useFadeIn(options = {}) {
  const { duration = 0.5, delay = 0, y = 30 } = options;
  const ref = useRef(null);

  useGSAP(() => {
    gsap.from(ref.current, {
      opacity: 0,
      y,
      duration,
      delay,
      ease: 'power2.out'
    });
  });

  return ref;
}

// Usage
function Card() {
  const cardRef = useFadeIn({ delay: 0.2 });
  return <div ref={cardRef}>Card content</div>;
}
```

### useHoverAnimation Hook

```tsx
function useHoverAnimation(enterAnimation, leaveAnimation) {
  const ref = useRef(null);
  const { contextSafe } = useGSAP({ scope: ref });

  const onEnter = contextSafe(() => enterAnimation(ref.current));
  const onLeave = contextSafe(() => leaveAnimation(ref.current));

  return { ref, onMouseEnter: onEnter, onMouseLeave: onLeave };
}

// Usage
function Button() {
  const hoverProps = useHoverAnimation(
    (el) => gsap.to(el, { scale: 1.05, duration: 0.2 }),
    (el) => gsap.to(el, { scale: 1, duration: 0.2 })
  );

  return <button {...hoverProps}>Hover me</button>;
}
```

## Temporal Collapse Patterns

### Animated Countdown Digit

```tsx
function CountdownDigit({ value, label }) {
  const digitRef = useRef(null);
  const prevValue = useRef(value);

  useGSAP(() => {
    if (prevValue.current !== value) {
      gsap.timeline()
        .to(digitRef.current, {
          rotationX: -90,
          opacity: 0,
          duration: 0.25,
          ease: 'power2.in'
        })
        .call(() => {
          digitRef.current.textContent = value;
          prevValue.current = value;
        })
        .fromTo(digitRef.current,
          { rotationX: 90, opacity: 0 },
          { rotationX: 0, opacity: 1, duration: 0.25, ease: 'power2.out' }
        );
    }
  }, { dependencies: [value] });

  return (
    <div className="digit-container">
      <span ref={digitRef} className="digit">{value}</span>
      <span className="label">{label}</span>
    </div>
  );
}
```

### Cosmic Pulse Effect

```tsx
function CosmicPulse({ children, color = '#00F5FF' }) {
  const containerRef = useRef(null);

  useGSAP(() => {
    gsap.to(containerRef.current, {
      boxShadow: `0 0 30px ${color}, 0 0 60px ${color}`,
      duration: 1,
      repeat: -1,
      yoyo: true,
      ease: 'sine.inOut'
    });
  }, { scope: containerRef });

  return <div ref={containerRef}>{children}</div>;
}
```

## Performance Tips

```tsx
// 1. Use will-change for heavy animations
gsap.set('.animated', { willChange: 'transform' });

// 2. Batch similar animations
useGSAP(() => {
  gsap.to('.item', { opacity: 1, stagger: 0.1 }); // Single tween
  // Not: items.forEach(item => gsap.to(item, ...)) // Multiple tweens
});

// 3. Use refs over selectors for frequently animated elements
const boxRef = useRef(null);
gsap.to(boxRef.current, { x: 100 }); // Faster

// 4. Kill animations on rapid state changes
const tweenRef = useRef(null);
useEffect(() => {
  tweenRef.current?.kill();
  tweenRef.current = gsap.to(...);
}, [dependency]);
```

## Reference

- See `gsap-fundamentals` for animation basics
- See `gsap-sequencing` for timeline composition
- See `gsap-scrolltrigger` for scroll-based animations
