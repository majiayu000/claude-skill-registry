---
name: optimize
description: Applied optimization op — locate a hot path, fan out five transformation lenses as worktree-isolated agents, benchmark each candidate, gate on behavior preservation, commit the winner with a proven speedup. Use when the user says "optimize this", "make X faster", "speed up the hot path", "reduce allocations", "fix the perf regression on <target>", or "profile and optimize <symbol>"; distinct from perf-profile (diagnosis only, no transform), perf-investigate (auditable ledger + verdict, no commit), and simplify (behavior-preserving entropy reduction, no measurement).
metadata:
  short-description: Applied optimization op — transform a hot path and prove the win
---

# Optimize — applied hot-path transform with a proven win

A self-contained diagnose→optimize→verify loop. Locate the hot path (lightly — no full
investigation ledger), fan out five candidate transformations as worktree-isolated `Agent` calls,
benchmark each, gate on behavior, commit the winner. The deliverable is a **committed, measured
change** — not a verdict, not a report, not a list of suggestions.

Op-cell is context-dependent: `correct` + `Restores: spec:<budget>` when a `--budget` or a named
regression is the target; `compress` when removing wasted work with no stated budget; `extend` when
the winning change adds an approximation or cache contract that changes observable semantics.
Rejection grounds: **Excess** (micro-opt with no measured hotspot), **Graft** (optimization applied
before the hotspot is confirmed), **Sprawl** (added complexity that outweighs the earned speedup).

**Reference files (verbatim prompts, agent dispatch shapes, harness templates):**
- `references/lenses.md` — five lens prompts sent to candidate agents, one per lens
- `references/tooling.md` — per-language benchmark/profile tooling matrix + minimal harness
  templates for the author-a-harness phase

## Constitutional Rules (Non-Negotiable)

1. **No optimization without a measured hotspot.** Accept a supplied profile, symbol, or `perf-profile` output — or run Phase 2's light locate. Never fan out candidates against unmeasured code.
2. **Benchmark before landing.** Every accepted change carries a before/after `hyperfine --warmup 3 --min-runs 10` measurement (variance-aware). If no harness exists, author a minimal throwaway under `.outline/optimize/`. Fall back to a rigorous complexity/allocation argument only when benchmarking is genuinely impractical — label it `[UNMEASURED]` in the commit body.
3. **Behavior preservation is a gate, not a guideline.** Observable output must be identical by default. Approximation (lossy fast-path, float reassociation, bounded staleness, bounded cache eviction) is permitted only when the user explicitly requests it in prose AND the skill presents the exact contract change for confirmation before applying anything.
4. **One optimization concern per atomic commit.** Algorithmic change + data-structure swap in one commit trips exit 15; split first.
5. **Auto-skip for trivial targets.** A single function <50 LOC with an obvious single-concern win runs a single-pass optimize-and-measure, not a five-agent fleet. Name the auto-skip in the output so the user knows.

## When to Apply

- The user says "optimize this", "make X faster", "speed up the hot path in Y", "reduce allocations in Z", "fix the perf regression", "profile and optimize `<symbol>`".
- A hotspot has already been identified (perf-profile output, flamegraph, or named symbol) and the next step is transformation.
- A performance budget is stated (`--budget`) and the current code does not meet it.
- Active context (current diff/file/stack) is measurably slow and the user wants the fix landed, not analyzed.

## When NOT to Apply

- **Diagnosis with no transform authorized** — that is `perf-profile`. Use it first if the hotspot is unknown; then come back here.
- **Full investigation with a persisted ledger + keep/stop verdict** — that is `perf-investigate`. Use it when you need an auditable case file across multiple experiments.
- **Behavior-preserving entropy reduction on a diff** — that is `simplify`. It runs no benchmarks and explicitly forbids behavior-affecting speedups.
- **Unmeasured code with speculative "this might be slow"** — Graft rejection; locate the hotspot first.
- **No measurable improvement expected** — if the candidate analysis shows noise-level gains, exit 12.
- **Architecture-level redesign** — `perf-investigate` or a plain planning session. Optimization surgery within a hot path is in scope; full module rewrites are not.

## Workflow

### Phase 1 — Resolve target

If `/optimize <path|symbol|diff>` was given, use that as the target. If no arg, detect active
context (current diff, current file in editor, top of git stack) as `tidy` does — if the context is
empty or unresolvable, error explicitly rather than guessing.

