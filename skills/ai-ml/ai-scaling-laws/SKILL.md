---
name: ai-scaling-laws
description: "Sizes models and token budgets using Kaplan/Chinchilla scaling laws. Use when reasoning about compute-optimal N and D, tokens-per-parameter ratios, or over-training tradeoffs."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.0"
last_validated: 2026-07-11
---

# AI Scaling Laws — Compute-Optimal Sizing Skill

**Functional reference** for pre-training researchers and engineers who need to reason cold about compute, token, and parameter tradeoffs. Covers Kaplan et al. (2020), Chinchilla / Hoffmann et al. (2022), GPT-3 sizing, over-training for inference efficiency, and the mechanics of budget allocation for a from-scratch run.

This is a standard interview probe. Know the key ratios and be ready to work through a concrete sizing calculation without a lookup.

## Quick Reference

| Concept | Formula / Heuristic | Notes |
|---------|---------------------|-------|
| Compute budget | C ≈ 6 N D | N = non-embedding params, D = training tokens; approximate, constant ≈6 accounts for forward + backward |
| Chinchilla-optimal ratio | D ≈ 20 × N | From Hoffmann et al. 2022; holds compute constant |
| Kaplan (2020) ratio | D ≈ 1.7–2 × N (roughly) | Pre-Chinchilla; model-heavy. Difference from Chinchilla is *methodological* (FLOP counting, warmup, optimizer tuning), not simply "wrong" — see post-Chinchilla ref |
| Optimal N given C | N* ≈ (C / 120)^0.5 | Approximate; from Chinchilla Table A3 |
| Optimal D given C | D* ≈ (C / 0.3)^0.5 | Paired with above; verify against Hoffmann et al. Table A3 numbers |
| Over-training (Llama-style) | D ≫ 20 × N | Trades higher training loss for cheaper inference; standard for deployed open models. Llama 3 8B: 15T tokens ≈ 1,875 tok/param (dense example). Llama 4 (2025) is the current MoE example — apply the ratio to *activated*, not total, params |
| GPT-3 (175B) training tokens | ~300B tokens | 175B params × ~1.7 tok/param (Kaplan-era; undercooked by Chinchilla standard) |
| Chinchilla (70B) training tokens | ~1.4T tokens | 70B × 20; compute-matched to GPT-3 but smaller and more accurate |
| GPT-2 (124M) repro budget | ≈1–3 B tokens minimum | See worked example below |
| Published fit constants | α≈0.336, β≈0.283 | **Corrected by Besiroglu et al. 2024 to α≈0.35, β≈0.37** — original fit had convergence/rounding errors |

**Key distinction:** Chinchilla-optimal minimizes validation loss *for a given compute budget*. It is not inference-optimal. Over-training a smaller model to more tokens gives a model that is cheaper per inference call, even though it spent more of the compute budget on data than the loss-optimal split would dictate.

## ASCII Flow

```text
Fix compute budget C (e.g. GPU-hours × FLOPs/hour)
           |
           v
C ≈ 6 N D  →  Solve for Chinchilla-optimal pair
           N* ≈ sqrt(C / 120),  D* ≈ 20 × N*
           |
           v
Adjust for inference cost constraint
  If inference is expensive: shrink N, increase D (over-train)
  If training cost dominates: stay near Chinchilla-optimal
           |
           v
Set token budget D = training tokens
  Constrain by data availability — data quality shifts the curve
  Verify token count is achievable from your corpus
           |
           v
Choose batch size, LR schedule, warmup to fill D tokens
```

## When to Use This Skill

- Answering: "How many tokens should I train on for a model of size X?"
- Answering: "Given a GPU budget of Y A100-hours, what model size and token count should I target?"
- Evaluating whether a published training run is compute-optimal, over-trained, or under-trained
- Sizing a GPT-2 reproduction or any from-scratch experiment
- Interview preparation: compute/data/param tradeoff reasoning

