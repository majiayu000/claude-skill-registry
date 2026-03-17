---
name: model-steering
description: Control model behavior through persistent edits and steering interventions. Use when modifying model outputs, applying steering vectors, or creating persistently modified model versions.
---

# Model Steering

Model steering manipulates model activations to control outputs without retraining. This includes one-off interventions, persistent edits, and steering vector techniques.

## Basic Steering Intervention

Modify activations during a single forward pass:

```python
from nnsight import LanguageModel
import torch

model = LanguageModel("openai-community/gpt2", device_map="auto", dispatch=True)

# Add a steering vector to layer 10
steering_vector = torch.randn(768)  # Match hidden dimension

with model.trace("I think the movie was") as tracer:
    # Add steering vector to residual stream
    model.transformer.h[10].output[0][:, -1, :] += steering_vector
    steered_logits = model.lm_head.output.save()
```

## Computing Steering Vectors

### Contrastive Activation Difference

```python
positive_prompts = [
    "I love this! It's fantastic",
    "This is wonderful and amazing",
    "I'm so happy about this"
]
negative_prompts = [
    "I hate this! It's terrible",
    "This is awful and horrible",
    "I'm so sad about this"
]

layer_idx = 10
positive_acts = []
negative_acts = []

with model.trace() as tracer:
    for prompt in positive_prompts:
        with tracer.invoke(prompt):
            act = model.transformer.h[layer_idx].output[0][:, -1, :].save()
            positive_acts.append(act)

    for prompt in negative_prompts:
        with tracer.invoke(prompt):
            act = model.transformer.h[layer_idx].output[0][:, -1, :].save()
            negative_acts.append(act)

# Average difference = steering vector
pos_mean = torch.stack([a.value for a in positive_acts]).mean(dim=0)
neg_mean = torch.stack([a.value for a in negative_acts]).mean(dim=0)
steering_vector = pos_mean - neg_mean
```

### Applying the Steering Vector

```python
steering_strength = 1.5

with model.trace("The weather today is"):
    # Steer toward positive sentiment
    model.transformer.h[layer_idx].output[0][:, :, :] += steering_strength * steering_vector
    output = model.lm_head.output.save()

# Generate with steering (apply to all generation steps)
with model.generate("The weather today is", max_new_tokens=20) as tracer:
    with tracer.all():  # Apply intervention to every generation iteration
        model.transformer.h[layer_idx].output[0][:, -1, :] += steering_strength * steering_vector

    generated = model.generator.output.save()

print(model.tokenizer.decode(generated[0]))
```

## Persistent Model Editing

Create a modified model version that persists across traces:

```python
# Extract activations from a "source" prompt
with model.trace("The capital of France is Paris") as tracer:
    paris_hidden = model.transformer.h[-1].output[0].save()

# Create persistently edited model
with model.edit() as edited_model:
    model.transformer.h[-1].output[0][:] = paris_hidden.value

# Use edited model - will always output Paris-related content
with edited_model.trace("The capital of Germany is"):
    logits = model.lm_head.output.save()

# Can use edited model multiple times
with edited_model.trace("The capital of Japan is"):
    logits2 = model.lm_head.output.save()
```

## Ablation Studies

Zero out components to test necessity:

```python
# Zero ablation of attention head
head_idx = 5
head_dim = model.config.n_embd // model.config.n_head
start = head_idx * head_dim
end = (head_idx + 1) * head_dim

with model.trace(prompt):
    # Zero this head's contribution
    attn_out = model.transformer.h[10].attn.c_proj.input[0][0]
    attn_out[:, :, start:end] = 0
    ablated_logits = model.lm_head.output.save()
```

### Mean Ablation

Replace with mean activation (less disruptive):

```python
# First compute mean activation over many prompts
mean_acts = []
with model.trace() as tracer:
    for prompt in calibration_prompts:
        with tracer.invoke(prompt):
            act = model.transformer.h[10].output[0].save()
            mean_acts.append(act)

mean_activation = torch.stack([a.value for a in mean_acts]).mean(dim=0)

# Apply mean ablation
with model.trace(test_prompt):
    model.transformer.h[10].output[0][:] = mean_activation
    ablated_logits = model.lm_head.output.save()
```

## Activation Addition (ActAdd)

Add vectors at inference time without modifying weights:

```python
def actadd_generate(model, prompt, steering_vector, layer, strength=1.0, max_tokens=50):
    with model.generate(prompt, max_new_tokens=max_tokens) as tracer:
        with tracer.all():  # Apply to all generation iterations
            model.transformer.h[layer].output[0][:, -1, :] += strength * steering_vector

        output = model.generator.output.save()

    return model.tokenizer.decode(output[0])
```

## Linear Probing for Steering

Train a probe to find steering directions:

```python
from sklearn.linear_model import LogisticRegression

# Collect activations with labels
activations = []
labels = []

with model.trace() as tracer:
    for prompt, label in labeled_data:
        with tracer.invoke(prompt):
            act = model.transformer.h[layer_idx].output[0][:, -1, :].save()
            activations.append(act)
            labels.append(label)

X = torch.stack([a.value.squeeze() for a in activations]).numpy()
y = labels

# Train probe
probe = LogisticRegression()
probe.fit(X, y)

# Use probe coefficients as steering vector
steering_direction = torch.tensor(probe.coef_[0])
```

## Multi-Layer Steering

Apply steering across multiple layers:

```python
layer_weights = {6: 0.5, 8: 1.0, 10: 1.5, 12: 1.0}  # Layer: strength

with model.generate(prompt, max_new_tokens=30) as tracer:
    with tracer.all():  # Apply to all generation iterations
        for layer_idx, strength in layer_weights.items():
            model.transformer.h[layer_idx].output[0][:, -1, :] += \
                strength * steering_vector

    generated = model.generator.output.save()

print(model.tokenizer.decode(generated[0]))
```

## Steering Vector Analysis

Interpret what your steering vector represents:

```python
# Project steering vector through unembedding
steering_logits = model.lm_head.weight @ steering_vector

# Top tokens affected
top_k = 20
top_values, top_indices = steering_logits.topk(top_k)
bottom_values, bottom_indices = steering_logits.topk(top_k, largest=False)

print("Tokens boosted by steering:")
for val, idx in zip(top_values, top_indices):
    print(f"  {model.tokenizer.decode(idx)}: {val:.3f}")

print("\nTokens suppressed by steering:")
for val, idx in zip(bottom_values, bottom_indices):
    print(f"  {model.tokenizer.decode(idx)}: {val:.3f}")
```

## Best Practices

1. **Layer selection**: Middle-to-late layers often work best
2. **Strength tuning**: Start small (0.1-0.5), increase gradually
3. **Validation**: Test on diverse prompts to avoid overfitting
4. **Orthogonalization**: Remove overlap with other behaviors
5. **Position**: Final token position usually most effective
