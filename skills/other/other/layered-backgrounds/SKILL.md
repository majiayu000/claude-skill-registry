---
name: layered-backgrounds
description: Use when creating hero sections, landing pages, or premium visual effects. Covers gradient orbs, blur layers, noise textures.
versions:
  tailwindcss: "4.1"
  framer-motion: "11"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
related-skills: glassmorphism-advanced, generating-components
---

# Layered Backgrounds

## Agent Workflow (MANDATORY)

Before implementation, use `TeamCreate` to spawn 3 agents:

1. **fuse-ai-pilot:explore-codebase** - Check existing background patterns
2. **fuse-ai-pilot:research-expert** - CSS filter and blend modes

After: Run **fuse-ai-pilot:sniper** for validation.

---

## Overview

| Layer | Z-Index | Purpose |
|-------|---------|---------|
| Content | z-10 | UI elements |
| Noise | z-5 | Grain texture |
| Glass | z-0 | Surface |
| Orbs | z-[-1] | Color blobs |
| Base | z-[-2] | Gradient |

---

## Quick Reference

### Gradient Orbs

```tsx
<div className="absolute inset-0 -z-10 overflow-hidden">
  <div className="absolute -top-1/4 -left-1/4 w-[600px] h-[600px]
                  bg-primary/30 rounded-full blur-3xl" />
  <div className="absolute -bottom-1/4 -right-1/4 w-[500px] h-[500px]
                  bg-accent/20 rounded-full blur-3xl" />
</div>
```

### Animated Orbs

```tsx
<motion.div
  className="absolute w-[600px] h-[600px] bg-primary/30 rounded-full blur-3xl"
  animate={{ x: [0, 100, 0], y: [0, -50, 0] }}
  transition={{ duration: 20, repeat: Infinity, ease: "easeInOut" }}
/>
```

### Noise Overlay

```tsx
<div
  className="absolute inset-0 opacity-[0.03] pointer-events-none"
  style={{
    backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")`,
  }}
/>
```

### Complete Hero Background

```tsx
function HeroBackground() {
  return (
    <>
      <div className="absolute inset-0 -z-20 bg-gradient-to-b from-background to-muted" />
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <div className="absolute -top-1/4 -left-1/4 w-[600px] h-[600px] bg-primary/20 rounded-full blur-3xl" />
        <div className="absolute -bottom-1/4 -right-1/4 w-[500px] h-[500px] bg-accent/15 rounded-full blur-3xl" />
      </div>
      <div className="absolute inset-0 bg-[url('/noise.png')] opacity-[0.02] mix-blend-overlay" />
    </>
  );
}
```

### Dark Mode

```tsx
<div className="bg-primary/20 dark:bg-primary/30 blur-3xl" />
```

---

## Validation Checklist

```
[ ] Multiple layers with z-index separation
[ ] Gradient orbs with blur (blur-2xl or blur-3xl)
[ ] Colors from CSS variables
[ ] Overflow hidden on container
[ ] Dark mode variant defined
```

---

## Best Practices

### DO
- Use CSS variables for colors
- Add overflow-hidden to container
- Use will-change for animated orbs
- Reduce blur on mobile

### DON'T
- Hard-code colors
- Forget overflow control
- Skip dark mode
- Use too many orbs (max 3)
