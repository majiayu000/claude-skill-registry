---
name: motherduck-create-dive
description: Create interactive MotherDuck Dives with live SQL queries. Use when building, previewing, saving, styling, updating, or embedding a Dive, especially when the workflow depends on get_dive_guide, useSQLQuery, theme prompts, and live MotherDuck data.
argument-hint: [dive-goal]
license: MIT
---

# Create MotherDuck Dives

Use this skill when the user needs a persistent, shareable Dive rather than a one-off chart or a full customer-facing analytics application.

## Source Of Truth

- Prefer current MotherDuck Dive docs first.
- If MotherDuck MCP is available, call `get_dive_guide` before generating, saving, or updating a Dive.
- Keep theming, local-preview, code-management, and embedding guidance aligned with the current Dive docs.

## Default Posture

- Validate the underlying SQL and schema first with `motherduck-explore` and `motherduck-query`.
- Keep Dive queries fully qualified and SQL-heavy; let React handle presentation, not data reshaping.
- When a Dive uses shared databases in `REQUIRED_DATABASES`, always suffix the `alias` (e.g. `_share`) so it cannot collide with an existing database name. Never set `alias` to conflict with an existing database name.
- Start from a named theme direction such as `Corporate Dashboard`, `Tufte Minimal`, or `FT Salmon` instead of vague visual prompts.
- Prefer one query per visual section rather than one giant cross-purpose query.
- Include loading, empty, and error states for every live query before saving or embedding the Dive.
- Preview locally before saving when the environment supports it.
- Treat embedded Dives as the first-choice path when a product needs a live read-only Dive surface. Move to `motherduck-build-cfa-app` when the app needs custom backend contracts, writes, non-Dive routing, or richer authorization.
- For existing Dives, prefer reading version metadata before overwriting content; MCP `list_dives` returns `current_version`, and `read_dive` can fetch historical versions.

## Workflow

1. Explore the live schema and validate the core SQL first.
2. Decide the Dive story, sections, and interaction model.
3. Call `get_dive_guide` if MCP is available.
4. Build and preview the Dive locally when possible.
5. Save or update the Dive only after the live queries, theme, and loading states are correct.
6. If teammates need access, make sure the underlying data is shared appropriately.

## Open Next

- `references/DIVE_DESIGN_GUIDE.md` for `useSQLQuery` mechanics, theming prompts, chart-selection rules, loading/error states, layout patterns, and common Dive implementation gotchas

## Related Skills

- `motherduck-explore` for discovering the real tables, views, and dimensions before visualizing them
- `motherduck-query` for validating the SQL each Dive section will run
- `motherduck-build-dashboard` when the work is really a multi-section dashboard composition problem
- `motherduck-build-cfa-app` when the requirement is a fuller product surface with per-customer isolation or backend policy control
