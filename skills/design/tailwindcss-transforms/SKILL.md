---
name: tailwindcss-transforms
description: "Transform & Animation utilities Tailwind CSS v4.1. Transform (scale-*, rotate-*, translate-*, skew-*, transform-origin), Transition (transition-*, duration-*, ease-*, delay-*), Animation (animate-*, @keyframes)."
user-invocable: false
---

# Tailwind CSS Transforms & Animations v4.1

Complete reference for Transform, Transition, and Animation utilities in Tailwind CSS v4.1.

## Transform Utilities

### Scale
Transform an element by scaling (resizing) it.

```html
<!-- Scale in X, Y, or both -->
<div class="scale-50">50%</div>
<div class="scale-100">100%</div>
<div class="scale-125">125%</div>
<div class="scale-150">150%</div>
<div class="scale-x-50">Scale X only</div>
<div class="scale-y-75">Scale Y only</div>
```

**Responsive**: `sm:scale-125`, `md:scale-150`, `lg:scale-100`
**States**: `hover:scale-110`, `focus:scale-105`, `group-hover:scale-125`

### Rotate
Rotate an element by an angle.

```html
<!-- Rotate by degrees -->
<div class="rotate-0">0°</div>
<div class="rotate-45">45°</div>
<div class="rotate-90">90°</div>
<div class="rotate-180">180°</div>
<div class="-rotate-45">-45°</div>
```

**Responsive**: `sm:rotate-90`, `md:rotate-180`, `lg:rotate-0`
**States**: `hover:rotate-45`, `focus:rotate-90`

### Translate
Move an element along X and Y axes.

```html
<!-- Translate X and Y -->
<div class="translate-x-0">No translation</div>
<div class="translate-x-2">X direction</div>
<div class="translate-y-4">Y direction</div>
<div class="translate-x-6 translate-y-8">Both axes</div>
<div class="-translate-x-2">Negative X</div>
<div class="-translate-y-4">Negative Y</div>
```

**Responsive**: `sm:translate-x-4`, `md:translate-y-8`
**States**: `hover:translate-y-2`, `focus:translate-x-1`

### Skew
Skew an element along X and Y axes.

```html
<!-- Skew transform -->
<div class="skew-x-3">Skew X</div>
<div class="skew-y-6">Skew Y</div>
<div class="skew-x-3 skew-y-6">Both skew</div>
<div class="-skew-x-3">Negative skew</div>
```

**Responsive**: `sm:skew-x-6`, `md:skew-y-3`
**States**: `hover:skew-x-2`, `group-hover:skew-y-4`

### Transform Origin
Set the origin point for transform operations.

```html
<!-- Origin positioning -->
<div class="origin-center">Default center</div>
<div class="origin-top">Top</div>
<div class="origin-bottom">Bottom</div>
<div class="origin-left">Left</div>
<div class="origin-right">Right</div>
<div class="origin-top-left">Top-left</div>
<div class="origin-top-right">Top-right</div>
<div class="origin-bottom-left">Bottom-left</div>
<div class="origin-bottom-right">Bottom-right</div>
```

**Responsive**: `sm:origin-top`, `md:origin-bottom-right`
**States**: `hover:origin-left`, `focus:origin-center`

## Transition Utilities

### Transition Property
Enable transitions on specific properties.

```html
<!-- Transition targets -->
<div class="transition">All properties</div>
<div class="transition-none">No transitions</div>
<div class="transition-all">All properties</div>
<div class="transition-colors">Color changes</div>
<div class="transition-opacity">Opacity changes</div>
<div class="transition-transform">Transform changes</div>
<div class="transition-shadow">Shadow changes</div>
```

**Responsive**: `sm:transition-colors`, `md:transition-transform`
**States**: `hover:transition-all`, `focus:transition-opacity`

### Duration
Set the duration of a transition or animation.

```html
<!-- Duration in milliseconds -->
<div class="duration-75">75ms</div>
<div class="duration-100">100ms</div>
<div class="duration-150">150ms</div>
<div class="duration-200">200ms</div>
<div class="duration-300">300ms</div>
<div class="duration-500">500ms</div>
<div class="duration-700">700ms</div>
<div class="duration-1000">1000ms</div>
```

**Responsive**: `sm:duration-200`, `md:duration-500`
**Common**: `hover:duration-300`, `focus:duration-200`

