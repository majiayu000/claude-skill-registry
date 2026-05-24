---
name: pixi-install-nvidia
description: Use when the user says "use pixi to install <some nvidia tool>" (or similar) and wants NVIDIA/CUDA/GPU packages installed via Pixi (no sudo/apt), e.g., CUDA toolkit pieces, cuDNN/NCCL, PyTorch CUDA builds, RAPIDS.
---

# Pixi Install NVIDIA

## Trigger

Use this skill when the user asks to install NVIDIA tooling *via Pixi*, especially in the form:
- "use pixi to install <some nvidia tool>"

Examples:
- "use pixi to install cuda"
- "use pixi to install nvcc"
- "use pixi to install cudnn/nccl"
- "use pixi to install pytorch cuda 12.1"

## Overview

This skill provides workflows for setting up **No-Sudo**, **User-Space** GPU environments. By installing CUDA toolkits and libraries via Pixi, you avoid modifying the host system (`apt install`) and ensure perfect reproducibility across different machines.

## Key Benefits
*   **No Root Needed**: Install compilers (NVCC) and libraries (cuDNN, NCCL) without sudo.
*   **Isolation**: Project CUDA version is independent of the host's `/usr/local/cuda`.
*   **Reproducibility**: `pixi.lock` guarantees the exact same driver-compatible libraries everywhere.

## Workflow

### 1. Channel Configuration
Ensure the correct channels are present in `pyproject.toml`. The order determines priority.
*   **Command**: `pixi project channel add nvidia` (and `pytorch` if needed).
*   **Priority**: `nvidia` **MUST** be prioritized over `conda-forge` for all NVIDIA tools and libraries (CUDA, cuDNN, NCCL, etc.), unless the user explicitly requests otherwise.

### 2. Adding GPU Packages
Use specific versions to ensure compatibility between CUDA and the framework. **Always** prefer the `nvidia` channel for these packages.

#### PyTorch (Recommended)
```bash
pixi add pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
```

#### CUDA Toolkit Components
Instead of the massive `cuda-toolkit`, consider adding only what's needed:
```bash
pixi add cuda-compiler cuda-libraries-dev
```

### 3. Verification
After installation, verify GPU visibility:
```bash
pixi run python -c "import torch; print(torch.cuda.is_available())"
```

## Troubleshooting & References

*   **CUDA Version Mismatch**: Check `nvidia-smi` on the host to ensure the installed `pytorch-cuda` version is supported by the host driver.
*   **Library Loading Issues**: If `libcuda.so` or `libcudart.so` are not found, ensure the environment is activated (`pixi shell`).
*   **Detailed Package List**: See [nvidia-packages.md](references/nvidia-packages.md) for a comprehensive list of available NVIDIA and GPU libraries.
*   **Compiling Code**: See [compiling-cuda.md](references/compiling-cuda.md) for instructions on using `nvcc` and `cmake` with the Pixi-managed toolkit.

## Resources

### references/
*   **[nvidia-packages.md](references/nvidia-packages.md)**: Comprehensive guide on channels, packages, and versioning for NVIDIA ecosystems.
*   **[compiling-cuda.md](references/compiling-cuda.md)**: Guide for compiling CUDA C++ code using the Pixi-managed toolchain.
