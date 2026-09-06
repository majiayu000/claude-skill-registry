---
name: openmp
description: 'Use when parallelizing loops or tasks with OpenMP: parallel for, schedules, reductions, data sharing, simd, target offload, OMP_* tuning, or false sharing. Not for multi-node work: use mpi.'
---

# OpenMP

OpenMP adds shared-memory parallelism to C, C++, and Fortran through `#pragma omp` directives, compiled in with `-fopenmp` on GCC and Clang. The runtime (libgomp on GCC 16.2, the grounding compiler) reads `OMP_*` variables at startup. Every command and directive below compiled and ran on GCC 16.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user parallelizes loops on a multicore CPU, needs a reduction or task graph, wants `simd` hints, offloads to a GPU with `target`, tunes thread count and binding, or has a program that scales badly or gives wrong answers under threads. |
| Authority | Reversible local: writes only source files and compiled binaries in the working directory; rollback is deleting them. Environment variables are set for the run, not persisted. No remote mutation. |
| Side effect | Source and binaries on disk; runs start `OMP_NUM_THREADS` threads. |
| Done | The parallel program gives the same result as the serial version, the timing with `omp_get_wtime` shows the speedup, every shared variable written by more than one thread is under a `reduction`, `atomic`, or `critical`, and thread placement is confirmed by `OMP_DISPLAY_ENV`. |

## Inputs

- Compiler with OpenMP support: `gcc -fopenmp`, `clang -fopenmp`. `-fopenmp-simd` enables only the `simd` directives without the threading runtime.
- Core count and topology (`lscpu`, `nproc`) to size threads and places.
- For offload: a GCC built with an offload target (`gcc -v` lists `OFFLOAD_TARGET_NAMES`), or a vendor compiler; `-foffload=nvptx-none` or `-foffload=amdgcn-amdhsa` selects it and `-foffload-options=<target>=<opts>` passes target flags such as `-march=sm_80`.
- The serial baseline result and timing, to check correctness and speedup.

## Procedure

1. Parallelize the hot loop with a reduction for the accumulator:

   ```c
   #include <omp.h>
   #include <stdio.h>

   int main(void) {
       const int n = 1000000;
       double sum = 0.0;
       double t0 = omp_get_wtime();
       #pragma omp parallel for reduction(+:sum)
       for (int i = 0; i < n; i++)
           sum += i * 0.001;
       printf("sum = %f threads = %d elapsed = %f s\n", sum, omp_get_max_threads(), omp_get_wtime() - t0);
       return 0;
   }
   ```

   `gcc -fopenmp -O2 -o omp_sum omp_sum.c && OMP_NUM_THREADS=8 ./omp_sum`. Done when: the result matches the serial run and the time falls with threads.
2. Choose the schedule from the iteration cost profile:

   | Clause | Use when |
   |---|---|
   | `schedule(static)` | Every iteration costs the same; lowest overhead |
   | `schedule(static, 1)` | Interleave iterations across threads for cache blocking |
   | `schedule(dynamic, 64)` | Iteration cost varies; chunks of 64 amortize the queue |
   | `schedule(guided)` | Cost decreases along the loop; chunk size shrinks |
   | `schedule(runtime)` | Read `OMP_SCHEDULE` at run time to compare without recompiling |

   Done when: the schedule matches the measured per-iteration cost and the timing confirms it.
3. Declare data sharing explicitly. `private(x)` gives each thread an uninitialized copy; `firstprivate(x)` copies the value in; `lastprivate(x)` copies the last iteration's value out; `shared(x)` is one variable for all threads; `reduction(op:x)` combines per-thread copies with `+`, `*`, `-`, `max`, `min`, `&`, `|`, `^`, `&&`, `||`. Add `default(none)` to force every variable to be listed and let the compiler catch the omission. A shared variable written by several threads outside a reduction needs `#pragma omp atomic` (one scalar update) or `#pragma omp critical` (a block). Done when: `default(none)` compiles and no unprotected shared write remains.
4. Vectorize with `simd`. `#pragma omp simd` before an inner loop asks the compiler to vectorize it; `#pragma omp parallel for simd` combines threads and vectors. Confirm with `-fopt-info-vec`, which prints `loop vectorized` with the vector width for each loop it handled. Done when: `-fopt-info-vec` reports the loop vectorized.
5. Use tasks for irregular or recursive work:

   ```c
   #pragma omp parallel
   {
       #pragma omp single
       {
           for (int i = 0; i < 10; i++) {
               #pragma omp task firstprivate(i)
               process_subtree(i);
           }
           #pragma omp taskwait
       }
   }
   ```

   `single` lets one thread create the tasks while the team executes them; `taskwait` joins the children. Done when: the task version produces the serial result.
