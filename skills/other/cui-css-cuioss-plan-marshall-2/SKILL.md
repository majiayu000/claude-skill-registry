---
name: cui-css
description: Modern CSS standards covering essentials, responsive design, quality practices, and tooling for CUI projects
user-invocable: false
allowed-tools: Read, Grep, Glob
---

# CSS Development Standards

**REFERENCE MODE**: This skill provides reference material. Load specific standards on-demand based on current task.

## Overview

Provides modern CSS development standards for CUI projects, covering fundamentals, responsive design patterns, performance optimization, accessibility, and build tooling.

## Standards Documents

- **css-essentials.md** - Core principles, naming conventions (BEM), custom properties, selectors, file structure, component architecture
- **css-responsive.md** - Mobile-first approach, Grid/Flexbox layouts, Container Queries, fluid typography, responsive patterns
- **css-quality-tooling.md** - Performance optimization, accessibility standards, dark mode, PostCSS/Stylelint/Prettier setup, build pipeline

## What This Skill Provides

### CSS Essentials
- Modern CSS features (custom properties, Grid, Flexbox, modern functions)
- BEM naming methodology and semantic naming patterns
- Selector best practices (low specificity, avoiding IDs, nesting limits)
- Property organization and file structure
- Component architecture patterns
- Utility classes and hybrid approach

### Responsive Design
- Mobile-first development patterns
- CSS Grid layouts (dashboard, content grid, auto-fit)
- Flexbox patterns (navigation, cards, centering)
- Container Queries for responsive components
- Fluid typography with clamp()
- Responsive images, spacing, and common patterns

### Quality & Tooling
- Performance (efficient selectors, containment, critical CSS, bundle optimization)
- Accessibility (focus management, color contrast, motion preferences, touch targets)
- Dark mode (system preference and manual toggle)
- PostCSS configuration (import, nested, autoprefixer, csso)
- Stylelint setup (property ordering, naming patterns, best practices)
- Build pipeline (development, production, quality checks)
- CI/CD integration

## When to Activate

Use this skill when:
- Writing or modifying CSS code
- Setting up CSS tooling (PostCSS, Stylelint, Prettier)
- Implementing design systems and theming
- Building responsive layouts
- Optimizing CSS performance
- Ensuring accessibility compliance
- Reviewing CSS code

## Workflow

1. **Identify task** - Determine which standards document(s) apply
2. **Apply standards** - Follow BEM naming, use custom properties, implement responsive patterns, ensure accessibility
3. **Quality check** - Run Stylelint, Prettier, test responsiveness and accessibility
4. **Document** - Comment complex patterns, explain custom properties

## Best Practices

1. Use CSS custom properties for design tokens
2. Follow mobile-first approach
3. Use BEM naming convention
4. Implement container queries for responsive components
5. Support dark mode via custom properties
6. Ensure accessibility (focus states, motion preferences, contrast ratios)
7. Run quality tools before committing
