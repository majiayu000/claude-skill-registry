---
name: ai-distributed-training
description: "Guides multi-GPU pre-training: DDP, FSDP2, ZeRO, tensor/pipeline/expert parallelism, fp8/Muon. Use when scaling a run, training MoE, or reproducing GPT-2 on rented GPUs."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# Distributed Training - Systems Performance Skill

**Operational focus**: picking and implementing the right parallelism strategy, not the theory. Covers data parallelism through FSDP/ZeRO/tensor+pipeline parallelism, memory-efficient attention, mixed precision at scale, activation checkpointing, rented-GPU cost discipline, and reproducing GPT-2 124M as the canonical sanity check.

Profile before you scale. Debug on the smallest GPU that fits. Stop the instance when done.

## ASCII Flow

```text
single GPU (debug/prototype)
  └─ DDP: replicate model, all-reduce gradients — linear scale up to ~8 GPUs
      └─ FSDP2 / ZeRO: shard optimizer state, gradients, params across GPUs
          └─ tensor parallelism: split weight matrices across GPUs (intra-node)
              └─ pipeline parallelism: split layers across nodes (inter-node)
                  └─ context parallelism: shard the sequence dim (long context)
                      └─ expert parallelism: route MoE experts across GPUs (all-to-all)
                          └─ N-D parallelism: DP + TP + PP + CP + EP (frontier MoE)

profile-before-scale
  └─ nsys / torch.profiler → find bottleneck (compute? memory? dataloader?)
      └─ fix bottleneck at small scale, then scale
```

## When to Use This Skill

Activate when the user asks about:

- Choosing between DDP, FSDP2, DeepSpeed ZeRO stages 1/2/3, or Megatron-LM
- Training Mixture-of-Experts (MoE) models: expert parallelism, all-to-all, load balancing
- OOM errors on multi-GPU training runs
- Memory-efficient attention (FlashAttention-2/3, xformers)
- Mixed precision (bf16, fp8, nvfp4) trade-offs at pre-training scale
- Optimizer choice at scale (AdamW vs Muon/MuonClip)
- Targeting current-gen hardware (H100, Blackwell B200/GB200 NVL72, early Rubin NVL72 access)
- Gradient checkpointing vs activation checkpointing cost
- Pre-training frameworks: litgpt, torchtitan, nanotron, levanter
- Reproducing GPT-2 (llm.c or modded-nanoGPT as the reference)
- Rented GPU cost management (RunPod, Lambda, Vast.ai, Modal)
- Spot / interruptible instance checkpoint strategies
- Profiling a training run before deciding to scale

## Scope Boundaries (Use These Skills for Depth)

- **Single-GPU pre-training build, data pipelines, tokenization** -> [ai-pretraining](../ai-pretraining/SKILL.md)
- **Token budget, compute-optimal scaling, Chinchilla** -> [ai-scaling-laws](../ai-scaling-laws/SKILL.md)
- **Serving optimization, batching, quantization, inference** -> [ai-llm-inference](../ai-llm-inference/SKILL.md)
- **General cloud/infra cost optimization** -> [ops-cost-optimization](../ops-cost-optimization/SKILL.md)
- **Production MLOps, model registry, monitoring, deployment** -> [ai-mlops](../ai-mlops/SKILL.md)

## Default Workflow

1. **Confirm scale and budget**: how many GPUs, which provider, on-demand or spot, target hours.
2. **Profile at small scale**: run `nsys` or `torch.profiler` on 1-2 GPUs before adding more.
3. **Pick parallelism strategy**: data parallel (DDP) -> FSDP/ZeRO -> tensor+pipeline only as needed.
4. **Enable memory optimizations**: FlashAttention, gradient checkpointing, bf16, activation offload.
5. **Wire checkpointing**: use Distributed Checkpoint (DCP) for sharded state, save async to object storage every N steps; test restore before long runs.
6. **Scale and re-profile**: verify near-linear throughput scaling; fix communication bottlenecks.
7. **Stop instance**: confirm instance termination; verify storage persistence; check billing.

## Quick Reference

