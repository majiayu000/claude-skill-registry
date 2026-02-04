---
name: pytorch-lightning
description: High-level training framework for PyTorch that abstracts boilerplate while maintaining flexibility. Includes the Trainer, LightningModule, and support for multi-GPU scaling and reproducibility. (lightning, pytorch-lightning, lightningmodule, trainer, callback, ddp, fast_dev_run, seed_everything)
---

## Overview

PyTorch Lightning is a lightweight wrapper for PyTorch that decouples the research code from the engineering code. It automates 40+ engineering details like epoch loops, optimization, and hardware acceleration, while allowing researchers to retain full control over the model logic.

## When to Use

Use Lightning when you want to scale models to multi-GPU or multi-node environments without changing training code, or when you want to eliminate boilerplate for logging, checkpointing, and reproducibility.

## Decision Tree

1. Are you testing code logic on a small subset?
   - YES: Use `Trainer(fast_dev_run=True)`.
2. Do you need to scale to multiple GPUs?
   - YES: Set `accelerator='gpu'` and `devices=N` in the Trainer.
3. Do you have logic that is non-essential to the model (e.g., special logging)?
   - YES: Implement it as a `Callback`.

## Workflows

1. **Transitioning from Raw PyTorch to Lightning**
   1. Define a class inheriting from `L.LightningModule`.
   2. Move model architecture into `__init__` and logic into `training_step`.
   3. Implement `configure_optimizers` to return the optimizer and optional scheduler.
   4. Instantiate an `L.Trainer` and pass the model and DataLoader to `trainer.fit()`.

2. **Multi-GPU Training Scaling**
   1. Initialize the Trainer with `accelerator='gpu'` and `devices=N`.
   2. Set `strategy='ddp'` or `'deepspeed_stage_2'` for multi-node/large-scale runs.
   3. Optionally enable 16-bit precision using `precision='16-mixed'`.
   4. Run the script without code changes to standard logic.

3. **Ensuring Training Reproducibility**
   1. Call `seed_everything(seed, workers=True)` at the start of the script.
   2. Initialize the Trainer with `deterministic=True`.
   3. Avoid data-dependent logic in transforms that isn't handled by the derived seeds.

## Non-Obvious Insights

- **Overhead Analysis**: The 'barebones' mode in the Trainer is specifically for overhead analysis and disables almost all logging and checkpointing for speed.
- **Callback State Management**: Custom callbacks must implement a `state_key` property if multiple instances of the same callback type are used in a single Trainer.
- **Superior Debugging**: The `fast_dev_run` flag is superior to limiting batches manually because it avoids all side effects like checkpointing or logging that might clutter the workspace during debugging.

## Evidence

- "The Lightning Trainer automates 40+ tricks including: Epoch and batch iteration, optimizer.step(), loss.backward(), optimizer.zero_grad() calls." (https://lightning.ai/docs/pytorch/stable/starter/introduction.html)
- "By setting workers=True in seed_everything(), Lightning derives unique seeds across all dataloader workers." (https://lightning.ai/docs/pytorch/stable/common/trainer.html)

## Scripts

- `scripts/pytorch-lightning_tool.py`: Template for a LightningModule and Trainer setup.
- `scripts/pytorch-lightning_tool.js`: Script to trigger Lightning training with CLI arguments.

## Dependencies

- lightning
- torch

## References

- [PyTorch Lightning Reference](references/README.md)