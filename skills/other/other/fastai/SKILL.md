---
name: fastai
description: fast.ai deep learning library. Use for practical deep learning.
---

# fastai

fastai is a layered API on top of PyTorch. It popularized **Transfer Learning** and good defaults (One Cycle Policy).

## When to Use

- **Learning DL**: The best course/library for beginners ("Practical Deep Learning for Coders").
- **Quick Baselines**: Get state-of-the-art results in 5 lines of code.

## Core Concepts

### Defaults

fastai chooses the best learning rate finder, optimizer (AdamW), and augmentations for you.

### Layered API

You can use the high-level `Learner` or peel back layers to raw PyTorch.

## Best Practices (2025)

**Do**:

- **Watch the Course**: Jeremy Howard's course updates annually and is world-class.
- **Use `nbdev`**: fastai's literate programming environment is powerful.

**Don't**:

- **Don't get stuck**: If you need something very custom, drop down to PyTorch.

## References

- [fast.ai](https://www.fast.ai/)