| Decision | Default Move | Promote When | Avoid |
|----------|-------------|--------------|-------|
| Parallelism for ≤8 GPUs | DDP or FSDP2 (ZeRO-2 equiv) | Model does not fit in one GPU | Jumping to tensor parallel before model is too large |
| Parallelism for >8 GPUs | FSDP2 (ZeRO-3 equiv) or DeepSpeed ZeRO-3 | Multiple nodes needed | Mixing FSDP + DeepSpeed naively |
| FSDP version | FSDP2 (`fully_shard`, DTensor) | All new PyTorch projects | FSDP1 (`FullyShardedDataParallel`) — deprecated since PyTorch 2.11 |
| MoE routing at scale | Expert parallelism + all-to-all | Sparse MoE, experts exceed one GPU | TP on experts before EP (all-to-all is cheaper on NVLink) |
| Attention kernel | FlashAttention-2/3 | A100+ / H100 (FA3 = Hopper) | xformers as default (verify support for your GPU) |
| Mixed precision | bf16 | A100 / H100 (native bf16) | fp16 on A100+ (bf16 is safer; less loss spike risk) |
| Low-precision training | fp8 (H100 TransformerEngine/torchao) | Proven recipe + per-tile scaling | nvfp4/fp8 without loss-vs-bf16 validation |
| Optimizer | AdamW | Default, well-understood | — |
| Optimizer (frontier) | Muon / MuonClip | Matmul params, want ~1.3–1.5× token efficiency | Muon on embeddings/scalars (keep those on AdamW) |
| Gradient checkpointing | Always on for large models | Any model >1B params | Disabled when GPU memory is not a constraint |
| Optimizer state sharding | ZeRO-1 | Memory pressure from optimizer | ZeRO-3 when params fit on one GPU |
| Compile | `torch.compile` on the model | Want MFU; using torchtitan/FSDP2 | Leaving eager mode on long production runs |
| Framework for ≤7B pre-training | litgpt or torchtitan | Need Megatron-grade scale | Rolling your own training loop before reading existing frameworks |
| Dev / debug GPU | Smallest A10G or L4 that fits | Need bf16 native | H100/B200/Rubin for debugging (cost bloat) |
| Production training GPU | H100; B200/GB200 NVL72 for frontier; Rubin NVL72 where available | Need fp8/nvfp4 + NVLink-domain scale | Renting Blackwell/Rubin to debug a 124M model |
| Checkpoint storage | S3-compatible object store + DCP async | Spot instances (checkpoint every N steps) | Local disk only (lost on preemption) |

## Parallelism Deep Dive

### Data Parallelism (DDP)

Each worker holds a full model replica. Forward + backward runs independently per GPU. `AllReduce` synchronizes gradients. Scales well up to ~64 GPUs before communication becomes the bottleneck. Memory cost: full model + optimizer state on every GPU.

```python
# PyTorch DDP minimal setup
model = DistributedDataParallel(model, device_ids=[local_rank])
```

### FSDP2 (Fully Sharded Data Parallel)

PyTorch-native. Shards parameters, gradients, and optimizer state across all workers. **Use FSDP2 (`fully_shard`) for all new work** — the original `FullyShardedDataParallel` (FSDP1, FlatParameter-based) is deprecated as of PyTorch 2.11. FSDP2 shards each parameter individually as a DTensor (`Shard(dim=0)`), giving simpler/inspectable sharded state dicts, cleaner composition with TP/PP/CP via DeviceMesh, and tight `torch.compile` integration.

ZeRO-stage equivalents map onto `reshard_after_forward`:

- `reshard_after_forward=False` → keep params gathered after forward (ZeRO-2-like: shard grads + optimizer state, trade memory for fewer all-gathers)
- `reshard_after_forward=True` (default) → re-shard params after forward (ZeRO-3-like: shard params + grads + optimizer state)

```python
# FSDP2 (PyTorch >=2.11). Shard each transformer block, then the root.
from torch.distributed.fsdp import fully_shard, MixedPrecisionPolicy

mp = MixedPrecisionPolicy(param_dtype=torch.bfloat16, reduce_dtype=torch.float32)
for block in model.layers:
    fully_shard(block, mp_policy=mp)
fully_shard(model, mp_policy=mp)
```

FSDP1 (`FullyShardedDataParallel` + `ShardingStrategy.FULL_SHARD/SHARD_GRAD_OP/NO_SHARD`) still appears in older tutorials; migrate to FSDP2. Checkpoints are compatible across the two, but the construction API is not.

### DeepSpeed ZeRO Stages

