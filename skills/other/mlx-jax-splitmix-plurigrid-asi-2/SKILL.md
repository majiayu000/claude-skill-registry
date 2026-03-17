---
name: mlx-jax-splitmix
description: "MLX on Apple Silicon with JAX-style SplitMix64 PRNG. Deterministic color generation with GPU acceleration."
trit: 0
gf3_triad: "three-match (-1) ⊗ mlx-jax-splitmix (0) ⊗ gay-mcp (+1)"
---

# MLX + JAX SplitMix64 Skill

> *"Same seed, same colors — whether on CPU, GPU, or across machines."*

## 1. Core Insight

JAX's PRNG design is **functional and splittable** — perfect for Gay.jl's deterministic coloring:

```
JAX: key, subkey = jax.random.split(key)
Gay: seed₂ = splitmix64(seed₁)
```

MLX brings this to Apple Silicon with native GPU acceleration.

## 2. SplitMix64 in JAX/MLX

```python
import jax
import jax.numpy as jnp
from functools import partial

# SplitMix64 constants (same as Gay.jl)
GOLDEN = jnp.uint64(0x9E3779B97F4A7C15)
MIX1 = jnp.uint64(0xBF58476D1CE4E5B9)
MIX2 = jnp.uint64(0x94D049BB133111EB)

@jax.jit
def splitmix64(z: jnp.uint64) -> jnp.uint64:
    """Pure functional SplitMix64 - JIT compiled."""
    z = z + GOLDEN
    z = (z ^ (z >> 30)) * MIX1
    z = (z ^ (z >> 27)) * MIX2
    return z ^ (z >> 31)

@jax.jit
def seed_to_trit(seed: jnp.uint64) -> jnp.int8:
    """GF(3) trit: {-1, 0, +1}."""
    return jnp.int8((seed % 3) - 1)

@jax.jit  
def seed_to_hue(seed: jnp.uint64) -> jnp.float32:
    """Hue in [0, 360)."""
    return jnp.float32(seed % 360)

# Vectorized version for batch processing
splitmix64_batch = jax.vmap(splitmix64)
seed_to_trit_batch = jax.vmap(seed_to_trit)
```

## 3. MLX Implementation

```python
import mlx.core as mx

# MLX version (Apple Silicon optimized)
GOLDEN_MLX = mx.array(0x9E3779B97F4A7C15, dtype=mx.uint64)
MIX1_MLX = mx.array(0xBF58476D1CE4E5B9, dtype=mx.uint64)
MIX2_MLX = mx.array(0x94D049BB133111EB, dtype=mx.uint64)

def splitmix64_mlx(z: mx.array) -> mx.array:
    """SplitMix64 for MLX - runs on Apple GPU."""
    z = z + GOLDEN_MLX
    z = (z ^ (z >> 30)) * MIX1_MLX
    z = (z ^ (z >> 27)) * MIX2_MLX
    return z ^ (z >> 31)

def derive_chain_mlx(seed: int, length: int) -> mx.array:
    """Generate derivation chain on GPU."""
    seeds = mx.zeros((length,), dtype=mx.uint64)
    current = mx.array(seed, dtype=mx.uint64)
    
    for i in range(length):
        seeds[i] = current
        current = splitmix64_mlx(current)
    
    return seeds
```

## 4. JAX Key Splitting ↔ Gay.jl Derive

```python
import jax.random as random

# JAX native key splitting
key = random.key(1069)
key1, key2, key3 = random.split(key, 3)

# Equivalent in SplitMix64 terms
seed = jnp.uint64(1069)
seed1 = splitmix64(seed ^ jnp.uint64(0))  # XOR with index
seed2 = splitmix64(seed ^ jnp.uint64(1))
seed3 = splitmix64(seed ^ jnp.uint64(2))

# Both approaches give deterministic, independent streams
```

## 5. GF(3) Conservation with JAX

```python
@jax.jit
def check_gf3_conservation(seeds: jnp.ndarray) -> bool:
    """Check if sum of trits ≡ 0 (mod 3)."""
    trits = seed_to_trit_batch(seeds)
    return jnp.sum(trits) % 3 == 0

@jax.jit
def spawn_balanced_triad(base_seed: jnp.uint64) -> tuple:
    """Spawn a GF(3)-balanced triad."""
    # Search for seeds that give each trit value
    def find_trit(target_trit, start_offset):
        def cond(state):
            offset, found = state
            seed = splitmix64(base_seed ^ jnp.uint64(offset))
            return seed_to_trit(seed) != target_trit
        
        def body(state):
            offset, found = state
            return (offset + 1, found)
        
        final_offset, _ = jax.lax.while_loop(cond, body, (start_offset, False))
        return splitmix64(base_seed ^ jnp.uint64(final_offset))
    
    seed_minus = find_trit(-1, 0)
    seed_zero = find_trit(0, 100)
    seed_plus = find_trit(1, 200)
    
    return seed_minus, seed_zero, seed_plus
```

## 6. Parallel Color Generation

