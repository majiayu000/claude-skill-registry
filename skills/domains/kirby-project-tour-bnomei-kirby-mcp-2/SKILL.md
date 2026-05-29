---
name: kirby-project-tour
description: Maps a Kirby project using Kirby MCP tools/resources, including roots, templates, snippets, controllers, models, blueprints, plugins, runtime status, and key config. Use when a user wants a project overview, file locations, or a quick orientation before making changes.
---

# Kirby Project Tour

## Quick start

- Follow the workflow below for a structured tour.

## KB entry points

- `kirby://kb/glossary/roots`
- `kirby://kb/glossary/template`
- `kirby://kb/glossary/controller`
- `kirby://kb/glossary/blueprint`
- `kirby://kb/glossary/plugin`

## Required inputs

- Focus area (Panel, frontend, performance, security).
- Desired depth and output format.
- Any known pain points to prioritize.

## Output template

- Roots: templates, snippets, controllers, models, blueprints, content, config, plugins.
- Inventory: templates/snippets/controllers/models/blueprints/plugins counts and notable overrides.
- Config highlights: debug/cache/routes/languages.
- Risks or gaps: missing runtime, unknown plugins, stale blueprints.
- Next steps: 3 targeted recommendations (DX/perf/security).

## First edits

- Content display tweaks: `site/templates` and `site/snippets`.
- Query logic: `site/controllers`.
- Panel schema: `site/blueprints`.

## Common pitfalls

- Reporting locations without reading `kirby://roots`.
- Skipping runtime install when indexes look empty.

## Workflow

1. Call `kirby:kirby_init` to capture versions and composer audit details.
2. Read `kirby://roots` and summarize where templates, snippets, controllers, models, blueprints, content, config, and plugins live.
3. Inventory project surface (prefer parallel calls):
   - `kirby:kirby_templates_index`
   - `kirby:kirby_snippets_index`
   - `kirby:kirby_controllers_index`
   - `kirby:kirby_models_index`
   - `kirby:kirby_blueprints_index`
   - `kirby:kirby_plugins_index`
4. If runtime-backed data is needed, check `kirby:kirby_runtime_status` and run `kirby:kirby_runtime_install` if required, then retry indexes.
5. Read key config values when relevant: `kirby://config/debug`, `kirby://config/cache`, `kirby://config/routes`, `kirby://config/languages`.
6. Use `kirby:kirby_search` to jump into task playbooks (examples: "scaffold page type", "custom routes", "search page", "custom blocks").
7. If you hit unfamiliar terms, consult `kirby://glossary` and `kirby://glossary/{term}`.
8. If you are unsure which tool/resource to use next, call `kirby:kirby_tool_suggest` or read `kirby://tools`.

## Output checklist

- Provide a "where to edit what" cheat sheet (template vs controller vs snippet vs blueprint vs content vs config).
- Highlight notable customizations (page models, plugins, blueprint overrides, unusual roots).
- Offer 3 next-step recommendations (DX, performance, security).
