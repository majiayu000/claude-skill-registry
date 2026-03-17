---
name: ml-experiment
description: Track ML experiments with proper logging and reproducibility. Use when training models or running experiments.
---

## Reproducibility Checklist

- [ ] Random seeds set (Python, NumPy, PyTorch/TensorFlow)
- [ ] Data version tracked
- [ ] Code version tracked (git commit)
- [ ] Environment captured (requirements.txt)
- [ ] Hyperparameters logged
- [ ] Metrics logged
- [ ] Model artifacts saved

## Setting Random Seeds
```python
import random
import numpy as np

def set_seeds(seed: int = 42) -> None:
    """Set all random seeds for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
    
    # PyTorch
    try:
        import torch
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
    except ImportError:
        pass
    
    # TensorFlow
    try:
        import tensorflow as tf
        tf.random.set_seed(seed)
    except ImportError:
        pass
```

## Experiment Logging Template
```python
from datetime import datetime
from pathlib import Path
import json

class Experiment:
    def __init__(self, name: str):
        self.name = name
        self.timestamp = datetime.now().isoformat()
        self.params = {}
        self.metrics = {}
        self.artifacts = []
        
    def log_params(self, **params):
        self.params.update(params)
        
    def log_metrics(self, **metrics):
        self.metrics.update(metrics)
        
    def log_artifact(self, path: str):
        self.artifacts.append(path)
        
    def save(self, output_dir: str = "experiments"):
        Path(output_dir).mkdir(exist_ok=True)
        path = f"{output_dir}/{self.name}_{self.timestamp}.json"
        
        with open(path, "w") as f:
            json.dump({
                "name": self.name,
                "timestamp": self.timestamp,
                "params": self.params,
                "metrics": self.metrics,
                "artifacts": self.artifacts,
            }, f, indent=2)
        
        return path

# Usage
exp = Experiment("baseline_model")
exp.log_params(
    learning_rate=0.001,
    batch_size=32,
    epochs=100,
    model_type="transformer",
)

# ... training ...

exp.log_metrics(
    train_loss=0.05,
    val_loss=0.08,
    accuracy=0.92,
    f1_score=0.89,
)
exp.log_artifact("models/baseline_v1.pt")
exp.save()
```

## Hyperparameter Organization
```python
from dataclasses import dataclass

@dataclass
class TrainingConfig:
    # Model
    model_type: str = "transformer"
    hidden_size: int = 256
    num_layers: int = 4
    dropout: float = 0.1
    
    # Training
    learning_rate: float = 1e-4
    batch_size: int = 32
    epochs: int = 100
    
    # Data
    train_split: float = 0.8
    val_split: float = 0.1
    
    # Reproducibility
    seed: int = 42

config = TrainingConfig(learning_rate=0.001)
```

## Model Checkpointing
```python
def save_checkpoint(model, optimizer, epoch, loss, path):
    """Save training checkpoint."""
    torch.save({
        "epoch": epoch,
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "loss": loss,
    }, path)

def load_checkpoint(model, optimizer, path):
    """Load training checkpoint."""
    checkpoint = torch.load(path)
    model.load_state_dict(checkpoint["model_state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
    return checkpoint["epoch"], checkpoint["loss"]
```

## Experiment Comparison
```python
def compare_experiments(exp_dir: str = "experiments"):
    """Load and compare all experiments."""
    import pandas as pd
    from pathlib import Path
    
    experiments = []
    for path in Path(exp_dir).glob("*.json"):
        with open(path) as f:
            experiments.append(json.load(f))
    
    # Flatten for comparison
    rows = []
    for exp in experiments:
        row = {"name": exp["name"], "timestamp": exp["timestamp"]}
        row.update(exp["params"])
        row.update(exp["metrics"])
        rows.append(row)
    
    return pd.DataFrame(rows).sort_values("accuracy", ascending=False)
```

## Directory Structure
```
project/
├── experiments/           # Experiment logs
│   └── baseline_2024-01-15.json
├── models/               # Saved models
│   └── baseline_v1.pt
├── data/                 # Data (versioned separately)
│   ├── raw/
│   └── processed/
├── notebooks/            # Exploration
├── src/                  # Production code
└── configs/              # Config files
    └── training.yaml
```
