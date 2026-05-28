---
name: l0
description: L0 regularization for neural network sparsification and intelligent sampling - used in survey calibration
---

# L0 Regularization

L0 is a PyTorch implementation of L0 regularization for neural network sparsification and intelligent sampling, used in PolicyEngine's survey calibration pipeline.

## For Users 👥

### What is L0?

L0 regularization helps PolicyEngine create more efficient survey datasets by intelligently selecting which households to include in calculations.

**Impact you see:**
- Faster population impact calculations
- Smaller dataset sizes
- Maintained accuracy with fewer samples

**Behind the scenes:**
When PolicyEngine shows population-wide impacts, L0 helps select representative households from the full survey, reducing computation time while maintaining accuracy.

## For Analysts 📊

### What L0 Does

L0 provides intelligent sampling gates for:
- **Household selection** - Choose representative samples from CPS
- **Feature selection** - Identify important variables
- **Sparse weighting** - Create compact, efficient datasets

**Used in PolicyEngine for:**
- Survey calibration (via microcalibrate)
- Dataset sparsification in policyengine-us-data
- Efficient microsimulation

### Installation

```bash
pip install l0-python
```

### Quick Example: Sample Selection

```python
from l0 import SampleGate

# Select 1,000 households from 10,000
gate = SampleGate(n_samples=10000, target_samples=1000)
selected_data, indices = gate.select_samples(data)

# Gates learn which samples are most informative
```

### Integration with microcalibrate

```python
from l0 import HardConcrete
from microcalibrate import Calibration

# L0 gates for household selection
gates = HardConcrete(
    len(household_weights),
    temperature=0.25,
    init_mean=0.999  # Start with most households
)

# Use in calibration
# microcalibrate applies gates during weight optimization
```

## For Contributors 💻

### Repository

**Location:** PolicyEngine/L0

**Clone:**
```bash
git clone https://github.com/PolicyEngine/L0
cd L0
```

### Current Implementation

**To see structure:**
```bash
tree l0/

# Key modules:
ls l0/
# - hard_concrete.py - Core L0 distribution
# - layers.py - L0Linear, L0Conv2d
# - gates.py - Sample/feature gates
# - penalties.py - L0/L2 penalty computation
# - temperature.py - Temperature scheduling
```

**To see specific implementations:**
```bash
# Hard Concrete distribution (core algorithm)
cat l0/hard_concrete.py

# Sample gates (used in calibration)
cat l0/gates.py

# Neural network layers
cat l0/layers.py
```

### Key Concepts

**Hard Concrete Distribution:**
- Differentiable approximation of L0 norm
- Allows gradient-based optimization
- Temperature controls sparsity level

**To see implementation:**
```bash
cat l0/hard_concrete.py
```

**Sample Gates:**
- Binary gates for sample selection
- Learn which samples are most informative
- Used in microcalibrate for household selection

**Feature Gates:**
- Select important features/variables
- Reduce dimensionality
- Maintain prediction accuracy

### Usage in PolicyEngine

**In microcalibrate (survey calibration):**
```python
from l0 import HardConcrete

# Create gates for household selection
gates = HardConcrete(
    n_items=len(households),
    temperature=0.25,
    init_mean=0.999  # Start with almost all households
)

# Gates produce probabilities (0 to 1)
probs = gates()

# Apply to weights during calibration
masked_weights = weights * probs
```

**In policyengine-us-data:**
```bash
# See usage in data pipeline
grep -r "from l0 import" ../policyengine-us-data/
```

### Temperature Scheduling

**Controls sparsity over training:**
```python
from l0 import TemperatureScheduler, update_temperatures

scheduler = TemperatureScheduler(
    initial_temp=1.0,  # Start relaxed
    final_temp=0.1,    # End sparse
    total_epochs=100
)

for epoch in range(100):
    temp = scheduler.get_temperature(epoch)
    update_temperatures(model, temp)
    # ... training ...
```

**To see implementation:**
```bash
cat l0/temperature.py
```

### L0L2 Combined Penalty

**Prevents overfitting:**
```python
from l0 import compute_l0l2_penalty

# Combine L0 (sparsity) with L2 (regularization)
penalty = compute_l0l2_penalty(
    model,
    l0_lambda=1e-3,  # Sparsity strength
    l2_lambda=1e-4   # Weight regularization
)

loss = task_loss + penalty
```

### Testing

**Run tests:**
```bash
make test

# Or
pytest tests/ -v --cov=l0
```

**To see test patterns:**
```bash
cat tests/test_hard_concrete.py
cat tests/test_gates.py
```

## Advanced Usage

### Hybrid Gates (L0 + Random)

```python
from l0 import HybridGate

# Combine L0 selection with random sampling
hybrid = HybridGate(
    n_items=10000,
    l0_fraction=0.25,      # 25% from L0
    random_fraction=0.75,  # 75% random
    target_items=1000
)

selected, indices, types = hybrid.select(data)
```

### Feature Selection

```python
from l0 import FeatureGate

# Select top features
gate = FeatureGate(n_features=1000, max_features=50)
selected_data, feature_indices = gate.select_features(data)

# Get feature importance
importance = gate.get_feature_importance()
```

## Mathematical Background

**L0 norm:**
- Counts non-zero elements
- Non-differentiable (discontinuous)
- Hard to optimize directly

**Hard Concrete relaxation:**
- Continuous, differentiable approximation
- Enables gradient descent
- "Stretches" binary distribution to allow gradients

**Paper:**
Louizos, Welling, & Kingma (2017): "Learning Sparse Neural Networks through L0 Regularization"
https://arxiv.org/abs/1712.01312

## Related Packages

**Uses L0:**
- microcalibrate (survey weight calibration)
- policyengine-us-data (household selection)

**See also:**
- **microcalibrate-skill** - Survey calibration using L0
- **policyengine-us-data-skill** - Data pipeline integration

## Resources

**Repository:** https://github.com/PolicyEngine/L0
**Documentation:** https://policyengine.github.io/L0/
**Paper:** https://arxiv.org/abs/1712.01312
**PyPI:** https://pypi.org/project/l0-python/
