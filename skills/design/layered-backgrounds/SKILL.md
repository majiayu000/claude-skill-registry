---
name: layered-backgrounds
description: Layered background effects with gradient orbs, blur layers, noise textures, and depth. Use when creating hero sections, landing pages, or premium visual effects.
allowed-tools: Read, Write, Edit, Glob, Grep
user-invocable: true
---

# Layered Backgrounds

Premium background effects inspired by DesignCode UI.

## Agent Workflow (MANDATORY)

Before implementation:
1. **fuse-ai-pilot:explore-codebase** - Check existing background patterns
2. **fuse-ai-pilot:research-expert** - CSS filter and blend modes

After: Run **fuse-ai-pilot:sniper** for validation.

## Layer Stack

```
┌─────────────────────────────────────┐
│ Content (z-10)                      │
├─────────────────────────────────────┤
│ Noise/Grain overlay (z-5)           │
├─────────────────────────────────────┤
│ Glass surface (z-0)                 │
├─────────────────────────────────────┤
│ Gradient orbs (z-[-1])              │
├─────────────────────────────────────┤
│ Base gradient (z-[-2])              │
└─────────────────────────────────────┘
```

## Gradient Orbs

```tsx
function GradientBackground() {
  return (
    <div className="absolute inset-0 -z-10 overflow-hidden">
      {/* Primary orb - top left */}
      <div
        className="absolute -top-1/4 -left-1/4 w-[600px] h-[600px]
                   bg-primary/30 rounded-full blur-3xl"
      />

      {/* Accent orb - bottom right */}
      <div
        className="absolute -bottom-1/4 -right-1/4 w-[500px] h-[500px]
                   bg-accent/20 rounded-full blur-3xl"
      />

      {/* Secondary orb - center */}
      <div
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2
                   w-[400px] h-[400px] bg-secondary/15 rounded-full blur-2xl"
      />
    </div>
  );
}
```

## Animated Orbs

```tsx
import { motion } from "framer-motion";

function AnimatedBackground() {
  return (
    <div className="absolute inset-0 -z-10 overflow-hidden">
      <motion.div
        className="absolute w-[600px] h-[600px] bg-primary/30 rounded-full blur-3xl"
        animate={{
          x: [0, 100, 0],
          y: [0, -50, 0],
        }}
        transition={{
          duration: 20,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        style={{ top: "-25%", left: "-15%" }}
      />

      <motion.div
        className="absolute w-[500px] h-[500px] bg-accent/20 rounded-full blur-3xl"
        animate={{
          x: [0, -80, 0],
          y: [0, 60, 0],
        }}
        transition={{
          duration: 25,
          repeat: Infinity,
          ease: "easeInOut",
        }}
        style={{ bottom: "-20%", right: "-10%" }}
      />
    </div>
  );
}
```

## Noise/Grain Texture

```tsx
/* CSS noise overlay */
function NoiseOverlay() {
  return (
    <div
      className="absolute inset-0 z-5 opacity-[0.03] pointer-events-none"
      style={{
        backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")`,
      }}
    />
  );
}

/* Tailwind approach */
<div className="absolute inset-0 bg-[url('/noise.png')] opacity-5 mix-blend-overlay" />
```

## Mesh Gradient

```tsx
function MeshBackground() {
  return (
    <div
      className="absolute inset-0 -z-10"
      style={{
        background: `
          radial-gradient(at 40% 20%, var(--color-primary) 0px, transparent 50%),
          radial-gradient(at 80% 0%, var(--color-accent) 0px, transparent 50%),
          radial-gradient(at 0% 50%, var(--color-secondary) 0px, transparent 50%),
          radial-gradient(at 80% 100%, var(--color-primary) 0px, transparent 50%),
          radial-gradient(at 0% 100%, var(--color-accent) 0px, transparent 50%)
        `,
        opacity: 0.3,
      }}
    />
  );
}
```

## Complete Hero Background

```tsx
function HeroBackground() {
  return (
    <>
      {/* Base gradient */}
      <div className="absolute inset-0 -z-20 bg-gradient-to-b from-background via-background to-muted" />

      {/* Gradient orbs */}
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <div className="absolute -top-1/4 -left-1/4 w-[600px] h-[600px] bg-primary/20 rounded-full blur-3xl" />
        <div className="absolute -bottom-1/4 -right-1/4 w-[500px] h-[500px] bg-accent/15 rounded-full blur-3xl" />
      </div>

      {/* Grid pattern */}
      <div
        className="absolute inset-0 -z-5 opacity-[0.02]"
        style={{
          backgroundImage: `linear-gradient(var(--color-foreground) 1px, transparent 1px),
                           linear-gradient(90deg, var(--color-foreground) 1px, transparent 1px)`,
          backgroundSize: "64px 64px",
        }}
      />

      {/* Noise overlay */}
      <div className="absolute inset-0 bg-[url('/noise.png')] opacity-[0.02] mix-blend-overlay" />
    </>
  );
}
```

## Dark Mode Backgrounds

```tsx
/* Light mode */
<div className="bg-gradient-to-b from-white via-gray-50 to-gray-100" />

/* Dark mode */
<div className="dark:bg-gradient-to-b dark:from-gray-950 dark:via-gray-900 dark:to-gray-950" />

/* Orbs in dark mode - more vibrant */
<div className="bg-primary/20 dark:bg-primary/30 blur-3xl" />
```

## Performance Tips

```tsx
/* Use will-change for animated orbs */
className="will-change-transform"

/* Reduce blur on mobile */
className="blur-2xl md:blur-3xl"

/* Use CSS containment */
style={{ contain: "paint" }}
```

## Validation

```
[ ] Multiple layers with z-index separation
[ ] Gradient orbs with blur (blur-2xl or blur-3xl)
[ ] Colors from CSS variables
[ ] Overflow hidden on container
[ ] Mobile performance considered
[ ] Dark mode variant defined
```

## References

- `../../references/gradients-guide.md` - Gradient types
- `../../references/theme-presets.md` - Visual styles
- `../../skills/glassmorphism-advanced/SKILL.md` - Glass effects
