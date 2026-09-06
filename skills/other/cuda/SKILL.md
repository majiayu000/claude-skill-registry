---
name: cuda
description: 'Use when writing CUDA kernels, managing the thread, block, and grid hierarchy, tiling shared memory, using streams, setting nvcc flags, or using Thrust. Not for kernel debugging: use cuda-debugging.'
---

# CUDA

## Contract

| Field | Bound contract |
|---|---|
| Trigger | CUDA C or C++ kernel code is being written, optimized, or reviewed: launch configuration, memory hierarchy, streams, nvcc flags, Thrust, or known performance traps such as warp divergence and uncoalesced access. |
| Authority | Read-only. The skill emits guidance and code; it writes no files. Nothing to roll back. No remote mutation. |
| Side effect | Guidance, code samples, and flag recommendations in chat output. |
| Done | A launch configuration, memory plan, build command, and pitfall review exist for the kernel in question, each grounded in the toolkit version the project pins. |

## Inputs

1. Kernel goal (required): the operation to move to the GPU, or the existing kernel under review.
2. GPU model (required if code must run on it): compute capability from `nvidia-smi --query-gpu=compute_cap`.
3. Toolkit version (required if not inferrable): `nvcc --version`. The grounded current stable is CUDA Toolkit 13.3 Update 1.
4. Build system (optional): existing nvcc or CMake CUDA flags.

## Procedure

1. Identify the GPU compute capability and toolkit version. CUDA 13.x supports Turing (sm_75) and later; older targets require an older toolkit. Done when: the `sm_XX` target and toolkit line are recorded, or the mismatch is reported.
2. Write or review the launch: threads grouped into blocks, blocks into a grid. Cap a block at 1024 threads. Compute `blocks = (n + threads - 1) / threads` and guard every load and store with `if (i < n)`. Check each launch with `cudaGetLastError()` and each sync with a second check. Done when: the launch math covers every element and both error checks are present.
3. Place data at the right level of the hierarchy. Registers hold per-thread scalars. Shared memory holds tiles reused across the block. Global memory holds large arrays, read coalesced. Constant memory holds broadcast read-only data. Latency numbers below are order-of-magnitude guides on current parts, not constants:

| Memory | Scope | Typical latency | Use |
|---|---|---|---|
| Registers | Per thread | ~1 cycle | Scalars, indices |
| Shared (`__shared__`) | Per block | low tens of cycles | Tiled data |
| Global | Device | hundreds of cycles | Large arrays, coalesced |
| Constant (`__constant__`) | Device, cached | fast broadcast | Parameters, lookup tables |

Done when: every buffer has an assigned level and tiles reuse shared memory.

4. Tile matrix work through shared memory and `__syncthreads()`:

```c
#define TILE 16

__global__ void matmul_tiled(const float *A, const float *B, float *C, int N) {
    __shared__ float As[TILE][TILE];
    __shared__ float Bs[TILE][TILE];

    int row = blockIdx.y * TILE + threadIdx.y;
    int col = blockIdx.x * TILE + threadIdx.x;
    float sum = 0.0f;

    for (int t = 0; t < (N + TILE - 1) / TILE; t++) {
        As[threadIdx.y][threadIdx.x] = (row < N && t * TILE + threadIdx.x < N)
            ? A[row * N + t * TILE + threadIdx.x] : 0.0f;
        Bs[threadIdx.y][threadIdx.x] = (col < N && t * TILE + threadIdx.y < N)
            ? B[(t * TILE + threadIdx.y) * N + col] : 0.0f;
        __syncthreads();

        for (int k = 0; k < TILE; k++)
            sum += As[threadIdx.y][k] * Bs[k][threadIdx.x];
        __syncthreads();
    }
    if (row < N && col < N)
        C[row * N + col] = sum;
}
```

Done when: each tile load is bounds-checked and the sync points separate load from use.

5. Move copies off the critical path with streams and pinned memory. `cudaMallocHost` pins host buffers so `cudaMemcpyAsync` overlaps compute with DMA. Assign each stage its own `cudaStream_t` and pass the stream as the fourth launch parameter. Synchronize with `cudaStreamSynchronize`, not the whole device, when streams run independently. Done when: copies and kernels overlap across streams or a single-stream design is justified.
6. Select nvcc flags for the build purpose:

| Flag | Effect |
|---|---|
| `-O3` | Optimize device code |
| `-arch=sm_XX` | Target one architecture |
| `-gencode arch=compute_XX,code=sm_XX` | Fat binary for several GPUs |
| `-G` | Disable optimizations for cuda-gdb |
| `-lineinfo` | Source-line correlation in profiles |
| `--use_fast_math` | Faster, less precise math intrinsics |
| `-maxrregcount=N` | Cap registers per thread |
| `-Xcompiler -fopenmp` | Pass host flags to the host compiler |

Done when: the build command targets the recorded `sm_XX` and omits `-G` outside debugging.

7. Estimate occupancy before tuning by hand. Call `cudaOccupancyMaxActiveBlocksPerMultiprocessor`, or read `sm__warps_active.avg.pct_of_peak_sustained_active` in Nsight Compute. Treat a low achieved-occupancy reading as a signal to check register pressure, shared memory size, and block size against the measured stall reasons, not as a failure on its own. A compute-bound kernel with enough instruction-level parallelism can run well at a low occupancy; a latency-bound streaming kernel usually cannot. Done when: occupancy is measured and any change made to registers, shared memory, or block size is tied to a named limiting factor.
8. Use Thrust for sort, scan, and reduce instead of hand-written kernels:

```cpp
#include <thrust/device_vector.h>
#include <thrust/sort.h>
#include <thrust/reduce.h>

thrust::device_vector<int> d_vec(1000000);
thrust::sort(d_vec.begin(), d_vec.end());
int sum = thrust::reduce(d_vec.begin(), d_vec.end());
```

Write custom kernels for fused, domain-specific operations. Done when: every primitive that Thrust covers is delegated or the custom kernel is justified.

9. Review the kernel against the two common traps. Divergence: threads in a warp of 32 execute in lockstep, so a branch on `threadIdx` serializes the paths. Uncoalesced access: consecutive threads must read consecutive addresses; a strided read like `data[threadIdx.x * stride]` defeats the memory system. Done when: no hot branch splits a warp and every hot load is coalesced.

## Failure and recovery

| Failure class | Behavior |
|---|---|
| GPU or toolkit version unknown | Ask for `nvidia-smi --query-gpu=compute_cap` and `nvcc --version` output. Guidance stays generic until both are known. |
| `cudaErrorIllegalAddress` (700) | Out-of-bounds device pointer. Re-run under `compute-sanitizer --tool memcheck` and add bounds checks. |
| `cudaErrorLaunchTimeout` (702) | Kernel exceeded the watchdog limit, primarily Windows TDR. Split the kernel or shrink the work per launch. |
| `no kernel image available` | Binary lacks this GPU's `sm_XX`. Rebuild with the recorded compute capability. |
| Copies dominate the timeline | Host buffers are pageable. Pin them with `cudaMallocHost`. |
| CPU and GPU results differ | Race on shared or global memory. Audit `__syncthreads()` placement and use atomics for cross-thread reductions. |

## Output

Guidance in chat: the launch configuration, the memory plan per buffer, the nvcc build command for the recorded target, the occupancy measurement with its limiting factor, and the pitfall review. Each recommendation names the toolkit and architecture it assumes.
