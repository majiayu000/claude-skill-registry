---
name: animation
description: Expert guidance for creating premium, performant animations in React using Motion (motion.dev). Covers all animation types, best practices, accessibility, and performance optimization.
---

# Animation Skill

You are an expert in creating world-class, premium animations for React applications using **Motion** (motion.dev), the modern animation library for React.

## Installation

```bash
npm install motion
```

Import from `"motion/react"`:

```javascript
import { motion } from "motion/react";
```

---

## Core Concepts

### 1. The `<motion />` Component

The foundation of all animations in Motion. It's a React component that wraps any HTML or SVG element and supercharges it with animation capabilities.

**Basic Usage:**

```javascript
<motion.div animate={{ x: 100 }} />
<motion.button whileHover={{ scale: 1.1 }} />
<motion.svg whileTap={{ rotate: 90 }} />
```

**Key Props:**

- `initial`: Starting visual state (can be an object, variant name, or `false` to disable enter animation)
- `animate`: Target state to animate to
- `exit`: State to animate to when removed from DOM (requires `<AnimatePresence>`)
- `transition`: Customize animation timing and easing
- `variants`: Reusable animation states
- `style`: React style prop with support for MotionValues

---

## Animation Types

### 2. Enter Animations

Components automatically animate to `animate` values when they mount.

```javascript
<motion.div initial={{ opacity: 0, y: 50 }} animate={{ opacity: 1, y: 0 }} />
```

**Disable enter animation:**

```javascript
<motion.div initial={false} animate={{ opacity: 1 }} />
```

---

### 3. Gesture Animations

Motion provides declarative gesture handlers that feel better than CSS or plain JavaScript events.

#### Hover

```javascript
<motion.button
  whileHover={{ scale: 1.1, backgroundColor: "#ff0000" }}
  transition={{ duration: 0.2 }}
/>
```

#### Tap/Press

```javascript
<motion.button
  whileTap={{ scale: 0.95 }}
  onTap={() => console.log("Tapped!")}
/>
```

#### Focus

```javascript
<motion.input whileFocus={{ borderColor: "#0099ff" }} />
```

#### Drag

```javascript
<motion.div
  drag
  dragConstraints={{ left: -100, right: 100, top: -100, bottom: 100 }}
  whileDrag={{ scale: 1.1 }}
/>
```

**Drag Options:**

- `drag={true}`: Drag in all directions
- `drag="x"`: Horizontal only
- `drag="y"`: Vertical only
- `dragConstraints`: Limits (object or ref to container)
- `dragElastic`: Elasticity when out of bounds (0-1, default: 0.5)
- `dragMomentum`: Enable momentum on release (default: true)

---

### 4. Scroll Animations

#### Scroll-Triggered (whileInView)

Animate when element enters viewport:

```javascript
<motion.div
  initial={{ opacity: 0, y: 100 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, amount: 0.5 }}
/>
```

**viewport options:**

- `once`: Only trigger once (default: false)
- `amount`: How much of element must be visible ("some", "all", or 0-1)
- `margin`: Offset from viewport edges
- `root`: Custom scroll container

#### Scroll-Linked (useScroll)

Link animations directly to scroll position:

```javascript
const { scrollYProgress } = useScroll();

return <motion.div style={{ scaleX: scrollYProgress }} />;
```

**useScroll returns:**

- `scrollX`, `scrollY`: Scroll offset in pixels
- `scrollXProgress`, `scrollYProgress`: Scroll progress (0-1)

**Advanced scroll tracking:**

```javascript
const { scrollYProgress } = useScroll({
  target: ref, // Element to track
  offset: ["start end", "end start"], // When to start/end
});
```

---

### 5. Layout Animations

Motion uses FLIP (First, Last, Invert, Play) to animate layout changes using performant transforms.

#### Simple Layout Animation

```javascript
<motion.div layout />
```

#### Shared Element Transitions

```javascript
{
  isExpanded ? <motion.div layoutId="card" /> : <motion.div layoutId="card" />;
}
```

**Layout Props:**

