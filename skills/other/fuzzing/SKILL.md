---
name: fuzzing
description: 'Use when planning an end-to-end fuzzing program for a project: engine and target selection, corpus management, and CI or nightly wiring. Not for harness design: use fuzz-harness-writing. Not for engine operation or triage: use libfuzzer. Not for sanitizer flag reference: use sanitizers.'
---

# Fuzzing

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Coverage-guided fuzz testing for a parser, deserializer, codec, or API boundary: harness writing, libFuzzer or AFL++ setup, corpus management, crash reproduction, or CI runs. |
| Authority | Reversible local. Writes are limited to fuzz binaries, corpora, dictionaries, findings, and logs under the project tree; rollback is deleting those directories. No remote mutation. |
| Side effect | Built fuzz targets, corpus directories, crash artifacts, and coverage measurements. |
| Done | A fuzz target runs against a seeded corpus, the crash or clean verdict is reproduced on demand, and the CI or nightly plan is written down. |

## Inputs

1. Target code (required): the library or entry point to fuzz, ideally a parse or I/O boundary.
2. Seeds (required when they exist): known-good inputs from tests or real traffic.
3. Toolchain (required): Clang for libFuzzer; AFL++ installed for fork-mode fuzzing. Grounded channels: Clang 23.1.0, AFL++ v5.03c (AGPL 3.0+ since v5.00c, mixed licensing in the repo).
4. Time budget (optional): seconds for CI regression runs, hours for nightly.

## Procedure

1. Write the target as a function of arbitrary bytes. The harness owns every guarantee:

```c
// fuzz_parser.c
#include <stdint.h>
#include <stddef.h>
#include "myparser.h"

int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    MyParser *p = parser_create();
    if (p) {
        parser_feed(p, (const char *)data, size);
        parser_destroy(p);
    }
    return 0;
}
```

Rules: return 0 for uninteresting input instead of exiting; never call `abort` or `exit`; never read or write outside `[data, data + size)`; keep no state between calls; stay fast, since the fuzzer calls it millions of times. Done when: the harness passes a review against each rule.
2. Build with libFuzzer and the sanitizer set. `-fsanitize=fuzzer` links libFuzzer and supplies `main`, so the target must not define one:

```bash
clang -fsanitize=fuzzer,address,undefined -fno-omit-frame-pointer -g -O1 \
    fuzz_parser.c myparser.c -o fuzz_parser
```

Done when: the binary links without a duplicate `main` and runs `-help=1` cleanly.
3. Seed and run:

```bash
mkdir -p corpus
cp tests/inputs/* corpus/          # real seeds sharply cut time to coverage
./fuzz_parser corpus/ -max_len=65536 -timeout=10
./fuzz_parser corpus/ -max_total_time=3600
./fuzz_parser corpus/ -jobs=4 -workers=4
```

Defaults worth knowing: `-max_len` 4096 when unset, `-timeout` 1200 seconds, `-rss_limit_mb` 2048, `-error_exitcode` 77, `-len_control` 100. Workers default to half the core count when unset. Done when: the run starts consuming the corpus and reporting new coverage.
4. Reproduce and minimize every finding. Artifacts land as `crash-<hash>`, `oom-<hash>`, or `timeout-<hash>` in the artifact prefix directory:

```bash
./fuzz_parser crash-abc123                 # reproduce
./fuzz_parser -minimize_crash=1 -max_total_time=60 crash-abc123
```

Re-run the minimized case under gdb (`gdb --args ./fuzz_parser crash-min`) to name the faulting frame. Done when: one small input reproduces the bug deterministically.
5. Add AFL++ where process-level isolation or non-library targets are needed:

```bash
afl-clang-fast -g -O1 -o prog_afl main.c myparser.c
afl-fuzz -i afl-input -o afl-output -- ./prog_afl @@    # @@ = input file path
afl-fuzz -i afl-input -o afl-output -- ./prog_afl       # stdin target: drop @@
```

Persistent mode avoids a fork per input and raises throughput for library targets; `__AFL_LOOP(1000)` bounds each iteration batch. Scale out with `-M main` plus one `-S name` instance per spare core, and read status with `afl-whatsup afl-output`. Done when: at least one AFL++ instance reports stable cycles with new paths.
6. Manage the corpus as an asset. Merge runs to the coverage-unique subset, and keep the corpus in version control or CI cache:

```bash
./fuzz_parser -merge=1 corpus_min/ corpus/ run1/ run2/
afl-cmin -i afl-output/default/queue -o corpus_min -- ./prog_afl @@
./fuzz_parser corpus/ -runs=0 -print_coverage=1     # coverage of the corpus
```

Done when: one minimized corpus exists and reproduces the union of coverage.
7. Guide mutation with a dictionary when the format has tokens:

```c
# parser.dict
kw1="<"
kw2=">"
null_byte="\x00"
magic1="\x89PNG"
```

```bash
./fuzz_parser corpus/ -dict=parser.dict
afl-fuzz -i corpus/ -o out/ -x parser.dict -- ./prog_afl @@
```

For structured formats that checksum or length-prefix, implement `LLVMFuzzerCustomMutator` and repair the invariant after `LLVMFuzzerMutate`, or the fuzzer never passes the header. Done when: deep paths are reached without human-crafted inputs.
8. Wire CI as a fixed-time regression, not an open-ended run:

```yaml
- name: Build fuzz target
  run: |
    clang -fsanitize=fuzzer,address,undefined -g -O1 \
      fuzz_parser.c myparser.c -o fuzz_parser
- name: Fuzz regression (60 seconds)
  run: |
    ./fuzz_parser corpus/ -max_total_time=60 -error_exitcode=1 \
      -artifact_prefix=artifacts/
- name: Reproduce known crashes
  run: |
    for f in known_crashes/*; do ./fuzz_parser "$f" || exit 1; done
```

Longer campaigns go to scheduled jobs with `-max_total_time=3600` or to OSS-Fuzz infrastructure. Done when: a pull request cannot merge with a target that regresses.
9. Add Python targets with Atheris, and Zig targets through the built-in fuzzer (Zig 0.13 and later):

```python
import atheris, sys

with atheris.instrument_imports():
    import myparser

def TestOneInput(data: bytes) -> None:
    fdp = atheris.FuzzedDataProvider(data)
    try:
        myparser.parse(fdp.ConsumeString(sys.maxsize))
    except myparser.ParseError:
        pass

if __name__ == "__main__":
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()
```

```bash
zig build test --fuzz
```

Done when: each language boundary has its own target or a recorded decision not to fuzz it.

Harness templates and the full flag tables live in references/targets.md.

## Failure and recovery

| Failure class | Behavior |
|---|---|
| Fuzzer finds no coverage growth | The harness or sanitizer set blocks depth. Check that `-fsanitize=fuzzer` is in the build and seeds are real inputs. |
| Crash does not reproduce | The bug depends on corpus state or is flaky. Re-run the single input ten times; check for uninitialized reads (initcheck) or a race. |
| OOM artifacts flood the run | Lower `-rss_limit_mb`, cap `-max_len`, or bound allocations inside the harness. |
| AFL++ target dies at startup | Memory limit too low for the target. Raise `-m` or add `-t` for slow inputs. |
| CI run too slow | Shrink `-max_total_time`, run `-workers=$(nproc)`, and cache the corpus between runs. |
| Fuzzer slows to a crawl mid-run | The target leaks or retains state between calls. Audit the harness against the step 1 rules. |

## Output

The built targets, the seeded and minimized corpora, the crash reproduction commands, and the CI configuration. Every finding carries its minimized artifact and the sanitizer report that explains it.
