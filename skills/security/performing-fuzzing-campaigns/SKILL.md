---
name: performing-fuzzing-campaigns
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: performing-fuzzing-campaigns
description: >-
  Execute coverage-guided fuzzing campaigns with AFL++, libFuzzer, and honggfuzz to discover memory corruption vulnerabilities, triage crashes, and minimize test cases for exploit development.
domain: cybersecurity
subdomain: exploit-development
tags:
  - afl-plus-plus
  - libfuzzer
  - honggfuzz
  - fuzzing
  - crash-triage
  - coverage
version: "1.0"
author: defconxt
license: AGPL-3.0
metadata:
  mitre-attack: ["T1190", "T1203"]
  frameworks: ["MITRE ATT&CK", "Metasploit"]
  tools: ["afl-fuzz", "afl-clang-fast", "libfuzzer", "honggfuzz", "gdb"]
---

# Performing Fuzzing Campaigns

## Overview

Coverage-guided fuzzing systematically discovers memory corruption by mutating
inputs and tracking code coverage. AFL++, libFuzzer, and honggfuzz find crashes
that become exploit primitives — stack overflows, heap corruption, use-after-free.

## Prerequisites

| Tool / Requirement | Details |
|---|---|
| `afl-fuzz (AFL++)` | Security tooling |
| `clang with libFuzzer` | Security tooling |
| `honggfuzz` | Security tooling |
| Target source code or binary for instrumentation | Environment requirement |
| Seed corpus of valid inputs | Environment requirement |
| Sufficient disk and CPU for campaign duration | Environment requirement |

## Workflow

### Step 1: Instrumentation and Compilation

```bash
# AFL++ instrumented build
export CC=afl-clang-fast
export CXX=afl-clang-fast++
export AFL_USE_ASAN=1
./configure --disable-shared && make clean && make -j$(nproc)

# libFuzzer harness compilation
clang -g -O1 -fsanitize=fuzzer,address -o fuzz_target harness.c target.c

# honggfuzz build
hfuzz-clang -g -O1 -fsanitize=address -o hfuzz_target target.c
```

### Step 2: Seed Corpus Preparation

```bash
# Create minimal seed corpus
mkdir -p seeds/
echo -n "AAAA" > seeds/minimal.txt

# Minimize existing corpus
afl-cmin -i raw_corpus/ -o seeds/ -- ./target_binary @@

# Trim individual test cases
afl-tmin -i seeds/large_input.txt -o seeds/trimmed.txt -- ./target_binary @@
```

### Step 3: Campaign Execution

```bash
# Single-core AFL++ campaign
afl-fuzz -i seeds/ -o findings/ -m none -t 1000 -- ./target_binary @@

# Multi-core parallel fuzzing
afl-fuzz -i seeds/ -o findings/ -M main -- ./target_binary @@
afl-fuzz -i seeds/ -o findings/ -S worker01 -- ./target_binary @@
afl-fuzz -i seeds/ -o findings/ -S worker02 -- ./target_binary @@

# libFuzzer campaign
./fuzz_target corpus/ -max_len=4096 -jobs=$(nproc) -workers=$(nproc)

# honggfuzz campaign
honggfuzz -i seeds/ -o findings/ --threads $(nproc) -- ./hfuzz_target ___FILE___
```

### Step 4: Crash Triage

```bash
# Deduplicate and triage AFL++ crashes
afl-collect -d findings/ -e ./target_binary -r crashes_triaged/

# Analyze crash with GDB
gdb -batch -ex "run < findings/crashes/id:000000,sig:11" \
  -ex "bt full" -ex "info registers" ./target_binary

# Classify with AddressSanitizer
ASAN_OPTIONS=symbolize=1 ./target_binary < findings/crashes/id:000000,sig:11

# Agent-assisted triage
node scripts/agent.js triage --findings findings/crashes/ --binary ./target_binary
```

### Step 5: Campaign Monitoring

```bash
# Check AFL++ stats
afl-whatsup -s findings/

# Plot coverage over time
afl-plot findings/ plot_output/

# Agent campaign status
node scripts/agent.js status --campaign findings/
```

## Detection

```yaml
title: Fuzzing Campaigns Detection
id: 7ec0f782-ea04-4b01-a189-27845ab0c1a4
status: experimental
description: Detects suspicious activity related to performing fuzzing campaigns techniques in exploit development context
logsource:
  category: process_creation
  product: windows
detection:
  selection:
    CommandLine: "*performing*fuzzing*"
  condition: selection
level: critical
tags:
  - attack.t1190
  - attack.t1203
  - attack.execution
falsepositives:
  - Vulnerability scanner testing known exploit signatures
```


**Detection Opportunities**

| Indicator | Source | Detection Logic |
|---|---|---|
| Fuzzing Campaigns Detection | windows/process_creation | Sigma rule (critical) |
| ATT&CK Coverage | MITRE ATT&CK | T1190, T1203 |

## Verification

- [ ] Target compiled with sanitizers (ASAN/UBSAN) and coverage instrumentation
- [ ] Seed corpus minimized and validated
- [ ] Campaign ran for sufficient duration (24h+ recommended)
- [ ] All unique crashes triaged and classified
- [ ] Exploitable crashes prioritized for exploit development
- [ ] Coverage metrics show thorough code exploration

## References

- [AFL++](https://aflplus.plus/) — Coverage-guided fuzzing framework
- [libFuzzer](https://llvm.org/docs/LibFuzzer.html) — In-process coverage-guided fuzzer
- [honggfuzz](https://honggfuzz.dev/) — Security-oriented software fuzzer
