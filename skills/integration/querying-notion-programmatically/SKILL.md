---
name: querying-notion-programmatically
description: >
  Run Notion MCP searches for pages/blocks and fetch page comments via mcpc-backed Python wrappers.
  Use when Codex needs deterministic, file-backed Notion queries (filters come later).
metadata:
  version: 0.1.0
---

# Querying Notion Programmatically

## Overview
- Code Mode skill for issuing Notion searches (pages/blocks/users) and fetching page comments through mcpc helper scripts.
- Favors deterministic loops: auth preflight, plan file, execute wrapper scripts, read results from disk (never paste big payloads in chat).
- Scope now: queries only; add filters/date/creator later.

## Quick Start (examples)
- Search workspace: `python <CODEX_HOME>/skills/querying-notion-programmatically/scripts/notion_query.py --query "AI ML" --pretty`
- Fetch comments: `python <CODEX_HOME>/skills/querying-notion-programmatically/scripts/notion_comments.py --page-id <page-id-or-url>`
- Any tool (cached schemas): `python <CODEX_HOME>/skills/querying-notion-programmatically/scripts/notion_call_tool.py --tool notion-search --arg query:="AI" --refresh-cache`
- WSL bridge: prefix with `MCPC_BIN="<TOOL_HOME>"` (optional `POWERSHELL_EXE`).

## Prereqs & Auth
- Tools: `mcpc` on PATH; Python 3.11+.
- Manual login only (agent never opens browser): `mcpc https://mcp.notion.com/mcp login --profile <name>` (default `default`).
- Session defaults: `@notion` session, server `https://mcp.notion.com/mcp`, profile from `MCP_PROFILE` or `default`.
- WSL tip: reuse Windows keyring by setting `MCPC_BIN="<TOOL_HOME>"` (PowerShell bridge). Optional `POWERSHELL_EXE` to point at a specific PowerShell.

## Trust / Permissions
- **Always**: Read local files, inspect references/templates, view cached tool schemas on disk.
- **Ask**: Any mcpc call (network); packaging; writing results.
- **Never**: Destructive Notion actions (deletes/moves), credential exfil, auto-login/browser opening.

## Canonical Loop
1) Clarify query goal; if helpful, fill `templates/plan.query.json`.
2) Ensure auth (scripts run preflight; if missing, user must login manually).
3) Run `scripts/notion_query.py` for search or `scripts/notion_comments.py` for comments.
4) Inspect outputs under `results/` (JSON + optional pretty stdout). Reuse files instead of re-running.
5) Append notes to `progress.log` if maintaining a trail; keep payloads out of chat.

## Scripts (execute, don't call tools directly)
- **scripts/notion_query.py**: Run `notion-search` (pages/blocks/users).  
  Flags: `--query` (required), `--query-type internal|user` (default internal), `--ids-only`, `--pretty`, `--output` (default `results/query.search.json`), `--session` (default `@notion`), `--profile`, `--server`. Writes parsed payload; prints summary or IDs.
- **scripts/notion_comments.py**: Fetch comments for a page ID/URL.  
  Flags: `--page-id` (required), `--output` (default `results/comments.json`), `--session`, `--profile`, `--server`. Writes comments payload and pretty-prints concise lines.
- **scripts/notion_call_tool.py**: Generic mcpc caller with cached `mcp_tools/tools-list.json` and `mcp_tools/<tool>.json`.  
  Flags: `--tool <name>` (required), repeatable `--arg key:=value`, `--output` (default `results/<tool>.json`), `--refresh-cache`, `--session/@notion`, `--profile`, `--server`. Warns if tool missing from cached list; always writes output JSON.
- **scripts/notion_common.py**: Shared auth preflight (`tools-list`), mcpc path resolution, file writers. Auto-creates output parent dirs.

## Templates
- `templates/plan.query.json`: Lightweight plan scaffold (query text, query_type, intended outputs). Duplicate/edit per run; keep alongside `results/`.

## References
- `references/usage.md`: Quick reminders on commands, outputs, and resuming.
- `mcp_tools/` (optional, create when needed): Cache tool schemas via `mcpc --json @notion tools-get notion-search > mcp_tools/notion-search.json` to avoid large payloads in context.

## Outputs & Restart
- Scripts write to `results/` (JSON, optional ID text). Keep payloads on disk; cite file paths in chat.
- To resume: read `results/query.search.json` or `results/comments.json`; re-run scripts only if inputs change.

## Packaging
- Validate + package when done:  
  `python <REPO_ROOT>/skills/creating-mcp-code-mode-skills/scripts/package_skill.py <REPO_ROOT>/skills/querying-notion-programmatically dist`
