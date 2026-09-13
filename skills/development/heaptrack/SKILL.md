---
name: heaptrack
description: 'Use when tracking heap allocations on Linux with heaptrack: allocation hotspots, peak heap, temporary allocations, leaks, or a diff of two runs via heaptrack_print. Not for heap errors: use valgrind.'
---

# heaptrack

heaptrack (1.5.0 on the grounding host) intercepts `malloc`, `free`, `realloc`, and the C++ allocation operators through `LD_PRELOAD` or injection, records a backtrace per allocation, and compresses the trace to one file. `heaptrack_print` reads that file into four rankings: most calls, peak consumption, most temporary allocations, and leaks. It needs no rebuild and runs far faster than Valgrind's Massif.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A program uses too much memory, allocates too often, or leaks, and the user wants the allocating call stacks; or two builds must be compared for allocation behavior. |
| Authority | Reversible local: writes only heaptrack data files (`heaptrack.<prog>.<pid>.zst` or the `-o` target), `heaptrack_print` output files, and the test binary in the working directory; rollback is deleting them. No remote mutation. |
| Side effect | Data files on disk. The traced program runs slower while every allocation is unwound and logged. |
| Done | The report names the top call stacks by peak bytes, by call count, and by temporary allocations, lists the leak records with their stacks, and, for a comparison, the per-stack delta between the two runs. |

## Inputs

- Target binary with debug info (`-g`, or a `RelWithDebInfo` CMake build) so backtraces carry function names and source lines. Optimization level stays as in production.
- A representative workload; heaptrack records allocation counts, so the workload must exercise the suspected path.
- For Rust: the binary must use the system allocator (`#[global_allocator] static A: std::alloc::System = System;`) so the interposed `malloc` sees every allocation.
- For a comparison: two recorded data files.

## Procedure

1. Record. `heaptrack ./myapp args` writes `heaptrack.myapp.<pid>.zst` in the current directory and prints the analyze command on exit; `heaptrack -o run1 ./myapp` names the file `run1.zst`; `heaptrack -p <pid>` attaches to a running process by injection; `--record-only` skips the automatic analysis launch. Done when: the `.zst` file exists and heaptrack printed its summary lines (`calls to allocation functions`, `temporary allocations`).
2. Print the summary and rankings. `heaptrack_print -f run1.zst` prints, in order, `MOST CALLS TO ALLOCATION FUNCTIONS`, `PEAK MEMORY CONSUMERS`, `MOST TEMPORARY ALLOCATIONS`, and a summary block:

   ```text
   total runtime: 2.34s.
   calls to allocation functions: 145234 (62064/s)
   temporary allocations: 89123 (38087/s)
   peak heap memory consumption: 45.23M
   peak RSS (including heaptrack overhead): 78.45M
   total memory leaked: 2.34M
   ```

   Each ranking entry reads `N calls to allocation functions with X peak consumption from` followed by the stack, leaf first. Toggle sections with `-p 0` (peaks), `-a 0` (allocation counts), `-T 0` (temporary), and `-l 1` (leaks, off by default); `-n 20` widens the number of reported peaks from the default 10, `-s` limits sub-peak backtraces. `-t 1` shortens template identifiers and `-m 1` merges backtraces (both on by default). Done when: the four rankings and the summary are captured.
3. Read each summary line against the code. `calls to allocation functions` high relative to work done: many small allocations, so pool or reserve. `temporary allocations` (freed before the next allocation) as a large share of calls: churn in a hot loop, so hoist the buffer. `peak heap memory consumption`: the live-heap maximum to compare with the memory budget. `peak RSS` includes heaptrack's own overhead and non-heap mappings, so compare peak heap between runs, not RSS. `total memory leaked`: bytes never freed at exit; the `-l 1` ranking names the stacks. Done when: each non-trivial line is tied to a call stack.
4. Draw the allocation flamegraph. `heaptrack_print -f run1.zst -F stacks.folded --flamegraph-cost-type peak` writes folded stacks (cost types: `allocations`, `temporary`, `leaked`, `peak`); then `flamegraph.pl --countname bytes --title "Peak heap" stacks.folded > heap.svg` from `flamegraphs`. Done when: the SVG opens and the widest frame matches the top ranking entry.
5. Compare two runs with the built-in diff: `heaptrack_print -f after.zst -d before.zst` prints every ranking as the delta of `after` minus `before`, so a positive peak entry is a regression and a negative one an improvement. Done when: the top positive and top negative deltas are named with their stacks.
6. Export to Massif format when a Massif-reading tool is already in the workflow: `heaptrack_print -f run1.zst -M run1.massif`, then `ms_print run1.massif`. Done when: `ms_print` renders the timeline.
7. Suppress known leaks from third-party code: write a suppression file with one `leak:<function pattern>` line per pattern and pass `--suppressions leaks.supp`; `--print-suppressions 1` lists the matches and the suppressed byte total; `--disable-builtin-suppressions` reveals what heaptrack hides by default. Done when: the leak ranking holds only owned code.

## Failure and recovery

| Failure | Cause | Fix |
|---|---|---|
| Stacks show only addresses | No debug info | Rebuild with `-g`; for Rust add `debug = true` to the profile |
| Rust program records almost nothing | Custom global allocator bypasses `malloc` | Switch to `std::alloc::System` for the profiling build |
| `total memory leaked` is large but the program frees on exit paths | Exit through `_exit` or `quick_exit` skipped destructors | Read the leak stacks; a still-referenced global at exit is not a bug, and a suppression records that decision |
| Data file is huge | Allocation-heavy workload | Shorten the workload; record only the phase under suspicion by attaching with `-p` after startup |
| `heaptrack -p` fails to attach | ptrace restricted | Run as the process owner or propose `CAP_SYS_PTRACE`; otherwise start the program under heaptrack |
| Comparison shows every stack changed | Different workloads or non-deterministic addresses in symbols | Use identical inputs and `-m 1`; compare peak heap totals first |

Massif reaches the same heap questions on platforms without heaptrack and at a much higher slowdown; `valgrind` covers it. Leak detection without profiling cost is LeakSanitizer through `sanitizers`.

## Output

An allocation report with the summary block, the top stacks by peak, by call count, and by temporary allocations, the leak records, the flamegraph path when drawn, the per-stack deltas when two runs were compared, and the data file paths.
