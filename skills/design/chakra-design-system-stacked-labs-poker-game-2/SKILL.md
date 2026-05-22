---
name: chakra-design-system
description: Build and refactor UI in this repo using Chakra UI v2 + Emotion and the repo theme (`app/theme.ts`). Use for Chakra component usage, responsive layout, a11y, theme tokens/semanticTokens, component variants, and UI polish.
---

# Chakra Design System (Stacked Poker)

## First steps (always)

1. Read the repo rules: `.cursor/rules/frontend-guidelines.mdc`.
2. Check the theme: `app/theme.ts` (colors, semantic tokens, breakpoints, shadows, variants).
3. Find the closest existing component under `app/components/` and follow its patterns.

## Preferred patterns in this repo

- Use Chakra props over ad-hoc CSS when possible; use `sx` for complex selectors/media queries.
- Prefer semantic tokens (`text.primary`, `bg.navbar`, `input.lightGray`, etc) over hardcoded colors.
- Prefer `colors.brand.*` for brand colors (navy/pink/green/yellow).
- Use responsive props or Chakra breakpoint helpers; keep portrait/landscape styling in `sx` only when needed.
- Use `useReducedMotion()` for motion-heavy UI and provide a non-animated fallback.

## Documentation sources (don’t paste full docs)

- Use the Chakra MCP server (see `.cursor/mcp.json`) for component docs and props.
- Chakra LLM docs (as per repo rules): https://chakra-ui.com/llms-full.txt
- Chakra v2 component docs: https://v2.chakra-ui.com/docs/components

## What to load next

- For tokens, variants, and how to name colors: read `references/theme-and-tokens.md`.
- For component composition patterns used in this repo: read `references/component-patterns.md`.
- For starter templates: copy from `assets/`.

