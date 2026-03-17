---
name: svg-illustrations
description: Expert knowledge for creating hand-drawn style SVG illustrations. Activate when creating custom diagrams, working with illustration components, or needing consistent visual design for lessons.
triggers:
  - creating illustrations
  - SVG diagrams
  - visual diagrams
  - hand-drawn style
  - IllustrationLinearFlow
  - IllustrationChecklist
  - IllustrationTeamComposition
  - IllustrationComparisonMap
  - IllustrationPyramid
  - pyramid diagram
  - testing pyramid
  - hierarchy diagram
---

# SVG Illustration System

This skill provides guidance for creating consistent, high-quality hand-drawn style SVG illustrations for the DevOps LMS.

## Overview

The illustration system uses a **hybrid approach**:
1. **Reusable Vue Components** - For common diagram patterns
2. **Design System Composable** - Shared constants and utilities
3. **Custom SVG** - Only when no component fits (rare)

---

## Available Components

### 1. IllustrationLinearFlow

**Purpose:** Sequential step-by-step processes

**Best For:**
- CI/CD Pipelines
- SDLC Phases
- Scrum Framework Flow
- Any A → B → C → D process

**Props:**
```typescript
interface Props {
  steps: Array<{
    label: string      // Main text
    sublabel?: string  // Secondary text
    icon?: string      // Emoji icon
    color: string      // Tailwind color name
  }>
  direction?: 'horizontal' | 'vertical'  // Auto-determined by step count (optional)
  showFeedbackLoop?: boolean             // Show return arrow
  feedbackLabel?: string                 // Label for feedback
  size?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | 'full'
}
```

**Auto-Direction (No need to specify direction):**

| Steps | Layout | Behavior |
|-------|--------|----------|
| ≤5 | Horizontal | Side-by-side flow, full width |
| 6-10 | Vertical | Stacked flow, 280px width |
| >10 | Vertical + Scroll | 600px max-height with scrolling |

You can still override with `direction: horizontal` or `direction: vertical` if needed.

**MDC Usage:**
```md
::illustration-linear-flow
---
steps:
  - label: Plan
    sublabel: Sprint Planning
    icon: 📋
    color: violet
  - label: Build
    sublabel: Development
    icon: 🔨
    color: blue
  - label: Test
    sublabel: QA
    icon: ✅
    color: emerald
  - label: Deploy
    sublabel: Release
    icon: 🚀
    color: amber
showFeedbackLoop: true
feedbackLabel: Continuous Improvement
---
::
```

---

### 2. IllustrationChecklist

**Purpose:** Checkbox-style lists with hand-drawn aesthetic

**Best For:**
- Definition of Done
- Prerequisites
- Acceptance Criteria
- Best Practices lists
- Requirements checklists

**Props:**
```typescript
interface Props {
  title: string                           // Checklist title
  items: Array<string | {                 // Simple string or object
    text: string
    icon?: string
  }>
  note?: string                           // Optional footnote with 💡
  color?: string                          // Default: emerald
  size?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | 'full'  // Default: 2xl
}
```

**MDC Usage:**
```md
::illustration-checklist
---
title: Definition of Done
items:
  - text: Code reviewed and approved
    icon: 👀
  - text: Unit tests passing
    icon: ✅
  - text: Documentation updated
    icon: 📝
  - text: Deployed to staging
    icon: 🚀
note: All items must be checked before marking complete
color: emerald
---
::
```

---

### 3. IllustrationTeamComposition

**Purpose:** Team roles in a container with responsibilities

**Best For:**
- Scrum Team structure
- DevOps Team roles
- Any team/role diagram
- Organizational charts

**Props:**
```typescript
interface Props {
  title: string                           // Team title
  subtitle?: string                       // Optional subtitle
  roles: Array<{
    name: string                          // Role name
    owns: string                          // What they own
    icon: string                          // Emoji icon
    color: string                         // Tailwind color
    responsibilities: string[]            // List of responsibilities
  }>
  footnote?: string                       // Optional footnote
  size?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | 'full'  // Default: full
}
```

