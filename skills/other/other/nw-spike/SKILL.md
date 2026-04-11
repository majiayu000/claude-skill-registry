---
name: nw-spike
description: "Runs a timeboxed spike to validate one core assumption before DESIGN. Use after DISCUSS when the feature involves a new mechanism, performance requirement, or external integration."
user-invocable: true
argument-hint: "[feature-description] - Example: \"wave-matrix -- derive feature status from pytest + filesystem\""
---

# NW-SPIKE: Timeboxed Assumption Validation

**Wave**: SPIKE (between DISCUSS and DESIGN) | **Agent**: Attila (nw-software-crafter) | **Command**: `/nw-spike`

## Overview

Execute a timeboxed spike (max 1 hour) to validate a single core assumption before investing in architecture design. Produces throwaway code and permanent findings. The spike answers: does the mechanism work, does it meet the performance budget, and what did we assume wrong?

## Skip Check

Before running, verify the spike is needed. If ALL answers are "no", skip and proceed to DESIGN:

1. Is there a new mechanism never tried before in this codebase?
2. Is there a performance requirement that cannot be validated by reasoning alone?
3. Is there an external integration with unknown behavior?

If skipping: tell the user and recommend `/nw-design` directly.

## Prior Wave Consultation

1. **DISCUSS artifacts**: Read `docs/feature/{feature-id}/discuss/` (required)
   - `user-stories.md` -- scope and acceptance criteria
   - `wave-decisions.md` -- constraints and assumptions to test
2. **DIVERGE artifacts**: Read `docs/feature/{feature-id}/diverge/recommendation.md` (if present)

## Interactive Decision Points

### Decision 1: Spike Scope
**Question**: What is the ONE assumption you need to validate?
**Examples**:
1. "Can we parse pytest output reliably in <5 seconds?"
2. "Can the CEL library evaluate 100 expressions in <1 second?"
3. "Can we write to .git/hooks/ from a subprocess without corruption?"

### Decision 2: Performance Budget
**Question**: What is the timing constraint? (Enter "none" if mechanism validation only)
**Examples**:
1. "<5 seconds end-to-end"
2. "<100ms per operation"
3. "Handle 10K items without OOM"

## Agent Invocation

@nw-software-crafter

**SKILL_LOADING**: Before starting, load your spike methodology skill at `~/.claude/skills/nw-spike-methodology/SKILL.md` using the Read tool.

Execute spike for "{feature-description}".

**Spike question**: {Decision 1 answer}
**Performance budget**: {Decision 2 answer}

**Rules**:
- Code goes in `/tmp/spike_{feature_id}/`. Never in `src/`.
- Max 1 hour. No tests, no types, no error handling, no abstractions.
- One file preferred. Two files maximum.
- Use `time.perf_counter()` for timing.
- Print results to stdout.

**After spike completes**:
1. Write findings to `docs/feature/{feature-id}/spike/findings.md`
2. Delete the spike code from `/tmp/`
3. Report the binary verdict: WORKS or DOESN'T WORK

## Progress Tracking

The invoked agent MUST create a task list from its workflow phases at the start of execution using TaskCreate. Each phase becomes a task with the gate condition as completion criterion. Mark tasks in_progress when starting each phase and completed when the gate passes.

## Success Criteria

- [ ] Exactly one assumption tested (not two, not zero)
- [ ] Spike code lives in `/tmp/`, never in `src/`
- [ ] Completed within 1 hour (or escalated with "BIGGER THAN EXPECTED")
- [ ] `findings.md` written with binary verdict, timing, and edge cases
- [ ] Spike code deleted after findings written
- [ ] Design implications documented (what was assumed wrong)

## Next Wave

**Handoff To**: nw-solution-architect (DESIGN wave)
**Deliverables**: `docs/feature/{feature-id}/spike/findings.md`
**Design reads findings before starting** -- spike results override any prior assumptions.

## Wave Decisions Summary

Before completing SPIKE, produce `docs/feature/{feature-id}/spike/wave-decisions.md`:

```markdown
# SPIKE Decisions -- {feature-id}

## Assumption Tested
- {the one question}

## Verdict
- {WORKS / DOESN'T WORK}: {one-line summary}

## Design Implications
- {what DESIGN must account for based on spike results}

## Constraints Discovered
- {any new constraints from edge cases}
```

## Examples

### Example 1: Performance spike
```
/nw-spike "wave-matrix -- derive feature status from pytest + filesystem"
```
Spike question: "Can we collect pytest markers + parse filesystem state in <5 seconds?"
Agent writes 50-line script in `/tmp/spike_wave_matrix/`, discovers pytest collection takes 44 seconds (budget blown). Findings document the correct approach (cache + collect-only). Code deleted. DESIGN proceeds with cache-first architecture.

### Example 2: Integration spike
```
/nw-spike "cel-policy-engine -- evaluate access control expressions"
```
Spike question: "Can cel-python evaluate 100 policy expressions in <1 second?"
Agent installs cel-python, writes evaluation loop, measures 23ms for 100 expressions. Verdict: WORKS. Edge case: nested map access syntax differs from Go CEL. Findings inform DESIGN's expression schema.

### Example 3: Mechanism spike
```
/nw-spike "git-hook-wiring -- install hooks via subprocess"
```
Spike question: "Can we write to .git/hooks/ from a Python subprocess without file corruption?"
Agent writes hook installer, tests with concurrent access. Verdict: WORKS but needs file locking. Edge case: Windows line endings corrupt hook on WSL. Findings feed into DESIGN's cross-platform strategy.

## Expected Outputs

```
docs/feature/{feature-id}/spike/
  findings.md
  wave-decisions.md
```