- `layout`: Animate size and position changes
- `layoutId`: Shared element transitions between components
- `layoutDependency`: Force recalculation on value change
- `layoutScroll`: Animate within scrollable containers

**Performance Note:** Layout animations run at 60fps by animating transforms, not layout properties.

---

### 6. Exit Animations

Wrap components with `<AnimatePresence>` to enable exit animations:

```javascript
<AnimatePresence mode="wait">
  {isVisible && (
    <motion.div
      key="modal"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    />
  )}
</AnimatePresence>
```

**AnimatePresence Props:**

- `mode`: "sync" (default), "wait", "popLayout"
- `initial`: Disable initial animations (default: true)
- `onExitComplete`: Callback when all exit animations complete

---

### 7. SVG Animations

Motion supports SVG-specific animations:

```javascript
// Line drawing
<motion.path
  initial={{ pathLength: 0 }}
  animate={{ pathLength: 1 }}
/>

// Morphing (same number of points)
<motion.path
  animate={{ d: "M10,10 L20,20 ..." }}
/>

// Attributes
<motion.circle
  animate={{
    cx: 50,
    r: 20,
    fill: "#ff0000"
  }}
/>
```

---

## Advanced Features

### 8. Variants

Reusable animation states with propagation and orchestration:

```javascript
const variants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      delay: 0.2,
      when: "beforeChildren",
      staggerChildren: 0.1,
    },
  },
};

<motion.ul variants={variants} initial="hidden" animate="visible">
  <motion.li variants={variants} />
  <motion.li variants={variants} />
</motion.ul>;
```

**Variant Orchestration:**

- `when`: "beforeChildren", "afterChildren"
- `staggerChildren`: Delay between child animations
- `delayChildren`: Delay before first child
- `staggerDirection`: 1 (forward) or -1 (backward)

**Dynamic Variants:**

```javascript
const variants = {
  visible: (i) => ({
    opacity: 1,
    transition: { delay: i * 0.1 },
  }),
};

<motion.div custom={index} variants={variants} />;
```

---

### 9. Transitions

Configure animation timing and behavior:

#### Tween (Time-based)

```javascript
<motion.div
  animate={{ x: 100 }}
  transition={{
    duration: 0.5,
    ease: "easeInOut", // or [.17,.67,.83,.67] for cubic-bezier
  }}
/>
```

**Easing options:** "linear", "easeIn", "easeOut", "easeInOut", "circIn", "circOut", "circInOut", "backIn", "backOut", "backInOut", "anticipate"

#### Spring (Physics-based)

```javascript
<motion.div
  animate={{ x: 100 }}
  transition={{
    type: "spring",
    stiffness: 100,
    damping: 10,
    mass: 1,
  }}
/>
```

**Spring Presets:**

- `bounce: 0.25`: Natural feel (default)
- `bounce: 0`: No bounce
- `bounce: 0.6`: Very bouncy

Or use `duration` with `bounce`:

```javascript
transition={{ duration: 0.8, bounce: 0.3 }}
```

#### Keyframes

```javascript
<motion.div
  animate={{
    x: [0, 100, 0],
    backgroundColor: ["#ff0000", "#00ff00", "#0000ff"],
  }}
  transition={{
    duration: 2,
    times: [0, 0.5, 1], // Optional: control keyframe timing
    ease: ["easeIn", "easeOut"], // Different easing per segment
  }}
/>
```

---

### 10. Motion Values

Track and compose values without triggering re-renders:

```javascript
const x = useMotionValue(0);
const opacity = useTransform(x, [0, 100], [1, 0]);

return <motion.div style={{ x, opacity }} />;
```

**Key Hooks:**

#### useMotionValue

```javascript
const x = useMotionValue(0);
x.set(100); // Update without re-render
x.get(); // Get current value
```

#### useTransform

```javascript
// Map one range to another
const y = useTransform(scrollY, [0, 300], [0, 100]);

// Custom function
const color = useTransform(x, (latest) =>
  latest > 50 ? "#ff0000" : "#0000ff",
);
```

#### useSpring

```javascript
const x = useMotionValue(0);
const smoothX = useSpring(x, {
  stiffness: 100,
  damping: 20,
});
```