**MDC Usage:**
```md
::illustration-team-composition
---
title: Scrum Team
subtitle: Self-organizing, cross-functional
roles:
  - name: Product Owner
    owns: Product Backlog
    icon: 🎯
    color: violet
    responsibilities:
      - Maximizes value
      - Manages backlog
      - Stakeholder liaison
  - name: Scrum Master
    owns: Process
    icon: 🛡️
    color: blue
    responsibilities:
      - Removes impediments
      - Facilitates events
      - Coaches team
  - name: Developers
    owns: Sprint Work
    icon: 👥
    color: emerald
    responsibilities:
      - Build increment
      - Self-organize
      - Cross-functional
footnote: Typical team size: 5-9 people
---
::
```

---

### 4. IllustrationComparisonMap

**Purpose:** Side-by-side concept mapping with connectors

**Best For:**
- Scrum ↔ DevOps mapping
- Traditional vs Modern approaches
- Before/After comparisons
- Any concept mapping

**Props:**
```typescript
interface Props {
  leftTitle: string                       // Left column title
  rightTitle: string                      // Right column title
  leftColor?: string                      // Default: violet
  rightColor?: string                     // Default: cyan
  connections: Array<{
    left: string                          // Left item text
    right: string                         // Right item text
    icon: string                          // Connector emoji
  }>
  footnote?: string                       // Optional footnote
  size?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | 'full'  // Default: full
}
```

**MDC Usage:**
```md
::illustration-comparison-map
---
leftTitle: Scrum
rightTitle: DevOps
leftColor: violet
rightColor: cyan
connections:
  - left: Sprint
    right: Pipeline
    icon: 🔄
  - left: Backlog
    right: Kanban Board
    icon: 📋
  - left: Retrospective
    right: Post-mortem
    icon: 🔍
footnote: Both emphasize continuous improvement
---
::
```

---

### 5. IllustrationPyramid

**Purpose:** Pyramid/hierarchy diagrams where size indicates quantity or importance

**Best For:**
- Testing Pyramid (Unit → Integration → E2E)
- Priority hierarchies
- Layered architectures
- Any bottom-up structure where base is largest

**Props:**
```typescript
interface Props {
  layers: Array<{
    label: string           // Layer name (displayed inside)
    description?: string    // Text shown to the right
    icon?: string           // Emoji shown to the left
    color: string           // Tailwind color name
  }>  // Order: top (smallest) to bottom (largest)
  title?: string            // Optional title above pyramid
  footnote?: string         // Optional centered footnote below
  size?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | 'full'  // Default: xl
}
```

**MDC Usage:**
```md
::illustration-pyramid
---
layers:
  - label: E2E Tests
    description: Few - slow, fragile
    icon: 🌐
    color: rose
  - label: Integration
    description: Some - moderate speed
    icon: 🔗
    color: amber
  - label: Unit Tests
    description: Many - fast, cheap
    icon: 🧩
    color: emerald
footnote: More tests at the bottom, fewer at the top
size: xl
---
::
```

**Visual Structure:**
```
         /\
        /  \     ← Top layer (few/small) - rose
       /____\
      /      \   ← Middle layer (some/medium) - amber
     /________\
    /          \ ← Bottom layer (many/large) - emerald
   /______________\
```

---

## Size Options

All illustration components support a `size` prop to control the maximum width:

| Size | Max Width | Best For |
|------|-----------|----------|
| `sm` | 384px | Vertical flows, simple diagrams |
| `md` | 448px | Compact horizontal flows |
| `lg` | 512px | Medium checklists |
| `xl` | 576px | Standard illustrations |
| `2xl` | 672px | Checklists with longer text |
| `3xl` | 768px | Wide comparisons |
| `full` | 100% | Full-width illustrations (default for most) |

