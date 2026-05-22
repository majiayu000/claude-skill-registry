---
name: motherduck-create-dive
description: Create, edit, manage, share, or embed MotherDuck Dives. Use when the work involves Dive authoring, live React + SQL components, MCP get_dive_guide, useSQLQuery, local preview, version history, Dives-as-code, required resources, team sharing, or embedded Dive sessions.
argument-hint: [dive-goal]
license: MIT
---

# Create and Manage MotherDuck Dives

Use this skill when the user needs a persistent, shareable, editable Dive rather than a one-off chart. Dives are live React + SQL data apps inside MotherDuck; they can be built conversationally, edited from existing workspace content, managed as code, shared with teammates, or embedded in another application.

## Source Of Truth

- Prefer current MotherDuck Dive docs first.
- If MotherDuck MCP is available, call `get_dive_guide` before generating, saving, or updating a Dive.
- Use the blessed Dives example repo as the reference implementation for local preview, Dives-as-code layout, metadata, CI previews, and deploy scripts.
- Use Dives SQL functions when the user wants a scriptable SQL-native create/read/update/delete workflow instead of MCP tools.
- Treat ordinary Dives and embedded Dives separately: current public materials say Dives are available on all plans, while embedding requires a Business plan.
- Keep authoring, local-preview, required-resource, sharing, versioning, code-management, and embedding guidance aligned with current docs.

## Default Posture

- First classify the job: new Dive, existing Dive edit, Dives-as-code workflow, team sharing, or embedding.
- Validate the underlying SQL and schema first with `motherduck-explore` and `motherduck-query`; a good Dive starts with a correct query.
- Keep Dive queries fully qualified and SQL-heavy; let React handle presentation, not data reshaping.
- Treat the component contract as React + `useSQLQuery`, a default export, supported runtime libraries, explicit loading/empty/error states, and no browser-side secrets.
- When local preview uses `REQUIRED_DATABASES`, keep the export on one line and mirror the real share dependencies in metadata or save/update inputs. Avoid aliases that collide with existing database names.
- Start from a named theme direction such as `Corporate Dashboard`, `Tufte Minimal`, or `FT Salmon` instead of vague visual prompts.
- Prefer one query per visual section or interaction surface rather than one giant cross-purpose query.
- Preview locally before saving when the environment supports it.
- For existing Dives, read the current content and version metadata before overwriting anything. MCP `list_dives` returns `current_version`, and `read_dive` can fetch historical versions.
- Treat embedded Dives as the first-choice path when a product needs a live read-only Dive surface with a backend-created embed session. Move to `motherduck-build-cfa-app` when the app needs custom API contracts, writes, non-Dive routing, tenant policy enforcement, or richer authorization.
- For shared repos or CI/CD, use a service-account token so Dive ownership is not tied to one human user.

## Workflow

1. Classify the delivery path: workspace Dive, edit existing Dive, Dives-as-code, share with teammates, or embed in an app.
2. Explore the live schema and validate the core SQL first.
3. Call `get_dive_guide` if MCP is available, then design the story, sections, interactions, and theme.
4. Build or edit the Dive component, using local preview/hot reload when possible.
5. Save, update, or deploy only after queries, loading states, required resources, and visual behavior are correct.
6. If teammates or application users need access, configure the underlying shares or embed-session flow explicitly.

## Open Next

- `references/DIVE_DESIGN_GUIDE.md` for authoring workflows, `useSQLQuery` mechanics, Dives-as-code, editing/version history, sharing, embedding, SQL functions, theming prompts, chart-selection rules, loading/error states, layout patterns, and implementation gotchas

## Related Skills

- `motherduck-explore` for discovering the real tables, views, and dimensions before visualizing them
- `motherduck-query` for validating the SQL each Dive section will run
- `motherduck-build-dashboard` when the work is really a multi-section dashboard composition problem
- `motherduck-build-cfa-app` when the requirement is a fuller product surface with per-customer isolation or backend policy control
