---
name: cuda-guide
description: |
  CUDA/GPU computing guardrails, patterns, and best practices for AI-assisted development.
  Use when working with CUDA files (.cu, .cuh), or when the user mentions CUDA/GPU programming.
  Provides kernel design patterns, memory hierarchy guidelines, and occupancy optimization
  specific to this project's coding standards.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: language
  language: cuda
  extensions: ".cu,.cuh"
---

# CUDA Guide

> Applies to: CUDA 11+, GPU Computing, Deep Learning, Scientific Computing, HPC

## Core Principles

1. **Parallelism First**: Design algorithms for thousands of concurrent threads; serial thinking is the primary enemy of GPU performance
2. **Memory Hierarchy Awareness**: Global memory is 100x slower than shared memory and 1000x slower than registers; every kernel design starts with memory access planning
3. **Coalesced Access**: Adjacent threads must access adjacent memory addresses; a single misaligned access pattern can reduce bandwidth by 32x
4. **Occupancy Over Cleverness**: Maximize active warps per SM by managing register count, shared memory usage, and block dimensions together
5. **Minimize Host-Device Transfers**: PCIe bandwidth is the bottleneck; overlap transfers with computation using streams and pinned memory

## Guardrails

### Error Checking

- ALWAYS check CUDA API return values with a macro wrapper
- ALWAYS call `cudaGetLastError()` after every kernel launch
- ALWAYS call `cudaDeviceSynchronize()` before reading kernel results on the host
- Use `compute-sanitizer` (successor to `cuda-memcheck`) in development builds
- Handle `cudaErrorMemoryAllocation` gracefully; never assume GPU memory is infinite

```cuda
#define CUDA_CHECK(call)                                                    \
    do {                                                                    \
        cudaError_t err = call;                                            \
        if (err != cudaSuccess) {                                          \
            fprintf(stderr, "CUDA error at %s:%d: %s\n",                   \
                    __FILE__, __LINE__, cudaGetErrorString(err));           \
            exit(EXIT_FAILURE);                                            \
        }                                                                   \
    } while (0)

#define CUDA_CHECK_KERNEL()                                                 \
    do {                                                                    \
        cudaError_t err = cudaGetLastError();                              \
        if (err != cudaSuccess) {                                          \
            fprintf(stderr, "Kernel launch error at %s:%d: %s\n",          \
                    __FILE__, __LINE__, cudaGetErrorString(err));           \
            exit(EXIT_FAILURE);                                            \
        }                                                                   \
    } while (0)
```

### Memory Management

- Pair every `cudaMalloc` with a `cudaFree`; prefer RAII wrappers in C++ host code
- Use `cudaMallocManaged` (Unified Memory) for prototyping; switch to explicit transfers for production
- Use `cudaMallocHost` (pinned memory) when streaming data to the GPU; pageable memory cannot overlap with compute
- Prefer `cudaMemcpyAsync` with streams over synchronous `cudaMemcpy`
- Never access device pointers from host code or host pointers from device code (except Unified Memory)
- Call `cudaMemset` or `cudaMemsetAsync` to zero-initialize device buffers

### Kernel Design

- Block size must be a multiple of warp size (32); prefer 128, 256, or 512
- Calculate grid size as `(n + block_size - 1) / block_size`
- Always include bounds checking: `if (idx < n)` at the top of every kernel
- Use grid-stride loops for kernels that must handle arbitrary data sizes
- Document thread mapping: which dimension maps to which data axis
- Mark device-only helpers as `__device__`, host+device as `__host__ __device__`

```cuda
// Grid-stride loop: works with any grid size, any data size
__global__ void saxpy(float a, const float* x, float* y, int n) {
    for (int i = blockIdx.x * blockDim.x + threadIdx.x;
         i < n;
         i += blockDim.x * gridDim.x) {
        y[i] = a * x[i] + y[i];
    }
}
```

### Synchronization

- Use `__syncthreads()` after every shared memory write before any thread reads another thread's value
- Never place `__syncthreads()` inside a conditional branch that not all threads in a block will reach (deadlock)
- Use `__syncwarp()` (CUDA 9+) for warp-level synchronization instead of relying on implicit warp-synchronous execution
- Use `cudaDeviceSynchronize()` sparingly in production; prefer stream synchronization with `cudaStreamSynchronize()`
- Use CUDA events (`cudaEventRecord` / `cudaEventSynchronize`) for fine-grained inter-stream ordering

### Performance

- Profile before optimizing: use Nsight Compute for kernel analysis, Nsight Systems for system-level view
- Target >50% theoretical occupancy; use the CUDA Occupancy Calculator to tune block dimensions
- Aim for >60% of peak memory bandwidth in memory-bound kernels
- Avoid warp divergence: ensure threads within a warp take the same branch when possible
- Prefer `float` over `double` on consumer GPUs (2x throughput difference)
- Minimize atomic operations on global memory; use shared memory atomics with a final reduction

