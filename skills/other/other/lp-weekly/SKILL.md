---
name: lp-weekly
description: S10 weekly orchestration wrapper. Coordinates the full weekly decision, audit/CI, measurement compilation, and experiment lane flows into one deterministic sequence. Additive-first; never replaces canonical S10 authorities. No new hard stage blocks in first iteration.
---

# lp-weekly — S10 Weekly Orchestrator

`/lp-weekly` is the S10 orchestration entrypoint. It coordinates existing weekly flows into one deterministic sequence and emits an additive weekly packet. It does NOT replace stage graph authority or weekly decision-prompt authority.

## Authority Stack

| Surface | Authority | Non-authority |
|---|---|---|
| `docs/business-os/startup-loop/specifications/loop-spec.yaml` | Stage graph, stage ordering | Not weekly memo content |
| `docs/business-os/workflow-prompts/_templates/weekly-kpcs-decision-prompt.md` | Weekly decision content (Sections A–H) | Not stage graph |
| `/lp-weekly` | Execution order, preflight checks, lane sequencing, packetization, cross-artifact linking | Does NOT replace prompt authority or stage graph authority |

## Invocation

```
/lp-weekly --biz <BIZ> --week <YYYY-Www> [--as-of-date <YYYY-MM-DD>] [--run-root <path>]
```

### Parameters

| Parameter | Required | Default | Notes |
|---|---|---|---|
| `--biz` | Required | — | Business identifier (e.g., `BRIK`, `PET`). Must match a directory under `docs/business-os/strategy/`. |
| `--week` | Required | — | ISO week key, UTC Monday anchor. Format: `YYYY-Www` (e.g., `2026-W07`). Derived from invocation date if not supplied; operator may override. |
| `--as-of-date` | Optional | Today (YYYY-MM-DD) | Used for artifact naming and week key derivation. |
| `--run-root` | Optional | `docs/business-os/strategy/<BIZ>/` | Path prefix for stage artifacts. Deterministically derived from `--biz` when omitted. |

### Week key derivation rule

Derived from UTC date at invocation using ISO 8601 week numbering. Week boundary: Monday 00:00:00 UTC to Sunday 23:59:59 UTC. Zero-padded two-digit week number, e.g., `2026-W07`.

## Global Invariants

### Operating mode

**ORCHESTRATE + SEQUENCE + EMIT**

### Allowed actions

- Read stage artifacts, KPI sources, prior-week packet, and canonical prompt docs.
- Invoke sub-flows: GATE-LOOP-GAP-03 feedback-loop audit, `/lp-experiment readout` (per experiment), KPCS prompt handoff.
- Write one weekly packet per `YYYY-Www` key (overwrite in-place on rerun).
- Emit lane status summaries and REM delta sections within the packet.

### Prohibited actions

- Replacing or modifying the canonical weekly KPCS decision memo.
- Introducing new hard stage blocks or gate-semantics changes (first iteration no-block posture).
- Modifying `docs/business-os/startup-loop/specifications/loop-spec.yaml` stage graph.
- Removing or suppressing GATE-BD-08 or GATE-LOOP-GAP-03 dispatch behaviors.
- Silent failure: partial inputs must produce `restricted` lane state + REM, not silent degraded output.
- Destructive shell or git commands.
- Creating files outside the weekly packet and its cross-artifact links.

## Module Routing

Execute modules in sequence:

| Step | Module | Sequence role |
|---|---|---|
| 1 | `modules/preflight.md` | Validate inputs; determine `ready` or `restricted`; emit missing-input list |
| 2–5 | `modules/orchestrate.md` | Compile measurements; execute decisioning handoff; run audit/CI lane (`a`); roll up experiments lane (`c`) |
| 6 | `modules/publish.md` | Emit additive weekly packet; update latest pointer; record lane statuses |

See each module for detailed sub-step sequencing.

## Lane Summary

| Lane | ID | Sequence steps | Exit |
|---|---|---|---|
| Audit + CI | `a` | Steps 3–4 (orchestrate.md) | `complete` or `incomplete` |
| Measurement + reporting | `b` | Step 2 (orchestrate.md) | `ready` or `restricted` |
| Next experiments | `c` | Step 5 (orchestrate.md) | `complete` or `carry-forward` |

## Idempotency

Packet path is fixed per week key: `docs/business-os/strategy/<BIZ>/s10-weekly-packet-<YYYY-Www>.md`.
On rerun for the same week key: overwrite in-place. No version-suffix copies. Git history is the audit trail.
All canonical artifact references are re-linked in the overwritten packet; they are never deleted.

## Output Contract

**Weekly packet**: `docs/business-os/strategy/<BIZ>/s10-weekly-packet-<YYYY-Www>.md`

Required packet sections:
- `week_key`: `YYYY-Www`
- `biz`: business identifier
- `as_of_date`: invocation date
- `preflight_status`: `ready` or `restricted`
- `missing_inputs`: list (empty if `ready`)
- `lane_a_status`: `complete` | `incomplete`
- `lane_b_status`: `ready` | `restricted`
- `lane_c_status`: `complete` | `carry-forward`
- `kpcs_decision_ref`: path to canonical KPCS decision artifact
- `feedback_audit_ref`: path to feedback loop audit artifact (if exists this cycle)
- `measurement_summary`: normalized measurement summary or `restricted` note
- `rem_delta`: new and resolved REM items this week
- `experiment_portfolio_summary`: rollup of active/completed experiments
- `next_cycle_backlog_delta`: new next-experiment specs added or carried forward
- `pending_reviews_delta`: new R9 flags, review items, stale queue packets, and resolved items found by the Lane A pending reviews scan (Step 4.8)
- `run_trace`: list of sub-flows invoked with their outcomes

**Restricted lane state**: when lane `b` inputs are incomplete, `lane_b_status` is set to `restricted`. A REM task is emitted identifying the missing denominator or KPI family. The packet is still written; the operator is not blocked from closing the weekly cycle.

## Exit Conditions

| Condition | Description | Packet emitted? |
|---|---|---|
| `complete` | All lanes reached exit or documented carry-forward; packet written | Yes |
| `partial` | Preflight passed but one or more lanes are `incomplete` or `restricted`; REM emitted per incomplete lane | Yes |
| `restricted` | Preflight returned `restricted`; critical inputs missing; packet written with `preflight_status: restricted` | Yes (restricted) |
| `fail-closed` | `--biz` does not exist, or `--week` cannot be derived, or `run_root` is missing | No |

## Integration

**Sub-flows invoked by `/lp-weekly`:**
- GATE-LOOP-GAP-03 feedback-loop audit — pre-decision advisory input (lane `a`)
- KPCS decision prompt handoff — authoritative weekly decision (step 3, decisioning)
- `/lp-experiment readout` — per-experiment readout (lane `c`, experiment rollup step)

**Startup-loop integration (Phase 1):**
During S10 advance, `/startup-loop` routes through `/lp-weekly` before returning to standard BOS sync and advance flow. See `.claude/skills/startup-loop/modules/cmd-advance.md` for Phase 1 dispatch invocation.

**Canonical artifacts produced outside `/lp-weekly` (referenced, not replaced):**
- `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-weekly-kpcs-decision.user.md`
- `docs/business-os/strategy/<BIZ>/feedback-loop-audit-<YYYY-MM-DD>.md`
- `docs/business-os/strategy/<BIZ>/<YYYY-MM>-monthly-audit.user.md`

## Orchestration Contract

Full S10 sequence, lane contracts, authority isolation, and idempotency rules:
`docs/business-os/startup-loop/contracts/s10-weekly-orchestration-contract-v1.md`
