---
name: valgrind
description: 'Use when running Valgrind Memcheck for heap errors, leaks, or uninitialised reads on an unmodified binary, or Cachegrind, Callgrind, or Massif profiling. Not for ASan builds: use address-sanitizer.'
---

# Valgrind

Valgrind (current stable 3.27.1) runs an unmodified binary on a synthetic CPU and instruments every memory access. Four tools matter here: Memcheck finds memory errors and leaks, Cachegrind simulates the cache, Callgrind records exact call counts and inclusive costs, and Massif samples the heap over time. Nothing needs recompiling, so Valgrind is the tool when the build cannot be changed or when uninitialised-value tracking is the question.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A native program corrupts the heap, leaks, reads uninitialised memory, or needs cache, call-count, or heap-growth profiling, and the user cannot or does not want to rebuild with sanitizers. |
| Authority | Reversible local: writes only Valgrind output files (`cachegrind.out.*`, `callgrind.out.*`, `massif.out.*`, `--log-file` targets, suppression files) and the test binary in the working directory; rollback is deleting them. No remote mutation. |
| Side effect | Output files on disk. The program runs 10 to 50 times slower under Memcheck (Valgrind's own figure), so long workloads need trimming. |
| Done | Each reported error is classified with its source line, each leak record carries its kind, and the exit code reflects the error count when `--error-exitcode` is set. Profiling runs end with an annotated report naming the top functions or the peak heap snapshot. |

## Inputs

- Target binary with debug info: build with `-g`. Memcheck works at any optimization level, but `-O0` or `-O1` gives the clearest line attribution; at `-O2` and above the compiler may hoist or fold loads and Memcheck's "conditional jump depends on uninitialised value" reports become harder to map to source.
- A representative, short workload. Memcheck's slowdown makes a full production run impractical.
- The question: correctness (Memcheck), instruction and cache cost per line (Cachegrind), who calls whom and how often (Callgrind), or heap size over time (Massif).
- Existing suppression files for third-party noise, when any.

## Procedure

1. Pick the tool from the question. Memcheck is the default (`--tool=memcheck` is implied). Done when: one tool is named.
2. Run Memcheck with the full flag set:

   ```bash
   valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes \
            --error-exitcode=1 ./prog args
   ```

   | Flag | Default | Effect |
   |---|---|---|
   | `--leak-check=full` | `summary` | Print each leak record with its stack |
   | `--show-leak-kinds=all` | `definite,possible` | Include indirectly lost and still reachable |
   | `--track-origins=yes` | `no` | Report where each uninitialised value was created (slower) |
   | `--error-exitcode=N` | `0` | Exit with `N` when errors were found; the CI hook |
   | `--log-file=<file>` | stderr | Write the report to a file |
   | `--suppressions=<file>` | none | Silence known reports |
   | `--gen-suppressions=yes` | `no` | Print a suppression block after each error |
   | `--num-callers=<n>` | `12` | Stack depth per report |
   | `--trace-children=yes` | `no` | Follow `execve` into child processes |
   | `--malloc-fill=<hex>` | off | Fill new allocations to expose reads of uninitialised heap |
   | `--free-fill=<hex>` | off | Fill freed blocks to expose use after free |
   | `--max-stackframe=<n>` | 2000000 | Raise when a large stack frame is misread as a stack switch |
   | `--xml=yes --xml-file=<f>` | off | Machine-readable output for CI parsers |

   Done when: the run ends with an `ERROR SUMMARY` line.
3. Read each Memcheck report by its first line. `Invalid read of size N` or `Invalid write of size N`: out-of-bounds or use after free; the `Address ... is N bytes after a block of size M alloc'd` line names the block. `Conditional jump or move depends on uninitialised value(s)`: a read before write; with `--track-origins=yes` the `Uninitialised value was created by` block names the allocation or stack frame. `Invalid free()` or `Mismatched free() / delete / delete []`: ownership or allocator mismatch. Done when: every distinct error context has a source line and a classification.
4. Read the leak summary by kind. `definitely lost`: no pointer to the block remains; a real leak. `indirectly lost`: reachable only through a definitely-lost block; fixing the root record clears it. `possibly lost`: only interior pointers remain; common with custom allocators and often benign. `still reachable`: a pointer exists at exit; never freed but not lost. For library code, `--show-leak-kinds=definite,indirect` drops the reachable noise. Done when: each leak record is assigned a kind and a decision (fix, suppress, ignore).
5. Suppress third-party noise. Run once with `--gen-suppressions=yes`, copy each `{ ... }` block into `valgrind.supp`, give it a name on the first line, and rerun with `--suppressions=valgrind.supp`. Suppress only frames outside the code under test. Done when: the rerun reports only errors in owned code.
6. Cachegrind, when the question is cost per line. Cache simulation is off by default (`--cache-sim=no`), so enable it: `valgrind --tool=cachegrind --cache-sim=yes ./prog`. Add `--branch-sim=yes` for branch mispredictions. Then `cg_annotate cachegrind.out.<pid>` prints per-function and per-line counts; `--annotate` (the default) adds source annotation and replaces the deprecated `--auto=yes`. Compare two runs with `cg_annotate --diff a.out b.out` or `cg_diff`. Columns: `Ir` instructions, `I1mr`/`ILmr` L1 and last-level instruction misses, `D1mr`/`DLmr` data read misses, `D1mw`/`DLmw` data write misses, `Bcm`/`Bim` conditional and indirect branch mispredictions. Done when: the top lines by the chosen column are listed.
7. Callgrind, when the question is who calls whom. `valgrind --tool=callgrind --callgrind-out-file=callgrind.out ./prog`, then `callgrind_annotate callgrind.out` for inclusive and self costs per function. `kcachegrind callgrind.out` opens the graphical call graph when installed. Callgrind counts every call exactly, needs no root, and runs slower than `perf` sampling; `linux-perf` is the tool when a sampling profile is enough. Done when: the top functions by inclusive cost and their callers are named.
8. Massif, when the question is heap size over time. `valgrind --tool=massif ./prog` writes `massif.out.<pid>`; `ms_print massif.out.<pid>` prints the timeline and the detailed snapshots with allocation trees. `--pages-as-heap=yes` measures all mapped pages instead of heap allocations; `--stacks=yes` adds stack usage. Done when: the peak snapshot and its top allocation sites are named.
9. Verify the fix by rerunning the same command and confirming `ERROR SUMMARY: 0 errors` and, with `--error-exitcode=1`, an exit status of `0`. Done when: the rerun is clean or the remaining errors are listed.

## Failure and recovery

| Failure | Behavior |
|---|---|
| Errors only in third-party frames | Suppress them (step 5); report the suppression file path and what it hides |
| No line numbers in stacks | Rebuild with `-g`; Valgrind cannot recover source lines without debug info |
| Run too slow to finish | Shorten the workload; drop `--track-origins`; reserve Memcheck for the failing path and use `address-sanitizer` for the broad suite |
| Cachegrind prints only `Ir` | Cache simulation was off; rerun with `--cache-sim=yes` |
| Program uses a custom allocator | Memcheck sees one large block; wrap the allocator with `VALGRIND_MALLOCLIKE_BLOCK` client requests from `valgrind/valgrind.h`, or test with the system allocator |
| Memcheck reports `Warning: client switching stacks?` | Large frame; raise `--max-stackframe` to the printed size |

Valgrind and AddressSanitizer both intercept `malloc`; running a sanitizer-instrumented binary under Valgrind is unsupported. Use one per run. `references/valgrind-vs-asan.md` states when each applies.

## Output

A Memcheck report with each error context classified and located, the leak summary by kind with a decision per record, the suppression file when one was written, the exit status from the verification rerun, and, for the profiling tools, the annotated report from `cg_annotate`, `callgrind_annotate`, or `ms_print` with the top entries and the output file paths.
