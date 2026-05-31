---
name: done-blocked
description: Reusable reporting contract for any agent that hands work back to the pipeline. Forces ONE of two terminal statuses (DONE or BLOCKED) with a specific evidence shape. Stops vague "probably finished" and "kind of stuck" verdicts.
when_to_use: |
  Apply to every terminal verdict an agent writes — the last line of a spawned agent run, the top of a report file, or the summary appended to a Beads task comment. Specifically:
  - architect ARCH doc completion → DONE or BLOCKED
  - senior-dev task close → DONE or BLOCKED
  - qa-engineer QA report verdict → DONE (PASS) or BLOCKED (FAIL with evidence)
  - security-officer CSO audit verdict → DONE (APPROVED) or BLOCKED (findings)
  - devops deploy step → DONE or BLOCKED
  - l3-support incident triage step → DONE or BLOCKED
  - project-auditor audit completion → DONE or BLOCKED
  Do NOT force this on intermediate progress pings (those are advisory). Only terminal verdicts.
effort: low
allowed-tools: Read, Write, Bash
paths:
  - ".great_cto/verdicts/**"
  - "docs/**"
---

# DONE / BLOCKED Reporting Contract

Terminal status is exactly two states, and BLOCKED requires specific evidence — not vague obstruction reports.

## The contract

Every agent's final handoff line is one of:

```
DONE: <one-sentence summary of what shipped>
  artifact: <path to report/PR/commit>
  next: <who picks this up — pipeline stage, gate, or "pipeline continues">
```

```
BLOCKED: <one-sentence summary of the obstacle>
  tried: <what was attempted — file paths, commands, error signatures>
  failed_because: <concrete reason — not "unclear", not "complex">
  need: <specific unblock — file access, missing config, CTO decision, another agent>
```

## Hard rules

1. **No third state.** "Mostly done", "done with caveats", "almost there" → choose. If caveats exist, the caveat itself decides:
   - Caveat is cosmetic / P2+ → **DONE** (file a Beads bug, move on)
   - Caveat blocks the next pipeline stage → **BLOCKED** (do not pretend)

2. **BLOCKED requires three fields.** `tried` + `failed_because` + `need`. Missing any field → the verdict is rejected and the agent must re-report. No exceptions for "obvious" cases.

3. **Silence is not DONE.** If the agent stops producing output without a terminal line, the parent / next stage treats it as BLOCKED with `failed_because: silent — no terminal verdict written`.

4. **`failed_because` must be concrete.** These are rejected:
   - "environment issue" → say *which* command failed with *what* error
   - "tests failing" → say *which* tests and the actual assertion message
   - "unclear requirements" → say *which* decision is needed and the two options
   - "not enough context" → say *which* file / doc / config you tried to read

5. **`need` names a specific unblock.** These are rejected:
   - "more information" → ask one specific question
   - "help from another agent" → name the agent (architect / security-officer / …)
   - "CTO approval" → state the exact choice (approve gate X, pick option A vs B, waive check)

## Where the verdict goes

Every agent writes the verdict to **two places**:

1. **Last line of agent output** (visible to the orchestrator that spawned it).
2. **`.great_cto/verdicts/<agent>-<YYYY-MM-DD-HHMMSS>.log`** — append-only audit trail.

```bash
mkdir -p .great_cto/verdicts
VERDICT_FILE=".great_cto/verdicts/<agent>-$(date -u +%Y-%m-%d-%H%M%S).log"
printf '%s\n' "$VERDICT_LINE" > "$VERDICT_FILE"
```

## Examples

**Good — DONE:**
```
DONE: CSO audit passed — 0 P0, 2 P1 findings filed as Beads tasks.
  artifact: docs/security/CSO-2026-04-19.md
  next: gate:ship ready for CTO approval
```

**Good — BLOCKED:**
```
BLOCKED: senior-dev cannot claim task BD-42 — circular dependency with BD-38.
  tried: bd ready → BD-42 did not appear; bd dep tree BD-42 → shows BD-38 blocks BD-42, BD-42 blocks BD-38
  failed_because: both tasks depend on each other transitively (BD-42 → BD-38 → BD-39 → BD-42)
  need: architect to split BD-39 into two tasks so the cycle breaks
```

**Rejected — vague BLOCKED:**
```
BLOCKED: couldn't finish QA — environment problems.
  tried: ran tests
  failed_because: stuff broken
  need: help
```
Why rejected: `tried` lacks command/path; `failed_because` is tautological; `need` is not actionable.

## Measuring the contract

`.great_cto/verdicts/*.log` is machine-readable. Weekly digest can compute:
- `DONE:BLOCKED` ratio per agent — too many BLOCKED from one agent = that role is under-resourced or prompt is unclear
- `failed_because` clustering — if the same reason appears 3+ times, that's a recurring obstruction worth a meta-fix (tooling, doc, skill)
- Silence rate (agents with no terminal verdict written) — should trend to zero

## Anti-patterns

- Writing both DONE and BLOCKED in the same report ("DONE but blocked on X"). Pick one. If you're blocked, the work isn't done.
- Using DONE as a politeness signal when the gate still fails. The verdict is for the machine, not the CTO's feelings.
- Writing the verdict only to stdout without persisting to `.great_cto/verdicts/`. The audit trail is what makes the contract measurable.
