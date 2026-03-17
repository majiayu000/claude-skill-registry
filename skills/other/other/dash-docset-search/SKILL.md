---
name: dash-docset-search
description: Search and reason about Dash.app docsets and cheatsheets on macOS. Use when the task involves explaining Dash capabilities, listing installed docsets, searching one or more docsets, enabling full-text search for selected docsets, or detecting a missing docset and recommending installation paths before handing off to $dash-docset-install-generate.
---

# Dash Docset Search

## Overview

Use this skill to search Dash content with a strict fallback order:

1. `dash-mcp-server` tools first
2. local Dash HTTP API second
3. Dash URL scheme and macOS Service guidance last

Use `references/dash_mcp_tools.md`, `references/dash_http_api.md`, and `references/dash_url_and_service.md` for exact details.

## Automation Prompting

- Codex App automation fit: Strong. Suitable for recurring search and reporting workflows.
- Codex CLI automation fit: Strong. Suitable for non-interactive probe/search tasks with fallback handling.
- Use `references/automation-prompts.md` for Codex App and Codex CLI templates, placeholders, and output shapes.
- Keep install and generation actions out of this skill's automation prompts; hand off to `$dash-docset-install-generate` when needed.

## Workflow

### 1) Establish access path

1. If Dash MCP tools are available, use them first.
2. If Dash MCP tools are unavailable, run:
   - `uv run python scripts/dash_api_probe.py`
3. If probe indicates local API healthy, use `/docsets/list`, `/search`, and `/docsets/enable_fts`.
4. If local API is unavailable, provide `dash://` and Service fallback guidance.

### 2) List installed docsets

- Preferred:
  - `list_installed_docsets`
- HTTP fallback:
  - `GET {base_url}/docsets/list`

Normalize and present:

- display name
- identifier
- platform
- full-text status

### 3) Search one or many docsets

- Preferred:
  - `search_documentation(query, docset_identifiers, search_snippets, max_results)`
- HTTP fallback:
  - `GET /search?query=...&docset_identifiers=...`

Rules:

- Use explicit identifiers from installed docsets.
- Disable snippet search if user asks for docset-only results.
- For multi-docset searches, pass comma-separated identifiers in one query.

### 4) Enable FTS when requested

- Preferred:
  - `enable_docset_fts(identifier)`
- HTTP fallback:
  - `GET /docsets/enable_fts?identifier=...`

Handle `full_text_search` status:

- `enabled`: continue searching
- `disabled`: enable then retry search
- `indexing`: explain indexing in progress
- `not supported`: skip FTS path

### 5) Missing docset recommendation

Use catalog snapshots and matcher:

1. `uv run python scripts/dash_catalog_match.py --query "<text>"`
2. classify top results into:
   - built-in
   - user-contributed
   - cheatsheet
3. if no strong hit, suggest generator flow
4. suggest GitHub or Stack Overflow generation only as last resort

When installation or generation is needed, hand off to `$dash-docset-install-generate`.

## Fallback Search Guidance

When no API path is usable, provide direct commands:

- AppleScript:
  - `open location "dash://?query={query}"`
  - `open location "dash://?query=python:{query}"`
- Terminal:
  - `open "dash://?query={query}"`
- macOS Service:
  - select text, then `Services > Look Up in Dash`

## Scripts

- `scripts/dash_api_probe.py`
  - Probe local Dash API state and schema path availability.
- `scripts/dash_catalog_refresh.py`
  - Refresh built-in, contributed, and cheatsheet snapshots.
- `scripts/dash_catalog_match.py`
  - Rank candidate docsets and cheatsheets for a query.
- `scripts/dash_url_search.py`
  - Launch `dash://` query URLs.
- `scripts/dash_url_install.py`
  - Confirm-first launcher for `dash-install://`.

## References

- `references/dash_mcp_tools.md`
- `references/dash_http_api.md`
- `references/dash_url_and_service.md`
- `references/automation-prompts.md`
- `references/catalog_built_in_docsets.json`
- `references/catalog_user_contrib_docsets.json`
- `references/catalog_cheatsheets.json`

## Optional Visual Troubleshooting

If Dash UI behavior needs visual confirmation, use the `$screenshot` skill if it is available in the user's environment.
