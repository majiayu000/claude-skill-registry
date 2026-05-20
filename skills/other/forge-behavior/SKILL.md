---
name: forge-behavior
description: Manage dotforge v3 behavior governance — view status, toggle behaviors, adjust strictness. Use when the user asks about active behaviors, wants to disable one for the current session, or adjust escalation thresholds.
---

# /forge behavior

Thin wrapper around `scripts/forge-behavior/cli.sh`. Dispatches behavior
governance actions. This skill is part of dotforge v3 (Phase 1 of behavior
governance) and should only be used inside dotforge itself or projects that
have adopted v3 — not on v2.9 projects.

## When to use

Invoke this skill when the user asks any of:

- "What behaviors are active?"
- "What's the counter on search-first?"
- "Disable search-first for this session"
- "Turn off the nudge on writes"
- "Make search-first stricter / more relaxed"

Do NOT invoke this skill for v2.9 configuration tasks (use `/forge audit`,
`/forge sync`, etc.) or for behaviors that have not yet been catalogued
(Phase 1 only ships search-first).

## Actions

```bash
scripts/forge-behavior/cli.sh status [--session SESSION_ID]
scripts/forge-behavior/cli.sh on  <behavior_id> [--project | --session SESSION_ID]
scripts/forge-behavior/cli.sh off <behavior_id> [--project | --session SESSION_ID]
scripts/forge-behavior/cli.sh strict  <behavior_id>
scripts/forge-behavior/cli.sh relaxed <behavior_id>
```

**status** — Print the current catalogue (`behaviors/index.yaml`) plus a
per-session summary from `.forge/runtime/state.json`: counters, effective
levels, override counts, pending_block status, and any session-scope
overrides.

**on / off** — Toggle a behavior's active state.
- `--project` (default): mutates `behaviors/index.yaml`. Persistent.
  After changing, recompile the behavior with
  `scripts/compiler/compile.sh behaviors/<id>/behavior.yaml <output_dir>`
  and restart Claude Code so the new hook registration takes effect.
- `--session SESSION_ID`: mutates only
  `.forge/runtime/state.json`'s `behavior_overrides[]` for that session.
  The compiled hook short-circuits silently when disabled. No recompile
  needed. Effect lasts until the session is purged by TTL.

**strict / relaxed** — Mutate `behaviors/<id>/behavior.yaml` escalation:
- `strict`: halves each `after` threshold, minimum 1. Makes violations
  escalate sooner.
- `relaxed`: doubles each `after` threshold. Makes violations escalate
  later.
- Both project-scope only in v1. Session-scope strictness deferred to
  Phase 2 — the runtime would need to pass a strictness multiplier into
  `forge_resolve_level`, which v1 does not support.

## Preconditions

- `jq` must be installed (runtime requirement).
- `python3` with `pyyaml` must be installed (YAML reading/writing).
- The project must already have `behaviors/index.yaml`. If missing,
  create one with `behaviors: []` and populate via `on <id>`.

## Scope matrix

| Action    | --project        | --session              |
|-----------|------------------|------------------------|
| status    | always shown     | filters to one session |
| on / off  | mutates index.yaml | writes to state.json   |
| strict    | mutates yaml     | (not implemented v1)   |
| relaxed   | mutates yaml     | (not implemented v1)   |

## Example flows

**Check what is active right now:**
```
/forge behavior status
```

**Silence search-first for a noisy debugging session:**
```
/forge behavior off search-first --session <session_id>
```

**Tighten up for strict development mode:**
```
/forge behavior strict search-first
# then recompile and restart
```

## Notes

- The CLI honors `FORGE_BEHAVIORS_DIR` as an override of `behaviors/`
  location — useful for tests and isolated environments.
- Direct tool result for tests: `scripts/forge-behavior/tests/run_all.sh`.