### Default Sizes by Component

| Component | Default Size | Reasoning |
|-----------|--------------|-----------|
| `IllustrationLinearFlow` | Auto-sized | Direction and size determined by step count |
| `IllustrationChecklist` | `2xl` | Single-column lists don't need full width |
| `IllustrationTeamComposition` | `full` | Team cards spread horizontally |
| `IllustrationComparisonMap` | `full` | Side-by-side comparisons need space |
| `IllustrationPyramid` | `xl` | Pyramid with side descriptions needs moderate width |

### IllustrationLinearFlow Auto-Sizing

The component automatically determines layout and size:
- **≤5 steps**: Horizontal layout, full width
- **6-10 steps**: Vertical layout, 280px width
- **>10 steps**: Vertical layout with 600px max-height scrolling

### When to Override Defaults

- Override `direction` only when you specifically need horizontal for >5 items or vertical for ≤5 items
- Use `size: md` or `size: lg` when you want a more compact look
- Defaults work well for most cases - only override when needed

---

## Design System Constants

Located in `app/composables/useIllustrationDesign.ts`

### Color Palette

| Color Name | Main Hex | Light Hex | Text Hex | Use For |
|------------|----------|-----------|----------|---------|
| `violet` | #8b5cf6 | #a78bfa | #c4b5fd | Planning, Strategy, Product |
| `blue` | #3b82f6 | #60a5fa | #93c5fd | Development, Build, Process |
| `emerald` | #10b981 | #34d399 | #6ee7b7 | Testing, Success, Done |
| `amber` | #f59e0b | #fbbf24 | #fcd34d | Warnings, Important, Deploy |
| `rose` | #f43f5e | #fb7185 | #fda4af | Critical, Errors, Blockers |
| `cyan` | #06b6d4 | #22d3ee | #67e8f9 | Information, Links, Ops |
| `gray` | #6b7280 | #9ca3af | #d1d5db | Neutral, Disabled, Background |

### Spacing Constants

```typescript
SPACING = {
  boxPadding: 20,        // Inside boxes
  itemGap: 35,           // Between list items
  arrowLength: 50,       // Arrow length
  containerPadding: 30,  // Container padding
  boxWidth: 140,         // Standard box
  boxHeight: 70,         // Standard box
  largeBoxWidth: 160,    // Role cards
  largeBoxHeight: 200,   // Role cards
  borderRadius: 12,      // Rounded corners
  iconRadius: 25         // Icon circles
}
```

### Stroke Styles

```typescript
STROKES = {
  boxDash: '8,4',           // Box stroke pattern
  arrowDash: '4,3',         // Arrow stroke pattern
  containerDash: '10,5',    // Container stroke pattern
  boxStrokeWidth: 2.5,      // Box stroke width
  arrowStrokeWidth: 2,      // Arrow stroke width
  containerStrokeWidth: 2   // Container stroke width
}
```

### Typography

```typescript
TYPOGRAPHY = {
  fontFamily: "'Segoe UI', system-ui, sans-serif",
  titleSize: 14,      // Titles/headers
  labelSize: 12,      // Main labels
  sublabelSize: 10,   // Secondary text
  smallSize: 9,       // Notes/captions
  iconSize: 20        // Emoji size
}
```

---

## When to Use Each Component

### Decision Tree

```
What type of diagram do you need?
│
├── Sequential process? (A → B → C)
│   └── Use: IllustrationLinearFlow
│
├── Checklist/list with checkboxes?
│   └── Use: IllustrationChecklist
│
├── Team/roles with responsibilities?
│   └── Use: IllustrationTeamComposition
│
├── Side-by-side comparison?
│   └── Use: IllustrationComparisonMap
│
├── Pyramid/hierarchy where size shows quantity?
│   └── Use: IllustrationPyramid
│
└── None of the above?
    └── Create custom SVG (see below)
```

---

## Creating Custom SVG (Rare Cases)

