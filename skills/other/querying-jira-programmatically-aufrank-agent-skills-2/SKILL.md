---
name: querying-jira-programmatically
description: >
  Run Jira MCP searches (Rovo or JQL) via mcpc-backed Python wrappers with cached tool schemas and file-backed outputs.
  Use when Codex needs deterministic Jira queries using @jira and mcpc (no direct HTTP).
metadata:
  version: 0.1.0
---

# Querying Jira Programmatically

## Overview
- Code Mode skill for querying Jira through MCP: Rovo `search` and `searchJiraIssuesUsingJql`, with generic tool caller and cached schemas.
- Uses mcpc wrappers (supports MCPC_BIN/POWERSHELL_EXE for WSL Windows keyring) and writes outputs to disk (`results/` + `.mcpc-skill-caches/`).
- Scope: queries/read-only; no edits/transitions by default.

## Quick Start (examples)
- Rovo search: `python <CODEX_HOME>/skills/querying-jira-programmatically/scripts/jira_search.py --query "incident backlog"`
- JQL search: `python <CODEX_HOME>/skills/querying-jira-programmatically/scripts/jira_search_jql.py --jql "project = ABC ORDER BY updated DESC" --max-results 25`
- Any tool (cached schemas): `python <CODEX_HOME>/skills/querying-jira-programmatically/scripts/jira_call_tool.py --tool search --arg query:="AI" --refresh-cache`
- WSL bridge: prefix with `MCPC_BIN="<TOOL_HOME>"` (optional `POWERSHELL_EXE`).

## Prereqs & Auth
- Tools: `mcpc` on PATH; Python 3.11+.
- Manual login only: `mcpc https://mcp.atlassian.com/v1/mcp login --profile <name>` (default `default`).
- Session defaults: `@jira` session, server `https://mcp.atlassian.com/v1/mcp`, profile from `MCP_PROFILE` or `default`.
- WSL tip: reuse Windows keyring by exporting `MCPC_BIN="<TOOL_HOME>"`; set `POWERSHELL_EXE` for a specific PowerShell if needed.

## Trust / Permissions
- **Always**: Read caches/references; inspect templates; view cached schemas on disk.
- **Ask**: Any mcpc call (network); any tool call that mutates Jira (edits, transitions, create, comments); packaging.
- **Never**: Direct HTTP or credential exposure; destructive actions without explicit user direction.

## Canonical Loop
1) Clarify query (Rovo vs JQL). Optionally fill `templates/plan.search.json` or `templates/plan.jql.json`.
2) Ensure auth (scripts run tools-list preflight; if missing, user must login).
3) Use scripted wrappers: `jira_search.py` (Rovo), `jira_search_jql.py` (JQL), or `jira_call_tool.py` (any tool).
4) Inspect outputs under `results/` and cached schemas under `.mcpc-skill-caches/querying-jira-programmatically/mcp_tools/`. Reuse files instead of re-running.
5) Keep payloads out of chat; reference file paths.

## Scripts (execute, don't call tools directly)
- **scripts/jira_search.py**: Rovo search via `search`.  
  Flags: `--query` (required), `--content-type jira|confluence|all` (default jira), `--output` (default `results/jira.search.json`), `--session/@jira`, `--profile`, `--server`. Writes payload; prints count + key/url summary when possible.
- **scripts/jira_search_jql.py**: JQL search via `searchJiraIssuesUsingJql`.  
  Flags: `--jql` (required), `--cloud-id` (default cached for this Jira instance), `--max-results` (default 50), `--pages` (follow nextPageToken), `--output` (default `results/jira.jql.json`), optional `--raw-output`, `--no-output`, `--timestamp-output`, `--session/@jira`, `--profile`, `--server`. Parses `content[0].text` JSON string when present; writes parsed payload (overwrites by default) and pretty-prints key/summary/status.
- **scripts/jira_call_tool.py**: Generic mcpc caller with cached `mcp_tools/tools-list.json` and `mcp_tools/<tool>.json` under `.mcpc-skill-caches/...`.  
  Flags: `--tool <name>` (required), repeatable `--arg key:=value`, `--output` (default `results/<tool>.json`), `--timestamp-output`, `--refresh-cache`, `--session/@jira`, `--profile`, `--server`. Warns if tool missing from cached list; always writes output JSON.
- **scripts/jira_common.py**: Shared auth preflight (`tools-list`), MCPC_BIN/PowerShell resolution, cache/results root detection, file writers.
- **scripts/jira_team_workload.py**: Group issues by assignee for a project/team (membersOf).  
  Flags: `--project` or `--jql` (one required), `--team`, `--cloud-id` (default set), `--max-results`, `--output`, `--summary-output`, optional `--raw-output`, `--no-output`, `--no-summary`, `--timestamp-output`.
- **scripts/jira_unassigned.py**: Find open unassigned issues.  
  Flags: `--project` or `--jql`, `--include-done`, `--cloud-id`, `--max-results`, `--output`, optional `--raw-output`, `--no-output`, `--timestamp-output`.
- **scripts/jira_backfill_analysis.py**: Fetch “backfill/backlog” items (label or text match) and summarize patterns by status/type/priority.  
  Flags: `--project` or `--jql`, `--label` (else text~\"backfill\"), `--include-done`, `--cloud-id`, `--max-results`, `--output`, `--summary-output`, optional `--raw-output`, `--no-output`, `--no-summary`, `--timestamp-output`.

## Templates
- `templates/plan.search.json`: Rovo search plan scaffold (query, content_type, expected outputs).
- `templates/plan.jql.json`: JQL search plan scaffold (jql, expected outputs).

## References
- `references/usage.md`: Quick commands, MCPC_BIN tip, cache locations.
- Runtime caches: `.mcpc-skill-caches/querying-jira-programmatically/mcp_tools/` (tools-list + per-tool schemas). Should be gitignored; regenerate anytime.

## Outputs & Restart
- Outputs land in `results/`; caches in `.mcpc-skill-caches/querying-jira-programmatically/mcp_tools/`.
- To resume, reuse existing `results/*.json` instead of re-calling MCP when possible.

## Packaging
- Validate + package when done:  
  `python <REPO_ROOT>/skills/creating-mcp-code-mode-skills/scripts/package_skill.py <REPO_ROOT>/skills/querying-jira-programmatically dist`
