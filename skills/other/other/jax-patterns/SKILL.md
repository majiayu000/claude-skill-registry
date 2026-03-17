---
name: jax-patterns
description: JAX, Flax, Optax, and Equinox patterns for ML training. Covers JIT, vmap, pmap, TPU usage, and functional model design. Use when building or debugging JAX-based training pipelines.
---

# JAX Patterns

## Framework Selection

| Framework | Style | Strengths | Weaknesses | Use When |
|-----------|-------|-----------|------------|----------|
| **Flax (NNX)** | Pythonic, mutable | Google-backed, large ecosystem, NNX is latest API | Linen API is legacy; NNX still maturing | Default for new projects, TPU training |
| **Equinox** | PyTorch-like, pytree-native | Clean API, composable, feels natural | Smaller ecosystem, fewer examples | Prefer PyTorch style, research code |
| **Haiku** | Functional transforms | DeepMind ecosystem, simple | Maintenance mode (use Flax NNX instead) | Legacy DeepMind codebases only |

Default recommendation: Flax NNX for production/TPU work. Equinox for research where API ergonomics matter.

## Core JAX Concepts

### JIT Compilation

```python
import jax
import jax.numpy as jnp
from functools import partial

# Basic JIT -- function must be pure (no side effects)
@jax.jit
def compute(x, y):
    return jnp.dot(x, y) + jnp.sin(x)

# Static arguments -- use for values that change compilation (shapes, dtypes, booleans)
@partial(jax.jit, static_argnums=(2,))
def forward(params, x, use_dropout: bool):
    ...
```

### vmap -- Automatic Batching

```python
def single_loss(params, x, y):
    pred = model.apply(params, x)
    return jnp.mean((pred - y) ** 2)

batched_loss = jax.vmap(single_loss, in_axes=(None, 0, 0))  # batch over x, y; not params
per_sample_grads = jax.vmap(jax.grad(single_loss), in_axes=(None, 0, 0))  # for DP
```

### pmap -- Data Parallelism

```python
@jax.pmap
def train_step(state, batch):
    def loss_fn(params):
        logits = state.apply_fn(params, batch["input"])
        return optax.softmax_cross_entropy_with_integer_labels(
            logits, batch["label"]
        ).mean()

    grads = jax.grad(loss_fn)(state.params)
    # All-reduce gradients across devices
    grads = jax.lax.pmean(grads, axis_name="devices")
    state = state.apply_gradients(grads=grads)
    return state

# Data must be sharded: (num_devices, per_device_batch, ...)
sharded_batch = jax.tree.map(
    lambda x: x.reshape(jax.local_device_count(), -1, *x.shape[1:]),
    batch,
)
state = train_step(state, sharded_batch)
```

## Flax NNX Model Definition

```python
from flax import nnx
import optax

class MLP(nnx.Module):
    def __init__(self, din, dhidden, dout, *, rngs: nnx.Rngs):
        self.linear1 = nnx.Linear(din, dhidden, rngs=rngs)
        self.bn = nnx.BatchNorm(dhidden, rngs=rngs)
        self.linear2 = nnx.Linear(dhidden, dout, rngs=rngs)
        self.dropout = nnx.Dropout(rate=0.1, rngs=rngs)

    def __call__(self, x):
        x = nnx.relu(self.bn(self.linear1(x)))
        x = self.dropout(x)
        return self.linear2(x)

model = MLP(784, 256, 10, rngs=nnx.Rngs(0))
optimizer = nnx.Optimizer(model, optax.adamw(1e-3))
```

## JIT-Compiled Training Step (Flax NNX)

```python
@nnx.jit
def train_step(model, optimizer, batch):
    def loss_fn(model):
        logits = model(batch["image"])
        loss = optax.softmax_cross_entropy_with_integer_labels(
            logits, batch["label"]
        ).mean()
        return loss, {"logits": logits}

    grad_fn = nnx.value_and_grad(loss_fn, has_aux=True)
    (loss, aux), grads = grad_fn(model)
    optimizer.update(grads)
    return loss, aux
```

## Equinox Alternative

