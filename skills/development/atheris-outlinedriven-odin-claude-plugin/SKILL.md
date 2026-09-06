---
name: atheris
description: 'Use when a user needs coverage-guided fuzzing for Python code or a Python native extension using Atheris. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# Atheris

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User needs coverage-guided fuzzing for Python code or a Python native extension using Atheris. |
| Authority | Reversible local: writes only the Atheris harness file, a corpus directory, and when required for dependency management `pyproject.toml` and `uv.lock` in the harness directory; rollback is deleting the harness file and corpus directory and restoring `pyproject.toml` and `uv.lock` to their pre-run state. No remote mutation. No source under test is mutated. |
| Side effect | Local writes: a `fuzz.py` (or named) harness, a `corpus/` directory of seed and crash artifacts, and a transient fuzzing process. |
| Done | Atheris executes an instrumented target through a deterministic `TestOneInput` harness, reports coverage, and any saved crash artifact reproduces the same failure when replayed. |

## Inputs

- Target: the Python function or module to fuzz, or the Python C extension to fuzz. Required.
- Target kind: pure Python, or native C extension. Required; it selects the instrumentation and build path.
- Expected exceptions: the exception types the target legitimately raises on bad input, so the harness catches them instead of crashing. Optional but recommended.
- Seed corpus: initial input files for `corpus/`. Optional; Atheris can start empty.
- Time/length budget: `-max_total_time` and `-max_len` values. Optional; defaults are libFuzzer defaults.
- Sanitizers: whether AddressSanitizer and/or UndefinedBehaviorSanitizer are enabled. Optional; ASan is the default for native extensions.

## Procedure

1. **Determine target kind.** If the target is pure Python, follow the pure-Python path. If it is a C extension compiled from source, follow the native-extension path. Do not guess; ask the user when the kind is ambiguous. Done when: the target kind is determined as pure Python or native C extension.

2. **Install Atheris.** If the harness directory is not already a uv project (no `pyproject.toml` present), run `uv init --bare` once. Then `uv add atheris`. Verify with `python -c "import atheris; print(atheris.__version__)"`. Done when: Atheris is installed and importable.

3. **Write the harness** (`fuzz.py` or a named file). The harness must be deterministic: no `random`, `time`, or other nondeterministic input inside `TestOneInput`.
   - Decorate the entry point with `@atheris.instrument_func`.
   - Define `TestOneInput(data: bytes)`. Return early on inputs too short to be meaningful. Call the target. Catch only the expected exception types and `pass`; let every other exception propagate so the fuzzer records it as a crash.
   - In `main()`, call `atheris.Setup(sys.argv, TestOneInput)` then `atheris.Fuzz()`.
   - For structured input, use `atheris.FuzzedDataProvider(data)` to split one `bytes` input into typed values (`ConsumeUnicodeNoSurrogates`, `ConsumeBool`, `ConsumeIntInRange`, etc.). Draw in a fixed order; once the buffer runs dry each remaining method returns a zero-value of its type. Do not slice `data` by hand when the target takes several typed arguments, because every mutation shifts the byte offsets of everything after it. Done when: the harness is written with a deterministic `TestOneInput` and `main()`.

4. **Instrument pure-Python targets.** Wrap imports of the code under test in `with atheris.instrument_imports():` so coverage is collected. Do not import the target module after `atheris.Setup()`. Use `atheris.instrument_func` for a single function, `atheris.instrument_imports()` for selected modules, or `atheris.instrument_all()` only when system-wide instrumentation is intended. Done when: the target is instrumented with the appropriate Atheris mechanism.

5. **Build native C extensions with instrumentation.** Before installing the extension from source, export:
   ```
   CC=clang
   CXX=clang++
   CFLAGS="-fsanitize=address,fuzzer-no-link"
   CXXFLAGS="-fsanitize=address,fuzzer-no-link"
   LDSHARED="clang -shared"
   LDSHAREDXX="clang++ -shared"
   ```
   For uv-managed projects, set `no-binary = ["<pkg>"]` under `[tool.uv]` in `pyproject.toml` and run `uv sync --reinstall-package <pkg>` so the package is built from source; a later `uv sync` can otherwise silently swap in an uninstrumented wheel. Add `undefined` to the sanitizer list (`-fsanitize=address,undefined,fuzzer-no-link`) when UBSan is requested. Done when: the native extension is built from source with sanitizer and fuzzer instrumentation flags.

