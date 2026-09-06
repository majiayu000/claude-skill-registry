---
name: optimize
description: 'Use when asked to optimize code, speed up a path, reduce allocations, repair a regression, or profile a target. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# Optimize

Two modes share one authority: reversible local writes to the resolved target, never push, tag, publish, deploy, or mutate a remote. Full mode runs an isolated five-lens search with an integrated 1.05x gate and an atomic commit. Quick mode runs a single measure-identify-fix-verify loop with a noise-aware keep/revert and a CI guard for the obvious-bottleneck case.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user asks to optimize code, make a path faster, reduce allocations, fix a performance regression, profile and optimize a path, symbol, or diff, or a performance requirement, slowness report, Core Web Vitals miss, or profiling evidence identifies a bottleneck. |
| Authority | Reversible local: writes only the resolved local target and `.outline/optimize/<target>/` (full mode) or the named target and a CI performance-budget or field-monitor guard (quick mode), committing one winning optimization in full mode; rollback is version control. Never tags. No remote mutation. |
| Side effect | Full mode: append measurements and decisions to `.outline/optimize/<target>/log.jsonl`, benchmark isolated candidates, apply the winner, create one atomic commit. Quick mode: apply one targeted fix; may add a CI performance budget or field monitor. |
| Done | Full mode: exit 0 only after the committed change preserves authorized behavior, passes the adversarial and repository gates, and measures at least 1.05x faster in the integrated benchmark. Quick mode: the identified bottleneck is measurably improved past noise, tests remain green, no new regressions, and a CI budget or field monitor guards the metric. |

## Inputs

Required (both modes): a resolvable path, symbol, diff, or active local change; a representative workload or benchmark command (full mode) or a performance symptom and the codebase under optimization (quick mode); and repository-native verification commands. A supplied profile or named hotspot is optional.

Optional (full mode): a performance budget, maximum gate attempts, maximum wall time, and minimum marginal speedup. An observable approximation is permitted only when the user's request already authorizes it and the exact changed contract is confirmed before mutation. If the target or workload cannot be resolved without guessing, stop with exit 11.

Optional (quick mode): existing measurements, profiling evidence, performance budgets, or Core Web Vitals targets.

## Mode selection

| User says or evidence | Mode | Gate |
|---|---|---|
| optimize this path, profile and optimize, reduce allocations, fix a regression, hot-path speedup | full | Integrated benchmark proves at least 1.05x; adversarial behavior gate; atomic commit |
| quick optimize, obvious bottleneck, Web Vitals miss, slowness report, single targeted fix | quick | Improvement past measurement noise; tests green; CI guard added |

When the user names a hot path and a benchmark, use full mode. When the user names a single symptom and an evident bottleneck (N+1 query, missing index, bundle size, re-renders), use quick mode. When the evidence is a profiling trace with one dominant hotspot under 5% of total time, use full mode; when one evident fix addresses the symptom, use quick mode.

## Full mode

