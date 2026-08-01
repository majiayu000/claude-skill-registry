---
name: handling-animations
description: 'Define animations with @keyframes within @theme directive, use animate-{name}
  utilities, and implement entry animations with starting: variant. Use when creating
  custom animations or entry effects.'
---

---
name: handling-animations
description: Define animations with @keyframes within @theme directive, use animate-{name} utilities, and implement entry animations with starting: variant. Use when creating custom animations or entry effects.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Handling Animations

## Purpose

Define custom animations using `@keyframes` within the `@theme` directive and use Tailwind's animation utilities with full variant support.

## Basic Animation Pattern

Define animations within `@theme`:

```css
@import 'tailwindcss';

@theme {
  --animate-fade-in: fade-in 0.3s ease-out;

  @keyframes fade-in {
    0% {
      opacity: 0;
    }
    100% {
      opacity: 1;
    }
  }
}
```

**Usage:**

```html
<div class="animate-fade-in">Fades in on load</div>
```

## Animation Variable Naming

**Pattern:** `--animate-{name}: {animation-shorthand};`

The variable name determines the utility class:

```css
@theme {
  --animate-spin: spin 1s linear infinite;
  --animate-bounce: bounce 1s infinite;
  --animate-pulse: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
```

Generates utilities:
- `animate-spin`
- `animate-bounce`
- `animate-pulse`

## Common Animation Types

### Fade Animations

**Fade In:**

```css
@theme {
  --animate-fade-in: fade-in 0.3s ease-out;

  @keyframes fade-in {
    0% { opacity: 0; }
    100% { opacity: 1; }
  }
}
```

**Fade In with Scale:**

```css
@theme {
  --animate-fade-in-scale: fade-in-scale 0.3s ease-out;

  @keyframes fade-in-scale {
    0% {
      opacity: 0;
      transform: scale(0.95);
    }
    100% {
      opacity: 1;
      transform: scale(1);
    }
  }
}
```

### Slide Animations

**Slide Up:**

```css
@theme {
  --animate-slide-up: slide-up 0.4s ease-out;

  @keyframes slide-up {
    0% {
      opacity: 0;
      transform: translateY(20px);
    }
    100% {
      opacity: 1;
      transform: translateY(0);
    }
  }
}
```

For complete directional slide examples (left, right, top, bottom), see [Animation Library](references/animation-library.md#slide-in-from-directions).

### Motion Animations

**Spin:**

```css
@theme {
  --animate-spin: spin 1s linear infinite;

  @keyframes spin {
    to { transform: rotate(360deg); }
  }
}
```

**Bounce:**

```css
@theme {
  --animate-bounce: bounce 1s infinite;

  @keyframes bounce {
    0%, 100% {
      transform: translateY(-25%);
      animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
    }
    50% {
      transform: translateY(0);
      animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
    }
  }
}
```

For additional motion animations (pulse, ping, shake, wiggle), see [Animation Library](references/animation-library.md#complete-animation-examples).

## Entry Animations with starting:

The `starting:` variant applies styles before animations begin:

```html
<div class="opacity-100 transition-opacity duration-300 starting:opacity-0">
  Fades in smoothly
</div>

<div class="
  translate-y-0 opacity-100
  transition-all duration-300
  starting:translate-y-4 starting:opacity-0
">
  Slides up while fading in
</div>
```

**How it works:**

1. Element starts with `starting:` styles
2. Browser renders first frame
3. Transition/animation begins to final state

## Animation with Variants

Animations work with all Tailwind variants:

```html
<div class="hover:animate-spin">Spins on hover</div>
<div class="focus:animate-pulse">Pulses on focus</div>
<div class="group-hover:animate-bounce">Bounces when parent hovered</div>
<div class="lg:animate-fade-in">Animates on large screens</div>
<div class="dark:animate-pulse">Pulses in dark mode</div>
```

## Advanced Animation Techniques

### Staggered Animations

```html
<div class="space-y-4">
  <div class="animate-slide-up [animation-delay:0s]">Item 1</div>
  <div class="animate-slide-up [animation-delay:0.1s]">Item 2</div>
  <div class="animate-slide-up [animation-delay:0.2s]">Item 3</div>
  <div class="animate-slide-up [animation-delay:0.3s]">Item 4</div>
</div>
```

### Animation Control

**Delayed Animation:**

```html
<div class="
  animate-fade-in
  [animation-delay:0.1s]
  [animation-fill-mode:both]
">
  Delayed fade in
</div>
```

**Pause on Hover:**

```html
<div class="animate-spin hover:[animation-play-state:paused]">
  Pauses on hover
</div>
```

## Best Practices

1. **Define within @theme** - Keep all animations in one place
2. **Use semantic names** - `fade-in` not `anim-1`
3. **Include timing in variable** - Full animation shorthand
4. **Test performance** - Avoid animating expensive properties (width, height)
5. **Use transform and opacity** - Hardware accelerated
6. **Add will-change sparingly** - Only for known animations
7. **Respect prefers-reduced-motion** - Disable animations for accessibility

## Accessibility

Respect user motion preferences:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## References

For comprehensive animation examples and patterns, see:

- [Animation Library](references/animation-library.md) - Complete collection of animation examples
  - Fade animations (in, out, scale)
  - Slide animations (all directions)
  - Motion animations (spin, pulse, ping, bounce)
  - Complex patterns (shake, wiggle, loading dots)
  - Complete animation library code
  - Advanced techniques and performance considerations

## See Also

- RESEARCH.md sections: "Entry Animations with starting:" and "Animation Keyframes"
