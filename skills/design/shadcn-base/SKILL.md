---
name: shadcn-base
description: Use when you need the Base UI version of shadcn/ui components, docs, CLI, theming, forms, registries, or MCP guidance for shadcn’s Base UI stack.
---

# shadcn/ui (Base UI) — shadcn-base

## Overview
This skill documents the Base UI version of shadcn/ui. Use it to navigate the official Base UI docs and the shadcn/ui Base UI component pages.

shadcn/ui is not headless. It provides styled, copy-and-own components built on top of Base UI’s headless primitives. Composition follows compound components, composition-over-inheritance, and variant-driven styling.

Primary docs:
- Docs entry point: https://ui.shadcn.com/docs
- Base UI project docs: https://base-ui.com
- Base UI skill: skills/base-ui

Important:
- Base UI vs Radix docs and the conversion rule are defined in `references/overview.md`. Use that guidance instead of the Radix components index.

## Start Here
1. Read `references/overview.md` for scope and doc entry points.
2. Use `references/components.md` to find the component you need.
3. Use `references/installation.md` or `references/cli.md` to set up a project.
4. Use `references/theming.md` and `references/dark-mode.md` for design tokens.
5. Use `references/components-json.md` for CLI config details.
6. Use `references/forms.md` for field patterns and `references/forms-integrations.md` for form libs.
7. Use `references/registry.md` and `references/registry-schema.md` for registries.
8. Use `references/blocks.md` for blocks workflows.
9. Use `references/composition-pattern.md` for the composition paradigm and Base UI render rule.
10. Use `references/examples.md` for render and useRender patterns.
11. Check `references/changelog.md` before shipping.

## Composition Pattern (Short)
Base UI + shadcn/ui uses **copy-and-own styled components on headless primitives**, composed via **compound subcomponents** and **render-prop substitution** (`render` / `useRender`). Reference: `references/composition-pattern.md`.

## Reference Map
- `references/overview.md`: what shadcn/ui is and official doc entry points.
- `references/components.md`: full component list from llms.txt.
- `references/installation.md`: create/init and per-framework installation links.
- `references/cli.md`: CLI commands and options.
- `references/components-json.md`: components.json schema and key fields.
- `references/theming.md`: theming and design tokens.
- `references/dark-mode.md`: dark mode guidance and framework-specific pages.
- `references/forms.md`: field usage patterns and validation structure.
- `references/forms-integrations.md`: React Hook Form and TanStack Form pages.
- `references/registry.md`: registry docs.
- `references/registry-schema.md`: registry.json and registry-item.json schema details.
- `references/blocks.md`: blocks library workflows.
- `references/composition-pattern.md`: Base UI composition rule (render/useRender only).
- `references/examples.md`: render and useRender examples (Base UI).
- `references/mcp.md`: MCP server guidance.
- `references/changelog.md`: release notes.
- `references/links.md`: quick links index.
