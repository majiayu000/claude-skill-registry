---
name: setup-design-system
description: Initialize the design system or create new UI components with accessibility, Tailwind/shadcn integration, and documentation. Use when setting up the initial design system, adding component categories, or creating complex UI components that need design review.
user-invokable: true
---

# Design System Workflow

Initialize or extend the project's design system with properly accessible, consistent UI components using Tailwind CSS and shadcn/ui.

## Step 0: Verify Feature Branch

Ensure we are on a feature branch based on the latest `main`:

```bash
git fetch origin main
```

If on `main`, create a new feature branch:

```bash
git checkout -b feature/design-system origin/main
```

If already on a feature branch, rebase onto latest `origin/main`:

```bash
git status --porcelain
```

If the working tree is dirty, stash before rebasing:

```bash
git stash push -m "setup-design-system: stash before rebase"
git rebase origin/main
git stash pop
```

If the working tree is clean, rebase directly:

```bash
git rebase origin/main
```

## Step 1: Assess Current State

Check if a design system already exists:

- Look for `packages/ui/` directory structure
- Check for shadcn/ui configuration (`components.json`)
- Check Tailwind configuration (`src/index.css` for `@theme` directives in v4, or `tailwind.config.*` for v3)
- Identify existing components and their patterns
- Check for design tokens (colors, spacing, typography definitions)

Ask the user:

- **Initializing** a new design system or **extending** the existing one?
- If extending: what components or patterns are needed?
- Any brand guidelines, color palette, or Figma designs to reference?
- Dark mode support needed?

## Step 2: Product Council Design Review (for initialization or major changes)

If initializing the design system or making significant structural changes, activate a Product Council subset:

> **Model Selection**: See the [Model Selection](../../README.md#model-selection) section in README.md for mapping agent model specs to Task tool parameters.

### Design Lead (Lead) — consult: ui-design

- **Brand Identity**: Color palette, typography, visual language
- **Component Hierarchy**: Primitives vs composed components
- **Design Tokens**: Token architecture (colors, spacing, typography, shadows)
- **Recommendations**: Design system structure and principles

### Frontend Specialist — consult: frontend-mobile-development

- **Technical Architecture**: Component library structure, build pipeline
- **Framework Integration**: Vite + React 19 compatibility, tree-shaking
- **Recommendations**: Implementation patterns, tooling choices

### Product Strategist

- **User-Facing Priorities**: Which components are needed first?
- **Brand Consistency**: Does this align with product vision?
- **Recommendations**: Prioritization of design system investment

### CHECKPOINT: Present the design system architecture proposal to the user. Wait for approval of structure and token definitions before building.

## Step 3: Design System Infrastructure

### If initializing a new design system:

Invoke `/ui-design:design-system-setup` for initialization guidance.

Set up the foundation:

**Design Tokens**

- Color palette (primary, secondary, neutral, semantic: success/warning/error/info)
- Typography scale (font families, sizes, weights, line heights)
- Spacing scale (consistent spacing values: 0, 1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64)
- Border radii (none, sm, md, lg, xl, full)
- Shadows (sm, md, lg, xl)
- Breakpoints (sm, md, lg, xl, 2xl)

**Tailwind Configuration**
Using `/frontend-mobile-development:tailwind-design-system`:

- Extend the Tailwind theme with design tokens
- Configure shadcn/ui with project-specific theme colors
- Set up CSS custom properties for runtime theming
- Configure dark mode strategy (class-based or media-query)

**Component Structure**

```
packages/ui/src/
├── components/
│   ├── primitives/    # Button, Input, Badge, Label, Switch
│   ├── layout/        # Container, Grid, Stack, Spacer, Divider
│   ├── navigation/    # Navbar, Sidebar, Breadcrumb, Tabs
│   ├── feedback/      # Alert, Toast, Modal, Dialog, Skeleton
│   ├── data-display/  # Card, Table, List, Avatar, Tooltip
│   └── forms/         # Form, FormField, Select, Checkbox, Radio
├── tokens/            # Design token definitions
├── hooks/             # Shared UI hooks (useMediaQuery, useTheme)
└── utils/             # UI utilities (cn, cva variants)
```

### If extending an existing design system:

Read the existing patterns and conventions before adding new components. Match the established API patterns.

## Step 4: Build Components

For each component needed, follow this process:

### 4a. Component Design

Invoke `/ui-design:create-component` for guided component creation.

Define the component API:

- **Props interface**: All configurable options with TypeScript types
- **Variants**: Size, color, and style variants (using cva or tailwind-variants)
- **Default values**: Sensible defaults that work out-of-the-box
- **Composition**: How it works with child components

### 4b. Implementation

Build each component with:

- Full TypeScript typing (no `any` types)
- Tailwind CSS styling with shadcn/ui patterns
- `React.forwardRef` for ref forwarding
- `className` prop merged with `cn()` utility for style overrides
- Responsive behavior using Tailwind breakpoints

### 4c. Accessibility

Every component must include:

- Semantic HTML elements (button, nav, dialog, etc.)
- ARIA attributes (aria-label, aria-describedby, role, etc.)
- Keyboard navigation (Tab, Enter, Escape, Arrow keys as appropriate)
- Focus management (visible focus ring, focus trap for modals)
- Screen reader announcements for dynamic content
- Color contrast meeting WCAG AA (4.5:1 for text, 3:1 for large text)
- Touch target minimum size (44x44px for interactive elements)

### 4d. Tests

For each component, write:

- **Render test**: Component renders without errors
- **Props test**: All variants and prop combinations render correctly
- **Interaction test**: Click, hover, keyboard interactions work
- **Accessibility test**: ARIA attributes present, keyboard nav works

### CHECKPOINT: After each component (or batch of related components), present the implementation to the user for visual review. Show the component API, variants, and accessibility features.

## Step 5: Accessibility Audit

After all components are built, run a comprehensive accessibility audit:

Invoke `/ui-design:accessibility-audit` on all new/modified components.

Check for:

- **WCAG 2.1 AA compliance** (minimum standard)
- **Color contrast**: All text meets contrast ratios
- **Keyboard navigation**: Complete keyboard operability
- **Screen reader**: All interactive elements announced correctly
- **Focus management**: Logical focus order, visible focus indicators
- **Motion**: Respect `prefers-reduced-motion` media query
- **Touch targets**: Minimum 44x44px on mobile

### CHECKPOINT: Present accessibility audit findings. User approves the accessibility posture or requests changes.

## Step 6: Design Review

Invoke `/ui-design:design-review` to review the overall design system for:

- **Consistency**: All components follow the same patterns
- **Naming**: Props, variants, and CSS classes follow conventions
- **API patterns**: Consistent prop interfaces across components
- **Visual coherence**: Components look like they belong together
- **Completeness**: Common use cases are covered

Address any findings from the review.

## Step 7: Documentation

Document the design system:

- **Component catalog**: Each component with props table, usage examples, and do/don't patterns
- **Design tokens**: Complete reference of colors, typography, spacing
- **Accessibility guide**: Per-component accessibility notes and testing instructions
- **Getting started**: How to import and use components in the app

## Step 8: Commit

Commit with conventional commit format:

For new design system:

```
feat(ui): initialize design system with core components
```

For new components:

```
feat(ui): add <component-name> component
```

For design token changes:

```
feat(ui): update design tokens for <change-description>
```

## Step 9: Hand Off — STOP Here

> [!CAUTION]
> **This skill's work is done.** Do NOT proceed to create a pull request, push to remote, or run a code review. Those are separate skills with their own workflows and checkpoints.

Present the next step to the user:

- **Recommended**: Run `/review-code` for multi-perspective quality and accessibility review before submitting
- **If building a feature that uses these components**: Continue with `/build-feature` to implement the feature, then run `/review-code`
- **If this is standalone design system work**: Run `/review-code` → `/submit-pr`

> [!TIP]
> **Pipeline**: `/plan-feature` → `/build-feature` or `/build-api` → `/review-code` → `/submit-pr`
>
> **`/setup-design-system`** can be run at any point in the pipeline or independently. You are here — proceed to `/review-code` when ready.

**Do not push the branch, create a PR, or invoke `/submit-pr` from within this skill.**
