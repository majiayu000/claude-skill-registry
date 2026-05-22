---
name: design-system-starter
description: Use this skill when creating or evolving design systems for applications. Provides design token structures, component architecture patterns, documentation templates, and accessibility guidelines. Ensures consistent, scalable, and accessible UI design across products.
context: fork
agent: rapid-ui-designer
version: 1.0.0
author: AI Agent Hub
tags: [design-system, ui, components, design-tokens, accessibility, frontend]
user-invocable: false
---

# Design System Starter

## Overview

This skill provides comprehensive guidance for building robust, scalable design systems that ensure visual consistency, improve development velocity, and create exceptional user experiences.

**When to use this skill:**
- Creating a new design system from scratch
- Evolving or refactoring existing design systems
- Establishing design token standards
- Defining component architecture
- Creating design documentation
- Ensuring accessibility compliance (WCAG 2.1)
- Implementing theming and dark mode

**Bundled Resources:**
- `references/design-tokens.md` - Complete token definitions
- `references/component-patterns.md` - Architecture patterns
- `references/component-examples.md` - Full component implementations
- `references/theming.md` - Theme and dark mode patterns
- `templates/design-tokens-template.json` - W3C design token format
- `templates/component-template.tsx` - React component template

```typescript
// Example: Design token structure
const tokens = {
  colors: {
    primary: { base: "#0066cc", hover: "#0052a3" },
    semantic: { success: "#28a745", error: "#dc3545" }
  },
  spacing: { xs: "4px", sm: "8px", md: "16px", lg: "24px" }
};
```
- `checklists/design-system-checklist.md` - Design system audit checklist

---

## Design System Philosophy

A design system is more than a component library. It includes:

| Layer | Description | Examples |
|-------|-------------|----------|
| **Design Tokens** | Foundational design decisions | Colors, spacing, typography |
| **Components** | Reusable UI building blocks | Button, Input, Card, Modal |
| **Patterns** | Common UX solutions | Forms, Navigation, Layouts |
| **Guidelines** | Rules and best practices | Accessibility, naming, APIs |
| **Documentation** | How to use everything | Storybook, usage examples |

### Core Principles

1. **Consistency Over Creativity** - Predictable patterns reduce cognitive load
2. **Accessible by Default** - WCAG 2.1 Level AA compliance minimum
3. **Scalable and Maintainable** - Design tokens enable global changes
4. **Developer-Friendly** - Clear API contracts and documentation

---

## References

### Design Tokens
**See: `references/design-tokens.md`**

Key topics covered:
- Color scales (primitive 50-950, semantic tokens)
- Typography system (font families, sizes, weights, line heights)
- Spacing scale (4px base system)
- Border radius and shadow tokens
- W3C design token format
- Tailwind `@theme` integration

**Quick Reference - Token Categories:**

| Category | Examples | Scale |
|----------|----------|-------|
| Colors | `blue.500`, `text.primary`, `feedback.error` | 50-950 |
| Typography | `fontSize.base`, `fontWeight.semibold` | xs-5xl |
| Spacing | `spacing.4`, `spacing.8` | 0-24 (4px base) |
| Border Radius | `borderRadius.md`, `borderRadius.full` | none-full |
| Shadows | `shadow.sm`, `shadow.lg` | xs-xl |

---

### Component Patterns
**See: `references/component-patterns.md`**

Key topics covered:
- Atomic Design methodology (Atoms -> Pages)
- Props best practices (predictable names, sensible defaults)
- Composition over configuration
- Compound component pattern
- Polymorphic components
- CVA variant pattern

**See: `references/component-examples.md`** for full implementations.

**Quick Reference - Atomic Design:**

| Level | Description | Examples |
|-------|-------------|----------|
| Atoms | Indivisible primitives | Button, Input, Label, Icon |
| Molecules | Simple compositions | FormField, SearchBar, Card |
| Organisms | Complex compositions | Navigation, Modal, DataTable |
| Templates | Page layouts | DashboardLayout, AuthLayout |
| Pages | Specific instances | HomePage, SettingsPage |

---

### Theming
**See: `references/theming.md`**

Key topics covered:
- Theme structure and TypeScript interfaces
- Dark mode implementation approaches
- Tailwind `@theme` directive (recommended)
- Tailwind dark mode variant
- Styled Components ThemeProvider
- Theme toggle component
- System preference detection

**Quick Reference - Dark Mode Approaches:**