6. **Configure the native-extension runtime.** Set `LD_PRELOAD` to the Atheris sanitizer shared library:
   ```
   export LD_PRELOAD="$(python -c 'import atheris, os; print(os.path.join(os.path.dirname(atheris.__file__), "asan_with_fuzzer.so"))')"
   ```
   Set `ASAN_OPTIONS="allocator_may_return_null=1,detect_leaks=0"` to suppress allocation-failure and leak noise. Set `ASAN_SYMBOLIZER_PATH` to the `llvm-symbolizer` for the installed clang when stack traces are needed. Done when: `LD_PRELOAD` and `ASAN_OPTIONS` are set for the native-extension runtime.

7. **Create the corpus.** `mkdir corpus` and add seed inputs as individual files. Run `uv run python fuzz.py corpus/` so libFuzzer loads and grows the corpus. Minimize a merged corpus with `uv run python fuzz.py -merge=1 new_corpus/ old_corpus/`. Done when: the corpus directory is created and seeded.

8. **Run the campaign.** `uv run python fuzz.py corpus/` with optional `-max_total_time=<seconds>`, `-max_len=<bytes>`, and `-workers=N -jobs=N` for parallel exploration. Read the output: `NEW cov: X` means new coverage and corpus growth; `ERROR: libFuzzer` means a crash was detected and a crash artifact was written. Done when: the campaign runs and produces coverage output or crash artifacts.

9. **Reproduce failures.** A crash artifact (named `crash-*` or `leak-*`) is written next to the harness. Replay it deterministically with `uv run python fuzz.py <artifact>` and confirm the same failure recurs. Done when: each saved artifact reproduces the same failure or is classified as nondeterministic.

## Failure and recovery
- No coverage increase. Cause: poor seed corpus or target not instrumented. Recovery: add representative seeds; confirm `instrument_imports()` wraps the target imports and `@atheris.instrument_func` wraps the entry point. Do not declare success on a stall.
- Import errors / modules imported before instrumentation. Recovery: move the target imports inside the `atheris.instrument_imports()` context manager, before `atheris.Setup()`.
- Segfault with no ASan output. Cause: `LD_PRELOAD` not set for a native extension. Recovery: export `LD_PRELOAD` to `asan_with_fuzzer.so` and rerun.
- Build failures for a native extension. Cause: wrong compiler or missing flags. Recovery: verify `CC`, `CXX`, `CFLAGS`, `CXXFLAGS`, and the clang version; configure `no-binary = ["<pkg>"]` under `[tool.uv]` and run `uv sync --reinstall-package <pkg>`.
- Memory-allocation or leak noise. Recovery: set `ASAN_OPTIONS=allocator_may_return_null=1,detect_leaks=0`.
- Crash artifact does not reproduce. Cause: nondeterminism in the harness (randomness, time, unordered iteration over mutable state). Recovery: remove the nondeterminism so `TestOneInput` is a pure function of `data`, then rerun. A non-reproducing crash is not a confirmed defect.
- Partial-result rule. A campaign that finds no crash is a partial result (coverage gained, no defect proven), not proof of absence. Report coverage and corpus growth; do not claim the target is bug-free.
- Rollback. Delete the harness file and the `corpus/` directory. Restore `pyproject.toml` and `uv.lock` to their pre-run state, or if they were created by this skill, remove the added atheris entry and `no-binary` configuration. The source under test is never modified by this skill.

## Output
- A deterministic, instrumented Atheris harness file.
- A `corpus/` directory of seed and discovered inputs, plus any `crash-*`/`leak-*` artifacts.
- A campaign report: coverage reached, corpus size, executions per second, and for each crash artifact a confirmed reproduction (same failure on replay) or a nondeterminism flag.
- Terminal classification per crash: **confirmed defect** (reproduces), **nondeterministic** (does not reproduce), or **no crash found** (partial result, not proof of absence).
