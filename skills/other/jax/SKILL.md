---
name: jax
description: JAX high-performance numerical computing. Use for ML research.
---

# JAX

JAX is "NumPy on steroids". It combines Autograd (automatic differentiation) with XLA (compilation). 2025 sees **Flax NNX** (PyTorch-style OOP) becoming standard.

## When to Use

- **TPU Training**: JAX runs natively on Google TPUs.
- **Research**: If you need to compute 10th order derivatives or strange math.
- **Massive Scale**: DeepMind and OpenAI use JAX for training frontier models.

## Core Concepts

### Functional Transformations

`grad()`, `jit()`, `vmap()`, `pmap()`.

### Flax (NNX)

Neural network library. NNX introduces mutable state (OOP) to make JAX feel like PyTorch.

### Statelessness

(Legacy Flax) parameters are stored separately from the model.

## Best Practices (2025)

**Do**:

- **Use `jit`**: Always compile your functions.
- **Use Flax NNX**: Avoid the complexity of legacy immutable Flax/Haiku.
- **Use `shard_map`**: For distributed training across devices.

**Don't**:

- **Don't use side effects**: `print()` inside a `jit` function only runs once (during tracing).

## References

- [JAX Documentation](https://jax.readthedocs.io/)