| Stage | What is Sharded | Memory Reduction | Overhead |
|-------|-----------------|------------------|---------|
| ZeRO-1 | Optimizer state | ~4x vs baseline | Low |
| ZeRO-2 | Optimizer state + gradients | ~8x vs baseline | Low |
| ZeRO-3 | Optimizer state + gradients + params | ~64x vs baseline | Communication cost |

ZeRO-Infinity extends stage 3 to NVMe offload. Use only when GPU memory is genuinely exhausted — disk bandwidth becomes the bottleneck.

### Tensor Parallelism (Megatron-LM style)

Splits weight matrices across GPUs within a node (column/row parallel linear). Requires high-bandwidth NVLink. Megatron-LM implements Transformer-specific tensor parallel (TP) with sequence parallel (SP) for activation memory reduction. Best for models that cannot fit even with full sharding, or where communication budget allows.

### Pipeline Parallelism

Splits model layers across nodes (or GPU groups). Interleaved schedules (1F1B) reduce pipeline bubble overhead. Adds complexity: microbatch sizing, bubble fraction tuning. Typically combined with TP and DP in 3-D parallelism (Megatron-LM, nanotron).

**DualPipe** (DeepSeek-V3, 2024) is a bidirectional pipeline schedule that fully overlaps forward/backward compute with communication, driving the bubble toward zero — the reference design for large MoE training where cross-node all-to-all would otherwise dominate.

### Expert Parallelism (MoE)

Mixture-of-Experts models activate only a few experts per token, so total params (e.g. 1T) vastly exceed activated params (e.g. 32B). **Expert parallelism (EP)** places different experts on different GPUs; the router dispatches each token to its experts via **all-to-all** communication (dispatch), then a second all-to-all gathers results (combine). EP composes with DP/TP/PP/CP as an extra mesh dimension.

Key concerns specific to MoE training:

