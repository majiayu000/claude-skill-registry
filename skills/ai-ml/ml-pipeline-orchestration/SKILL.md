---
name: ml-pipeline-orchestration
description: ML pipeline design with Metaflow, Kubeflow, and ZenML including GPU steps, artifact tracking, and production patterns.
---

# ML Pipeline Orchestration

## Orchestrator Selection

| Criteria | Metaflow | Kubeflow | ZenML |
|----------|----------|----------|-------|
| Setup complexity | Low (pip install) | High (K8s cluster) | Medium (pip + stack) |
| GPU support | Via `@batch`/`@kubernetes` | Native K8s GPU scheduling | Via orchestrator backend |
| Experiment tracking | Built-in (cards, artifacts) | External (MLflow/W&B) | Built-in + integrations |
| Production readiness | High (Netflix-proven) | High (K8s-native) | Medium (maturing) |
| Local dev experience | Excellent (`--local`) | Poor (needs cluster) | Good (local stack) |
| Team size sweet spot | 2-20 | 20-100+ | 2-15 |
| Best for | Data science teams | Platform engineering | MLOps standardization |

**Recommendation**: Start with Metaflow for most teams. Move to Kubeflow only if you already run Kubernetes and need multi-tenant scheduling. ZenML fits teams wanting vendor-neutral MLOps with plugin architecture.

## Pipeline Design Pattern

Standard ML pipeline stages:

```
data_ingest -> preprocess -> validate -> train -> evaluate -> register -> deploy
```

Keep each step single-responsibility. Pass artifacts (not raw data) between steps.

## Metaflow

### Flow Definition

```python
from metaflow import FlowSpec, step, batch, Parameter, card, current

class TrainFlow(FlowSpec):
    """End-to-end training pipeline."""

    lr = Parameter("lr", default=1e-4, type=float)
    epochs = Parameter("epochs", default=10, type=int)
    dataset_version = Parameter("dataset_version", default="latest")

    @step
    def start(self):
        """Load and validate dataset."""
        from data_loader import load_dataset
        self.train_df, self.val_df = load_dataset(self.dataset_version)
        print(f"Train: {len(self.train_df)}, Val: {len(self.val_df)}")
        self.next(self.train)

    @batch(gpu=1, memory=32000, image="my-registry/train:latest")
    @card
    @step
    def train(self):
        """Train model on GPU."""
        import torch
        from model import build_model, train_epoch

        model = build_model()
        optimizer = torch.optim.AdamW(model.parameters(), lr=self.lr)

        for epoch in range(self.epochs):
            loss = train_epoch(model, self.train_df, optimizer)
            current.card.append(f"Epoch {epoch}: loss={loss:.4f}")

        self.model_state = model.state_dict()
        self.next(self.evaluate)

    @batch(gpu=1, memory=16000, image="my-registry/train:latest")
    @step
    def evaluate(self):
        """Evaluate on validation set."""
        import torch
        from model import build_model, evaluate

        model = build_model()
        model.load_state_dict(self.model_state)
        self.metrics = evaluate(model, self.val_df)
        print(f"Val accuracy: {self.metrics["accuracy"]:.4f}")
        self.next(self.register)

    @step
    def register(self):
        """Register model if metrics pass threshold."""
        if self.metrics["accuracy"] > 0.85:
            from registry import register_model
            self.model_uri = register_model(self.model_state, self.metrics)
            print(f"Registered: {self.model_uri}")
        else:
            print(f"Accuracy {self.metrics["accuracy"]:.4f} below threshold")
            self.model_uri = None
        self.next(self.end)

    @step
    def end(self):
        print("Pipeline complete.")

if __name__ == "__main__":
    TrainFlow()
```

Run locally: `python train_flow.py run --lr 0.001`
Run on AWS Batch: `python train_flow.py --with batch run`

### Metaflow Parallel Training (Fan-Out)

```python
@step
def start(self):
    self.hparams = [
        {"lr": 1e-3, "batch_size": 32},
        {"lr": 1e-4, "batch_size": 64},
        {"lr": 5e-5, "batch_size": 128},
    ]
    self.next(self.train, foreach="hparams")

@batch(gpu=1, memory=32000)
@step
def train(self):
    """Parallel hyperparameter search."""
    self.config = self.input
    # ... train with self.config["lr"], etc.
    self.next(self.join)

@step
def join(self, inputs):
    """Pick best model from parallel runs."""
    best = max(inputs, key=lambda x: x.metrics["accuracy"])
    self.best_model = best.model_state
    self.best_metrics = best.metrics
    self.next(self.end)
```

## Kubeflow Pipeline with GPU Steps

```python
from kfp import dsl
from kfp.dsl import Output, Input, Model, Dataset

@dsl.component(
    base_image="nvidia/cuda:12.2.0-runtime-ubuntu22.04",
    packages_to_install=["torch==2.1.0", "transformers==4.35.0"],
)
def train_model(
    dataset: Input[Dataset],
    model_output: Output[Model],
    epochs: int = 10,
    learning_rate: float = 1e-4,
):
    import torch
    from transformers import AutoModelForSequenceClassification

    model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
    # ... training logic ...
    model.save_pretrained(model_output.path)
    model_output.metadata["accuracy"] = 0.92

@dsl.component(base_image="python:3.11-slim")
def evaluate_model(model: Input[Model], threshold: float = 0.85) -> bool:
    accuracy = float(model.metadata.get("accuracy", 0))
    return accuracy >= threshold

@dsl.pipeline(name="training-pipeline")
def training_pipeline(epochs: int = 10):
    train_task = train_model(
        dataset=load_data_task.output,
        epochs=epochs,
    ).set_gpu_limit(1).set_memory_limit("32G")

    evaluate_model(model=train_task.outputs["model_output"])
```

Compile and submit:
```bash
kfp dsl compile --py pipeline.py --output pipeline.yaml
kfp run submit --experiment training --pipeline pipeline.yaml
```

## Gotchas and Anti-Patterns

### Pipeline Serialization Issues

**Problem**: Steps pass data via serialization (pickle/cloudpickle). Large tensors or non-picklable objects (DB connections, tokenizers) break.

**Fix**: Save artifacts to storage (S3/GCS), pass URIs between steps. Never pass model weights as in-memory objects in Kubeflow; use `Output[Model]` artifacts.

### GPU Resource Allocation

**Problem**: Pipeline step requests GPU but spends 80% of time on data preprocessing (CPU-bound). Wastes expensive GPU hours.

**Fix**: Split into CPU step (preprocess) and GPU step (train). In Kubeflow:
```python
preprocess_task = preprocess_data(...).set_cpu_limit("8").set_memory_limit("32G")
train_task = train_model(...).set_gpu_limit(1).set_memory_limit("64G")
```

### Artifact Storage Costs

**Problem**: Every pipeline run saves full model checkpoints. 100 runs x 5GB = 500GB.

**Fix**: Implement retention policy. Tag runs, auto-delete artifacts older than N days except tagged-for-keep:
```python
# Metaflow: use @project + namespaces to organize
# Kubeflow: configure artifact TTL in pipeline spec
# General: checkpoint only best model per run, not every epoch
```

### Pipeline Versioning

**Problem**: Code changes but pipeline definition hash stays the same. Stale cached steps execute.

**Fix**: Pin data versions explicitly. Include code hash in step cache key. In Metaflow, use `@project(name="v2")` to namespace. In Kubeflow, set `caching_strategy.max_cache_staleness` to control cache invalidation window.
