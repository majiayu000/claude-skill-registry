---
name: frontend-enhancer
description: This skill should be used when enhancing the visual design and aesthetics of web applications. It provides modern UI components, design patterns, color palettes, animations, and layout templates. REQUIRES ui-research skill first. Use this skill for tasks like improving styling, creating responsive designs, implementing modern UI patterns, adding animations, selecting color schemes, or building aesthetically pleasing frontend interfaces.
---

# Frontend Enhancer

Transform web applications into visually polished, human-designed experiences.

## PREREQUISITE: Research First

**Before using this skill, ALWAYS complete:**

```
Skill(ui-research)
```

Research is mandatory to avoid generic AI-generated looks. See [UI Inspiration Sources](../_shared/UI_INSPIRATION_SOURCES.md) for source list.

---

## When to Use

**Use for:**

- Improving styling and visual design
- Creating responsive layouts
- Adding animations and transitions
- Selecting color schemes
- Building modern UI patterns
- Enhancing aesthetics

**Don't use when:**

- Need inspiration first → use `ui-research` (MANDATORY)
- UX flow design → use `generic-ux-designer`
- Code architecture → use `generic-feature-developer`
- Code review → use `generic-code-reviewer`

**Foundational References:**

- [UI Inspiration Sources](../_shared/UI_INSPIRATION_SOURCES.md) - Research sources
- [Design Patterns](../_shared/DESIGN_PATTERNS.md) - Visual tokens

## Research-Driven Enhancement Workflow

1. **Research** - Use `ui-research` skill first (5-10 examples minimum)
2. **Assess** - Identify current gaps against research findings
3. **Plan** - Define direction based on inspiration analysis
4. **Foundation** - Set up colors, spacing, animations in theme
5. **Apply** - Implement with human polish (not defaults)
6. **Anti-AI Check** - Verify no generic AI patterns
7. **Refine** - Test responsiveness, verify accessibility
8. **Review** - Check hierarchy, consistency, performance

## Color Palette Selection

| Palette         | Use Case                    |
| --------------- | --------------------------- |
| Corporate Blue  | Business apps, SaaS         |
| Vibrant Purple  | Creative tools, portfolios  |
| Minimalist Gray | Clean, sophisticated        |
| Warm Sunset     | Consumer apps, e-commerce   |
| Ocean Fresh     | Health, finance apps        |
| Dark Mode       | Developer tools, dashboards |

Each palette needs: Primary, Secondary, Accent, Background, Foreground, Muted, Success, Warning, Error

## Component Patterns

### Buttons

- Variants: primary, secondary, outline, ghost, danger
- Sizes: sm, md, lg
- States: loading, disabled

### Cards

- Variants: default, bordered, elevated, interactive
- Subcomponents: Header, Title, Description, Content, Footer

### Forms

- Clear focus states
- Validation feedback
- Helper text
- Required indicators

## Animation Guidelines

**GPU-Accelerated Only:**

```css
/* ✅ DO animate */
transform: translateY(-4px);
opacity: 0.8;

/* ❌ AVOID */
margin-top: -4px;
height: 100px;
```

**Duration Guidelines:**

- Micro-interactions: 100-200ms
- Transitions: 200-300ms
- Complex animations: 300-500ms

**Accessibility:**

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none !important;
    transition: none !important;
  }
}
```

## Responsive Strategy

| Breakpoint | Min Width | Target       |
| ---------- | --------- | ------------ |
| base       | 0         | Mobile       |
| sm         | 640px     | Large phones |
| md         | 768px     | Tablets      |
| lg         | 1024px    | Laptops      |
| xl         | 1280px    | Desktops     |

## Accessibility Checklist

- [ ] Color contrast >= 4.5:1 (WCAG AA)
- [ ] Keyboard accessible
- [ ] Visible focus indicators
- [ ] Semantic HTML
- [ ] Alt text on images
- [ ] Form labels
- [ ] Respects prefers-reduced-motion
- [ ] Touch targets >= 44x44px

## Layout Patterns

### Hero Section

- Centered, split, or minimal variants
- Primary + secondary CTAs
- Optional background gradients

### Feature Grid

- 2, 3, or 4 columns
- Icon + title + description
- Staggered animations
- Hover effects

## Performance

- Bundle size awareness
- Lazy load heavy components
- Optimize images (WebP, responsive)
- 60fps animations

## cn Utility Setup

```typescript
// lib/utils.ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

## Before/After Pattern

When enhancing, document changes:

```
Before: Plain gray button, no hover state
After: Gradient primary button with hover lift effect
```

## Avoiding the AI Look

### Red Flags to Check

Before finalizing, ensure you DON'T have:

- [ ] Default blue/purple gradients
- [ ] Perfectly symmetrical layouts
- [ ] Generic blob/wave decorations
- [ ] Undraw-style stock illustrations
- [ ] "Hero with laptop mockup" cliché
- [ ] Unchanged default color schemes
- [ ] Cookie-cutter card grids
- [ ] Overused glassmorphism/blur

### Human Touch Checklist

Ensure you DO have:

- [ ] Custom color palette (not defaults)
- [ ] Intentional layout asymmetry
- [ ] Unique typography pairing
- [ ] Real/custom imagery
- [ ] Micro-interactions with personality
- [ ] Brand-specific details
- [ ] Thoughtful empty/loading states
- [ ] Copy with character

### Quality Comparison

| Aspect      | Generic AI    | Human-Polished         |
| ----------- | ------------- | ---------------------- |
| **Color**   | Default blue  | Custom brand palette   |
| **Layout**  | Perfect grid  | Intentional variation  |
| **Images**  | Stock/generic | Curated/custom         |
| **Copy**    | Lorem ipsum   | Real, personality-rich |
| **Motion**  | Basic fades   | Purposeful, branded    |
| **Details** | None          | Hover states, feedback |

---

## See Also

- [UI Inspiration Sources](../_shared/UI_INSPIRATION_SOURCES.md) - Research sources (USE FIRST)
- [Design Patterns](../_shared/DESIGN_PATTERNS.md) - Visual design reference
- [UX Principles](../_shared/UX_PRINCIPLES.md) - User experience
- `ui-research` - Mandatory prerequisite skill
- Project `CLAUDE.md` - Design constraints