Only create custom SVG when no component fits. Follow these rules:

### 1. Use Design System Constants

```vue
<script setup>
import {
  COLORS,
  SPACING,
  STROKES,
  OPACITY,
  TYPOGRAPHY,
  getColor,
  getHandDrawnRotation
} from '~/composables/useIllustrationDesign'
</script>
```

### 2. Hand-Drawn Style Rules

- **Dashed strokes**: Use `stroke-dasharray` with design system patterns
- **Slight rotation**: Apply `getHandDrawnRotation(index)` for variation
- **Semi-transparent fills**: Use `fill-opacity` from OPACITY constants
- **Rounded corners**: Use `rx` attribute with SPACING.borderRadius

### 3. Template Structure

```vue
<template>
  <svg
    :viewBox="`0 0 ${width} ${height}`"
    class="w-full h-auto"
    role="img"
    aria-label="Descriptive label"
  >
    <!-- Elements here -->
  </svg>
</template>
```

### 4. Accessibility

- Always include `role="img"` and `aria-label`
- Use descriptive labels for screen readers
- Ensure sufficient color contrast

---

## Integration with Lessons

### In Markdown Files (MDC)

Components are automatically available in markdown via MDC syntax:

```md
Here's how the Scrum framework flows:

::illustration-linear-flow
---
steps:
  - label: Sprint Planning
    color: violet
  - label: Daily Scrum
    color: blue
  - label: Sprint Review
    color: emerald
  - label: Retrospective
    color: amber
---
::

As you can see, Scrum is an iterative process...
```

### In Vue Pages

Import directly from the components directory:

```vue
<script setup>
import { IllustrationLinearFlow } from '~/components/illustrations'
</script>

<template>
  <IllustrationLinearFlow :steps="mySteps" />
</template>
```

---

## Common Patterns by Topic

### SDLC Topics
- **Flow diagrams**: IllustrationLinearFlow
- **Phase comparison**: IllustrationComparisonMap
- **Methodology checklist**: IllustrationChecklist

### DevOps Topics
- **Pipeline visualization**: IllustrationLinearFlow (horizontal)
- **Tool comparison**: IllustrationComparisonMap
- **Team structure**: IllustrationTeamComposition

### Agile/Scrum Topics
- **Sprint cycle**: IllustrationLinearFlow (with feedback loop)
- **Team roles**: IllustrationTeamComposition
- **Definition of Done**: IllustrationChecklist
- **Scrum vs Kanban**: IllustrationComparisonMap

### Container Topics
- **Deployment flow**: IllustrationLinearFlow
- **Architecture comparison**: IllustrationComparisonMap

---

## File Locations

```
app/
├── components/content/           # MDC components (auto-registered for markdown)
│   ├── IllustrationLinearFlow.vue
│   ├── IllustrationChecklist.vue
│   ├── IllustrationTeamComposition.vue
│   ├── IllustrationComparisonMap.vue
│   └── IllustrationPyramid.vue
└── composables/
    └── useIllustrationDesign.ts
```

**Important:** Components must be in `components/content/` for MDC syntax to work in markdown files.

---

## Quality Checklist

Before completing any illustration:

- [ ] Uses appropriate component (or justified custom SVG)
- [ ] Colors match topic semantics (e.g., emerald for success)
- [ ] Text is readable and not overlapping
- [ ] Has accessible aria-label
- [ ] Renders correctly in dark mode
- [ ] Responsive (uses w-full h-auto)
- [ ] Integrates naturally with lesson content

---

## Future Components (Planned)

When these patterns are needed frequently, new components will be added:

- **IllustrationTimeline** - Events on a timeline
- **IllustrationCycle** - Circular/cyclic processes
- **IllustrationHierarchy** - Tree structures (parent-child relationships)
- **IllustrationPillars** - Supporting pillars diagram

Note: IllustrationPyramid was added to support testing pyramids and layered hierarchies.
