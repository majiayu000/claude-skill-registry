---
name: layout-framework
description: Use for any frontend layout or form arrangement work in PierceDesk. Covers Box/Container/Grid/Stack/Paper usage, responsive sizing, spacing rules, and how to align pages with the app’s layout framework. Trigger when asked to fix layout issues, align fields, create grids, or ensure design-system consistency.
---

# Layout Framework Skill

## Core rules (always follow)

- Use MUI v7 Grid with the `size` prop (not `xs`/`md` props).
- Prefer `Grid container` for column layouts; use `Stack` for simple vertical rhythm.
- Avoid hardcoded widths/heights; use theme spacing and responsive values (`{ xs, md }`).
- Wrap major sections in `Paper background={1}` with `p: { xs: 3, md: 5 }` and `borderRadius: 6` unless the surrounding layout already provides a card.
- Keep inputs aligned in a consistent grid (e.g., 12 / 6 / 3 / 3, 8 / 4, 6 / 6). No uneven, ad-hoc sizing.
- Use `Container` only for page-level width constraints. Inside cards, use `Grid` for structure.

## When to read references

- For exact examples of Box/Container/Grid/Stack usage, read:
  - `references/component-docs-map.md`
  - `references/layout-patterns.md`

## Default layout patterns

- **Two-column forms**: `Grid container spacing={{ xs: 2, md: 3 }}` with `size={{ xs: 12, md: 6 }}`.
- **Primary + secondary field**: `size={{ xs: 12, md: 8 }}` + `size={{ xs: 12, md: 4 }}`.
- **Address block**: street `12`, city `6`, state `3`, zip `3`.
- **Section cards**: each form block inside `Paper background={1}` with internal `Grid` or `Stack`.

## Process checklist

1. Identify the page sections and their cards.
2. Decide row/column structure using `Grid` (avoid ad-hoc `sx` flex sizing).
3. Normalize spacing with `spacing={{ xs: 2, md: 3 }}` and `p: { xs: 3, md: 5 }`.
4. Verify that labels/inputs align across rows and breakpoints.
5. Remove any hardcoded widths or manual flex ratios unless they map to a grid size.