- **Load balancing**: an auxiliary load-balancing loss (or DeepSeek-V3's auxiliary-loss-free bias-update scheme) keeps tokens spread across experts; without it, a few experts saturate and the rest idle.
- **All-to-all is the bottleneck**, not all-reduce. It scales with cross-node bandwidth — keep EP inside the NVLink domain where possible, and overlap it with compute (DualPipe). DeepSeek-V3 trained a 671B MoE with **no tensor parallelism**, relying on EP + DualPipe + fp8 instead.
- **Token dropping vs capacity factor**: a capacity factor caps tokens per expert; overflow is dropped or rerouted. Tune to balance throughput against quality.
- **Frameworks**: Megatron-Core, DeepSpeed-MoE, and nanotron implement EP; `torch.distributed` provides the all-to-all primitives.

## Memory-Efficient Attention

**FlashAttention** (Dao et al., 2022/2024): reorders attention computation to avoid materializing the full N×N attention matrix. Result: O(N) memory vs O(N²), significant speedup on A100/H100.

```python
# PyTorch ≥2.3: select the Flash backend via the current API
from torch.nn.attention import sdpa_kernel, SDPBackend
with sdpa_kernel(SDPBackend.FLASH_ATTENTION):
    out = F.scaled_dot_product_attention(q, k, v)
# (torch.backends.cuda.sdp_kernel(...) is the deprecated pre-2.3 form)
```

FlashAttention-3 (2024) targets H100 with further hardware-specific optimizations. xformers provides `memory_efficient_attention` as an alternative with broader GPU support.

## Mixed Precision at Scale

`bf16` (bfloat16) is the safe default for A100+ and H100. Same exponent range as fp32 (avoids the overflow spikes common in fp16), 16-bit mantissa precision. `torch.cuda.amp.autocast(dtype=torch.bfloat16)` or pass `torch_dtype=torch.bfloat16`. Gradient scaler (`torch.cuda.amp.GradScaler`) is needed for fp16 but not for bf16.

**fp8** is now production-proven on Hopper (H100), not just emerging. DeepSeek-V3 trained at fp8 with fine-grained scaling — per-token 1×128 / per-block 128×128 tiles plus high-precision CUDA-core accumulation — keeping the loss within ~0.25% of bf16. Use **TransformerEngine** or **torchao float8** for the linear layers; keep a bf16/fp32 master copy of weights and the optimizer state. Validate loss-vs-bf16 on your workload before committing a long run.

**nvfp4 / fp4** arrives with Blackwell. The B200/GB200 add hardware FP4 (including NVIDIA's NVFP4, 16-element micro-scaled blocks with e4m3 scales, vs MXFP4's 32-element UE8M0 blocks). It has moved past pure research: NVIDIA pre-trained a **12B model on 10T tokens with NVFP4 matching the fp8 baseline** (arXiv 2509.25149), and MXFP4 needed ~36% more tokens to reach the same loss — so NVFP4 is the stronger FP4 format. Still validate against bf16/fp8 on your own workload before a long run; the recipe (which tensors stay higher-precision, scaling, outlier handling) is less battle-tested than fp8.

### Hardware Tiers (mid-2026)

- **A10G / L4** — cheap debug and architecture validation. Native bf16 on L4.
- **A100 80GB** — bf16 workhorse; still common and cost-effective on spot.
- **H100** — bf16 + fp8 (TransformerEngine), FlashAttention-3, NVLink/NVSwitch domains. Now the mainstream production tier, not the frontier.
- **Blackwell B200 / GB200 NVL72** — mainstream frontier: fp4/nvfp4 hardware, ~2–3× faster training than H100, and a 72-GPU NVLink domain (NVL72) that lets EP/TP span a whole rack at NVLink bandwidth. Widely available on major clouds by mid-2026.
- **Rubin / Vera Rubin NVL72** — newest generation: entered production ~June 2026, with cloud/neocloud availability (AWS, GCP, Azure, CoreWeave, Lambda, Nebius) rolling out through H2 2026. Treat as capacity-constrained and premium-priced for now; verify current availability and quoted pricing before planning around it. Reserve any Blackwell/Rubin tier for frontier-scale runs, not 124M debugging.

### torch.compile

`torch.compile(model)` (TorchInductor) fuses kernels and is essential for competitive MFU on modern hardware. It composes with FSDP2 and is on by default in torchtitan. Compile once outside the training loop; expect a warm-up cost on the first steps. Pair with bf16/fp8 — most of the published MFU numbers assume compile is on.

## Activation / Gradient Checkpointing

`torch.utils.checkpoint.checkpoint(function, *args)` recomputes activations during the backward pass instead of storing them. Reduces activation memory by ~sqrt(layers), adds ~33% compute overhead. Use on every transformer block for large models.

Selective checkpointing (checkpointing only the memory-expensive ops like attention) is supported in FSDP via `checkpoint_wrapper`.

## Optimizers at Scale

**AdamW** remains the default and the best-understood choice. Its memory cost (two fp32 moments ≈ 2× params) is what ZeRO/FSDP optimizer-state sharding targets.

**Muon / MuonClip** is the notable frontier shift since 2024. Muon (Keller Jordan, originating in modded-nanoGPT speedruns) applies Newton–Schulz orthogonalization to 2-D matmul weight matrices, treating each weight as a matrix rather than a flat vector. It delivers roughly 1.3–1.5× token efficiency over AdamW on pre-training and holds the modded-nanoGPT GPT-2 speed records. *"Muon is Scalable for LLM Training"* (arXiv 2502.16982) supplied the two fixes — weight decay and per-parameter update-scale adjustment — that make it work at scale without bespoke tuning. By 2026 it trains trillion-param MoE in production: **MuonClip** (a stability-clamped variant) pre-trained Moonshot's **Kimi K2** (1T-param MoE, 15.5T tokens; arXiv 2507.20534), and Muon now also underpins **DeepSeek-V4** (arXiv 2606.19348 names Muon explicitly for faster convergence and stability) and **GLM-4.5/GLM-5** (Zhipu/Z.ai; GLM-5's paper, arXiv 2602.15763, adds a "Muon Split" per-head orthogonalization plus a zero-redundancy distributed Muon implementation), plus Karpathy's nanochat. It is a serious AdamW replacement at frontier scale, not a speedrun curiosity. Re-verify against the primary report before quoting exact figures — these are recent releases and details can be revised.

Practical notes:

- Apply Muon only to 2-D matmul parameters; keep embeddings, the LM head, biases, and norm/scalar params on AdamW (a hybrid optimizer).
- Muon's per-step orthogonalization adds compute but less optimizer memory than Adam's two moments — a useful trade under memory pressure.
- For distributed use, see the DeepSpeed Muon integration; sharding Muon's update across DP ranks needs care.

