---
name: responsive-system
description: Responsive design system with breakpoints, container queries, and fluid typography. Use when implementing responsive layouts, mobile-first design, or adaptive components.
allowed-tools: Read, Write, Edit, Glob, Grep
user-invocable: true
---

# Responsive System

Breakpoint system inspired by DesignCode UI (720/920/1200px).

## Agent Workflow (MANDATORY)

Before implementation:
1. **fuse-ai-pilot:explore-codebase** - Check existing breakpoints
2. **fuse-ai-pilot:research-expert** - Container queries support

After: Run **fuse-ai-pilot:sniper** for validation.

## Breakpoint Scale

| Name | Width | Tailwind | Use Case |
|------|-------|----------|----------|
| xs | 0-479px | default | Mobile portrait |
| sm | 480-719px | `sm:` | Mobile landscape |
| md | 720-919px | `md:` | Tablet portrait |
| lg | 920-1199px | `lg:` | Tablet landscape |
| xl | 1200-1439px | `xl:` | Desktop |
| 2xl | 1440px+ | `2xl:` | Large desktop |

## Tailwind v4 Configuration

```css
/* app.css */
@import "tailwindcss";

@theme {
  --breakpoint-sm: 480px;
  --breakpoint-md: 720px;
  --breakpoint-lg: 920px;
  --breakpoint-xl: 1200px;
  --breakpoint-2xl: 1440px;
}
```

## Mobile-First Pattern

```tsx
/* Start mobile, enhance upward */
<div className="
  grid grid-cols-1      /* mobile: 1 column */
  sm:grid-cols-2        /* sm: 2 columns */
  lg:grid-cols-3        /* lg: 3 columns */
  xl:grid-cols-4        /* xl: 4 columns */
  gap-4 sm:gap-6 lg:gap-8
">
```

## Container Queries (Modern)

```tsx
/* Parent container */
<div className="@container">
  {/* Child responds to parent, not viewport */}
  <div className="@md:flex @md:gap-4">
    <div className="@md:w-1/2">Left</div>
    <div className="@md:w-1/2">Right</div>
  </div>
</div>
```

## Container Query Breakpoints

```css
@theme {
  --container-3xs: 8rem;   /* 128px */
  --container-2xs: 12rem;  /* 192px */
  --container-xs: 16rem;   /* 256px */
  --container-sm: 20rem;   /* 320px */
  --container-md: 28rem;   /* 448px */
  --container-lg: 32rem;   /* 512px */
  --container-xl: 36rem;   /* 576px */
}
```

## Fluid Typography

```css
/* Clamp for smooth scaling */
.hero-title {
  font-size: clamp(2rem, 5vw + 1rem, 4rem);
  line-height: 1.1;
}

/* Tailwind approach */
className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl xl:text-6xl"
```

## Responsive Spacing

```tsx
/* Padding scales with viewport */
<section className="px-4 sm:px-6 md:px-8 lg:px-12 xl:px-16">

/* Using max-width container */
<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
```

## Hide/Show Pattern

```tsx
/* Mobile-only */
<div className="block sm:hidden">Mobile nav</div>

/* Desktop-only */
<div className="hidden lg:block">Desktop sidebar</div>

/* Tablet+ */
<div className="hidden md:flex">Tablet and up</div>
```

## Responsive Grid Templates

```tsx
/* Dashboard layout */
<div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
  {/* Sidebar - full width on mobile */}
  <aside className="lg:col-span-3 xl:col-span-2">
    Sidebar
  </aside>

  {/* Main content */}
  <main className="lg:col-span-9 xl:col-span-10">
    Content
  </main>
</div>
```

## Card Grid Responsive

```tsx
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
  {cards.map(card => <Card key={card.id} {...card} />)}
</div>
```

## Validation

```
[ ] Mobile-first approach (start smallest)
[ ] Breakpoints at 720/920/1200 (or project standard)
[ ] Container queries for complex layouts
[ ] Fluid typography with clamp()
[ ] Touch targets 44x44px on mobile
[ ] No horizontal scroll on mobile
```

## References

- `../../references/grids-layout.md` - 12-column grid
- `../../references/tailwind-best-practices.md` - Tailwind v4
