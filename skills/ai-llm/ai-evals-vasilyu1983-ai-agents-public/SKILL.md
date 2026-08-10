---
name: ai-evals
description: "Designs trustworthy LLM/agent evals and optimization loops. Use when building graders, calibrating judges, choosing eval/fine-tune methods, thresholds, or fixing noisy scores."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.3"
last_validated: 2026-07-11
---

# AI Evaluation and Fine-Tuning Methodology Skill

**Core stance**: an eval is an instrument. An untrusted instrument is worse than
no instrument, because it produces confident wrong numbers that ship regressions.
Fine-tuning is an optimization loop around that instrument. If the instrument is
weak, training just makes the model better at gaming bad measurement. This skill
is the cross-domain methodology layer that domain eval and model-lifecycle skills
defer to: how to keep an LLM-as-judge honest, integrate eval frameworks, choose
between prompting/context/tools/test-time compute/SFT/preference/RFT/PEFT/
distillation, derive thresholds instead of guessing them, and stop flaky runs or
training leakage from masquerading as progress.

This is the **methodology umbrella** for evals. Domain skills own *what* to
measure; this skill owns *whether you can trust the measurement*.

- Building an eval system for a **coding agent** -> [ai-coding-agents-observability-evals](../ai-coding-agents-observability-evals/SKILL.md)
- Evaluating **RAG / retrieval / search** -> [ai-rag](../ai-rag/SKILL.md)
- Running **Hub model benchmarks** (inspect-ai, lighteval) -> use the `huggingface-skills:` plugin (external)
- General **LLM lifecycle** decisions -> [ai-llm](../ai-llm/SKILL.md)
- This skill: **judge bias, framework choice, calibration, reproducibility,
  optimization technique gates** —
  the parts those four share and none owns in depth.

## ASCII Flow

```text
eval need
  |
  v
define verifiable goal  (what would FAIL if the requirement reverted?)
  |
  v
choose grader
  deterministic check  ->  LLM-as-judge  ->  human label  (cheapest that works)
  |
  v
control judge bias
  position / length / self-preference / verbosity
  |
  v
derive thresholds from a labeled calibration set  (not vibes)
  |
  v
choose optimization path  (prompt/RAG/tools -> SFT -> preference/RFT/PEFT)
  |
  v
choose inference-time lift  (self-consistency / rerank / verify / refine)
  |
  v
control flake  (pass@k, low temp, quarantine unstable cases)
  |
  v
trustworthy gate  ->  train / block / ship / rollback
```

## Quick Reference

| Task | Read or Run | Outcome |
|------|-------------|---------|
| Build a (question, ideal-answer) set and tune it | `references/dataset-construction.md` | Sourcing, ideal-answer authoring, run→compare→tune loop |
| Stop a judge from rating its own output high | `references/llm-judge-bias.md` | Self-preference, position, length, verbosity controls |
| Pick / wire an eval framework | `references/framework-integration.md` | inspect-ai, lighteval, Ragas, DeepEval, promptfoo, Braintrust integration snippets + when to use each |
| Choose a pass threshold defensibly | `references/threshold-derivation.md` | Derive thresholds from a labeled set; inter-rater agreement; gate design |
| Stop flaky runs reading as regressions | `references/flake-and-reproducibility.md` | pass@k, seeds, temperature, quarantine, contamination/leakage |
| Decide if "A beats B" is real, size the set | `references/eval-statistics.md` | Bootstrap CIs, McNemar, power/MDE sizing, FDR, variance reduction |
| Get maximum from an LLM | `references/llm-optimization-technique-map.md` | Technique ladder across prompts, data, RAG/tools, test-time compute, SFT, preference/RFT, PEFT, distillation |
| Decide whether and how to fine-tune | `references/fine-tuning-eval-loop.md` | Prompt/RAG/tool baseline, SFT vs preference/RFT vs PEFT, split hygiene, promotion gates |
| Evaluate on live/production traffic | `references/online-production-eval.md` | Offline-online correlation, A/B+guardrails, shadow/canary, drift, regression replay, HITL |
| Evaluate refusals, jailbreaks, harm | `references/safety-redteam-eval.md` | Over/under-refusal, ASR per attack family, injection, harm rubrics, robustness |
| Go beyond one judge | `references/advanced-judging.md` | Juries, fine-tuned judges, CoT/probability scoring, calibration (kappa/ECE), agentic reward |

