---
name: layered-defect-hunt
description: |-
  Use when running systematic multi-pass bug hunting across correctness, edges, concurrency, and failures.
  Triggers:
practices:
- code-review
- root-cause-analysis
- evidence-driven
hexagonal_role: supporting
consumes:
- code-under-review
produces:
- bug-findings.md
context_rel: []
skill_api_version: 1
user-invocable: false
context:
  window: isolated
metadata:
  tier: judgment
  stability: experimental
  dependencies: []
output_contract: 'file: bug-findings.md (deduped findings ledger, one row per confirmed bug)'
---

# layered-defect-hunt — one lens per pass, loop until a clean cycle

## ⚠️ Critical Constraints

- **One lens per pass. Never mix.** Each pass reads the WHOLE target asking
  exactly one question. **Why:** a single "find bugs" sweep anchors on the first
  bug class it sees (usually correctness) and the brain stops re-reading for
  off-lens classes; a race condition is invisible while you're reading for
  off-by-one errors.
  - WRONG: "Review this file for any bugs." → one pass, correctness-only in practice.
  - CORRECT: pass 1 correctness → pass 2 edges → pass 3 concurrency → ... each a fresh read.
- **A finding is a hypothesis until proven.** Confirm with a trigger (input,
  interleaving, or trace) before it enters the ledger. **Why:** unproven findings
  flood the ledger with false positives and erode trust in the real ones.
- **Stop on convergence, not on a pass count.** Loop the lens cycle until ONE
  full cycle adds zero new confirmed findings. **Why:** a fixed "3 passes" either
  quits with bugs left or burns budget re-scanning clean code.
- **Never edit during a hunt pass.** Hunting and fixing are separate phases.
  **Why:** a mid-pass fix changes line numbers and behavior under you,
  invalidating the rest of the pass and hiding bugs the edit introduced.

## Why This Exists

Bug density is uneven across *classes*, and human + LLM attention is single-lens
by default: whatever question you hold while reading is the only class you
actually see. Reading once "for bugs" reliably finds correctness mistakes and
misses concurrency, resource, and security bugs entirely — they are real, but
off the lens you were holding. This skill forces a known taxonomy of lenses
through the code one at a time, so every class gets a dedicated, full-attention
pass, and adds a convergence stop so the loop ends on evidence (a clean cycle)
rather than on fatigue or an arbitrary count.

## Quick Start

1. **Scope the target.** A file, module, or diff. If a diff, also pass over the
   surrounding callers — a diff bug often lives in the seam, not the change.
2. **Run the six lens passes in order** (below). One full read per lens.
3. **Confirm each candidate** with a concrete trigger; record only confirmed ones.
4. **Check convergence.** Did this whole cycle add a new confirmed finding? If
   yes, loop the cycle again. If no, stop.
5. **Emit `bug-findings.md`** — the deduped ledger. Fixing is a separate phase.

## The Lens Passes (run in this order, one full read each)

| # | Lens | The single question this pass asks | Smells to chase |
|---|------|-----------------------------------|-----------------|
| 1 | **Correctness** | Does it compute the right result on the normal path? | inverted conditions, wrong operator, off-by-one, bad return, copy-paste var |
| 2 | **Edge / boundary** | What happens at the extremes and empties? | empty/null/zero, max/overflow, first/last element, single-item, unicode, negative |
| 3 | **Concurrency** | Can two things run at once and corrupt state? | shared mutable state, missing lock, check-then-act (TOCTOU), await-holding-lock, unbounded queue |
| 4 | **Error handling** | What happens when a call fails? | swallowed exception, ignored return code, partial write, no rollback, error path leaks resource |
| 5 | **Resource leaks** | Is every acquired thing released on every path? | unclosed file/socket/handle, leaked goroutine/thread, unbounded cache/growth, missing defer/finally |
| 6 | **Security** | Can untrusted input cause harm? | injection (SQL/cmd/path), missing authz check, secret in log, unsafe deserialization, SSRF, weak validation |

Order matters: correctness first (the loudest, biases everything), security last
(needs the structure the earlier passes mapped). Pass discipline: at the start of
each pass, write the one question at the top of your notes and answer ONLY it.

## Convergence — the stop condition

Track `new_confirmed_this_cycle`. A **cycle** = passes 1–6 once.

```
cycle = 0
do:
  cycle += 1
  new_confirmed_this_cycle = 0
  for lens in [correctness, edge, concurrency, error, leak, security]:
    for each candidate found by lens:
      if confirm(candidate) and not in ledger:
        ledger.add(candidate); new_confirmed_this_cycle += 1
while new_confirmed_this_cycle > 0 and cycle < MAX_CYCLES   # MAX_CYCLES = 4 (escape hatch)
```

- **Converged** = a full cycle (all six lenses) added **zero** new confirmed
  findings → stop, the code is clean *to this method*.
- **Why re-loop at all:** fixing a pass-3 bug in your head, or simply
  understanding the code better on cycle 2, exposes bugs invisible on cycle 1.
- **MAX_CYCLES = 4** is an escape hatch, not a target. Hitting it means the
  target is too large or too churny — split it and hunt the pieces.

## Output Specification

Write `bug-findings.md`. One row per **confirmed** bug, deduped (same root cause
across passes = one row, list both lenses).

```markdown
# Bug findings — <target> (<N> cycles, converged: yes/no)

| ID | Lens | Severity | Location | Bug | Trigger (proof) | Suggested fix |
|----|------|----------|----------|-----|-----------------|---------------|
| B1 | concurrency | high | cache.go:42 | check-then-set race on `m` | two goroutines call Get→Set | guard with mutex / use sync.Map |
```

Severity: critical / high / medium / low. "Trigger" must be a concrete input,
interleaving, or trace — not "could happen". End with a **Convergence note**:
cycles run, whether it converged, and any lens skipped (with reason).

## Quality Rubric

- Every confirmed finding has a concrete reproducing trigger, not a hunch.
- All six lenses were applied in distinct passes (the convergence note proves it).
- The loop ended on a clean cycle OR documents why MAX_CYCLES was hit.
- The ledger is deduped: one root cause = one row, even if two lenses caught it.

## Examples

**A diff hunt.** A PR adds a cache layer. Cycle 1: pass 1 finds nothing; pass 3
(concurrency) flags `Get` then `Set` without a lock — confirmed by imagining two
callers → B1. Pass 5 (leaks) flags an unbounded map → B2. Cycle 2: now holding
B1/B2 in mind, pass 4 (error handling) notices the eviction error is swallowed →
B3. Cycle 3: zero new findings → converged. Ledger has B1–B3.

**When to stop early.** A 30-line pure function converges in one cycle (no shared
state, no I/O → passes 3/5/6 are quick and empty). Don't manufacture findings to
justify more cycles — a clean cycle is a valid, reportable result.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Every pass finds correctness bugs only | Lens discipline slipped | Re-state the one question at the top of each pass; re-read for that class only |
| Ledger full of "could happen" entries | Skipping the confirm step | Demand a concrete trigger before adding; drop the rest |
| Never converges (hits MAX_CYCLES) | Target too large / churny | Split into smaller targets and hunt each |
| Same bug appears as 3 findings | Not deduping by root cause | Merge by root cause; list multiple lenses on one row |
| Fixes during hunt hide other bugs | Hunting and fixing interleaved | Hunt to a frozen ledger first, fix in a separate phase |

## See Also

- `bug-hunt` — single-investigation root-cause workflow for one known bug.
- `review` — diff-scoped correctness + cleanup review (less exhaustive).
- `red-team` — adversarial stress of a plan or design, not line-level code.
