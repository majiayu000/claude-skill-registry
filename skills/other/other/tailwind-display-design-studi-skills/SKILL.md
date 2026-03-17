---
name: tailwind
description: >-
  Tailwind CSS v4 best-practices skill covering utility-first patterns, @theme
  variables, responsive design, dark mode, custom styles, performance,
  accessibility, and a Figma-to-Tailwind theme generation workflow. Use when
  the user mentions Tailwind, tailwindcss, @theme, utility classes, Tailwind
  config, Figma design tokens, or asks to build, configure, audit, or migrate
  a Tailwind CSS project (including v3 to v4 migrations).
---

# Tailwind CSS Best Practices

Tailwind CSS v4 guide organized as modular rules. Covers the utility-first model, `@theme` variables, responsive/state variants, custom styles, performance, accessibility, and the **Figma → Tailwind theme workflow** for generating design tokens directly from Figma variables.

## ROUTING: Which rule file to load

**IF setting up Tailwind or understanding how utility classes work:**
→ Read `rules/core-utility-model.md`

**IF working with theme variables (`@theme`), design tokens, colors, fonts, spacing:**
→ Read `rules/core-theme-variables.md`

**IF working with responsive design, hover/focus states, dark mode, or custom variants:**
→ Read `rules/core-responsive-and-states.md`

**IF adding custom CSS, component classes, base styles, or custom utilities:**
→ Read `rules/core-custom-styles.md`

**IF optimizing build size, purging unused classes, or configuring content detection:**
→ Read `rules/perf-purging-and-scanning.md`

**IF working on accessibility or dark mode strategies:**
→ Read `rules/a11y-and-dark-mode.md`

**IF translating Figma variables/design tokens into Tailwind v4 theme CSS:**
→ Read `rules/figma-to-theme-workflow.md` + see `figma-tokens/` templates

## Rule index

| Topic | Description | File |
|-------|-------------|------|
| Sections overview | Categories and reading order | [rules/_sections.md](rules/_sections.md) |
| Utility model | Utility-first principles, composing classes, arbitrary values | [rules/core-utility-model.md](rules/core-utility-model.md) |
| Theme variables | `@theme` directive, namespaces, extend/override, `inline`/`static` | [rules/core-theme-variables.md](rules/core-theme-variables.md) |
| Responsive & states | Breakpoints, hover/focus/dark variants, custom variants | [rules/core-responsive-and-states.md](rules/core-responsive-and-states.md) |
| Custom styles | `@layer`, `@utility`, `@variant`, component classes | [rules/core-custom-styles.md](rules/core-custom-styles.md) |
| Performance | Content detection, JIT, build optimization | [rules/perf-purging-and-scanning.md](rules/perf-purging-and-scanning.md) |
| A11y & dark mode | Accessibility utilities, dark mode patterns | [rules/a11y-and-dark-mode.md](rules/a11y-and-dark-mode.md) |
| **Figma workflow** | **Agent workflow: Figma variables → Tailwind `@theme` CSS** | [rules/figma-to-theme-workflow.md](rules/figma-to-theme-workflow.md) |

## Figma → Tailwind theme workflow

This skill includes a dedicated agent workflow to convert Figma design variables into Tailwind v4 `@theme` CSS files. The workflow is described in `rules/figma-to-theme-workflow.md` and uses the annotated templates in `figma-tokens/` as output targets.

**How to trigger it:** paste your Figma CSS variables into chat and ask the agent to generate the Tailwind theme files.

Template files in `figma-tokens/`:
- `colors.css` — `--color-*` namespace
- `typography.css` — `--font-*`, `--text-*`, `--font-weight-*`, `--tracking-*`, `--leading-*`
- `spacing.css` — `--spacing` and `--spacing-*`
- `radius-shadows.css` — `--radius-*`, `--shadow-*`
- `breakpoints.css` — `--breakpoint-*`

## Rule categories by priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Utility model & theme | CRITICAL | `core-` |
| 2 | Responsive & states | HIGH | `core-` |
| 3 | Custom styles | HIGH | `core-` |
| 4 | Figma workflow | HIGH | (standalone) |
| 5 | Performance | MEDIUM-HIGH | `perf-` |
| 6 | Accessibility | MEDIUM | `a11y-` |

## Coverage and maintenance

- Coverage map: `rules/_coverage-map.md`
- Source: https://tailwindcss.com/docs (v4.2)
- Update when Tailwind releases a new major/minor version with breaking `@theme` changes.
