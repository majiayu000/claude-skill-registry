---
name: ai-pretraining
description: "Builds a transformer/GPT and BPE tokenizer from scratch. Use when implementing autograd, self-attention, a nanoGPT-style pretraining loop, or a byte-level tokenizer."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.3"
last_validated: 2026-07-11
---

# Pretraining From Scratch

**Domain**: building a transformer/GPT and a BPE tokenizer from first principles — the from-first-principles training-layer competency. Does NOT cover applications-layer fine-tuning, RLHF, or inference optimization; those belong to sibling skills.

Canonical teachers: Karpathy "Neural Networks: Zero to Hero" (micrograd → makemore → "Let's build GPT" → "Let's build the GPT Tokenizer" → "Let's reproduce GPT-2"), Karpathy nanochat (full-stack from-scratch successor to nanoGPT, 2025), Raschka "Build a Large Language Model From Scratch", nanoGPT, minbpe, "Attention Is All You Need".

GPT-2 is the pedagogical spine here — the right thing to build *first*. The 2026 from-scratch baseline then swaps four components onto that spine (RoPE, RMSNorm, SwiGLU, GQA) and runs attention through FlashAttention/SDPA; see [Modern Architecture Deltas](references/modern-architecture-deltas.md).

## ASCII Flow

```text
Raw text corpus
  |
  v
BPE Tokenizer (byte-level merges, vocab, encode/decode)
  |
  v
Token IDs -> Embedding table (vocab_size x n_embd)
  |
  v
+ Positional Embedding (learned, shape: block_size x n_embd)
  |
  v
Transformer Block x N
  ├── LayerNorm (pre-norm placement in GPT-2 style)
  ├── Multi-Head Self-Attention (causal mask, k/q/v projections)
  ├── Residual connection
  ├── LayerNorm
  ├── FFN (Linear -> GELU -> Linear, 4x expansion)
  └── Residual connection
  |
  v
Final LayerNorm
  |
  v
LM Head (Linear, n_embd -> vocab_size, weight-tied to embedding)
  |
  v
Cross-entropy loss -> Pretraining loop
  (bf16/autocast, grad accumulation, cosine LR + warmup, checkpoint)
```

## When to Use This Skill

Activate when the user asks about:

- Implementing autograd / backprop from scratch (micrograd-style)
- Building makemore (bigram, MLP, WaveNet-style character LMs)
- Implementing self-attention, multi-head attention, causal masking
- Building the transformer block (pre-norm vs post-norm, residual, FFN)
- Stacking blocks into a GPT with an LM head and weight tying
- Writing the pretraining loop: cross-entropy, bf16 mixed precision, gradient accumulation, gradient checkpointing, cosine LR schedule with warmup, model checkpointing
- Building a BPE tokenizer from scratch: byte-level, merge algorithm, vocab construction, encode/decode (minbpe-style)
- Reproducing GPT-2 (124M) from scratch end-to-end (nanoGPT path)
- Implementing temperature scaling and top-k sampling for text generation

## Scope Boundaries (Use These Skills for Depth)

- **LLM lifecycle, fine-tuning, provider selection, deployment** -> [ai-llm](../ai-llm/SKILL.md)
- **Multi-GPU training: DDP, FSDP, tensor/pipeline parallelism** -> [ai-distributed-training](../ai-distributed-training/SKILL.md)
- **Token/param budget, Chinchilla scaling, compute-optimal runs** -> [ai-scaling-laws](../ai-scaling-laws/SKILL.md)
- **Dataset curation, deduplication, quality filtering for pretraining** -> [ai-data-curation-pretraining](../ai-data-curation-pretraining/SKILL.md)
- **Evaluation harnesses, benchmark design, evals post-pretraining** -> [ai-evals](../ai-evals/SKILL.md)
- **Mixture-of-Experts (MoE)**: swaps the dense FFN for a router + expert FFNs (DeepSeek-V2/V3, Mixtral). A frontier architectural variant, not a from-scratch fundamental. For training: [ai-distributed-training](../ai-distributed-training/SKILL.md); for serving/inference: [ai-llm-inference](../ai-llm-inference/SKILL.md).
- **Classification fine-tuning, instruction/SFT fine-tuning, LoRA/PEFT**: post-pretraining applications. Raschka's book covers these; this skill stops at pretraining. -> [ai-llm](../ai-llm/SKILL.md)

## Default Workflow

