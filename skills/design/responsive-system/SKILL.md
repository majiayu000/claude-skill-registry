---
name: responsive-system
description: Use when implementing responsive layouts, mobile-first design, or adaptive components. Covers breakpoints, container queries, fluid typography.
versions:
  tailwindcss: "4.1"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
related-skills: designing-systems, generating-components
---

# Responsive System

## Agent Workflow (MANDATORY)

Before implementation, use `TeamCreate` to spawn 3 agents:

1. **fuse-ai-pilot:explore-codebase** - Check existing breakpoints
2. **fuse-ai-pilot:research-expert** - Container queries support

After: Run **fuse-ai-pilot:sniper** for validation.

---

## Overview

| Name | Width | Tailwind | Use Case |
|------|-------|----------|----------|
| xs | 0-479px | default | Mobile portrait |
| sm | 480-719px | `sm:` | Mobile landscape |
| md | 720-919px | `md:` | Tablet portrait |
| lg | 920-1199px | `lg:` | Tablet landscape |
| xl | 1200px+ | `xl:` | Desktop |

---

## Quick Reference

### Mobile-First Pattern

```tsx
<div className="
  grid grid-cols-1      /* mobile: 1 column */
  sm:grid-cols-2        /* sm: 2 columns */
  lg:grid-cols-3        /* lg: 3 columns */
  gap-4 sm:gap-6 lg:gap-8
">
```

### Container Queries

```tsx
<div className="@container">
  <div className="@md:flex @md:gap-4">
    <div className="@md:w-1/2">Left</div>
    <div className="@md:w-1/2">Right</div>
  </div>
</div>
```

### Fluid Typography

```css
.hero-title {
  font-size: clamp(2rem, 5vw + 1rem, 4rem);
}
```

### Hide/Show Pattern

```tsx
<div className="block sm:hidden">Mobile only</div>
<div className="hidden lg:block">Desktop only</div>
```

### Tailwind v4 Config

```css
@theme {
  --breakpoint-sm: 480px;
  --breakpoint-md: 720px;
  --breakpoint-lg: 920px;
  --breakpoint-xl: 1200px;
}
```

---

## Validation Checklist

```
[ ] Mobile-first approach (start smallest)
[ ] Container queries for complex layouts
[ ] Fluid typography with clamp()
[ ] Touch targets 44x44px on mobile
[ ] No horizontal scroll on mobile
```

---

## Best Practices

### DO
- Start mobile, enhance upward
- Use container queries for components
- Use clamp() for fluid sizing
- Test on real devices

### DON'T
- Desktop-first (hard to maintain)
- Fixed breakpoints for everything
- Ignore touch targets
- Skip mobile testing
