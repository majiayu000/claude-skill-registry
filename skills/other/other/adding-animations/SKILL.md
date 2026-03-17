---
name: adding-animations
description: Use when adding animations, transitions, hover effects, or motion design. MANDATORY for every component. Covers Framer Motion patterns.
versions:
  framer-motion: "11"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Task
references: references/motion-patterns.md, references/buttons-guide.md, references/cards-guide.md, references/ui-visual-design.md, references/patterns-cards.md, references/patterns-buttons.md, references/patterns-navigation.md, references/patterns-microinteractions.md
related-skills: generating-components, interactive-states
---

# Adding Animations (MANDATORY)

## Agent Workflow (MANDATORY)

Before ANY animation work, use `TeamCreate` to spawn 3 agents:

1. **fuse-ai-pilot:explore-codebase** - Find existing Framer Motion patterns
2. **fuse-ai-pilot:research-expert** - Verify latest Framer Motion v11 API
3. Check existing animation timing conventions

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

| Feature | Description |
|---------|-------------|
| **Framer Motion** | Animation library (REQUIRED) |
| **Stagger** | List/grid reveal patterns |
| **Hover/Tap** | Interactive micro-animations |
| **Accessibility** | prefers-reduced-motion support |

---

## Critical Rules

1. **Every component needs animation** - No static components
2. **Stagger on lists** - Container + item variants
3. **Hover on interactive** - Buttons, cards, links
4. **Respect reduced motion** - useReducedMotion hook
5. **Match existing patterns** - Analyze codebase first

---

## Timing Guidelines

| Interaction | Duration | Easing |
|-------------|----------|--------|
| Hover | 50-100ms | ease-out |
| Button press | 100-150ms | ease-out |
| Modal open | 200-300ms | ease-out |
| Page transition | 300-400ms | ease-in-out |

---

## Reference Guide

### Concepts

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Motion Patterns** | [motion-patterns.md](references/motion-patterns.md) | Framer Motion examples |
| **Buttons** | [buttons-guide.md](references/buttons-guide.md) | Hover/press timing |
| **Cards** | [cards-guide.md](references/cards-guide.md) | Card hover effects |
| **UI Design** | [ui-visual-design.md](references/ui-visual-design.md) | Micro-interactions |
| **Card Patterns** | [patterns-cards.md](references/patterns-cards.md) | Card animations |
| **Button Patterns** | [patterns-buttons.md](references/patterns-buttons.md) | Button animations |
| **Navigation** | [patterns-navigation.md](references/patterns-navigation.md) | Nav animations |
| **Micro-interactions** | [patterns-microinteractions.md](references/patterns-microinteractions.md) | Small details |

---

## Quick Reference

### Container + Stagger

```tsx
const container = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.1 } }
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
};

<motion.div variants={container} initial="hidden" animate="show">
  <motion.div variants={item}>Item 1</motion.div>
  <motion.div variants={item}>Item 2</motion.div>
</motion.div>
```

### Hover Effects

```tsx
// Card hover
<motion.div whileHover={{ y: -4 }} transition={{ duration: 0.2 }}>

// Button hover
<motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
```

### Scroll Animation

```tsx
<motion.div
  initial={{ opacity: 0, y: 40 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, margin: "-100px" }}
/>
```

### Reduced Motion

```tsx
import { useReducedMotion } from "framer-motion";

const shouldReduce = useReducedMotion();
<motion.div
  animate={shouldReduce ? {} : { y: 0 }}
  transition={shouldReduce ? { duration: 0 } : { duration: 0.3 }}
/>
```

→ See [motion-patterns.md](references/motion-patterns.md) for complete patterns

---

## FORBIDDEN

```tsx
// ❌ Random bouncing loops
animate={{ y: [0, -10, 0] }}
transition={{ repeat: Infinity }}

// ❌ Excessive effects
whileHover={{ scale: 1.2, rotate: 5 }}

// ❌ Slow animations
transition={{ duration: 1.5 }}
```

---

## Best Practices

### DO
- Use container + item variants for lists
- Add hover to all interactive elements
- Respect prefers-reduced-motion
- Keep animations under 400ms
- Match existing timing patterns

### DON'T
- Create static components without animation
- Use infinite looping animations
- Make animations too slow (>400ms)
- Forget accessibility considerations
- Mix animation libraries (stick to Framer)
