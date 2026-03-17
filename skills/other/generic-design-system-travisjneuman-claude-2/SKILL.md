---
name: generic-design-system
description: Complete design system reference for any project - colors, typography, spacing, components, animations. Adapts to project theme and tech stack. Use when implementing UI, choosing colors, creating animations, or ensuring brand consistency. For new design systems, use ui-research skill first.
---

# Generic Design System

Design system reference adapting to any project's visual language.

## Research First for New Systems

When creating a NEW design system (not following an existing one):

```
Skill(ui-research)  # Research modern patterns first
```

**References:**

- [UI Inspiration Sources](../_shared/UI_INSPIRATION_SOURCES.md) - Research sources
- [Design Patterns](../_shared/DESIGN_PATTERNS.md) - Visual tokens

## When to Use This Skill

**Use for:**

- Implementing UI components
- Choosing colors or typography
- Creating animations or transitions
- Ensuring visual consistency
- Setting up design tokens
- Reviewing design system compliance

**Don't use when:**

- UX flow design → use `generic-ux-designer`
- Feature architecture → use `generic-feature-developer`
- Code quality review → use `generic-code-reviewer`

## Design System Architecture

### When to Build vs Reference

| Situation              | Action                                  |
| ---------------------- | --------------------------------------- |
| Existing design system | Follow it strictly                      |
| No design system       | Use this skill to establish foundations |
| Partial system         | Identify gaps, extend consistently      |

### Token Organization

| Layer     | Example               | Purpose    |
| --------- | --------------------- | ---------- |
| Primitive | `--color-blue-500`    | Raw values |
| Semantic  | `--color-primary`     | Meaning    |
| Component | `--button-background` | Context    |

**Decision:** Use semantic tokens in code, primitive tokens as foundation only.

### Consistency Decision Tree

1. **Component exists?** → Use existing pattern
2. **Similar exists?** → Adapt existing (don't create competing pattern)
3. **New category?** → Propose to user, document reasoning

## Color System

**Every project should define:**

- Primary, Secondary, Accent
- Background, Foreground, Muted
- Destructive, Success, Warning

### Contrast Requirements

| Use Case      | Minimum    |
| ------------- | ---------- |
| Body text     | 4.5:1 (AA) |
| Large text    | 3:1 (AA)   |
| UI components | 3:1 (AA)   |

## Typography

### Font Stack

```css
--font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
--font-mono: "SF Mono", Monaco, "Courier New", monospace;
```

### Type Scale

| Name | Size | Use             |
| ---- | ---- | --------------- |
| sm   | 14px | Secondary text  |
| base | 16px | Body text       |
| lg   | 18px | Lead paragraphs |
| xl   | 20px | Section headers |
| 2xl  | 24px | Page headers    |

## Spacing System

**Base unit:** 4px or 8px

| Token | 4px Base | Use           |
| ----- | -------- | ------------- |
| 1     | 4px      | Tight spacing |
| 2     | 8px      | Default gap   |
| 4     | 16px     | Card padding  |
| 6     | 24px     | Page margins  |

## Animation

### GPU-Accelerated Only

**DO animate:** `transform`, `opacity`
**AVOID:** `width`, `height`, `top`, `left`, `margin`, `padding`

### Duration

| Token   | Duration | Use                |
| ------- | -------- | ------------------ |
| fast    | 100ms    | Micro-interactions |
| DEFAULT | 200ms    | Most transitions   |
| slow    | 300ms    | Complex animations |

### Timing

```css
--ease-default: cubic-bezier(0.4, 0, 0.2, 1);
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
```

## Components

### Component States

| State    | Visual Treatment  | Example                 |
| -------- | ----------------- | ----------------------- |
| Default  | Base styling      | Normal button           |
| Hover    | Subtle feedback   | Lighter/darker bg       |
| Active   | Pressed state     | Scaled down slightly    |
| Focus    | Visible outline   | 2px ring, offset        |
| Disabled | Reduced opacity   | 50% opacity, no pointer |
| Loading  | Spinner/skeleton  | Button with spinner     |
| Error    | Destructive color | Red border/text         |

### Touch Targets

- **Minimum:** 44x44px (WCAG 2.1 AAA)
- **Spacing:** 8px between adjacent targets
- **Mobile:** Consider 48x48px for primary actions

### Buttons

| Variant     | Use                 | Min Size |
| ----------- | ------------------- | -------- |
| Primary     | Main actions        | 44x44px  |
| Secondary   | Alternative actions | 44x44px  |
| Ghost       | Subtle actions      | 44x44px  |
| Destructive | Delete actions      | 44x44px  |

### Form Inputs

- Clear focus states (2px visible ring)
- Error states with messages
- Label always visible
- Required indicator

### Modals

- Focus trapped inside
- Escape to close
- Dark overlay (50-70% opacity)

## Responsive Breakpoints

| Token | Min Width |
| ----- | --------- |
| sm    | 640px     |
| md    | 768px     |
| lg    | 1024px    |
| xl    | 1280px    |

## Dark Mode

```css
:root {
  --background: #ffffff;
  --foreground: #000000;
}
[data-theme="dark"] {
  --background: #000000;
  --foreground: #ffffff;
}
```

## See Also

- [Design Patterns](./../_shared/DESIGN_PATTERNS.md) - Atomic Design, tokens, component docs
- [Code Review Standards](./../_shared/CODE_REVIEW_STANDARDS.md) - Accessibility checks
- `generic-ux-designer` - For UX flow and research decisions
- Project `CLAUDE.md` - Project-specific design constraints

**READ references when:**

- Setting up new design system → DESIGN_PATTERNS.md (full structure)
- Complex component patterns → DESIGN_PATTERNS.md (Atomic Design section)
