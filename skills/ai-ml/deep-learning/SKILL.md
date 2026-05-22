---
name: deep-learning
description: Build and train neural networks with PyTorch - MLPs, CNNs, and training best practices
version: "1.4.0"
sasmp_version: "1.4.0"
bonded_agent: 04-deep-learning
bond_type: PRIMARY_BOND

# Parameter Validation
parameters:
  required:
    - name: model
      type: nn.Module
      validation: "Valid PyTorch model"
    - name: train_loader
      type: DataLoader
      validation: "Non-empty DataLoader"
  optional:
    - name: epochs
      type: integer
      default: 10
      validation: "1 <= epochs <= 1000"
    - name: lr
      type: float
      default: 0.001
      validation: "1e-6 <= lr <= 1"

# Retry Logic
retry_logic:
  strategy: exponential_backoff
  max_attempts: 3
  base_delay_ms: 1000

# Observability
logging:
  level: info
  metrics: [train_loss, val_loss, val_accuracy, gpu_memory]
---

# Deep Learning Skill

> Build and train neural networks using PyTorch.

## Quick Start

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

# Define model
class SimpleNN(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, x):
        return self.layers(x)

# Train
model = SimpleNN(10, 64, 2)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()

for epoch in range(10):
    model.train()
    for batch_x, batch_y in train_loader:
        optimizer.zero_grad()
        output = model(batch_x)
        loss = criterion(output, batch_y)
        loss.backward()
        optimizer.step()
```

## Key Topics

### 1. Neural Network Architectures

| Architecture | Use Case | Key Layers |
|-------------|----------|------------|
| **MLP** | Tabular data | Linear, ReLU, Dropout |
| **CNN** | Images | Conv2d, MaxPool2d, BatchNorm |
| **RNN/LSTM** | Sequences | LSTM, GRU |
| **Transformer** | NLP, Vision | MultiheadAttention |

```python
class MLP(nn.Module):
    def __init__(self, dims, dropout=0.3):
        super().__init__()
        layers = []
        for i in range(len(dims) - 1):
            layers.extend([
                nn.Linear(dims[i], dims[i+1]),
                nn.BatchNorm1d(dims[i+1]) if i < len(dims) - 2 else nn.Identity(),
                nn.ReLU() if i < len(dims) - 2 else nn.Identity(),
                nn.Dropout(dropout) if i < len(dims) - 2 else nn.Identity()
            ])
        self.network = nn.Sequential(*layers)

    def forward(self, x):
        return self.network(x)
```

### 2. Training Loop Template

```python
import torch.cuda.amp as amp

def train_epoch(model, loader, optimizer, criterion, device, scaler=None):
    model.train()
    total_loss = 0

    for batch_x, batch_y in loader:
        batch_x, batch_y = batch_x.to(device), batch_y.to(device)

        optimizer.zero_grad()

        if scaler:  # Mixed precision
            with amp.autocast():
                output = model(batch_x)
                loss = criterion(output, batch_y)
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            output = model(batch_x)
            loss = criterion(output, batch_y)
            loss.backward()
            optimizer.step()

        total_loss += loss.item()

    return total_loss / len(loader)
```

### 3. Learning Rate Scheduling

```python
from torch.optim.lr_scheduler import OneCycleLR, CosineAnnealingLR

# OneCycle (recommended)
scheduler = OneCycleLR(
    optimizer,
    max_lr=1e-3,
    epochs=epochs,
    steps_per_epoch=len(train_loader)
)

# Cosine Annealing
scheduler = CosineAnnealingLR(optimizer, T_max=epochs)
```

### 4. Regularization

| Technique | Implementation |
|-----------|----------------|
| **Dropout** | `nn.Dropout(p=0.3)` |
| **Weight Decay** | `AdamW(weight_decay=0.01)` |
| **Batch Norm** | `nn.BatchNorm1d(dim)` |
| **Early Stopping** | Monitor val_loss |

### 5. Model Checkpointing

```python
def save_checkpoint(model, optimizer, epoch, val_loss, path):
    torch.save({
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'val_loss': val_loss
    }, path)

def load_checkpoint(model, optimizer, path):
    checkpoint = torch.load(path)
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    return checkpoint['epoch'], checkpoint['val_loss']
```

## Best Practices

### DO
- Use mixed precision training (AMP)
- Apply gradient clipping
- Save checkpoints regularly
- Use AdamW over Adam
- Monitor learning curves
- Initialize weights properly

### DON'T
- Don't use large batches without LR scaling
- Don't train without validation
- Don't skip weight initialization
- Don't ignore NaN losses

## Exercises

### Exercise 1: Basic MLP
```python
# TODO: Build an MLP for MNIST classification
# Architecture: 784 -> 256 -> 128 -> 10
```

### Exercise 2: Training with AMP
```python
# TODO: Implement mixed precision training
# and compare speed with FP32 training
```

## Unit Test Template

```python
import pytest
import torch

def test_model_forward():
    """Test model forward pass."""
    model = SimpleNN(10, 64, 2)
    x = torch.randn(32, 10)

    output = model(x)

    assert output.shape == (32, 2)

def test_model_backward():
    """Test gradient flow."""
    model = SimpleNN(10, 64, 2)
    x = torch.randn(32, 10)
    y = torch.randint(0, 2, (32,))

    output = model(x)
    loss = nn.CrossEntropyLoss()(output, y)
    loss.backward()

    # Check gradients exist
    for param in model.parameters():
        assert param.grad is not None
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| NaN loss | Exploding gradients | Add gradient clipping |
| Loss plateau | LR too low | Increase LR or use scheduler |
| Overfitting | Model too complex | Add dropout, reduce layers |
| GPU OOM | Batch too large | Reduce batch size |

## Related Resources

- **Agent**: `04-deep-learning`
- **Previous**: `clustering`
- **Next**: `nlp-basics`
- **Docs**: [PyTorch Tutorials](https://pytorch.org/tutorials/)

---

**Version**: 1.4.0 | **Status**: Production Ready
