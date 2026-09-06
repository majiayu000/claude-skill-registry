---
name: clang
description: 'Use when a C or C++ build uses clang and needs diagnostics, optimization remarks, clang-tidy, ThinLTO with lld, LLVM PGO, or a GCC-to-Clang migration. Not for LLVM IR work: use llvm.'
---

# Clang

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A project compiles with `clang` or `clang++` and the user asks for better diagnostics, wants to see what the optimizer did or skipped, wants static analysis with clang-tidy, needs LTO through lld or LLVM PGO, or is moving a GCC build to Clang. |
| Authority | Read-only. The skill emits flags, commands, and readings to chat; `clang-tidy --fix` is shown but the user runs it. Rollback is not needed because no project file is written. No remote mutation. |
| Side effect | Chat output. Scratch compiles target a scratch file, never the project tree. |
| Done | The requested flag set or command is reported, every flag in it is confirmed against the installed Clang, and every remark or diagnostic in the request has a reading and a next action. |

## Inputs

- Compiler version: required, from `clang --version`. The current stable line is LLVM/Clang 23.1.0; Apple's `clang` reports an Apple version and lags upstream.
- The task: required. One of diagnostics, remarks, static analysis, LTO, PGO, GCC migration, or macOS specifics.
- Source file or compile command that reproduces the question: required for diagnostics and remarks.
- Linker available (`ld.lld`, `ld64`, GNU `ld`): required for LTO questions.

## Procedure

1. Confirm the compiler and driver: run `clang --version`. On macOS, `xcrun clang` resolves to the Xcode toolchain; Homebrew LLVM installs a separate upstream `clang`. Done when: the vendor and version are recorded.
2. Map GCC flags to Clang where they differ. Clang accepts most GCC driver flags. Differences that matter: `-Oz` shrinks harder than `-Os`; `-flto=thin` selects ThinLTO; `-fprofile-instr-generate` and `-fprofile-instr-use` select LLVM's own PGO format while `-fprofile-generate` and `-fprofile-use` keep the GCC-compatible format; `-Weverything` enables every warning and suits a one-off audit, not a production build; `--analyze` runs the Clang Static Analyzer where GCC has `-fanalyzer`. Attributes differ: gate GCC-only attributes with `__has_attribute(name)`. Done when: each GCC flag in the request has its Clang spelling or a note that it is unchanged.
3. Tune diagnostics with confirmed flags: `-ferror-limit=N` stops after N errors (default 20); `-fno-elide-type` prints full template types; `-fdiagnostics-show-template-tree` shows a tree diff for template mismatches; `-ftemplate-backtrace-limit=N` bounds the instantiation backtrace; `-fdiagnostics-parseable-fixits` emits fix-its in a machine-readable form; `-fdiagnostics-format=vi` or `msvc` changes the location format. Fix-it hints already print inline by default. Done when: the diagnostic flags are stated with their effect.
4. Read optimization remarks. Emit them with `-Rpass=<regex>` (transform happened), `-Rpass-missed=<regex>` (transform skipped), `-Rpass-analysis=<regex>` (why), for example `clang -O2 -Rpass-analysis=loop-vectorize src.c`. Save all remarks with `-fsave-optimization-record`, which writes `<object>.opt.yaml` next to the object file. Interpret: an inline remark on a hot path is good; `loop not vectorized: loop control flow is not understood` calls for restructuring the loop; a reordering-safety remark calls for `__restrict__` or `#pragma clang loop vectorize(assume_safety)` after the user proves no aliasing. Done when: each remark in the request has a reading and a next action.
5. Run static analysis. Built-in analyzer: `clang --analyze -Xanalyzer -analyzer-output=text src.c`. clang-tidy: `clang-tidy src.cpp -- -std=c++20 -I<dir>` for one file, `-p build/` against `compile_commands.json` (generate it with `cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON`), `run-clang-tidy -j<N> -p build/` for the tree, `-checks='clang-analyzer-*,bugprone-*,modernize-*,performance-*'` to select families, `--fix` to apply fix-its in place. Suppress one line with `// NOLINT(check-name)` or the following line with `// NOLINTNEXTLINE(check-name)`. Done when: the analysis command and check families match the code class.
6. Configure LTO. Full: `clang -O2 -flto -fuse-ld=lld`. Thin: `clang -O2 -flto=thin -fuse-ld=lld`. Confirm the linker with `clang -fuse-ld=lld -Wl,--version`. ThinLTO links faster than full LTO on large programs; measure the code-quality difference on the project rather than assuming a ratio. `-fwhole-program-vtables` and `-fvirtual-function-elimination` need LTO. On macOS the default linker is `ld64`; `-fuse-ld=lld` needs an upstream LLVM install. Done when: the LTO mode, linker, and confirmation command are stated.
7. Configure PGO: `clang -O2 -fprofile-instr-generate` to instrument, run the workload (writes `default.profraw`; set `LLVM_PROFILE_FILE="prog-%p.profraw"` for parallel runs), `llvm-profdata merge -output=prog.profdata *.profraw`, then `clang -O2 -fprofile-instr-use=prog.profdata`. Sampling-based profiles use `-fprofile-sample-use=<file>`. The full flow, context-sensitive PGO, and BOLT: use pgo. Done when: the four PGO commands are listed.
8. Handle macOS specifics when asked: set the deployment target with `-mmacosx-version-min=X.Y`; sanitizer runtimes are injected at load, so do not strip a sanitized binary; `xcrun clang` selects the Xcode toolchain. Done when: the macOS points relevant to the request are stated.
9. Confirm every flag against the installed Clang with a scratch compile; drop any the driver rejects and say so. Done when: no unconfirmed flag remains.

## Failure and recovery

| Failure class | Behavior |
|---|---|
| Version unknown | Run or request `clang --version`; do not guess. |
| Flag rejected by the driver | Remove it, report the rejection, offer the nearest supported flag. `--show-fixits` is one such flag: it does not exist, fix-its print by default. |
| `-fuse-ld=lld` fails | Report that lld is not installed for this toolchain and fall back to the system linker with `-flto`. |
| Remark regex matches nothing | Widen to `-Rpass-missed=.*` on the one file, then narrow. |
| `compile_commands.json` missing | Give the CMake export command, or run clang-tidy with explicit `--` flags on one file. |

## Output

A chat report with the flag set or command for the task, a reading of every diagnostic or remark supplied, and a confirmation line naming the Clang version the flags were checked against and any flag dropped.
