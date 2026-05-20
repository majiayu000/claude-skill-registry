---
name: nsys-optimizer
description: >
  Optimize CUDA/GPU simulation code using NVIDIA Nsight Systems (nsys) profiling.
  Use this skill whenever the user mentions performance problems, slow simulations,
  profiling, nsys, Nsight Systems, kernel optimization, GPU bottlenecks, or wants
  to speed up CUDA code. Also trigger when the user compares two scenes and one is
  unexpectedly slower, or asks "why is this slow?" about GPU code. This skill
  covers the full optimization loop: profiling, bottleneck diagnosis, targeted
  optimization, verification, and iterative measurement.
---

# CUDA Performance Optimization with nsys

This skill guides systematic GPU performance optimization using NVIDIA Nsight Systems profiling. The methodology is: **profile → diagnose → understand the algorithm → optimize → re-profile → verify correctness**, repeated until the target performance is achieved.

The core philosophy: profiling data tells you *what* is slow, but understanding the algorithm (from papers, docs, or code comments) tells you *why* it's slow and *how* to fix it correctly. Both are essential.

## Phase 1: Establish Baselines

### Create or adapt example scenes

Before profiling, ensure you have appropriate test scenes. Be proactive here — don't just use whatever the user gives you. Think about what scenes would best expose the bottleneck:

- **If comparing two configurations** (e.g., rigid vs deformable): create minimal, matched scenes that isolate the difference. Strip away unnecessary complexity (visualization, extra objects) and use headless mode.
- **If investigating a single slow scene**: create a simplified version that reproduces the slowness faster (fewer timesteps, smaller domain) while preserving the hot path.
- **If the bottleneck is unclear**: create multiple scene variants that stress different subsystems (contact detection, force accumulation, BVH construction, etc.) to narrow down which subsystem is the culprit.
- **For A/B testing optimizations**: create a scene that amplifies the specific bottleneck you're targeting, so improvements are clearly measurable.

When modifying example scripts for profiling:
- Set `DISPLAY=` (empty) to force headless mode — no GPU resources wasted on rendering
- Reduce step count to the minimum needed for meaningful profiling (enough to amortize startup, typically 50-100 steps)
- Print wall-clock time or summary stats at the end for quick sanity checks
- Keep the original script untouched; create a copy or a new file for profiling variants

### Profile with nsys

Run nsys profile sequentially (never in parallel — GPU resource contention corrupts timing data):

```bash
DISPLAY= nsys profile --stats=true -o /tmp/profile_baseline -f true \
    python examples/your_scene.py 2>&1 | tee /tmp/profile_baseline.log
```

Key flags:
- `--stats=true`: print summary statistics after capture
- `-o <path>`: output file path (without .nsys-rep extension)
- `-f true`: overwrite existing output
- `DISPLAY=` (empty string): force headless mode, prevent GPU rendering overhead

If comparing two configurations, profile them **sequentially** and save to separate files.

### Extract timing data

Use `nsys stats` to get structured timing data:

```bash
nsys stats /tmp/profile_baseline.nsys-rep 2>&1
```

This produces several tables. Focus on:
1. **CUDA Kernel Statistics**: kernel name, total time, instances, avg/min/max duration
2. **CUDA API Statistics**: cudaMemcpy, cudaLaunchKernel, cudaDeviceSynchronize times
3. **NVTX Range Statistics** (if annotations exist): named code regions with timing

For deeper analysis, export to SQLite:

```bash
nsys export --type=sqlite /tmp/profile_baseline.nsys-rep
sqlite3 /tmp/profile_baseline.sqlite "SELECT name, (end-start)/1e6 as ms FROM NVTX_EVENTS ORDER BY ms DESC LIMIT 20;"
```

## Phase 2: Diagnose Bottlenecks

### Reading the profile data

Look for these patterns:

**Pattern 1: Synchronous transfers hiding GPU bottlenecks**
If `cudaMemcpy` (Host-to-Device or Device-to-Host) dominates wall time, it may be acting as an implicit sync point — the CPU waits for all prior GPU work to finish. The real bottleneck is often a slow kernel that launched *before* the memcpy. Look at which kernels precede the synchronous call.

**Pattern 2: Low-parallelism kernels**
If a kernel has high average duration but low instance count, it's likely under-utilizing the GPU. Check:
- Launch configuration: is it using enough threads/blocks?
- Is one thread doing serial work that could be parallelized across threads?
- Classic sign: kernel processes N elements but launches with <<<1, 1>>> or <<<num_objects, 1>>>

**Pattern 3: Excessive kernel launches**
Many tiny kernels can be bottlenecked by launch overhead. Look for kernels with very low average duration but very high instance count.

**Pattern 4: Memory-bound kernels**
If kernel compute time is low but total GPU time is high, memory access patterns may be the issue (uncoalesced access, cache thrashing).

### Add NVTX annotations to pinpoint issues

If the existing profiling annotations don't provide enough granularity, add more. This is the project's annotation pattern:

