---
name: llm-pretraining
description: Plan and execute large language model pretraining from data preparation to checkpoint management
---

# LLM Pretraining

End-to-end pretraining workflow: data mixing, tokenizer co-design, scaling law estimation, compute budgeting, checkpoint management, and training stability monitoring.

## Decision Table

| Scale (params) | Data Budget | Batch Size (tokens) | LR | Key Considerations |
|---|---|---|---|---|
| 100M-500M | 5-10B tokens | 256K-512K | 3e-4 | Quick experiments, single-node |
| 1-3B | 20-60B tokens | 512K-1M | 2e-4 | Chinchilla ~20 tok/param |
| 7-13B | 140-500B tokens | 1M-2M | 1.5e-4 | Multi-node, activation ckpt |
| 30-70B | 1-2T tokens | 2M-4M | 1e-4 | TP+PP, quality annealing phase |
| 200B+ | 4T+ tokens | 4M-8M | 6e-5 | MoE likely, multi-phase curriculum |

## Data Mixing and Curriculum

### Multi-Phase Training Configuration

```python
from dataclasses import dataclass

@dataclass
class DomainSource:
    name: str
    path: str
    weight: float          # fraction of tokens from this source
    quality_threshold: float  # min quality score to include
    dedup_strategy: str    # "exact", "fuzzy", "none"

@dataclass
class TrainingPhase:
    name: str
    token_budget: int
    sources: list[DomainSource]
    batch_size_tokens: int
    learning_rate: float

    def validate(self):
        total = sum(s.weight for s in self.sources)
        assert abs(total - 1.0) < 1e-6, f"Weights sum to {total}, need 1.0"

# Phase 1: broad pretraining (80% of compute)
phase1 = TrainingPhase(
    name="foundation",
    token_budget=int(4e12),
    sources=[
        DomainSource("web_filtered", "/data/web", 0.50, 0.7, "fuzzy"),
        DomainSource("books", "/data/books", 0.12, 0.8, "exact"),
        DomainSource("academic", "/data/papers", 0.10, 0.8, "exact"),
        DomainSource("code", "/data/code", 0.18, 0.6, "exact"),
        DomainSource("math", "/data/math", 0.05, 0.9, "exact"),
        DomainSource("encyclopedic", "/data/wiki", 0.05, 0.9, "exact"),
    ],
    batch_size_tokens=2_097_152,
    learning_rate=1.5e-4,
)

# Phase 2: quality annealing (15% of compute)
phase2 = TrainingPhase(
    name="quality_annealing",
    token_budget=int(750e9),
    sources=[
        DomainSource("web_hq", "/data/web_hq", 0.30, 0.9, "fuzzy"),
        DomainSource("books", "/data/books", 0.20, 0.9, "exact"),
        DomainSource("code_hq", "/data/code_hq", 0.25, 0.8, "exact"),
        DomainSource("academic", "/data/papers", 0.15, 0.9, "exact"),
        DomainSource("math", "/data/math", 0.10, 0.95, "exact"),
    ],
    batch_size_tokens=4_194_304,
    learning_rate=3e-5,
)
```

### Tokenizer-Data Co-Design

```python
import sentencepiece as spm
from pathlib import Path
import random

def build_tokenizer_corpus(sources: list[DomainSource], sample_size: int = 10_000_000,
                           output_path: str = "/tmp/claude/tok_corpus.txt") -> str:
    """Sample lines proportional to mix weight for tokenizer training."""
    lines_per_source = {s.name: int(sample_size * s.weight) for s in sources}
    with open(output_path, "w") as out:
        for source in sources:
            count = lines_per_source[source.name]
            src_files = list(Path(source.path).glob("*.txt"))
            written = 0
            for f in random.sample(src_files, min(len(src_files), 500)):
                for line in open(f):
                    if written >= count:
                        break
                    out.write(line)
                    written += 1
    return output_path

def train_tokenizer(corpus_path: str, vocab_size: int = 64000):
    spm.SentencePieceTrainer.train(
        input=corpus_path, model_prefix="tokenizer", vocab_size=vocab_size,
        model_type="bpe", byte_fallback=True, split_digits=True,
        num_threads=64, character_coverage=0.9999,
        max_sentence_length=16384, shuffle_input_sentence=True,
        train_extremely_large_corpus=True,
    )
    # Fertility check: good tokenizer = 1.2-1.5 tokens per whitespace word
```

## Scaling Law Estimation

