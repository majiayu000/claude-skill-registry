---
name: ln-72-product-outcome-evaluator
description: "Evaluates observed product outcomes against a prior hypothesis; does not run experiments or change user treatment."
---

# Product Outcome Evaluator

**Goal:** Determine what available evidence supports about a delivered product outcome and recommend continuation, adjustment or stopping. Remain read-only: do not change instrumentation, experiments, user treatment, campaigns or product files.

**Execution contract:** The ordered checkboxes are the Definition of Done. Track every item internally as `PENDING`, `PROVEN` with concrete evidence, `CLEARED` with evidence that its condition is absent, or `UNPROVEN` with a gap; reading, delegation, or tool failure is not proof. Reconcile items after each section. Before returning, resolve all `PENDING` and count only `PROVEN` and `CLEARED`; apply the skill's verdict and approval rules to every gap.
Preserve user intent, scope, and existing authorization. Continue authorized work; ask only for consequential unresolved choices or required external approval. Scale depth to material risk without silently skipping checks. Preserve dependency and safety ordering; otherwise choose the verification method appropriate to each obligation.
Treat equivalent user or repository evidence as valid input; another skill, named artifact, or complete lifecycle is not a prerequisite. Preserve source requirement and decision identifiers when available. Bind reused evidence to the relevant source version, dirty changes, configuration, and environment; invalidate only affected claims after a change.
On continuation, reconcile the task, existing authorization, current state, and unresolved evidence before resuming. For long work, return a compact continuation record or update an already authorized task artifact; read-only skills do not persist it. Distinguish artifact readiness, verified behavior, and authority to perform an external action.
Prepare authorized work before any required approval. If an instruction prevents progress, identify its exact source and explain the unresolved boundary; do not invent an approval gate from general caution.


## Tool Routing

| Need | Preferred capability | Fallback |
|---|---|---|
| Original hypothesis | Product intent, baseline, experiment/measurement plan and accepted targets | Reconstruct from attributable sources; keep missing targets unknown |
| Outcome evidence | Authorized analytics, experiment results, customer behavior and cost/support evidence | Sanitized exports with explicit measurement limits |
| Analysis | Reproducible queries/statistics appropriate to the study design | Transparent arithmetic and qualitative inference; no fabricated causal confidence |

## Domain Rules

- Distinguish delivered behavior, observed metric movement and causal product impact. A release or acceptance test proves neither adoption nor business value.
- Do not choose success thresholds after seeing the result. Separate predeclared criteria from exploratory findings and owner preferences.
- Use only authorized data with necessary minimization. A recommendation is not permission to run an experiment or contact users.

## Checklist

### 1. Frame the Outcome Decision

- [ ] Resolve the delivered capability, intended audience, original hypothesis, decision horizon and outcome decision requested.
- [ ] Identify the released/deployed version, rollout/exposure window and relevant baseline or comparison group.
- [ ] Recover predeclared primary metrics, guardrails, targets and stop rules; mark absent criteria rather than inventing them.
- [ ] Separate product intent and owner preference from measured behavior and external assumptions.

### 2. Assess Measurement Fitness

- [ ] Inspect metric definitions, units, denominators, event coverage, deduplication, identity joins and missing data.
- [ ] Check whether users were actually exposed and whether observation duration supports the intended outcome.
- [ ] Assess cohort composition, selection bias, seasonality, concurrent changes and other confounders.
- [ ] For experiments, inspect assignment, contamination, sample imbalance and uncertainty using the actual study design.
- [ ] Distinguish trustworthy measurements, reported results, estimates, qualitative signals and unavailable evidence.

### 3. Evaluate Value and Harm

- [ ] Compare outcomes with valid baselines or controls using reproducible calculations and appropriate uncertainty.
- [ ] Check guardrails and material regressions in user experience, reliability, support burden, cost or data quality.
- [ ] Separate aggregate effects from relevant segments and expose tradeoffs without fishing for favorable subgroups.
- [ ] Distinguish causal conclusions supported by the design from correlations and exploratory interpretations.
- [ ] Identify whether failure lies in adoption, interaction, correctness, measurement or the original value hypothesis.

### 4. Recommend the Next Decision

- [ ] Recommend continue, adjust or stop only to the degree supported by the evidence; explain what could reverse the recommendation.
- [ ] For uncertainty, define the cheapest next measurement or experiment with audience, signal, boundary and decision criterion without executing it.
- [ ] Return results linked to the original requirement/hypothesis and observed deployment state.
- [ ] Report data and causal limitations explicitly; do not transform lack of proof into proof of no effect.

## Verdict

- `SUPPORTED`: evidence supports the intended outcome within the stated population, window and causal limits.
- `NOT_SUPPORTED`: valid evidence contradicts the declared outcome or violates a required guardrail.
- `INCONCLUSIVE`: evidence cannot establish the outcome or causal interpretation.
- `BLOCKED`: essential hypothesis, exposure identity or authorized data is unavailable.

## Self-Check

- [ ] **Reconcile before returning.** Check item-level evidence, requirement coverage, contradictions, scope, verdict, and applicable cleanup. Correct the report or authorized artifacts. Reuse valid evidence; do not automatically rescan the repository or rerun successful commands. Repeat checks only for relevant changes, failures, or unresolved evidence. Disclose remaining gaps.

## Output Contract

Report in the user's language, in this order; retain all five fields and state each fact once. Small results may use one line per field; omit empty tables and do not copy linked artifacts:

1. **Result:** Skill-specific verdict and supported outcome.
2. **Scope:** Reviewed/changed scope, exclusions, baseline, and material assumptions.
3. **Evidence:** Skill-specific fields below; distinguish facts, inferences, and unverified claims. Link artifacts; use tables when useful.
4. **Verification:** Checks/results, unavailable evidence, and applicable cleanup/external state.
5. **Completion:** `Checklist: X/Y complete`; `Incomplete: None` or each `UNPROVEN` item's reason, outcome impact, and exact next action; residual risks and required decisions.

**Skill-specific evidence:** Hypothesis, deployed exposure, baseline/control, metric definitions and quality, reproducible results and uncertainty, guardrails, causal limits, recommendation and next evidence action.
