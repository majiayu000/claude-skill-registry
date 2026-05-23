---
name: keras
description: Keras high-level neural network API. Use for deep learning.
---

# Keras

Keras 3 is a game changer: it is now **multi-backend**. You can write Keras code and run it on top of **JAX, PyTorch, or TensorFlow**.

## When to Use

- **Portability**: Write once, run on any framework.
- **Simplicity**: `model.fit()` is still the cleanest API in the industry.
- **XLA**: Keras 3 enables XLA compilation on all backends by default.

## Core Concepts

### Backend Agnostic

The Model is just a blueprint. You choose the engine at runtime.
`os.environ["KERAS_BACKEND"] = "jax"`

### Functional API

Defining models as a graph of layers: `x = Dense()(inputs)`.

### Keras Core (`keras.ops`)

A numpy-like API that works across all frameworks (differentiable numpy).

## Best Practices (2025)

**Do**:

- **Use Keras 3**: Migrate from `tf.keras`.
- **Use JAX backend**: For fastest training on TPUs/GPUs.
- **Use PyTorch backend**: If you need to integrate into a larger PyTorch codebase.

**Don't**:

- **Don't mix `tf.*` ops**: Use `keras.ops.*` to remain framework-agnostic.

## References

- [Keras Documentation](https://keras.io/)
