---
name: ghm-gate-check
description: >
  Validates gate criteria before PRD lifecycle advancement by delegating to
  the readiness scoring pipeline (scripts/readiness.py). Returns a graduated
  PASS / WARN / BLOCK verdict with top blockers and their causal chain.
  Triggers before advancing from v0.X to v0.Y or explicit `/ghm-gate-check`.
context: inline
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# Gate Check

Validate whether the PRD stage is ready to advance to the next version. Delegates to the three-layer readiness scorer — SoT files → EPICs → stage — then surfaces the leverage view (what to fix first, and which EPICs it unblocks).

## Workflow Overview

1. **Compute** → run `scripts/readiness.py run --quiet` to refresh `status/readiness.json`
2. **Read** → parse `status/readiness.json`
3. **Report** → PASS / WARN / BLOCK verdict with top blockers and causal links
4. **Recommend** → actionable next steps (always highest-leverage first)

## Authority

`references/gate-criteria.md` remains the canonical source of mandatory artifacts per gate. The scorer's `GATE_REQUIREMENTS` table mirrors it. Do not hand-roll checklists here — the scoring engine is the single source of truth.

## Step 1: Compute

Run the orchestrator. It runs SoT → EPIC → stage in dependency order and writes `status/readiness.json`.

```bash
python scripts/readiness.py run --quiet
# exit 0 = all pass, 1 = warn, 2 = block, 3 = error
```

If the exit code is `3`, report a runtime error and stop. If `0/1/2`, proceed to Step 2.

### Fallback: no scripts available

If `scripts/readiness.py` is missing or Python is unavailable, fall back to reading `status/readiness.json` directly. If that's also absent, report: "Readiness not yet computed — install scripts/requirements.txt and run `python scripts/readiness.py run`."

## Step 2: Read

```bash
cat status/readiness.json
```

Extract:
- `summary.current_stage` — the gate being evaluated and its score
- `summary.top_blockers` — ranked SoT files blocking progress
- `stages.{target}` — detailed stage block (dimensions, unmet_criteria, caps)
- `epics.{id}` — per-EPIC scores (cite the lowest ones)

## Step 3: Report

Use this template. Fill every field from the JSON — do not improvise scores.

```markdown
## Gate Check Report: {stage.gate_description}

**Verdict**: [PASS | WARN | BLOCK]
**Stage Score**: {stage.score} / 100  (warn < {threshold_warn}, block < {threshold_block})
**Date**: {now}

### Stage Dimensions

| Dimension | Score | Weight |
|-----------|-------|--------|
| required_ids_present | {score} | {weight} |
| relevant_sot_readiness | {score} | {weight} |
| cross_ref_integrity | {score} | {weight} |
| downstream_epic_readiness | {score or "n/a"} | {weight or "—"} |

### Top Blockers (leverage view)

1. **{file}** (score {score}) — blocks {N} EPICs: {EPIC-XX, …} — impact {impact}
2. …

### Unmet Criteria (high severity first)

- [high] {ref}: {reason}
- [medium] {ref}: {reason}

### Recommendation

**If PASS**: Advance to {next_version}. Run `ghm-status-sync` to update the README dashboard.

**If WARN / BLOCK**: Do not advance. Address top blockers in order — fixing the highest-impact SoT file cascades up the graph.

**Next action**: {top_blockers[0] → concrete fix}
```

### Verdict bands

| Stage score | Verdict | Meaning |
|---|---|---|
| ≥ 70 | PASS | Safe to advance |
| 50–69 | WARN | Advance with documented risk; log in PRD change log |
| < 50 | BLOCK | Cannot advance — per rule 05-lifecycle-gates, update the EPIC and STOP |

## Step 4: Recommend

Always prioritize by `impact = (100 − score) × #EPICs blocked`. The top blocker is the single highest-leverage fix; cite its `blocking_epics` list so the human understands what unblocks.

## Quality Gates

- [ ] Stage score cited from JSON, not estimated
- [ ] Top blockers include their consumer EPICs
- [ ] Recommendation is actionable (specific file, specific action)
- [ ] Verdict matches the score band exactly (don't round up)

## Anti-Patterns

| Pattern | Example | Fix |
|---|---|---|
| Ignoring the score | "Feels ready; pass" | Cite `stage.score` verbatim |
| Skipping blockers | "Minor stuff, advance anyway" | Block if score < 50; warn if < 70 |
| Hand-rolling criteria | Re-checking IDs manually | Trust the scorer; if wrong, fix `GATE_REQUIREMENTS` in `_readiness/stage.py` |
| Forcing PASS | Overriding the verdict | Never override; the score is the contract |

## Boundaries

**DO**:
- Delegate computation to `readiness.py`
- Cite specific scores, files, and EPICs from the JSON
- Surface the `top_blockers` leverage view

**DON'T**:
- Modify `status/readiness.json` directly — it's computed output
- Create missing artifacts inside this skill (that's the author's job)
- Override PASS/BLOCK verdicts subjectively

## Handoff

After a report:
- **PASS**: Trigger `ghm-status-sync`; the gate advancement updates the README dashboard
- **WARN**: Same as PASS but note the risks in the PRD change log
- **BLOCK**: Return control to the human. The `top_blockers[0]` fix is the single most important next action

## References

- `references/gate-criteria.md` — canonical gate requirements (consumed by scorer)
- `references/examples.md` — pass/warn/block report examples
- `.claude/rules/07-readiness-protocol.md` — the discipline rule
- `docs/READINESS_PROTOCOL.md` — full schema