#### useScroll

```javascript
const { scrollYProgress } = useScroll({
  target: containerRef,
  offset: ["start start", "end end"],
});
```

#### useInView

```javascript
const ref = useRef(null);
const isInView = useInView(ref, {
  once: true,
  amount: 0.5,
});
```

#### useVelocity

```javascript
const x = useMotionValue(0);
const xVelocity = useVelocity(x);
```

---

## Premium Components

### 11. AnimateNumber

Animate number changes with layout animations:

```javascript
import { AnimateNumber } from "motion/react";

<AnimateNumber value={count} transition={{ duration: 0.5 }} />;
```

---

### 12. Carousel

Production-ready carousel with infinite scrolling:

```javascript
import { Carousel } from "motion/react";

<Carousel.Root loop>
  <Carousel.Viewport>
    {items.map((item) => (
      <Carousel.Item key={item.id}>{item.content}</Carousel.Item>
    ))}
  </Carousel.Viewport>
  <Carousel.Controls />
</Carousel.Root>;
```

---

### 13. Cursor

Custom cursor with auto-adaptation to interactive elements:

```javascript
import { Cursor } from "motion/react";

<Cursor className="custom-cursor" />;
```

---

### 14. Ticker

Infinite scrolling marquee:

```javascript
import { Ticker } from "motion/react";

<Ticker speed={50}>
  <div>Scrolling content...</div>
</Ticker>;
```

---

### 15. Typewriter

Realistic typing animation:

```javascript
import { Typewriter } from "motion/react";

<Typewriter text="Hello, world!" speed={50} />;
```

---

### 16. Reorder

Drag-to-reorder lists:

```javascript
import { Reorder } from "motion/react";

<Reorder.Group values={items} onReorder={setItems}>
  {items.map((item) => (
    <Reorder.Item key={item} value={item}>
      {item}
    </Reorder.Item>
  ))}
</Reorder.Group>;
```

---

## Performance & Optimization

### 17. LazyMotion

Reduce bundle size by loading features on demand:

```javascript
import { LazyMotion, domAnimation } from "motion/react";

<LazyMotion features={domAnimation} strict>
  <App />
</LazyMotion>;
```

**Features:**

- `domAnimation`: ~30kb (gestures, drag, layout)
- `domMax`: ~60kb (all features)
- Async loading: `features={() => import('./features')}`

---

### 18. MotionConfig

Configure all child motion components:

```javascript
<MotionConfig
  transition={{ duration: 0.3 }}
  reducedMotion="user" // Respect prefers-reduced-motion
>
  <App />
</MotionConfig>
```

---

### 19. Performance Tips

**Hardware Acceleration:** Motion automatically uses transforms for layout animations (60fps).

**Avoid animating:** `width`, `height`, `top`, `left` directly. Use `scale` and `x`/`y` instead.

**Good:**

```javascript
<motion.div animate={{ x: 100, scale: 1.2 }} />
```

**Bad:**

```javascript
<motion.div animate={{ left: 100, width: 200 }} /> // Forces layout recalc
```

**Will-change:** Motion automatically applies `will-change` when needed.

**Reduce render triggers:** Use MotionValues to update without re-renders.

---

## Accessibility

### 20. Reduced Motion

Respect user preferences:

```javascript
const shouldReduceMotion = useReducedMotion();

<motion.div
  animate={shouldReduceMotion ? { opacity: 1 } : { opacity: 1, y: 0 }}
/>;
```

Or globally:

```javascript
<MotionConfig reducedMotion="user">
  <App />
</MotionConfig>
```

---

## Best Practices

### 21. Premium Animation Guidelines

1. **Natural Motion:** Use spring animations for interactive elements

   ```javascript
   transition={{ type: "spring", bounce: 0.25 }}
   ```

2. **Micro-interactions:** Add subtle hover/tap feedback

   ```javascript
   whileHover={{ scale: 1.05 }}
   whileTap={{ scale: 0.98 }}
   ```

3. **Stagger Children:** Create elegant cascading effects

   ```javascript
   variants={{
     visible: {
       transition: { staggerChildren: 0.1 }
     }
   }}
   ```