```cpp
#include "core/profiler.h"

// Wrap code regions:
AVBD_RANGE_PUSH("descriptive_label");
// ... code to measure ...
AVBD_RANGE_POP();

// For indexed ranges (inside loops):
char range_name[64];
snprintf(range_name, sizeof(range_name), "vbd_iteration_%d", iter);
AVBD_RANGE_PUSH(range_name);
// ... iteration body ...
AVBD_RANGE_POP();
```

Build with profiling enabled: `cmake .. -DAVBD_PROFILING=ON && make -j`

These compile to no-ops in normal builds, so feel free to add them liberally. Use descriptive labels:
- `"kernel_*"` for kernel launches
- `"bvh_*"` for BVH operations
- Plain names for CPU-side phases (`"detect_contacts"`, `"recolor"`)

After adding annotations, re-profile and examine NVTX ranges to see exactly where time is spent within high-level phases.

## Phase 3: Understand the Algorithm

Before optimizing, understand *what the code is supposed to do*. This prevents "optimizations" that silently break correctness.

### Cross-reference with papers and documentation

- Check `docs/` for paper PDFs and summaries (`.md` files)
- Check `CLAUDE.md` for architecture overview and key equations
- Check `reference/` for reference implementations
- Read code comments citing specific equations

Key things to understand before optimizing a kernel:
1. **What mathematical operation does this kernel perform?** (e.g., force accumulation, Schur complement solve, quaternion integration)
2. **What are the data dependencies?** Which values must be computed before others?
3. **What is the reduction structure?** Does the kernel reduce per-vertex quantities to per-body or global quantities?
4. **What are the correctness constraints?** (e.g., quaternion must stay unit-length, energy must be conservative)

This understanding directly informs the optimization strategy. For example, if a kernel accumulates per-vertex forces into a body-level force/torque (a reduction), you know you can parallelize the per-vertex work and use a parallel reduction — but you must preserve the summation semantics.

## Phase 4: Optimize

### Common CUDA optimization patterns

**Serial-to-parallel (most impactful for this codebase)**

When a kernel uses 1 thread per object but loops over many sub-elements (vertices, contacts, etc.), convert to 1 block per object with threads splitting the sub-element work:

```cuda
// BEFORE: 1 thread loops over all vertices
__global__ void kernel(int num_bodies, ...) {
    int b = blockIdx.x * blockDim.x + threadIdx.x;
    if (b >= num_bodies) return;
    for (int i = 0; i < num_verts[b]; i++) {
        // sequential work per vertex
    }
}
// Launch: <<<ceil(num_bodies/256), 256>>>

// AFTER: 1 block per body, threads split vertex work
__global__ void kernel(int num_bodies, ...) {
    int b = blockIdx.x;
    if (b >= num_bodies) return;
    for (int i = threadIdx.x; i < num_verts[b]; i += blockDim.x) {
        // parallel work per vertex
    }
}
// Launch: <<<num_bodies, 256>>>
```

**Parallel reduction with warp shuffle + shared memory**

When threads within a block must sum their results (e.g., per-vertex forces → body force):

```cuda
// Warp-level reduction
__device__ float warp_reduce_sum(float val) {
    for (int offset = warpSize / 2; offset > 0; offset /= 2)
        val += __shfl_down_sync(0xFFFFFFFF, val, offset);
    return val;
}

// Block-level reduction
__shared__ float shared[32];  // one slot per warp
float val = /* per-thread contribution */;
val = warp_reduce_sum(val);
int lane = threadIdx.x % warpSize;
int warp_id = threadIdx.x / warpSize;
if (lane == 0) shared[warp_id] = val;
__syncthreads();
// First warp reduces across warps
if (warp_id == 0) {
    val = (lane < blockDim.x / warpSize) ? shared[lane] : 0.0f;
    val = warp_reduce_sum(val);
}
// Thread 0 now has the total
```

**Shared memory for body-level quantities**

When thread 0 computes body-level values that all threads need:

```cuda
__shared__ float3 s_translation;
__shared__ float4 s_quaternion;
if (threadIdx.x == 0) {
    // compute body-level quantities
    s_translation = new_translation;
    s_quaternion = new_quaternion;
}
__syncthreads();
// All threads use s_translation, s_quaternion for vertex updates
```

### Making changes

- Make one optimization at a time. Don't batch multiple changes — if something breaks or doesn't help, you need to know which change caused it.
- Keep the original code nearby (commented or in version control) for reference during debugging.
- After each change, immediately re-profile AND run tests.

## Phase 5: Measure and Verify

### Statistically rigorous A/B profiling

Single-run profiling is unreliable due to GPU clock variance, thermal throttling, and OS scheduling noise. Use the repeated profiling scripts for statistically sound comparisons.

**Scripts location:** `~/.claude/skills/nsys-optimizer/scripts/`

**Step 1: Profile each condition multiple times**

