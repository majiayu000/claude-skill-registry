---
name: ln-34-benchmark-comparator
description: "Compares tools or implementations through reproducible A/B workloads, correctness oracles, and controlled measurements. Use to choose alternatives; not to optimize a known bottleneck."
---

# Benchmark Comparator

Compare alternatives under controlled, reproducible conditions. Correctness comes before speed, and measured data must remain separate from estimates, setup cost, and interpretation.

## Tool Routing

| Need | Preferred tool | Use it when | Fallback |
|---|---|---|---|
| Canonical workload and oracle | Repository fixtures, tests, expected diffs, schemas, or independently specified outcomes | Defining what success means before either candidate runs | Create the smallest deterministic fixture that represents the decision |
| Isolation | Clean Git worktrees, temporary directories, controlled environment, fixed seeds, and resettable caches | Preventing one candidate or run from contaminating another | Sequential clean-room setup with verified cleanup |
| Execution | The same shell runner and wrapper for every candidate | Capturing commands, exit status, stdout, stderr, timing, and artifacts consistently | Manual execution with an explicit reproducibility limitation |
| Activation proof | Logs, traces, command records, process metadata, or candidate-specific artifacts | Verifying the intended alternative actually ran and did not fall back | Treat the run as invalid when activation cannot be proven |
| Correctness grading | Tests, output parser, diff, schema validation, or independent oracle | Every scenario before cost comparison | Manual blind grading against written expectations |
| Performance and cost | Monotonic timer, resource metrics, token or usage telemetry, tool-call logs, and failure counts | Metrics are observable through the same method for all candidates | Label derived or estimated values and keep them out of measured aggregates |
| External semantics | Official documentation and specifications | Candidate configuration or claimed behavior needs current verification | Primary-source web research; otherwise mark the claim `UNVERIFIED` |

Do not tune the scenario after observing a preferred candidate, mix measurements from different workloads, or present internal estimates as externally measured facts. Benchmarking may create temporary worktrees and artifacts but must not change the source baseline or unapproved external state.

## Evidence Rules

- Specify scenarios, oracle, metrics, exclusions, and decision rule before running candidates.
- Hold all non-tested variables constant or record and analyze the confounder.
- Correctness failure cannot be compensated by better speed, token use, or cost unless the decision explicitly allows degraded correctness.
- Use repeated runs and report raw values, center, spread, failures, and outliers; never headline the best run.
- Keep setup or indexing cost, steady-state cost, maintenance burden, and runtime cost separate.
- Report measured, derived, estimated, and qualitative evidence in distinct fields.

## Checklist

### 1. Define the Decision and Experiment

- [ ] State the decision the benchmark must support, the candidates, intended users, representative workloads, and explicit non-goals.
- [ ] Include ordinary cases where a simpler or built-in candidate could reasonably win as well as cases exercising each candidate's claimed advantage; do not construct a feature demo for one side.
- [ ] Define scenario inputs, expected outcomes, correctness criteria, failure conditions, and an oracle independent of candidate self-report.
- [ ] Define primary and secondary metrics, units, measurement point, acceptance threshold, allowed tradeoffs, and tie or inconclusive rules.
- [ ] Identify variables that must remain fixed: repository revision, model, prompts, permissions, runtime, hardware, data, cache policy, and network conditions.
- [ ] Predeclare a pilot-derived repetition count tied to the minimum meaningful effect and observed noise, or a bounded sequential stopping rule with fixed error tolerance and maximum runs.
- [ ] Freeze and hash the scenario text, fixtures, expectations, runner, parser, and decision rule before the first candidate result is inspected.
- [ ] Read repository instructions and inspect Git state before creating worktrees, temporary data, or runners.
- [ ] Start a run-owned resource ledger with every created absolute path, worktree, process ID, cache, account, dataset, report, and temporary artifact; never register pre-existing resources or credentials as cleanup targets.
- [ ] Require side-effect-free or idempotent scenarios and disposable accounts or datasets; define external-write authorization, cost and rate budgets, cleanup, and rollback evidence before execution.
- [ ] Return `BLOCKED` if candidates do not solve the same task, correctness cannot be independently graded, external effects cannot be isolated, or the decision rule is being chosen after results.

### 2. Build a Symmetric Harness

- [ ] Use the same runner, timeout, logging, environment construction, and artifact collection for every candidate.
- [ ] Create clean worktrees or equivalent isolated copies from the same commit and verify identical starting state.
- [ ] Control seeds, clock, locale, concurrency, network access, dependency versions, cache state, warmup, and scenario order where they can influence results.
- [ ] Record exact candidate configuration, feature flags, prompts, command lines, permissions, and versions.
- [ ] Define a symmetric tuning policy and budget—default configuration, equally tuned configuration, or both—so one candidate is not optimized after seeing the other's result.
- [ ] Add an activation check that proves each candidate was used and identifies silent fallback, partial activation, or mixed execution.
- [ ] Validate the output parser, diff rules, test oracle, and metric collector on known pass and fail fixtures before benchmarking.
- [ ] Separate one-time setup, indexing, compilation, or download cost from steady-state execution and amortized cost.
- [ ] Define cleanup and failure recovery from the resource ledger so a crashed or timed-out run cannot contaminate later runs.

