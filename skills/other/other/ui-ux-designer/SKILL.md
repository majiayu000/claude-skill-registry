---
name: ui-ux-designer
description: Comprehensive skill for UI/UX design and implementation in web applications. Use for tasks involving design systems, component creation, responsive layouts, accessibility, theming, and frontend best practices. Triggers on requests to build, design, or style web components, pages, or applications with a focus on high-quality user experience.
---

# UI/UX Designer Skill

This skill provides a comprehensive toolkit for designing and implementing high-quality user interfaces in web applications, following modern best practices.

## Core Concepts

The skill is built around a flexible design system, a library of reusable components and layouts, and a set of guidelines for creating accessible, performant, and visually appealing user experiences.

Start by exploring the `assets/` directory for ready-to-use templates.

## Getting Started: Project Setup

1.  **Theme & Styles**: Copy the files from `assets/theme/` into your project.
    -   `tailwind.config.js`: A pre-configured Tailwind CSS theme.
    -   `global.css`: Includes base styles, CSS variables for theming, and Tailwind directives.
2.  **Utilities**: Copy the utility functions from `assets/utils/`, like `cn.ts` for merging class names.
3.  **Dependencies**: Install the necessary dependencies mentioned in the asset files (e.g., `class-variance-authority`, `tailwindcss-animate`).

## Building Components & Layouts

-   **Components**: Use the examples in `assets/components/` (e.g., `Button.tsx`, `Input.tsx`) as a starting point for your component library.
-   **Layouts**: The `assets/layouts/` directory contains templates for common page structures like dashboards and marketing pages.

## Design Guidelines & Best Practices

The `references/` directory contains detailed documentation on all aspects of the design and development process. Refer to these guides as you work.

### Foundational Guides
- **[01-design-system.md](./references/01-design-system.md)**: Color, typography, spacing.
- **[02-component-design-patterns.md](./references/02-component-design-patterns.md)**: Atomic design, variants, states.
- **[03-layout-grid-systems.md](./references/03-layout-grid-systems.md)**: Responsive grids, breakpoints.

### Interaction & Accessibility
- **[04-user-flow-interaction.md](./references/04-user-flow-interaction.md)**: Form design, feedback patterns.
- **[05-accessibility.md](./references/05-accessibility.md)**: WCAG checklist, ARIA, keyboard navigation.
- **[06-dark-mode-theming.md](./references/06-dark-mode-theming.md)**: Implementing dark mode.

### Advanced Topics
- **[07-animation-motion-design.md](./references/07-animation-motion-design.md)**: Animation principles, performance.
- **[08-mobile-first-responsive-design.md](./references/08-mobile-first-responsive-design.md)**: Mobile patterns, responsive images.
- **[09-design-handoff-prototyping.md](./references/09-design-handoff-prototyping.md)**: Storybook, visual regression testing.
- **[10-ui-pattern-library.md](./references/10-ui-pattern-library.md)**: When to use different components.
- **[11-performance-optimization.md](./references/11-performance-optimization.md)**: CSS, images, bundle size.
- **[12-design-tools-technologies.md](./references/12-design-tools-technologies.md)**: Recommended tech stack.
