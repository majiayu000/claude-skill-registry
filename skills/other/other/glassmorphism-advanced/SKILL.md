---
name: glassmorphism-advanced
description: Use when creating frosted glass effects, transparent overlays, or modern glass UI. Covers blur, layering, colored shadows.
versions:
  tailwindcss: "4.1"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
related-skills: designing-systems, generating-components
---

# Glassmorphism Advanced

## Agent Workflow (MANDATORY)

Before implementation, use `TeamCreate` to spawn 3 agents:

1. **fuse-ai-pilot:explore-codebase** - Check existing glass patterns
2. **fuse-ai-pilot:research-expert** - Latest backdrop-filter support

After: Run **fuse-ai-pilot:sniper** for validation.

---

## Overview

| Feature | Description |
|---------|-------------|
| **Blur Levels** | sm, md, xl, 3xl |
| **Opacity Layers** | Multiple glass layers for depth |
| **Colored Glass** | Tinted with CSS variables |
| **Borders** | Subtle white/20 borders |

---

## Critical Rules

1. **backdrop-blur required** - No flat backgrounds
2. **Semi-transparent bg** - Use bg-white/10, bg-black/40
3. **Subtle borders** - border-white/20
4. **Shadow for depth** - shadow-xl shadow-primary/10
5. **Dark mode variant** - Always define both

---

## Quick Reference

### Base Glassmorphism

```tsx
className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-2xl"
```

### With Colored Shadow

```tsx
className="bg-white/10 backdrop-blur-xl border border-white/20 shadow-xl shadow-primary/10"
```

### Blur Levels

| Level | Class | Use Case |
|-------|-------|----------|
| Subtle | `backdrop-blur-sm` | Overlays on clean backgrounds |
| Medium | `backdrop-blur-md` | Cards, modals |
| Strong | `backdrop-blur-xl` | Primary surfaces |
| Maximum | `backdrop-blur-3xl` | Hero sections |

### Layered Glass Stack

```tsx
<div className="relative">
  {/* Background layer - most blur */}
  <div className="absolute inset-0 bg-white/5 backdrop-blur-3xl rounded-3xl" />

  {/* Middle layer */}
  <div className="absolute inset-2 bg-white/10 backdrop-blur-xl rounded-2xl" />

  {/* Content layer - least blur */}
  <div className="relative bg-white/20 backdrop-blur-md rounded-xl p-6">
    {children}
  </div>
</div>
```

### Dark Mode

```tsx
/* Light mode */
className="bg-white/80 backdrop-blur-xl"

/* Dark mode */
className="dark:bg-black/40 dark:backdrop-blur-xl"
```

---

## Validation Checklist

```
[ ] backdrop-blur-* present
[ ] Semi-transparent background (bg-*/opacity)
[ ] Subtle border (border-white/20)
[ ] Works on gradient backgrounds
[ ] Dark mode variant defined
```

---

## Best Practices

### DO
- Use multiple blur layers for depth
- Add colored shadows for vibrancy
- Define dark mode variants
- Use CSS variables for glass-bg

### DON'T
- Use flat backgrounds
- Hard borders (use /20 opacity)
- Skip shadow effects
- Forget dark mode
