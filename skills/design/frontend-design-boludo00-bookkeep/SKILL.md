---
name: frontend-design
description: |
  Creates distinctive, production-grade frontend interfaces for Bookkeep using the cinematic dark theme with jewel-tone accents.
  Use when: Building new components, pages, or features that need to match the established visual language.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, mcp__plugin_playwright_playwright__browser_snapshot, mcp__plugin_playwright_playwright__browser_take_screenshot, mcp__plugin_playwright_playwright__browser_navigate
---

# Frontend Design Skill

Bookkeep uses a **cinematic dark theme** with jewel-tone accents (emerald primary, amber accent) and extensive glassmorphism. The design prioritizes book covers as hero elements with reflection effects, glow states, and lazy-loaded imagery.

## Quick Start

### Card with Glassmorphism

```tsx
<div className="glass rounded-xl p-6 space-y-4">
  <h3 className="text-lg font-semibold tracking-tight">Section Title</h3>
  <p className="text-sm text-muted-foreground">Description text</p>
</div>
```

### Status Badge

```tsx
<span className="status-approved inline-flex items-center gap-1.5 px-2.5 py-1 text-xs font-medium rounded-full border">
  <CheckCircle className="h-3 w-3" />
  Approved
</span>
```

### Interactive Card

```tsx
<div className="group card-hover rounded-xl border border-border/50 bg-card/50 p-4 cursor-pointer">
  <div className="transition-transform duration-300 group-hover:translate-x-1">
    Content slides on hover
  </div>
</div>
```

## Key Concepts

| Concept | Class | Usage |
|---------|-------|-------|
| Glass effect | `glass`, `glass-subtle`, `glass-strong` | Layered surfaces |
| Book cover | `book-cover`, `book-cover-glow` | Hero imagery |
| Card lift | `card-lift` | Elevated hover state |
| Status colors | `status-{state}` | Semantic badges |
| Gradient text | `text-gradient-emerald` | Accent headings |

## Common Patterns

### Page Header with Ambient Glow

```tsx
<div className="relative mb-8">
  <div className="absolute -top-20 -left-20 w-64 h-64 bg-primary/10 rounded-full blur-3xl" />
  <h1 className="text-3xl font-bold tracking-tight">Page Title</h1>
  <p className="text-muted-foreground mt-2">Subtitle description</p>
</div>
```

### Form Input with Focus Ring

```tsx
<Input
  className="bg-card/50 border-border/50 focus:bg-card focus:border-primary/30 
             transition-all duration-300 rounded-xl h-11"
  placeholder="Search..."
/>
```

## Design Tokens

| Token | Value | Usage |
|-------|-------|-------|
| Primary | `hsl(158 64% 42%)` | CTAs, active states |
| Accent | `hsl(38 92% 55%)` | Warnings, highlights |
| Background | `hsl(220 20% 4%)` | Page bg |
| Radius | `0.75rem` | All corners |
| Transition | `300ms ease-out` | Default timing |

## See Also

- [aesthetics](references/aesthetics.md) - Color, typography, visual identity
- [components](references/components.md) - UI component patterns
- [layouts](references/layouts.md) - Page structure and grids
- [motion](references/motion.md) - Animation and transitions
- [patterns](references/patterns.md) - DO/DON'T guidance

## Related Skills

- See the **tailwind** skill for utility classes and theme configuration
- See the **react** skill for component architecture and hooks
- See the **shadcn-ui** skill for primitive component usage