## Memory Hierarchy

Understanding the memory hierarchy is the single most important factor in CUDA performance.

| Memory Type | Scope | Latency (cycles) | Size | Cached | Read/Write |
|-------------|-------|-------------------|------|--------|------------|
| Registers | Thread | 1 | ~255 per thread | N/A | R/W |
| Shared | Block | ~5 | 48-164 KB per SM | N/A | R/W |
| L1 Cache | SM | ~28 | 48-192 KB per SM | Auto | R |
| L2 Cache | Device | ~200 | 4-40 MB | Auto | R/W |
| Global | Device | ~400-600 | 4-80 GB (HBM/GDDR) | Yes | R/W |
| Constant | Device | ~5 (cached) | 64 KB | Yes (broadcast) | R |
| Texture | Device | ~400 (cached) | Global pool | Yes (spatial) | R |

**Decision guide:**
- Data reused within a thread -> registers (automatic via local variables)
- Data shared across threads in a block -> `__shared__` memory
- Read-only data broadcast to all threads -> `__constant__` memory
- Large read-only data with spatial locality -> texture memory
- Everything else -> global memory with coalesced access patterns

## Key Patterns

### Kernel Launch Configuration

```cuda
// Query device for optimal configuration
void launch_optimized(const float* input, float* output, int n) {
    int block_size;
    int min_grid_size;

    // Let the runtime suggest optimal block size for maximum occupancy
    cudaOccupancyMaxPotentialBlockSize(
        &min_grid_size, &block_size, my_kernel, 0, n);

    int grid_size = (n + block_size - 1) / block_size;
    my_kernel<<<grid_size, block_size>>>(input, output, n);
    CUDA_CHECK_KERNEL();
}
```

### Coalesced Memory Access

```cuda
// BAD: Strided access -- adjacent threads access non-adjacent memory
// Each warp issues 32 separate memory transactions
__global__ void transpose_naive(const float* in, float* out, int W, int H) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;
    if (x < W && y < H) {
        out[x * H + y] = in[y * W + x];  // Write is strided
    }
}

// GOOD: Use shared memory to coalesce both reads and writes
__global__ void transpose_coalesced(
    const float* in, float* out, int W, int H
) {
    __shared__ float tile[32][33]; // +1 padding avoids bank conflicts

    int x = blockIdx.x * 32 + threadIdx.x;
    int y = blockIdx.y * 32 + threadIdx.y;

    if (x < W && y < H) {
        tile[threadIdx.y][threadIdx.x] = in[y * W + x]; // Coalesced read
    }
    __syncthreads();

    x = blockIdx.y * 32 + threadIdx.x;
    y = blockIdx.x * 32 + threadIdx.y;

    if (x < H && y < W) {
        out[y * H + x] = tile[threadIdx.x][threadIdx.y]; // Coalesced write
    }
}
```

### Shared Memory Tiling

```cuda
// Dot product of two vectors using shared memory reduction
__global__ void dot_product(
    const float* a, const float* b, float* result, int n
) {
    __shared__ float cache[256];

    int tid = threadIdx.x;
    int idx = blockIdx.x * blockDim.x + threadIdx.x;

    // Each thread computes its partial sum via grid-stride
    float partial = 0.0f;
    for (int i = idx; i < n; i += blockDim.x * gridDim.x) {
        partial += a[i] * b[i];
    }
    cache[tid] = partial;
    __syncthreads();

    // Tree reduction in shared memory
    for (int s = blockDim.x / 2; s > 0; s >>= 1) {
        if (tid < s) {
            cache[tid] += cache[tid + s];
        }
        __syncthreads();
    }

    if (tid == 0) {
        atomicAdd(result, cache[0]);
    }
}
```

### Warp-Level Primitives (CUDA 9+)

```cuda
// Warp-level reduction using shuffle instructions -- no shared memory needed
__device__ float warp_reduce_sum(float val) {
    for (int offset = warpSize / 2; offset > 0; offset /= 2) {
        val += __shfl_down_sync(0xFFFFFFFF, val, offset);
    }
    return val;
}

// Block-level reduction combining warp shuffles and shared memory
__device__ float block_reduce_sum(float val) {
    __shared__ float warp_sums[32]; // One slot per warp (max 32 warps/block)

    int lane = threadIdx.x % warpSize;
    int warp_id = threadIdx.x / warpSize;

    val = warp_reduce_sum(val);

    if (lane == 0) {
        warp_sums[warp_id] = val;
    }
    __syncthreads();

    // First warp reduces the warp sums
    int num_warps = (blockDim.x + warpSize - 1) / warpSize;
    val = (threadIdx.x < num_warps) ? warp_sums[threadIdx.x] : 0.0f;
    if (warp_id == 0) {
        val = warp_reduce_sum(val);
    }

    return val;
}
```

