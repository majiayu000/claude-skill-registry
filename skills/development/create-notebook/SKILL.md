---
name: create-notebook
description: Skill from tsilva/aiml-notebooks
---

## 📓 **AI/ML Notebook Creation Guide**

Create **highly engaging, interactive notebooks** (50-80 cells) that build deep intuitions through step-by-step progression.

---

### 🎯 Core Philosophy

**Build knowledge like climbing stairs — each step small, solid, and leading naturally to the next.**

Notebooks should feel like a conversation with an expert teacher who shows before telling.

---

### ⚙️ Essential Rules

#### **Structure**
* **Markdown before every code cell** — even if just one line
* **Theory before practice** — explain "why" before "how"
* **Incremental progression** — each concept builds on the last
* **50-80 cells** — enough depth without overwhelming
* **Self-contained** — runnable end-to-end

#### **Content**
* **One concept per section** — don't bundle multiple ideas
* **Visualize after implementation** — always show, don't just tell
* **Concrete before abstract** — examples before generalizations
* **Bold key terms** — e.g., **embedding**, **attention**

#### **Code Cells**
* One logical unit per cell (model, training, visualization)
* Clear variable names
* Comments for non-obvious logic only
* Print/plot results immediately

---

### ⚙️ Technical Requirements

#### **1. CONFIG Dictionary (at top, after setup imports)**
All hyperparameters in one place with inline comments:

```python
CONFIG = {
    # Reproducibility
    'seed': 42,  # Random seed for reproducibility

    # Data
    'batch_size': 128,  # Number of samples per training batch
    'num_workers': 0,  # Number of worker processes for data loading

    # Training
    'learning_rate': 0.001,  # Optimizer learning rate
    'max_epochs': 50,  # Maximum number of training epochs
    'early_stop_patience': 10,  # Epochs to wait before early stopping

    # Model
    'num_classes': 10,  # Number of output classes
}
```

#### **2. PyTorch Lightning (default)**
Use Lightning unless explicitly teaching training fundamentals:
* Models inherit from `L.LightningModule`
* Implement `training_step`, `validation_step`, `configure_optimizers`
* Use `L.Trainer` with `CSVLogger` to track metrics
* **Always use `EarlyStopping` callback** (monitors `val_loss`, patience=10)
* Lightning handles device management automatically
* **Always plot training/validation curves** after training (loss and accuracy/metrics)

#### **3. Distributed Imports**
Place imports **in the same cell** as their first usage:
* Setup: `from aiml_notebooks import get_device, set_seed` (with CONFIG/seed)
* Data: `from torchvision import datasets, transforms` (with transforms)
* Model: `import torch, torch.nn as nn, lightning as L` (with model)
* Viz: `import matplotlib.pyplot as plt` (with first plot)

Exception: Very long cells may have a separate import cell immediately before.

#### **4. Shared Library**
```python
from aiml_notebooks import CharacterTokenizer, create_dataset, get_device, set_seed

%load_ext autoreload
%autoreload 2
```

#### **5. Random Seed & Device**
```python
set_seed(CONFIG['seed'])
device = get_device()  # or get_device(prefer_cpu=True) for Transformers
```

---

### 📐 Template Structure

```markdown
# Title: Clear, Descriptive Name

## 1. Introduction
- What we'll learn and why it matters
- What intuitions we'll build

## 2. Setup
### Configuration
[CONFIG dictionary here - see above]

### Random Seed & Device
[Setup imports, seed, device - see above]

## 3-5. Building Blocks
Each section: Intuition → Implementation → Visualization → Key Insight

## 6. Putting It Together
Combine concepts, show full picture

## 7. Experiments & Exploration
Ablations, parameter sensitivity, edge cases

## 8. Key Takeaways
Bullet points of core intuitions
```

---

### ✅ Lightning Model Example

```markdown
### Implement the Model
We'll use PyTorch Lightning to keep code clean.
```

```python
import torch.nn as nn
import lightning as L

class MyModel(L.LightningModule):
    def __init__(self, num_classes=CONFIG['num_classes'],
                 learning_rate=CONFIG['learning_rate']):
        super().__init__()
        self.save_hyperparameters()
        self.fc = nn.Linear(10, num_classes)
        self.criterion = nn.CrossEntropyLoss()

    def forward(self, x):
        return self.fc(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        loss = self.criterion(self(x), y)
        self.log('train_loss', loss, prog_bar=True)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        loss = self.criterion(self(x), y)
        acc = (self(x).argmax(1) == y).float().mean()
        self.log('val_loss', loss, prog_bar=True)
        self.log('val_acc', acc, prog_bar=True)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.hparams.learning_rate)
```

```python
from lightning.pytorch.loggers import CSVLogger
from lightning.pytorch.callbacks import EarlyStopping

model = MyModel()
logger = CSVLogger('logs', name='my_model')

# Create early stopping callback
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=CONFIG['early_stop_patience'],
    mode='min',
    verbose=False  # Only print when stopping
)

trainer = L.Trainer(
    max_epochs=CONFIG['max_epochs'],
    accelerator='auto',
    devices=1,
    logger=logger,
    callbacks=[early_stop],
    enable_progress_bar=True
)
trainer.fit(model, train_loader, val_loader)
```

