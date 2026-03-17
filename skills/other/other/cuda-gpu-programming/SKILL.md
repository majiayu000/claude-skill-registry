---
name: cuda-gpu-programming
description: Custom CUDA kernels, Triton GPU programming, nsight profiling, memory optimization, and kernel fusion patterns.
---

# CUDA and GPU Programming

## Kernel Implementation Decision Table

| Scenario | PyTorch Native | Triton | Custom CUDA |
|---|---|---|---|
| Standard ops (matmul, conv, attention) | Yes | | |
| Fused activation + normalization | | Yes | |
| Custom attention variant | | Yes | |
| Exotic memory access pattern | | | Yes |
| Warp-level primitives needed | | | Yes |
| Rapid prototyping of custom ops | | Yes | |
| Maximum perf, known bottleneck | | | Yes |
| Cross-platform (AMD + NVIDIA) | Yes | Yes | |
| Team has no CUDA experience | Yes | Yes | |

**Default**: PyTorch native first. Profile bottleneck -> try Triton. Drop to CUDA only when Triton abstraction blocks you.

## Triton Matrix Multiplication Kernel

```python
import triton
import triton.language as tl
import torch

@triton.jit
def matmul_kernel(
    a_ptr, b_ptr, c_ptr,
    M, N, K,
    stride_am, stride_ak,
    stride_bk, stride_bn,
    stride_cm, stride_cn,
    BLOCK_M: tl.constexpr, BLOCK_N: tl.constexpr, BLOCK_K: tl.constexpr,
):
    pid_m = tl.program_id(0)
    pid_n = tl.program_id(1)

    offs_m = pid_m * BLOCK_M + tl.arange(0, BLOCK_M)
    offs_n = pid_n * BLOCK_N + tl.arange(0, BLOCK_N)
    offs_k = tl.arange(0, BLOCK_K)

    a_ptrs = a_ptr + offs_m[:, None] * stride_am + offs_k[None, :] * stride_ak
    b_ptrs = b_ptr + offs_k[:, None] * stride_bk + offs_n[None, :] * stride_bn

    acc = tl.zeros((BLOCK_M, BLOCK_N), dtype=tl.float32)

    for k in range(0, K, BLOCK_K):
        a = tl.load(a_ptrs, mask=(offs_m[:, None] < M) & (offs_k[None, :] < K))
        b = tl.load(b_ptrs, mask=(offs_k[:, None] < K) & (offs_n[None, :] < N))
        acc += tl.dot(a, b)
        a_ptrs += BLOCK_K * stride_ak
        b_ptrs += BLOCK_K * stride_bk
        offs_k += BLOCK_K

    c_ptrs = c_ptr + offs_m[:, None] * stride_cm + offs_n[None, :] * stride_cn
    mask = (offs_m[:, None] < M) & (offs_n[None, :] < N)
    tl.store(c_ptrs, acc, mask=mask)

def triton_matmul(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    M, K = a.shape
    K2, N = b.shape
    assert K == K2
    c = torch.empty((M, N), device=a.device, dtype=a.dtype)
    grid = lambda meta: (
        triton.cdiv(M, meta["BLOCK_M"]),
        triton.cdiv(N, meta["BLOCK_N"]),
    )
    matmul_kernel[grid](
        a, b, c, M, N, K,
        a.stride(0), a.stride(1),
        b.stride(0), b.stride(1),
        c.stride(0), c.stride(1),
        BLOCK_M=64, BLOCK_N=64, BLOCK_K=32,
    )
    return c
```

## Custom CUDA Extension for PyTorch

### Kernel Source (`csrc/fused_gelu.cu`)

```cuda
#include <torch/extension.h>
#include <cuda_runtime.h>

__device__ __forceinline__ float gelu(float x) {
    return 0.5f * x * (1.0f + tanhf(0.7978845608f * (x + 0.044715f * x * x * x)));
}

__global__ void fused_bias_gelu_kernel(
    const float* __restrict__ input,
    const float* __restrict__ bias,
    float* __restrict__ output,
    int n, int d
) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n * d) {
        int col = idx % d;
        output[idx] = gelu(input[idx] + bias[col]);
    }
}

torch::Tensor fused_bias_gelu(torch::Tensor input, torch::Tensor bias) {
    TORCH_CHECK(input.is_cuda(), "input must be CUDA tensor");
    auto output = torch::empty_like(input);
    int total = input.numel();
    int threads = 256;
    int blocks = (total + threads - 1) / threads;
    fused_bias_gelu_kernel<<<blocks, threads>>>(
        input.data_ptr<float>(),
        bias.data_ptr<float>(),
        output.data_ptr<float>(),
        input.size(0), input.size(1)
    );
    return output;
}

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
    m.def("fused_bias_gelu", &fused_bias_gelu, "Fused bias + GeLU");
}
```