## Performance

### Occupancy Calculator

```cuda
// Query occupancy at compile time for tuning
void report_occupancy() {
    int block_size = 256;
    int num_blocks;

    cudaOccupancyMaxActiveBlocksPerMultiprocessor(
        &num_blocks, my_kernel, block_size, 0);

    cudaDeviceProp prop;
    cudaGetDeviceProperties(&prop, 0);

    int active_warps = num_blocks * (block_size / prop.warpSize);
    int max_warps = prop.maxThreadsPerMultiProcessor / prop.warpSize;
    float occupancy = (float)active_warps / max_warps;

    printf("Occupancy: %.1f%% (%d/%d warps)\n",
           occupancy * 100, active_warps, max_warps);
}
```

### Nsight Profiling Workflow

```bash
# System-level trace: find CPU/GPU idle gaps, stream concurrency
nsys profile -o trace ./program
nsys stats trace.nsys-rep

# Kernel-level analysis: roofline, memory throughput, occupancy
ncu --set full -o kernel_report ./program
ncu -i kernel_report.ncu-rep    # Open in Nsight Compute GUI

# Quick single-metric check
ncu --metrics sm__throughput.avg.pct_of_peak_sustained_elapsed ./program
```

### Memory Bandwidth Measurement

```cuda
// Measure effective bandwidth of a kernel
void measure_bandwidth(int n) {
    size_t bytes = 2 * n * sizeof(float); // Read A + Write B

    cudaEvent_t start, stop;
    CUDA_CHECK(cudaEventCreate(&start));
    CUDA_CHECK(cudaEventCreate(&stop));

    CUDA_CHECK(cudaEventRecord(start));
    copy_kernel<<<grid, block>>>(d_in, d_out, n);
    CUDA_CHECK(cudaEventRecord(stop));
    CUDA_CHECK(cudaEventSynchronize(stop));

    float ms = 0;
    CUDA_CHECK(cudaEventElapsedTime(&ms, start, stop));

    float gb_per_sec = bytes / (ms * 1e6);
    printf("Effective bandwidth: %.2f GB/s\n", gb_per_sec);

    CUDA_CHECK(cudaEventDestroy(start));
    CUDA_CHECK(cudaEventDestroy(stop));
}
```

## Tooling

### Essential Commands

```bash
# Compile CUDA code
nvcc -arch=sm_80 -O3 -o program main.cu         # Single file
nvcc -arch=native -lineinfo -o program main.cu   # With debug line info

# CMake build
cmake -B build -DCMAKE_CUDA_ARCHITECTURES="70;80;86"
cmake --build build -j$(nproc)

# Runtime debugging
compute-sanitizer ./program                      # Memory errors (replaces cuda-memcheck)
compute-sanitizer --tool racecheck ./program     # Shared memory race conditions
compute-sanitizer --tool initcheck ./program     # Uninitialized device memory reads
compute-sanitizer --tool synccheck ./program     # Synchronization errors

# Profiling
nsys profile ./program                           # System-level timeline
ncu ./program                                    # Kernel-level metrics
ncu --kernel-name my_kernel --launch-skip 2 --launch-count 1 ./program

# Device info
nvidia-smi                                       # GPU status and memory usage
nvcc --version                                   # CUDA compiler version
```

### CMakeLists.txt Template

```cmake
cmake_minimum_required(VERSION 3.18)
project(myproject LANGUAGES CXX CUDA)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CUDA_STANDARD 17)
set(CMAKE_CUDA_ARCHITECTURES 70 80 86)
set(CMAKE_CUDA_SEPARABLE_COMPILATION ON)

find_package(CUDAToolkit REQUIRED)

add_library(kernels src/kernels.cu)
target_include_directories(kernels PUBLIC include)

add_executable(main src/main.cpp)
target_link_libraries(main kernels CUDA::cudart)

enable_testing()
add_executable(tests tests/test_kernels.cu)
target_link_libraries(tests kernels CUDA::cudart)
add_test(NAME gpu_tests COMMAND tests)
```

## References

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- Tiled matrix multiply, parallel reduction tree, stream overlap pipeline

## External References

- [CUDA C++ Programming Guide](https://docs.nvidia.com/cuda/cuda-c-programming-guide/)
- [CUDA C++ Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/)
- [Nsight Compute Documentation](https://docs.nvidia.com/nsight-compute/)
- [Nsight Systems Documentation](https://docs.nvidia.com/nsight-systems/)
- [Thrust Documentation](https://nvidia.github.io/cccl/thrust/)
- [CUDA Samples](https://github.com/NVIDIA/cuda-samples)
- [NVIDIA Occupancy Calculator](https://docs.nvidia.com/cuda/cuda-occupancy-calculator/)
- [GPU Memory Hierarchy (GTC talk)](https://developer.nvidia.com/blog/tag/cuda/)
