---
name: generating-components
description: Generate production-ready React components using shadcn/ui, 21st.dev, and Tailwind CSS. Use when user asks for UI components, buttons, forms, cards, hero sections, or mentions design inspiration.
allowed-tools: Read, Write, Edit, Glob, Grep, Task, mcp__magic__21st_magic_component_builder, mcp__magic__21st_magic_component_inspiration, mcp__magic__21st_magic_component_refiner, mcp__shadcn__search_items_in_registries, mcp__shadcn__view_items_in_registries, mcp__shadcn__get_item_examples_from_registries, mcp__shadcn__get_add_command_for_items
user-invocable: true
---

# Generating Components

## APEX WORKFLOW (MANDATORY)

### Phase A: ANALYZE

```
Task: explore-codebase
Prompt: "Analyze UI: components, colors, typography, spacing, animations"
```

### Phase A: SEARCH INSPIRATION

```typescript
// 21st.dev (MANDATORY FIRST)
mcp__magic__21st_magic_component_inspiration({
  message: "Create a hero section",
  searchQuery: "hero section glassmorphism"
})

// shadcn/ui
mcp__shadcn__search_items_in_registries({
  registries: ["@shadcn"],
  query: "button"
})
```

### Phase P: PLAN

TodoWrite with file breakdown (<100 lines each):
- `components/ui/HeroSection.tsx` (~60 lines)
- `components/ui/HeroBackground.tsx` (~30 lines)

### Phase E: CODE

Write component using:
- Design tokens from Phase A
- Inspiration from 21st.dev/shadcn
- Framer Motion animations
- WCAG 2.2 AA compliance

### Phase X: VALIDATE

```
Task: sniper
Prompt: "Validate component: lint, accessibility, design consistency"
```

## ANTI-AI SLOP (MANDATORY)

| FORBIDDEN | USE INSTEAD |
|-----------|-------------|
| Roboto, Arial, system default | Inter, Clash Display, Satoshi, Syne |
| Purple/pink gradients | CSS variables, sharp accents |
| Border-left indicators | Icon + bg-*/10 rounded |
| Flat backgrounds | Glassmorphism, gradient orbs |
| No animations | Framer Motion stagger |

**See:** `../../references/typography.md`, `../../references/color-system.md`

## Component Template

```tsx
"use client";
import { motion } from "framer-motion";

const variants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { staggerChildren: 0.1 } }
};

export function Component({ className }: { className?: string }) {
  return (
    <motion.div variants={variants} initial="hidden" animate="show">
      {/* Background from existing design tokens */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-3xl" />
      </div>
      {/* Content */}
    </motion.div>
  );
}
```

## Validation

```
[ ] Phase 0 completed (analyze existing)
[ ] Inspiration searched (21st.dev, shadcn)
[ ] Matches existing design tokens
[ ] No AI slop patterns
[ ] Framer Motion animations
[ ] Files < 100 lines
```

## References

- **UI Visual Design**: `../../references/ui-visual-design.md` (visual hierarchy, spacing, 2026 trends)
- **UX Principles**: `../../references/ux-principles.md` (Nielsen heuristics, Laws of UX, cognitive psychology)
- **Typography**: `../../references/typography.md` (fonts, sizes, line-height, mobile guidelines)
- **Colors**: `../../references/color-system.md` (psychology, palettes, OKLCH, 60-30-10)
- **Buttons**: `../../references/buttons-guide.md` (states, sizing, accessibility)
- **Forms**: `../../references/forms-guide.md` (validation, layout, states)
- **Icons**: `../../references/icons-guide.md` (types, consistency, scalability)
- **Grids & Layout**: `../../references/grids-layout.md` (12-column, responsive, containers)
- **Motion**: `../../references/motion-patterns.md`
- **Design Patterns**: `../../references/design-patterns.md`
- **21st.dev Guide**: `../../references/21st-dev.md`
