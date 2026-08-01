---
name: motherduck-design-dive
description: Design or redesign a MotherDuck Dive as a responsive, reusable analytics interface. Use when a Dive must be mobile-friendly from the start, support light and dark modes, reserve space for filters, use restrained Power BI-style information design, embed small charts inside metric components, or work across customers without one-off layout changes.
license: MIT
---

# Design a MotherDuck Dive

Use this skill for the visual system and interaction design of a Dive. Pair it with `motherduck-create-dive` for current React and `useSQLQuery` mechanics, and with `motherduck-build-dashboard` when the task also includes defining the analytical story and SQL.

## Design Contract

Every designed or redesigned Dive must:

- start at a 320 px viewport and enhance upward
- use fluid containers and responsive grids instead of fixed desktop widths
- expose a light/dark theme control with token-based chart and UI colors, using the system preference as the initial default when practical
- reserve a predictable filter surface: visible on wide screens and a drawer or sheet on narrow screens
- keep charts inside bounded, responsive containers with readable labels at every breakpoint
- use a restrained business-analytics visual language: neutral surfaces, compact hierarchy, visible axes, quiet borders, and limited decoration
- make each KPI component useful on its own with value, label, comparison context, and a small trend or progress visual when the data supports it
- keep customer variation in data, labels, logo, and theme tokens rather than changing the information architecture
- support keyboard use, visible focus, 44 px touch targets, sufficient contrast, and non-color status cues

Avoid ornamental gradients, glass effects, glowing accents, oversized hero metrics, decorative bento layouts, excessive pills, floating shapes, and prose that sounds like a marketing landing page.

## Workflow

1. Inspect the existing Dive, supplied design paper, screenshots, and live schema before proposing a layout.
2. If MotherDuck MCP is available, call `get_dive_guide` before writing Dive code and again before any save or update if the guide may have changed. Use it for current runtime and query contracts; use this skill for the responsive shell when generic styling examples conflict with the user's explicit design requirements.
3. Define the audience, primary decision, metric hierarchy, filter dimensions, and reuse boundary.
4. Sketch the 320 px composition first: header, filter trigger, compact one- or two-column KPI group, primary chart, supporting sections, and detail view.
5. Expand that composition into tablet and desktop grids without changing reading order.
6. Implement semantic design tokens, theme switching, reusable cards, responsive chart wrappers, and filter state.
7. Validate query correctness separately, then preview the complete Dive with loading, empty, error, long-label, and dense-data states.
8. Run the screenshot, inspection, iteration, and evidence workflow in `references/VISUAL_QA_PLAYBOOK.md`.
9. Verify the viewport and theme matrix in `references/RESPONSIVE_DIVE_DESIGN_SYSTEM.md` before saving or updating the Dive.

For answer, review, or planning requests, return the requested design artifact without changing a Dive. For build or redesign requests, implement and preview the in-scope Dive; save or update it only when the request includes that operation.

## Deliverable

Provide:

- the information hierarchy and component map
- filter behavior on mobile, tablet, and desktop
- breakpoint and reflow rules
- light/dark token roles and chart palette
- reusable component boundaries and customer-specific inputs
- accessibility and responsive QA results
- a versioned evidence bundle with desktop, mobile, theme, and filter screenshots plus a short iteration report

Do not call a design mobile-friendly based only on responsive CSS. Report the viewports and states actually checked.

## Open Next

- Read `references/RESPONSIVE_DIVE_DESIGN_SYSTEM.md` for the layout grid, component anatomy, theme tokens, filter model, anti-patterns, and QA checklist.
- Read `references/VISUAL_QA_PLAYBOOK.md` for the repeatable screenshot, visual inspection, iteration, and reviewer handoff loop.

## Related Skills

- `motherduck-create-dive` for the current component contract, preview, save/update, and required resources
- `motherduck-build-dashboard` for the analytical story, section queries, and end-to-end dashboard workflow
- `motherduck-explore` for discovering real dimensions and filter candidates
- `motherduck-query` for validating the SQL behind each visual state
