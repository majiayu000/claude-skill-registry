---
name: policyengine-data-testing
description: Testing patterns for PolicyEngine data generation pipelines (policyengine-us-data, policyengine-uk-data)
---

# PolicyEngine Data Testing Patterns

Testing patterns and optimization strategies for PolicyEngine data generation repositories.

## Quick Reference

### Test Mode Pattern
```python
import os

TESTING = os.environ.get("TESTING") == "1"

# Reduce expensive parameters in test mode
epochs = 32 if TESTING else 512
batch_size = 256 if TESTING else 1024
```

### CI Configuration
```yaml
# .github/workflows/test.yml
env:
  TESTING: 1  # Enable fast test mode
```

---

## 1. Test Mode Environment Variable

### Pattern

Data generation pipelines often involve expensive operations:
- Neural network training (calibration, imputation)
- Large-scale data processing
- Multiple iterations/epochs

For CI tests, use a `TESTING` environment variable to reduce runtime:

```python
import os

TESTING = os.environ.get("TESTING") == "1"

def create_dataset():
    # Use reduced parameters in test mode
    if TESTING:
        epochs = 32
        sample_size = 1000
        iterations = 10
    else:
        epochs = 512
        sample_size = 100000
        iterations = 100

    # Rest of implementation...
```

### Where to Apply

Use `TESTING` mode for:
- **Neural network training** - Reduce epochs from 512 to 32-64
- **Calibration iterations** - Reduce from 1000s to 100s
- **Sample sizes** - Use smaller representative samples
- **Data validation** - Check subset instead of full dataset

### Don't Use For

- **Data correctness logic** - Always validate fully
- **Critical calculations** - Never skip important steps
- **File I/O operations** - These are usually fast enough

---

## 2. CI/CD Configuration

### GitHub Actions

Set `TESTING=1` in workflow files:

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    env:
      TESTING: 1  # Enable fast test mode

    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -e .
      - name: Run tests
        run: make test
```

### Local Testing

Users can enable test mode locally:

```bash
# Fast test mode
TESTING=1 pytest

# Production mode (full training)
pytest
```

---

## 3. Common Data Pipeline Operations

### Neural Network Training

```python
import os
from microcalibrate import Calibrator

TESTING = os.environ.get("TESTING") == "1"

def calibrate_weights(data, targets):
    calibrator = Calibrator(
        data=data,
        targets=targets,
        epochs=32 if TESTING else 512,  # Reduce training time
        batch_size=256 if TESTING else 1024,
        learning_rate=0.01,
        early_stopping=True if TESTING else False  # Stop early in tests
    )

    return calibrator.fit()
```

### Data Imputation

```python
import os
from microimpute import Imputer

TESTING = os.environ.get("TESTING") == "1"

def impute_variables(data):
    imputer = Imputer(
        method="random_forest",
        n_estimators=10 if TESTING else 100,  # Fewer trees
        max_depth=5 if TESTING else 20,       # Shallower trees
        n_jobs=-1
    )

    return imputer.fit_transform(data)
```

### Sample Size Reduction

```python
import os
import pandas as pd

TESTING = os.environ.get("TESTING") == "1"

def load_and_process_data():
    data = pd.read_csv("raw_data.csv")

    if TESTING:
        # Use 1% sample for testing
        data = data.sample(frac=0.01, random_state=42)

    # Process full or sample data
    return process(data)
```

---

## 4. Runtime Impact Examples

### Before: 40+ minute CI tests
```python
# create_datasets.py
def create_enhanced_cps():
    # Always use 512 epochs
    calibrate_weights(data, targets, epochs=512)
    # CI timeout issues, slow feedback
```

### After: 5-10 minute CI tests
```python
# create_datasets.py
import os

TESTING = os.environ.get("TESTING") == "1"

def create_enhanced_cps():
    epochs = 32 if TESTING else 512
    calibrate_weights(data, targets, epochs=epochs)
    # Fast CI, quick feedback, full training in production
