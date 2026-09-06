---
name: arm-sve
description: 'Use when writing or porting AArch64 SIMD to SVE or SVE2: arm_sve.h intrinsics, predicates, vector-length-agnostic loops, auto-vectorization, or SVE registers in GDB. Not for NEON: use simd-intrinsics.'
---

# Arm SVE and SVE2

## Contract

| Field | Bound contract |
|---|---|
| Trigger | AArch64 code needs vector-length-agnostic SIMD: a NEON loop is being ported, an `arm_sve.h` kernel is being written, auto-vectorization to SVE is being checked, or SVE register state is being inspected in GDB. |
| Authority | Reversible local: writes only the source files the user names; rollback is reverting them in version control. No remote mutation. |
| Side effect | New or edited C sources. Runs the binary on the host or under QEMU for verification. |
| Done | The kernel compiles with `-march=armv9-a+sve2`, produces the same result as the scalar reference for lengths that are not a multiple of the vector length, and runs correctly at two different vector lengths (hardware and QEMU, or two QEMU `sve<N>` settings). |

## Inputs

- Source loop or NEON kernel to port, with a scalar reference to compare against.
- Target machines and their SVE level: Graviton3 (Neoverse V1) has SVE, Graviton4 (Neoverse V2) has SVE2, Apple M1 through M3 have NEON only, Apple M4 has SME with streaming SVE and no non-streaming SVE.
- Compiler: GCC or Clang, and version (`gcc --version`, `clang --version`).
- GDB version if debugging (`gdb --version`).

## Procedure

1. Confirm the hardware and the compiler agree. Vector length (VL) is 128 to 2048 bits in 128-bit steps and is fixed per CPU; the code must not assume it. Done when: `/proc/cpuinfo` lists `sve` (and `sve2` if needed) and the compiler defines `__ARM_FEATURE_SVE` under the chosen `-march`.

   ```bash
   grep -o -m1 -E 'sve2?' /proc/cpuinfo
   clang --target=aarch64-linux-gnu -march=armv9-a+sve2 -dM -E - </dev/null | grep __ARM_FEATURE_SVE
   ```

2. Write the kernel with predicates instead of a scalar tail. `svwhilelt_b32(i, n)` is true for lanes with `i + lane < n`, so the last iteration is partial with no cleanup loop. `svcntw()` returns the 32-bit lanes per vector at runtime. Done when: the loop below matches the scalar `y[i] += alpha * x[i]` for `n = 0`, `n = 1`, `n = svcntw() - 1`, and `n = 3 * svcntw() + 1`.

   ```c
   #include <arm_sve.h>
   #include <stddef.h>

   void saxpy_sve(float *y, const float *x, float alpha, size_t n) {
       svbool_t pg = svwhilelt_b32((uint64_t)0, (uint64_t)n);
       size_t i = 0;
       do {
           svfloat32_t vx = svld1_f32(pg, &x[i]);
           svfloat32_t vy = svld1_f32(pg, &y[i]);
           vy = svmla_n_f32_x(pg, vy, vx, alpha);
           svst1_f32(pg, &y[i], vy);
           i += svcntw();
           pg = svwhilelt_b32((uint64_t)i, (uint64_t)n);
       } while (svptest_any(svptrue_b32(), pg));
   }
   ```

   ```bash
   gcc -march=armv9-a+sve2 -O3 -o saxpy saxpy.c
   ```

   Registers: `Z0` to `Z31` hold data, `P0` to `P15` hold predicates. `svcntb()` gives bytes per vector; `svcntw()` and `svcntd()` give 32-bit and 64-bit lane counts.

