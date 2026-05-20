---
name: mlip-guide
description: Machine Learning Interatomic Potentials (MLIPs) (4 sub-skills: mace-advanced, mlip-validation, torchsim-batch, universal-mlip)
---

# Machine Learning Interatomic Potentials (MLIPs)

Universal and specialized machine learning interatomic potentials for rapid atomistic simulation without DFT. Covers model selection, usage patterns, validation strategies, and known limitations.

## Sub-Skills

| Sub-Skill | Directory | Description |
|---|---|---|
| Universal MLIPs | `universal-mlip/` | MACE-MP-0, CHGNet, M3GNet/MatGL, SevenNet-0: setup, usage, benchmarking, and validation against DFT |
| TorchSim Batch GPU | `torchsim-batch/` | GPU-accelerated batch MD and optimization with TorchSim: 10-100x speedup, auto-batching, parallel relaxation and screening |

## Method Decision Guide

```
What do you need MLIPs for?

Quick geometry relaxation / screening many structures?
  --> universal-mlip/  (MACE-MP-0 medium is fastest, CHGNet is a good alternative)
  --> torchsim-batch/  (GPU available? 10-100x faster batch relaxation with TorchSim)

Molecular dynamics (phonons, thermal, diffusion)?
  --> universal-mlip/  (MACE-MP-0 large for best accuracy)
  --> torchsim-batch/  (GPU available? TorchSim for 10-100x faster MD on GPU)

Elastic constants / equation of state?
  --> universal-mlip/  (any universal MLIP; validate against DFT for novel systems)

Band gaps / electronic properties / magnetic ordering?
  --> MLIPs CANNOT predict these. Use Quantum ESPRESSO DFT instead.

System contains rare elements / extreme conditions?
  --> Validate MLIP against DFT first; MLIPs may extrapolate poorly.
```

## Pre-installed vs. Installable

| MLIP | Status | Install Command |
|---|---|---|
| MACE-MP-0 | Pre-installed | -- |
| CHGNet | pip install | `pip install chgnet` |
| M3GNet (MatGL) | pip install | `pip install matgl` |
| SevenNet | pip install | `pip install sevenn` |
| ORB Models | pip install | `pip install orb-models` |
| TorchSim | pip install | `pip install torch-sim` (requires PyTorch + CUDA for GPU) |
