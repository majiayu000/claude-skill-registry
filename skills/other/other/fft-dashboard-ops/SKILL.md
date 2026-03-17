---
name: fft-dashboard-ops
description: Build and apply Home Assistant Lovelace dashboards from templates using a staged workflow with screenshot verification and context-reactive themes.
---

# FFT Dashboard Ops

Use this skill for generating, staging, applying, and validating farm dashboards.

## Guardrails

- Never run destructive git commands unless explicitly requested.
- Preserve unrelated worktree changes.
- Dashboard apply operations are main/admin chat only.
- Always use the staging file flow; never modify live YAML directly.

## Template Sources

- View/card/theme templates: `/workspace/dashboard-templates/`
- Writable dashboard config mount: `/workspace/dashboard/`

Use templates as a baseline, then adapt entity references using live discovery from `/workspace/farm-state/devices.json`.

## Lovelace Structure Rules

- Top-level structure should include `title` and `views`.
- Each view should define `title`, optional `path`, and `cards`.
- Use supported custom cards when available:
  - `custom:mushroom-*`
  - `custom:apexcharts-card`
- Prefer robust layouts (`grid`, `vertical-stack`, `horizontal-stack`) with clear labels.

## Workflow

1. Read `/workspace/farm-state/current.json` and `/workspace/farm-state/calendar.json` for context.
2. Draft dashboard YAML to `/workspace/dashboard/ui-lovelace-staging.yaml`.
3. Request apply via `ha_apply_dashboard` with `stagingFile` set to the staging path.
4. Request screenshot via `ha_capture_screenshot` for the relevant view.
5. Verify screenshot and iterate until readable and operational.

## Context-Reactive Theming

Use `current.json.context.suggestedTheme` to choose theme variants (for example: dawn, midday, dusk, night, storm, frost, harvest).

- High alert level: emphasize warnings/errors and simplify visual noise.
- Normal operations: prioritize trend visibility and quick actions.
- Calendar-heavy periods: feature timeline/task cards in primary views.

## Safety Expectations

- Never bypass staging-to-live apply flow.
- Never execute shell-level infrastructure changes from dashboard tasks.
- Keep entity IDs explicit and avoid wildcard assumptions.