1. **Autograd first**: implement Value class with backward(), build MLP, verify gradients against PyTorch.
2. **Character LM ladder**: bigram table -> MLP (makemore) -> verify loss convergence and sampling.
3. **Attention module**: single-head self-attention with causal mask; verify attention weights sum to 1 per row.
4. **Multi-head attention**: split heads, concatenate, project; match PyTorch `nn.MultiheadAttention` output exactly.
5. **Transformer block**: add FFN (4x, GELU), pre-LayerNorm, residuals; match nanoGPT block.
6. **GPT assembly**: stack N blocks, add LM head, tie weights with embedding; verify forward pass shape.
7. **Pretraining loop**: DataLoader, cross-entropy, `torch.autocast(bf16)`, gradient accumulation, cosine LR, checkpoint.
8. **BPE tokenizer**: byte-level text encoding, count bigram frequencies, greedy merge loop, build vocab, encode/decode round-trip.
9. **GPT-2 reproduction**: load OpenAI weights via HuggingFace, verify logits match, then train from scratch on FineWeb-Edu.
9a. **Sampling**: implement temperature scaling and top-k sampling for generation; optionally add a KV-cache for inference speed (see Quick Reference).
10. **Modernize**: swap to the 2026 baseline — RoPE for `wpe`, RMSNorm for LayerNorm, SwiGLU for the GELU-MLP, GQA, and `F.scaled_dot_product_attention`; optionally train with Muon. See [Modern Architecture Deltas](references/modern-architecture-deltas.md).

## Modern Baseline (2026)

Build GPT-2 first to understand the mechanics, then apply the deltas — the pre-norm residual skeleton is unchanged; you swap sublayers, not the architecture.

| GPT-2 (2019) | 2026 baseline | Why |
|--------------|---------------|-----|
| Learned absolute pos embed (`wpe`) | RoPE (rotary, in attention) | Relative position; better length extrapolation; no `block_size` ceiling |
| LayerNorm | RMSNorm | Cheaper, no centering/bias, stable at depth |
| GELU-MLP (4×) | SwiGLU (`~8/3×`) | Gated FFN improves quality per param |
| MHA (KV heads = query heads) | GQA (fewer KV heads) | Shrinks KV cache for inference |
| Hand-rolled softmax attention | `F.scaled_dot_product_attention` | FlashAttention kernel — `O(T)` memory, much faster |
| AdamW for all params | Muon (2D matrices) + AdamW (embed/head/norms) | Newton-Schulz orthogonalized updates; large per-step speedup |

Frontier reference: the `modded-nanoGPT` speedrun stacks Muon, QK-Norm, ReLU², logit softcap, and embedding-skip connections to drive GPT-2-grade FineWeb val loss to ~3.28 far below the original wall-clock on 8×H100 (record still ~3.28-target as of mid-2026, per the repo README). The record is a moving target — verify the current repo README, don't quote a fixed time. For the full from-scratch *pipeline* (tokenizer → pretrain → SFT → RL → serve), Karpathy's nanochat is the 2025 successor to nanoGPT; its headline benchmark shifted in 2026 to "time to GPT-2" (wall-clock to beat GPT-2 1.6B on DCLM CORE, 8×H100) — check the repo, not this doc, for the current number.

## Quick Reference

| Component | Key Detail | Common Mistake |
|-----------|-----------|----------------|
| Autograd | `Value.backward()` accumulates `+=` into `.grad`, not `=` | Forgetting to zero grads before `.backward()` |
| Embedding | `nn.Embedding(vocab_size, n_embd)` — random init, learned | Confusing token embed with positional embed shape |
| Causal mask | `torch.tril(torch.ones(T,T))` before softmax; fill `-inf` not 0 | Using `0` fill — attention leaks future tokens |
| Attention math | `softmax(QK^T / sqrt(d_k)) * V` | Forgetting `/sqrt(d_k)` — variance explodes |
| LayerNorm placement | Pre-norm (before attention/FFN) in GPT-2; original paper was post-norm | Post-norm makes deep stacks hard to train |
| FFN expansion | 4x hidden dim, GELU activation | Using ReLU — slight quality difference, matters at scale |
| Weight tying | LM head matrix = transpose of embedding matrix | Forgetting tying doubles params and degrades loss |
| Init scaling | `std=0.02` for most; residual projections: `std=0.02/sqrt(2*n_layer)` | Flat 0.02 everywhere — residual stream variance grows |
| Gradient accumulation | accumulate N micro-batches, divide loss by N, step once | Forgetting to divide loss — effective LR N× too large |
| bf16 autocast | `torch.autocast('cuda', dtype=torch.bfloat16)` | Using fp16 without loss scaling — NaN on older GPUs |
| BPE merges | greedy highest-frequency pair; merge in-place, repeat | Not updating pair counts after each merge — wrong vocab |
| Cosine LR | warmup linearly for ~1% of steps, then cosine decay to ~10% of peak | Skipping warmup — loss spike at start |
| Temperature | `logits / temperature` before softmax; `T<1` sharpens (more deterministic), `T>1` flattens (more random) | Applying temperature after softmax — has no effect on the distribution |
| Top-k sampling | zero out all logits except the top-k before softmax; draw from the remaining distribution | Top-k=1 is greedy decoding; top-k=vocab_size is pure sampling |
| KV-cache | at inference, cache K and V tensors for all past positions; on each new token only compute Q/K/V for the single new position and append to cache | Re-computing all K/V at each generation step — O(T²) cost; cache turns it O(T) |

