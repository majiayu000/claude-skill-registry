---
name: Fuzzing Harness Development
description: Building effective fuzzing harnesses to maximize code coverage and vulnerability discovery through automated input generation
when_to_use: When setting up automated vulnerability discovery, testing parsers or complex input handlers, or conducting long-term security research on software components
version: 1.0.0
languages: c, c++, python
---

# Fuzzing Harness Development

## Overview

A fuzzing harness is the code infrastructure that feeds inputs to a target program and monitors for crashes or anomalous behavior. Effective harnesses maximize code coverage, minimize overhead, and detect subtle vulnerabilities. This skill covers designing, implementing, and optimizing fuzzing harnesses for various target types.

**Core principle:** Design harnesses to reach deep code paths efficiently. Monitor comprehensively. Triage systematically.

## When to Use

- Setting up continuous fuzzing for a codebase
- Testing file parsers, network protocols, or complex input handlers
- Vulnerability research on specific code components
- Regression testing for security fixes
- Building security into CI/CD pipelines

## Types of Fuzzing Harnesses

### 1. In-Process Harness (libFuzzer)

**Best for:** Library functions, isolated components

```cpp
// libfuzzer_harness.cpp
#include <stdint.h>
#include <stddef.h>

// Target function to fuzz
extern "C" int parse_data(const uint8_t *data, size_t size);

// Fuzzer entry point
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    // Call target function
    parse_data(data, size);
    return 0;
}
```

```bash
# Compile with libFuzzer
clang++ -fsanitize=fuzzer,address -g libfuzzer_harness.cpp target.cpp -o fuzzer

# Run fuzzer
./fuzzer corpus/ -max_len=1024 -jobs=4
```

### 2. File-Based Harness (AFL++)

**Best for:** Programs that read files

```c
// afl_harness.c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <input_file>\n", argv[0]);
        return 1;
    }
    
    // Read file
    FILE *f = fopen(argv[1], "rb");
    if (!f) return 1;
    
    fseek(f, 0, SEEK_END);
    size_t size = ftell(f);
    fseek(f, 0, SEEK_SET);
    
    uint8_t *data = malloc(size);
    fread(data, 1, size, f);
    fclose(f);
    
    // Call target
    parse_data(data, size);
    
    free(data);
    return 0;
}
```

```bash
# Compile with AFL instrumentation
export CC=afl-clang-fast
make clean && make

# Run AFL++
afl-fuzz -i seeds/ -o findings/ -- ./harness @@
```

### 3. Network Protocol Harness

**Best for:** Network services, protocol implementations

```python
# boofuzz_harness.py
from boofuzz import *

def main():
    # Define target
    session = Session(
        target=Target(
            connection=SocketConnection("localhost", 8080, proto='tcp')
        )
    )
    
    # Define protocol structure
    s_initialize("http_request")
    s_static("GET ")
    s_string("/", name="path")
    s_static(" HTTP/1.1\r\n")
    s_static("Host: ")
    s_string("target.com", name="host")
    s_static("\r\n")
    s_static("Content-Length: ")
    s_size("body", output_format="ascii", name="content_length")
    s_static("\r\n\r\n")
    s_binary("", name="body")
    
    session.connect(s_get("http_request"))
    session.fuzz()

if __name__ == "__main__":
    main()
```

## Harness Design Principles

### 1. Maximize Code Coverage

```cpp
// Good: Directly calls target function
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    if (size < 4) return 0;  // Minimum size check
    
    // Parse input format
    uint32_t command = *(uint32_t*)data;
    
    // Route to different code paths based on input
    switch(command % 5) {
        case 0: handle_format_a(data + 4, size - 4); break;
        case 1: handle_format_b(data + 4, size - 4); break;
        case 2: handle_format_c(data + 4, size - 4); break;
        case 3: handle_format_d(data + 4, size - 4); break;
        case 4: handle_format_e(data + 4, size - 4); break;
    }
    
    return 0;
}
```

### 2. Minimize Overhead

