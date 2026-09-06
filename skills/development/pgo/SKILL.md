---
name: pgo
description: 'Use when a C or C++ binary needs profile-guided optimization with GCC or Clang: instrumented or sampled profiles, merging, the two-stage build, or BOLT. Not for base flags: use gcc or clang.'
---

# Profile-guided optimization

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user asks how to apply PGO, how `-fprofile-generate` and `-fprofile-use` fit together, how to collect a representative profile, or how BOLT differs from PGO. |
| Authority | Read-only. The skill emits the build sequence, collection commands, and a measurement plan to chat; the user runs them. Rollback is not needed. No remote mutation. |
| Side effect | Chat output. |
| Done | A two-stage build sequence for the user's compiler is reported with the profile format named, the workload checklist is applied, and the speedup claim rests on a before-and-after measurement command rather than a number. |

## Inputs

- Compiler and version: required. GCC 16.2 or Clang 23.1.0 are current stable; each has its own profile format.
- A representative workload the instrumented binary can run: required.
- Build system: required for wiring; CMake shown below.
- Whether `perf` with branch sampling is available: required for SamplePGO and BOLT.
- Baseline flags already in use: required; PGO layers on `-O2` or `-O3`.

## Procedure

1. Decide whether PGO applies. Standard optimization comes first: `-O2` or `-O3`, and `-march=` for the deployment CPU. PGO pays off on code where static heuristics guess wrong: branch-heavy paths, many hot and cold functions, call-heavy code where inlining decisions matter. Do not promise a percentage; the gain is measured in step 7. Done when: the user knows PGO is a candidate and what will decide it.
2. Run the GCC flow. Instrument: `gcc -O2 -fprofile-generate -fprofile-dir=./pgo-data prog.c -o prog`. Run the workload; `.gcda` files land in `./pgo-data/`. Rebuild: `gcc -O2 -fprofile-use -fprofile-dir=./pgo-data -fprofile-correction prog.c -o prog`. Keep the same output name in both builds, because GCC derives the `.gcda` file name from the object name and a renamed second build reports `-Wmissing-profile`. `-fprofile-correction` reconciles counts from multi-threaded runs; include it. Done when: the three commands share one output name.
3. Run the Clang instrumented flow. Instrument: `clang -O2 -fprofile-instr-generate prog.c -o prog_instr`. Run the workload; it writes `default.profraw`, or per-process files with `LLVM_PROFILE_FILE="prog-%p.profraw"`. Merge: `llvm-profdata merge -output=prog.profdata *.profraw`. Rebuild: `clang -O2 -fprofile-instr-use=prog.profdata prog.c -o prog_pgo`. Weight workloads with `-weighted-input=3,a.profraw -weighted-input=1,b.profraw`; inspect with `llvm-profdata show --all-functions prog.profdata`; compare two profiles with `llvm-profdata overlap a.profdata b.profdata`. Done when: the merged `.profdata` exists and the rebuild command names it.
4. Add context-sensitive PGO when inlining decisions matter: take the stage-1 `.profdata`, build `clang -O2 -fprofile-use=stage1.profdata -fcs-profile-generate`, run the workload, merge the new `.profraw` files into `cs.profdata`, and build the final binary with `-fprofile-use=cs.profdata`. Done when: the second-stage profile feeds the final build.
5. Use sampling when instrumentation overhead is unacceptable. Build with `-fno-omit-frame-pointer`, record `perf record -b -e cycles:u ./prog < workload`, convert `perf script -F ip,brstack > perf.script`, then `llvm-profgen --binary=./prog --perfscript=perf.script --output=prog.profdata`, and rebuild with `-fprofile-sample-use=prog.profdata`. GCC's sampling counterpart is `-fauto-profile=<file>` with a profile converted from `perf` data. Done when: the sample profile feeds the rebuild.
6. Apply BOLT after PGO when instruction-cache layout is the remaining cost. Link with `-Wl,--emit-relocs`. Collect `perf record -e cycles:u -j any,u -o perf.data -- ./prog < workload`, convert `perf2bolt -p perf.data -o perf.fdata ./prog`, or instrument with `llvm-bolt prog -instrument -o prog.instr` and run it (profile lands in `/tmp/prof.fdata`). Optimize: `llvm-bolt prog -o prog.bolt -data=perf.fdata -reorder-blocks=ext-tsp -reorder-functions=cdsort -split-functions -split-all-cold -split-eh -dyno-stats`. GCC 8 and later need `-fno-reorder-blocks-and-partition` at compile time for BOLT. Done when: the BOLT binary exists.
7. Measure. `hyperfine --runs 5 "./prog_baseline < workload" "./prog_pgo < workload" --export-markdown results.md`, or `perf stat` on each binary. Report the measured ratio and the noise across runs; a PGO or BOLT build that does not beat the baseline on the deployment workload is discarded. Done when: the numbers come from the user's workload.
8. Wire CMake with two options, `PGO_INSTRUMENT` adding `-fprofile-instr-generate` to compile and link options and `PGO_USE` adding `-fprofile-instr-use=<path>` to both, driven by two configure-build cycles into separate build directories. Done when: the two build directories and the profile path are named.

## Failure and recovery

| Failure class | Behavior |
|---|---|
| Workload not representative | Apply the checklist: covers the hot paths, runs long enough to exercise them, weights production scenarios higher, excludes debug builds and one-off startup unless startup matters. A tiny synthetic benchmark trains the wrong layout. |
| `-Wmissing-profile` from GCC | The second build's object name differs from the first; use one output name. |
| `perf record -b` unsupported | The CPU or VM lacks branch sampling; use instrumented PGO instead of SamplePGO and BOLT. |
| `llvm-bolt` not installed | BOLT builds as an LLVM project (`-DLLVM_ENABLE_PROJECTS=bolt`); report it missing rather than substituting. |
| Profile format mismatch | `-fprofile-instr-*` and `-fprofile-generate`/`-fprofile-use` are different formats in Clang; do not mix them across stages. |

## Output

A chat report with the ordered build, run, merge, and rebuild commands for the user's compiler, the optional CS-PGO, SamplePGO, and BOLT steps when they apply, the workload checklist verdict, and the measurement command whose result decides whether the build ships.
