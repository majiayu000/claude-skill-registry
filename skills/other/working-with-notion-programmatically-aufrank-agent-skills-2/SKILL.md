---
name: working-with-notion-programmatically
description: "Use mcpc to interact with the Notion MCP server: connect sessions, search workspace content, fetch pages/databases, and run helper scripts for common Notion actions."
metadata:
  short-description: Notion MCP via mcpc with scripted preflight, caching, and file outputs.
  stability: stable
  version: "1.1.0"
---
# working-with-notion-programmatically

## When to use
Drive the Notion MCP server via `mcpc` for search, fetch, comments, and follow-on Notion tools using deterministic scripts. This skill favors Code Mode patterns: auth preflight, dynamic schema caching, file-backed outputs, and small templates.

## Requirements
- Interactive auth: Notion MCP login needs network, a browser, and a foreground shell. The agent cannot automate it. If preflight fails, the user must run `mcpc https://mcp.notion.com/mcp login --profile <name>` manually, then retry.
- Shell: PowerShell (quote `@notion` as `'@notion'`).
- Tools: `mcpc` on PATH; Python 3.12+ for scripts; `jq` optional for local inspection.

## Degrees of freedom & trust
- **Always (explore)**: Read local files, inspect `references/`, `templates/`, `mcp_tools/`, view script help, and run auth preflight that only reads profiles.
- **Ask (shape/execute)**: Any `mcpc` call (network), connecting sessions, and all helper scripts (they call `mcpc`). Prompt the user to login in their own shell/browser if auth is missing.
- **Never**: Destructive Notion moves/deletes without explicit user instruction; backgrounding or auto-opening `mcpc ... login`.

## Canonical loop
1) Run auth preflight (built into scripts via `notion_common.ensure_auth`) to ensure profile + connectivity; if it fails, instruct the user to login manually.  
2) Cache tool schemas as needed into `mcp_tools/` (see instructions below).  
3) Shape a plan using `templates/plan.search.json` or `templates/plan.fetch.json`; note expected outputs.  
4) Execute scripts (search/fetch/comments) — they write outputs under `results/` and keep stdout minimal.  
5) Append progress/errors; reuse cached outputs instead of re-running when possible.

## Artifacts & caching
- `templates/`: `plan.*.json`, `results.*.json`, `progress.log` skeleton.
- `mcp_tools/`: Cache of tool schemas pulled via `mcpc --json … tools-get …` to avoid large responses in context.
- `references/`: Minimal pointers for filters, tool names, and PowerShell quoting.
- Runtime outputs: scripts write to `results/` (JSON + snippets) so the model can re-open files instead of re-calling MCP.

## Scripts (all gate on auth preflight)
- `scripts/notion_search.py`: search with filters; supports `--pretty`, `--ids-only`, `--output`. Writes parsed payload to `results/search.json` by default.
- `scripts/notion_fetch.py`: fetch page/database; `--output` writes raw JSON (default `results/fetch.json`).
- `scripts/notion_fetch_plain.py`: fetch + compact snippet; `--output` writes summary text (default `results/fetch_snippet.txt`) and payload JSON if requested.
- `scripts/notion_comments.py`: fetch comments, optional author filter; `--output` writes parsed comments (default `results/comments.json`).
- `scripts/notion_pretty.py`: pretty-printer for any `mcpc --json` output (no network).

## Authentication (manual, interactive)
- User must run login in a foreground shell with a browser:  
  `mcpc https://mcp.notion.com/mcp login --profile <name>`  
  Default profile: `default`. Server override: set `MCP_SERVER`.  
- Scripts check `~/.mcpc/profiles.json` for the profile/server and then run a lightweight connectivity probe (`tools-list`). On failure they exit with clear instructions to login manually; they do **not** open a browser.

## Restart/resume
- Reuse `results/` files before re-running network calls.
- Keep notes in `progress.log`. If interrupted, read existing outputs and continue from step 3 of the loop.

## Avoid
- Dumping large MCP JSON into chat; point to files under `results/` or `mcp_tools/`.
- Mixing freedom levels in one step; decide → configure → execute.
## New rails for search→fetch→mentions→users
- `scripts/notion_search_and_fetch.py`: search + fetch in one run; outputs search payload + search IDs (`results/search_and_fetch.search_ids.txt`), fetch IDs (`results/search_and_fetch.fetch_ids.txt`), snippets, fetch JSON, optional payloads dir.
- `scripts/notion_bulk_fetch.py`: fetch IDs from `--ids/--ids-file`; outputs JSON, snippets, and `results/bulk_fetch.ids.txt` for downstream steps.
- `scripts/notion_extract_mentions.py`: scan payload JSONs (default `results/payloads`) for `user://…` mentions; outputs `results/mentions.ids.txt` and `results/mentions.json` (counts per file/total).
- `scripts/notion_resolve_users.py`: resolve user IDs via `notion-get-user`; outputs `results/user_lookup.json` and `results/user_lookup.txt`.

### Recommended pipeline
1) `notion_search_and_fetch.py --query "<text>" --payload-dir results/payloads`
2) `notion_extract_mentions.py --payload-dir results/payloads`
3) `notion_resolve_users.py --ids-file results/mentions.ids.txt`
