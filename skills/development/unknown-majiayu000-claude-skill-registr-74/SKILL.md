---
name: tailwind
description: Tailwind CSS v4 performance optimization and best practices guidelines (formerly tailwindcss-v4-style). This skill should be used when writing, reviewing, or refactoring Tailwind CSS v4 code to ensure optimal build performance, minimal CSS output, and correct usage of v4 features. Triggers on tasks involving Tailwind configuration, @theme directive, utility classes, responsive design, dark mode, container queries, or CSS generation optimization.
---

# Tailwind Labs Tailwind CSS v4 Best Practices

Comprehensive performance optimization guide for Tailwind CSS v4 applications, maintained by Tailwind Labs. Contains 42 rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Configuring Tailwind CSS v4 build tooling (Vite plugin, PostCSS, CLI)
- Writing or migrating styles using v4's CSS-first approach
- Optimizing CSS bundle size and build performance
- Implementing responsive designs with breakpoints or container queries
- Setting up theming with @theme directive and design tokens

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Build Configuration | CRITICAL | `build-` |
| 2 | CSS Generation | CRITICAL | `gen-` |
| 3 | Bundle Optimization | HIGH | `bundle-` |
| 4 | Utility Patterns | HIGH | `util-` |
| 5 | Component Architecture | MEDIUM-HIGH | `comp-` |
| 6 | Theming & Design Tokens | MEDIUM | `theme-` |
| 7 | Responsive & Adaptive | MEDIUM | `resp-` |
| 8 | Animation & Transitions | LOW-MEDIUM | `anim-` |

## Quick Reference

### 1. Build Configuration (CRITICAL)

- [`build-vite-plugin`](references/build-vite-plugin.md) - Use Vite Plugin Over PostCSS
- [`build-css-import`](references/build-css-import.md) - Use CSS Import Over @tailwind Directives
- [`build-content-detection`](references/build-content-detection.md) - Leverage Automatic Content Detection
- [`build-node-version`](references/build-node-version.md) - Use Node.js 20+ for Optimal Performance
- [`build-postcss-simplify`](references/build-postcss-simplify.md) - Remove Redundant PostCSS Plugins
- [`build-cli-package`](references/build-cli-package.md) - Use Correct CLI Package

### 2. CSS Generation (CRITICAL)

- [`gen-css-first-config`](references/gen-css-first-config.md) - Use CSS-First Configuration Over JavaScript
- [`gen-avoid-theme-bloat`](references/gen-avoid-theme-bloat.md) - Avoid Excessive Theme Variables
- [`gen-oklch-colors`](references/gen-oklch-colors.md) - Use OKLCH Color Space for Vivid Colors
- [`gen-utility-directive`](references/gen-utility-directive.md) - Use @utility for Custom Utilities
- [`gen-dynamic-utilities`](references/gen-dynamic-utilities.md) - Use Dynamic Utility Values
- [`gen-css-variable-syntax`](references/gen-css-variable-syntax.md) - Use Parentheses for CSS Variable References

### 3. Bundle Optimization (HIGH)

- [`bundle-remove-unused-plugins`](references/bundle-remove-unused-plugins.md) - Remove Built-in Plugins
- [`bundle-avoid-preprocessors`](references/bundle-avoid-preprocessors.md) - Avoid Sass/Less Preprocessors
- [`bundle-css-minification`](references/bundle-css-minification.md) - Enable CSS Minification in Production
- [`bundle-avoid-cdn-production`](references/bundle-avoid-cdn-production.md) - Avoid Play CDN in Production
- [`bundle-split-critical-css`](references/bundle-split-critical-css.md) - Extract Critical CSS for Initial Render

### 4. Utility Patterns (HIGH)

- [`util-renamed-utilities`](references/util-renamed-utilities.md) - Use Renamed Utility Classes
- [`util-important-modifier`](references/util-important-modifier.md) - Use Trailing Important Modifier
- [`util-variant-stacking`](references/util-variant-stacking.md) - Use Left-to-Right Variant Stacking
- [`util-explicit-colors`](references/util-explicit-colors.md) - Use Explicit Border and Ring Colors
- [`util-opacity-modifier`](references/util-opacity-modifier.md) - Use Slash Opacity Modifier
- [`util-gradient-via-none`](references/util-gradient-via-none.md) - Use via-none to Reset Gradient Stops

### 5. Component Architecture (MEDIUM-HIGH)

- [`comp-avoid-apply-overuse`](references/comp-avoid-apply-overuse.md) - Avoid Overusing @apply
- [`comp-reference-directive`](references/comp-reference-directive.md) - Use @reference for CSS Module Integration
- [`comp-utility-file-scope`](references/comp-utility-file-scope.md) - Understand Utility File Scope
- [`comp-smart-sorting`](references/comp-smart-sorting.md) - Leverage Smart Utility Sorting
- [`comp-container-customize`](references/comp-container-customize.md) - Customize Container with @utility

### 6. Theming & Design Tokens (MEDIUM)

- [`theme-semantic-tokens`](references/theme-semantic-tokens.md) - Use Semantic Design Token Names
- [`theme-dark-mode-class`](references/theme-dark-mode-class.md) - Use Class-Based Dark Mode for Control
- [`theme-prefix-variables`](references/theme-prefix-variables.md) - Use Prefix for Variable Namespacing
- [`theme-runtime-variables`](references/theme-runtime-variables.md) - Leverage Runtime CSS Variables
- [`theme-color-scheme`](references/theme-color-scheme.md) - Set color-scheme for Native Dark Mode

### 7. Responsive & Adaptive (MEDIUM)

- [`resp-mobile-first`](references/resp-mobile-first.md) - Use Mobile-First Responsive Design
- [`resp-container-queries`](references/resp-container-queries.md) - Use Container Queries for Component-Level Responsiveness
- [`resp-custom-breakpoints`](references/resp-custom-breakpoints.md) - Define Custom Breakpoints in @theme
- [`resp-hover-capability`](references/resp-hover-capability.md) - Understand Hover Behavior on Touch Devices
- [`resp-logical-properties`](references/resp-logical-properties.md) - Use Logical Properties for RTL Support

### 8. Animation & Transitions (LOW-MEDIUM)

- [`anim-gpu-accelerated`](references/anim-gpu-accelerated.md) - Use GPU-Accelerated Transform Properties
- [`anim-starting-style`](references/anim-starting-style.md) - Use @starting-style for Entry Animations
- [`anim-gradient-interpolation`](references/anim-gradient-interpolation.md) - Use OKLCH Gradient Interpolation
- [`anim-3d-transforms`](references/anim-3d-transforms.md) - Use Built-in 3D Transform Utilities

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

## Full Compiled Document

For a complete guide with all rules expanded, see [AGENTS.md](AGENTS.md).

## Reference Files

| File | Description |
|------|-------------|
| [AGENTS.md](AGENTS.md) | Complete compiled guide with all rules |
| [references/_sections.md](references/_sections.md) | Category definitions and ordering |
| [assets/templates/_template.md](assets/templates/_template.md) | Template for new rules |
| [metadata.json](metadata.json) | Version and reference information |
