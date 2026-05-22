---
name: mlx-apple-silicon
description: Run LLMs on Apple Silicon with MLX/mlx_lm - unified memory, 4-bit quantization, streaming generation, prompt caching. Optimal for M-series chips.
version: 1.0.0
---


# MLX Apple Silicon Skill

> *"Unified memory means no GPU↔CPU transfers - arrays live in shared memory."*

**Trit**: +1 (PLUS - generative)
**Color**: Warm (optimistic/fast)

## Overview

[MLX](https://github.com/ml-explore/mlx) is Apple's ML framework for Apple Silicon:
- **Unified Memory**: No GPU↔CPU data transfers
- **Lazy Evaluation**: Compute only what's needed
- **Metal Backend**: Native GPU acceleration
- **4-bit Quantization**: 75% smaller models

[MLX-LM](https://github.com/ml-explore/mlx-lm) provides high-level LLM APIs.

## Quick Start

```bash
# Install (macOS Apple Silicon)
pip install mlx mlx-lm

# Install (Linux CUDA - v0.28+)
pip install "mlx[cuda]"

# Generate text
mlx_lm.generate --model mlx-community/Mistral-7B-Instruct-v0.3-4bit \
  --prompt "Hello" --max-tokens 100

# Interactive chat
mlx_lm.chat --model mlx-community/Mistral-7B-Instruct-v0.3-4bit

# Vision/Multimodal (mlx-vlm)
pip install mlx-vlm
mlx_vlm.chat --model mlx-community/Qwen2.5-VL-7B-Instruct-4bit
```

## Python API

### Basic Generation

```python
from mlx_lm import load, generate

# Load 4-bit quantized model
model, tokenizer = load("mlx-community/Mistral-7B-Instruct-v0.3-4bit")

# Generate
messages = [{"role": "user", "content": "Write a haiku"}]
prompt = tokenizer.apply_chat_template(messages, add_generation_prompt=True)
text = generate(model, tokenizer, prompt=prompt, max_tokens=100)
print(text)
```

### Streaming Generation

```python
from mlx_lm import load, stream_generate

model, tokenizer = load("mlx-community/Mistral-7B-Instruct-v0.3-4bit")

for response in stream_generate(model, tokenizer, prompt="Hello", max_tokens=100):
    print(response.text, end="", flush=True)
    # response.token, response.logprobs, response.generation_tps available
```

### Batch Generation

```python
from mlx_lm import load, batch_generate

model, tokenizer = load("mlx-community/Mistral-7B-Instruct-v0.3-4bit")

prompts = ["Story about AI", "Explain ML", "Write a poem"]
result = batch_generate(model, tokenizer, prompts, max_tokens=100)

for text in result.texts:
    print(text)
```

### Sampling Control

```python
from mlx_lm import load, generate
from mlx_lm.sample_utils import make_sampler

model, tokenizer = load("mlx-community/Mistral-7B-Instruct-v0.3-4bit")

sampler = make_sampler(
    temp=0.7,              # Temperature
    top_p=0.9,             # Nucleus sampling
    top_k=50,              # Top-k sampling
    min_p=0.05,            # Min probability threshold
    repetition_penalty=1.1
)

text = generate(model, tokenizer, prompt="Tell me a joke", sampler=sampler)
```

### Prompt Caching (Multi-turn)

```python
from mlx_lm import load, stream_generate
from mlx_lm.models.cache import make_prompt_cache, save_prompt_cache, load_prompt_cache

model, tokenizer = load("mlx-community/Mistral-7B-Instruct-v0.3-4bit")

# Create cache for system prompt + context
system = "You are an expert. " + long_context
cache = make_prompt_cache(model)

# Prime the cache
for r in stream_generate(model, tokenizer, system, prompt_cache=cache, max_tokens=1):
    break

# Save for reuse
save_prompt_cache("my_cache.safetensors", cache)

# Later: reuse with different queries
cache = load_prompt_cache("my_cache.safetensors")
for r in stream_generate(model, tokenizer, "What is 2+2?", prompt_cache=cache, max_tokens=50):
    print(r.text, end="", flush=True)
```

### KV Cache Rotation (Long Sequences)

```python
from mlx_lm import load, generate

model, tokenizer = load("mlx-community/Mistral-7B-Instruct-v0.3-4bit")

# Limit KV cache to 512 tokens (bounded memory for long sequences)
text = generate(
    model, tokenizer,
    prompt="Very long context...",
    max_kv_size=512,
    max_tokens=1000
)
```

### Speculative Decoding

```python
from mlx_lm import load, stream_generate

# Main model
model, tokenizer = load("mlx-community/Mistral-7B-Instruct-v0.3-4bit")
# Faster draft model
draft_model, _ = load("mlx-community/Mistral-3B-Instruct-4bit")

for r in stream_generate(
    model, tokenizer,
    prompt="Tell me about ML",
    draft_model=draft_model,
    num_draft_tokens=3,
    max_tokens=512
):
    print(r.text, end="", flush=True)
```

## Model Conversion & Quantization

```python
from mlx_lm import convert

# Download, quantize, and optionally upload
convert(
    hf_path="mistralai/Mistral-7B-Instruct-v0.3",
    mlx_path="./my-mistral-4bit",
    quantize=True,
    q_bits=4,           # 4-bit, 8-bit, or MXFP4/NVFP4
    q_group_size=64,
    dtype="float16",
    upload_repo="mlx-community/my-mistral-4bit"  # Optional
)
```

```bash
# CLI conversion
mlx_lm.convert --hf-path mistralai/Mistral-7B-Instruct-v0.3 \
  -q --upload-repo mlx-community/my-mistral-4bit
```

## LoRA/QLoRA Fine-Tuning

### LoRALinear Adapter

```python
import mlx.core as mx
import mlx.nn as nn

class LoRALinear(nn.Module):
    """Low-Rank Adaptation: W' = W + scale * (A @ B)"""
    def __init__(self, input_dims, output_dims, r=8, scale=20.0, dropout=0.0):
        self.linear = nn.Linear(input_dims, output_dims)
        self.dropout = nn.Dropout(p=dropout)
        self.scale = scale
        # A: (input, r), B: (r, output) - B zero-init for stable start
        self.lora_a = mx.random.uniform(low=-1/mx.sqrt(input_dims), 
                                         high=1/mx.sqrt(input_dims), 
                                         shape=(input_dims, r))
        self.lora_b = mx.zeros((r, output_dims))
    
    def __call__(self, x):
        y = self.linear(x)
        z = (self.dropout(x) @ self.lora_a) @ self.lora_b
        return y + (self.scale * z).astype(x.dtype)
```

### Training Loop with Gradient Accumulation

```python
from functools import partial
import mlx.optimizers as optim

# Freeze base, unfreeze LoRA layers
model.freeze()
for l in model.model.layers[-16:]:  # Last 16 layers
    l.self_attn.q_proj = LoRALinear.from_linear(l.self_attn.q_proj)
    l.self_attn.v_proj = LoRALinear.from_linear(l.self_attn.v_proj)

optimizer = optim.Adam(learning_rate=1e-5)

def loss_fn(model, inputs, targets, lengths):
    logits = model(inputs)
    mask = build_mask(lengths)
    ce = nn.losses.cross_entropy(logits, targets) * mask
    return ce.sum() / mask.sum()

loss_and_grad = nn.value_and_grad(model, loss_fn)

# Compiled step with gradient accumulation
@partial(mx.compile, inputs=model.state, outputs=model.state)
def step(batch, accumulated_grad, do_update, accum_steps):
    loss, grad = loss_and_grad(model, *batch)
    if accumulated_grad:
        grad = tree_map(lambda a, b: a + b, grad, accumulated_grad)
    if do_update:
        grad = tree_map(lambda g: g / accum_steps, grad)
        optimizer.update(model, grad)
        grad = None
    return loss, grad

# Gradient checkpointing for memory
mx.checkpoint(layer.__call__)  # Recompute activations in backward
```

### CLI Fine-Tuning

```bash
mlx_lm.lora --model mlx-community/Mistral-7B-Instruct-v0.3-4bit \
  --data ./train.jsonl --iters 1000 --batch-size 4 \
  --lora-layers 16 --lora-rank 8 --learning-rate 1e-5 \
  --adapter-path ./adapters
```

## Sampling Strategies

```python
from mlx_lm.sample_utils import make_sampler

# Temperature: higher = more random
# Top-K: keep top K tokens only
# Top-P (nucleus): keep tokens until cumsum(prob) > p
# Min-P: keep tokens with prob > top_prob * min_p
# Repetition penalty: discourage repeated tokens

sampler = make_sampler(
    temp=0.7,
    top_p=0.9,
    top_k=50,
    min_p=0.05,
    repetition_penalty=1.1,
    repetition_context_size=100
)

# Sampler internals:
# 1. Apply repetition penalty to seen tokens
# 2. Apply top-k filter (argpartition)
# 3. Apply min-p filter (relative to top logprob)
# 4. Apply top-p filter (cumulative threshold)
# 5. Sample with temperature: categorical(logits / temp)
```

## Generation Loop Internals

```python
# Prefill: process prompt in chunks
for i in range(0, len(prompt), prefill_step_size):
    chunk = prompt[i:i+prefill_step_size]
    _ = model(chunk, cache=cache)

# Decode: async token generation
stream = mx.new_stream(mx.default_device())
with mx.stream(stream):
    for _ in range(max_tokens):
        logits = model(tokens[None], cache=cache)[:, -1, :]
        logprobs = logits - mx.logsumexp(logits, keepdims=True)
        token = sampler(logprobs)
        mx.async_eval(token)
        yield token
```

## Speculative Decoding

```python
from mlx_lm import load, stream_generate

# Main model + faster draft model
model, tok = load("mlx-community/Mistral-7B-4bit")
draft, _ = load("mlx-community/Mistral-1B-4bit")

for r in stream_generate(
    model, tok, prompt="...",
    draft_model=draft,
    num_draft_tokens=4,  # Draft generates 4, main verifies
):
    print(r.text, end="")
# Pattern: draft → verify → accept prefix → rewind cache
```

## Supported Models

### Text Models (mlx-lm)
- **Llama** (2, 3, 3.2, 3.3)
- **Mistral** (v0.1-v0.3, Nemo)
- **Phi** (3, 3.5, 4)
- **Gemma** (2, 3)
- **Qwen** (2, 2.5, 3, Coder)
- **DeepSeek** (v2, v3, R1)
- **Mixtral** (MoE 8x7B, 8x22B)
- 100+ more on [mlx-community](https://huggingface.co/mlx-community)

### Vision/Multimodal (mlx-vlm)
- **Qwen-VL** (2, 2.5, 3)
- **LLaVA** (1.5, 1.6, NeXT, Interleave)
- **PaliGemma** (2)
- **Pixtral** (12B)
- **Molmo** (7B, 72B)
- **DeepSeek-VL** (v2)
- **Phi-3-Vision**, **Florence2**, **Idefics3**

```python
# Vision example
from mlx_vlm import load, generate
model, processor = load("mlx-community/Qwen2.5-VL-7B-Instruct-4bit")
output = generate(model, processor, "image.jpg", "Describe this image")
```

## Core MLX Concepts

### Unified Memory

```python
import mlx.core as mx

# Arrays live in shared memory - no GPU↔CPU transfers
a = mx.random.normal((1000, 1000))
b = mx.random.normal((1000, 1000))
c = mx.matmul(a, b)  # Automatic device selection, no data copy
```

### Lazy Evaluation

```python
import mlx.core as mx

a = mx.ones((1000, 1000))
b = mx.ones((1000, 1000))
c = mx.matmul(a, b)  # Not computed yet

mx.eval(c)  # Now computed
```

### Composable Transforms

```python
import mlx.core as mx

def loss_fn(w, x, y):
    return mx.mean((mx.matmul(x, w) - y) ** 2)

# Automatic differentiation
grad_fn = mx.grad(loss_fn)

# Vectorization
vmap_fn = mx.vmap(loss_fn)
```

## Performance

| Feature | Benefit |
|---------|---------|
| Unified Memory | No GPU↔CPU transfers |
| Metal Backend | Native M-series acceleration |
| CUDA Backend | Linux NVIDIA GPU support (v0.28+) |
| 4-bit Quantization | 75% smaller, fits on small Macs |
| MXFP4/NVFP4 | New microscaling formats (v0.29+) |
| Lazy Evaluation | Reduced memory footprint |
| Prompt Caching | Fast multi-turn dialogue |
| KV Rotation | Infinite context in bounded memory |
| Speculative Decoding | 2-3x faster with draft model |
| M5 Neural Accelerators | 3.5-4x TTFT speedup (v0.30+) |
| Wired Memory | Large models on macOS 15+ |
| mx.distributed | Multi-GPU training (NCCL) |

## GF(3) Triads

```
mlx-apple-silicon (+1) ⊗ unworld (0) ⊗ segal-types (-1) = 0 ✓
mlx-apple-silicon (+1) ⊗ gay-mcp (0) ⊗ temporal-coalgebra (-1) = 0 ✓
mlx-apple-silicon (+1) ⊗ rama-gay-clojure (0) ⊗ bisimulation-game (-1) = 0 ✓
```

## Commands

```bash
# Generate
mlx_lm.generate --model MODEL --prompt "..." --max-tokens N

# Chat
mlx_lm.chat --model MODEL

# Convert
mlx_lm.convert --hf-path HF_MODEL -q --mlx-path ./local

# Cache prompt
mlx_lm.cache_prompt --model MODEL --prompt "..." --prompt-cache-file cache.safetensors

# LoRA fine-tune
mlx_lm.lora --model MODEL --data ./data --output ./lora-adapters
```

## Integration with Gay.jl Coloring

```python
from mlx_lm import load, stream_generate

# Each generation step can be colored by trit
GOLDEN = 0x9E3779B97F4A7C15

def splitmix64(x):
    z = (x + GOLDEN) & 0xFFFFFFFFFFFFFFFF
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & 0xFFFFFFFFFFFFFFFF
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & 0xFFFFFFFFFFFFFFFF
    return (z ^ (z >> 31)) & 0xFFFFFFFFFFFFFFFF

def token_to_trit(token_id, seed):
    h = splitmix64(seed ^ token_id)
    return (h % 3) - 1  # {-1, 0, +1}

model, tokenizer = load("mlx-community/Mistral-7B-Instruct-v0.3-4bit")
seed = 0x42D

for i, r in enumerate(stream_generate(model, tokenizer, prompt="Hello", max_tokens=10)):
    trit = token_to_trit(r.token, seed + i)
    print(f"{r.text} [trit={trit:+d}]", end=" ")
```

## Model Architecture Internals (LLaMA)

### Attention with Grouped Query Attention (GQA)

```python
class Attention(nn.Module):
    def __init__(self, args):
        self.n_heads = args.num_attention_heads      # e.g., 32
        self.n_kv_heads = args.num_key_value_heads   # e.g., 8 (GQA compression)
        self.head_dim = args.hidden_size // self.n_heads
        self.scale = self.head_dim ** -0.5
        
        self.q_proj = nn.Linear(dim, self.n_heads * self.head_dim)
        self.k_proj = nn.Linear(dim, self.n_kv_heads * self.head_dim)
        self.v_proj = nn.Linear(dim, self.n_kv_heads * self.head_dim)
        self.o_proj = nn.Linear(self.n_heads * self.head_dim, dim)
        self.rope = initialize_rope(...)
    
    def __call__(self, x, mask=None, cache=None):
        B, L, D = x.shape
        q = self.q_proj(x).reshape(B, L, self.n_heads, -1).transpose(0, 2, 1, 3)
        k = self.k_proj(x).reshape(B, L, self.n_kv_heads, -1).transpose(0, 2, 1, 3)
        v = self.v_proj(x).reshape(B, L, self.n_kv_heads, -1).transpose(0, 2, 1, 3)
        
        # RoPE: Rotary Position Embeddings (θ_i = base^(-2i/d))
        q, k = self.rope(q, offset=cache.offset if cache else 0), self.rope(k, offset=cache.offset if cache else 0)
        
        if cache:
            k, v = cache.update_and_fetch(k, v)
        
        out = mx.fast.scaled_dot_product_attention(q, k, v, scale=self.scale, mask=mask)
        return self.o_proj(out.transpose(0, 2, 1, 3).reshape(B, L, -1))
```

### SwiGLU MLP

```python
class MLP(nn.Module):
    def __call__(self, x):
        # SwiGLU: Down(SiLU(Gate(x)) ⊙ Up(x))
        return self.down_proj(nn.silu(self.gate_proj(x)) * self.up_proj(x))
```

### TransformerBlock (Pre-Norm)

```python
class TransformerBlock(nn.Module):
    def __call__(self, x, mask=None, cache=None):
        h = x + self.self_attn(self.input_layernorm(x), mask, cache)
        return h + self.mlp(self.post_attention_layernorm(h))
```

## Automatic Differentiation

```python
import mlx.core as mx
import mlx.nn as nn
import mlx.optimizers as optim

def loss_fn(model, x, y):
    logits = model(x)
    return mx.mean(nn.losses.cross_entropy(logits, y))

# Value and gradient in one pass
loss_and_grad_fn = nn.value_and_grad(model, loss_fn)
loss, grads = loss_and_grad_fn(model, inputs, targets)

# Gradient clipping + optimizer step
grads = optim.clip_grad_norm(grads, max_norm=1.0)
optimizer.update(model, grads)
mx.eval(model.parameters(), optimizer.state)
```

### Gradient Flow Through Attention

```
∂L/∂values ← softmax_backward(attention_weights, ∂L/∂output)
∂L/∂scores ← attention_weights^T @ ∂L/∂output
∂L/∂keys   ← queries^T @ ∂L/∂scores  
∂L/∂queries ← ∂L/∂scores @ keys
# All fused in mx.fast.scaled_dot_product_attention backward
```

## RoPE Variants

| Variant | Context | Base θ Formula |
|---------|---------|----------------|
| Default | 4K-8K | `10000^(-2i/d)` |
| Llama3RoPE | 128K | Frequency interpolation + scaling |
| YarnRoPE | 64K+ | Smooth frequency scaling |
| SuScaledRoPE | 100K+ | Split short/long frequency scaling |

## KV Cache Strategies

```python
# Standard incremental cache
cache = KVCache()  # Pre-allocates in 256-token chunks

# Rotating cache for sliding window attention (Mistral, LLaMA 3.2)
cache = RotatingKVCache(max_size=4096, keep=4)  # keep=N attention sinks

# Prompt caching (reuse system prompt)
from mlx_lm.models.cache import make_prompt_cache, save_prompt_cache
cache = make_prompt_cache(model)
save_prompt_cache("system.safetensors", cache)
```

## Latent Space Topology

### Extracting Hidden States

```python
# Hook into transformer layers for latent analysis
def extract_activations(model, inputs):
    activations = []
    h = model.model.embed_tokens(inputs)
    for layer in model.model.layers:
        h = layer(h, mask=None, cache=None)
        activations.append(h.copy())  # Snapshot each layer
    return activations

# Analyze residual stream
residual_norms = [mx.linalg.norm(a, axis=-1).mean() for a in activations]
```

### Hyperbolic Distance (Beyond Euclid)

```python
def poincare_distance(u, v, eps=1e-5):
    """Hyperbolic distance in Poincaré ball model"""
    diff = u - v
    norm_u = mx.linalg.norm(u, axis=-1, keepdims=True)
    norm_v = mx.linalg.norm(v, axis=-1, keepdims=True)
    norm_diff = mx.linalg.norm(diff, axis=-1, keepdims=True)
    
    denom = (1 - norm_u**2) * (1 - norm_v**2) + eps
    return mx.arccosh(1 + 2 * norm_diff**2 / denom)

# For attention patterns: heads form hyperbolic tree structures
# Low curvature → flat Euclidean, High curvature → hierarchical
```

### Active Inference Integration

```python
def free_energy(model, x, prior_mean, prior_var):
    """Variational free energy for active inference"""
    # Prediction: forward pass gives expected sensory input
    pred = model(x)
    
    # Prediction error (likelihood)
    pred_error = mx.mean((pred - x) ** 2)
    
    # Complexity (KL divergence from prior)
    posterior = model.model.layers[-1].self_attn.rope  # Use RoPE as approximate posterior
    kl = 0.5 * mx.sum(posterior / prior_var + mx.log(prior_var) - 1)
    
    return pred_error + kl  # Minimize to update beliefs
```

## References

- [ml-explore/mlx](https://github.com/ml-explore/mlx) (23K★)
- [ml-explore/mlx-lm](https://github.com/ml-explore/mlx-lm) (3.1K★)
- [mlx-community on HuggingFace](https://huggingface.co/mlx-community)
- [MLX Documentation](https://ml-explore.github.io/mlx/)
- [LLaMA model implementation](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/models/llama.py)

---

**Skill Name**: mlx-apple-silicon
**Type**: LLM Inference / Apple Silicon / Autodiff
**Trit**: +1 (PLUS - generative)
**GF(3)**: Generates tokens deterministically
**Platform**: macOS with Apple Silicon
**Active Inference**: Supports latent space extraction + free energy minimization



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Autodiff
- **jax** [○] via bicomodule
  - Automatic differentiation

### Bibliography References

- `general`: 734 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.