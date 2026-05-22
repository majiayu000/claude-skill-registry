---
name: activation-patching
description: Causal intervention via activation patching to identify important model components. Use when determining which layers, heads, or positions are causally responsible for model behavior.
---

# Activation Patching

Activation patching is a causal intervention technique that identifies which model components are responsible for specific behaviors by swapping activations between different inputs.

## Core Concept

1. **Clean run**: Run model on prompt that produces desired behavior
2. **Corrupted run**: Run on modified prompt that changes the behavior
3. **Patch**: Replace corrupted activations with clean ones, measure if behavior is restored

If patching a component restores the clean behavior, that component is causally important.

## Basic Setup

```python
from nnsight import LanguageModel
import torch

model = LanguageModel("openai-community/gpt2", device_map="auto", dispatch=True)

# Indirect Object Identification (IOI) task
clean_prompt = "After John and Mary went to the store, Mary gave a bottle of milk to"
corrupted_prompt = "After John and Mary went to the store, John gave a bottle of milk to"

# Target tokens
correct_token = model.tokenizer(" John")["input_ids"][0]   # Clean answer
incorrect_token = model.tokenizer(" Mary")["input_ids"][0]  # Corrupted answer
```

## Metric: Logit Difference

```python
def logit_diff(logits, correct_idx, incorrect_idx):
    """Measure how much model prefers correct over incorrect token."""
    return (logits[0, -1, correct_idx] - logits[0, -1, incorrect_idx]).item()
```

## Three-Run Patching Pattern

```python
n_layers = len(model.transformer.h)
results = torch.zeros(n_layers)

# Run 1: Clean - save activations
with model.trace(clean_prompt):
    clean_hiddens = [layer.output[0].save() for layer in model.transformer.h]
    clean_logits = model.lm_head.output.save()

# Run 2: Corrupted baseline
with model.trace(corrupted_prompt):
    corrupted_logits = model.lm_head.output.save()

# Runs 3+: Patch each layer (separate forward passes)
for layer_idx in range(n_layers):
    with model.trace(corrupted_prompt):
        # Replace corrupted activation with clean
        model.transformer.h[layer_idx].output[0][:] = clean_hiddens[layer_idx]
        patched_logits = model.lm_head.output.save()
    results[layer_idx] = logit_diff(patched_logits.value, correct_token, incorrect_token)

# Normalize results
clean_diff = logit_diff(clean_logits.value, correct_token, incorrect_token)
corrupted_diff = logit_diff(corrupted_logits.value, correct_token, incorrect_token)
normalized = (results - corrupted_diff) / (clean_diff - corrupted_diff)
```

## Position-Specific Patching

Patch only specific token positions:

```python
seq_len = len(model.tokenizer.encode(clean_prompt))
results = torch.zeros(n_layers, seq_len)

# Clean run - save activations
with model.trace(clean_prompt):
    clean_hiddens = [layer.output[0].save() for layer in model.transformer.h]

# Patch each layer x position (separate forward passes)
for layer_idx in range(n_layers):
    for pos_idx in range(seq_len):
        with model.trace(corrupted_prompt):
            # Patch only this position
            model.transformer.h[layer_idx].output[0][:, pos_idx, :] = \
                clean_hiddens[layer_idx][:, pos_idx, :]
            patched_logits = model.lm_head.output.save()
        results[layer_idx, pos_idx] = logit_diff(
            patched_logits.value, correct_token, incorrect_token
        )
```

## Attention Head Patching

Patch individual attention heads:

```python
n_heads = model.config.n_head
head_dim = model.config.n_embd // n_heads
results = torch.zeros(n_layers, n_heads)

# Clean run - save attention outputs (before projection)
with model.trace(clean_prompt):
    clean_attn = [layer.attn.c_proj.input[0][0].save()
                  for layer in model.transformer.h]

# Patch each layer x head (separate forward passes)
for layer_idx in range(n_layers):
    for head_idx in range(n_heads):
        with model.trace(corrupted_prompt):
            # Patch single head's output
            start = head_idx * head_dim
            end = (head_idx + 1) * head_dim
            model.transformer.h[layer_idx].attn.c_proj.input[0][0][:, :, start:end] = \
                clean_attn[layer_idx][:, :, start:end]
            patched_logits = model.lm_head.output.save()
        results[layer_idx, head_idx] = logit_diff(
            patched_logits.value, correct_token, incorrect_token
        )
```

## Noising (Reverse Patching)

Instead of restoring clean activations, corrupt clean activations:

```python
# Corrupted run - save activations
with model.trace(corrupted_prompt):
    corrupted_hiddens = [layer.output[0].save() for layer in model.transformer.h]

# For each layer, inject corrupted activation into clean run
noising_results = torch.zeros(n_layers)
for layer_idx in range(n_layers):
    with model.trace(clean_prompt):
        # Inject corrupted activation into clean run
        model.transformer.h[layer_idx].output[0][:] = corrupted_hiddens[layer_idx]
        noised_logits = model.lm_head.output.save()
    noising_results[layer_idx] = logit_diff(noised_logits.value, correct_token, incorrect_token)
```

## Visualization

```python
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(12, 8))
sns.heatmap(
    results.numpy(),
    xticklabels=[f"Pos {i}" for i in range(seq_len)],
    yticklabels=[f"Layer {i}" for i in range(n_layers)],
    cmap="RdBu_r",
    center=0,
    annot=True,
    fmt=".2f"
)
plt.title("Activation Patching Results")
plt.xlabel("Token Position")
plt.ylabel("Layer")
plt.tight_layout()
plt.show()
```

## Interpretation

- **High positive values**: Component is important for correct behavior
- **Values near 0**: Component doesn't affect this behavior
- **Negative values**: Component actively pushes toward wrong answer
- **Clusters of importance**: Suggest circuits or computational stages