```

### Typical Time Savings

| Operation | Production | Test Mode | Savings |
|-----------|-----------|-----------|---------|
| Calibration (512 epochs) | 30 min | 2 min | 93% |
| Imputation (100 trees) | 10 min | 1 min | 90% |
| Full pipeline | 45 min | 5 min | 89% |

---

## 5. Best Practices

### Do's ✅

- ✅ **Use for expensive operations** - Training, large-scale processing
- ✅ **Document the difference** - Comment what changes in test mode
- ✅ **Keep logic identical** - Only change hyperparameters, not algorithms
- ✅ **Set in CI configuration** - Always enable for automated tests
- ✅ **Make it optional** - Default to production mode if not set

### Don'ts ❌

- ❌ **Skip validation** - Always validate correctness
- ❌ **Change algorithms** - Same method, different scale
- ❌ **Hide errors** - Test mode should catch real issues
- ❌ **Make tests meaningless** - Keep tests representative
- ❌ **Forget documentation** - Explain the pattern in README

---

## 6. Example: Complete Implementation

### create_datasets.py

```python
"""
Enhanced dataset creation pipeline.

Set TESTING=1 to use reduced parameters for faster CI tests.
"""
import os
from pathlib import Path
from microcalibrate import Calibrator
from microimpute import Imputer

# Detect test mode
TESTING = os.environ.get("TESTING") == "1"

# Configure parameters based on mode
CONFIG = {
    "epochs": 32 if TESTING else 512,
    "batch_size": 256 if TESTING else 1024,
    "n_trees": 10 if TESTING else 100,
    "sample_frac": 0.01 if TESTING else 1.0,
}

if TESTING:
    print("Running in TESTING mode with reduced parameters")
    print(f"Config: {CONFIG}")


def create_enhanced_dataset():
    """Create enhanced dataset with imputation and calibration."""

    # Load data
    data = load_raw_data()

    # Sample if in test mode
    if TESTING:
        data = data.sample(frac=CONFIG["sample_frac"], random_state=42)

    # Impute missing values
    imputer = Imputer(
        method="random_forest",
        n_estimators=CONFIG["n_trees"],
        n_jobs=-1
    )
    data = imputer.fit_transform(data)

    # Calibrate weights to targets
    calibrator = Calibrator(
        data=data,
        targets=load_targets(),
        epochs=CONFIG["epochs"],
        batch_size=CONFIG["batch_size"],
    )
    data = calibrator.fit_transform(data)

    # Save results
    save_dataset(data)

    return data


if __name__ == "__main__":
    create_enhanced_dataset()
```

### .github/workflows/test.yml

```yaml
name: Test Data Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    env:
      TESTING: 1  # Enable fast test mode for CI

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -e .
          pip install pytest pytest-cov

      - name: Run data pipeline tests
        run: |
          python create_datasets.py
          pytest tests/
```

### README.md Addition

```markdown
## Testing

The data pipeline supports a fast test mode for CI:

```bash
# Fast test mode (reduced epochs, smaller samples)
TESTING=1 python create_datasets.py

# Production mode (full training)
python create_datasets.py
```

In test mode:
- Epochs reduced from 512 to 32
- Sample size reduced to 1%
- Tree count reduced from 100 to 10
- Runtime: ~5 minutes vs ~45 minutes
```

---

## 7. Repository-Specific Notes

### policyengine-us-data

- Primary bottleneck: CPS calibration with neural networks
- Test mode reduces 512 epochs → 32 epochs
- Savings: ~40 minutes → ~5 minutes in CI

### policyengine-uk-data

- Primary bottleneck: FRS data processing and calibration
- Apply same pattern for neural network training
- Consider sample size reduction for large datasets

---

## 8. When to Use This Pattern

### Use When

- Repository has data generation scripts
- CI tests take >10 minutes
- Pipeline includes ML training (calibration, imputation)
- Tests timeout or are too slow for rapid iteration

### Don't Use When

- Tests already run quickly (<5 minutes)
- No expensive operations (just file I/O)
- Correctness depends on full-scale processing
- Repository is not a data pipeline

---

## For Agents

When working on `policyengine-*-data` repositories:

1. **Check for slow CI** - Look at workflow run times
2. **Identify bottlenecks** - Usually neural network training
3. **Add TESTING variable** - Check `os.environ.get("TESTING") == "1"`
4. **Reduce expensive parameters** - Epochs, trees, sample sizes
5. **Update CI config** - Set `TESTING: 1` in workflow env
6. **Document the change** - Explain in comments and README
7. **Test both modes** - Verify test mode catches real issues
