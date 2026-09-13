---
name: ln-45-benchmark-comparator
description: "Compares tools or implementations through controlled benchmarks and independent correctness checks."
---

# Benchmark Comparator

**Goal:** Compare alternatives under controlled, reproducible conditions. Correctness comes before speed, and measured data must remain separate from estimates, setup cost, and interpretation.

**Execution contract:** The ordered checkboxes are the Definition of Done. Track every item internally as `PENDING`, `PROVEN` with concrete evidence, `CLEARED` with evidence that its condition is absent, or `UNPROVEN` with a gap; reading, delegation, or tool failure is not proof. Reconcile items after each section. Before returning, resolve all `PENDING` and count only `PROVEN` and `CLEARED`; apply the skill's verdict and approval rules to every gap.
Preserve user intent, scope, and existing authorization. Continue authorized work; ask only for consequential unresolved choices or required external approval. Scale depth to material risk without silently skipping checks. Preserve dependency and safety ordering; otherwise choose the verification method appropriate to each obligation.
Treat equivalent user or repository evidence as valid input; another skill, named artifact, or complete lifecycle is not a prerequisite. Preserve source requirement and decision identifiers when available. Bind reused evidence to the relevant source version, dirty changes, configuration, and environment; invalidate only affected claims after a change.
On continuation, reconcile the task, existing authorization, current state, and unresolved evidence before resuming. For long work, return a compact continuation record or update an already authorized task artifact; read-only skills do not persist it. Distinguish artifact readiness, verified behavior, and authority to perform an external action.
Prepare authorized work before any required approval. If an instruction prevents progress, identify its exact source and explain the unresolved boundary; do not invent an approval gate from general caution.


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
- [ ] Define the treatment variable, then hold other relevant variables fixed: revision, model, prompts, permissions, runtime, hardware, data, caches, and network. A variable being compared cannot also be declared fixed.
- [ ] Predeclare repetitions using existing variability evidence or a bounded pilot, or a bounded sequential rule with fixed error tolerance and maximum runs. Return `INCONCLUSIVE` if the budget cannot resolve the meaningful effect.
- [ ] Freeze and hash the scenario text, fixtures, expectations, runner, parser, and decision rule before the first candidate result is inspected.
- [ ] Read repository instructions and inspect Git state before creating worktrees, temporary data, or runners.
- [ ] Start a run-owned resource ledger with every created absolute path, worktree, process ID, cache, account, dataset, report, and temporary artifact; never register pre-existing resources or credentials as cleanup targets.
- [ ] Require side-effect-free or idempotent scenarios and disposable accounts or datasets; define external-write authorization, cost and rate budgets, cleanup, and rollback evidence before execution.
- [ ] Return `BLOCKED` if candidates do not solve the same task, correctness cannot be independently graded, external effects cannot be isolated, or the decision rule is being chosen after results.

### 2. Build a Symmetric Harness

- [ ] Use the same runner, timeout, logging, environment construction, and artifact collection for every candidate.
- [ ] Create clean worktrees or equivalent isolated copies from the same commit and verify identical starting state.
- [ ] Inventory global and user-level instructions, hooks, plugins, settings, credentials, caches, and environment variables that can leak candidate behavior across supposedly isolated arms; disable, equalize, or record each one.
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
- [ ] Grade task completeness separately from correctness and efficiency: verify every required outcome and prohibited side effect, rather than treating a smaller diff, lower token count, or successful subset as completion.
- [ ] Blind manual or qualitative graders to candidate identity and randomize presentation order; record disagreements instead of resolving them toward a preferred candidate.
- [ ] Record timeout, crash, malformed output, partial completion, tool error, and environmental failure as distinct failure classes.
- [ ] Follow the predeclared repetition or sequential stopping rule; count and preserve all attempts, including failed and invalid runs. Do not keep retrying until the desired number of successes appears.
- [ ] Pause when environmental drift, rate limits, external outages, background load, or runner defects make additional runs incomparable.
- [ ] After a harness fix, invalidate affected comparisons and rerun both candidates for those scenarios under the corrected harness; retain unaffected evidence and label prior invalid results.
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
- [ ] Use `TIE` only when evidence supports the predefined negligible-difference margin or balanced tradeoff; failure to detect a difference with insufficient evidence is `INCONCLUSIVE`.
- [ ] Use `INCONCLUSIVE` when sample size, activation, oracle, environmental control, or conflicting scenarios prevent a reliable choice.
- [ ] Preserve reproducible commands, configuration, scenario definitions, expectations, raw results, normalized results, and analysis needed for independent verification.
- [ ] Remove only run-owned ledger entries: verify absolute paths remain inside approved temporary roots, stop exact recorded process IDs, preserve dirty or pre-existing worktrees, never delete credentials, and verify source and external baseline state.
- [ ] Report invalid runs, exclusions, confounders, sensitivity to assumptions, and how the conclusion could be falsified.
- [ ] Report residual decision risks that remain after the comparison, including unsupported workloads, unmeasured costs, unstable environments, and assumptions that could reverse the verdict.
- [ ] Verify that decision guidance follows scenario-level evidence and the frozen rule, with cleanup and limitations accounted for.

- [ ] Identify which decision the comparison can support, its valid workload/environment range, and conditions requiring another experiment; do not extrapolate outside observed evidence.

## Self-Check

- [ ] **Reconcile before returning.** Check item-level evidence, requirement coverage, contradictions, scope, verdict, and applicable cleanup. Correct the report or authorized artifacts. Reuse valid evidence; do not automatically rescan the repository or rerun successful commands. Repeat checks only for relevant changes, failures, or unresolved evidence. Disclose remaining gaps.

## Output Contract

Report in the user's language, in this order; retain all five fields and state each fact once. Small results may use one line per field; omit empty tables and do not copy linked artifacts:

1. **Result:** Skill-specific verdict and supported outcome.
2. **Scope:** Reviewed/changed scope, exclusions, baseline, and material assumptions.
3. **Evidence:** Skill-specific fields below; distinguish facts, inferences, and unverified claims. Link artifacts; use tables when useful.
4. **Verification:** Checks/results, unavailable evidence, and applicable cleanup/external state.
5. **Completion:** `Checklist: X/Y complete`; `Incomplete: None` or each `UNPROVEN` item's reason, outcome impact, and exact next action; residual risks and required decisions.

**Skill-specific evidence:** Frozen decision, candidates, scenarios, independent oracle, fixed variables, configuration, metrics, repetitions, exclusions, and decision rule. Prove activation and harness validity; report invalid runs, confounders, exclusions, and cleanup. Compare scenario-level completeness, correctness, failures, primary metric, spread/sample size, and other costs before aggregating. Preserve setup/maintenance tradeoffs, sensitivity, falsification conditions, raw results, configurations, scenario artifacts, and hashes when available.
