---
name: google-continuous-fuzzing
description: Apply Google's continuous fuzzing methodology using OSS-Fuzz and ClusterFuzz. Emphasizes coverage-guided fuzzing, automated bug triage, and integration into CI/CD. Use when building robust testing infrastructure or finding security vulnerabilities at scale.
---

# Google Continuous Fuzzing

## Overview

Google's continuous fuzzing infrastructure (OSS-Fuzz + ClusterFuzz) has found over 10,000 bugs in 1,000+ open source projects, including critical security vulnerabilities like Heartbleed-class bugs. This technique turns fuzzing from a one-time activity into a continuous quality gate.

## References

- **Paper**: "OSS-Fuzz - Google's continuous fuzzing service for open source software" (USENIX Security '17)
- **Documentation**: https://google.github.io/oss-fuzz/
- **ClusterFuzz**: https://google.github.io/clusterfuzz/

## Core Philosophy

> "Fuzzing should be continuous, not a one-time event."

> "Every bug found by fuzzing is a bug not found by attackers."

Fuzzing is most effective when it runs continuously against the latest code, with automatic bug reporting and regression tracking.

## Key Concepts

### Coverage-Guided Fuzzing

```
Traditional Fuzzing:     Random input generation
Coverage-Guided Fuzzing: Inputs that increase code coverage are kept

Corpus → Mutate → Execute → Measure Coverage → Keep interesting inputs
   ↑                                                      |
   └──────────────────────────────────────────────────────┘
```

### The Fuzzing Pipeline

1. **Build**: Compile with sanitizers (ASan, MSan, UBSan)
2. **Fuzz**: Run fuzzers continuously on cluster
3. **Triage**: Automatically deduplicate and file bugs
4. **Reproduce**: Generate minimal reproducer
5. **Verify**: Confirm fix eliminates the bug
6. **Regress**: Add reproducer to regression corpus

## When Implementing

### Always

- Use sanitizers (AddressSanitizer, MemorySanitizer, UndefinedBehaviorSanitizer)
- Build seed corpus from existing tests and real inputs
- Integrate fuzzing into CI/CD pipeline
- Track coverage metrics over time
- Minimize reproducers for easier debugging
- Keep regression tests for all found bugs

### Never

- Fuzz only once and declare victory
- Ignore crashes in dependencies
- Skip sanitizers to "improve performance"
- Discard valuable corpus data
- Treat fuzzing as separate from testing

### Prefer

- LibFuzzer/AFL++ over basic random testing
- Structure-aware fuzzing for complex formats
- Continuous fuzzing over periodic runs
- Automated triage over manual analysis
- Coverage metrics over time-based metrics

## Implementation Patterns

### Basic Fuzz Target (C/C++)

```cpp
// fuzz_target.cc
// A fuzz target is a function that takes arbitrary bytes

#include <stdint.h>
#include <stddef.h>

// Your library headers
#include "parser.h"

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    // Call the function under test with fuzzer-provided data
    parse_input(data, size);
    
    // Return 0 - non-zero return values are reserved
    return 0;
}

// Build with:
// clang++ -g -fsanitize=address,fuzzer fuzz_target.cc parser.cc -o fuzzer
// Run with:
// ./fuzzer corpus_dir/
```

### Fuzz Target with Structure

```cpp
// Structure-aware fuzzing for better coverage

#include <stdint.h>
#include <stddef.h>
#include <string.h>

// Fuzz a function expecting a specific structure
struct Header {
    uint32_t magic;
    uint32_t version;
    uint32_t length;
    uint8_t  flags;
};

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    // Need at least header size
    if (size < sizeof(Header)) {
        return 0;
    }
    
    Header header;
    memcpy(&header, data, sizeof(Header));
    
    // Constrain to valid magic (helps fuzzer find deeper paths)
    if (header.magic != 0xDEADBEEF) {
        return 0;
    }
    
    // Constrain length to available data
    size_t payload_size = size - sizeof(Header);
    if (header.length > payload_size) {
        header.length = payload_size;
    }
    
    const uint8_t *payload = data + sizeof(Header);
    
    // Now fuzz with valid-looking input
    process_packet(&header, payload, header.length);
    
    return 0;
}
```

### Python Fuzzing with Atheris

```python
#!/usr/bin/env python3
# fuzz_json_parser.py

import atheris
import sys

# Import the module to fuzz
import json

def test_one_input(data):
    """Fuzz target: called with random bytes"""
    fdp = atheris.FuzzedDataProvider(data)
    
    # Convert bytes to string for JSON parsing
    json_str = fdp.ConsumeUnicodeNoSurrogates(
        fdp.ConsumeIntInRange(0, 1024)
    )
    
    try:
        # This should never crash, only raise ValueError
        json.loads(json_str)
    except (json.JSONDecodeError, ValueError):
        pass  # Expected for invalid input
    except Exception as e:
        # Unexpected exception = potential bug
        raise

def main():
    atheris.Setup(sys.argv, test_one_input)
    atheris.Fuzz()

if __name__ == "__main__":
    main()

# Run with:
# python fuzz_json_parser.py corpus_dir/ -max_len=1024
```

### Go Fuzzing (Native)

```go
// fuzz_test.go
// Go 1.18+ has built-in fuzzing support

package parser

import (
    "testing"
)

func FuzzParseInput(f *testing.F) {
    // Seed corpus with known inputs
    f.Add([]byte("valid input"))
    f.Add([]byte("{\"key\": \"value\"}"))
    f.Add([]byte(""))
    
    f.Fuzz(func(t *testing.T, data []byte) {
        // Call function under test
        result, err := ParseInput(data)
        
        if err != nil {
            // Errors are fine, panics are not
            return
        }
        
        // Optionally verify invariants
        if result != nil && result.Length < 0 {
            t.Errorf("negative length: %d", result.Length)
        }
    })
}

// Run with:
// go test -fuzz=FuzzParseInput -fuzztime=60s
```

### OSS-Fuzz Integration

```dockerfile
# Dockerfile for OSS-Fuzz integration

FROM gcr.io/oss-fuzz-base/base-builder

RUN apt-get update && apt-get install -y \
    make \
    autoconf \
    automake \
    libtool

# Clone your project
RUN git clone --depth 1 https://github.com/your/project.git

WORKDIR project
COPY build.sh $SRC/
```

```bash
#!/bin/bash
# build.sh - OSS-Fuzz build script

# Build the library with fuzzing instrumentation
./configure
make clean
make -j$(nproc) CC="$CC" CXX="$CXX" CFLAGS="$CFLAGS" CXXFLAGS="$CXXFLAGS"

# Build fuzz targets
$CXX $CXXFLAGS $LIB_FUZZING_ENGINE \
    fuzz_target.cc -o $OUT/fuzz_target \
    -I. libproject.a

# Copy seed corpus
zip -j $OUT/fuzz_target_seed_corpus.zip seeds/*

# Copy dictionary if available
cp project.dict $OUT/fuzz_target.dict
```

### Corpus Management

```python
# corpus_manager.py
# Manage and minimize fuzzing corpus

import subprocess
import hashlib
import os
from pathlib import Path

class CorpusManager:
    def __init__(self, corpus_dir: str):
        self.corpus_dir = Path(corpus_dir)
        self.corpus_dir.mkdir(exist_ok=True)
    
    def add(self, data: bytes) -> str:
        """Add input to corpus with content-based filename"""
        hash_name = hashlib.sha256(data).hexdigest()[:16]
        path = self.corpus_dir / hash_name
        
        if not path.exists():
            path.write_bytes(data)
        
        return str(path)
    
    def minimize(self, fuzzer_binary: str) -> int:
        """Minimize corpus using fuzzer's merge feature"""
        minimized_dir = self.corpus_dir.parent / "corpus_minimized"
        minimized_dir.mkdir(exist_ok=True)
        
        # LibFuzzer merge minimizes corpus
        result = subprocess.run([
            fuzzer_binary,
            "-merge=1",
            str(minimized_dir),
            str(self.corpus_dir)
        ], capture_output=True)
        
        return len(list(minimized_dir.iterdir()))
    
    def get_coverage_report(self, fuzzer_binary: str) -> dict:
        """Generate coverage report for corpus"""
        # Run with coverage instrumentation
        result = subprocess.run([
            fuzzer_binary,
            "-runs=0",  # Don't generate new inputs
            str(self.corpus_dir)
        ], capture_output=True, text=True)
        
        # Parse coverage from output
        # (actual implementation depends on sanitizer output format)
        return {"corpus_size": len(list(self.corpus_dir.iterdir()))}
```

### CI/CD Integration

```yaml
# .github/workflows/fuzz.yml
name: Continuous Fuzzing

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 0 * * *'  # Daily

jobs:
  fuzz:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Build fuzzer
        run: |
          clang++ -g -O1 \
            -fsanitize=address,fuzzer \
            -fno-omit-frame-pointer \
            fuzz_target.cc -o fuzzer
      
      - name: Download corpus
        uses: actions/cache@v3
        with:
          path: corpus
          key: fuzz-corpus-${{ github.sha }}
          restore-keys: fuzz-corpus-
      
      - name: Run fuzzer
        run: |
          mkdir -p corpus
          timeout 600 ./fuzzer corpus/ -max_total_time=600 || true
      
      - name: Upload crash artifacts
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: crashes
          path: crash-*
          if-no-files-found: ignore
      
      - name: Check for crashes
        run: |
          if ls crash-* 1> /dev/null 2>&1; then
            echo "Crashes found!"
            exit 1
          fi
```

## Mental Model

Google's fuzzing approach asks:

1. **Is this running continuously?** One-time fuzzing misses regression bugs
2. **Are sanitizers enabled?** Crashes without sanitizers miss real bugs
3. **Is the corpus growing?** Coverage should increase over time
4. **Are bugs being tracked?** Automatic filing and deduplication
5. **Are fixes verified?** Reproducers become regression tests

## Signature Moves

- Coverage-guided mutation (LibFuzzer, AFL++)
- Sanitizer builds (ASan, MSan, UBSan, TSan)
- Automatic corpus management and minimization
- CI/CD integration for every commit
- Regression corpus from found bugs
- Structure-aware fuzzing for protocols