## Scope Boundaries

Depth on adjacent topics lives in these skills:

- **Pre-training implementation, data pipelines, optimizer config** → [ai-pretraining](../ai-pretraining/SKILL.md)
- **Distributed training, tensor/pipeline parallelism, MFU** → [ai-distributed-training](../ai-distributed-training/SKILL.md)
- **Token budget sourcing, deduplication, quality filters** → [ai-data-curation-pretraining](../ai-data-curation-pretraining/SKILL.md)
- **Model architecture, post-training, deployment** → [ai-llm](../ai-llm/SKILL.md)

## Sizing Workflow

1. **Fix compute budget C** in FLOPs. Multiply GPU-hours by peak FLOPs/s and hardware utilization (MFU; typically 30–50% for realistic training).
2. **Apply C ≈ 6 N D** to enumerate feasible (N, D) pairs along the iso-compute curve.
3. **Pick Chinchilla-optimal point**: D* ≈ 20 × N (equivalently N* ≈ D / 20). For the exact coefficients use Hoffmann et al. Table A3.
4. **Check data availability**: if your corpus yields fewer than D* tokens at acceptable quality, you are data-constrained; shrink N or accept suboptimal allocation.
5. **Adjust for inference regime**: if you will serve the model at high QPS, favor a smaller N trained on more tokens (over-trained relative to Chinchilla). If training cost is the binding constraint, stay near Chinchilla-optimal.
6. **Set hyperparameters**: peak LR typically scales as ~N^{-0.5} (rough heuristic); batch size scales with D; cosine decay or trapezoidal schedule over D tokens.

## Worked Example: GPT-2 124M Reproduction on 8× A100s

**Given:**
- 8 × A100 80GB, ~312 TFLOP/s each at BF16
- Rough MFU: ~40% (realistic for a small well-tuned training script)
- Available training time: ~8 GPU-hours (≈ 1 hour wall-clock on 8 GPUs)

**Step 1 — Compute budget C:**
```
C = 8 GPUs × 312e12 FLOP/s × 0.40 MFU × 8 × 3600 s
  ≈ 8 × 312e12 × 0.40 × 28800
  ≈ 2.9e19 FLOPs   (≈ 29 PetaFLOP)
```

**Step 2 — N for GPT-2 124M:**
N ≈ 124e6 params (non-embedding; the embedding matrix ~38M is conventionally excluded from scaling law N; total is ~162M but N ≈ 124M is the standard usage)

**Step 3 — Chinchilla-optimal D:**
```
D* ≈ 20 × N = 20 × 124e6 ≈ 2.5B tokens
```

**Step 4 — Sanity-check with C ≈ 6 N D:**
```
C_needed = 6 × 124e6 × 2.5e9 ≈ 1.86e18 FLOPs
```
Our 8-GPU 8-hour budget of ~2.9e19 FLOPs comfortably covers this — we have ≈15× more compute than strictly needed for Chinchilla-optimal at 124M. This means we could:
- Train for far fewer hours (≈ 30 min wall-clock), or
- Over-train to 3–5B tokens to improve the model cheaply while we have the budget.

**Conclusion:** For a GPT-2 124M reproduction at this budget, target **2–3B tokens minimum**; the budget supports over-training to 5–10B tokens if data is available, yielding a better model at no extra GPU cost.

**Note:** All figures above are approximate. MFU, batch size, and sequence length all affect realized throughput. Verify your actual tokens/second empirically before locking a training schedule.

## Known Traps

1. **Using Kaplan (2020) ratios after Chinchilla corrected them.** Kaplan suggested scaling models much faster than data (~D ∝ N^{0.74}). Chinchilla showed equal scaling. GPT-3 is a canonical example of a Kaplan-era undercooked model: 175B params but only ~300B tokens, whereas Chinchilla-optimal would require ~3.5T tokens.