```python
import math

def chinchilla_optimal(compute_flops: float) -> dict:
    """Estimate optimal N (params) and D (tokens) for given compute."""
    n_opt = (compute_flops / 120) ** 0.5
    d_opt = 20 * n_opt
    return {"params_B": n_opt / 1e9, "tokens_T": d_opt / 1e12, "compute_flops": compute_flops}

def estimate_training_time(params_B: float, tokens_T: float, num_gpus: int,
                           gpu_tflops: float = 312, mfu: float = 0.40) -> dict:
    flops_total = 6 * params_B * 1e9 * tokens_T * 1e12
    effective_tflops = gpu_tflops * mfu * num_gpus
    seconds = flops_total / (effective_tflops * 1e12)
    return {"gpu_hours": seconds * num_gpus / 3600, "wall_days": seconds / 86400,
            "total_pflops_days": flops_total / (1e15 * 86400), "mfu": mfu}

# 13B model, Chinchilla-optimal: ~260B tokens, ~128 H100s, ~10 days
```

## Checkpoint Management

```python
import torch
import torch.distributed.checkpoint as dcp
from pathlib import Path
import json, time, shutil

class CheckpointManager:
    def __init__(self, base_dir: str, max_keep: int = 5):
        self.base_dir = Path(base_dir)
        self.max_keep = max_keep
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save(self, model, optimizer, step: int, loss: float, extra: dict = None):
        ckpt_dir = self.base_dir / f"step_{step:08d}"
        ckpt_dir.mkdir(exist_ok=True)
        dcp.save({"model": model, "optimizer": optimizer}, checkpoint_id=str(ckpt_dir))
        meta = {"step": step, "loss": loss, "timestamp": time.time(), **(extra or {})}
        (ckpt_dir / "meta.json").write_text(json.dumps(meta))
        self._prune_old()

    def load_latest(self, model, optimizer) -> dict:
        ckpts = sorted(self.base_dir.glob("step_*"))
        if not ckpts:
            raise FileNotFoundError("No checkpoints found")
        latest = ckpts[-1]
        dcp.load({"model": model, "optimizer": optimizer}, checkpoint_id=str(latest))
        return json.loads((latest / "meta.json").read_text())

    def rollback_to(self, model, optimizer, step: int) -> dict:
        target = self.base_dir / f"step_{step:08d}"
        if not target.exists():
            raise FileNotFoundError(f"Checkpoint step_{step:08d} not found")
        dcp.load({"model": model, "optimizer": optimizer}, checkpoint_id=str(target))
        return json.loads((target / "meta.json").read_text())

    def _prune_old(self):
        ckpts = sorted(self.base_dir.glob("step_*"))
        while len(ckpts) > self.max_keep:
            shutil.rmtree(ckpts.pop(0))
```

### Loss Spike Detection

```python
import numpy as np
from collections import deque

class StabilityMonitor:
    def __init__(self, window: int = 100, spike_threshold: float = 2.0):
        self.losses = deque(maxlen=window * 5)
        self.window = window
        self.spike_threshold = spike_threshold
        self.last_stable_step = 0

    def record(self, step: int, loss: float, grad_norm: float) -> dict:
        self.losses.append(loss)
        status = {"step": step, "spike": False, "action": "continue"}
        if len(self.losses) < self.window:
            self.last_stable_step = step
            return status
        recent = list(self.losses)[-self.window:]
        rolling_mean = np.mean(recent[:-1])
        rolling_std = np.std(recent[:-1])
        if loss > rolling_mean + self.spike_threshold * rolling_std:
            status["spike"] = True
            severity = (loss - rolling_mean) / max(rolling_std, 1e-8)
            status["action"] = "rollback" if severity > 5.0 else "skip_and_reduce_lr"
            if severity > 5.0:
                status["rollback_step"] = self.last_stable_step
        else:
            self.last_stable_step = step
        if grad_norm > 10.0:
            status["action"] = "clip_and_reduce_lr"
        return status
```

## Gotchas

- **Data dedup across phases**: repeated high-quality data in annealing causes memorization; track doc-level overlap
- **Tokenizer fertility drift**: adding domains with poor coverage drops effective sequence length
- **Chinchilla is a lower bound**: overtrained models transfer better; plan 2-5x Chinchilla tokens at smaller scales
- **Batch size ramp timing**: ramp too fast = instability; ramp over 2-5% of total steps
- **Checkpoint storage**: 70B checkpoint ~140GB; with Adam states ~420GB per save; budget 10-50TB
- **Loss spikes below 1B tokens are normal**: don't rollback before 0.5-1% of total training tokens
- **MFU drops with PP**: expect 30-35% with pipeline parallelism vs 40-45% with pure TP/FSDP
- **LR restarts between phases**: use smooth transitions at phase boundaries, not cold restarts
- **bf16 vs fp32 accumulation**: always accumulate gradients in fp32; skipping causes slow divergence
- **Z-loss regularization**: add small aux loss on logit magnitude (1e-4) to prevent logit drift
