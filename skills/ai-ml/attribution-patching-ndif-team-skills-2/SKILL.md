---
name: attribution-patching
description: Gradient-based approximation to activation patching for scalable circuit analysis. Use when activation patching is too slow or when analyzing many components simultaneously.
---

# Attribution Patching

Attribution patching uses gradients to approximate activation patching results in a single backward pass, making it practical to analyze thousands of components simultaneously.

## Core Idea

Instead of running separate forward passes for each component:

1. Run clean and corrupted forward passes
2. Compute gradients of the metric w.r.t. corrupted activations
3. Multiply gradients by (clean - corrupted) activation differences

This linear approximation works when clean and corrupted runs are similar.

## Mathematical Formula

```
attribution(component) = grad_corrupted(metric) * (clean_activation - corrupted_activation)
```

## Setup

```python
from nnsight import LanguageModel
import torch

model = LanguageModel("openai-community/gpt2", device_map="auto", dispatch=True)

clean_prompt = "After John and Mary went to the store, Mary gave a bottle of milk to"
corrupted_prompt = "After John and Mary went to the store, John gave a bottle of milk to"

correct_token = model.tokenizer(" John")["input_ids"][0]
incorrect_token = model.tokenizer(" Mary")["input_ids"][0]

def logit_diff(logits):
    return logits[0, -1, correct_token] - logits[0, -1, incorrect_token]
```

## Basic Attribution Patching

```python
n_layers = len(model.transformer.h)

clean_acts = []
corrupted_acts = []
corrupted_grads = []

# Clean forward pass - save activations
with model.trace(clean_prompt):
    for layer in model.transformer.h:
        act = layer.output[0]
        clean_acts.append(act.save())

# Corrupted forward + backward pass
with model.trace(corrupted_prompt):
    # Register intermediate values in forward order
    for layer in model.transformer.h:
        act = layer.output[0]
        act.requires_grad = True
        corrupted_acts.append(act.save())

    # Compute metric
    logits = model.lm_head.output
    metric = logit_diff(logits)

    # Access gradients in REVERSE order within backward context
    with metric.backward():
        for layer in reversed(model.transformer.h):
            corrupted_grads.insert(0, layer.output[0].grad.save())

# Compute attributions
attributions = []
for i in range(n_layers):
    clean = clean_acts[i].value
    corrupted = corrupted_acts[i].value
    grad = corrupted_grads[i].value

    # Attribution = grad * (clean - corrupted)
    attr = (grad * (clean - corrupted)).sum()
    attributions.append(attr.item())

attributions = torch.tensor(attributions)
```

## Per-Position Attribution

```python
seq_len = clean_acts[0].value.shape[1]
position_attrs = torch.zeros(n_layers, seq_len)

for layer_idx in range(n_layers):
    clean = clean_acts[layer_idx].value
    corrupted = corrupted_acts[layer_idx].value
    grad = corrupted_grads[layer_idx].value

    # Sum over hidden dimension only, keep position
    diff = clean - corrupted
    attr = (grad * diff).sum(dim=-1).squeeze()  # [seq_len]
    position_attrs[layer_idx] = attr
```

## Attention Head Attribution

```python
from einops import rearrange

n_heads = model.config.n_head
head_dim = model.config.n_embd // n_heads
head_attrs = torch.zeros(n_layers, n_heads)

# Collect clean attention outputs
clean_attn = []
with model.trace(clean_prompt):
    for layer in model.transformer.h:
        attn_out = layer.attn.c_proj.input[0][0]  # Before projection
        clean_attn.append(attn_out.save())

# Collect corrupted attention outputs and gradients
corrupted_attn = []
attn_grads = []

with model.trace(corrupted_prompt):
    # Register intermediate values in forward order
    for layer in model.transformer.h:
        attn_out = layer.attn.c_proj.input[0][0]
        attn_out.requires_grad = True
        corrupted_attn.append(attn_out.save())

    metric = logit_diff(model.lm_head.output)

    # Access gradients in REVERSE order within backward context
    with metric.backward():
        for layer in reversed(model.transformer.h):
            attn_grads.insert(0, layer.attn.c_proj.input[0][0].grad.save())

# Compute per-head attributions
for layer_idx in range(n_layers):
    clean = clean_attn[layer_idx].value
    corrupted = corrupted_attn[layer_idx].value
    grad = attn_grads[layer_idx].value

    # Reshape to [batch, seq, heads, head_dim]
    clean_heads = rearrange(clean, 'b s (h d) -> b s h d', h=n_heads)
    corrupted_heads = rearrange(corrupted, 'b s (h d) -> b s h d', h=n_heads)
    grad_heads = rearrange(grad, 'b s (h d) -> b s h d', h=n_heads)

    # Attribution per head
    diff = clean_heads - corrupted_heads
    attr = (grad_heads * diff).sum(dim=(0, 1, 3))  # Sum batch, seq, head_dim
    head_attrs[layer_idx] = attr
```

## Efficient Batched Version

Process both prompts in a single forward pass using batching:

```python
# Batch both prompts together in a single trace
all_acts = []
all_grads = []

with model.trace([clean_prompt, corrupted_prompt]):
    # Register intermediate values in forward order
    for layer in model.transformer.h:
        act = layer.output[0]
        act.requires_grad = True
        all_acts.append(act.save())

    logits = model.lm_head.output
    # Metric on corrupted (index 1)
    metric = logit_diff(logits[1:2])

    # Access gradients in REVERSE order within backward context
    with metric.backward():
        for layer in reversed(model.transformer.h):
            all_grads.insert(0, layer.output[0].grad.save())

# Split clean/corrupted and compute attributions
attributions = []
for i in range(n_layers):
    acts = all_acts[i].value
    grads = all_grads[i].value

    clean = acts[0:1]
    corrupted = acts[1:2]
    grad = grads[1:2]  # Gradient is only for corrupted

    attr = (grad * (clean - corrupted)).sum()
    attributions.append(attr.item())
```

## Comparison with Activation Patching

| Aspect | Activation Patching | Attribution Patching |
| ------ | ------------------- | -------------------- |
| Accuracy | Exact | Approximation |
| Speed | O(n_components) forwards | O(1) forward + backward |
| Memory | Lower per run | Higher (stores grads) |
| Best for | Few components | Many components |

## Validation

Compare attribution results against ground truth patching:

```python
# Scatter plot: attribution vs actual patching effect
import matplotlib.pyplot as plt

plt.scatter(attributions, actual_patching_results)
plt.xlabel("Attribution Score")
plt.ylabel("Actual Patching Effect")
plt.title("Attribution vs Patching Correlation")
correlation = torch.corrcoef(torch.stack([attributions, actual_patching_results]))[0, 1]
plt.text(0.1, 0.9, f"r = {correlation:.3f}", transform=plt.gca().transAxes)
```

## When to Use

- **Use attribution patching**: Initial exploration, many components, large models
- **Use activation patching**: Validating specific components, exact measurements needed
- **Combine both**: Attribution for screening, patching for confirmation
