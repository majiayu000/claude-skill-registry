---
name: hip-rocm
description: 'Use when writing HIP kernels with hipcc, porting CUDA code through HIPIFY, profiling with rocprofv3, debugging with rocgdb, or optimizing for MI300X. Not for NVIDIA-side kernels: use cuda.'
---

# HIP and ROCm

## Contract

| Field | Bound contract |
|---|---|
| Trigger | AMD GPU work: HIP kernel authoring, CUDA porting with HIPIFY, ROCm toolchain setup, rocprofv3 profiling, rocgdb debugging, or MI300X tuning. |
| Authority | Read-only. The skill emits guidance, code, and commands; it writes no files. Nothing to roll back. No remote mutation. |
| Side effect | Guidance, ported code samples, build commands, and tool invocations for the user to run. |
| Done | A build command targeting a named `gfx` arch, a port plan or review, and AMD-side profiling and debugging commands exist for the code in question. |

## Inputs

1. Task (required): new HIP kernel, CUDA port, profiling, debugging, or tuning.
2. GPU (required): `rocminfo` or `rocm-smi` output naming the device; MI300X is `gfx942`.
3. ROCm version (required if not inferrable): `hipcc --version`. Grounded current stable: ROCm 10.0.0 (2026-08-26).
4. CUDA source (required for ports): the `.cu` files and their CUDA toolkit usage.

## Procedure

1. Verify the stack. Install the ROCm packages for the distribution, then confirm:

```bash
rocminfo | head -30
hipconfig --version
hipcc --version
rocm-smi
```

Device access needs the user in the `render` (and usually `video`) group. Export `HIP_PLATFORM=amd`. Pick the arch per build with `--offload-arch`, not the deprecated `AMDGPU_TARGETS` variable. Done when: `rocminfo` lists the GPU and the arch string is recorded.
2. Write the kernel. HIP mirrors CUDA: same `__global__`, same builtins, same `__syncthreads()`, `hipMalloc` and `hipMemcpy` in place of the `cuda` calls:

```cpp
// vector_add.hip
#include <hip/hip_runtime.h>

__global__ void vector_add(const float *a, const float *b, float *c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n)
        c[i] = a[i] + b[i];
}

int main(void) {
    const int n = 1 << 20;
    size_t bytes = n * sizeof(float);
    float *d_a, *d_b, *d_c;
    hipMalloc(&d_a, bytes);
    hipMalloc(&d_b, bytes);
    hipMalloc(&d_c, bytes);

    int threads = 256;
    int blocks = (n + threads - 1) / threads;
    hipLaunchKernelGGL(vector_add, dim3(blocks), dim3(threads), 0, 0,
                       d_a, d_b, d_c, n);
    hipDeviceSynchronize();

    hipFree(d_a); hipFree(d_b); hipFree(d_c);
    return 0;
}
```

```bash
hipcc -O3 --offload-arch=gfx942 -o vector_add vector_add.hip
```

`hipLaunchKernelGGL` is the portable form; hipcc also accepts the CUDA `<<<blocks, threads>>>` syntax. Check launches with `hipGetLastError()`. Done when: the kernel builds for the recorded arch and both error checks exist.
3. Port CUDA with HIPIFY. Assess before converting, convert in place, review the diff:

```bash
hipexamine-perl.sh cuda_project/          # report conversion scope
hipconvertinplace-perl.sh cuda_project/   # hipify-perl engine; text-level
hipconvertinplace.sh cuda_project/        # hipify-clang engine; AST-level, needs CUDA headers
```

Both wrappers keep a `.prehip` backup of each converted file. Single-file conversion runs `hipify-perl file.cu > file.hip` or `hipify-clang -inplace main.cu`. Core API mappings are one-for-one (`cudaMalloc` to `hipMalloc`, `cudaMemcpyAsync` to `hipMemcpyAsync`, `cudaStream_t` to `hipStream_t`). Expect manual work for cooperative groups and texture references. Done when: the code compiles under hipcc and every unconverted CUDAism is listed.
4. Select hipcc flags per purpose:

```bash
hipcc --offload-arch=gfx942 -O3 -o app main.hip                 # one arch
hipcc --offload-arch=gfx90a --offload-arch=gfx942 -o app main.hip  # fat binary
hipcc -g -O0 --offload-arch=gfx942 -o app_debug main.hip        # debug
hipcc -lrocblas -o app main.hip                                 # link rocBLAS
```

Done when: the build command names every target arch the fleet needs.
5. Profile with the ROCm profiler. Quick stats first, then metric collection:

```bash
rocprof --stats ./app
rocprofv3 --kernel-trace -- ./app
```

Read VALU utilization for compute activity, LDS bank conflict counters for shared memory stalls, and HBM throughput against the part's peak. Done when: each hot kernel has a named limiting resource.
6. Debug with rocgdb. Build with `-g -O0`, then use standard GDB commands; GPU waves appear in `info threads` as `AMDGPU Wave` target IDs:

```bash
rocgdb ./app_debug
```

```gdb
(rocgdb) break vector_add
(rocgdb) run
(rocgdb) info threads        # host threads plus AMDGPU Wave entries
(rocgdb) thread 4            # focus one wave
(rocgdb) info agents         # devices in the session
(rocgdb) info dispatches     # kernel dispatch state
(rocgdb) print i
```

Done when: the faulting wave is identified and its variables are inspected.
7. Tune for MI300X with its hardware facts: 64-lane wavefronts, 64 KB of LDS per CU, and about 5.3 TB/s of HBM3e peak bandwidth:

| Lever | Action |
|---|---|
| Wavefront width | Start reduction shuffles at offset 32, not 16 |
| LDS | Tile through the 64 KB budget; pad to break bank conflicts |
| Bandwidth | Coalesce every hot access; measure against the 5.3 TB/s figure |
| Matrix work | rocBLAS or hipBLASLt for GEMM; MFMA intrinsics for custom kernels |
| Atomics | `-munsafe-fp-atomics` relaxes atomic safety for speed; use only where the access pattern is provably safe |

```cpp
__device__ float wavefront_reduce_sum(float val) {
    // 64-lane wavefront: start at half width
    for (int offset = 32; offset > 0; offset >>= 1)
        val += __shfl_down(val, offset);
    return val;
}
```

Done when: block sizes are multiples of 64 and each tuning change names the hardware limit it addresses.
8. Map libraries by role: cuBLAS to rocBLAS or hipBLAS, cuDNN to MIOpen, NCCL to RCCL, Thrust to hipCUB, cuFFT to rocFFT. Done when: every NVIDIA library dependency has an AMD counterpart named.

## Failure and recovery

| Failure class | Behavior |
|---|---|
| `hipErrorNoDevice` | Driver not loaded or no device permission. Check `rocm-smi`; add the user to `render`. |
| Wrong-arch binary | `--offload-arch` does not match the device. Re-read `rocminfo` and rebuild. |
| Incomplete hipify port | CUDA-specific APIs remain. Port cooperative groups and texture references by hand. |
| Slower than the CUDA reference | 64-lane wavefronts change reduction and block shape. Retune to multiples of 64 and re-measure. |
| `HSA_STATUS_ERROR` | Device busy or out of memory. Check `rocm-smi --showmeminfo`; shrink allocations. |
| rocprof writes nothing | No kernels launched. Verify `hipGetLastError()` after each launch. |

## Output

A build command for the recorded arch, the port plan or review with unconverted APIs listed, profiling commands with their reading guide, and debugging commands for the fault. Each claim names the ROCm release it assumes.