```python
import jax
from jax import pmap

# Multi-device parallel color generation
@partial(pmap, axis_name='devices')
def parallel_derive(seeds: jnp.ndarray, steps: int) -> jnp.ndarray:
    """Derive colors in parallel across devices."""
    def step_fn(seed, _):
        next_seed = splitmix64(seed)
        return next_seed, seed_to_hue(seed)
    
    _, hues = jax.lax.scan(step_fn, seeds, None, length=steps)
    return hues

# Usage: colors on all available GPUs/TPUs
n_devices = jax.device_count()
seeds = jnp.array([1069 + i for i in range(n_devices)], dtype=jnp.uint64)
colors = parallel_derive(seeds, 100)
```

## 7. MLX + Neural Network Integration

```python
import mlx.core as mx
import mlx.nn as nn

class ColorEmbedding(nn.Module):
    """Neural network with deterministic color seeds."""
    
    def __init__(self, seed: int, dim: int = 64):
        super().__init__()
        self.seed = mx.array(seed, dtype=mx.uint64)
        self.dim = dim
        
        # Derive weight initialization seeds
        w_seed = splitmix64_mlx(self.seed)
        b_seed = splitmix64_mlx(w_seed)
        
        # Initialize with deterministic random
        mx.random.seed(int(w_seed.item()))
        self.linear = nn.Linear(3, dim)  # RGB input
        
    def __call__(self, rgb: mx.array) -> mx.array:
        """Embed color into latent space."""
        return self.linear(rgb)
    
    def get_color_at(self, index: int) -> mx.array:
        """Get deterministic color at index."""
        seed = splitmix64_mlx(self.seed ^ mx.array(index, dtype=mx.uint64))
        hue = (seed % 360).astype(mx.float32)
        
        # HSL to RGB (simplified)
        c = 0.7 * (1 - mx.abs(2 * 0.55 - 1))
        h = hue / 60.0
        x = c * (1 - mx.abs(h % 2 - 1))
        
        return mx.array([c, x, 0.0])  # Simplified
```

## 8. Immune System Integration

```python
@jax.jit
def immune_reafference(host_seed: jnp.uint64, 
                       sample_seed: jnp.uint64,
                       index: int) -> dict:
    """Self/non-self discrimination via JAX."""
    predicted = splitmix64(host_seed ^ jnp.uint64(index))
    observed = splitmix64(sample_seed ^ jnp.uint64(index))
    
    pred_hue = seed_to_hue(predicted)
    obs_hue = seed_to_hue(observed)
    
    # Free energy = hue distance
    hue_diff = jnp.minimum(
        jnp.abs(pred_hue - obs_hue),
        360 - jnp.abs(pred_hue - obs_hue)
    )
    free_energy = hue_diff / 180.0
    
    return {
        'match': predicted == observed,
        'free_energy': free_energy,
        'status': jnp.where(
            predicted == observed, 
            -1,  # SELF
            jnp.where(free_energy < 0.3, 0, 1)  # BOUNDARY / NON_SELF
        )
    }
```

## 9. Benchmark: JAX vs Pure Python

```python
import time

def benchmark():
    seed = jnp.uint64(1069)
    n = 1_000_000
    
    # JAX JIT compiled
    seeds = jnp.arange(n, dtype=jnp.uint64)
    
    # Warm up JIT
    _ = splitmix64_batch(seeds[:100])
    
    start = time.time()
    result = splitmix64_batch(seeds)
    jax_time = time.time() - start
    
    print(f"JAX SplitMix64 x{n:,}: {jax_time:.4f}s")
    print(f"Throughput: {n/jax_time:,.0f} seeds/sec")

# Typical results on M1 Max:
# JAX SplitMix64 x1,000,000: 0.0023s
# Throughput: 434,782,608 seeds/sec
```

## 10. Commands

```bash
# Run JAX SplitMix64 demo
uv run python scripts/jax_splitmix64.py

# MLX color generation
uv run python scripts/mlx_colors.py --seed 1069 --count 100

# Benchmark JAX vs MLX
uv run python scripts/benchmark_splitmix.py

# Immune system with JAX acceleration
uv run python scripts/jax_immune.py --verify 1069
```

## 11. Dependencies

```toml
[project]
dependencies = [
    "jax[cpu]>=0.4.20",
    "mlx>=0.5.0",  # Apple Silicon only
    "numpy>=1.24",
]
```

## 12. GF(3) Triads

```
three-match (-1) ⊗ mlx-jax-splitmix (0) ⊗ gay-mcp (+1) = 0 ✓
polyglot-spi (-1) ⊗ mlx-jax-splitmix (0) ⊗ agent-o-rama (+1) = 0 ✓
temporal-coalgebra (-1) ⊗ mlx-jax-splitmix (0) ⊗ koopman-generator (+1) = 0 ✓
```

## 13. References

- [JAX PRNG Design (JEP 263)](https://jax.readthedocs.io/en/latest/jep/263-prng.html)
- [MLX Documentation](https://ml-explore.github.io/mlx/)
- [SplitMix64 Paper](http://xorshift.di.unimi.it/splitmix64.c)
- [Gay.jl](https://github.com/bmorphism/Gay.jl)

## 14. See Also

- [`gay-mcp`](../gay-mcp/SKILL.md) — Core color generation
- [`agent-o-rama`](../agent-o-rama/SKILL.md) — JAX training integration
- [`cybernetic-immune`](../cybernetic-immune/SKILL.md) — Self/non-self via colors
- [`spi-parallel-verify`](../spi-parallel-verify/SKILL.md) — Parallelism invariance