### Build and Load

```python
from torch.utils.cpp_extension import load

fused_ops = load(
    name="fused_ops",
    sources=["csrc/fused_gelu.cu"],
    extra_cuda_cflags=["-O3", "--use_fast_math"],
)

# Use it
output = fused_ops.fused_bias_gelu(hidden_states, bias)
```

## Nsight Profiling Workflow

### Command-Line Profiling

```bash
# Systems-level trace (kernel timings, memory transfers)
nsys profile --trace=cuda,nvtx --output=report python train.py

# Kernel-level analysis (occupancy, memory throughput)
ncu --set full --target-processes all -o kernel_report python train.py

# Profile specific kernel only (skip warmup)
ncu --kernel-name "fused_bias_gelu_kernel" --launch-skip 10 --launch-count 5 \
    -o gelu_report python train.py
```

### PyTorch Profiler Integration

```python
from torch.profiler import profile, ProfilerActivity, schedule

with profile(
    activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
    schedule=schedule(wait=1, warmup=2, active=3, repeat=1),
    on_trace_ready=torch.profiler.tensorboard_trace_handler("./profiler_logs"),
    record_shapes=True,
    with_stack=True,
) as prof:
    for step, batch in enumerate(dataloader):
        train_step(batch)
        prof.step()
        if step >= 6:
            break

# Quick summary
print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=20))
```

## Memory Optimization Patterns

### Coalesced Memory Access

```cuda
// BAD: strided access (column-major traversal of row-major data)
// Each thread in a warp reads addresses 'stride' apart
float val = input[threadIdx.x * stride + col];

// GOOD: coalesced access (adjacent threads read adjacent memory)
// Warp reads a contiguous 128-byte cache line
float val = input[row * width + threadIdx.x];
```

### Shared Memory Tiling

```cuda
__global__ void tiled_matmul(float* A, float* B, float* C, int N) {
    __shared__ float As[TILE][TILE];
    __shared__ float Bs[TILE][TILE];

    int row = blockIdx.y * TILE + threadIdx.y;
    int col = blockIdx.x * TILE + threadIdx.x;
    float sum = 0.0f;

    for (int t = 0; t < N / TILE; t++) {
        As[threadIdx.y][threadIdx.x] = A[row * N + t * TILE + threadIdx.x];
        Bs[threadIdx.y][threadIdx.x] = B[(t * TILE + threadIdx.y) * N + col];
        __syncthreads();

        for (int k = 0; k < TILE; k++)
            sum += As[threadIdx.y][k] * Bs[k][threadIdx.x];
        __syncthreads();
    }
    C[row * N + col] = sum;
}
```

## Gotchas and Anti-Patterns

### Warp Divergence
- **Problem**: `if (threadIdx.x % 2 == 0)` causes half the warp to idle while the other half executes.
- **Fix**: Restructure so divergence aligns on warp boundaries (groups of 32). Move branching outside the kernel or reorganize data so threads in the same warp take the same path.

### Shared Memory Bank Conflicts
- **Problem**: 32 banks, each 4 bytes wide. If multiple threads in a warp access the same bank (different addresses), accesses serialize.
- **Fix**: Pad shared memory arrays: `__shared__ float s[TILE][TILE + 1]`. The +1 offset strides access across banks.

### Register Pressure
- **Problem**: Too many variables per thread reduces occupancy. The compiler spills to slow local memory.
- **Fix**: Check with `ncu --metrics launch__registers_per_thread`. Reduce per-thread state, use `__launch_bounds__(maxThreads, minBlocks)` to hint the compiler.

### Kernel Launch Overhead vs Compute
- Launching a kernel costs ~5-10us. Tiny kernels (< 1000 elements) spend more time launching than computing. Fuse small operations into a single kernel. For very small tensors, consider CPU. Profile with nsys to see launch gaps.

### Ignoring Occupancy
- Low occupancy means SMs idle during memory stalls. Use the CUDA occupancy calculator. Aim for >50%. Adjust block size, reduce shared memory/registers if needed. Not always the bottleneck -- check nsight first.

### Synchronization Overkill
- `__syncthreads()` in loops/conditionals stalls the entire block. Sync only when shared memory is read by a thread that didn't write it. Never place inside divergent branches (deadlock). Use `__syncwarp()` for warp-level coordination.
