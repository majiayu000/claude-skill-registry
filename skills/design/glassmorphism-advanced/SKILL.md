---
name: glassmorphism-advanced
description: Advanced glassmorphism techniques with blur, layering, colored shadows, and depth. Use when creating frosted glass effects, transparent overlays, or modern glass UI.
allowed-tools: Read, Write, Edit, Glob, Grep
user-invocable: true
---

# Glassmorphism Advanced

Modern glass UI effects inspired by DesignCode UI.

## Agent Workflow (MANDATORY)

Before implementation:
1. **fuse-ai-pilot:explore-codebase** - Check existing glass patterns
2. **fuse-ai-pilot:research-expert** - Latest backdrop-filter support

After: Run **fuse-ai-pilot:sniper** for validation.

## Core Technique

```tsx
/* Base glassmorphism */
className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-2xl"

/* With colored shadow */
className="bg-white/10 backdrop-blur-xl border border-white/20
           shadow-xl shadow-primary/10"
```

## Blur Levels

| Level | Class | Use Case |
|-------|-------|----------|
| Subtle | `backdrop-blur-sm` | Overlays on clean backgrounds |
| Medium | `backdrop-blur-md` | Cards, modals |
| Strong | `backdrop-blur-xl` | Primary surfaces |
| Maximum | `backdrop-blur-3xl` | Hero sections |

## Opacity Layers (DesignCode Pattern)

```tsx
/* Light mode */
<div className="bg-white/80 backdrop-blur-xl">

/* Dark mode */
<div className="bg-black/40 backdrop-blur-xl">

/* Adaptive (CSS variables) */
<div className="bg-[var(--glass-bg)] backdrop-blur-xl">
```

## Layered Glass Stack

```tsx
/* Multiple glass layers for depth */
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

## Colored Glass

```tsx
/* Primary tinted glass */
className="bg-primary/10 backdrop-blur-xl border border-primary/20"

/* Accent glow */
className="bg-accent/5 backdrop-blur-xl shadow-lg shadow-accent/20"
```

## Border Techniques

```tsx
/* Subtle inner glow */
className="border border-white/20"

/* Gradient border (pseudo-element) */
className="relative before:absolute before:inset-0 before:rounded-2xl
           before:p-px before:bg-gradient-to-b before:from-white/30 before:to-transparent"
```

## Critical Rules

| NEVER | ALWAYS |
|-------|--------|
| Flat backgrounds | Add backdrop-blur |
| Hard borders | Use /20 opacity borders |
| No shadow | Add shadow-*/10 |
| Static glass | Animate opacity on hover |

## Validation

```
[ ] backdrop-blur-* present
[ ] Semi-transparent background (bg-*/opacity)
[ ] Subtle border (border-white/20)
[ ] Works on gradient backgrounds
[ ] Dark mode variant defined
```

## References

- `../../references/theme-presets.md` - Glassmorphism preset
- `../../references/ui-visual-design.md` - Depth and layering
