---
name: hpc-python
description: Python HPC patterns — threading/multiprocessing/async, CUDA streams, latency hiding, PyTorch DDP. Use when writing performance-sensitive Python code, distributed training, or parallel data processing.
user-invocable: true
---

# HPC Python

Python parallelism, PyTorch DDP, and CPU/GPU latency hiding patterns.

## Extension Files

| File | Content |
|------|---------|
| `parallel-python.md` | Threading vs multiprocessing vs asyncio decision tree, GIL rules, CUDA+fork safety |
| `latency-hiding.md` | CUDA streams, double buffering, compute/comm overlap, CUDAGraphs, async checkpoint |
| `pytorch-ddp.md` | DDP internals, gradient buckets, common bugs, mixed precision, DistributedSampler |
| `preload-caching.md` | Three-level caching: L1 file (disk/memmap/shm), L2 function (lru_cache/dedup/index), L3 variable (buffer/GPU cache/warmup/KV cache) |
| `torch-compile.md` | torch.compile modes, graph break diagnosis/fixes, reading generated Triton as starting point for hand-tuning |
| `benchmarking.md` | Correct GPU timing (CUDA events, torch.utils.benchmark.Timer), warmup, common pitfalls, what to measure |
| `dataloader.md` | DataLoader params (num_workers/pin_memory/prefetch_factor), dataset patterns, data formats, collation, worker issues |

## Quick Decision Tree

```
What is the bottleneck?
├─ I/O bound         → threading (ThreadPoolExecutor) or asyncio
├─ CPU bound         → multiprocessing (mp.Pool, fork BEFORE CUDA!)
├─ GPU bound         → batch inputs, don't parallelize
├─ Mixed CPU→GPU     → pipeline + CUDA streams (see latency-hiding.md)
└─ DDP communication → tune bucket_cap_mb, use model.no_sync()
```

## Critical Rules

1. **mp.Pool BEFORE CUDA**: Create multiprocessing pool before any `torch.cuda` call (fork+CUDA = deadlock)
2. **Never `.item()` in loops**: Accumulate on GPU, transfer final result only
3. **`pin_memory=True`**: Required for `non_blocking=True` transfers to actually be async
4. **DDP `no_sync()`**: Use during gradient accumulation steps to avoid redundant AllReduce
5. **`find_unused_parameters=True`**: Only when needed — it's expensive

## Review Checklist (Python)

```
□ No .cpu()/.item()/.numpy() in hot loops?
□ DataLoader: num_workers > 0, pin_memory=True?
□ mp.Pool created before CUDA init?
□ Threading used only for I/O, not CPU-bound work?
□ DDP gradient accumulation uses no_sync()?
□ CUDA streams used for transfer/compute overlap?
□ Pre-allocated buffers reused (not created per iteration)?
```
