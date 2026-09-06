---
name: msvc-cl
description: 'Use when building C or C++ on Windows with cl.exe or clang-cl: GCC-to-MSVC flag translation, /MT versus /MD, PDB output, or an LNK error. Not for MinGW cross builds from Linux: use cross-gcc.'
---

# MSVC cl.exe and clang-cl

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user compiles on Windows with `cl.exe` or `clang-cl`, needs the MSVC spelling of a GCC flag, must pick a runtime library, wants PDB files, or has an `LNK` error. |
| Authority | Read-only. The skill emits flags, commands, and CMake settings to chat; the user runs them. Rollback is not needed. No remote mutation. |
| Side effect | Chat output. |
| Done | The flag set, runtime choice, and debug-info settings are reported, every flag is confirmed against the Microsoft compiler-options reference or `clang-cl /?`, and every `LNK` code in the request has a cause and fix. |

## Inputs

- Compiler: required. `cl.exe` from a Visual Studio install, or `clang-cl` from an LLVM release or the Visual Studio LLVM component. Current upstream Clang is 23.1.0.
- Target architecture: required. x64 or x86; selects the `vcvars` script.
- Build system: required. Command line, MSBuild, or CMake.
- The GCC or Clang flags being translated: required for translation requests.
- The exact `LNK` message: required for link diagnosis.

## Procedure

1. Set up the environment. Open a Developer Command Prompt, or run `"C:\Program Files\Microsoft Visual Studio\2022\<edition>\VC\Auxiliary\Build\vcvars64.bat"` for x64 native and `vcvarsamd64_x86.bat` for an x86 target from an x64 host. Confirm with `cl /?`. With CMake, pass `-G "Visual Studio 17 2022"`. Done when: `cl` runs from the shell.
2. Translate flags from the table. Done when: each requested flag has its MSVC spelling.

   | GCC or Clang | cl.exe |
   |---|---|
   | `-O0` | `/Od` |
   | `-O1` | `/O1` (size) |
   | `-O2` | `/O2` (speed) |
   | `-O3` | `/Ox` |
   | `-Os` | `/Os` |
   | `-g` | `/Zi` (external PDB) or `/Z7` (in the object) |
   | `-Wall` | `/W4`; `/Wall` is far noisier than GCC's |
   | `-Werror` | `/WX` |
   | `-Wno-xxxx` | `/wd<code>` |
   | `-std=c++20` | `/std:c++20`; add `/permissive-` for conformance |
   | `-DFOO=1` | `/DFOO=1` |
   | `-I dir` | `/I dir` |
   | `-c` | `/c` |
   | `-o out` | `/Fe:out.exe` or `/Fo:out.obj` |
   | `-shared` | `/LD` |
   | `-fPIC` | Not needed on Windows |
   | `-flto` | `/GL` at compile and `/LTCG` at link |

3. Choose the runtime library, the most common source of link errors: `/MD` (dynamic `MSVCRT`, the default for release), `/MDd` (dynamic debug), `/MT` (static `LIBCMT`), `/MTd` (static debug). Every object and library in one link must use the same choice. Done when: one runtime is chosen for the whole link.
4. Use clang-cl where wanted: it accepts `cl.exe` flags, so `clang-cl /O2 /std:c++20 /MD src.cpp /Fe:prog.exe` works, and `/clang:<arg>` passes a Clang-native flag through, for example `/clang:-Rpass=inline`. In CMake: `-DCMAKE_C_COMPILER=clang-cl -DCMAKE_CXX_COMPILER=clang-cl`. Microsoft documents Clang 8 as the minimum for its MSBuild integration; use the current LLVM release. Done when: the clang-cl command or CMake setting is stated.
5. Produce debug information. `cl /Zi /Fd:prog.pdb /O2 src.cpp /link /DEBUG` writes an external PDB; `cl /Z7 /O2 src.cpp /link /DEBUG /PDB:prog.pdb` embeds debug data in each object and lets the linker build the PDB. The linker's `/DEBUG:FASTLINK` links faster but needs the object PDBs present when debugging. Keep the PDB beside the executable or on the debugger's symbol path. Done when: the PDB flags match the workflow.
6. Diagnose `LNK` errors from the table. Done when: each code has a cause and fix.

   | Error | Cause | Fix |
   |---|---|---|
   | `LNK2019: unresolved external` | A `.lib` is missing from the link | Add it in project settings or `/link foo.lib` |
   | `LNK2038: mismatch detected for 'RuntimeLibrary'` | `/MT` and `/MD` objects mixed | One runtime for every object and library |
   | `LNK1104: cannot open file 'foo.lib'` | Library not on the search path | `/LIBPATH:<dir>` or the `LIB` variable |
   | `LNK2005: already defined` | A symbol defined in two objects | Remove the duplicate; `__declspec(selectany)` for intentionally repeated data |
   | `LNK4098: defaultlib 'LIBCMT' conflicts` | Runtime mismatch between libraries | Unify runtimes, or `/NODEFAULTLIB:LIBCMT` as documented for that warning |

7. Answer inspection questions with the exact flag: `/P` writes preprocessed output to `.i`, `/FA` writes an assembly listing and `/FAs` interleaves source, `/showIncludes` prints the include tree, `/analyze` runs static analysis, `/Za` disables Microsoft extensions. Linker flags after `/link`: `/SUBSYSTEM:CONSOLE` or `/SUBSYSTEM:WINDOWS`, `/DLL`, `/ENTRY:fn`, `/INCREMENTAL:NO`, `/LIBPATH:`, `/NODEFAULTLIB:`. Done when: each question maps to one flag.
8. Confirm every flag: `clang-cl /?` lists the ones it accepts on any host; for `cl.exe`-only flags cite the Microsoft compiler-options reference. Done when: no unconfirmed flag remains.

## Failure and recovery

| Failure class | Behavior |
|---|---|
| `cl` not found | The `vcvars` script has not run in this shell; give the script path for the target. |
| `LNK` code not in the table | Give the Microsoft error page for that code rather than a guess. |
| Flag absent from `clang-cl /?` and from the reference | Drop it and say so. |
| Cross-compiling from Linux | MinGW triplets: use cross-gcc; Zig's `x86_64-windows-gnu`: use zig-cross. |
| Clang-native diagnostics wanted | Pass through `/clang:` and consult clang for the flag set. |

## Output

A chat report with the environment command, the translated flag set, the runtime choice with the rule that every object must match, the PDB flags, and the `LNK` entries that apply, each flag traced to `clang-cl /?` or the Microsoft reference.
