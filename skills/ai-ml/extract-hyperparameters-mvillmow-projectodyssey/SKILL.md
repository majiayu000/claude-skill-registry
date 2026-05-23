---
name: extract-hyperparameters
description: "Identify and document model hyperparameters from papers. Use when setting up training configurations."
mcp_fallback: none
category: analysis
tier: 2
user-invocable: false
---

# Extract Hyperparameters

Locate and document all hyperparameters mentioned in research papers including learning rates, batch sizes, and model configurations.

## When to Use

- Reproducing paper results
- Setting up model training configurations
- Comparing hyperparameter choices across papers
- Planning hyperparameter tuning experiments

## Quick Reference

```bash
# Extract numeric values and parameters from papers
pdftotext paper.pdf - | grep -i "learning rate\|batch\|epochs\|weight decay\|dropout" | head -20

# Common pattern search
grep -E "\\b(lr|batch_size|epochs|momentum|dropout|layers)\\s*[=:]" config.py
```

## Workflow

1. **Find hyperparameter table**: Look for "Table 1" or "Hyperparameters" section
2. **Document architecture parameters**: Layer sizes, activation functions, normalization
3. **Extract training parameters**: Learning rate, batch size, epochs, optimizers
4. **Note regularization**: Dropout, weight decay, batch normalization
5. **Create configuration file**: Translate to implementation format (YAML/JSON/Mojo)

## Output Format

Hyperparameter documentation:

- Model architecture (layers, sizes, activations)
- Training parameters (LR, batch size, epochs)
- Optimizer configuration (type, momentum, decay)
- Regularization settings (dropout, L1/L2)
- Data preprocessing (normalization, augmentation)
- Hardware and precision (float32, float64)

## References

- See `prepare-dataset` skill for data configuration
- See `train-model` skill for training implementation
- See `/notes/review/mojo-ml-patterns.md` for Mojo configuration patterns