2. **Conflating Chinchilla-optimal with inference-optimal.** The Chinchilla optimum minimizes training loss for a fixed compute budget. Llama, Mistral, and most open-weight models deliberately over-train smaller models because inference cost matters more than training cost for deployed models.

3. **Conflating total parameters with non-embedding parameters.** Scaling laws in Kaplan and Chinchilla use N = non-embedding parameters. For models with large vocabularies, the embedding table can be 20–30% of total parameters. Use the non-embedding count in the C ≈ 6ND formula.

4. **Ignoring that data is often the binding constraint.** High-quality deduplicated text in a specific domain is finite. When the corpus cannot provide D* tokens at acceptable quality, the model is data-constrained regardless of the compute budget. Data quality shifts the effective loss curve — better data means lower loss at the same N and D.

5. **Treating the 20:1 heuristic as a universal law.** The exact coefficient varies with model architecture, data quality, and what loss metric is being optimized. The 20:1 ratio is the central Chinchilla finding but empirical fits from Epoch AI and others show the true optimum is sensitive to these factors.

6. **Quoting Chinchilla's published fit constants as ground truth.** Besiroglu et al. (2024) showed the Approach-3 fit (α≈0.336, β≈0.283) is biased by a pre-convergence optimizer and rounding; corrected exponents are α≈0.35, β≈0.37. Use the corrected values for projections.

7. **Saying "Kaplan was wrong."** The Kaplan/Chinchilla split is methodological (FLOP counting, warmup, optimizer tuning); correcting those reproduces Chinchilla's C^0.50 from Kaplan's setup (Pearce & Song 2024; Porian et al. 2024).

8. **Ignoring inference cost when sizing a deployed model.** Chinchilla optimizes training loss for training compute only. For anything served at scale, minimize *total* train+serve compute — which means smaller-and-longer than Chinchilla (Sardana & Frankle 2024).

9. **Assuming the param count is precision-independent.** Low-precision training lowers the *effective* param count, and PTQ damage grows with training tokens (Kumar et al. 2024). Plan quantization headroom alongside the token budget.

## Common Anti-Patterns

- Choosing model size from a published architecture (e.g., "I want to do a GPT-2 run") without computing whether the training token budget is sufficient for that size.
- Setting training tokens to a round number (e.g., "1B tokens") without reference to the model size.
- Reporting parameter count without specifying whether embedding parameters are included.
- Assuming the Chinchilla-optimal training run produces the best inference-time model.
- Extrapolating scaling law curves beyond the range of the original data without acknowledging the extrapolation.

## Core Principles

1. **Hold compute constant when comparing.** Scaling law comparisons are only meaningful on an iso-compute curve. Comparing a bigger model trained for fewer steps to a smaller model trained for more steps conflates model size with compute.

2. **Tokens and parameters scale together.** The Chinchilla result is not "more data is better." It is that the *ratio* D/N should be ~20 when compute is the constraint. Both must scale proportionally.

3. **The optimum is a ratio, not a number.** There is no universal "correct" model size. Given a fixed compute budget, there is an optimal (N, D) pair. Given a fixed inference budget, the optimal N is smaller (more over-training).

4. **Data quality shifts the loss curve.** Two training runs with the same N and D but different data quality will reach different loss values. Scaling laws are fit on specific corpora; the exact coefficients do not transfer directly to new domains without re-fitting or empirical validation.

## Post-Chinchilla Developments (2023–2026)

Kaplan and Chinchilla are foundations, not the current frontier. A July-2026 answer is incomplete without these. Full detail in **[post-chinchilla-developments.md](references/post-chinchilla-developments.md)**.

