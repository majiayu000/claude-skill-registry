---
name: generating-components
description: Use when generating UI components, buttons, forms, cards, hero sections, or using design tools. Covers Gemini Design MCP, shadcn/ui, 21st.dev, and Tailwind CSS.
versions:
  tailwindcss: "4.1"
  framer-motion: "11"
  shadcn-ui: "2.x"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Task, mcp__gemini-design__create_frontend, mcp__gemini-design__snippet_frontend, mcp__gemini-design__modify_frontend, mcp__magic__21st_magic_component_builder, mcp__magic__21st_magic_component_inspiration, mcp__magic__21st_magic_component_refiner, mcp__shadcn__search_items_in_registries, mcp__shadcn__view_items_in_registries, mcp__shadcn__get_item_examples_from_registries, mcp__shadcn__get_add_command_for_items
references: references/gemini-design-workflow.md, references/21st-dev.md, references/shadcn.md, references/buttons-guide.md, references/forms-guide.md, references/cards-guide.md, references/icons-guide.md, references/ui-visual-design.md, references/grids-layout.md, references/design-patterns.md, references/component-examples.md, references/templates/hero-section.md, references/templates/feature-grid.md, references/templates/pricing-card.md, references/templates/contact-form.md, references/templates/testimonial-card.md, references/templates/stats-section.md, references/templates/faq-accordion.md, references/templates/hero-glassmorphism.md, references/templates/pricing-cards.md
related-skills: designing-systems, adding-animations, validating-accessibility
---

# Generating Components

## Agent Workflow (MANDATORY)

Before ANY component generation, use `TeamCreate` to spawn 3 agents:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing UI patterns, colors, typography
2. **fuse-ai-pilot:research-expert** - Verify latest component patterns via Context7
3. **mcp__magic__21st_magic_component_inspiration** - Search 21st.dev for inspiration

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

| Feature | Description |
|---------|-------------|
| **Gemini Design MCP** | AI-powered frontend generation (create, modify, snippet) |
| **21st.dev** | Component inspiration and builder |
| **shadcn/ui** | Copy-paste component library |
| **Anti-AI-Slop** | Mandatory rules against generic designs |

---

## Critical Rules

1. **ALWAYS use Gemini Design** - Never write UI code manually
2. **Search inspiration first** - 21st.dev before coding
3. **Match existing tokens** - Analyze codebase before generating
4. **No forbidden fonts** - Inter, Roboto, Arial are BANNED
5. **Framer Motion required** - Every component needs animations

---

## Architecture

```
components/
├── ui/
│   ├── Button.tsx        (~40 lines)
│   ├── Card.tsx          (~50 lines)
│   └── HeroSection.tsx   (~80 lines)
└── sections/
    ├── HeroBackground.tsx (~30 lines)
    └── FeatureGrid.tsx    (~60 lines)
```

→ See [hero-section.md](references/templates/hero-section.md) for complete example

---

## Reference Guide

### Concepts

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Gemini Workflow** | [gemini-design-workflow.md](references/gemini-design-workflow.md) | MANDATORY - Read first |
| **21st.dev** | [21st-dev.md](references/21st-dev.md) | Component inspiration |
| **shadcn/ui** | [shadcn.md](references/shadcn.md) | Component library |
| **Buttons** | [buttons-guide.md](references/buttons-guide.md) | Button states, sizing |
| **Forms** | [forms-guide.md](references/forms-guide.md) | Validation, layout |
| **Cards** | [cards-guide.md](references/cards-guide.md) | Card patterns |
| **Icons** | [icons-guide.md](references/icons-guide.md) | Icon usage |
| **UI Design** | [ui-visual-design.md](references/ui-visual-design.md) | 2026 trends, animations |
| **Grids** | [grids-layout.md](references/grids-layout.md) | Layout system |
| **Patterns** | [design-patterns.md](references/design-patterns.md) | Common patterns |

### Templates

| Template | When to Use |
|----------|-------------|
| [hero-section.md](references/templates/hero-section.md) | Landing page hero |
| [hero-glassmorphism.md](references/templates/hero-glassmorphism.md) | Glassmorphism hero |
| [feature-grid.md](references/templates/feature-grid.md) | Features showcase |
| [pricing-card.md](references/templates/pricing-card.md) | Pricing tiers |
| [contact-form.md](references/templates/contact-form.md) | Contact forms |
| [testimonial-card.md](references/templates/testimonial-card.md) | Reviews/testimonials |
| [stats-section.md](references/templates/stats-section.md) | Stats with counters |
| [faq-accordion.md](references/templates/faq-accordion.md) | FAQ sections |

---

## Quick Reference

### Gemini Design Tools

```typescript
// Create full view from scratch
mcp__gemini-design__create_frontend({
  prompt: "Hero section with glassmorphism",
  designSystem: "contents of design-system.md"
})

// Modify existing component
mcp__gemini-design__modify_frontend({
  existingCode: "<Button>...",
  prompt: "Add hover animation"
})

// Generate snippet
mcp__gemini-design__snippet_frontend({
  prompt: "Loading spinner"
})
```

→ See [gemini-design-workflow.md](references/gemini-design-workflow.md) for complete workflow

### Anti-AI-Slop Table

| FORBIDDEN | USE INSTEAD |
|-----------|-------------|
| Inter, Roboto, Arial | Clash Display, Satoshi, Syne |
| Purple/pink gradients | CSS variables, sharp accents |
| Border-left indicators | Icon + bg-*/10 rounded |
| Flat backgrounds | Glassmorphism, gradient orbs |
| No animations | Framer Motion stagger |

→ See [ui-visual-design.md](references/ui-visual-design.md) for 2026 trends

---

## Best Practices

### DO
- Read gemini-design-workflow.md FIRST
- Search 21st.dev for inspiration before coding
- Match existing design tokens exactly
- Use Framer Motion for all animations
- Split components into <100 line files

### DON'T
- Write UI code manually (use Gemini Design)
- Use forbidden fonts (Inter, Roboto, Arial)
- Skip inspiration search phase
- Forget hover/focus states
- Create components without animations

---

## Framework Delegation (AFTER Gemini)

**After generating UI, ALWAYS delegate to framework expert for SOLID validation.**

### Detection → Expert

| Project Files | Delegate To |
|---------------|-------------|
| `next.config.*` | `fuse-nextjs:nextjs-expert` |
| `package.json` + React | `fuse-react:react-expert` |
| `composer.json` | `fuse-laravel:laravel-expert` |

### Why Delegate?

design-expert handles:
- ✅ Beautiful UI (Anti-AI-Slop)
- ✅ Animations (Framer Motion)
- ✅ Accessibility (WCAG 2.2)

Framework expert handles:
- ✅ SOLID compliance (files < 100 lines)
- ✅ Framework patterns (App Router, Server Components)
- ✅ Integration (Better Auth, Prisma, TanStack)

### Delegation Workflow

```
1. Generate component with Gemini Design
2. Detect framework from project files
3. Launch Task with framework expert
4. Expert validates SOLID + patterns
5. sniper runs final validation
```
