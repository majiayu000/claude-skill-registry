---
name: ml-experiment-lifecycle
description: Use when designing ML experiments, choosing evaluation metrics, tracking experiments, tuning hyperparameters, debugging training, ensuring reproducibility, or building ML pipelines. Covers W&B/MLflow integration, seed management, deterministic training, HPO strategy, and MLOps pipeline design.
---

# ML Experiment Lifecycle

## Metric Selection

| Task | Primary | When to Prefer Alternative |
|------|---------|---------------------------|
| Classification | F1 (macro) | AUC-ROC for imbalanced; MCC for binary with skew |
| Detection | mAP@0.5:0.95 | mAP@0.5 for coarse localization |
| NLP Generation | BERTScore | ROUGE for extractive; perplexity for language modeling |
| Regression | MAE | MSE when outlier penalty matters; MAPE for interpretability |
| Ranking/RAG | NDCG | MRR when only first hit matters; Precision@K for top-heavy use |

## Statistical Comparison

- **Paired bootstrap** over t-test: no normality assumption, more robust for ML
- **McNemar's test** for classifier comparison on same test set
- **Always report**: effect size (Cohen's d) alongside p-values
- **Multiple comparisons**: Benjamini-Hochberg for exploratory ablations, Bonferroni for confirmatory claims
- **Minimum seeds**: 5-10 for reliable multi-seed comparison; 3 is insufficient
- **Paired tests** when models share test data; independent otherwise

## LLM Evaluation

- LLM-as-judge: always validate with human agreement checks before trusting
- Pairwise comparison (A vs B) more reliable than absolute scoring
- Use temperature=0 for judge calls; run each judgment 3x for stability
- Track judge consistency (self-agreement rate) as a meta-metric

## Experiment Tracking

### Platform Selection

| Feature | W&B | MLflow | Neptune |
|---------|-----|--------|---------|
| Hosted option | Yes (default) | Self-hosted or Databricks | Yes |
| Free tier | 100 GB artifacts | Unlimited (self-hosted) | Limited |
| UI quality | Best | Functional | Good |
| Sweep/HPO | Built-in (Bayesian, grid, random) | Manual or Optuna plugin | Built-in |
| Team collaboration | Strong | Basic | Good |
| Git integration | Auto-logs commit hash | Manual | Auto-logs |
| Large artifacts | W&B Artifacts (versioned) | MLflow Artifacts (S3/GCS) | Neptune Artifacts |
| Best for | Research teams, LLM training | MLOps pipelines, Databricks shops | Lightweight alternative |

**Decision rule**: Research/experimentation-heavy → W&B. Production MLOps on Databricks → MLflow. Budget-conscious or simple needs → Neptune or MLflow self-hosted.

### Metric Naming Convention

```
{split}/{metric_name}          # train/loss, eval/accuracy
{split}/{task}/{metric_name}   # eval/mmlu/accuracy, eval/gsm8k/exact_match
system/{resource}              # system/gpu_memory, system/gpu_utilization
```

Establish naming conventions before the first experiment, not after. Inconsistent names make comparison impossible.

### W&B Run Configuration

```python
import wandb

run = wandb.init(
    project="llm-fine-tuning",
    name="llama-3.1-8b-lora-r64",
    config={
        "model": "meta-llama/Llama-3.1-8B",
        "method": "lora",
        "lora_r": 64,
        "learning_rate": 2e-4,
        "batch_size": 16,
    },
    tags=["lora", "llama-3.1", "qa-task"],
    group="lora-rank-sweep",
)
```

### Artifact Versioning

```python
# Save model artifact
artifact = wandb.Artifact(
    name="llama-lora-adapter", type="model",
    metadata={"base_model": "meta-llama/Llama-3.1-8B", "lora_r": 64},
)
artifact.add_dir("./output/final_adapter")
run.log_artifact(artifact)

# Load in another run
artifact = run.use_artifact("llama-lora-adapter:latest")
artifact_dir = artifact.download()
```

### Sweep Configuration

```yaml
# sweep_config.yaml
program: train.py
method: bayes
metric:
  name: eval/f1
  goal: maximize
parameters:
  learning_rate:
    distribution: log_uniform_values
    min: 1e-5
    max: 1e-3
  lora_r:
    values: [8, 16, 32, 64, 128]
  weight_decay:
    values: [0.0, 0.01, 0.1]
early_terminate:
  type: hyperband
  min_iter: 100
  eta: 3
```

## Reproducibility

### Seed Management

```python
import os, random
import numpy as np

def seed_everything(seed: int = 42) -> None:
    """Set seed for all common sources of randomness. Call BEFORE any model/data init."""
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    except ImportError:
        pass
```

### Per-Component Seeds

```python
from dataclasses import dataclass

@dataclass
class SeedConfig:
    """Separate seeds per concern -- change data split without re-initializing model."""
    global_seed: int = 42
    data_seed: int = 100      # Data loading, augmentation, splits
    model_seed: int = 200     # Weight initialization
    train_seed: int = 300     # Dropout, sampling during training
```

### Deterministic PyTorch

```python
import torch, os

def enable_deterministic(warn_only: bool = False) -> None:
    """Enable deterministic ops. WARNING: 10-20% slower. Use for final results only."""
    torch.use_deterministic_algorithms(True, warn_only=warn_only)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
```

### Known Non-Deterministic PyTorch Ops
`index_add_`, `scatter_add_`, `bincount`, `histc`, `F.interpolate` (some modes), `F.grid_sample`, `ReflectionPad2d`, `ctc_loss`

### DataLoader Determinism

```python
def worker_init_fn(worker_id: int) -> None:
    seed = torch.initial_seed() % 2**32
    np.random.seed(seed + worker_id)
    random.seed(seed + worker_id)

loader = DataLoader(
    dataset, batch_size=32, num_workers=4,
    worker_init_fn=worker_init_fn,
    generator=torch.Generator().manual_seed(42),
)
```

### Checkpoint State

```python
checkpoint = {
    "model": model.state_dict(),
    "optimizer": optimizer.state_dict(),
    "scheduler": scheduler.state_dict(),
    "epoch": epoch,
    "rng_states": {
        "python": random.getstate(),
        "numpy": np.random.get_state(),
        "torch": torch.random.get_rng_state(),
        "cuda": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None,
    },
}
```

### Environment Locking
- `pip-compile` with `--generate-hashes` (preferred over bare `pip freeze`)
- Pin CUDA version in Docker image tag, not just PyTorch version
- Log git commit + dirty state + full diff for every experiment run

### Config Management
- Hydra for CLI overrides + YAML composition
- Pydantic with `extra = "forbid"` to catch config typos at startup
- Save resolved config JSON alongside every checkpoint

## Model Debugging Checklist

| Symptom | Check First | Common Fix |
|---------|-------------|------------|
| Loss not decreasing | LR, gradient norms, frozen params | LR finder; unfreeze layers |
| NaN loss | log(0), div-by-zero, extreme logits | Gradient clipping, lower LR, input normalization |
| Overfitting | Train/val gap trend over 5+ epochs | Dropout, weight decay, data augmentation, early stopping |
| Underfitting | Model capacity, feature quality | Increase depth/width, better features |
| Gradient explosion | Norm > 100 on any layer | Clip gradients (max_norm=1.0) |
| Dead neurons | Zero gradient norms | Check activation functions, initialization |

### LR Finder Protocol
Run LR range test (1e-7 to 10) before any serious training. Pick LR at steepest descent point (not minimum loss). Restore model/optimizer state after the sweep.

## Hyperparameter Optimization

### Strategy Selection

| Budget (trials) | Strategy | Key Setting |
|-----------------|----------|-------------|
| < 20 | Random search | Focus on top 2-3 params only |
| 20-100 | TPE (Optuna) | `n_startup_trials=10`, `multivariate=True` |
| 100+ | Hyperband/ASHA | `grace_period=10`, `reduction_factor=3` |
| Large models, RL | PBT (Ray Tune) | `perturbation_interval=5` |

### Search Space Opinions
- **Learning rate**: always log-uniform
- **Weight decay**: log-uniform with conditional enable/disable
- **Batch size**: categorical powers of 2 (not continuous)
- **Hidden dims**: step-aligned to head count for transformers
- **Optimizer-specific params**: conditional (beta1/beta2 only if Adam family)
- Enable **pruning** in every Optuna study; unpruned runs waste GPU hours

### Post-HPO
- Analyze parameter importance before expanding search space
- Sensitivity analysis: correlation of each param with objective
- Validate final config with 5+ seeds on held-out test set (not validation set used during tuning)

### Preferred Stack
- **Optuna** (default): TPE + Hyperband pruner, SQLite storage for persistence
- **Ray Tune**: when distributed across machines or using PBT
- **W&B / MLflow**: experiment tracking (log git commit, code snapshot, full config)

## Pipeline Design

### Stage Ordering
Data ingestion → validation → feature engineering → training → evaluation → deployment

### Principles
- **Idempotent stages**: re-running any stage produces same output
- **Version everything**: data (DVC), code (git), models (registry), configs (alongside checkpoints)
- **Gate deployments**: automated metric comparison against baseline before promotion

### Deployment Strategy Selection

| Strategy | When |
|----------|------|
| Shadow | First deployment; validate without user impact |
| Canary | Incremental rollout with rollback capability |
| Blue-Green | Zero-downtime full cutover |
| A/B Test | Comparing model variants with statistical rigor |

### Orchestrator Selection
- **Airflow**: mature, DAG-based, large ecosystem
- **Dagster**: asset-oriented, better local dev experience
- **Kubeflow Pipelines**: Kubernetes-native, good for GPU workloads
- **Prefect**: simpler API, good for smaller teams

### Model Registry Practices
- Every model artifact: metrics, config, data version, git hash, training duration
- Promote through stages: dev → staging → production
- Maintain rollback to previous production model at all times
- Monitor drift: data distribution shift, prediction distribution shift, latency degradation

## Gotchas

### Tracking
- Not logging exact command/config to reproduce a run
- Forgetting `wandb.finish()` without `with` context manager (data loss)
- Logging `torch.Tensor` instead of `.item()` -- silently stores the whole tensor
- Not setting `group` for related runs -- sweeps hard to analyze
- Logging eval metrics at training step count (misaligns x-axis in charts)

### Reproducibility
- Parallel reductions (multi-GPU) change floating point accumulation order -- document exact GPU count
- PyTorch weight init changed between versions -- same seed, different version = different weights
- FP16/BF16 results vary across GPU architectures (A100 vs V100 vs H100)
- `num_workers > 0` introduces OS-level scheduling non-determinism -- use `worker_init_fn`
- Saving model weights without optimizer/scheduler/RNG state makes resume non-deterministic