## When to Use This Skill

Activate when the user asks for:

- An LLM-as-judge / LLM grader and how to keep it honest
- Why eval scores look inflated, noisy, or contradictory
- Which eval framework to use, or how to integrate one
- How to set or justify a pass/fail threshold or release gate
- Pairwise / preference evaluation between two prompts, models, or harnesses
- Reducing eval flakiness, contamination, or testset leakage
- Calibrating a judge against human labels
- Deciding whether to fine-tune, how to select SFT vs preference/RFT vs PEFT, or
  whether a fine-tuned model is genuinely better than a prompt/RAG/tool baseline
- Getting maximum performance from an LLM using known techniques, including
  prompt/context/tool changes, test-time compute, reranking, distillation, or
  post-training

## Scope Boundaries (Use These Skills for Depth)

- **Domain metrics for retrieval** (nDCG/MRR/recall, faithfulness) -> [ai-rag](../ai-rag/SKILL.md)
- **Agent golden tasks, tool-call grading, cost ops** -> [ai-coding-agents-observability-evals](../ai-coding-agents-observability-evals/SKILL.md)
- **Running benchmark harnesses on Hub models** -> use the `huggingface-skills:` plugin (external)
- **Prompt CI/CD and structured output contracts** -> [ai-prompt-engineering](../ai-prompt-engineering/SKILL.md)
- **General model selection, serving, quantization, and deployment economics** ->
  [ai-llm](../ai-llm/SKILL.md) and [ai-llm-inference](../ai-llm-inference/SKILL.md)

## Workflow

1. **Transform the vague ask into a verifiable goal.** "Is it good?" is not
   gradeable. Ask: which case would fail first if the requirement reverted?
2. **Build the dataset before the grader.** Source real questions, author ideal
   answers from the system's allowed context, and plan the run→compare→tune loop
   — see `references/dataset-construction.md`. No dataset, no eval.
3. **Pick the cheapest grader that works.** Deterministic check > LLM judge >
   human. Reserve the LLM judge for what code cannot decide (Rule 5: use the
   model only for judgment calls).
4. **If using an LLM judge, control its bias** before trusting any number — see
   `references/llm-judge-bias.md`. Untreated judge bias is the #1 source of
   confidently-wrong eval scores. When one judge isn't enough (high stakes, weak
   agreement, open-ended), escalate to juries / fine-tuned judges / calibrated
   scoring — see `references/advanced-judging.md`.
5. **Control flake and leakage** with pass@k, low judge temperature, seed
   pinning, and held-out testsets — see `references/flake-and-reproducibility.md`.
6. **Derive thresholds from a labeled calibration set**, not intuition or copied
   targets — see `references/threshold-derivation.md`. **Size the gating set and
   judge "A beats B" with statistics** (bootstrap CIs, McNemar, power/MDE, FDR) —
   see `references/eval-statistics.md`. A score difference without a CI is not a
   result.
7. **Only fine-tune after the baseline has earned it.** Compare prompt/RAG/tool
   fixes first, then choose SFT for imitation/style/format/tool-call behavior,
   preference/RFT for rubric-scored reasoning or tradeoffs, and PEFT/LoRA/QLoRA
   when adapting an open model under compute or deployment constraints — see
   `references/fine-tuning-eval-loop.md`. Training loss is telemetry; held-out
   behavior is the verdict.
8. **Apply the full optimization ladder, not one pet method.** For maximum LLM
   performance, evaluate cheap prompt/context/tool fixes, then inference-time
   methods (self-consistency, best-of-N, rerank/verify/refine), then data/SFT,
   preference/RFT/RLVR, PEFT, and distillation as the evidence warrants — see
   `references/llm-optimization-technique-map.md`. Each technique gets its own
   failure mode and gate.