## Known Traps

- **Zero-grad placement**: call `optimizer.zero_grad()` before the forward pass (or `set_to_none=True` for speed), not after `.step()`.
- **Post-norm vs pre-norm**: original "Attention Is All You Need" uses post-norm; GPT-2 and nanoGPT use pre-norm. Pre-norm trains more stably at depth.
- **Causal mask fill value**: use `-float('inf')` or `float('-inf')`, not a large negative constant like `-1e9` — softmax on `-inf` gives exact 0, large negatives can give small nonzero values.
- **Gradient accumulation scaling**: divide the loss by the accumulation steps inside the micro-batch loop, not outside.
- **Weight tying in state_dict**: when saving checkpoints, the LM head weight is the same tensor as the embedding weight — loading requires care to avoid double-counting params.
- **BPE encode-decode round-trip**: bytes, not characters — always encode text as UTF-8 bytes first before running BPE.
- **DataLoader seeding**: fix random seeds for reproducibility across runs; DataLoader worker seeds need explicit `worker_init_fn`.
- **`torch.compile` interaction**: `torch.compile` + gradient checkpointing can conflict in some PyTorch versions — test before enabling both.

## Common Anti-Patterns

- Implementing attention without verifying `attn_weights.sum(dim=-1)` is all-ones (no causal leak check).
- Skipping the PyTorch parity check: always compare custom layer output to `torch.nn.` equivalent before stacking.
- Starting with the full GPT before the single-head attention works — build bottom-up.
- Training without a baseline loss: for character-level with vocab V, random model should give `ln(V)` loss; check this at step 0.
- Using Adam with default `betas=(0.9, 0.999)` — GPT-2 paper used `betas=(0.9, 0.95)` for stability at scale.
- Tokenizing the entire dataset in memory — stream and chunk for large corpora.
- Shipping the GPT-2 architecture as the *final* product — it is the teaching spine, not the 2026 baseline. Apply the [modern deltas](references/modern-architecture-deltas.md) (RoPE/RMSNorm/SwiGLU/GQA/SDPA) once the GPT-2 build verifies.

## Core Principles

1. **Build then read**: implement first, then verify against PyTorch source or the paper. Reading first encourages copy-paste, not understanding.
2. **No black boxes**: every component must be verified with a unit check before it's stacked.
3. **One component at a time**: single-head attention -> multi-head -> block -> GPT. Never jump layers.
4. **PyTorch parity check**: custom attention output must match `nn.MultiheadAttention` on identical inputs before moving on.
5. **Fail loud on training metrics**: if step-0 loss deviates from `ln(vocab_size)` by >10%, stop and debug — don't train through bad initialization.

## Navigation: Core References

- **[Transformer From Scratch](references/transformer-from-scratch.md)** — attention math, block assembly, weight init, GPT architecture notes
- **[BPE Tokenizer](references/bpe-tokenizer.md)** — byte-level BPE algorithm, merge loop, vocab construction, encode/decode
- **[Pretraining Loop](references/pretraining-loop.md)** — training loop anatomy, mixed precision, gradient accumulation, cosine LR, checkpointing
- **[Modern Architecture Deltas](references/modern-architecture-deltas.md)** — GPT-2 → 2026 baseline: RoPE, RMSNorm, SwiGLU, GQA, FlashAttention/SDPA, Muon and the speedrun frontier
- **[Architecture Limitations and Workarounds](references/architecture-limitations-and-workarounds.md)** — failure-mode companion: each component's limitation → workaround → tradeoff (softmax pathologies/attention sinks, MHA→MQA→GQA→MLA + decoupled RoPE, positional design space + YaRN/NTK, MoE routing pitfalls, norm/residual/depth stability, fp8/fp4 precision, long-context, encoder/decoder/encoder-decoder contrast)

## Fact-Checking

- Verify PyTorch API details (autocast dtype names, `torch.compile` flags, DataLoader args) against current PyTorch docs before recommending.
- Verify current nanoGPT and minbpe repo states (file structure, hyperparameters) against the GitHub repos — they are actively maintained.
- If you cannot verify, say so explicitly and present the guidance as a dated assumption.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.
