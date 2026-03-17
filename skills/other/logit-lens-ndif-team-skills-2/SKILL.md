---
name: logit-lens
description: Decode intermediate layer predictions using the Logit Lens technique. Use when analyzing what a model predicts at each layer, understanding information flow, or visualizing layer-wise processing.
---

# Logit Lens

Logit Lens decodes intermediate layer activations into vocabulary predictions, revealing what the model "thinks" at each processing step rather than just the final output.

## Concept

Transformer language models build predictions incrementally across layers. By applying the final layer norm and unembedding head to intermediate hidden states, we can see evolving predictions.

## Basic Implementation

```python
from nnsight import LanguageModel
import torch

model = LanguageModel("openai-community/gpt2", device_map="auto", dispatch=True)

prompt = "The Eiffel Tower is in the city of"
layers = model.transformer.h
probs_layers = []

with model.trace(prompt):
    for layer_idx, layer in enumerate(layers):
        # Get layer output, apply final layer norm, then lm_head
        hidden = layer.output[0]
        normed = model.transformer.ln_f(hidden)
        logits = model.lm_head(normed)

        # Convert to probabilities
        probs = torch.nn.functional.softmax(logits, dim=-1).save()
        probs_layers.append(probs)
```

## Extract Top Predictions

```python
# Stack all layer probabilities
all_probs = torch.stack([p.value for p in probs_layers])  # [n_layers, batch, seq, vocab]

# Get top prediction at each layer for final token
final_token_probs = all_probs[:, 0, -1, :]  # [n_layers, vocab]
top_probs, top_tokens = final_token_probs.max(dim=-1)

# Decode predictions
for layer_idx, (prob, token) in enumerate(zip(top_probs, top_tokens)):
    word = model.tokenizer.decode(token.item())
    print(f"Layer {layer_idx}: '{word}' (prob: {prob:.3f})")
```

## Full Sequence Visualization

```python
import numpy as np

# Get predictions for all positions
max_probs, tokens = all_probs[:, 0, :, :].max(dim=-1)  # [n_layers, seq_len]

# Decode to words
words = [[model.tokenizer.decode(t.item()) for t in layer_tokens]
         for layer_tokens in tokens]

# Create visualization matrix
input_tokens = model.tokenizer.encode(prompt)
input_words = [model.tokenizer.decode(t) for t in input_tokens]

print("Position:", input_words)
for layer_idx, layer_words in enumerate(words):
    print(f"Layer {layer_idx:2d}:", layer_words)
```

## Efficient Batched Version

For analyzing multiple prompts or comparing behaviors:

```python
prompts = [
    "The capital of France is",
    "The capital of Germany is",
    "The capital of Japan is"
]

all_results = []

with model.trace() as tracer:
    for prompt in prompts:
        with tracer.invoke(prompt):
            prompt_probs = []
            for layer in model.transformer.h:
                hidden = layer.output[0]
                logits = model.lm_head(model.transformer.ln_f(hidden))
                probs = torch.nn.functional.softmax(logits[:, -1, :], dim=-1).save()
                prompt_probs.append(probs)
            all_results.append(prompt_probs)
```

## Remote Execution for Large Models

```python
from nnsight import CONFIG
CONFIG.set_default_api_key("YOUR_API_KEY")

model = LanguageModel("meta-llama/Llama-3.1-70B")

with model.trace("The meaning of life is", remote=True):
    layer_probs = []
    for layer in model.model.layers:
        hidden = layer.output[0]
        normed = model.model.norm(hidden)
        logits = model.lm_head(normed)
        probs = torch.nn.functional.softmax(logits[:, -1, :], dim=-1).save()
        layer_probs.append(probs)
```

## Interpretation Tips

- **Early layers**: Often predict generic/common tokens
- **Middle layers**: Begin forming task-relevant predictions
- **Late layers**: Converge to final prediction
- **Sudden changes**: May indicate important computation happening at that layer
- **Persistent wrong predictions**: Suggests information not yet integrated

## Visualization with Plotly

```python
import plotly.graph_objects as go

fig = go.Figure(data=go.Heatmap(
    z=max_probs.numpy(),
    x=input_words,
    y=[f"Layer {i}" for i in range(len(layers))],
    colorscale="Blues",
    text=words,
    texttemplate="%{text}",
    textfont={"size": 10},
))

fig.update_layout(
    title="Logit Lens: Layer-wise Predictions",
    xaxis_title="Input Position",
    yaxis_title="Layer"
)
fig.show()
```

## Use Cases

1. **Debugging model behavior**: See where predictions go wrong
2. **Understanding factual recall**: When does the model "know" the answer?
3. **Comparing model architectures**: Different models show different patterns
4. **Identifying critical layers**: Which layers matter most for a task?
