---
name: deep-learning
description: "Build and train deep neural networks including CNNs, RNNs, Transformers, and advanced architectures. Use for image classification, object detection, NLP, sequence modeling, transfer learning, and complex pattern recognition tasks."
---

# Deep Learning

Build and train deep neural networks for computer vision, natural language processing, and complex pattern recognition.

## Overview

This skill provides comprehensive guidance for deep learning across convolutional networks, recurrent networks, transformers, and modern architectures.

## Quick Reference

| Scenario | Recommended Approach | Reference File |
|----------|---------------------|----------------|
| Image classification, object detection | CNNs (ResNet, EfficientNet) | `/references/cnn-guide.md` |
| Sequential data, time-series, NLP | RNNs, LSTMs, GRUs | `/references/rnn-guide.md` |
| Modern NLP, attention-based models | Transformers (BERT, GPT) | `/references/transformer-guide.md` |
| Training optimization and techniques | Best practices, regularization | `/references/training-guide.md` |

## Core Principles

1. **Architecture Selection** - Choose network type based on data structure and task
2. **Gradient Flow** - Ensure effective backpropagation through deep networks
3. **Regularization** - Prevent overfitting with dropout, batch norm, data augmentation
4. **Transfer Learning** - Leverage pre-trained models for faster, better results
5. **Optimization** - Use appropriate optimizers, learning rates, and schedules

## Network Types

### Convolutional Neural Networks (CNNs)
Process grid-like data (images) using convolutional layers.

**Key Architectures:**
- ResNet: Residual connections for very deep networks
- EfficientNet: Optimal accuracy-efficiency trade-off
- Vision Transformers: Attention-based image processing

**Use Cases:** Image classification, object detection, segmentation

### Recurrent Neural Networks (RNNs)
Process sequential data with temporal dependencies.

**Variants:**
- LSTM: Long Short-Term Memory for long sequences
- GRU: Gated Recurrent Unit, simpler than LSTM
- Bidirectional: Process sequences in both directions

**Use Cases:** Time-series, text processing, speech recognition

### Transformers
Attention-based architecture for parallel sequence processing.

**Models:**
- BERT: Bidirectional encoder for understanding
- GPT: Autoregressive decoder for generation
- Vision Transformers: Apply transformers to images

**Use Cases:** NLP, machine translation, text generation

## Training Strategies

**Optimization:**
- Adam/AdamW for most tasks
- SGD with momentum for computer vision
- Learning rate schedules (cosine, one-cycle)

**Regularization:**
- Dropout (0.1-0.5)
- Batch/Layer normalization
- Data augmentation
- Weight decay (1e-4 to 1e-5)

**Transfer Learning:**
- Use pre-trained models as starting point
- Fine-tune with lower learning rate
- Freeze early layers, train later layers

## Using the Reference Files

**`/references/cnn-guide.md`** — CNN architectures, convolution operations, pooling, popular models (ResNet, EfficientNet), implementation tips.

**`/references/rnn-guide.md`** — RNN fundamentals, LSTM/GRU details, sequence-to-sequence models, attention mechanisms.

**`/references/transformer-guide.md`** — Transformer architecture, self-attention, BERT, GPT, Vision Transformers, training techniques.

**`/references/training-guide.md`** — Optimization algorithms, learning rate schedules, regularization, debugging, mixed precision training.

## Best Practices

- Start with pre-trained models when available
- Use batch normalization for training stability
- Apply data augmentation to prevent overfitting
- Monitor training and validation metrics closely
- Use gradient clipping for RNNs and Transformers
- Implement early stopping
- Leverage GPU acceleration with appropriate batch sizes
- Use mixed precision (FP16) for faster training

## Common Pitfalls to Avoid

- Learning rate too high (causes divergence)
- Not normalizing input data
- Forgetting eval mode during inference
- Using batch norm with batch size = 1
- Not shuffling training data
- Ignoring class imbalance
- Applying dropout during inference
- Not monitoring gradient magnitudes

## Key Frameworks

**PyTorch:** Dynamic graphs, research-friendly, torchvision/torchtext
**TensorFlow/Keras:** Production deployment, TF Serving, high-level API
**JAX:** Functional programming, XLA compilation

## Hardware Considerations

- NVIDIA GPUs with CUDA for training
- Mixed precision (FP16) for 2-3x speedup
- Multi-GPU training with DistributedDataParallel
- Gradient accumulation for larger effective batch sizes
