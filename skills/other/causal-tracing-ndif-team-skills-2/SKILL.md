---
name: causal-tracing
description: Causal mediation analysis to identify which model components mediate specific behaviors. Use when investigating how information flows through the network and which neurons or layers are causally responsible for outputs.
---

# Causal Tracing

Causal tracing (causal mediation analysis) identifies which intermediate computations causally mediate the relationship between inputs and outputs. It reveals not just what correlates with behavior, but what causes it.

## Core Concepts

### Three Types of Causal Effects

1. **Total Effect**: Change in output when modifying input
2. **Direct Effect**: Effect of restoring a component from clean to corrupted run
3. **Indirect Effect**: Effect of corrupting a component in an otherwise clean run

### The Interchange Intervention

Swap activations between two runs to test causal relationships:

- **Source run**: Produces the activation value
- **Base run**: Receives the swapped activation

## Setup

```python
from nnsight import LanguageModel
import torch

model = LanguageModel("openai-community/gpt2", device_map="auto", dispatch=True)

# Factual recall task
base_prompt = "The Eiffel Tower is located in"    # Expects: Paris
source_prompt = "The Colosseum is located in"      # Expects: Rome

# Get target tokens
paris_token = model.tokenizer(" Paris")["input_ids"][0]
rome_token = model.tokenizer(" Rome")["input_ids"][0]
```

## Computing Total Effect

```python
with model.trace() as tracer:
    with tracer.invoke(base_prompt):
        base_logits = model.lm_head.output.save()

    with tracer.invoke(source_prompt):
        source_logits = model.lm_head.output.save()

base_prob = torch.softmax(base_logits.value[0, -1], dim=-1)[paris_token]
source_prob = torch.softmax(source_logits.value[0, -1], dim=-1)[rome_token]

total_effect = base_prob - source_prob  # How much does changing input change output?
```

## Direct Effect (Restoration)

Does restoring a component from source restore source behavior?

```python
n_layers = len(model.transformer.h)
direct_effects = torch.zeros(n_layers)

# Get source activations
with model.trace(source_prompt):
    source_hiddens = [layer.output[0].save() for layer in model.transformer.h]

# Patch each layer: run base, inject source activation
for layer_idx in range(n_layers):
    with model.trace(base_prompt):
        model.transformer.h[layer_idx].output[0][:] = source_hiddens[layer_idx]
        patched_logits = model.lm_head.output.save()

    prob = torch.softmax(patched_logits.value[0, -1], dim=-1)[rome_token]
    direct_effects[layer_idx] = prob.item()
```

## Indirect Effect (Corruption)

Does corrupting a component in source disrupt source behavior?

```python
indirect_effects = torch.zeros(n_layers)

# Get base activations (for corruption)
with model.trace(base_prompt):
    base_hiddens = [layer.output[0].save() for layer in model.transformer.h]

# For each layer: run source, inject base (corrupted) activation
for layer_idx in range(n_layers):
    with model.trace(source_prompt):
        model.transformer.h[layer_idx].output[0][:] = base_hiddens[layer_idx]
        corrupted_logits = model.lm_head.output.save()

    prob = torch.softmax(corrupted_logits.value[0, -1], dim=-1)[rome_token]
    indirect_effects[layer_idx] = source_prob - prob.item()  # Drop from source baseline
```

## Position-Specific Causal Tracing

Identify which token positions carry causal information:

```python
seq_len = len(model.tokenizer.encode(source_prompt))
position_effects = torch.zeros(n_layers, seq_len)

# Get source activations
with model.trace(source_prompt):
    source_hiddens = [layer.output[0].save() for layer in model.transformer.h]

# Patch each layer x position
for layer_idx in range(n_layers):
    for pos_idx in range(seq_len):
        with model.trace(base_prompt):
            # Only patch this specific position
            model.transformer.h[layer_idx].output[0][:, pos_idx, :] = \
                source_hiddens[layer_idx][:, pos_idx, :]
            patched_logits = model.lm_head.output.save()

        prob = torch.softmax(patched_logits.value[0, -1], dim=-1)[rome_token]
        position_effects[layer_idx, pos_idx] = prob.item()
```

## Noising-Based Causal Tracing

Add noise to corrupt, then restore specific components:

```python
def add_noise(activation, noise_level=0.1):
    return activation + noise_level * torch.randn_like(activation)

window_size = 3  # Restore window of layers around target
restoration_effects = torch.zeros(n_layers)

# Clean run - save activations
with model.trace(source_prompt):
    clean_hiddens = [layer.output[0].save() for layer in model.transformer.h]

# For each layer: noise everything, restore window around this layer
for center_layer in range(n_layers):
    with model.trace(source_prompt):
        for layer_idx, layer in enumerate(model.transformer.h):
            if abs(layer_idx - center_layer) <= window_size // 2:
                # Restore clean
                layer.output[0][:] = clean_hiddens[layer_idx]
            else:
                # Add noise
                layer.output[0][:] = add_noise(layer.output[0])

        restored_logits = model.lm_head.output.save()

    prob = torch.softmax(restored_logits.value[0, -1], dim=-1)[rome_token]
    restoration_effects[center_layer] = prob.item()
```

## MLP vs Attention Decomposition

Separate contributions of MLP and attention:

```python
mlp_effects = torch.zeros(n_layers)
attn_effects = torch.zeros(n_layers)

# Get source MLP and attention outputs
with model.trace(source_prompt):
    source_mlp = [layer.mlp.output[0].save() for layer in model.transformer.h]
    source_attn = [layer.attn.output[0].save() for layer in model.transformer.h]

# Test MLP contributions
for layer_idx in range(n_layers):
    with model.trace(base_prompt):
        model.transformer.h[layer_idx].mlp.output[0][:] = source_mlp[layer_idx]
        mlp_logits = model.lm_head.output.save()
    mlp_effects[layer_idx] = torch.softmax(mlp_logits.value[0, -1], dim=-1)[rome_token]

# Test attention contributions
for layer_idx in range(n_layers):
    with model.trace(base_prompt):
        model.transformer.h[layer_idx].attn.output[0][:] = source_attn[layer_idx]
        attn_logits = model.lm_head.output.save()
    attn_effects[layer_idx] = torch.softmax(attn_logits.value[0, -1], dim=-1)[rome_token]
```

## Visualization

```python
import matplotlib.pyplot as plt
import seaborn as sns

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Layer-wise effects
axes[0].bar(range(n_layers), direct_effects, alpha=0.7, label='Direct')
axes[0].bar(range(n_layers), indirect_effects, alpha=0.7, label='Indirect')
axes[0].set_xlabel('Layer')
axes[0].set_ylabel('Causal Effect')
axes[0].legend()
axes[0].set_title('Causal Effects by Layer')

# Position x Layer heatmap
input_tokens = model.tokenizer.encode(source_prompt)
token_labels = [model.tokenizer.decode(t) for t in input_tokens]

sns.heatmap(
    position_effects.numpy(),
    ax=axes[1],
    xticklabels=token_labels,
    yticklabels=[f'L{i}' for i in range(n_layers)],
    cmap='viridis'
)
axes[1].set_title('Causal Effect by Position and Layer')
axes[1].set_xlabel('Token Position')
axes[1].set_ylabel('Layer')

plt.tight_layout()
```

## Interpretation Guidelines

- **Early layers + subject position**: Often store entity information
- **Middle layers + last subject token**: Information extraction/lookup
- **Late layers + final position**: Prediction formation
- **High indirect effect**: Component is necessary for behavior
- **High direct effect**: Component is sufficient to cause behavior
