<!-- SOURCE-OF-TRUTH: shared/references/loop_health_contract.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Loop Health Contract

**Version:** 1.0.0
**Last Updated:** 2026-04-25

> **Paths:** All paths are relative to the skills repository root.

## Purpose

Loop health is retry-usefulness evidence. It does not replace lifecycle status, checkpoints, artifacts, task board status, or domain verdicts.

Use it when a procedural skill can repeat a task, worker, stage, scenario segment, advisor session, or quality cycle.

## Model

| Field | Meaning | Owner |
|-------|---------|-------|
| `status` | workflow location now | existing runtime state |
| `artifact` / `checkpoint` | completion evidence | runtime artifact/checkpoint layer |
| `loop_health` | whether another retry can add value | coordinator/orchestrator runtime |

## Signal Classes

| Class | Retry action |
|-------|--------------|
| `none` | continue normally |
| `timeout_idle` | retry only while loop health allows |
| `timeout_productive` | verify/review before retry |
| `permission_denial` | pause immediately |
| `tool_missing` | pause immediately |
| `auth_missing` | pause immediately |
| `rate_limited` | pause/defer; not a domain failure |
| `asked_question` | pause for decision or refine prompt |
| `agent_error` | retry only while loop health allows |
| `unknown` | retry only while loop health allows |

## Default Policy

| Policy | Value |
|--------|-------|
| `no_progress_limit` | `3` |
| `same_error_limit` | `3` |
| immediate pause | `permission_denial`, `tool_missing`, `auth_missing` |
| progress reset | any confirmed objective progress |

Valid progress evidence includes new/changed artifacts, checkpoint deltas, task/status transitions, changed finding sets, accepted repairs, changed metrics, new bottlenecks, or benchmark improvements.

Do not treat repeated prose, identical findings, or unchanged failed assertions as progress.

## Pause Output

When loop health pauses a flow, include scope, reason, evidence key/error signature, and the next operator decision or missing dependency.

## Runtime Requirements

- `loop_health` remains optional so existing runtime state stays readable.
- Runtime history records loop-health updates as `LOOP_HEALTH_RECORDED`.
- Domain counters remain domain counters; loop health measures whether another retry is useful.
- Transport/agent failures must not become domain verdicts without domain evidence.
