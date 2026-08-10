---
name: ai-local-model-ops
description: "Runs local and self-hosted LLM workflows with Ollama, LM Studio, MLX, Open WebUI, llamafile, and adapters. Use when operating private model stacks."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# Local Model Operations

Use this skill to choose and operate local or self-hosted LLM workflows when privacy, offline access, or low-friction experimentation matter more than large-cluster serving.

This skill covers:

- local runtime choice for laptops, workstations, and small self-hosted setups
- team-facing local or private chat surfaces
- single-binary or minimal-dependency model packaging
- lightweight adaptation paths before full training or cluster-scale serving
- evaluation and escalation rules before a local stack becomes a product dependency

## ASCII Flow

```text
local/private model need
  |
  v
constraint
  privacy | offline | cost | hardware | demo portability | team chat
  |
  v
runtime selection
  Ollama | LM Studio | MLX | Microsoft Foundry Local | Open WebUI | llamafile | lightweight adapter workflow
  |
  v
local operating contract
  pinned model + quantization + eval set + storage/privacy boundary
  + optimization levers: KV-cache quant | speculative decoding | NPU tier
  |
  v
use or escalate
  local workflow OR hand off to inference/MLOps for production serving
```

## Quick Reference

| Need | Default path | Notes |
|------|--------------|-------|
| Run a local model quickly | Ollama | Lowest-friction day-0 local runtime for experiments and private workflows |
| Share a self-hosted chat UI | Open WebUI | Best fit when a team needs a ChatGPT-like local or private interface |
| Ship a no-install demo or portable binary | llamafile | Useful for single-file distribution and low-ops delivery |
| Apple Silicon on-device inference at framework level | MLX (mlx-lm) | Primary path for Metal-native inference and LoRA fine-tune on Mac; verify at https://github.com/ml-explore/mlx-lm |
| GUI model browser and switcher (non-technical users) | LM Studio | Supports GGUF and MLX; good for rapid model comparisons |
| Windows / enterprise SDK-first local inference | Microsoft Foundry Local | Curated Microsoft catalog; SDK + REST; verify at https://learn.microsoft.com/en-us/ai/foundry-local |
| Fine-tune or adapt cheaply | Unsloth + `../ai-llm/SKILL.md` | Good for lightweight adaptation, not a substitute for full training ops |
| Optimize throughput or production serving | `../ai-llm-inference/SKILL.md` | Use this skill for local ops; use `ai-llm-inference` for deeper serving engineering |

## Runtime Selection

| Situation | Best fit |
|-----------|----------|
| Solo developer or analyst on one machine | Ollama |
| Internal team chat with local or self-hosted models | Open WebUI |
| Portable model demo or offline executable distribution | llamafile |
| Fast adapter and fine-tuning iteration on limited hardware | Unsloth |
| Apple Silicon, framework-level inference or LoRA fine-tune | MLX (mlx-lm) |
| Non-technical user, GUI model management | LM Studio |
| Windows-primary, SDK-first, Microsoft model catalog | Microsoft Foundry Local |

See [references/desktop-runtime-landscape.md](references/desktop-runtime-landscape.md) for a detailed Ollama / LM Studio / Foundry Local comparison.

## Local vs Hosted API: Judgment, Not Reflex

Do not default to "local" just because privacy or cost was mentioned once. Decide with a real eval set and a real cost model:

- Local tends to win on data residency/offline requirements, steady high-volume traffic that amortizes hardware cost, sub-100ms latency needs, and narrow tasks where a well-evaluated 7–32B open model already matches frontier quality.
- Hosted API tends to win on frontier-tier reasoning or long-context needs that no locally-runnable model size covers yet, spiky/low-volume traffic, or when local ops overhead (drivers, quant regressions, capacity planning) would cost more engineering time than the API bill.
- Full frontier-scale open weights (DeepSeek-V3/R1-class, Mistral Large 3, Llama 4 Maverick) do not fit on a single consumer GPU or single H100 at usable quant — "open-weight" does not mean "runs on your laptop." Check the model-sizing matrix before promising local feasibility.

