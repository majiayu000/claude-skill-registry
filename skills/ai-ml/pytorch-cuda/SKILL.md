---
name: pytorch-cuda
description: PyTorch CUDA environment and performance guidance, with emphasis on CUDA 13 toolkit/driver requirements, PyTorch wheel compatibility, and runtime checks. Use when configuring PyTorch on NVIDIA GPUs, debugging CUDA setup, or migrating to CUDA 13; triggers: pytorch cuda, cuda 13, driver version, nvcc, torch.version.cuda, tf32, streams.
---

# PyTorch CUDA

## Overview
Configure and verify CUDA 13 readiness (toolkit, driver, and PyTorch wheel support), then run PyTorch CUDA with reliable timing and memory practices.

## When to Use
Use this skill only when the frontmatter triggers apply; otherwise start with a standard PyTorch setup or CPU run.

## Decision Tree
1. Are you targeting CUDA 13?
   - Yes: verify driver minimums and toolkit availability.
2. Do you rely on prebuilt PyTorch wheels?
   - Yes: confirm the available CUDA builds (11.8/12.6/12.8) before upgrading.
3. Do you need GPU profiling accuracy?
   - Yes: use CUDA events and explicit synchronization.

## Workflows

### 1. CUDA 13 Readiness Check
1. Read the installed driver version (`nvidia-smi`).
2. Compare against CUDA 13.0 minimums (GA/Update 1/Update 2).
3. Confirm toolkit availability (`nvcc --version`).
4. Probe PyTorch runtime (`torch.version.cuda`, `torch.cuda.is_available()`).

### 2. PyTorch Wheel Compatibility Gate
1. Check the PyTorch install selector for CUDA wheel versions.
2. If the required CUDA version is not listed, keep the current CUDA or build from source.
3. Pin PyTorch wheel URLs to the listed CUDA build for reproducibility.

### 3. Accurate CUDA Timing
1. Create `torch.cuda.Event(enable_timing=True)` start/end events.
2. Record start, run the kernel, record end.
3. Synchronize the end event before reading elapsed time.

## Non-Obvious Insights
- CUDA toolkit components are versioned independently, so library versions can diverge from the toolkit label.
- CUDA 13 driver minimums differ across 13.0 GA and updates; verify the exact update target.
- PyTorch prebuilt wheels list CUDA 11.8, 12.6, and 12.8; plan CUDA 13 adoption accordingly.

## Evidence
- "CUDA Toolkit 13.1.0 (December 2025), Versioned Online Documentation" - [NVIDIA](https://developer.nvidia.com/cuda-toolkit-archive)
- "Starting with CUDA 11, individual components within the CUDA Toolkit (for example: compiler, libraries, tools) are versioned independently." - [NVIDIA](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html)
- "CUDA 13.0 Update 2 >=580.95.05 N/A CUDA 13.0 Update 1 >=580.82.07 N/A CUDA 13.0 GA >=580.65.06 N/A" - [NVIDIA](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html)
- "CUDA 11.8 CUDA 12.6 CUDA 12.8" - [PyTorch](https://pytorch.org/get-started/locally/)

## Scripts
- `scripts/pytorch-cuda_tool.py`: CLI for probing CUDA versions and checking driver minimums.
- `scripts/pytorch-cuda_tool.js`: Node.js CLI for the same checks.

## Dependencies
- Python 3.11+ or Node 18+.

## References
- [references/README.md](references/README.md)