```cpp
// Avoid repeated initialization
static bool initialized = false;
static TargetContext *ctx = nullptr;

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    // Initialize once
    if (!initialized) {
        ctx = create_context();
        initialized = true;
    }
    
    // Reset state, don't recreate
    reset_context(ctx);
    
    // Fuzz target
    process_input(ctx, data, size);
    
    return 0;
}
```

### 3. Handle Expected Errors Gracefully

```cpp
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    // Ignore obviously invalid inputs
    if (size < MIN_SIZE || size > MAX_SIZE) {
        return 0;
    }
    
    // Catch expected errors
    try {
        parse_data(data, size);
    } catch (const ParseException &e) {
        // Expected error, not a crash
        return 0;
    } catch (...) {
        // Unexpected error - let it crash for analysis
        throw;
    }
    
    return 0;
}
```

## Sanitizer Integration

### AddressSanitizer (ASan)

```bash
# Detect memory errors
CFLAGS="-fsanitize=address -g" \
CXXFLAGS="-fsanitize=address -g" \
make clean && make
```

Detects:
- Buffer overflows
- Use-after-free
- Double free
- Memory leaks

### UndefinedBehaviorSanitizer (UBSan)

```bash
# Detect undefined behavior
CFLAGS="-fsanitize=undefined -g" \
CXXFLAGS="-fsanitize=undefined -g" \
make clean && make
```

Detects:
- Integer overflow
- Null pointer dereference
- Invalid casts
- Misaligned access

### MemorySanitizer (MSan)

```bash
# Detect uninitialized memory reads
CFLAGS="-fsanitize=memory -g" \
CXXFLAGS="-fsanitize=memory -g" \
make clean && make
```

## Corpus Management

### Seed Corpus Creation

```bash
# Create initial seeds
mkdir corpus/

# Valid inputs that exercise different features
echo "valid_input_1" > corpus/seed1.txt
echo "another_valid_input" > corpus/seed2.txt

# Edge cases
echo "" > corpus/empty.txt
printf "\x00\x00\x00\x00" > corpus/nulls.bin

# Real-world samples
cp /path/to/real/samples/* corpus/
```

### Corpus Minimization

```bash
# AFL corpus minimization
afl-cmin -i corpus/ -o corpus_min/ -- ./target @@

# Keep only unique coverage
afl-tmin -i corpus/crash -o corpus/minimized_crash -- ./target @@
```

### Dictionary Files

```bash
# Create dictionary for structured input
cat > dict.txt << EOF
# HTTP keywords
keyword1="GET"
keyword2="POST"
keyword3="HTTP/1.1"

# Common values
value1="admin"
value2="root"

# Magic bytes
magic1="\x50\x4B\x03\x04"  # ZIP
magic2="\xFF\xD8\xFF"      # JPEG
EOF

# Use with AFL
afl-fuzz -i corpus/ -o findings/ -x dict.txt -- ./target @@
```

## Crash Triage

### Automated Triage

```python
#!/usr/bin/env python3
# triage_crashes.py

import os
import subprocess
import hashlib

def get_crash_hash(crash_file, target):
    """Get unique hash for crash based on stack trace"""
    result = subprocess.run(
        ['gdb', '-batch', '-ex', 'run', '-ex', 'bt', target, crash_file],
        capture_output=True,
        text=True
    )
    
    # Extract stack trace
    bt = result.stdout
    
    # Hash it
    return hashlib.md5(bt.encode()).hexdigest()

def triage_crashes(crash_dir, target):
    """Triage crashes, group by unique stack trace"""
    crashes = {}
    
    for crash_file in os.listdir(crash_dir):
        if not crash_file.startswith('id:'):
            continue
        
        path = os.path.join(crash_dir, crash_file)
        crash_hash = get_crash_hash(path, target)
        
        if crash_hash not in crashes:
            crashes[crash_hash] = []
        crashes[crash_hash].append(path)
    
    # Report unique crashes
    print(f"Total crashes: {sum(len(v) for v in crashes.values())}")
    print(f"Unique crashes: {len(crashes)}")
    
    for i, (hash, files) in enumerate(crashes.items(), 1):
        print(f"\nUnique crash #{i}:")
        print(f"  Representative: {files[0]}")
        print(f"  Count: {len(files)}")

if __name__ == "__main__":
    triage_crashes("findings/default/crashes/", "./target")
```