**Auto-skip check:** if the resolved target is a single function <50 LOC and only one obvious
concern is visible, declare auto-skip, note it aloud, and proceed with a single-pass loop (Phases
3 → 5 single-agent → 6 → 7 → 8). Otherwise proceed with the full five-agent fan-out.

Parse `--budget <metric>` (e.g. `--budget p95<3ms`, `--budget throughput>10k/s`,
`--budget alloc<1MB`) — sets the op-cell to `correct` and the stop condition.

### Phase 2 — Locate / accept the hotspot

If a profile artifact, flamegraph, or named symbol was supplied, accept it and skip profiling.

Otherwise run a light locate:
1. `hyperfine '<workload cmd>'` — confirm the workload takes measurable wall-clock time.
2. One profiler pass at the right level (see `references/tooling.md` for per-language choice).
3. Identify the top self-time function or widest plateau. Document it as `HOT_PATH`.

If no hotspot clears a 5 % share of total time, exit 11 — no actionable target.

### Phase 3 — Establish baseline benchmark

Author or locate a benchmark harness for `HOT_PATH` (see `references/tooling.md`). If none exists,
write a minimal throwaway harness under `.outline/optimize/<target>/bench.*` that exercises the hot
function in isolation. Run:

```
hyperfine '<bench cmd>' --warmup 3 --min-runs 10 --export-json .outline/optimize/<target>/before.json
```

Record: median, stddev, min/max. This is the before measurement. **Do not proceed if stddev >
20 % of median** — fix measurement noise first (pin CPU frequency, isolate the process, widen
`--min-runs`).

### Phase 4 — Fan out candidate agents

Launch five worktree-isolated agents in **one tool-call message** (independent by construction —
disjoint lenses, no shared files). For each lens `L` in {`algo`, `data`, `cache`, `concur`,
`arch`}:

```
Agent(
  prompt  = references/lenses.md § <L> + "\n\n---\n\nHOT_PATH: " + <symbol> +
            "\n\nCODE:\n" + <hot-path source> +
            "\n\nBEFORE (hyperfine median): " + <before_median>,
  isolation = "worktree"
)
```

Each agent must:
1. Apply its transformation inside the worktree.
2. Run the harness: `hyperfine '<bench cmd>' --warmup 3 --min-runs 10 --export-json after.json`.
3. Report back a JSON result: `{lens, change_summary, before_median, after_median, speedup_ratio, behavior_self_assessment, readability_cost, diff_patch}`.

Document the independence argument in the spawn message: "disjoint lenses, isolated worktrees,
read-only phase after reporting".

### Phase 5 — Score and rank candidates

Collect the five result objects (null = agent failed; `.filter(Boolean)` before ranking). Compute:

```
composite = speedup_ratio × behavior_safety × (1 - readability_cost × 0.3)
```

Where `behavior_safety` = 1.0 (exact behavior claimed), 0.7 (approximation with disclosed
contract), or 0.0 (unsafe / undisclosed). Sort descending. Name the winner and the runner-up.

If `speedup_ratio < 1.05` for all candidates, exit 12 — no candidate clears noise.

If the winner relies on approximation (behavior_safety < 1.0) and the user has not already
confirmed in prose: present the exact contract change and wait for confirmation. If declined, exit
14. If confirmed, set op-cell to `extend` and document the contract change in the commit body.

### Phase 6 — Adversarial behavior gate

Dispatch a single adversarial reviewer agent:

```
Agent(
  prompt = "You are an adversarial reviewer. The following optimization diff was applied to <HOT_PATH>.
            Try hard to construct any input or call sequence where the optimized version produces
            a different observable result than the original. Check: output identity, error
            semantics, public API contract, edge inputs (empty, max, negative, NaN, concurrent).
            If approximation is claimed, check that the contract was disclosed correctly.
            Return: {passed: bool, failure_scenario: string|null}"
)
```

If `passed = false`, log the failure scenario, revert the candidate worktree, promote the
runner-up, and repeat Phase 6. If all candidates fail the gate, exit 13.

### Phase 7 — Apply winner + commit