6. Offload to a GPU when the loop is large enough to pay for the transfer:

   ```c
   #pragma omp target teams distribute parallel for map(to: a[0:n]) map(from: c[0:n])
   for (int i = 0; i < n; i++)
       c[i] = a[i] * 2.0f;
   ```

   Build with `gcc -fopenmp -foffload=nvptx-none -foffload-options=nvptx-none=-march=sm_80 -o offload offload.c` on a GCC with the nvptx offload compiler installed; `OMP_TARGET_OFFLOAD=MANDATORY` makes a missing device an error instead of a silent host fallback, and `OMP_DEFAULT_DEVICE=<n>` picks the device. Without an offload-enabled compiler the region runs on the host. `cuda` covers writing the kernel directly. Done when: `OMP_TARGET_OFFLOAD=MANDATORY` runs without error and the result matches.
7. Tune the runtime through the environment and print what it saw:

   ```bash
   export OMP_NUM_THREADS=16
   export OMP_PROC_BIND=close      # keep threads near the master
   export OMP_PLACES=cores         # one place per core
   export OMP_WAIT_POLICY=active   # spin instead of sleeping between regions
   export GOMP_SPINCOUNT=300000    # libgomp only: spins before a waiting thread sleeps
   export OMP_MAX_ACTIVE_LEVELS=2  # allow one level of nested parallelism (OMP_NESTED is deprecated)
   export OMP_DISPLAY_ENV=true     # print the effective settings at startup
   ```

   Done when: `OMP_DISPLAY_ENV=true` shows the intended values and the timing improves or the change is reverted.
8. Remove false sharing. Threads that write neighboring elements of one array (`sum_array[tid] += x`) bounce the same cache line between cores. Prefer a `reduction`; when per-thread slots are needed, pad each to a cache line (`double slots[MAX_THREADS][8]`, 64 bytes per row) or use `alignas(64)` on a per-thread struct. `cpu-cache-opt` covers measuring it. Done when: the per-thread accumulator version scales with threads.
9. Profile the parallel regions with Score-P: `scorep gcc -fopenmp -O2 -g -o app app.c`, run `./app`, and read `scorep-*/profile.cubex` with `scorep-score -r scorep-*/profile.cubex` (per-region time and visits) or the CUBE GUI; `SCOREP_ENABLE_TRACING=true` adds an OTF2 trace. TAU wraps the compiler as `tau_cc.sh -fopenmp -o app app.c` with `TAU_MAKEFILE` pointing at the configuration; the run writes `profile.*` files that `pprof` summarizes and `paraprof` displays. `intel-vtune-amd-uprof` shows OpenMP region efficiency in VTune's threading analysis. Done when: the region with the most time and the least parallel efficiency is named.

## Failure and recovery

| Failure | Cause | Fix |
|---|---|---|
| No speedup | Loop too small, or the parallel region is entered too often | Move the `parallel` outside the hot loop; add `if(n > threshold)` to the directive |
| Wrong result | Race on a shared variable | `default(none)` to find it; then `reduction`, `atomic`, or `critical` |
| Slower with more threads | False sharing or memory bandwidth ceiling | Pad per-thread data; check bandwidth with `hardware-counters` |
| Threads migrate or share cores | No binding | `OMP_PROC_BIND=close OMP_PLACES=cores`; confirm with `OMP_DISPLAY_ENV=true` |
| Offload silently runs on the host | Compiler lacks the offload target | `OMP_TARGET_OFFLOAD=MANDATORY` to make it fail loudly; install the offload compiler |
| Nested regions oversubscribe | Inner regions spawn full teams | `OMP_MAX_ACTIVE_LEVELS=1`, or size inner teams with `num_threads` |
| `simd` loop not vectorized | Loop-carried dependence or aliasing | Read the `-fopt-info-vec-missed` reason; add `restrict` or a `safelen` clause |

## Output

An OpenMP program whose parallel result matches the serial baseline, with the measured speedup from `omp_get_wtime`, the chosen schedule and data-sharing clauses, the `OMP_DISPLAY_ENV` output confirming placement, and, when profiled, the region with the most time and its parallel efficiency.
