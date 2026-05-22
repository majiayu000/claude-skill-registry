---
name: model
description: Algorithm/model development and fine-tuning skill. Use for tasks like dataset design/cleaning, supervised fine-tuning (SFT), preference optimization (DPO/RLHF concepts), LoRA/QLoRA, training configs, evaluation (offline/online), safety checks, deployment packaging, and cost/performance trade-offs.
---

# model

Use this skill for 算法/模型开发/模型微调：从数据到训练到评测再到上线。

## Defaults / assumptions to confirm

- Goal: improve quality, reduce cost/latency, add domain knowledge, safety alignment?
- Base model and license constraints
- Hardware: local GPU / multi-GPU / cloud
- Target inference stack (vLLM, TGI, llama.cpp, etc.)

## Workflow

1) Define the objective and success metrics
- Task definition and input/output format.
- Primary metrics (task-specific) + guardrails (safety, latency, cost).
- Failure analysis categories (hallucination, format errors, refusal, toxicity).

2) Data strategy (most important)
- Collect/curate dataset; define labeling guidelines.
- Remove duplicates, leakage, PII, and near-duplicates.
- Balance by scenario; ensure coverage of edge cases.
- Split train/val/test with strict leakage prevention.

3) Choose training approach
- SFT for instruction following and domain formatting.
- LoRA/QLoRA for efficient fine-tuning (default for most cases).
- DPO/Preference tuning when “style/quality preference” is the target.
- Avoid fine-tuning when RAG or prompting solves it cheaper.

4) Training setup
- Pick tokenizer/model family compatibility.
- Hyperparameters: LR, batch size, sequence length, warmup, weight decay.
- Checkpoints and resume strategy; deterministic seeds.
- Track experiments (configs, metrics, artifacts).

5) Evaluation
- Offline eval set: small but representative; include hard negatives.
- Automatic metrics where meaningful; human eval for subjective qualities.
- Regression tests: keep a fixed “golden set” across iterations.

6) Safety & compliance
- Filter sensitive data; define refusal policy and tests.
- Measure unsafe outputs; create adversarial eval prompts.

7) Deployment
- Export adapters/merged weights; document inference requirements.
- Quantization plan if needed; benchmark latency and throughput.
- Monitor in production: quality signals, drift, safety incidents.

## Outputs

- Data spec: sources, schema, labeling rules, splits.
- Training plan: method (SFT/LoRA/DPO), configs, compute estimate.
- Eval plan: datasets, metrics, sampling, acceptance thresholds.
- Deployment plan: packaging, quantization, benchmarks, monitoring.