```python
import equinox as eqx
import optax

class MLP(eqx.Module):
    layers: list

    def __init__(self, key):
        k1, k2 = jax.random.split(key)
        self.layers = [
            eqx.nn.Linear(784, 256, key=k1),
            eqx.nn.Linear(256, 10, key=k2),
        ]

    def __call__(self, x):
        x = jax.nn.relu(self.layers[0](x))
        return self.layers[1](x)

model = MLP(jax.random.PRNGKey(0))
optimizer = optax.adamw(1e-3)
opt_state = optimizer.init(eqx.filter(model, eqx.is_array))

@eqx.filter_jit
def train_step(model, opt_state, batch):
    @eqx.filter_value_and_grad
    def loss_fn(model):
        logits = jax.vmap(model)(batch["image"])
        return optax.softmax_cross_entropy_with_integer_labels(
            logits, batch["label"]
        ).mean()

    loss, grads = loss_fn(model)
    updates, opt_state = optimizer.update(grads, opt_state, model)
    model = eqx.apply_updates(model, updates)
    return model, opt_state, loss
```

## Optax Optimizer Chains

```python
import optax

# Composed optimizer: gradient clipping + AdamW + weight decay schedule
schedule = optax.warmup_cosine_decay_schedule(
    init_value=0.0, peak_value=1e-3,
    warmup_steps=1000, decay_steps=50000, end_value=1e-5,
)

optimizer = optax.chain(
    optax.clip_by_global_norm(1.0),       # gradient clipping
    optax.adamw(learning_rate=schedule, weight_decay=0.01),
)

# Separate treatment for different param groups
def partition_fn(params):
    """Label params for different optimizer treatment."""
    flat = flax.traverse_util.flatten_dict(params)
    labels = {k: "no_decay" if "bias" in k[-1] or "norm" in k[-1] else "decay"
              for k in flat}
    return flax.traverse_util.unflatten_dict(labels)

optimizer = optax.multi_transform({
    "decay": optax.adamw(1e-3, weight_decay=0.01),
    "no_decay": optax.adam(1e-3),
}, partition_fn)
```

## Custom Loss with Auxiliary Data

```python
def loss_fn(params, batch, rngs):
    logits = model.apply(params, batch["input"], rngs=rngs)
    loss = optax.softmax_cross_entropy_with_integer_labels(
        logits, batch["label"]
    ).mean()
    accuracy = jnp.mean(jnp.argmax(logits, axis=-1) == batch["label"])
    # Return loss as primary, metrics as aux
    return loss, {"accuracy": accuracy, "logits": logits}

grad_fn = jax.value_and_grad(loss_fn, has_aux=True)
(loss, metrics), grads = grad_fn(state.params, batch, {"dropout": rng})
```

## TPU-Specific Patterns

```python
print(jax.devices())  # [TpuDevice(id=0, ...), ...]

# TPU uses bfloat16 natively for matmuls. Store params in float32 for stability.
# Multi-host pmap (TPU pods) -- pmean handles all-reduce across hosts
@jax.pmap(axis_name="batch")
def train_step(state, batch):
    ...
    grads = jax.lax.pmean(grads, axis_name="batch")
    ...
```

## Gotchas and Anti-Patterns

### Functional Constraints
- **No in-place mutation**: `x[0] = 1` fails. Use `x = x.at[0].set(1)`
- **No side effects in JIT**: `print()` only runs at trace time. Use `jax.debug.print()` instead
- Random numbers require explicit key management: `key, subkey = jax.random.split(key)`

### Pytree Handling
- All JAX transforms operate on pytrees. Custom classes need pytree registration or a framework
- `None` values in pytrees are silently dropped -- can cause shape mismatches
- Use `jax.tree.map` (not manual loops) for transformations across nested structures

### XLA Compilation Caching
- First JIT call is slow (XLA compilation). Same-shape subsequent calls are fast
- Shape changes trigger recompilation -- pad to fixed shapes when possible
- Set `JAX_COMPILATION_CACHE_DIR` to persist compiled programs across runs

### TPU Topology
- `pmap` handles 1D parallelism. For 2D+ mesh, use `jax.sharding` + `mesh_utils`
- Data loading bottleneck: TPU VMs have limited CPU/RAM. Use `tf.data` or Grain
- TPU bfloat16 is default for matmuls -- don't force float16, it's slower on TPU

### Common Mistakes
- Using `np` instead of `jnp` inside JIT -- silent fallback to CPU
- Forgetting `axis_name` in `pmap` when using `pmean`/`psum`
- Creating arrays inside JIT -- they become constants baked into the compiled graph
- Reusing PRNG keys without splitting -- produces correlated "random" numbers
- Python `for` loops in JIT unroll fully -- use `jax.lax.scan` or `fori_loop` instead