1. Apply the winner's `diff_patch` to the main worktree.
2. **Integrated benchmark gate (pre-commit).** Run hyperfine on the main tree — not the worktree — to confirm the win survives integration:

   ```
   hyperfine '<bench_cmd>' --warmup 3 --min-runs 10 \
     --export-json .outline/optimize/<target>/after-integrated.json
   ```

   Compute `integrated_speedup = before_median / after_integrated_median`. Values > 1.0 mean
   faster; values < 1.0 mean a regression. If `integrated_speedup < 1.05` the win fell into noise
   — discard the patch with `git restore .` and exit 12. Do not commit a change whose speedup
   cannot survive integration; the deliverable is a proven win, not a worktree artifact.

3. Run repo-native tests. On red, discard the patch with `git restore .` (nothing is committed yet) and exit 13. Do **not** use `git revert HEAD` — that would revert the previous commit, not the uncommitted patch.
4. Commit with:

```
<type>(optimize): <hot-path>: <lens>: <speedup summary>

<prose rationale + evidence>

Before:      <before_median> ± <stddev>
After:       <after_integrated_median> ± <stddev>  (integrated, main tree)
Win:         <integrated_speedup>× (<pct>%)

Op: correct | compress | extend
Restores: spec:<budget>           ← only when --budget was given or regression restored
```

5. Clean up worktrees: `rm -rf .outline/optimize/<target>/agent-*`.

### Phase 8 — Guard

The integrated win was already confirmed in Phase 7 before the commit. Phase 8 records the
guard recommendation only.

Suggest (do not force) adding a CI regression guard: a benchmark invocation that fails if the
median regresses past `before_median × 1.05`. Place the guard command in the project's CI config
or a `Justfile` / `Makefile` target named `bench-guard`. The before-benchmark JSON artifact at
`.outline/optimize/<target>/before.json` can seed the threshold.

## Validation Gates

| Gate | Pass Criteria | Blocking |
|---|---|---|
| Hotspot identified | Hot path supplied or located with ≥5 % self-time share | Yes — exit 11 if no hotspot |
| Baseline captured | Before-benchmark median with stddev <20 % | Yes — fix measurement noise first |
| Fan-out dispatched | All candidate agents launched in one tool-call message (or auto-skip declared) | Yes |
| Composite score non-zero | At least one candidate speedup_ratio ≥1.05 | Yes — exit 12 if none |
| Approximation confirmed | If any winner claims approximation, user confirmed contract change | Yes — exit 14 if declined |
| Adversarial gate cleared | Adversarial reviewer returned passed=true for the winner | Yes — promote runner-up or exit 13 |
| Tests green | Repo-native tests pass after apply, before commit | Yes — discard patch with `git restore .` on red, exit 13 |
| Op trailer present | Commit body carries Op: correct\|compress\|extend | Yes |
| Worktrees cleaned | `.outline/optimize/<target>/agent-*` dirs removed | Yes |

## Exit Codes

| Code | Meaning |
|---|---|
| 0 | Clean — optimization landed, win proven, all gates passed |
| 11 | No measurable target — active context too trivial, no hotspot with ≥5 % share, or workload too fast to measure |
| 12 | No winning candidate — all five lens agents ran; none cleared the 1.05× noise threshold; no change committed |
| 13 | Behavior regression — adversarial gate rejected all candidates, or repo tests went red after apply; reverted |
| 14 | Approximation declined — user did not confirm the contract change; optimization aborted |
| 15 | Mixed-concern commit — more than one optimization concern bundled; split before committing |

## See also

- **perf-profile** — diagnosis upstream: locate the hotspot, establish whether optimization is warranted, and understand *where* to optimize. Run perf-profile before `/optimize` if the hotspot is unknown. `/optimize` accepts perf-profile output as a Phase 2 bypass.
- **perf-investigate** — the heavyweight sibling: persisted `.outline/perf/` ledger, baseline series, multiple keep/stop experiments, and an auditable verdict. Use when a case file and multi-experiment record are required. `/optimize` delivers a committed change in one pass; `perf-investigate` delivers a verdict across many.
- **simplify** — behavior-preserving entropy reduction on a diff; runs no benchmarks; explicitly forbids timing/memory-affecting speedups. Use simplify to compress code structure; use `/optimize` when runtime performance is the target.
- **refactor-break-bw-compat** — contract-breaking modernization. `/optimize` never breaks public API contracts (except the disclosed approximation path, which requires explicit user confirmation).