### 3. Execute and Capture Evidence

- [ ] Run candidates in a balanced or randomized order that avoids systematic warm-cache or temporal advantage.
- [ ] Capture start and end state, command, exit status, timing, resource metrics, logs, outputs, diffs, tests, and candidate-specific artifacts for every run.
- [ ] Verify activation before grading; mark unproven or fallback runs invalid rather than assigning them to the intended candidate.
- [ ] Grade correctness against the predefined oracle before examining performance and cost metrics.
- [ ] Blind manual or qualitative graders to candidate identity and randomize presentation order; record disagreements instead of resolving them toward a preferred candidate.
- [ ] Record timeout, crash, malformed output, partial completion, tool error, and environmental failure as distinct failure classes.
- [ ] Repeat valid runs according to the predefined count and preserve raw per-run results without deleting inconvenient data.
- [ ] Pause when environmental drift, rate limits, external outages, background load, or runner defects make additional runs incomparable.
- [ ] Re-run both candidates after fixing a harness defect; never repair evidence for only one side.
- [ ] Treat setup, activation, parser, and environmental failures separately from task incorrectness, then state whether setup reliability is part of the actual product decision.

### 4. Analyze Validity and Results

- [ ] Exclude only runs that meet a predefined invalidation rule and record the reason, evidence, and whether exclusion changes the conclusion.
- [ ] Report per-scenario correctness, failures, latency, resource use, tokens or usage, tool calls, and other costs before aggregating.
- [ ] Use median, percentile, confidence interval, or another statistic appropriate to the sample and distribution; show spread and sample size.
- [ ] Keep metrics with different units or workloads separate and avoid a single composite score unless its weighting was defined before execution.
- [ ] Check whether differences exceed measurement noise and whether one scenario dominates the aggregate.
- [ ] Analyze setup cost, steady-state cost, maintenance complexity, portability, failure behavior, and operational burden separately from runtime metrics.
- [ ] Label synthetic fixtures, estimated tokens, character-based proxies, modeled cost, and manual judgments so they cannot be mistaken for observed telemetry.
- [ ] Request an independent blind review when qualitative output quality materially affects the decision and automated correctness is insufficient.

### 5. Decide, Preserve, and Clean Up

- [ ] Use `WIN` only when the candidate satisfies correctness and the predefined decision rule with sufficient valid evidence.
- [ ] Use `TIE` when differences are operationally negligible or tradeoffs balance under the stated priorities.
- [ ] Use `INCONCLUSIVE` when sample size, activation, oracle, environmental control, or conflicting scenarios prevent a reliable choice.
- [ ] Preserve reproducible commands, configuration, scenario definitions, expectations, raw results, normalized results, and analysis needed for independent verification.
- [ ] Remove only run-owned ledger entries: verify absolute paths remain inside approved temporary roots, stop exact recorded process IDs, preserve dirty or pre-existing worktrees, never delete credentials, and verify source and external baseline state.
- [ ] Report invalid runs, exclusions, confounders, sensitivity to assumptions, and how the conclusion could be falsified.
- [ ] Report residual decision risks that remain after the comparison, including unsupported workloads, unmeasured costs, unstable environments, and assumptions that could reverse the verdict.
- [ ] Return scenario-level evidence, aggregate tradeoffs, verdict, decision guidance, limitations, and cleanup confirmation.

## Output Contract

```markdown
# Benchmark Comparison

**Verdict:** WIN <candidate> | TIE | INCONCLUSIVE | BLOCKED

## Experiment contract
- Decision, candidates, scenarios, and oracle
- Fixed variables and candidate configurations
- Metrics, repetitions, exclusions, and decision rule

## Validity
- Activation proof
- Harness validation
- Invalid runs, exclusions, and confounders

## Results
| Scenario | Candidate | Correctness | Failures | Primary metric | Spread | Other costs |
|---|---|---|---:|---:|---:|---|
| ... | ... | ... | ... | ... | ... | ... |

## Decision, limitations, and residual risks
Scenario tradeoffs, setup and maintenance cost, verdict rationale, sensitivity, falsification conditions, unresolved decision risks, and cleanup confirmation.

## Evidence artifacts
Run-owned paths and hashes for frozen scenarios, raw runs, exact configuration, environment capture, and cleanup proof.
```