1. **Chinchilla's published fit was corrected** (Besiroglu et al. 2024). The Approach-3 constants are biased (pre-convergence optimizer + rounding); corrected exponents are α≈0.35, β≈0.37. The ~20:1 heuristic survives as an order-of-magnitude rule; the exact constants do not.
2. **Repeating data is nearly free up to ~4 epochs** (Muennighoff et al. 2023). When data-bound, train a smaller model for more epochs rather than under-feeding a Chinchilla-sized model. Marginal value of repeats decays to ~0 past ~16 epochs.
3. **Inference-aware scaling** (Sardana & Frankle 2024). Account for serving cost: deployed models should be smaller and trained far longer than Chinchilla-optimal. Quality improves out to ~10,000 tok/param.
4. **Over-training is the deployed norm.** Llama 3 8B used 15T tokens (~1,875 tok/param), ~75× Chinchilla-optimal, deliberately, for inference efficiency.
5. **Precision-aware scaling** (Kumar et al. 2024). Low-precision training lowers *effective* param count; PTQ damage grows with training tokens, so over-training can hurt a heavily-quantized deployment. Use effective (precision-adjusted) params.
6. **MoE/sparsity scaling** (Ludziejewski et al. 2024; Abnar et al. 2025). Apply 6ND with *activated* params; expert granularity and sparsity are first-class optimization knobs, not a footnote on a dense law.
7. **Test-time-compute scaling** (Snell et al. 2024). Inference compute (sampling + verification, search over reasoning) is a third axis, substitutable with pretraining: few-query/low-volume favors a small model + heavy test-time compute (can beat a ~14× larger model); high-volume favors pretraining bigger. The scaling law under the o1/o3 reasoning paradigm.
8. **Distillation scaling** (Busbridge et al. 2025). A law for distilled-student loss vs teacher/student compute split: distill when a teacher exists or you serve many students; train supervised when only one student is needed and the teacher must also be trained.
9. **RL post-training compute — a fourth axis, still unsettled** (Meta et al. 2025; arXiv:2509.25300, 2025; CoScale-RL 2026). Reasoning-model RL compute (rollouts + verifier + policy updates) follows a sigmoidal, recipe-dependent curve, not a clean Chinchilla-style power law. Don't quote a fixed RL-compute coefficient as settled science — this is the least mature scaling regime as of mid-2026.

## Navigation: Core References

- **[Chinchilla Math](references/chinchilla-math.md)** — L(N,D) loss form, 20:1 derivation intuition, worked numbers from Hoffmann et al., the 2024 fit correction
- **[Compute Budget Estimation](references/compute-budget-estimation.md)** — C = 6ND derivation, FLOPs-to-GPU-hours conversion, worked table
- **[Post-Chinchilla Developments](references/post-chinchilla-developments.md)** — 2023–2026 corrections and extensions: data-constrained, inference-aware, precision, MoE, Kaplan/Chinchilla reconciliation, test-time-compute and distillation scaling

## External Sources

See **[data/sources.json](data/sources.json)** for canonical papers and primary sources:
- Kaplan et al. "Scaling Laws for Neural Language Models" (arXiv 2001.08361)
- Hoffmann et al. "Training Compute-Optimal Large Language Models" / Chinchilla (arXiv 2203.15556)
- Besiroglu et al. "Chinchilla Scaling: A replication attempt" (arXiv 2404.10102) — corrects the Chinchilla fit
- Muennighoff et al. "Scaling Data-Constrained Language Models" (arXiv 2305.16264)
- Sardana & Frankle "Beyond Chinchilla-Optimal: Accounting for Inference" (arXiv 2401.00448)
- Kumar et al. "Scaling Laws for Precision" (arXiv 2411.04330)
- Brown et al. GPT-3 (arXiv 2005.14165)

## Fact-Checking Rule

- Known bugs, regressions, framework/compiler/runtime footguns, and version-specific crash or workaround guidance must be verified against current primary web sources before being treated as current fact.
- Verify volatile external facts before final answers.
- Prefer official docs, standards, release notes, and pricing pages.
- If you cannot verify, say so explicitly and present the guidance as a dated assumption instead of a fact.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.