```markdown
### Plot training curves

Visualize how the model learned over time.
```

```python
import pandas as pd
import matplotlib.pyplot as plt

# Read metrics from CSV logger
metrics = pd.read_csv(f'{logger.log_dir}/metrics.csv')

# Aggregate by epoch (Lightning logs per step)
train_metrics = metrics[['epoch', 'train_loss', 'train_acc']].dropna()
val_metrics = metrics[['epoch', 'val_loss', 'val_acc']].dropna()
train_metrics = train_metrics.groupby('epoch').mean().reset_index()
val_metrics = val_metrics.groupby('epoch').mean().reset_index()

# Plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Loss curves
ax1.plot(train_metrics['epoch'], train_metrics['train_loss'],
         label='Train', marker='o', linewidth=2, color='#4ECDC4')
ax1.plot(val_metrics['epoch'], val_metrics['val_loss'],
         label='Validation', marker='s', linewidth=2, color='#FF6B6B')
ax1.set_xlabel('Epoch', fontsize=12)
ax1.set_ylabel('Loss', fontsize=12)
ax1.set_title('Training and Validation Loss', fontsize=14, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Mark early stopping point if triggered
if trainer.early_stopping_callback and trainer.early_stopping_callback.stopped_epoch > 0:
    stop_epoch = trainer.early_stopping_callback.stopped_epoch
    ax1.axvline(x=stop_epoch, color='red', linestyle='--', alpha=0.5, label='Early Stop')

# Accuracy/metric curves
ax2.plot(train_metrics['epoch'], train_metrics['train_acc'] * 100,
         label='Train', marker='o', linewidth=2, color='#4ECDC4')
ax2.plot(val_metrics['epoch'], val_metrics['val_acc'] * 100,
         label='Validation', marker='s', linewidth=2, color='#FF6B6B')
ax2.set_xlabel('Epoch', fontsize=12)
ax2.set_ylabel('Accuracy (%)', fontsize=12)
ax2.set_title('Training and Validation Accuracy', fontsize=14, fontweight='bold')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Mark early stopping point if triggered
if trainer.early_stopping_callback and trainer.early_stopping_callback.stopped_epoch > 0:
    ax2.axvline(x=stop_epoch, color='red', linestyle='--', alpha=0.5, label='Early Stop')

plt.tight_layout()
plt.show()

# Report training stats
epochs_trained = len(train_metrics)
print(f"\nTraining Statistics:")
print(f"  Epochs trained: {epochs_trained} / {CONFIG['max_epochs']}")
if trainer.early_stopping_callback and trainer.early_stopping_callback.stopped_epoch > 0:
    print(f"  Early stopping triggered at epoch {stop_epoch}")
print(f"\nFinal Results:")
print(f"  Train Accuracy: {train_metrics['train_acc'].iloc[-1]*100:.2f}%")
print(f"  Val Accuracy: {val_metrics['val_acc'].iloc[-1]*100:.2f}%")
print(f"  Overfitting Gap: {(train_metrics['train_acc'].iloc[-1] - val_metrics['val_acc'].iloc[-1])*100:.2f}%")
```

---

### 📝 Notebook Checklist

**Structure:**
- [ ] CONFIG at top with all hyperparameters + inline comments
- [ ] CONFIG includes `early_stop_patience` parameter
- [ ] Markdown cell before every code cell
- [ ] Imports in same cell as first usage (not separate/at top)
- [ ] `set_seed(CONFIG['seed'])` early
- [ ] 50-80 cells total

**Framework:**
- [ ] Lightning used (unless teaching fundamentals)
- [ ] Model inherits `L.LightningModule`
- [ ] Has `training_step`, `validation_step`, `configure_optimizers`
- [ ] Uses `L.Trainer` with `CSVLogger` and `EarlyStopping` callback
- [ ] No manual device movement (Lightning handles it)
- [ ] Training/validation curves plotted after training
- [ ] Early stopping point marked on curves (if triggered)

**Content:**
- [ ] Visualizations after new concepts
- [ ] Incremental progression
- [ ] Clear narrative flow
- [ ] Key insights explicitly stated
- [ ] No assumed knowledge

**Testing:**
- [ ] Runs end-to-end: `uv run jupyter nbconvert --to notebook --execute --inplace notebooks/your-notebook.ipynb`
- [ ] CONFIG changes work
- [ ] Reproducible (seed works)

**Common Mistakes (avoid these):**
- ❌ Code without markdown introduction
- ❌ All imports at beginning
- ❌ Hardcoded hyperparameters (not in CONFIG)
- ❌ Manual training loops (unless teaching fundamentals)
- ❌ CONFIG missing inline comments
- ❌ Skipping visualizations
- ❌ Not plotting training curves after training
- ❌ Not using early stopping callback

---

### 🎓 Teaching Principles

1. **Concrete → Abstract**: Examples first, then generalize
2. **Immediate Feedback**: Print/plot after every computation
3. **Progressive Complexity**: Simple → nuanced → edge cases

---

**Remember:** "Build intuitions, not just implementations. Always markdown before code. Always visualize after implementation."