### Exploitability Assessment

```bash
# Use exploitable GDB plugin
gdb -batch \
    -ex 'source /path/to/exploitable.py' \
    -ex 'run' \
    -ex 'exploitable' \
    ./target crash_file
```

## Continuous Fuzzing

### Integration with CI/CD

```yaml
# .github/workflows/fuzzing.yml
name: Continuous Fuzzing

on:
  schedule:
    - cron: '0 0 * * *'  # Daily
  push:
    branches: [main]

jobs:
  fuzz:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build with sanitizers
        run: |
          export CC=clang
          export CXX=clang++
          export CFLAGS="-fsanitize=fuzzer,address -g"
          make fuzzer
      
      - name: Run fuzzer
        run: |
          timeout 3600 ./fuzzer corpus/ || true
      
      - name: Upload crashes
        if: always()
        uses: actions/upload-artifact@v2
        with:
          name: crashes
          path: crash-*
```

### OSS-Fuzz Integration

```python
# For open-source projects
# https://github.com/google/oss-fuzz

# Create build script: projects/myproject/build.sh
#!/bin/bash

# Build project
./configure
make

# Build fuzzers
$CXX $CXXFLAGS -std=c++11 \
    fuzzer.cpp -o $OUT/fuzzer \
    -fsanitize=fuzzer \
    /path/to/library.a
```

## Performance Optimization

### Profile-Guided Optimization

```bash
# 1. Build with profiling
clang++ -fprofile-instr-generate -fcoverage-mapping harness.cpp -o harness_prof

# 2. Generate profile
./harness_prof corpus/*
llvm-profdata merge -o default.profdata default.profraw

# 3. Build optimized fuzzer
clang++ -fprofile-instr-use=default.profdata \
        -fsanitize=fuzzer,address \
        harness.cpp -o harness_optimized
```

### Parallel Fuzzing

```bash
# AFL++ parallel fuzzing
# Master instance
afl-fuzz -i seeds/ -o sync/ -M master -- ./target @@

# Slave instances
afl-fuzz -i seeds/ -o sync/ -S slave1 -- ./target @@
afl-fuzz -i seeds/ -o sync/ -S slave2 -- ./target @@
afl-fuzz -i seeds/ -o sync/ -S slave3 -- ./target @@
```

## Common Pitfalls

| Mistake | Impact | Solution |
|---------|--------|----------|
| Not checking basic invariants | Fuzzer wastes time | Add size/format checks |
| Slow initialization | Poor throughput | Initialize once, reset state |
| Catching all exceptions | Miss real crashes | Only catch expected errors |
| Poor seed corpus | Low coverage | Use diverse, valid inputs |
| Not using sanitizers | Miss subtle bugs | Always enable ASan/UBSan |
| Ignoring crash triaging | Duplicate work | Group by unique stack trace |

## Integration with Other Skills

- skills/analysis/zero-day-hunting - Primary technique for discovery
- skills/exploitation/exploit-dev-workflow - Validate found crashes
- skills/analysis/binary-analysis - Understand target structure

## Tool Recommendations

**Coverage-Guided:**
- AFL++ (fast, many features)
- libFuzzer (in-process, LLVM)
- Honggfuzz (feedback-driven)

**Protocol:**
- Boofuzz (protocol fuzzing)
- Peach Fuzzer (commercial)

**Infrastructure:**
- ClusterFuzz (Google's fuzzing infrastructure)
- OSS-Fuzz (for open source projects)

## Success Metrics

- Code coverage percentage
- Crashes found per hour (exec/s)
- Unique crash count
- Time to first crash
- Depth of code paths reached

## References

- AFL++ documentation
- libFuzzer documentation
- "Fuzzing: Brute Force Vulnerability Discovery" by Sutton et al.
- Google Project Zero fuzzing blog posts
- Trail of Bits fuzzing resources
