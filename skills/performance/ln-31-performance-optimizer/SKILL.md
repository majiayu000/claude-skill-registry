---
name: ln-31-performance-optimizer
description: "Optimizes a measured latency, throughput, memory, CPU, or I/O problem through profiling and keep-or-discard experiments. Use for a known bottleneck; not unbiased A/B comparison."
---

# Performance Optimizer

Optimize only measured problems. Preserve correctness, isolate experiments, and retain a change only when comparable evidence shows that it improves the agreed metric without unacceptable regressions.

## Tool Routing

| Need | Preferred tool | Use it when | Fallback |
|---|---|---|---|
| Repository state and safe edit boundary | Git status, diff, branch or worktree inspection, and repository instructions | Always before profiling or editing | Stop if user changes cannot be isolated safely |
| Baseline and final metric | Existing benchmark, load test, reproducible command, or production-like replay | The metric and workload reflect the reported problem | Create the smallest local benchmark that reproduces the behavior without inventing production scale |
| Bottleneck evidence | Existing profiler, tracing, query diagnostics, allocation tools, or OS-level metrics | Locating CPU, memory, I/O, lock, query, network, or scheduler cost | Targeted instrumentation with cleanup plan |
| Code path and blast radius | Language server or host-native code intelligence | Following hot symbols, callers, implementations, and affected contracts | Narrow search plus direct inspection of definitions and consumers |
| Correctness and regressions | Repository-defined tests, build, lint, type, and smoke commands | Before and after every retained experiment | Add a focused safety test when current coverage cannot detect the likely regression |
| Runtime and dependency semantics | Official documentation, release notes, and specifications matching installed versions | A hypothesis depends on optimizer, runtime, database, framework, or library behavior | Primary-source web research; otherwise mark the hypothesis `UNVERIFIED` |
| Independent challenge | One native subagent or advisor when policy and scope allow | Competing hypotheses, unfamiliar runtime behavior, or high-risk change needs independent scrutiny | Separate adversarial hypothesis review |

Do not optimize by aesthetic preference or benchmark a different workload from the reported problem. Never discard user changes, use destructive Git reset, or run uncontrolled load against production.

## Evidence Rules

- Define the primary metric and acceptance threshold before editing; do not move the goal after seeing results.
- Compare the same workload, environment, build mode, data, warmup, and measurement method before and after.
- Use repeated runs and report distribution or variance; a single faster run is not proof.
- Separate cold-start, warm steady-state, and saturated-load behavior when the reported problem can occur in more than one regime.
- Profile contribution and end-to-end impact separately: a hot function can improve while the user-visible metric does not.
- Treat profiler estimates, synthetic workloads, and production observations as different evidence classes and label them.
- Correctness, resource safety, and operational stability are hard constraints, not secondary metrics.

## Checklist

### 1. Define the Problem and Protect the Workspace

- [ ] Resolve the user-visible problem, affected workflow, target metric, workload, environment, constraints, and acceptance threshold.
- [ ] Run the wrong-tool gate: confirm the symptom is a performance problem rather than correctness, configuration, capacity, dependency, or observability failure.
- [ ] Read repository instructions and inspect Git state, branches, uncommitted changes, ignored artifacts, and available isolation mechanisms.
- [ ] Preserve user work and isolate experiments in a safe branch or worktree when changes, benchmarks, or generated artifacts could interfere.
- [ ] Start a run-owned resource ledger with every created absolute path, worktree, process ID, cache, profile, and temporary artifact; never register pre-existing resources as cleanup targets.
- [ ] Identify correctness, security, memory, cost, compatibility, and operational constraints that no optimization may violate.
- [ ] Locate existing benchmarks, profiles, performance tests, production traces, service-level objectives, and known environmental variability.

### 2. Establish a Reproducible Baseline

- [ ] Use the same metric type as the observed problem: latency distribution, throughput, CPU, memory, allocation, I/O, query count, lock wait, or another direct measure.
- [ ] Make the workload representative and deterministic enough to compare, including data size, concurrency, cache state, warmup, and build mode.
- [ ] Cover the operating points that could reverse the conclusion--at minimum the reported case plus relevant data-size or concurrency boundaries--without inventing synthetic scale.
- [ ] Run enough repetitions to expose noise and record raw results, median or appropriate percentile, spread, failures, and environment details.
- [ ] When drift or noise is material, interleave or randomize baseline and candidate runs and prefer paired comparisons over one block of "before" followed by one block of "after."
- [ ] Verify that the benchmark detects an intentionally slower or obviously changed path when practical; a benchmark insensitive to behavior cannot validate optimization.
- [ ] Run relevant correctness tests before editing so pre-existing failures are not attributed to experiments.
- [ ] Stop and report `BLOCKED` if the problem cannot be reproduced and no trustworthy production evidence can define a safe proxy.

