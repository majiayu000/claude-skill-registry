---
name: nw-spike
description: "Runs a timeboxed PROBE to validate one core assumption, then optionally PROMOTES the probe into a walking skeleton — the first e2e thin slice of the feature, committed and demo-able. Use after DISCUSS when the feature involves a new mechanism, performance requirement, or external integration."
user-invocable: true
argument-hint: "[feature-description] - Example: \"wave-matrix -- derive feature status from pytest + filesystem\""
---

# NW-SPIKE: Probe → Walking Skeleton

**Wave**: SPIKE (between DISCUSS and DESIGN) | **Agent**: Attila (nw-software-crafter) | **Command**: `/nw-spike`

## Overview

Execute a two-phase wave that turns a risky assumption into visible, iterable value as fast as possible:

1. **PROBE** — quick throwaway validation of one core assumption (30-60 min, code in `/tmp/`)
2. **PROMOTION GATE** (interactive) — ask the user whether to promote the probe
3. **WALKING SKELETON** — refactor the probe into an end-to-end thin slice committed to the repository (1-3 h, code in `src/` + 1 acceptance test)

The PROBE answers "does the mechanism work?". The WALKING SKELETON answers "can a user see it working end-to-end?". You never throw away working validated code — you promote it and iterate.

## When to use

The spike is needed when the feature introduces:
- A new mechanism never tried in this codebase
- A performance requirement that cannot be validated by reasoning alone
- An external integration with unknown behaviour

If none of the above apply, skip SPIKE and go to DESIGN.

## Prior Wave Consultation

1. **DISCUSS artifacts**: Read `docs/feature/{feature-id}/discuss/` (required)
   - `user-stories.md` — scope and acceptance criteria
   - `wave-decisions.md` — constraints and assumptions to test
2. **DIVERGE artifacts**: Read `docs/feature/{feature-id}/diverge/recommendation.md` (if present)

## Interactive decision points (Phase 1 entry)

### Decision 1: Probe scope
**Question**: What is the ONE assumption you need to validate?
**Examples**:
- "Can we parse pytest output reliably in <5 seconds?"
- "Can the CEL library evaluate 100 expressions in <1 second?"
- "Can we write to `.git/hooks/` from a subprocess without corruption?"

### Decision 2: Performance budget
**Question**: What is the timing constraint? (Enter "none" if mechanism validation only)
**Examples**:
- "<5 seconds end-to-end"
- "<100ms per operation"
- "Handle 10K items without OOM"

### Decision 3: End-to-end path preview
**Question**: If this probe works, what would the thinnest end-to-end slice look like?
Capture the rough path: `user-facing entry → business logic → persistence/services → user-visible output`. This is **not** a commitment — it's context for the promotion gate later.

## Phase 1 — PROBE

Throwaway validation of the assumption.

### Agent invocation

@nw-software-crafter

Execute PROBE for "{feature-description}".

**Probe question**: {Decision 1 answer}
**Performance budget**: {Decision 2 answer}
**Target e2e path (for later)**: {Decision 3 answer}

**Rules**:
- Code goes in `/tmp/spike_{feature_id}/`. Never in `src/`.
- Max 1 hour. No tests, no types, no error handling, no abstractions.
- One file preferred. Two files maximum.
- Use `time.perf_counter()` for timing.
- Print results to stdout.