### Timing Function (Easing)
Control the acceleration curve of a transition or animation.

```html
<!-- Easing functions -->
<div class="ease-linear">Linear</div>
<div class="ease-in">Ease in (slow start)</div>
<div class="ease-out">Ease out (slow end)</div>
<div class="ease-in-out">Ease in-out</div>
```

**Responsive**: `sm:ease-in`, `md:ease-out`
**States**: `hover:ease-linear`, `focus:ease-in-out`

### Delay
Add a delay before a transition or animation starts.

```html
<!-- Transition delay in milliseconds -->
<div class="delay-0">0ms</div>
<div class="delay-75">75ms</div>
<div class="delay-100">100ms</div>
<div class="delay-150">150ms</div>
<div class="delay-200">200ms</div>
<div class="delay-300">300ms</div>
<div class="delay-500">500ms</div>
<div class="delay-700">700ms</div>
<div class="delay-1000">1000ms</div>
```

**Responsive**: `sm:delay-150`, `md:delay-300`
**Staggering**: Sequential delays for animations

## Animation Utilities

### Animate
Apply built-in animations or custom @keyframes.

```html
<!-- Built-in animations -->
<div class="animate-none">No animation</div>
<div class="animate-spin">Rotating spinner</div>
<div class="animate-ping">Pulsing beacon</div>
<div class="animate-pulse">Fading pulse</div>
<div class="animate-bounce">Bouncing motion</div>
<div class="animate-wiggle">Wiggle motion</div>
<div class="animate-wave">Wave motion</div>
```

**Responsive**: `sm:animate-spin`, `md:animate-bounce`
**Responsive Disable**: `lg:animate-none`

### Custom Keyframes
Define custom animations with @keyframes.

```css
/* In your CSS or Tailwind config */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideInUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes slideInDown {
  from {
    transform: translateY(-20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes slideInLeft {
  from {
    transform: translateX(-20px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes slideInRight {
  from {
    transform: translateX(20px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes scaleIn {
  from {
    transform: scale(0.9);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}
```

## Combining Transforms, Transitions & Animations

### Example 1: Hover Scale with Transition
```html
<button class="scale-100 hover:scale-110 transition duration-200 ease-out">
  Hover me
</button>
```

### Example 2: Spinning Loader with Animation
```html
<div class="animate-spin">
  <svg class="w-8 h-8"><!-- SVG content --></svg>
</div>
```

### Example 3: Staggered Animation with Delay
```html
<div class="space-y-2">
  <div class="animate-pulse delay-0">Item 1</div>
  <div class="animate-pulse delay-150">Item 2</div>
  <div class="animate-pulse delay-300">Item 3</div>
</div>
```

### Example 4: Complex Transform Combination
```html
<div class="rotate-45 scale-110 translate-x-2 translate-y-4 transition-transform duration-500 ease-in-out">
  Complex transform
</div>
```

### Example 5: Origin-based Scaling
```html
<div class="origin-bottom scale-100 hover:scale-150 transition-transform duration-300">
  Scale from bottom
</div>
```

## Best Practices

1. **Use Duration with Transition**: Always pair `transition-*` with `duration-*`
2. **Add Easing for Smoothness**: Use `ease-out` or `ease-in-out` for natural motion
3. **Mobile First**: Apply base transforms, use responsive variants for larger screens
4. **Performance**: Use `transform` and `opacity` for best performance
5. **Accessibility**: Respect `prefers-reduced-motion` for animations
6. **Combine Operators**: Use state variants like `hover:`, `focus:`, `group-hover:`

## Performance Tips

- Use `transform` instead of `left`/`top` for positioning
- Use `opacity` instead of `visibility` for fade effects
- Prefer `scale` over `width`/`height` changes
- Apply animations only when necessary
- Use `animation-delay` for staggered effects
- Consider `will-change` for heavy animations

## Accessibility Considerations

```css
/* Respect user preferences */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Resources

- [Tailwind CSS Transforms Docs](https://tailwindcss.com/docs/transform)
- [Tailwind CSS Transitions Docs](https://tailwindcss.com/docs/transition-property)
- [Tailwind CSS Animation Docs](https://tailwindcss.com/docs/animation)
- [MDN CSS Transforms](https://developer.mozilla.org/en-US/docs/Web/CSS/transform)
- [MDN CSS Animations](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Animations)
