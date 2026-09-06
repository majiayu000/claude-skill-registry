---
name: ruzzy
description: 'Use when asked to set up and run coverage-guided fuzzing of Ruby code or C extensions with Ruzzy, producing crash reports or clean campaign summaries. Not for C/C++ fuzzing: use libfuzzer or libfuzzer.'
---

# Ruzzy fuzzing campaign

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User needs Ruzzy to run coverage-guided fuzzing on Ruby code or a Ruby native extension. |
| Authority | Reversible local: writes harness, tracer, sanitizer preload, corpus, and installed gem files to the working directory or the local Ruby gem path. Record the installed-gem list before install; rollback is file deletion plus uninstalling exactly the gem version this campaign added. No remote mutation. |
| Side effect | Write Ruzzy harness scripts, tracer scripts, sanitizer LD_PRELOAD paths, corpus files, and install the target gem with clang and sanitizer flags. |
| Done | Ruzzy executes the intended Ruby target with the correct tracer or extension setup and reproduces saved failures. |

## Inputs

Required: Ruby target path or gem name, sanitizer selection (ASan or UBSan).

Optional: corpus directory path, libFuzzer arguments (e.g., `-max_len=1024`), crash file to reproduce.

## Procedure

1. Confirm target: pure Ruby (requires tracer) or C extension (single harness). Done when: the target kind is confirmed as pure Ruby or C extension.
2. Confirm sanitizer: ASan (`Ruzzy::ASAN_PATH`) or UBSan (`Ruzzy::UBSAN_PATH`). Done when: the sanitizer is selected and the selected `Ruzzy::ASAN_PATH` or `Ruzzy::UBSAN_PATH` constant is confirmed.
3. For pure Ruby targets, write a tracer script calling `Ruzzy.trace('harness.rb')` and a separate harness script calling `Ruzzy.fuzz(test_one_input)`. For C extensions, write one harness script calling `Ruzzy.fuzz(test_one_input)`; no tracer required. Done when: the harness and, for pure Ruby, the tracer script are written.
4. Write the harness as a lambda named `test_one_input` that accepts data and returns `0`. Catch Ruby exceptions in C extension harnesses; let them propagate in pure Ruby harnesses. Done when: the harness lambda is written with the correct exception handling for the target kind.
5. Set `ASAN_OPTIONS=allocator_may_return_null=1:detect_leaks=0:use_sigaltstack=0`. Do not export `LD_PRELOAD`; use it inline with the ruby command. Done when: `ASAN_OPTIONS` is set and `LD_PRELOAD` is prepared for inline use.
6. Record `gem list --local` (each gem's name and version) before any install. Then install the gem with clang and sanitizer flags: set `CC=clang`, `CXX=clang++`, `LDSHARED="clang -shared"`, and `LDSHAREDXX="clang++ -shared"`; set `CFLAGS` and `CXXFLAGS` to `-fsanitize=address,fuzzer-no-link -fno-omit-frame-pointer -fno-common -fPIC -g` for an ASan build, or `-fsanitize=undefined,fuzzer-no-link -fno-omit-frame-pointer -fno-common -fPIC -g` for a UBSan build, matching the sanitizer selected in step 2 so the instrumented library the run preloads matches the build. Also set `MAKE="make --environment-overrides V=1"` so GNU make lets environment `CC`, `CFLAGS`, and related values override the mkmf Makefile; without `--environment-overrides`, Ruby's extension build can ignore those flags and install an uninstrumented native library. The `-shared` flag is required for `LDSHARED` and `LDSHAREDXX`; without it the native extension link fails. Done when: the pre-install gem list is recorded and the gem is installed with clang and the flags matching the selected sanitizer.
7. Run: `LD_PRELOAD=$(ruby -e 'require "ruzzy"; print Ruzzy::ASAN_PATH') ruby "<harness-or-tracer>.rb" [corpus] [libfuzzer-options]` for ASan, or set `SAN_PATH=$(ruby -e 'require "ruzzy"; print Ruzzy::UBSAN_PATH')` and run `LD_PRELOAD="$SAN_PATH" ruby "<harness-or-tracer>.rb" [corpus] [libfuzzer-options]` for UBSan. Done when: the fuzzer runs with the correct `LD_PRELOAD` and harness.
8. On `ERROR: AddressSanitizer:` or `ERROR: UndefinedBehaviorSanitizer:`, capture the crash file path, Base64 content, and reproducer command. Write `crash-*` files to the working directory. Done when: any sanitizer error is captured with crash file path, content, and reproducer command, or the campaign completes without error.
9. To reproduce a saved failure, run the same command passing the crash file path as the final argument. Done when: the saved failure is reproduced or confirmed non-reproducible.

## Failure and recovery
| Failure class | Meaning | Recovery |
|---|---|---|
| `platform-missing` | Platform is not Linux x86-64/ARM64, clang is unavailable, or Ruby is not installed | Halt; suggest Docker environment |
| `dependency-missing` | Gem not installed or wrong clang | Install gem with sanitizer flags; verify the selected `Ruzzy::ASAN_PATH` or `Ruzzy::UBSAN_PATH` constant resolves |
| `harness-error` | Ruby exception exits the fuzzer | Adjust exception handling for a C extension harness; a pure Ruby harness must not catch exceptions |
| `sanitizer-report` | ASan or UBSan error detected | Capture crash file; report class, address, reproducer |
| `no-crashes-found` | Fuzzer ran without sanitizer violations | Report campaign completed cleanly |
| `env-misconfigured` | Missing ASAN_OPTIONS or LD_PRELOAD | Set ASAN_OPTIONS and re-run inline LD_PRELOAD |

Rollback: delete written harness, tracer, and corpus files. Diff the pre-install `gem list --local` against the current list and `gem uninstall <name> -v <version>` only the name-version pair this campaign added. Leave every pre-existing gem version in place. No VCS mutation.

## Output
Fuzzing campaign report containing:

- Target gem or file fuzzed
- Sanitizer and version
- libFuzzer options used
- Execution duration and corpus state
- For each crash: sanitizer error type, crash file path, Base64 input, reproducer command
- If clean: total inputs, exec/s, coverage summary lines
