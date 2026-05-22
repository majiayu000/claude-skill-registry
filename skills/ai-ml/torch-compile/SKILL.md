---
name: torch-compile
description: Optimize PyTorch with torch.compile (TorchDynamo/Inductor), focusing on compile overhead, graph breaks, and benchmark methodology. Use when speeding up PyTorch models or debugging compile behavior; triggers: torch.compile, torchdynamo, inductor, graph break, pytorch optimization.
---

# Torch Compile

## Overview
Use `torch.compile` to JIT-compile PyTorch code into optimized kernels, then validate speedups with warmups and graph-break audits.

## When to Use
Use this skill only when the frontmatter triggers apply; otherwise keep eager mode.

## Decision Tree
1. Do you need to reduce Python overhead in hot paths?
   - Yes: compile and benchmark.
2. Are first runs much slower than eager?
   - Yes: warm up and re-measure after caching.
3. Are graph breaks frequent?
   - Yes: audit with `torch._dynamo.explain` or logging and reduce non-tensor logic.

## Workflows

### 1. Compile Benchmark With Warmup
1. Run a short eager baseline.
2. Compile the model and run warmup iterations.
3. Measure steady-state latency after warmup.
4. Compare the eager and compiled timings.

### 2. Graph Break Audit
1. Run `torch._dynamo.explain` on the target function.
2. Record graph break counts and reasons.
3. Move non-tensor logic outside the compiled region.
4. Re-run the explain pass to confirm fewer breaks.

### 3. Speedup Expectation Check
1. Confirm the workload is Python-overhead bound.
2. If the workload is GPU compute bound, expect lower gains.
3. Adjust batch size or fuse operations to increase gains.

## Non-Obvious Insights
- Compilation overhead shows up on the first few executions, so warmup is required before benchmarking.
- Speedup depends on reducing Python overhead and GPU read/writes; architecture and batch size affect the outcome.
- Graph breaks trade optimization opportunities for correctness rather than crashing.

## Evidence
- "torch.compile makes PyTorch code run faster by JIT-compiling PyTorch code into optimized kernels, while requiring minimal code changes." - [PyTorch](https://pytorch.org/tutorials/intermediate/torch_compile_tutorial.html)
- "torch.compile takes extra time to compile the model on the first few executions." - [PyTorch](https://pytorch.org/tutorials/intermediate/torch_compile_tutorial.html)
- "reducing Python overhead and GPU read/writes, and so the observed speedup may vary on factors such as model architecture and batch size." - [PyTorch](https://pytorch.org/tutorials/intermediate/torch_compile_tutorial.html)
- "Graph breaks result in lost optimization opportunities, which may still be undesirable, but this is better than silent incorrectness or a hard crash." - [PyTorch](https://pytorch.org/tutorials/intermediate/torch_compile_tutorial.html)

## Scripts
- `scripts/torch-compile_tool.py`: CLI for probing torch.compile availability, benchmarking, and explain output.
- `scripts/torch-compile_tool.js`: Node.js wrapper for the same CLI.

## Dependencies
- Python 3.11+ or Node 18+.
- PyTorch 2.0+ for torch.compile.

## References
- [references/README.md](references/README.md)