3. Pick the predication suffix on purpose. `_m` merges: inactive lanes keep the first operand's value. `_z` zeroes inactive lanes. `_x` leaves inactive lanes unspecified and lets the compiler pick the cheapest encoding. Loads and stores are always predicated, so a result only leaks through inactive lanes when an `_x` value is stored unpredicated or reduced. Done when: every intrinsic in the kernel has the suffix its consumer needs, and reductions over a partial vector use `_z` or a predicated reduction.

   | Intrinsic | Purpose |
   |---|---|
   | `svld1_f32(pg, ptr)` | Predicated load |
   | `svst1_f32(pg, ptr, v)` | Predicated store |
   | `svmul_f32_x(pg, a, b)` | Multiply |
   | `svmla_f32_x(pg, acc, a, b)` | Fused multiply-add |
   | `svwhilelt_b32(i, n)` | Predicate for the lanes still inside `n` |
   | `svcntw()` | 32-bit lanes per vector |
   | `svptrue_b32()` | All lanes active |
   | `svdot_s32(acc, a, b)` | Signed 8-bit dot product into 32-bit lanes; unpredicated, in base SVE |

4. Check auto-vectorization before hand-writing intrinsics. Both compilers vectorize simple loops to SVE at `-O3`; the remarks say so. Done when: the remark for the hot loop reports a `vscale` width, or the reason it failed is known.

   ```bash
   gcc   -march=armv9-a+sve2 -O3 -fopt-info-vec -c app.c
   clang -march=armv9-a+sve2 -O3 -Rpass=loop-vectorize -c app.c
   # clang prints: remark: vectorized loop (vectorization width: vscale x 4, ...)
   ```

   `#pragma omp simd` (with `-fopenmp-simd`) tells the compiler a loop has no loop-carried dependence when it cannot prove it.

5. Port a NEON loop. Replace the fixed stride (`i += 4`) with `svcntw()`, replace the scalar tail with a `svwhilelt` predicate, and pick `_m`, `_z`, or `_x` per step 3. Done when: the result matches the NEON version bit for bit for the same inputs, at every tested `n`.

6. Test at more than one vector length. QEMU's `max` CPU enables every SVE length by default; naming `sve<N>=on` properties enables only those lengths, and without KVM every smaller power-of-two length must be enabled too. The guest runs at the largest enabled length. Done when: the binary passes at VL 128 and at a larger VL.

   ```bash
   qemu-aarch64 -cpu max,sve128=on ./saxpy_test
   qemu-aarch64 -cpu max,sve128=on,sve256=on ./saxpy_test
   qemu-aarch64 -cpu max ./saxpy_test         # largest length QEMU supports
   ```

7. Debug SVE state in GDB. GDB has supported SVE on AArch64 Linux since version 8.2; the installed 17.2 does, and register width follows the VL of the running process. Done when: `p $z0` prints a union view of the vector and `p $p0` prints the predicate.

   ```
   (gdb) break saxpy_sve
   (gdb) run
   (gdb) p $z0
   (gdb) p $p0
   (gdb) info registers z0 z1 p0
   ```

8. Guard the build for non-SVE machines. Wrap the SVE path in `#if defined(__ARM_FEATURE_SVE)` with a NEON or scalar fallback, or dispatch at runtime on the `sve` feature bit. Done when: the same source builds and runs on an M1 and on a Graviton3.

## Failure and recovery

| Symptom | Cause | Fix |
|---|---|---|
| `SIGILL` on first SVE instruction | CPU without SVE (Apple M1 to M3), or M4 outside streaming mode | Check `/proc/cpuinfo` or `sysctl hw.optional.arm`; fall back to NEON. |
| Wrong values in the last vector | Inactive lanes from an `_x` operation were stored or reduced unpredicated | Use `_z` for the value feeding a reduction; keep stores predicated. |
| Slower than the NEON version | Very short arrays where the predicate setup dominates, or an unaligned store pattern | Measure with the array sizes the program uses; keep NEON or scalar for `n` below one vector when the measurement says so. |
| No vectorization remark | Unknown trip count with a possible alias, or floating-point reduction without `-ffast-math` | Add `restrict`, `#pragma omp simd`, or `-fno-trapping-math` after confirming the semantics allow it. |
| Build fails with SVE intrinsics on M3 | `-march` lacks `+sve` or the target has none | Guard with `__ARM_FEATURE_SVE`. |
| GDB prints no `z` registers | GDB older than 8.2, or the process is not on SVE hardware | Update GDB; run on SVE hardware or under QEMU with gdbstub. |

## Output

SVE source in the named files that matches the scalar reference at partial lengths and at two vector lengths, plus a note with the compiler remark for the hot loop and the machines the kernel was verified on.