See [references/model-sizing-matrix.md](references/model-sizing-matrix.md#local-vs-api-the-real-tradeoff) for the full tradeoff and current family-by-family sizing (Llama, Qwen, DeepSeek, Mistral, Gemma, GPT-OSS).

## Default Workflow

1. Define the real constraint first: privacy, offline use, cost ceiling, hardware ceiling, or demo portability.
2. Pick the runtime or UI layer that matches that constraint.
3. Pin model IDs, quantization choice, and prompt/eval set before broader rollout.
4. Decide whether the stack is only for local use or will become part of a product or team workflow.
5. If it needs stronger serving, routing, or monitoring, hand off to the adjacent skills instead of stretching a local-first setup too far.

## Operational Rules

- Keep model IDs and quantization choices explicit and versioned.
- Treat local and self-hosted endpoints as sensitive services, not casual defaults for internet exposure.
- Measure quality on a small real eval set before swapping local models into a user-facing workflow.
- Separate runtime selection from product integration. Running a model locally is not the same thing as shipping a good AI feature.

## Known Traps

- Treating a laptop prototype as proof that a workflow is production-ready. Latency, uptime, auth, and observability requirements change immediately once real users appear.
- Leaving model IDs, quant levels, and system prompts implicit. Local stacks drift quickly when operators rely on tags like `latest`.
- Exposing Ollama, Open WebUI, or ad hoc reverse proxies without an explicit threat model and access controls.
- Assuming a polished chat UI solves governance. UI convenience does not replace logging, retention policy, or approval paths.
- Using lightweight local adaptation as a substitute for evaluation discipline. Faster iteration is useful only if the eval loop is real.
- Using vLLM V0 features — V0 is fully deprecated as of 2026. Use the V1 engine (see https://docs.vllm.ai/en/stable/usage/v1_guide/).
- Citing vendor speedup figures (e.g., Microsoft Foundry Local vs cloud) as neutral benchmarks — always measure on your own workload.
- Assuming speculative decoding helps at high concurrency — the benefit is concentrated at batch size 1.
- Running NPU inference without confirming the accelerator is being used — fallback to CPU/GPU is silent in some runtimes.

## Common Anti-Patterns

- Installing several local runtimes at once before deciding which constraint actually matters: privacy, portability, cost ceiling, or offline access.
- Treating local models as drop-in replacements for hosted models without rechecking tool use, structured outputs, and long-context behavior.
- Shipping a team workflow on consumer hardware with no capacity envelope, backup path, or restart procedure.
- Using "local" as the only justification for a stack choice when a small self-hosted or managed setup would be operationally safer.

## Escalation Boundaries

Use adjacent skills when:

- you need cluster-scale serving or throughput tuning -> [ai-llm-inference](../ai-llm-inference/SKILL.md)
- you need full fine-tuning strategy, dataset design, or evaluation -> [ai-llm](../ai-llm/SKILL.md)
- you need product UX, streaming chat, or structured output in an app -> [software-ai-integration](../software-ai-integration/SKILL.md)
- you need deployment, monitoring, or operational governance -> [ai-mlops](../ai-mlops/SKILL.md)

## When To Use This Skill

Use this skill when the user asks:

- "Should I use Ollama or something else locally?"
- "How do I run private models on my machine or a small server?"
- "What should I use for a self-hosted ChatGPT-like interface?"
- "How do I package a model into a low-friction local demo?"
- "When should I stay local vs move to a real serving stack?"
- "What's the best way to run models on Apple Silicon / Mac?"
- "Should I use MLX or Ollama on my M-series Mac?"
- "What small models can I run locally? Gemma / Phi / Qwen / DeepSeek / Mistral?"
- "How do I speed up local inference with speculative decoding or KV-cache quantization?"
- "What is LM Studio / Microsoft Foundry Local for?"
- "Should I run this locally or just call a hosted API?"

## Navigation

**References**
- [references/runtime-selection.md](references/runtime-selection.md) - runtime, UI, and packaging choice rules
- [references/desktop-runtime-landscape.md](references/desktop-runtime-landscape.md) - Ollama vs LM Studio vs Microsoft Foundry Local: detailed comparison, decision heuristic, anti-patterns
- [references/adaptation-and-packaging.md](references/adaptation-and-packaging.md) - lightweight adaptation, portable delivery, and evaluation handoff rules
- [references/model-sizing-matrix.md](references/model-sizing-matrix.md) - Llama 4, Mixtral, Qwen 3, GPT-OSS across M3/M4/4090/H100 hardware tiers; MLX and Ollama Apple Silicon paths; throughput estimates
- [references/quantization-format-table.md](references/quantization-format-table.md) - GGUF Q4_K_M/Q5_K_M/Q8_0, AWQ, GPTQ, FP8, EXL2; KV-cache quantization; speculative decoding; NPU/accelerator tier; decision tree
- [references/small-model-tier-table.md](references/small-model-tier-table.md) - Gemma, Phi, Qwen small-instruct capability tiers: footprint, strengths, selection heuristic (versions hedged — verify current release)
- [data/sources.json](data/sources.json) - local-model tooling sources from the curated repo list

**Templates**
- [assets/templates/ollama-setup-recipe.md](assets/templates/ollama-setup-recipe.md) - end-to-end Ollama install, model pull, OpenAI-compatible API usage, Modelfile pinning
- [assets/templates/openwebui-deployment-recipe.md](assets/templates/openwebui-deployment-recipe.md) - Docker / Compose deployment of Open WebUI over Ollama, env vars, reverse proxy, upgrades

**Related Skills**
- [../ai-llm-inference/SKILL.md](../ai-llm-inference/SKILL.md) - serving, quantization, routing, and throughput tuning
- [../ai-llm/SKILL.md](../ai-llm/SKILL.md) - full LLM lifecycle and fine-tuning strategy
- [../ai-mlops/SKILL.md](../ai-mlops/SKILL.md) - deployment, monitoring, and governance
- [../software-ai-integration/SKILL.md](../software-ai-integration/SKILL.md) - product integration and AI UX

## Fact-Checking

- Known bugs, regressions, framework/compiler/runtime footguns, and version-specific crash or workaround guidance must be verified against current primary web sources before being treated as current fact.
- Start from `data/sources.json` for local-model tooling references.
- Verify current model support, install steps, and hardware caveats before giving time-sensitive recommendations.
- If web access is unavailable, mark runtime-specific claims as unverified.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.
