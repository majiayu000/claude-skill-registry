---
name: training-pipelines
version: "2.0.0"
sasmp_version: "1.3.0"
description: Master training pipelines - orchestration, distributed training, hyperparameter tuning
bonded_agent: 04-training-pipelines
bond_type: PRIMARY_BOND

# SKILL METADATA
category: training
difficulty: intermediate_to_advanced
estimated_hours: 40
prerequisites:
  - mlops-basics
  - experiment-tracking

# VALIDATION
validation:
  pre_conditions:
    - "Completed prerequisite skills"
    - "Access to GPU resources"
  post_conditions:
    - "Can build Kubeflow pipelines"
    - "Can configure distributed training"
    - "Can run hyperparameter tuning"

# OBSERVABILITY
observability:
  metrics:
    - pipelines_created
    - training_jobs_completed
    - gpu_utilization
---

# Training Pipelines Skill

> **Learn**: Build production training pipelines with orchestration and distributed training.

## Skill Overview

| Attribute | Value |
|-----------|-------|
| **Bonded Agent** | 04-training-pipelines |
| **Difficulty** | Intermediate to Advanced |
| **Duration** | 40 hours |
| **Prerequisites** | mlops-basics, experiment-tracking |

---

## Learning Objectives

1. **Design** end-to-end training pipelines
2. **Implement** distributed training with PyTorch DDP
3. **Configure** hyperparameter tuning with Optuna
4. **Deploy** pipelines to Kubeflow
5. **Optimize** GPU utilization and costs

---

## Topics Covered

### Module 1: Pipeline Design (10 hours)

**Pipeline Architecture:**

```
┌────────────────────────────────────────────────────────────────┐
│                    TRAINING PIPELINE                            │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌───────┐ │
│  │  Data   │─▶│Preprocess│─▶│  Train  │─▶│ Evaluate│─▶│Register│ │
│  │  Load   │  │         │  │         │  │         │  │       │ │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └───────┘ │
│                              ║                                  │
│                              ▼                                  │
│                        [Hyperparameter]                         │
│                        [   Tuning     ]                         │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

### Module 2: Distributed Training (12 hours)

**PyTorch DDP Setup:**

```python
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

def setup_distributed():
    dist.init_process_group(backend="nccl")
    local_rank = int(os.environ["LOCAL_RANK"])
    torch.cuda.set_device(local_rank)
    return local_rank

# Wrap model
model = DDP(model, device_ids=[local_rank])

# Use DistributedSampler
sampler = DistributedSampler(dataset)
loader = DataLoader(dataset, sampler=sampler)
```

**Exercises:**
- [ ] Convert single-GPU training to DDP
- [ ] Benchmark scaling efficiency
- [ ] Implement gradient accumulation

---

### Module 3: Hyperparameter Tuning (10 hours)

**Optuna Configuration:**

```python
import optuna

def objective(trial):
    lr = trial.suggest_float("lr", 1e-5, 1e-2, log=True)
    batch_size = trial.suggest_categorical("batch_size", [16, 32, 64])
    hidden_size = trial.suggest_int("hidden_size", 64, 512, step=64)

    model = build_model(hidden_size)
    metrics = train_model(model, lr, batch_size)

    return metrics["val_loss"]

study = optuna.create_study(
    direction="minimize",
    sampler=TPESampler(),
    pruner=HyperbandPruner()
)
study.optimize(objective, n_trials=100)
```

---

### Module 4: Pipeline Deployment (8 hours)

**Kubeflow Pipeline:**

```python
from kfp import dsl, compiler

@dsl.component
def train_model(data_path: str, model_path: str):
    # Training logic
    pass

@dsl.pipeline(name="training-pipeline")
def training_pipeline(dataset_uri: str):
    preprocess_task = preprocess_data(input_path=dataset_uri)
    train_task = train_model(data_path=preprocess_task.output)
    train_task.set_gpu_limit(1)
```

---

## Code Templates

### Template: Production Training Script

```python
# templates/train.py
import torch
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping

class ProductionTrainer:
    """Production-ready training wrapper."""

    def __init__(self, config: dict):
        self.config = config

    def train(self, model, train_loader, val_loader):
        callbacks = [
            ModelCheckpoint(
                monitor="val_loss",
                mode="min",
                save_top_k=3
            ),
            EarlyStopping(
                monitor="val_loss",
                patience=5
            )
        ]

        trainer = pl.Trainer(
            max_epochs=self.config["epochs"],
            accelerator="gpu",
            devices=self.config["gpus"],
            strategy="ddp" if self.config["gpus"] > 1 else "auto",
            callbacks=callbacks,
            precision="16-mixed"
        )

        trainer.fit(model, train_loader, val_loader)
        return trainer
```

---

## Troubleshooting Guide

| Issue | Cause | Solution |
|-------|-------|----------|
| GPU OOM | Batch too large | Reduce batch, use gradient accumulation |
| Slow training | I/O bottleneck | Increase workers, prefetch |
| Distributed hang | NCCL timeout | Check network, increase timeout |

---

## Resources

- [PyTorch DDP Tutorial](https://pytorch.org/tutorials/intermediate/ddp_tutorial.html)
- [Kubeflow Pipelines](https://www.kubeflow.org/docs/components/pipelines/)
- [Optuna Documentation](https://optuna.org/)
- [See: model-serving] - Deploy trained models

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2024-12 | Production-grade with DDP examples |
| 1.0.0 | 2024-11 | Initial release |
