---
name: ninja
description: 'Use when diagnosing Ninja build failures, tuning parallelism, interpreting verbose output, or working with build.ninja files as a CMake-generated low-level build executor.'
---

# Ninja

Ninja is the low-level build executor that CMake, Meson, and other generators emit `build.ninja` for. Grounded against Ninja 1.13.2.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The task diagnoses a Ninja build failure, tunes parallelism, interprets Ninja output, inspects or edits a `build.ninja` file, or uses Ninja as a CMake or Meson backend. |
| Authority | Reversible local: writes only build outputs inside the build directory; `build.ninja` itself is generated, so edits go to the generator's input files; rollback is version control plus `ninja -t clean`. No remote mutation. |
| Side effect | `ninja` runs build commands and writes outputs; `ninja -t clean` removes them. |
| Done | The build completes or the failing edge is identified with its cause, and the fix lands in the generator input rather than in `build.ninja`. |

## Inputs

- A configured build directory (required): `build.ninja` produced by CMake or Meson.
- The failing target or error text (required for diagnosis).
- Parallelism constraints (optional): job count or load limit.

## Procedure

1. Generate Ninja files from the meta-build system. Done when: `build.ninja` exists in the build directory.

```bash
cmake -S . -B build -G Ninja
cmake --build build                 # invokes ninja internally
ninja -C build                      # or run ninja directly

# Multi-config variant
cmake -S . -B build -G "Ninja Multi-Config"
cmake --build build --config Release
```

2. Control parallelism. `-j` defaults to a heuristic based on the machine's CPU count; `-l` throttles on load average; `-k` controls how many failures stop the build. Done when: the build runs at the intended concurrency.

```bash
ninja -j4              # exactly 4 jobs
ninja -j"$(nproc)"     # one per CPU
ninja -j0              # unlimited
ninja -l4.0            # no new jobs while load average exceeds 4.0
ninja -k5              # stop after 5 failures
ninja -k0              # never stop on failure
```

3. Diagnose with verbose and debug output. Done when: the failing command or the rebuild reason is visible.

```bash
ninja -v               # full command lines
ninja -n               # dry run: what would run
ninja -d explain myapp # why myapp is considered dirty
ninja -d stats         # operation counts and timing at end
ninja -d keepdepfile   # keep .d files after reading
ninja -d keeprsp       # keep @response files
```

4. Inspect the graph with sub-tools. Done when: the query answers the question asked.

```bash
ninja -t targets all          # every target
ninja -t targets rule cc      # targets built by rule cc
ninja -t query myapp          # inputs and outputs of one edge
ninja -t graph myapp | dot -Tsvg -o deps.svg   # graphviz
ninja -t compdb cc cxx > compile_commands.json # compilation database
ninja -t rules                # all rules
ninja -t clean                # remove outputs
ninja -t clean -g             # also remove generated files
```

5. Produce `compile_commands.json` for clang-tidy and IDEs. Done when: the database exists at the expected path.

```bash
cmake -S . -B build -G Ninja -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
ln -sf build/compile_commands.json .
```

6. Read `build.ninja` when debugging generated output. The file is generated; fix the generator input, not this file. Done when: the edge, rule, or variable causing the problem is identified.

```ninja
cflags = -Wall -O2

rule cc
  command = gcc $cflags -c $in -o $out
  description = CC $in
  depfile = $out.d
  deps = gcc

build foo.o: cc foo.c
build all: phony foo.o
default all
```

Key concepts: a `rule` is a command template; a `build` edge instantiates it; `$in` and `$out` are the edge's inputs and outputs; `deps = gcc` tells Ninja to read Makefile-style depfiles; `phony` marks a target always out of date; `default` selects what a bare `ninja` builds.

7. Diagnose common failures against this table. Done when: the error maps to a cause and a fix.

| Issue | Cause | Fix |
|---|---|---|
| `missing and no known rule to make it` | Source not in the generator's file list | Fix `add_executable`/`sources` and regenerate |
| Changes not picked up | Stale `build.ninja` | Re-run `cmake -S . -B build` or `meson setup --reconfigure` |
| `build stopped: subcommand failed` | A compile or link failed | Read the error above the line; `-v` shows the command |
| Slow parallel build | I/O-bound at high `-j` | Add `-l"$(nproc)"` to throttle on load |
| Circular dependency | Target depends on itself | Check the generator's dependency declarations |

For the full command, sub-tool, and `build.ninja` format reference see `references/cheatsheet.md`.

## Failure and recovery

- `build.ninja` edited by hand: revert; the next generator run overwrites it. Fix `CMakeLists.txt` or `meson.build` instead.
- `ninja -t compdb` output is empty: the generator did not emit `compdb` rules; use `CMAKE_EXPORT_COMPILE_COMMANDS=ON` instead.
- Dry run shows unexpected rebuilds: run `ninja -d explain <target>` to see which input is newer.
- Load throttling still saturates I/O: lower `-j` explicitly; `-l` only stops starting new jobs, it does not slow running ones.
- `ninja: error: loading 'build.ninja'`: the file is missing or corrupt; regenerate it.

## Output

A diagnosed build failure with its root cause in the generator input, or a tuned `ninja` invocation (`-j`/`-l`/`-k`) with the reason for each flag. For format questions, the identified rule, edge, or variable in `build.ninja` traced back to its generator source.
