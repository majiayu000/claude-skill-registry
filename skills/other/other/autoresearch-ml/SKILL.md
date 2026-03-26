---
name: autoresearch-ml
description: >-
  Specialized ML/LLM training skill extending the core autoresearch loop with
  GPU-specific workflows, data preparation, and a ready-to-use training template.
  Use this skill when the user asks to "train a model autonomously",
  "optimize LLM training", "run ML experiments", "autoresearch with GPU",
  "optimize val_bpb", "autonomous ML training", "LLM pretraining loop",
  "setup ML autoresearch", "GPU training experiments", "fine-tune a model",
  "pretrain from scratch", "speed up training", "lower my loss",
  "GPU optimization", "CUDA training", or mentions "train.py", "prepare.py",
  "bits per byte", "val_bpb", "NVIDIA GPU training", "RTX training",
  "H100 training", "autonomous model training", "consumer GPU training",
  "low VRAM training". Always use this skill when the user wants to autonomously
  optimize any ML training metric — even if they don't explicitly mention autoresearch.
version: 0.2.0
---

# Autoresearch ML: Autonomous LLM Training Optimization

Extends the core `autoresearch` skill with specialized ML/LLM training workflows.
Provides a ready-to-use training template based on [Karpathy's autoresearch](https://github.com/karpathy/autoresearch)
for single-GPU LLM pretraining experiments.

**Prerequisites:** This skill builds on the core `autoresearch` skill. The experiment loop,
metric parsing, logging, and keep/discard logic are all handled by the core skill.
This skill adds ML-specific setup, GPU guidance, and the training template.

## Quick Start with Template

To set up ML autoresearch from the bundled template:

1. Copy asset files to the project directory:
   ```bash
   cp ${CLAUDE_SKILL_DIR}/assets/prepare.py .
   cp ${CLAUDE_SKILL_DIR}/assets/train.py .
   cp ${CLAUDE_SKILL_DIR}/assets/pyproject.toml .
   cp ${CLAUDE_SKILL_DIR}/assets/program.md .
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Prepare data (downloads shards, trains tokenizer — ~2 min):
   ```bash
   uv run prepare.py
   ```

4. Run baseline training (~5 min):
   ```bash
   uv run train.py
   ```

5. Follow the core `autoresearch` skill to set up the experiment loop with:
   - **Command:** `uv run train.py`
   - **Primary metric:** `val_bpb` (bits per byte, lower is better)
   - **Files in scope:** `train.py` only (prepare.py is fixed)

## Template Architecture

### prepare.py (FIXED — never modify)

Handles all data infrastructure:

- **Data download:** Fetches parquet shards from HuggingFace (climbmix-400b-shuffle)
- **Tokenizer training:** Trains BPE tokenizer (8192 vocab) using rustbpe/tiktoken
- **Dataloader:** Best-fit document packing with 100% token utilization, BOS-aligned
- **Evaluation:** `evaluate_bpb()` computes bits-per-byte (vocab-size-independent metric)

Key constants:
- `MAX_SEQ_LEN = 2048` — context length
- `TIME_BUDGET = 300` — 5-minute training window (wall clock)
- `EVAL_TOKENS = 40 * 524288` — validation tokens (~21M)
- `VOCAB_SIZE = 8192` — BPE vocabulary size

### train.py (MODIFIED BY AGENT — the only editable file)

Contains the full model and training loop:

- **Model:** GPT with RoPE, sliding window attention, value embeddings, Flash Attention 3
- **Optimizer:** Hybrid MuonAdamW (Muon for matrices, AdamW for everything else)
- **Training:** Gradient accumulation, LR schedules (warmup/flat/warmdown), fixed time budget
- **Output:** Prints `val_bpb` and other metrics after training completes

Editable hyperparameters include: `ASPECT_RATIO`, `DEPTH`, `WINDOW_PATTERN`,
`TOTAL_BATCH_SIZE`, learning rates, LR schedule phases, and the full model architecture.

### program.md (Agent instructions)

Self-contained instructions for the autonomous loop. Can be used directly with any
Claude-compatible agent. Follows the same edit → commit → run → measure → keep/discard pattern.

**Key rule from program.md:** Once the loop starts, NEVER STOP. Never ask "should I continue?" The user expects autonomous operation — they may be asleep for 8+ hours while you run ~100 experiments.

## GPU Requirements

### Supported GPU Tiers

| Tier | GPUs | VRAM | Notes |
|------|------|------|-------|
| **Consumer** | GTX 1080 Ti, RTX 2080 Ti | 11GB | fp32 fallback, gradient checkpointing required |
| **Consumer+** | RTX 3090, RTX 4090 | 24GB | Great for experiments |
| **Enthusiast** | RTX 5090 | 32GB | Excellent — larger models possible |
| **Datacenter** | A100, H100 | 40-80GB | Original development target |

### Minimum Requirements

- **NVIDIA GPU** with CUDA support (compute capability ≥ 6.1 for consumer, ≥ 7.0 for bf16)
- **VRAM:** 8GB minimum (16GB+ recommended, 24GB+ for larger experiments)
- **CUDA:** 12.0+ (template targets CUDA 12.8)
- **Driver:** 535+ (check with `nvidia-smi`)

### Consumer GPU Adaptations

For GPUs with limited VRAM (< 16GB), the agent should:

1. **Enable gradient checkpointing** — always use `torch.utils.checkpoint.checkpoint()` with `use_reentrant=False`
2. **Use built-in attention** — replace Flash Attention 3 with `torch.nn.functional.scaled_dot_product_attention` (no external dependency)
3. **Auto-scale model size** — reduce `DEPTH` and `DEVICE_BATCH_SIZE` to fit VRAM budget
4. **Cap evaluation steps** — scale eval batch count by available VRAM (30-100 steps)
5. **fp32 fallback** — use fp32 instead of bf16 for Pascal GPUs (compute capability < 7.5)

### VRAM Auto-Scaling Guide

Use this table to estimate starting configs for different VRAM budgets:

| VRAM Budget | DEPTH | n_embd | Batch Size | Seq Length | ~Params |
|-------------|-------|--------|------------|------------|---------|
| 4GB | 2 | 128 | 4 | 512 | ~1M |
| 8GB | 4 | 256 | 8 | 1024 | ~5M |
| 12GB | 6 | 384 | 16 | 1024 | ~14M |
| 16GB | 8 | 512 | 32 | 2048 | ~25M |
| 24GB | 8 | 512 | 128 | 2048 | ~50M |
| 32GB | 12 | 768 | 128 | 2048 | ~85M |
| 80GB | 16 | 1024 | 128 | 2048 | ~200M |

**Note:** `n_embd` must be a multiple of `HEAD_DIM` (default 128). The formula is `n_embd = round_up(DEPTH * ASPECT_RATIO, HEAD_DIM)`.

**Rule of thumb:** VRAM usage ≈ model parameters × 12 bytes (params + grads + optimizer states)

**Config search strategy:** Start with the largest depth that fits, then try reducing `DEVICE_BATCH_SIZE` (128 → 64 → 32 → 16 → 8 → 4 → 2 → 1) and `MAX_SEQ_LEN` (2048 → 1024 → 768 → 512) if OOM.

### GPU Verification

Before starting, verify GPU setup:

```bash
nvidia-smi                          # Check driver and GPU
python -c "import torch; print(torch.cuda.is_available())"  # Check PyTorch CUDA
python -c "import torch; print(torch.cuda.get_device_name())"  # Check device name
python -c "import torch; print(f'VRAM: {torch.cuda.get_device_properties(0).total_mem / 1e9:.1f} GB')"
python -c "import torch; print(f'Compute: {torch.cuda.get_device_capability()}')"
```

### Performance Tuning

**Environment variables for optimal performance:**
```bash
export CUDA_DEVICE_ORDER=PCI_BUS_ID
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export CUBLAS_WORKSPACE_CONFIG=:4096:8  # For deterministic results
```

**torch.compile():** Enable graph optimization on compute capability ≥ 7. Falls back gracefully on older GPUs.

**GC management:** Disable Python garbage collector after first training step to avoid GC stalls within the 5-minute budget.

## ML-Specific Experiment Strategies

### What to Try

1. **Architecture changes:** Layer count, attention patterns, embedding dimensions, activation functions
2. **Optimizer tuning:** Learning rates (per-parameter), schedule phases, momentum, weight decay
3. **Attention patterns:** Window sizes, sliding window configurations, full vs. local attention
4. **Normalization:** RMS norm parameters, placement (pre-norm vs post-norm)
5. **Regularization:** Dropout, weight decay schedules, gradient clipping
6. **Batch size:** Trade-off between gradient quality and steps-per-budget
7. **Initialization:** Weight init schemes, residual scaling parameters
8. **Advanced:** Value embeddings, softcapped logits, GQA (grouped query attention)

### Key Constraints

- **Fixed 5-minute time budget.** All experiments are directly comparable regardless of
  model size or architecture — the wall clock is the equalizer.
- **Single file modification.** Only `train.py` changes; `prepare.py` is immutable.
  This ensures fair comparison (same data, same evaluation).
- **VRAM is a soft constraint.** Using more VRAM is acceptable but note the trade-off
  (larger model = fewer training steps in 5 minutes).

### Decision Rule

- Lower `val_bpb` = improvement → keep
- Equal or higher `val_bpb` = regression → discard
- Crash (OOM, CUDA error) → discard, note the failure, try a smaller change
- **Simplicity wins:** Equal val_bpb with simpler code → keep

### ML-Specific ASI Annotations

For ML experiments, include these in ASI:

```json
{
  "hypothesis": "Deeper model with fewer steps should compress better",
  "arch_change": "DEPTH 8→12, DEVICE_BATCH_SIZE 128→64",
  "result": "val_bpb improved 0.998→0.992, but 2x VRAM",
  "next_action_hint": "Try intermediate DEPTH=10 for better VRAM tradeoff"
}
```

## Metric: Bits Per Byte (BPB)

### What It Measures

- How well the model compresses text
- Normalized by byte count (not token count)
- **Vocabulary-size-independent** — changes to tokenizer/vocab don't affect comparability

### Formula

```
BPB = (cross_entropy_loss × tokens_in_sequence) / bytes_in_sequence × log2(e)
```

### Interpreting BPB

| Range | Quality |
|-------|---------|
| > 2.0 | Poor — model barely compresses |
| 1.5–2.0 | Moderate |
| 1.0–1.5 | Good |
| < 1.0 | Excellent |

### Why BPB over Perplexity

- Perplexity depends on vocab size — unfair for architecture changes
- BPB normalizes by bytes → all architectures directly comparable

## Benchmark Script for ML

When setting up the autoresearch loop, use this as `autoresearch.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Run training (5 minutes, outputs metrics to stderr)
uv run train.py > run.log 2>&1

# Extract metrics from output
val_bpb=$(grep "^val_bpb:" run.log | tail -1 | awk '{print $2}' || echo "0")
memory=$(grep "^peak_vram_mb:" run.log | tail -1 | awk '{print $2}' || echo "0")
mfu=$(grep "^mfu_percent:" run.log | tail -1 | awk '{print $2}' || echo "0")

echo "METRIC val_bpb=$val_bpb"
echo "METRIC peak_memory_mb=$memory"
echo "METRIC mfu_percent=$mfu"
```

## Additional Resources

### Reference Files

- **`references/gpu-training-guide.md`** — Detailed GPU setup, CUDA configuration, troubleshooting OOM errors, and performance tuning tips

### Asset Files

All files in `assets/` are ready to copy into a project:

- **`assets/prepare.py`** — Data preparation (download, tokenizer, dataloader, evaluation)
- **`assets/train.py`** — Model architecture and training loop
- **`assets/program.md`** — Self-contained agent instructions for the ML loop
- **`assets/pyproject.toml`** — Python dependencies (PyTorch, Flash Attention, etc.)
