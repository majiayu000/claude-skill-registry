---
name: ln-015-hex-line-uninstaller
description: "Use when removing Claude-side hex-line integration surfaces such as MCP registration, permissions, hooks, and output style."
license: MIT
model: claude-haiku-4-5
---

> **Paths:** File paths are relative to skills repo root. Locate this SKILL.md directory and go up one level for repo root.

# Hex-Line Uninstaller

**Type:** L3 Worker
**Category:** 0XX Shared

Removes Claude-side hex-line integration surfaces. This worker is standalone-capable but also supports managed `ln-010` family transport.

**MANDATORY READ:** Load `shared/references/coordinator_summary_contract.md`, `shared/references/environment_worker_runtime_contract.md`, and `shared/references/worker_runtime_contract.md`

This worker cleans Claude-side state directly from config files and CLI state. Missing MCP connectivity is not a blocker; continue with local cleanup and verification wherever possible.

## Input / Output

| Direction | Content |
|-----------|---------|
| **Input** | optional `dry_run`, optional `runId`, optional `summaryArtifactPath` |
| **Output** | Structured summary envelope with `summary_kind = env-cleanup`, `payload.status` = `completed` / `skipped` / `error`, plus cleanup outcomes in `changes` / `detail` |

Transport inputs:
- standalone: omit `runId` and `summaryArtifactPath`
- managed: pass both `runId` and `summaryArtifactPath`

## Runtime

Runtime family: `environment-worker-runtime`

Phase profile:
1. `PHASE_0_CONFIG`
2. `PHASE_1_RESOLVE_CLAUDE_STATE`
3. `PHASE_2_REMOVE_HEXLINE_REGISTRATION`
4. `PHASE_3_REMOVE_HEXLINE_ARTIFACTS`
5. `PHASE_4_VERIFY_CLEANUP`
6. `PHASE_5_WRITE_SUMMARY`
7. `PHASE_6_SELF_CHECK`

Runtime rules:
- emit `summary_kind=env-cleanup`
- standalone runs generate their own `run_id` and write the default worker-family artifact path
- managed runs require both `runId` and `summaryArtifactPath` and must write the summary to the exact provided path
- always write the validated summary artifact before terminal outcome

## Output Contract

Always build a structured `env-cleanup` summary envelope per:
- `shared/references/coordinator_summary_contract.md`
- `shared/references/environment_worker_runtime_contract.md`

Payload fields:
- `mcp_removed`
- `permissions_cleaned`
- `hooks_removed`
- `output_style_removed`
- `verification`
- `status`

## What It Removes

| Surface | Location | Action |
|---------|----------|--------|
| MCP registration | `claude mcp list` / user scope | Remove `hex-line` registration via `claude mcp remove -s user hex-line` when present |
| Permission entries | `~/.claude/settings.json` and `~/.claude/settings.local.json` | Remove `permissions.allow` entries that target `mcp__hex-line__*` |
| Hook entries | `~/.claude/settings.json` and `~/.claude/settings.local.json` | Remove hook entries matching the current hex-line hook signature |
| Output style file | `~/.claude/output-styles/hex-line.md` | Delete file |
| Output style setting | `~/.claude/settings.json` and `~/.claude/settings.local.json` | Clear only if value is `"hex-line"` |
| Hook directory | `~/.claude/hex-line/` | Delete only if empty after artifact cleanup |

## Workflow

### Phase 1: Resolve Claude State

1. Read `~/.claude/settings.json` if present
2. Read `~/.claude/settings.local.json` if present
3. Detect:
   - `hex-line` MCP registration in user scope
   - `permissions.allow` entries for `mcp__hex-line__*`
   - hook entries whose command points to the installed hex-line hook
   - `outputStyle = "hex-line"`
   - installed style file and hook directory
4. Record exactly which owned surfaces exist before mutating anything

### Phase 2: Remove Hex-Line Registration

1. If user-scope `hex-line` registration exists, run:

```text
claude mcp remove -s user hex-line
```

2. If registration is already absent, report `already removed`
3. Do not uninstall the npm package here. This worker owns Claude-side integration surfaces only

### Phase 3: Remove Hex-Line Artifacts

1. Update Claude settings surfaces:
   - remove `permissions.allow` entries for `mcp__hex-line__*`
   - remove hook entries whose command contains the active hex-line hook path
   - remove empty hook event arrays and remove `hooks` only when empty
   - clear `outputStyle` only when it is exactly `"hex-line"`
2. Delete `~/.claude/output-styles/hex-line.md` if present
3. Delete `~/.claude/hex-line/hook.mjs` if present
4. Delete `~/.claude/hex-line/` only when it is empty after file removal

Rules:
- preserve all non-hex-line settings
- never claim cache cleanup unless a concrete cache deletion step exists
- do not touch unrelated MCP registrations or permission entries

### Phase 4: Verify Cleanup

Confirm:
- no user-scope `hex-line` MCP registration remains
- no `permissions.allow` entry targets `mcp__hex-line__*`
- no hex-line hook entry remains in managed Claude settings files
- `outputStyle` is not `"hex-line"`
- `~/.claude/output-styles/hex-line.md` does not exist
- `~/.claude/hex-line/hook.mjs` does not exist

## Notes

- This worker removes Claude-side hex-line integration only
- It does not remove the npm package itself
- It is safe to run multiple times

## Definition of Done

- [ ] Claude user-scope `hex-line` MCP registration removed or confirmed absent
- [ ] `permissions.allow` no longer contains `mcp__hex-line__*`
- [ ] No hex-line hook entries remain in managed Claude settings files
- [ ] `outputStyle: "hex-line"` cleared where owned
- [ ] Installed style and hook artifacts removed
- [ ] Structured summary returned
- [ ] Summary artifact written to the managed or standalone runtime path

**Version:** 1.0.0
**Last Updated:** 2026-03-27