9. **Gate loudly.** A gate that passes while silently skipping cases is a
   failure dressed as success (Rule 12: fail loud). Report skipped/quarantined
   cases in the gate output.
10. **Extend past the offline gate where the system warrants it.** Add
   safety/red-team evaluation (refusal precision/recall, jailbreak ASR,
   injection, harm rubrics) — see `references/safety-redteam-eval.md` — and, once
   in production, online evaluation (offline-online correlation, A/B with
   guardrails, drift, regression replay) — see `references/online-production-eval.md`.
   The offline gate is a filter; production is the verdict.

## Core Principles

- **The judge is a model with failure modes.** Treat its scores as one
  calibrated input, never as ground truth.
- **Different judge than the one under test.** Self-preference bias is real and
  large; never gate on a model grading its own family/config.
- **Behavior, not plausibility.** Rubrics that reward "looks good" reward length
  and confidence. Pin rubrics to verifiable behavior.
- **No threshold without a labeled set.** A copied target (">95%") is a guess
  until validated on your own distribution.
- **No fine-tune without a baseline and a holdout.** A tuned model that beats no
  prompt/RAG/tool baseline, or only wins on the training/dev set, has not earned
  release.
- **No "maximum performance" without a technique ladder.** The best result often
  comes from composition: cleaner data + stronger retrieval/tool contracts +
  calibrated judge + small test-time search + selective post-training. Test the
  cheapest credible lift before moving weights.
- **Optimize behavior, not hidden knowledge.** Fine-tune for stable formatting,
  domain style, tool-use patterns, rubric-following, or compact specialized
  behavior. Use retrieval/context for facts that change or must be cited.
- **Flake is a broken test, not a regression.** A verdict that flips run-to-run
  means the eval is wrong, not the system.
- **Held-out or it's contaminated.** If tuning ever saw the eval cases, the
  scores are inflated.
- **Goodhart's Law is the default outcome, not an edge case.** Any metric that
  becomes a target (a threshold, a bonus, a promotion gate) will eventually be
  gamed — by the system under test, by whoever tunes against it, or by the judge
  itself. Every trap and anti-pattern in this file is a specific instance of
  this one law; treat a metric that stops correlating with the outcome you
  actually care about as expected decay, and re-anchor it against production
  outcomes or fresh human judgment on a schedule, not only when someone notices.
- **A point estimate is not a result.** Every reported number in this skill's
  gates — pass rate, win rate, judge-human agreement — is a sample statistic
  with sampling error. Report it with a confidence interval or it is not
  reportable; see `references/eval-statistics.md`.

## Known Traps

- Grading an agent with the same model that produced the output (self-preference)
- Comparing two candidates in fixed order and trusting the winner (position bias)
- Copying a `>95%` threshold from a blog without validating it on your data
- One judge call per request with no cheap deterministic pre-filter (cost blowup)
- Treating a run-to-run verdict flip as a real regression instead of quarantining
- Generating a synthetic testset from the same docs used to tune the system
- Reporting "all passed" when some cases were skipped or errored (silent success)
- Claiming "A beats B" from a point estimate with no confidence interval or test
- Gating a small regression on a set far too small to detect it (no power check)
- Tuning safety to block harm without a benign set, so the model over-refuses
- Trusting a seed for reproducibility through a hosted API that isn't deterministic
- Fine-tuning because the prompt is messy, the retrieval is broken, or the tool
  contract is ambiguous
- Declaring the fine-tune better from training loss, validation loss, or one
  cherry-picked demo instead of a paired held-out eval with CIs
- Letting the training set, grader calibration set, and release gate share cases
- Training a judge or reward model on labels produced only by the same model
  family it will later grade

## Common Anti-Patterns