| Approach | Best For | Complexity |
|----------|----------|------------|
| Tailwind `@theme` | New projects | Low |
| Tailwind `dark:` variant | Quick implementation | Low |
| CSS Variables | Framework-agnostic | Medium |
| ThemeProvider | CSS-in-JS apps | Medium |

---

## Accessibility Guidelines

### WCAG 2.1 Level AA Requirements

| Requirement | Threshold | Tools |
|-------------|-----------|-------|
| Normal text contrast | 4.5:1 minimum | WebAIM Contrast Checker |
| Large text contrast | 3:1 minimum | |
| UI components | 3:1 minimum | |

### Essential Patterns

- **Keyboard Navigation**: All interactive elements must be keyboard accessible
- **Focus Management**: Use focus traps in modals, maintain logical focus order
- **Semantic HTML**: Use `<button>`, `<nav>`, `<main>` instead of generic divs
- **ARIA Attributes**: `aria-label`, `aria-expanded`, `aria-controls`, `aria-live`
- **Screen Readers**: Provide meaningful labels, announce dynamic content

---

## Quick Start Checklist

When creating a new design system:

- [ ] Define design principles and values
- [ ] Establish design token structure (colors, typography, spacing)
- [ ] Create primitive color palette (50-950 scale)
- [ ] Define semantic color tokens (brand, text, background, feedback)
- [ ] Set typography scale and font families
- [ ] Establish spacing scale (4px or 8px base)
- [ ] **Use Tailwind `@theme` directive** to define tokens
- [ ] **Components use Tailwind utilities** (`bg-primary`, `text-text-primary`)
- [ ] Design atomic components (Button, Input, Label, etc.)
- [ ] Implement theming system (light/dark mode)
- [ ] Ensure WCAG 2.1 Level AA compliance
- [ ] Set up documentation (Storybook or similar)
- [ ] Create usage examples for each component
- [ ] Establish versioning and release strategy

**Current Implementation (January 2026):**
- All colors defined in `frontend/src/styles/tokens.css` using `@theme` directive
- Components use Tailwind utilities: `bg-primary`, `text-text-primary`, `border-border`
- DO NOT use CSS variables in className: `bg-[var(--color-primary)]`

---

## Design System Workflow

### 1. Design Phase
- Audit existing patterns and identify inconsistencies
- Define design tokens (colors, typography, spacing)
- Create component inventory
- Design in Figma (create component library)

### 2. Development Phase
- Set up tooling (Storybook, TypeScript, testing)
- Implement tokens (CSS variables or theme config)
- Build atoms first, then compose upward
- Document as you go

### 3. Adoption Phase
- Create migration guide for teams
- Provide codemods to automate migrations
- Run workshops to train teams
- Gather feedback and iterate

### 4. Maintenance Phase
- Version semantically (major/minor/patch)
- Define deprecation strategy
- Maintain changelog
- Monitor adoption across products

---

## Integration with Agents

| Agent | Usage |
|-------|-------|
| **Rapid UI Designer** | Uses tokens for consistent interfaces, references components |
| **Frontend UI Developer** | Implements components following patterns |
| **Code Quality Reviewer** | Validates design system adherence |

---

**Skill Version**: 1.0.0
**Last Updated**: 2025-10-31
**Maintained by**: AI Agent Hub Team

## Related Skills

- `a11y-testing` - Automated accessibility testing to validate WCAG compliance of design system components
- `focus-management` - Keyboard focus patterns for accessible interactive widgets in design systems
- `type-safety-validation` - End-to-end type safety with Zod for design token schemas and component props
- `react-server-components-framework` - React 19 patterns for server-rendered design system components

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Token Format | W3C Design Tokens | Industry standard, tool-agnostic, supports theming |
| Component Architecture | Atomic Design | Scalable hierarchy from atoms to pages |
| Styling Approach | Tailwind `@theme` directive | Native CSS variable integration, zero runtime |
| Variant Management | CVA (Class Variance Authority) | Type-safe variants, composable styles |
| Documentation | Storybook | Interactive component playground, visual testing |

## Capability Details

### design-tokens
**Keywords:** design tokens, css variables, theme, colors, spacing
**Solves:**
- Create design token system
- Color palette
- Typography scale

### component-architecture
**Keywords:** component library, atomic design, atoms, molecules
**Solves:**
- Structure component library
- Compound components
- Variants

### accessibility
**Keywords:** a11y, wcag, aria, keyboard navigation, focus
**Solves:**
- WCAG 2.1 AA compliance
- ARIA attributes
- Keyboard support

### theming
**Keywords:** theme, dark mode, light mode, color scheme
**Solves:**
- Implement dark/light mode
- Theme switching
- CSS custom properties