1. Resolve one target and bound writes to that target plus `.outline/optimize/<target>/`. Reject architecture-wide redesign and mixed optimization concerns. For a single function under 50 lines with one evident concern, report `auto-skip` and use one candidate; otherwise use all five lenses below. Done when: one target is resolved and writes are bounded, or `auto-skip` is reported.
2. Accept supplied profiler evidence or run the representative workload and one suitable profiler pass. Record the top self-time function or widest plateau as `HOT_PATH`. Stop with exit 11 if no path accounts for at least 5% of total time or the workload is not measurable. Done when: `HOT_PATH` is recorded with at least 5% of total time, or exit 11 is returned.
3. Locate or create a minimal benchmark under `.outline/optimize/<target>/`. Run the benchmark with three warmups and at least ten measured runs; capture median, standard deviation, minimum, and maximum. Do not continue while standard deviation exceeds 20% of the median; reduce environmental noise or increase runs. Append the baseline and benchmark command to `log.jsonl`. Done when: baseline is captured with standard deviation under 20% of median and appended to log.jsonl.
4. Before candidate work, append an `in-progress` run record containing a run ID, target, start time, stop limits, and a fingerprint of the target revision, hot-path source, and benchmark command. Never rewrite or truncate the log. On interruption, resume only when the fingerprint matches and a fresh baseline agrees with the recorded baseline; otherwise mark the measurements stale and start a new run. Reuse matching recorded candidates and rerun only missing ones. Done when: the in-progress run record is appended with all fields and the fingerprint is recorded.
5. Unless `auto-skip` applies, launch five independent, worktree-isolated candidates together. Give each the same hot-path source, benchmark, and baseline, but one distinct lens: `algo` changes complexity or removes work; `data` changes representation or layout; `cache` reuses valid results with explicit invalidation and bounds; `concur` changes safe parallelism or contention; `arch` removes a local boundary or transfer cost without redesigning the module. State that the lenses are disjoint, worktrees are isolated, and candidates become read-only after reporting. Done when: five worktree-isolated candidates are launched with distinct lenses, or `auto-skip` uses one candidate.
6. Require each candidate to apply one transformation, run the same benchmark protocol, and return its lens, change summary, before and after medians, speedup ratio, behavior assessment, readability cost, and patch. As each result arrives, append its candidate record before scoring it. Do not record a failed candidate, so a resumed run retries it. Done when: every candidate result is appended to the log before scoring.
7. Drop failed results and score each remaining candidate as `speedup_ratio * behavior_safety * (1 - readability_cost * 0.3)`, where exact behavior is `1.0`, a confirmed approximation is `0.7`, and unsafe or undisclosed behavior is `0.0`. Rank the winner and runner-up and append the ranking. Stop with exit 12 if no candidate reaches 1.05x. Stop with exit 14 if a required approximation confirmation is absent or declined. Done when: candidates are scored, ranked, and appended, or exit 12/14 is returned.
8. For the leading candidate, adversarially compare original and optimized behavior over output identity, error semantics, public contracts, empty and boundary inputs, negative values, NaN where applicable, and concurrent call sequences. Append every gate verdict and failure scenario. On failure, discard that candidate and consider the next ranked candidate. Done when: the leading candidate passes every adversarial gate with verdicts appended, or is discarded for the next ranked candidate.
9. Before each promotion, enforce the configured maximum attempts, maximum wall time, and minimum marginal-speedup floor; default maximum attempts to the viable-candidate count and the marginal floor to 1.02. If a limit trips before any candidate passes, append the best-so-far and terminal exit 16, then commit nothing. If candidates are exhausted, exit 13. Done when: a candidate is promoted within all limits, or exit 13/16 is returned.
10. Apply only the gate-cleared patch to the main worktree. Run the same benchmark there with three warmups and at least ten measured runs, append the integrated median and speedup, and discard the target patch if `baseline_median / integrated_median < 1.05`. Done when: the integrated benchmark proves at least 1.05x speedup with results appended, or the patch is discarded.
11. Run the repository-native checks that cover the changed behavior. If any fail, restore only the named target to its pre-run state, leave the append-only evidence intact, append terminal exit 13, and commit nothing. Done when: repository-native checks pass, or the target is restored and exit 13 is appended.
12. Commit exactly the named target as one optimization concern. Include the hot path, lens, rationale, baseline and integrated medians with variance, ratio, and any confirmed approximation contract in the commit message. Remove only `.outline/optimize/<target>/agent-*` worktrees, preserve the log and benchmark evidence, and append the authoritative terminal `run` record with status `done` and exit 0. Done when: one atomic commit is made with full rationale in the message, candidate worktrees are removed, and the terminal run record with exit 0 is appended.

## Quick mode