- Vibes-based eval: spot-checking a few outputs and calling it evaluation
- Single-metric gates: one aggregate number hiding per-slice regressions
- LLM-judge-only: no deterministic floor, so the gate inherits the judge's noise
- Threshold-on-the-fly: setting the cutoff after seeing results to make it pass
- Framework-as-strategy: adopting one vendor tool as the whole eval program
- Fine-tune-as-strategy: reaching for SFT/RFT/LoRA before proving the failure is
  learned behavior rather than prompt, context, tools, or product spec
- Technique soup: stacking CoT, self-consistency, rerankers, judges, and
  post-training without isolating which intervention caused the lift

## Navigation

Resources:

- [references/dataset-construction.md](references/dataset-construction.md) - Sourcing questions, authoring ideal answers, run→compare→tune loop
- [references/llm-judge-bias.md](references/llm-judge-bias.md) - Judge bias taxonomy and controls
- [references/framework-integration.md](references/framework-integration.md) - Framework selection and integration snippets
- [references/threshold-derivation.md](references/threshold-derivation.md) - Deriving thresholds and gates from labeled data
- [references/flake-and-reproducibility.md](references/flake-and-reproducibility.md) - Flake, seeds, contamination, leakage
- [references/eval-statistics.md](references/eval-statistics.md) - Bootstrap CIs, McNemar, power/MDE, FDR, variance reduction
- [references/llm-optimization-technique-map.md](references/llm-optimization-technique-map.md) - Maximum-performance technique ladder and eval gates
- [references/fine-tuning-eval-loop.md](references/fine-tuning-eval-loop.md) - Eval-first fine-tuning decisions, SFT/preference/RFT/PEFT selection, split hygiene, promotion gates
- [references/online-production-eval.md](references/online-production-eval.md) - Offline-online correlation, A/B+guardrails, drift, replay, HITL
- [references/safety-redteam-eval.md](references/safety-redteam-eval.md) - Refusal precision/recall, jailbreak/injection, harm rubrics, robustness
- [references/advanced-judging.md](references/advanced-judging.md) - Juries, fine-tuned judges, scoring methods, calibration, agentic reward
- [data/sources.json](data/sources.json) - Sources to verify against

Related skills:

- [ai-llm](../ai-llm/SKILL.md), [ai-rag](../ai-rag/SKILL.md), [ai-coding-agents-observability-evals](../ai-coding-agents-observability-evals/SKILL.md)

## Fact-Checking

- Eval framework APIs (inspect-ai, lighteval, Ragas, DeepEval, promptfoo,
  Braintrust) change across releases. Verify current API and version against
  official docs before recommending a specific call or flag.
- Fine-tuning platform support, model eligibility, dataset schemas, and RFT/grader
  APIs move quickly. Verify the current official docs before recommending a
  specific model, endpoint, hyperparameter, or CLI.
- Optimization-method papers from arXiv are often preprint-only and
  benchmark-sensitive. Treat unreplicated methods as `validate`, not `promote`,
  until they beat a strong local baseline with cost/latency/safety gates.
- Judge-bias findings (position, length, self-preference) are well-replicated
  through 2025-2026, but specific magnitudes are model- and prompt-dependent —
  re-measure on your own setup; do not quote a fixed number as universal.
- Fine-tuned-judge models (Prometheus, JudgeLM, and successors) and jailbreak
  attack/defense results move fast — verify the current model, license, and
  benchmark-agreement claims before recommending a specific judge or asserting a
  model is robust to a given attack family.
- Indirect prompt injection is the dominant agentic attack as of 2026; treat any
  "the agent is safe against injection" claim as requiring fresh adaptive testing.
- Statistics methods (bootstrap, McNemar, FDR, power/MDE) are stable, but verify
  the exact API (scipy/statsmodels) before copying a call.
- If web access is unavailable, mark framework-version claims as unverified.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md`
(and `learnings.md` if present). After applying it, append one dated bullet to
`learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py` if you
hit a pattern, mistake, or surprising fact. Do not modify `SKILL.md` itself.
