---
name: idea-option-forge
user-invocable: false
description: |-
  Use when generating, winnowing, and operationalizing many project improvement options.
  Triggers:
practices:
- lean-startup
- pragmatic-programmer
hexagonal_role: domain
consumes:
- existing-tracked-work
produces:
- vetted-idea-backlog
- tracked-issues-with-deps-and-tests
context_rel:
- kind: shared-kernel
  with: brainstorm
skill_api_version: 1
context:
  window: inherit
  intent:
    mode: task
  sections:
    exclude: [HISTORY]
metadata:
  tier: judgment
  dependencies: []
  stability: experimental
output_contract: "A vetted idea ledger (in plan space) + a set of self-documenting tracked issues (br beads) for the winners, each with dependencies and at least one test task; no implementation code is written by this skill."
---

# idea-option-forge — generate, winnow, operationalize

Turn a vague "make this project better" into a vetted, dependency-ordered backlog of
tracked issues. The method is a funnel run **entirely in plan space**: produce far more
ideas than you'll keep, reason each one through, cut hard to the best few, deepen those,
reconcile against what's already tracked, and only then operationalize the survivors into
self-documenting issues with dependencies and test tasks. Implementation comes later.

## ⚠️ Critical Constraints

- **Stay in plan space until the funnel is done.** Do NOT open files to edit or write
  implementation code during generate/winnow/expand. **Why:** the value is divergence then
  ruthless selection; jumping to code collapses the funnel to the first idea and wastes the
  other 29. The only artifacts produced are the idea ledger and tracked issues.
- **Generate WIDE before judging.** Produce the full ~30 before evaluating any of them.
  **Why:** interleaving generation and judgment anchors you and kills the long tail where
  the best ideas usually hide.
  - WRONG: "Here's idea 1 — and it's great, let's file it." (judging mid-generation)
  - CORRECT: list 30 candidates first; evaluation is a separate later pass.
- **Overlap-check against existing tracked work BEFORE filing.** Query the tracker and
  reconcile. **Why:** filing a duplicate of an open bead pollutes the backlog and erodes
  trust in it. A winner that overlaps an existing issue MERGES into it, it does not spawn a
  twin.
- **Issues must be self-documenting.** Each filed issue carries enough context (problem,
  rationale, acceptance check) to be picked up cold. **Why:** an issue that only makes sense
  to its author at filing time is unusable by the next agent and rots.
- **Every winner ships with at least one test task.** **Why:** an improvement with no way
  to verify it landed is unfalsifiable; the test task is the proof surface.

## Why This Exists

Naive "improve this project" requests produce one of two failure modes: a single shallow
idea implemented immediately, or a sprawling unstructured wishlist nobody can act on. This
skill imposes a disciplined funnel — wide generation, hard winnowing, focused expansion,
overlap reconciliation, then operationalization — so the output is a small set of *vetted,
dependency-ordered, testable* tracked issues instead of noise. The plan-space refinement
loop (several passes before implementation) is what separates a real backlog from a
brain-dump. See [the methodology reference](references/methodology.md) for the full per-phase
mechanics and [the prompts reference](references/prompts.md) for copy-paste prompt blocks.

## Quick Start

```text
1. Frame the project + the improvement axis (perf? DX? reliability? UX? cost?).
2. GENERATE ~30 candidate improvements (wide; no judging yet).
3. THINK each through: one line of upside, cost, and risk per idea.
4. WINNOW to the best 5 (explicit cut criteria; record why the rest were cut).
5. EXPAND the 5 into ~15 concrete sub-ideas (3-ish each).
6. OVERLAP-CHECK the ~15 against existing tracked work (`br list` / `br ready`).
7. OPERATIONALIZE survivors into self-documenting br issues + deps + test tasks.
8. REFINE in plan space over several passes; only then implement.
```

## Methodology (the funnel)

Each phase has a verification checkpoint — do not advance until it passes. Full mechanics
and rationale per phase are in [references/methodology.md](references/methodology.md).

| Phase | Do | Checkpoint before advancing |
|---|---|---|
| 1. Frame | State the project and the improvement axis in one sentence. | The axis is concrete (not "make it better"). |
| 2. Generate | List ~30 candidate improvements, numbered. No evaluation. | Count ≥ 25; long tail present (not 30 variants of one idea). |
| 3. Think | One line each: upside / cost / risk. | Every candidate has all three. |
| 4. Winnow | Cut to the best 5 against stated criteria; record cut reasons. | Exactly ~5 survive; each cut has a recorded reason. |
| 5. Expand | Break each survivor into ~3 concrete sub-ideas (~15 total). | Each survivor is decomposed into actionable pieces. |
| 6. Overlap | Compare the ~15 to existing tracked work; merge/drop dupes. | Every survivor is checked against the tracker. |
| 7. Operationalize | File self-documenting br issues + dependencies + test tasks. | Each issue is self-documenting and has ≥1 test task. |
| 8. Refine | Re-read the filed set in plan space; reorder/split/merge. Repeat. | The backlog is dependency-ordered and stable across a pass. |