1. **Establish baseline.** Measure the bottleneck with profiling tools or timing data before touching any code. Record the specific metric, the tool or method used, and the measured value. If baseline cannot be established, stop and report blocked. Done when: the metric, tool, and measured value are recorded.
2. **Identify the specific bottleneck.** Use the symptom to determine the profiling target: frontend performance (Lighthouse, DevTools Performance tab, web-vitals RUM), backend latency (APM, query logging, EXPLAIN ANALYZE), bundle analysis, or heap profiling. Do not assume the cause. The query plan is the measurement for database queries; the trace is the measurement for frontend jank. Done when: the profiling target is determined from the symptom.
3. **Fix the identified bottleneck only.** Apply one targeted change. Code it completely before measuring again. Common fixes: N+1 queries -> single query with join or include; unbounded pagination -> limit and offset; missing index -> CREATE INDEX with composite key shaped to the query; connection pool exhaustion -> size pool to database ceiling; large bundle -> code splitting or lazy loading; unoptimized images -> responsive srcset, lazy loading, modern format; unnecessary re-renders -> React.memo, useMemo, stable references; missing caching -> cache expensive reads with stated TTL and key design. Done when: one targeted change is coded completely.
4. **Re-measure under identical conditions.** Use the same tool, same conditions, same measurement method as the baseline. One change at a time. Done when: the after-measurement is recorded under identical conditions.
5. **Keep or revert strictly.** Past noise and tests green: keep. Within noise or tests red: revert immediately. Neutral is a revert. An optimization that wins by dropping needed work is a revert. Done when: the change is kept (past noise, tests green) or reverted (noise, tests red, or neutral).
6. **Guard the metric.** Add a synthetic CI performance budget or a field monitor (RUM p75) for the primary metric. This prevents the fix from regressing unseen. Done when: a CI performance budget or field monitor guards the primary metric.

## Failure and recovery

### Full mode

Exit 11 means no measurable or resolvable hotspot; exit 12 means no candidate or integrated result cleared 1.05x; exit 13 means all candidates changed behavior or repository checks failed; exit 14 means an approximation was not confirmed; exit 15 means the proposed commit mixes optimization concerns and must be split before retrying; exit 16 means a stopping limit ended promotion before a gate-cleared winner. Before commit, recover by restoring only the named target and removing only run-created candidate worktrees; retain append-only evidence and never revert an unrelated commit. A partial run is not success: append the exact terminal classification, commit nothing, and report the best measured result and blocking evidence. Resume only through the fingerprint match and fresh-baseline agreement in step 4.

### Quick mode

- Baseline unavailable. Measurement tools are unavailable or the codebase cannot be profiled. Result: blocked. Do not proceed without baseline evidence.
- No bottleneck found. Profiling reveals no measurable code-level bottleneck. Result: report uncertainty and whether environmental or statistical noise is suspected.
- Fix produces no measurable gain. Improvement is within noise range of the baseline. Result: revert. Never keep a neutral change.
- Correctness regression. Tests fail or behavior changes after the fix. Result: revert immediately. Correctness gates the metric.
- Fix exceeds available authority. The bottleneck requires unavailable credentials, remote mutation, or infrastructure changes outside local write scope. Result: document the requirement for a future attempt. Do not widen scope.

Partial-result rule (quick mode): reverted code leaves no trace. Keep a ledger entry (baseline, fix applied, before/after measurement, verdict) so discarded ideas are not re-profiled.

## Output

**Full mode.** On success, return exit 0 with the commit identifier, target, selected lens, benchmark command, baseline and integrated statistics, measured speedup, behavior-gate result, repository checks, and durable log path. On failure, return the applicable exit code, unchanged/rolled-back target state, measurements obtained, and the precise blocker; never report a worktree-only result as a landed win.

**Quick mode.** Optimized code with before/after measurements, plus a ledger entry per attempt (kept and reverted) documenting the hypothesis, baseline, result, and verdict. Each entry states the metric name, baseline value, result value, and tool used.

