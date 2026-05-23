---
name: mova-station-operator-v0
description: Use for running station one-button flow (gates -> quality -> finish-branch -> episode store) with evidence paths and zero interactive branches.
allowed-tools: Bash, Read, Grep, Glob
---

## Default action
- Prefer `/station-quick` for the full one-button flow.
- If only verification is requested, use `/gates`.

## Evidence checklist
- Collect artifacts from `artifacts/**` as printed by scripts.
- Always include `git status -sb` and `git diff --stat` when changes exist.
- If quality or station ran, note the newest artifacts path(s).

## Rules
- Documentation: use `/docs` via Context7 MCP only (read-only).
- Execution and side effects: run via station (npm scripts) and/or MOVA-controlled paths.
- No interactive branches; pick safe defaults and proceed.

## Tool selection rules
- If the user asks to run a workflow or do an action, use `mova_run_envelope_v0`.
- If the user asks to inspect or pull episodes, use `mova_search_episodes_v0`.
- If the user asks to run gates/quality/smoke, use `/gates`, `/station-quick`, or `mova_run_npm_v0` (allowlisted scripts only).
- Docs only via `/docs` (Context7, read-only).