### Phase 6 — overlap-check against tracked work

Before filing anything, enumerate what already exists and reconcile:

```bash
br list            # all tracked issues for this project
br ready           # what's already actionable
```

For each of the ~15 survivors decide: **NEW** (file it), **MERGE** (fold into an existing
issue — add context to it instead), or **DROP** (already covered). Record the decision.

### Phase 7 — operationalize into self-documenting issues

File each NEW survivor as a tracked issue whose body answers, on its own: what's the
problem, why does it matter, what does "done" look like. Then wire dependencies and add a
test task. See [references/prompts.md](references/prompts.md) for the exact issue-body
template and the THE EXACT PROMPT blocks.

```bash
# File the improvement (self-documenting body via -d), then a verification child.
br create "Improve X: <one-line outcome>" -d "<problem / rationale / acceptance check>"
br create "Test: verify X landed" -d "<how to prove the improvement is real>"
# Wire the test task to depend on the improvement, and chain prerequisite improvements.
br dep add <test-id> <improvement-id>
br dep add <dependent-improvement-id> <prerequisite-improvement-id>
```

### Phase 8 — refine in plan space

Re-read the filed set as a whole, several passes, **before writing any code**: split issues
that are too big, merge near-duplicates that survived, fix the dependency order so `br ready`
surfaces the right first move. The backlog is done when a full pass changes nothing.

## Output Specification

- **Idea ledger (plan space):** the numbered ~30 → ~5 → ~15 funnel with think-notes and cut
  reasons. Kept in the working conversation/plan; not a committed file unless asked.
- **Tracked issues:** one self-documenting `br` issue per NEW winner, each with wired
  dependencies and at least one child test task. This is the durable artifact.
- **Filename / location:** issues live in the project's `br` tracker (`.beads/`); no source
  files are created or edited by this skill.

## Quality Rubric

- The generate phase produced ≥ 25 distinct candidates with a real long tail (verifiable by
  counting the ledger; not 30 rewordings of one idea).
- Every filed issue is self-documenting: a cold reader can act on its body without the
  original conversation (verifiable by reading the issue alone).
- Every winner has ≥ 1 dependent test task and the dependency graph is acyclic and orders
  the work (verifiable: `br ready` surfaces only unblocked roots).
- No filed issue duplicates an existing tracked one (verifiable: each survivor has a recorded
  NEW/MERGE/DROP overlap decision).

## Examples

**Improve a CLI's startup time (axis = performance).** Generate 30 (lazy-load plugins,
cache config parse, defer network checks, …). Think each. Winnow to 5 (lazy plugins, config
cache, defer net checks, prune deps, parallel init). Expand to ~15. Overlap-check finds an
open bead for "config parse is slow" → MERGE the config-cache survivor into it. File the
other 4 as self-documenting issues, each with a "Test: measure cold-start before/after" task
depending on it. Refine: discover lazy-plugins must land before parallel-init → wire the dep.
Result: a 4-issue, dependency-ordered, testable backlog — zero code written yet.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Only got ~8 ideas, all similar | Judged while generating | Restart Phase 2; forbid evaluation until 30 exist; vary axes. |
| Backlog has duplicate of an open bead | Skipped Phase 6 | Run `br list`/`br ready`; convert the dup to MERGE; add context to the existing issue. |
| Next agent can't act on a filed issue | Body not self-documenting | Rewrite body: problem + rationale + acceptance check (Phase 7 template). |
| `br ready` shows a blocked issue as ready | Dependency not wired | `br dep add <dependent> <prerequisite>`; re-run Phase 8. |
| Tempted to start coding mid-funnel | Plan-space discipline slipped | Stop; complete the funnel; implementation is out of scope for this skill. |

## See Also

- [references/methodology.md](references/methodology.md) — full per-phase mechanics, cut
  criteria, and the plan-space refinement loop.
- [references/prompts.md](references/prompts.md) — THE EXACT PROMPT copy-paste blocks with
  iteration round-counts, plus the self-documenting issue-body template.