```bash
# Build the "after" version, then profile it
cd build && cmake .. -DAVBD_PROFILING=ON && make -j && cd ..
python ~/.claude/skills/nsys-optimizer/scripts/nsys_repeat_profile.py \
    --cmd "python examples/your_scene.py" \
    --label after --runs 10 --outdir /tmp/nsys_ab

# Checkout the "before" version, rebuild, then profile it
git checkout HEAD~1
cd build && cmake .. -DAVBD_PROFILING=ON && make -j && cd ..
python ~/.claude/skills/nsys-optimizer/scripts/nsys_repeat_profile.py \
    --cmd "python examples/your_scene.py" \
    --label before --runs 10 --outdir /tmp/nsys_ab

# Switch back
git checkout -
```

`nsys_repeat_profile.py` options:
- `--runs N`: number of profiling runs (default: 10)
- `--warmup N`: warmup runs before profiling (default: 1, not profiled)
- `--outdir DIR`: output directory (default: `/tmp/nsys_ab`)
- `--label NAME`: condition label, creates a subdirectory
- `--nsys-extra FLAGS`: extra flags passed to `nsys profile`

Reports are saved as `<outdir>/<label>/run_00.nsys-rep` with `.sqlite` exports alongside.

**Step 2: Compare with statistical analysis**

```bash
python ~/.claude/skills/nsys-optimizer/scripts/nsys_compare.py \
    --baseline /tmp/nsys_ab/before \
    --optimized /tmp/nsys_ab/after \
    --metric "nvtx:step" \
    --metric "kernel:sim_vbd_solve_kernel" \
    --metric "cuda_api:cudaMalloc" \
    --metric "wall"
```

**Metric specification formats** (each `--metric` flag):

| Format | Description | Example |
|--------|-------------|---------|
| `nvtx:<name>` | Total time of NVTX range (exact match on text) | `nvtx:step` |
| `nvtx_avg:<name>` | Average per-instance NVTX range time | `nvtx_avg:detect_contacts` |
| `kernel:<substring>` | Total GPU time for matching kernels | `kernel:sim_vbd_solve_kernel` |
| `kernel_avg:<substring>` | Average per-instance kernel time | `kernel_avg:detect_ee_contacts_kernel` |
| `cuda_api:<name>` | Total CUDA API time (substring match) | `cuda_api:cudaMalloc` |
| `sql:<query>` | Custom SQL returning a single value in ns | `sql:SELECT SUM(end-start) FROM CUPTI_ACTIVITY_KIND_KERNEL` |
| `wall` | Wall-clock time (first to last NVTX event) | `wall` |

Additional options:
- `--baseline-label` / `--optimized-label`: custom display labels
- `--csv FILE`: write results to CSV

**Output** includes per-metric: mean, std, median, min, max for each condition, percent change, speedup ratio, and Welch's t-test (t-statistic, degrees of freedom, p-value) with significance assessment.

**Important notes on NVTX text matching:** The NVTX text field in the SQLite database does **not** include the colon prefix shown by `nsys stats`. For example, `nsys stats` displays `:step` but the actual text is `step`. Use `nvtx:step`, not `nvtx::step`.

### Single-run quick profiling

For quick exploratory profiling (not A/B comparisons), single runs are still useful:

```bash
cd build && cmake .. && make -j && cd ..
DISPLAY= nsys profile --stats=true -o /tmp/profile_optimized -f true \
    python examples/your_scene.py 2>&1 | tee /tmp/profile_optimized.log
```

### Verify correctness

Run the full test suite after every optimization:

```bash
python -m pytest tests/ -v
```

Tests may take several minutes — be patient (10+ minutes is normal for large test suites).

Also do a quick sanity check: run the original scene and verify the simulation output hasn't changed (e.g., final positions, contact counts). Small floating-point differences from reordering parallel reductions are acceptable; large behavioral changes are not.

## Phase 6: Iterate

After each optimization round:
1. Check if the original performance goal is met
2. If not, re-examine the new profile to find the next bottleneck
3. Consider creating a new scene variant that isolates the new bottleneck
4. Repeat Phases 2-5

Common iteration patterns:
- First pass fixes the obvious serial bottleneck (e.g., 1-thread kernel → parallel)
- Second pass addresses the newly-exposed bottleneck (e.g., memory-bound kernel, sync points)
- Third pass is usually diminishing returns — present findings and let the user decide whether to continue

## Quick Reference: nsys Commands

| Command | Purpose |
|---------|---------|
| `nsys profile --stats=true -o out -f true python script.py` | Profile and print stats |
| `nsys stats report.nsys-rep` | Reprint stats from existing profile |
| `nsys export --type=sqlite -o out.sqlite report.nsys-rep` | Export to SQLite for custom queries |
| `sqlite3 report.sqlite "SELECT ..."` | Query profile data |

## Quick Reference: Build with Profiling

```bash
cd build && cmake .. -DAVBD_PROFILING=ON && make -j
```

Remember to rebuild without profiling for final performance measurements, since NVTX calls (while lightweight) do add overhead.
