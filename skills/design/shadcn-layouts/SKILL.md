---
name: shadcn-layouts
description: "Generate correct shadcn/Tailwind layouts by applying CSS mental models. This skill should be used when the user asks to 'create a shadcn layout', 'fix layout issues', 'debug CSS height problems', 'make scrolling work', or has issues with Tailwind flex/grid. Keywords: shadcn, Tailwind, layout, CSS, flex, grid, height, scroll, overflow."
license: MIT
compatibility: Works with shadcn/ui, Tailwind CSS v3/v4, React, Next.js.
metadata:
  author: jwynia
  version: "1.0"
---

# shadcn/Tailwind Layouts

Help generate shadcn/Tailwind components that render correctly the first time. Most agent-generated UI fails due to missing mental models about how CSS layout works—not syntax errors, but assumption gaps.

## When to Use This Skill

Use this skill when:
- Creating shadcn/Tailwind layouts
- Debugging height/scroll issues
- Fixing flex/grid problems
- Setting up full-page app shells

Do NOT use this skill when:
- Writing backend code
- Working on non-Tailwind CSS projects
- Designing (use frontend-design first)

## Core Principle

**CSS layout flows from constraints. Height flows down from explicit ancestors. Width flows up from content. Agents fail because they apply classes without understanding the constraint chain.**

## Critical Mental Models

### Model 1: Height Inheritance Chain

`h-full` means `height: 100%`. 100% of what? **100% of the parent's computed height.**

```
BROKEN (chain incomplete):
<html>                        <!-- no height -->
  <body>                      <!-- no height -->
    <div class="h-full">      <!-- 100% of nothing = 0 -->

WORKING (chain complete):
<html class="h-full">         <!-- 100% of viewport -->
  <body class="h-full">       <!-- 100% of html -->
    <div class="h-full">      <!-- 100% of body = works -->
```

**Rule:** Trace from element up to `<html>`. Every ancestor needs explicit height, OR use viewport units (`h-screen`) to break the chain.

### Model 2: Flex Overflow Gotcha

Flex children have implicit `min-height: auto`, preventing shrinking below content size.

```tsx
// BROKEN (won't scroll)
<div className="flex flex-col h-screen">
  <main className="flex-1 overflow-y-auto">  {/* Can't shrink! */}

// WORKING (scrolls correctly)
<div className="flex flex-col h-screen">
  <main className="flex-1 overflow-y-auto min-h-0">  {/* Can shrink */}
```

**Rule:** Flex children that scroll need `min-h-0`. Children that shouldn't shrink need `shrink-0`.

### Model 3: Grid Parent/Child Separation

Grid is defined on the **parent**. Children just occupy cells.

```tsx
// BROKEN
<div className="grid-cols-3">           {/* Missing 'grid'! */}

// WORKING
<div className="grid grid-cols-3">      {/* 'grid' enables grid-cols-* */}
```

**Rule:** `flex` or `grid` must be declared on parent before direction/template classes work.

### Model 4: Scroll Container Dimensions

Scroll containers need **explicit dimensions** to know when to scroll.

```tsx
// BROKEN (never scrolls)
<ScrollArea>  {/* No height constraint */}

// WORKING (flex-constrained)
<div className="flex flex-col h-screen">
  <ScrollArea className="flex-1 min-h-0">
```

## Diagnostic States

### SL1: Height Chain Broken
**Symptoms:** Elements collapse, `h-full` not working
**Fix:** Trace to html, add heights or use `h-screen`

### SL2: Flex Overflow Blocked
**Symptoms:** Scroll doesn't work, content overflows
**Fix:** Add `min-h-0` to flex children that scroll

### SL3: Grid Structure Wrong
**Symptoms:** Items stack vertically instead of columns
**Fix:** Ensure `grid grid-cols-*` on parent

### SL4: Styles Not Applying
**Symptoms:** Unstyled components, colors wrong
**Fix:** Check Tailwind content paths, CSS variables in globals.css

### SL5: Component Dependencies Missing
**Symptoms:** "Module not found", functionality broken
**Fix:** `npx shadcn add [component]`, install peer deps

## Common Layout Patterns

### Full-Page App Shell

```tsx
// layout.tsx
<html lang="en" className="h-full">
  <body className="h-full">{children}</body>
</html>

// page.tsx
<div className="flex h-full">
  <aside className="w-64 shrink-0 border-r overflow-y-auto">
    <nav>...</nav>
  </aside>
  <main className="flex-1 min-w-0 overflow-y-auto">
    {children}
  </main>
</div>
```

### Dashboard with Header

```tsx
<div className="flex flex-col h-screen">
  <header className="h-16 shrink-0 border-b">...</header>
  <div className="flex flex-1 min-h-0">
    <aside className="w-64 shrink-0 border-r overflow-y-auto">...</aside>
    <main className="flex-1 min-w-0 overflow-y-auto p-6">
      {children}
    </main>
  </div>
</div>
```

### Card Grid

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {items.map(item => (
    <Card key={item.id}>
      <CardHeader><CardTitle>{item.title}</CardTitle></CardHeader>
      <CardContent>{item.content}</CardContent>
    </Card>
  ))}
</div>
```

## Anti-Patterns

### The Height Assumption
Using `h-full` without verifying ancestor chain.
**Fix:** Trace to html. Use `h-screen` to break chain.

### The Overflow Ignorance
Adding `overflow-y-auto` without `min-h-0` on flex children.
**Fix:** Flex children need `min-h-0` to shrink.

### The Import Guess
Guessing import paths like `shadcn/ui`.
**Fix:** Check `components.json` for alias. Usually `@/components/ui/*`.

### The Flat Compound
Flattening compound components (Dialog without DialogTrigger/DialogContent).
**Fix:** Maintain required nesting structure.

## Pre-Generation Checklist

- [ ] Import alias known (`@/components/ui/*`)
- [ ] html has `h-full`
- [ ] body has `h-full` or `min-h-full`
- [ ] Scroll containers have explicit height
- [ ] Flex scroll children have `min-h-0`
- [ ] Fixed elements have `shrink-0`

## Related Skills

- **frontend-design** - Design decisions before implementation
- **react-pwa** - PWA features for React apps