**After probe completes**:
1. Write findings to `docs/feature/{feature-id}/spike/findings.md` — binary verdict (WORKS / DOESN'T WORK), timing, edge cases, design implications.
2. Do **not** delete the probe code yet — wait for the promotion gate.
3. Report verdict and ask the orchestrator to run the promotion gate.

## Phase 2 — PROMOTION GATE (interactive)

Run this gate **only after** the probe completes and findings.md is written.

Present the user with three choices:

| Choice | When to pick | Outcome |
|---|---|---|
| **PROMOTE** | Probe verdict is WORKS and the mechanism is worth building on | Proceed to Phase 3 — walking skeleton |
| **DISCARD** | Probe verdict is WORKS but not worth pursuing (findings are enough) | Delete `/tmp/spike_{feature_id}/`. Commit `findings.md`. Hand off to DESIGN. |
| **PIVOT** | Probe verdict is DOESN'T WORK or revealed a better approach | Delete probe code. Annotate `findings.md` with the pivot. Either loop back to DISCUSS or run a second probe. |

**Default**: if the probe verdict is WORKS and no reason to stop, recommend PROMOTE but let the user override.

Record the promotion decision in `docs/feature/{feature-id}/spike/wave-decisions.md` as an explicit wave decision with rationale.

## Phase 3 — WALKING SKELETON (only if PROMOTE)

Refactor the probe into the thinnest end-to-end slice that is committed, tested, and demo-able.

### Definition of Done (walking skeleton)

1. **End-to-end path**: the slice enters from a real user-facing entry point (CLI command, HTTP endpoint, UI action, hook) and exits at a real user-visible output (stdout, HTTP response, rendered screen, persisted file). Every layer in between is exercised — **no layer is mocked** unless that layer is an external paid service classified as costly in DISTILL's Walking Skeleton Strategy (then use the fake/contract test pattern).
2. **One acceptance test**: a `@walking_skeleton @driving_port` tagged scenario in `tests/{test-type-path}/{feature-id}/acceptance/walking-skeleton.feature`. The scenario MUST be green before hand-off.
3. **Production location**: code lives under `src/{production-path}/`, not in `/tmp/`. Minimal module skeleton is fine — no premature abstractions, no features beyond the walking skeleton.
4. **Committed**: the walking skeleton commit message is `feat({feature-id}): walking skeleton — {one-line description}`.
5. **Demo-able**: running the single acceptance test (or the real entry-point command) produces visible output that matches the user story from DISCUSS.
6. **Back-propagation**: if building the skeleton reveals a contradiction with DISCUSS or DESIGN, write the contradiction to `docs/feature/{feature-id}/spike/upstream-issues.md` and stop — do not hand off to DISTILL until resolved.

### Agent invocation (Phase 3)

@nw-software-crafter

Promote probe for "{feature-description}" into a walking skeleton.

**Source probe**: `/tmp/spike_{feature_id}/`
**Target driving adapter**: {from Decision 3, refined with user}
**Target acceptance test path**: `tests/{test-type-path}/{feature-id}/acceptance/walking-skeleton.feature`

**Rules**:
- Max 3 hours. Stop and escalate if over budget.
- One acceptance test only. No unit tests unless they are strictly required to make the acceptance test pass.
- No premature abstractions. The skeleton should be obviously incomplete — only the single path from the user story works. Error paths, edge cases, and other scenarios are DISTILL's job.
- Use the real driving adapter, the real domain code, the real driven adapter. In-memory doubles only for costly external services.
- Delete `/tmp/spike_{feature_id}/` after promotion.

### Walking skeleton commit checklist

- [ ] 1 acceptance test @walking_skeleton green
- [ ] Real user-facing entry point exercised (not a service function call)
- [ ] Real driven adapters for local resources (filesystem, git, subprocess, SQLite)
- [ ] Code in `src/`, not `/tmp/`
- [ ] Committed with conventional commit message
- [ ] Probe directory deleted
- [ ] Findings.md includes the "promoted on {date}" note

## Progress tracking

The invoked agent MUST create a task list from its workflow phases at the start of execution using TaskCreate. Each phase becomes a task with the gate condition as completion criterion. Phase 1, Phase 2, and Phase 3 are separate task groups — Phase 3 tasks are only created if the promotion gate says PROMOTE.

## Success criteria

### Phase 1 (always)
- [ ] Exactly one assumption tested (not two, not zero)
- [ ] Probe code lives in `/tmp/`, never in `src/`
- [ ] Completed within 1 hour (or escalated with "BIGGER THAN EXPECTED")
- [ ] `findings.md` written with binary verdict, timing, and edge cases

### Phase 2 (always)
- [ ] Promotion gate decision captured in `wave-decisions.md`
- [ ] One of: PROMOTE / DISCARD / PIVOT selected by user

### Phase 3 (only if PROMOTE)
- [ ] Walking skeleton acceptance test green
- [ ] E2E path exercised through all non-costly layers
- [ ] Skeleton code in `src/`, committed
- [ ] Probe directory deleted
- [ ] No upstream contradictions left unresolved

## Next wave

**Handoff to**: nw-solution-architect (DESIGN) — DESIGN reads findings.md and the walking skeleton (if promoted) before starting. The skeleton is a fait accompli — DESIGN designs the rest of the feature around it, not in place of it.

**DISTILL** (next wave after DESIGN) reads the walking skeleton as a prior artifact and adds additional scenarios and integration tests on top of it — it does not write the walking skeleton from scratch.

## Wave decisions summary

Before completing SPIKE, produce `docs/feature/{feature-id}/spike/wave-decisions.md`:

```markdown
# SPIKE Decisions -- {feature-id}

## Assumption Tested
- {the one question}

## Probe Verdict
- {WORKS / DOESN'T WORK}: {one-line summary}

## Promotion Decision
- {PROMOTE / DISCARD / PIVOT}: {rationale}

## Walking Skeleton (only if PROMOTE)
- Driving adapter: {entry point}
- Acceptance test: {path to .feature file}
- Commit: {commit sha of walking skeleton}
- Demo command: {how to run the skeleton}

## Design Implications
- {what DESIGN must account for based on probe results and skeleton learnings}

## Constraints Discovered
- {any new constraints from edge cases}
```

## Examples

### Example 1: Performance probe → promoted skeleton
```
/nw-spike "wave-matrix -- derive feature status from pytest + filesystem"
```
Probe question: "Can we collect pytest markers + parse filesystem state in <5 seconds?"
Agent writes 50-line script in `/tmp/spike_wave_matrix/`. Result: 44 seconds (budget blown), but discovers `pytest --collect-only --cache-only` completes in 200 ms.
**Gate**: user picks **PROMOTE** with the cache-only approach.
Phase 3: agent refactors the probe into `src/des/cli/wave_matrix.py` with a `wave-matrix` CLI command; one acceptance test exercises `subprocess.run(["wave-matrix", "--feature", "alpha"])` end-to-end and asserts the markdown output contains a row for `alpha`.
DESIGN now designs the rest (multi-feature aggregation, cell navigation, refresh strategy) around the already-working skeleton.

### Example 2: Integration probe → discard
```
/nw-spike "cel-policy-engine -- evaluate access control expressions"
```
Probe question: "Can cel-python evaluate 100 policy expressions in <1 second?"
Agent installs cel-python, writes evaluation loop, measures 23 ms for 100 expressions. Verdict: WORKS. Edge case: nested map access syntax differs from Go CEL.
**Gate**: user picks **DISCARD** — the findings are enough, the real access-control feature is large enough to deserve its own design wave.
Phase 3 skipped. Findings committed. DESIGN reads findings.md.

### Example 3: Mechanism probe → pivot
```
/nw-spike "git-hook-wiring -- install hooks via subprocess"
```
Probe question: "Can we write to `.git/hooks/` from a Python subprocess without file corruption?"
Agent tries concurrent access, discovers that the real risk is not corruption but the existing user hook being silently overwritten.
**Gate**: user picks **PIVOT** — the real question is "how do we install alongside existing user hooks?". Findings annotated with the pivot, new probe scheduled.

## Expected outputs

```
docs/feature/{feature-id}/spike/
  findings.md           # always
  wave-decisions.md     # always (with promotion decision)
  upstream-issues.md    # only if skeleton revealed prior-wave contradictions

src/{production-path}/  # only if PROMOTE
  {module}.py           # minimal walking skeleton

tests/{test-type-path}/{feature-id}/acceptance/
  walking-skeleton.feature  # only if PROMOTE — 1 scenario, @walking_skeleton @driving_port
  steps/                    # only if PROMOTE
```