## Pre-Training Frameworks

| Framework | Best For | Notes |
|-----------|----------|-------|
| litgpt | Research, ≤70B, HF-compatible | Clean PyTorch; easy to read |
| torchtitan | PyTorch-native large-scale | Meta's reference; FSDP2 + CP |
| nanotron | Efficient 3-D parallel | HuggingFace; powers BLOOM/IDEFICS training |
| levanter | TPU / JAX | Google; Chinchilla-optimal recipes |
| Megatron-LM | >70B, tensor+pipeline+data | NVIDIA; most complex, most scalable |
| modded-nanoGPT | Learning / GPT-2 reproduction | Keller Jordan; speed records; Muon optimizer |
| llm.c | Minimal C/CUDA GPT-2 | Karpathy; educational; fastest GPT-2 |
| nanochat | End-to-end small-model train+chat | Karpathy; uses Muon; modern reference loop |
| Megatron-Core / NeMo | Modular TP+PP+DP+EP building blocks | NVIDIA; library form of Megatron-LM for MoE + fp8 |

## Reproducing GPT-2 124M (Reference Run)

Target: ~3.28 loss on FineWeb/Hellaswag after ~10B tokens.

Using `llm.c` or `modded-nanoGPT`:
1. Download FineWeb-edu 10B token sample.
2. Set batch size to fill GPU memory (gradient accumulation for logical large batch).
3. Enable FlashAttention, bf16, gradient checkpointing.
4. Run for ~10B tokens; monitor loss curve and MFU (model FLOP utilization).
5. Cost estimate: ~$50-150 on 4×A100 80 GB on RunPod spot (8-12 hours).

Full GPT-2 124M with full convergence checks: **~$100-300** depending on GPU type and provider.

## Checkpointing at Scale (DCP)

For sharded training (FSDP2, TP, PP), a single-rank `state_dict` is the wrong pattern — it forces an all-gather of the full model onto one rank and serializes saving. Use **`torch.distributed.checkpoint` (DCP)**:

- Each rank saves its own shard in parallel; DCP handles resharding on load (save on 8 GPUs, resume on 16).
- **`dcp.async_save`** offloads the write so training continues while the checkpoint flushes to storage — critical on spot instances where every minute of stall is wasted cost.
- Save model + optimizer + dataloader/RNG state together so a resume is bit-for-bit resumable, not just architecturally loadable.

```python
import torch.distributed.checkpoint as dcp
state = {"model": model, "optim": optimizer}        # FSDP2 DTensors handled natively
dcp.async_save(state, checkpoint_id=f"s3://bucket/run/step-{step}")
```

## Cost Estimation

```
cost ≈ $/GPU-hr × num_GPUs × training_hours
```

Example: 4×A100 80GB at $2.50/GPU-hr × 10 hours = **$100**

| Run Type | GPUs | Hours | Est. Cost |
|----------|------|-------|-----------|
| GPT-2 124M debug (single GPU) | 1×A10G | 2-4 h | $1-3 |
| GPT-2 124M full run | 4×A100 | 8-12 h | $80-150 |
| GPT-2 124M fast (H100 cluster) | 8×H100 | 1-2 h | $80-160 |
| 7B model pre-training (100B tok) | 8×A100 | ~100 h | ~$2000 |
| Frontier MoE / large dense (fp8/fp4) | GB200 or Rubin NVL72 | varies | rack-scale; reserve/quote pricing |

Always check current spot pricing on RunPod, Lambda Labs, Vast.ai, or Modal before budgeting. Spot/interruptible discounts are typically 30-70% off on-demand.

## Rented GPU Cost Discipline

- **Debug on the smallest GPU that fits** (A10G at ~$0.60/hr vs H100 at ~$4/hr).
- **Spot / interruptible instances**: 30-70% cheaper; checkpoint every N steps (not just every epoch).
- **Checkpoint to object storage immediately** (S3-compatible): rclone, aws-cli, or provider's SDK.
- **Per-second billing**: terminate as soon as training ends; do not leave instances idle.
- **Validate checkpoint restore** before starting a long run on spot.
- **Estimate before running**: use the formula above; add 20% buffer for profiling/debugging.

## Known Traps

