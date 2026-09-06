---
name: llvm
description: 'Use when working with LLVM IR as a user: emitting IR from clang, running opt passes, lowering with llc, reading IR, or finding a missed optimization. Not for writing new passes: use llvm-passes.'
---

# LLVM IR and tooling

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user wants to see the IR for a function, run or inspect optimization passes with `opt`, lower IR to assembly with `llc`, read an IR construct, or find out why a transform did not fire. |
| Authority | Read-only. Commands write `.ll`, `.bc`, `.s`, and `.o` files only into a scratch location the user names; the project tree is not modified. Rollback is deleting the scratch outputs. No remote mutation. |
| Side effect | Scratch IR and object files; chat output. |
| Done | The requested IR, pass output, or lowering exists in the scratch location, and each construct or remark the user asked about has a one-line reading. |

## Inputs

- LLVM version: required, from `opt --version`. Current stable is LLVM 23.1.0; pass names below are new-pass-manager names and apply to any line since 14.
- Source file or existing `.ll`/`.bc` file: required.
- Target CPU and features when lowering: optional; defaults to the host.
- The question: required. One of emit, transform, lower, read, or diagnose.

## Procedure

1. Emit IR. Textual: `clang -O0 -emit-llvm -S src.c -o src.ll`. Bitcode: `clang -O2 -emit-llvm -c src.c -o src.bc`. Convert: `llvm-dis src.bc -o src.ll`, `llvm-as src.ll -o src.bc`. Emit at `-O0` when the goal is to read the front end's output, at `-O2` when the goal is to read what the optimizer produced. Done when: the `.ll` file exists.
2. Run passes with `opt`. Named passes: `opt -passes='mem2reg,instcombine,simplifycfg' src.ll -S -o out.ll`. Standard pipelines: `opt -passes='default<O2>' src.ll -S -o out.ll`. List available passes: `opt --print-passes`. Show the full pipeline clang builds: `clang -O2 -mllvm -print-pipeline-passes -c src.c -o /dev/null`. Dump IR after every pass: `opt -passes='default<O2>' -print-after-all src.ll -S 2>&1`, which is verbose; redirect it to a file. Done when: the transformed IR exists and the pass list is stated.
3. Lower with `llc`. Object: `llc -filetype=obj src.ll -o src.o`. Assembly: `llc -filetype=asm src.ll -o src.s`; Intel syntax on x86 is `--x86-asm-syntax=intel`. CPU and features: `llc -mcpu=skylake -mattr=+avx2 src.ll -o src.s`. Registered targets: `llc --version`. Done when: the assembly or object exists.
4. Read the IR using the construct table; expand any construct the user names from the reference. Done when: each construct in the question has a reading.

   | Construct | Meaning |
   |---|---|
   | `alloca` | Stack slot; `mem2reg` promotes it to SSA values |
   | `load`, `store` | Memory access through an opaque `ptr` |
   | `getelementptr` | Address arithmetic for fields and elements |
   | `phi` | SSA merge of values from predecessor blocks |
   | `call`, `invoke` | Call; `invoke` carries exception edges |
   | `icmp`, `fcmp` | Integer and float comparison |
   | `br`, `switch`, `ret` | Control flow and return |
   | `trunc`, `zext`, `sext`, `bitcast` | Width and representation changes |
   | `ptrtoint`, `inttoptr` | Pointer and integer conversion; avoid where possible |

5. Name the pass that owns a transform from the table when the user asks why something did or did not happen. Done when: the pass is named.

   | Pass | Effect |
   |---|---|
   | `mem2reg`, `sroa` | Promote allocas and split aggregates into SSA values |
   | `instcombine` | Peephole instruction combining |
   | `simplifycfg` | Control-flow cleanup, dead-block removal |
   | `gvn`, `early-cse` | Redundancy elimination |
   | `licm` | Loop-invariant code motion |
   | `loop-unroll` | Loop unrolling |
   | `loop-vectorize`, `slp-vectorize` | Loop and straight-line vectorization |
   | `inline` | Function inlining |
   | `argpromotion` | Pointer arguments to values |
   | `tailcallelim`, `reassociate`, `dce` | Tail calls, reassociation, dead code |

6. Diagnose a missed transform from source with remarks: `clang -O2 -Rpass-missed=loop-vectorize -Rpass-analysis=loop-vectorize src.c`. When the answer needs IR before and after one pass, use `opt -passes='<pass>' -print-before=<pass> -print-after=<pass>` on the `.ll` file. Done when: the analysis remark or the IR diff names the blocker.
7. Point to the companion tools by task: `llvm-link` joins bitcode files, `llvm-lto` runs standalone LTO, `llvm-nm` and `llvm-objdump` inspect objects, `llvm-profdata` merges profiles, `llvm-cov` reports coverage, `llvm-mca` estimates throughput and latency of an assembly block. GNU equivalents: use binutils. Done when: the tool for the follow-up task is named.

## Failure and recovery

| Failure class | Behavior |
|---|---|
| Pass name unknown to `opt` | Run `opt --print-passes` and pick the matching name; legacy `-passname` spellings are not accepted by the new pass manager. |
| `llc` rejects a flag | Run `llc --help-hidden` for the target-specific spelling; `-masm-syntax=intel` is not a flag, `--x86-asm-syntax=intel` is. |
| Front-end question rather than IR question | Lexer, parser, and IR generation from an AST: use compiler-frontend. |
| Runtime code generation | ORC JIT and in-memory execution: use jit-compilation. |
| New pass wanted | Writing and testing a PassPlugin: use llvm-passes. |

## Output

The scratch files produced (`.ll`, `.bc`, `.s`, `.o`) with the exact commands that made them, plus a chat reading of each construct, pass, or remark the user asked about.
