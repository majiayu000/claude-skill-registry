---
name: framer-motion-best-practices
description: Framer Motion performance optimization guidelines. This skill should be used when writing, reviewing, or refactoring React animations with Framer Motion to ensure optimal performance patterns. Triggers on tasks involving motion components, animations, gestures, layout transitions, scroll-linked effects, and SVG animations.
---

# Community Framer Motion Best Practices

Comprehensive performance optimization guide for Framer Motion animations in React applications. Contains 42 rules across 9 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Adding animations to React components with Framer Motion
- Optimizing bundle size for animation-heavy applications
- Preventing unnecessary re-renders during animations
- Implementing layout transitions or shared element animations
- Building scroll-linked or gesture-based interactions

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Bundle Optimization | CRITICAL | `bundle-` |
| 2 | Re-render Prevention | CRITICAL | `rerender-` |
| 3 | Animation Properties | HIGH | `anim-` |
| 4 | Layout Animations | HIGH | `layout-` |
| 5 | Scroll Animations | MEDIUM-HIGH | `scroll-` |
| 6 | Gesture Optimization | MEDIUM | `gesture-` |
| 7 | Spring & Physics | MEDIUM | `spring-` |
| 8 | SVG & Path Animations | LOW-MEDIUM | `svg-` |
| 9 | Exit Animations | LOW | `exit-` |

## Quick Reference

### 1. Bundle Optimization (CRITICAL)

- [`bundle-lazy-motion`](references/bundle-lazy-motion.md) - Use LazyMotion and m component instead of motion
- [`bundle-dynamic-features`](references/bundle-dynamic-features.md) - Dynamically import motion features
- [`bundle-dom-animation`](references/bundle-dom-animation.md) - Use domAnimation for basic animations
- [`bundle-use-animate-mini`](references/bundle-use-animate-mini.md) - Use mini useAnimate for simple cases
- [`bundle-strict-mode`](references/bundle-strict-mode.md) - Enable strict mode to catch accidental imports

### 2. Re-render Prevention (CRITICAL)

- [`rerender-motion-value`](references/rerender-motion-value.md) - Use useMotionValue instead of useState
- [`rerender-use-transform`](references/rerender-use-transform.md) - Derive values with useTransform
- [`rerender-stable-callbacks`](references/rerender-stable-callbacks.md) - Keep animation callbacks stable
- [`rerender-variants-object`](references/rerender-variants-object.md) - Define variants outside component
- [`rerender-animate-prop`](references/rerender-animate-prop.md) - Use stable animate values
- [`rerender-motion-value-event`](references/rerender-motion-value-event.md) - Use motion value events

### 3. Animation Properties (HIGH)

- [`anim-transform-properties`](references/anim-transform-properties.md) - Animate transform properties
- [`anim-opacity-filter`](references/anim-opacity-filter.md) - Prefer opacity and filter for visual effects
- [`anim-hardware-acceleration`](references/anim-hardware-acceleration.md) - Leverage hardware acceleration
- [`anim-will-change`](references/anim-will-change.md) - Use willChange prop judiciously
- [`anim-independent-transforms`](references/anim-independent-transforms.md) - Animate transforms independently
- [`anim-keyframes-array`](references/anim-keyframes-array.md) - Use keyframe arrays for sequences

### 4. Layout Animations (HIGH)

- [`layout-dependency`](references/layout-dependency.md) - Use layoutDependency to limit measurements
- [`layout-position-size`](references/layout-position-size.md) - Use layout="position" or "size" appropriately
- [`layout-group`](references/layout-group.md) - Group related layout animations
- [`layout-id-shared`](references/layout-id-shared.md) - Use layoutId for shared element transitions
- [`layout-scroll`](references/layout-scroll.md) - Add layoutScroll to scrollable ancestors

### 5. Scroll Animations (MEDIUM-HIGH)

- [`scroll-use-scroll`](references/scroll-use-scroll.md) - Use useScroll hook for scroll-linked animations
- [`scroll-use-spring-smooth`](references/scroll-use-spring-smooth.md) - Smooth scroll animations with useSpring
- [`scroll-element-tracking`](references/scroll-element-tracking.md) - Track specific elements entering viewport
- [`scroll-offset-configuration`](references/scroll-offset-configuration.md) - Configure scroll offsets
- [`scroll-container-ref`](references/scroll-container-ref.md) - Track scroll within specific containers

### 6. Gesture Optimization (MEDIUM)

- [`gesture-while-props`](references/gesture-while-props.md) - Use whileHover/whileTap instead of handlers
- [`gesture-variants-flow`](references/gesture-variants-flow.md) - Let gesture variants flow to children
- [`gesture-drag-constraints`](references/gesture-drag-constraints.md) - Use dragConstraints ref for boundaries
- [`gesture-drag-elastic`](references/gesture-drag-elastic.md) - Configure dragElastic for natural feel
- [`gesture-tap-cancel`](references/gesture-tap-cancel.md) - Use onTapCancel for interrupted gestures

### 7. Spring & Physics (MEDIUM)

- [`spring-physics-based`](references/spring-physics-based.md) - Use physics-based springs for interruptibility
- [`spring-damping-ratio`](references/spring-damping-ratio.md) - Configure damping to control oscillation
- [`spring-mass-inertia`](references/spring-mass-inertia.md) - Adjust mass for heavier/lighter feel
- [`spring-use-spring-hook`](references/spring-use-spring-hook.md) - Use useSpring for reactive values

### 8. SVG & Path Animations (LOW-MEDIUM)

- [`svg-path-length`](references/svg-path-length.md) - Use pathLength for line drawing animations
- [`svg-motion-components`](references/svg-motion-components.md) - Use motion.path and motion.circle
- [`svg-viewbox-animation`](references/svg-viewbox-animation.md) - Animate viewBox for zoom effects
- [`svg-morph-matching-points`](references/svg-morph-matching-points.md) - Match point counts for morphing

### 9. Exit Animations (LOW)

- [`exit-animate-presence`](references/exit-animate-presence.md) - Wrap conditional renders with AnimatePresence
- [`exit-unique-keys`](references/exit-unique-keys.md) - Provide unique keys for AnimatePresence children
- [`exit-mode-wait`](references/exit-mode-wait.md) - Use mode="wait" for sequential transitions

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

## Reference Files

| File | Description |
|------|-------------|
| [references/_sections.md](references/_sections.md) | Category definitions and ordering |
| [assets/templates/_template.md](assets/templates/_template.md) | Template for new rules |
| [metadata.json](metadata.json) | Version and reference information |
