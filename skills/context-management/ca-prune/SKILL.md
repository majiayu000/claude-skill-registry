---
name: ca-prune
description: Trim transcript clutter to extend session lifetime — analyze, prune a copy, or toggle the after-each-turn service. Dry-run by default; gains land at resume/compaction, not the current turn.
argument-hint: "status | dry | run <path> | audit <path> | on | off"
---

# /ca-prune — session transcript pruner

Long sessions die when their semantic history fills the context window with bulk: oversized tool
outputs, thinking blocks, MCP/shell noise, stale file reads, and host-specific sidecars. The shared
policy trims that bulk at safe quiescence boundaries while each host codec preserves its native
integrity model and the K most recent tool-bearing turns verbatim. Claude keeps byte-safe JSONL
serialization; Pi uses semantic entries and returns a native custom-compaction result.
Gains land at the host's next native resume/restart or compaction boundary, not by mutating the
running session's active file. **Pi-native compaction** is event-driven and never rewrites an active
Pi session file.

## Argument

`$ARGUMENTS` is one of:

- `status` (default) — report cumulative reduction and service state for this session from
  `~/.codearbiter/prune-state.json`, and whether `CODEARBITER_PRUNE` is `on`/`dry`/`off`. When
  the service has run in `dry` mode, every would-be prune is also recorded — one JSONL row per
  decision, across all sessions — to the shared data-collection log
  `~/.codearbiter/metrics/prune-dry.jsonl` (override with `CODEARBITER_PRUNE_METRICS`). That log is
  the evidence base for the `dry`→`on` decision: a clean record (every row `verdict: dry-run`,
  `validation_errors: 0`) over a representative set of sessions is the signal that enabling is safe.
  Read `context_bytes_freed` / `context_est_tokens_freed` for model-context benefit and
  `file_bytes_freed` / `file_pct` for disk and resume-parse benefit. `sidecar-collapse` is explicitly
  `file-only`; it must not count toward the context-benefit or cold-cache decision.
  The legacy `freed_bytes`, `pct`, and `est_tokens_before` / `est_tokens_after` fields remain
  whole-file compatibility aliases; do not use them as model-context evidence.
- `dry` — create a read-only semantic plan (or analyze a scratch copy where the host exposes a
  serialized transcript); present the per-strategy reduction table with every strategy labeled
  `context` or `file-only`. Never writes the active session.
- `run <path>` — prune the target with `--execute`. Targets a **copy or an old/inactive
  transcript only** — the tool refuses an active or recently-modified target by construction.
- `audit <path>` — read-only integrity report: line-parse, uuid chain, tool-pair coverage,
  condensation markers.
- `on` / `off` — guidance on enabling or disabling the after-each-turn service.

## Flow

1. **status / dry / audit** — run the backing tool and present its output verbatim:
   ```
   python3 "<plugin-root>/hooks/prune-transcript.py" <subcommand> [<path>] || python "<plugin-root>/hooks/prune-transcript.py" <subcommand> [<path>]
   ```
   For serialized hosts, `dry` analyzes `<path>.copy.jsonl`; Pi active sessions use the native
   semantic planner and return a custom compaction result without session-file writes.

2. **run** — confirm the path is a copy or an inactive session, then:
   ```
   python3 "<plugin-root>/hooks/prune-transcript.py" <path> --execute [--tier T] || python "<plugin-root>/hooks/prune-transcript.py" <path> --execute [--tier T]
   ```
   Present the per-strategy reduction report; follow with `audit` on the result.

3. **on/off** — explain the after-each-turn service: `UserPromptSubmit` and `PreCompact` hooks
   prune at safe quiescence points, always exit 0, and never block the prompt. Tiers: `gentle`
   (sidecar + oversize clamp), `standard` (+ reasoning fold, aged/MCP/shell), `aggressive`
   (+ stale-read, reminder dedup, image evict). Config via `CODEARBITER_PRUNE` (`off`|`dry`|`on`,
   ships **off**), `CODEARBITER_PRUNE_TIER`, `CODEARBITER_PRUNE_KEEP_RECENT` (the K most recent
   tool **turns** kept verbatim — each turn is an assistant tool_use plus its results),
   `CODEARBITER_PRUNE_MAXBYTES`. Enabling is the user's explicit choice — never set it unbidden.
   In `dry` mode the service writes no transcript but appends each would-be prune to
   `~/.codearbiter/metrics/prune-dry.jsonl` (path override: `CODEARBITER_PRUNE_METRICS`) for
   data collection; in `on` mode the executed prunes are recorded in `~/.codearbiter/prune.log`.
   If a prior service-mode prune was killed mid-write, the next run self-heals the transcript
   from the newest backup in `~/.codearbiter/prune-backups/` before doing anything else.

   **Cold-miss nudge** [Feature Forge — `preview`]: when `CODEARBITER_PRUNE` is `on`, an
   optional submit-time speed bump warns once before a cold cache re-cache lands on bloated
   context. Enable with `CODEARBITER_PRUNE_NUDGE=on` (default `off`). When all arming conditions
   hold (idle ≥ `CODEARBITER_PRUNE_NUDGE_IDLE_SECS`, default 240 s; estimated model-context
   tokens freed ≥
   `CODEARBITER_PRUNE_NUDGE_MIN_TOKENS`, default 80 000), the hook blocks the submit once with
   an advisory on stderr and returns exit code 2. File-only sidecar reduction never arms it. The
   advisory names the approximate avoidable context-token count and the host-native actions that
   move the re-cache to pruned context:
   native compaction or a normal exit + resume/restart. Resubmitting immediately proceeds. The block fires at most
   once per cold window; a subsequent warm submit (idle < floor) resets the window so the next
   genuine cold stretch re-arms. The gate is strictly opt-in, never fires in `dry`/`off` mode,
   and fails open on any error — a pruner fault will never block the session.

## When NOT to use

- Context bar nowhere near compaction — the most recent turns are protected anyway.
- Install health → `/ca-doctor`.
- Project progress → `/ca-status`.

## Hard gate

- MUST NOT run `--execute` against the **live** session's transcript — the tool refuses a
  recently-modified file by construction; manual `run` targets copies or old sessions only.
- MUST surface the native-boundary-only gains limitation whenever a user expects an immediate
  active-file context drop.
- MUST NOT enable the service (`CODEARBITER_PRUNE=on`) on behalf of the user — explain and let
  them decide.