- **Debugging on an 8xH100 box**: expensive and unnecessary; always debug on the smallest GPU first.
- **OOM blamed on GPUs when the real cause is the dataloader or precision bug**: profile first with `torch.profiler`; check `torch.cuda.memory_summary()`.
- **Forgetting to stop the instance**: set a billing alert and calendar reminder; auto-shutdown scripts on training completion.
- **Not checkpointing on spot instances**: a preemption without a recent checkpoint loses hours of training.
- **Using fp16 instead of bf16 on A100+**: fp16 is more prone to loss spikes at pre-training scale; bf16 is safer and equally fast on A100/H100.
- **Mixing FSDP + DeepSpeed**: incompatible; pick one sharding framework per run.
- **Skipping profiling and tuning MFU**: low MFU (below 30%) means the run is communication or dataloader bound, not compute bound. Fix before scaling.
- **Using FSDP1 in a new project**: deprecated since PyTorch 2.11; start on FSDP2 (`fully_shard`) or inherit unmaintained APIs.
- **Saving a full `state_dict` from sharded training**: all-gathers the whole model onto one rank and stalls every other GPU. Use DCP (`dcp.async_save`) instead.
- **Loss spikes at scale, then NaN**: not always the optimizer. Common causes are fp16 instead of bf16, missing/late LR warmup, no gradient clipping, or unstable attention logits — mitigate with bf16, grad-clip, QK-norm, and (for MoE) z-loss. Save a checkpoint immediately before resuming from a spike.
- **MoE without a load-balancing loss**: a few experts saturate while the rest idle, tanking effective throughput and quality. Use an aux load-balancing loss or DeepSeek-V3's bias-update scheme.
- **fp8/nvfp4 without a bf16 baseline**: low-precision training can silently degrade loss. Always validate against bf16 on your own workload before a long run.

## Common Anti-Patterns

- Adding more GPUs before understanding the current bottleneck.
- Using ZeRO-3 or tensor parallelism before the model is too large for simpler strategies.
- Training without a checkpoint on spot instances.
- Leaving an idle GPU instance running while reviewing results.
- Treating a DeepSpeed config from a blog post as production-ready without profiling on your workload.
- Using full fp32 training at scale (memory waste; use bf16 + loss scaling instead).

## Core Principles

1. **Profile before you scale**: identify the bottleneck (compute, memory, communication, or dataloader) at small scale before spending on more GPUs.
2. **Smallest GPU that fits for dev**: use A10G or L4 for debugging and architecture validation; reserve H100 for production runs.
3. **Understand one parallelism strategy fully before combining**: DDP → FSDP → 3-D parallel; do not combine before each layer is mastered.
4. **Checkpoint often on interruptible**: save to durable object storage every N steps; test restore before long runs.
5. **Stop the instance**: training end ≠ task end; terminate, verify persistence, confirm billing stopped.

## Navigation: Core References

- **[FSDP vs ZeRO Comparison](references/fsdp-vs-zero.md)** - side-by-side tradeoffs, when to pick each, config examples
- **[Parallelism Strategies](references/parallelism-strategies.md)** - DDP, tensor, pipeline, 3-D parallel decision guide
- **[Rented GPU Cost Guide](references/rented-gpu-cost.md)** - provider comparison, spot strategies, cost estimation

## External Sources

See **[data/sources.json](data/sources.json)** for curated primary sources across:

- FlashAttention 1/2/3 papers and implementation
- DeepSpeed ZeRO documentation and ZeRO paper
- PyTorch FSDP2 tutorial and torchtitan paper
- Megatron-LM (tensor parallel) and activation-recomputation papers
- DeepSeek-V3 (DualPipe / expert parallelism / fp8) and Ring Attention (context parallel)
- Muon / Kimi K2, DeepSeek-V4, and GLM-5 optimizer reports
- Karpathy's GPT-2 reproduction projects (llm.c, modded-nanoGPT)
- Rented GPU provider pricing and docs

## Fact-Checking

- GPU pricing, spot availability, and provider features change frequently. Always verify against current provider pricing pages before budgeting.
- FlashAttention version support varies by GPU architecture. Check the official repo for your target hardware.
- DeepSpeed ZeRO-Infinity NVMe offload performance depends heavily on NVMe bandwidth; benchmark before relying on it.
- Framework releases (torchtitan, nanotron, litgpt) move fast; verify current API against the repo's main branch.
- Known bugs, regressions, and framework footguns must be verified against current primary sources before being treated as fact.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.
