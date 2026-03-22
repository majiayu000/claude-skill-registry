---
name: lp-do-assessment-06-distribution-profiling
description: Distribution profiling for new startups (ASSESSMENT-06). Elicits ≥2 launch channels with cost/effort estimates and ICP fit rationale. Produces a distribution-plan artifact ready for measurement profiling. Upstream of lp-do-assessment-07-measurement-profiling.
---

# lp-do-assessment-06-distribution-profiling — Distribution Profiling (ASSESSMENT-06)

Elicits and records the operator's launch distribution plan before measurement planning runs. Identifies ≥2 channels, their cost/effort level, ICP fit rationale, and confirms no fatal resource blockers exist.

## Invocation

```
/lp-do-assessment-06-distribution-profiling --business <BIZ>
```

Required:
- `--business <BIZ>` — 3-4 character business identifier

**Business resolution pre-flight:** If `--business` is absent or the directory `docs/business-os/strategy/<BIZ>/` does not exist, apply `_shared/business-resolution.md` before any other step.

## Operating Mode

ELICIT + WRITE

This skill:
- Reads ASSESSMENT-01 (ICP — who is buying) and ASSESSMENT-03 (selected product — what is being sold)
- Pre-populates a draft artifact from any channel context already documented in strategy docs
- Surfaces gaps and asks the operator to fill or confirm each field
- Writes the final ASSESSMENT-06 artifact

Does NOT:
- Research external channel benchmarks or cost data (that is S6B territory)
- Recommend channels the operator hasn't indicated willingness to use
- Set field values the operator has not confirmed

## Precursor Inputs

Read before eliciting any fields:
- `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-problem-statement.user.md` — ICP Group 1 (primary), Group 2 (secondary)
- `docs/business-os/strategy/<BIZ>/s0c-option-select.user.md` — selected product and scope
- Any existing strategy doc with channel references (plan.user.md, index.user.md, etc.)

## Elicitation Questions

Present as a structured Q&A. Pre-populate from existing docs where possible; mark pre-populated answers as `(pre-filled — confirm or correct)`.

**Section A — Channel List**

For each channel the operator identifies:
1. Channel name and type (e.g. "Etsy — marketplace", "own-site DTC", "Instagram organic", "email list")
2. Cost/effort estimate: low / medium / high (order-of-magnitude only)
3. Fit rationale: why does this channel reach the primary ICP?

Minimum: 2 channels required. Prompt for a second if only one is given.

**Section B — Fatal Blocker Check**

For each channel:
- Does this channel require resources you don't currently have? (budget, team, infrastructure)
- If yes: is there a workaround, or is this channel excluded from the launch plan?

**Section C — Priority Order**

Which channel is primary (launch focus)? Which is secondary (probe/test)?

## Output Artifact

**Path:** `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-launch-distribution-plan.user.md`

**Frontmatter:**
```yaml
---
Type: Distribution-Plan
Stage: ASSESSMENT-06
Business: <BIZ>
Status: Draft
Created: <today>
Updated: <today>
Owner: <operator name>
---
```

**Sections:**

### A) Channel List

| Channel | Type | Cost/Effort | ICP Fit Rationale |
|---|---|---|---|
| <channel 1> | marketplace / DTC / social / etc. | low / medium / high | <why this reaches ICP Group 1> |
| <channel 2> | ... | ... | ... |

### B) Fatal Blocker Check

| Channel | Blocker | Workaround / Status |
|---|---|---|
| <channel> | <none / description> | <n/a / workaround> |

### C) Launch Priority

| Priority | Channel | Rationale |
|---|---|---|
| Primary | <channel> | <brief reason> |
| Secondary | <channel> | <brief reason> |

## Quality Gate

Before saving, verify:
- [ ] ≥2 channels present in Section A
- [ ] All Section A rows have a Cost/Effort value and a fit rationale
- [ ] Section B completed for every channel in Section A
- [ ] No channels with unresolved fatal blockers in launch plan
- [ ] Section C names a primary channel
- [ ] Frontmatter fields all present: Type, Stage, Business, Status, Created, Updated, Owner
- [ ] Artifact saved to correct path before completion message

## Red Flags

Invalid outputs — do not emit:
- Only 1 channel (minimum 2 required for ASSESSMENT gate to pass)
- Channels with "TBD" cost/effort (every channel must have an estimate)
- Fatal blockers without resolution (blocked channels must be marked excluded)
- Section C empty (primary channel must be named)
- Artifact not saved (output must be written to file, not only displayed in chat)

## Completion Message

> "Distribution plan recorded: `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-launch-distribution-plan.user.md`. [N] channels identified; [channel name] primary. Ready for ASSESSMENT-07 Measurement Profiling."

---

## Integration

**Upstream (ASSESSMENT-04):** Runs after `/lp-do-assessment-04-candidate-names --business <BIZ>` returns a naming shortlist.

**Downstream consumer:** `modules/assessment-intake-sync.md` reads `<YYYY-MM-DD>-launch-distribution-plan.user.md` as its fifth precursor (ASSESSMENT-06). Section A channels inform intake Section C (Channel Packet). Section C priority order informs intake Section A (Execution posture).

**Downstream:** `/lp-do-assessment-07-measurement-profiling --business <BIZ>` reads this artifact as input to determine which channels need measurement instrumentation.
