---
name: gcc
description: 'Use when a C or C++ build uses GCC and needs build-mode flags, warning triage, debug info, LTO, PGO, or a compilation error explained. Not for Clang-only diagnostics: use clang.'
---

# GCC

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A project compiles with `gcc` or `g++` and the user asks which flags to use for a build mode, how to read a warning or link error, how to enable LTO or PGO, or why a binary is too large or too slow. |
| Authority | Read-only. The skill emits flag sets, commands, and a diagnosis to chat; the user applies them to the build. Rollback is not needed because no file is written. No remote mutation. |
| Side effect | Chat output. Any throwaway compile the skill runs to confirm a flag targets a scratch file, not the project tree. |
| Done | A flag set and diagnosis are reported, every flag in it is confirmed by `gcc --help` or a scratch compile on the installed GCC, and each error symptom in the request has a named cause and fix. |

## Inputs

- Compiler version: required, from `gcc --version`. The current stable line is GCC 16.2; older lines lack some flags below and the skill checks each one.
- Build goal: required. One of debug, debuggable-optimized, release, size-constrained, or sanitizer.
- Language standard the project requires: required. Passed explicitly as `-std=`; C23 and C++23 are the current published standards, C++20 is the floor.
- The exact compiler or linker message when the request is a diagnosis: required.
- Build system in use (Make, CMake, shell script): optional; determines where flags go.

## Procedure

1. Confirm the compiler: run `gcc --version` and record the major line. Done when: the GCC line is recorded.
2. Pick the build mode from the table and always add an explicit `-std=`; never rely on the implicit default dialect. Done when: one row is chosen and `-std=` is set.

   | Goal | Flags |
   |---|---|
   | Debug | `-g -O0 -Wall -Wextra` |
   | Debug with debuggable optimization | `-g -Og -Wall -Wextra` |
   | Release | `-O2 -DNDEBUG -Wall` |
   | Release, native machine only | `-O3 -march=native -DNDEBUG` |
   | Release, minimum size | `-Os -DNDEBUG` |
   | Sanitizer, development | `-g -O1 -fsanitize=address,undefined` |

3. Set warning discipline: start from `-Wall -Wextra`, add `-Wpedantic` for standards conformance, and `-Werror` only in CI. Add targeted warnings where the code class warrants them: `-Wshadow`, `-Wconversion`, `-Wdouble-promotion`, `-Wformat=2`, `-Wnull-dereference`, `-Wundef`, `-Wcast-qual`; for C++ add `-Wnon-virtual-dtor`, `-Woverloaded-virtual`, `-Wold-style-cast`. Suppress a warning only in a narrow scope with `#pragma GCC diagnostic push`, `#pragma GCC diagnostic ignored "-Wname"`, and `#pragma GCC diagnostic pop`. Use `-w` only for third-party headers as a last resort. Done when: the warning set is stated and any suppression is scoped.
4. Set debug information: `-g` emits DWARF at level 2; `-g3` adds macro definitions for GDB `macro expand`; `-ggdb` selects GDB extensions; `-gsplit-dwarf` moves debug data to `.dwo` files and shortens link time; `-gz` compresses debug sections; `-fdebug-prefix-map=old=new` remaps paths for reproducible builds. Pair `-g` with `-Og`, not `-O0`, when the user needs readable optimized code under a debugger. Done when: the debug flags match the goal.
5. Decide the optimization level. `-O3` adds loop transformations and more inlining over `-O2`; recommend it only after a benchmark, because larger code can lose on instruction-cache-bound workloads. `-Ofast` enables `-ffast-math`, which drops IEEE 754 guarantees (NaN handling, associativity); recommend it only when the numerical domain explicitly permits it. `-march=native` binds the binary to the build host. Show what a level enables with `gcc -Q --help=optimizers -O2 | grep enabled`. Done when: the level is chosen with its trade-off stated.
6. Configure LTO when the goal is release: compile every object with `-flto` and link with `-flto` again; use `-flto=auto` for jobserver parallelism or `-flto=N` for a fixed job count; archive LTO objects with `gcc-ar` and `gcc-ranlib`, not `ar` and `ranlib`. GCC has no `-flto=thin`; that spelling is Clang-only. Linker-side details: use linkers-lto. Done when: the LTO commands cover compile, link, and archive.
7. Configure PGO when a representative workload exists: build with `-O2 -fprofile-generate`, run the workload to produce `.gcda` files, then rebuild with `-O2 -fprofile-use -fprofile-correction`. `-fprofile-correction` reconciles counts from multi-threaded runs; include it. For the full two-stage flow, BOLT, and Clang's formats: use pgo. Done when: the three PGO steps are listed.
8. Answer preprocessor and standards questions with the exact command: `gcc -E file.c` to see expansion, `gcc -dM -E - < /dev/null` for predefined macros, `-std=c11 -pedantic-errors` for strict conformance, `-std=cNN` rather than `-std=gnuNN` to disable GNU extensions, `gcc -v -E - < /dev/null` for the include search path, `gcc -S -masm=intel -O2 foo.c` for Intel-syntax assembly. Done when: each question maps to one command.
9. Triage errors from the table; when the symptom is absent, reproduce it on a scratch file before naming a cause. Done when: every reported symptom has a cause and fix.

   | Symptom | Cause | Fix |
   |---|---|---|
   | `undefined reference to 'foo'` | Missing `-lfoo` or the library precedes the object that needs it | Add `-lfoo` after the object files |
   | `multiple definition of 'x'` | A variable is defined, not declared, in a header | `extern` in the header, one definition in a `.c` file |
   | `implicit declaration of function` | Missing `#include` | Add the header that declares it |
   | `incompatible pointer types` | Wrong cast or missing prototype | Fix the type; check the declaring header |
   | C++ ABI mismatch at link | Mixed `-std=` or different `libstdc++` across TUs | One `-std=` and one toolchain for every TU |
   | `relocation truncated to fit` | A 32-bit relative relocation overflowed | `-mcmodel=large` or restructure the image |

10. Confirm every flag in the answer against the installed compiler: `gcc -Q --help=target | grep <flag>` for target flags, or a scratch compile for the rest. Drop any flag the installed line rejects and say so. Done when: no unconfirmed flag remains in the answer.

## Failure and recovery

| Failure class | Behavior |
|---|---|
| GCC version unknown | Ask for `gcc --version` output or run it; do not guess feature availability. |
| Flag rejected by the installed line | Remove it from the answer, name the line that rejected it, and offer the nearest supported flag. |
| Sanitizer report rather than a compiler error | Sanitizer runtime behavior is outside this skill; read the report's first frame and hand the user the reproduction command. |
| Link error whose library is not on the system | Report the missing library by name; do not invent a package name. |
| Numerical code and `-Ofast` requested | State the IEEE 754 loss and require an explicit domain permission before recommending it. |

## Output

A chat report with three parts: the flag set for the build goal with each flag's purpose, the diagnosis table for every reported symptom, and a confirmation line naming the GCC line the flags were checked against and any flag dropped because that line rejected it.
