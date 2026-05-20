---
name: scss-patterns
description: SCSS architecture and CSS variable policies. Use when writing SCSS stylesheets, CSS custom properties, or design system tokens. Do NOT use for plain CSS without SCSS or for CSS-in-JS solutions (styled-components, Emotion).
durability: encoded-preference
---

# SCSS Patterns

## Module System Policy

- **Always use `@use`** - `@import` is deprecated, causes duplicate CSS
- **Use `@forward`** for public API exposure in index files
- **Namespace imports** - `@use 'colors' as c` not bare `@use 'colors'`

## CSS Variable Naming Policy

**Pattern**: `--{prefix}-{property}[-{state}][-{variant}]`

| Example | Structure |
|---------|-----------|
| `--btn-background` | prefix + property |
| `--btn-background-hover` | + state |
| `--btn-background-hover-primary` | + variant |

Project-specific conventions (color palette structure, prefixes) belong in project's CLAUDE.md.

## Selector Policy

- **BEM naming** - `Block__Element--Modifier`
- **Max 3 levels nesting** - flatten if deeper
- **Single class selectors** - avoid `.parent .child .grandchild`
- **Use `&` for BEM** - `&__element`, `&--modifier`

## Loop Policy

- **Use `@each` for variants** - sizes, colors, breakpoints
- **Use maps for configuration** - not scattered variables

## Anti-Patterns

| Avoid | Why | Fix |
|-------|-----|-----|
| `@import` | Deprecated, duplicate CSS | Use `@use` |
| Magic numbers (`13px`) | Unmaintainable | Use variables |
| Deep nesting (> 3 levels) | Specificity wars | Flatten with BEM |
| `!important` | Specificity problem | Refactor selectors |
| Hardcoded colors | Breaks theming | Use CSS/SCSS variables |
| Bare `@use` without namespace | Name collisions | Always use `as` alias |