4. **Smooth Scroll Links:** Use scroll-linked animations for parallax and progress

   ```javascript
   const { scrollYProgress } = useScroll();
   ```

5. **Exit Animations:** Always animate elements out, don't just remove them

   ```javascript
   <AnimatePresence mode="wait">{/* content */}</AnimatePresence>
   ```

6. **Layout Animations:** Use `layout` prop for seamless size/position transitions

   ```javascript
   <motion.div layout />
   ```

7. **Performant Transforms:** Use scale/translate over width/height

   ```javascript
   // Good
   animate={{ scale: 1.2, x: 100 }}

   // Bad
   animate={{ width: 200, left: 100 }}
   ```

---

## Common Patterns

### 22. Page Transitions

```javascript
<AnimatePresence mode="wait">
  <motion.div
    key={router.pathname}
    initial={{ opacity: 0, x: -20 }}
    animate={{ opacity: 1, x: 0 }}
    exit={{ opacity: 0, x: 20 }}
    transition={{ duration: 0.3 }}
  >
    {children}
  </motion.div>
</AnimatePresence>
```

### 23. Modal/Dialog

```javascript
<AnimatePresence>
  {isOpen && (
    <>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onClose}
        className="backdrop"
      />
      <motion.div
        initial={{ opacity: 0, scale: 0.9, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.9, y: 20 }}
        className="modal"
      >
        {content}
      </motion.div>
    </>
  )}
</AnimatePresence>
```

### 24. Accordion

```javascript
<motion.div layout>
  <motion.button onClick={toggle} layout>
    {title}
  </motion.button>
  <AnimatePresence initial={false}>
    {isOpen && (
      <motion.div
        initial={{ height: 0, opacity: 0 }}
        animate={{ height: "auto", opacity: 1 }}
        exit={{ height: 0, opacity: 0 }}
      >
        {content}
      </motion.div>
    )}
  </AnimatePresence>
</motion.div>
```

### 25. Parallax Scroll

```javascript
const { scrollYProgress } = useScroll();
const y = useTransform(scrollYProgress, [0, 1], [0, -500]);

return <motion.div style={{ y }}>{content}</motion.div>;
```

### 26. Hover Cards

```javascript
<motion.div
  whileHover={{
    scale: 1.05,
    boxShadow: "0px 10px 30px rgba(0,0,0,0.2)",
  }}
  transition={{ type: "spring", stiffness: 300 }}
>
  {content}
</motion.div>
```

---

## Troubleshooting

### Common Issues

**Layout animations not working:**

- Ensure element has defined dimensions
- Check parent isn't `display: inline`
- Verify no `transform` in CSS (conflicts with Motion)

**Exit animations not working:**

- Must be direct child of `<AnimatePresence>`
- Ensure unique `key` prop
- Check component isn't conditional before `<AnimatePresence>`

**Performance issues:**

- Avoid animating layout properties directly
- Use `will-change` sparingly (Motion handles this)
- Consider `LazyMotion` for bundle optimization

**SVG animations broken:**

- Set `layout="position"` instead of `layout={true}`
- Use `attrX`/`attrY` for SVG positioning

---

## Resources

- **Documentation:** https://motion.dev/docs/react
- **Examples:** https://motion.dev/examples
- **GitHub:** https://github.com/motiondivision/motion

---

## Summary

Motion is the most powerful animation library for React, offering:

- ✅ Declarative API with `<motion />` components
- ✅ Gesture support (hover, tap, drag, focus)
- ✅ Layout animations using FLIP
- ✅ Scroll-triggered and scroll-linked animations
- ✅ Exit animations with `<AnimatePresence>`
- ✅ SVG animation support
- ✅ Motion values for performance
- ✅ Accessibility with reduced motion support
- ✅ Premium components (Carousel, Ticker, Typewriter, etc.)
- ✅ Tree-shakeable and optimizable with LazyMotion

**Remember:** Always prioritize performance by using transforms, respect user preferences with reduced motion, and create premium experiences with natural spring animations and thoughtful micro-interactions.