### 3. Profile and Form Hypotheses

- [ ] Profile the end-to-end path before focusing on a function, query, allocation, lock, or network call.
- [ ] Build a ranked cost map with measured contribution, call frequency, inclusive and exclusive cost where available, and affected workload.
- [ ] Trace the top costs to implementation, callers, data shape, concurrency model, configuration, and external dependencies.
- [ ] Distinguish root bottlenecks from downstream symptoms, measurement overhead, debug builds, cold starts, and one-time initialization.
- [ ] If profiling crosses services or processes whose code is in scope, align traces/correlation IDs and follow the measured downstream path; do not label an accessible internal service "external" and stop at its latency.
- [ ] Estimate profiler or instrumentation perturbation and confirm the final end-to-end result without invasive instrumentation.
- [ ] Research official runtime, framework, database, and dependency behavior only when it can confirm or reject a concrete hypothesis.
- [ ] Check existing platform and dependency capabilities before proposing custom caches, pools, schedulers, serializers, or data structures.
- [ ] Write a small ordered hypothesis set; for each state expected metric change, mechanism, affected files, risk, dependencies, and verification.
- [ ] Reject hypotheses that lack a measurable mechanism, require speculative scale, or cannot be rolled back independently.
- [ ] Use an independent challenge when competing explanations remain plausible; verify advisor claims before changing code.

### 4. Execute Atomic Keep-or-Discard Experiments

- [ ] Add or identify a safety test for behavior most likely to regress before applying each risky hypothesis.
- [ ] For caching, batching, parallelism, pooling, or retry changes, explicitly protect invalidation, ordering, idempotency, cancellation, backpressure, timeout, and bounded-resource semantics that the faster path could violate.
- [ ] Apply the smallest coherent change that tests one mechanism; group changes only when their effects are intentionally inseparable.
- [ ] Keep instrumentation bounded, low-overhead, and easy to remove; never leave secrets or sensitive payloads in diagnostic output.
- [ ] Run focused correctness checks immediately after the edit and discard the experiment if they fail.
- [ ] Repeat the exact baseline benchmark under comparable conditions and preserve raw results.
- [ ] Inspect the diff for accidental cleanup, unrelated refactoring, generated churn, debug flags, changed benchmark inputs, and hidden configuration changes.
- [ ] Mark the experiment `KEEP` only if the agreed metric improves beyond noise and all constraints pass.
- [ ] Mark it `DISCARD` and revert only that experiment when the target is missed, results regress, or safety becomes uncertain.
- [ ] After a kept change, establish the new compound baseline before testing the next hypothesis.

### 5. Stop, Verify, and Report

- [ ] Continue only when new measurement supports another hypothesis; stop at the target, diminishing returns, exhausted safe options, or a missing prerequisite.
- [ ] Run the full relevant build, lint, type, test, smoke, benchmark, and operational checks on the final retained state.
- [ ] Remove only run-owned ledger entries: verify absolute paths remain inside approved temporary roots, stop exact recorded process IDs, preserve dirty or pre-existing worktrees, and retain evidence artifacts intentionally reported.
- [ ] Confirm that the benchmark definition and acceptance threshold did not drift during the run.
- [ ] Report every kept and discarded hypothesis, not only the successful path, so future work does not repeat disproven experiments.
- [ ] Use `IMPROVED` only when at least one retained change improves the agreed metric beyond noise with every constraint passing; use `NO_CHANGE` when all experiments are discarded and the baseline is restored; use `BLOCKED` when a safety prerequisite, reproducible baseline, or safe restoration path is unavailable.
- [ ] Return the verdict with baseline, final distribution, delta, correctness evidence, limitations, and residual bottlenecks.

## Output Contract

```markdown
# Performance Optimization

**Verdict:** IMPROVED | NO_CHANGE | BLOCKED

## Target and method
- User-visible problem and workload
- Primary metric and acceptance threshold
- Environment, repetitions, and variance method
- Correctness and operational constraints

## Baseline and profile
| Metric | Baseline | Variance | Evidence |
|---|---:|---:|---|
| ... | ... | ... | ... |

## Experiments
| Hypothesis | Change | Result | Decision | Verification |
|---|---|---|---|---|
| ... | ... | ... | KEEP / DISCARD | ... |

## Final result
Comparable before/after metrics, full verification, cleanup, limitations, and residual bottlenecks.

## Evidence artifacts
Run-owned paths and hashes for raw samples, commands, environment capture, final diff, and cleanup proof.
```
