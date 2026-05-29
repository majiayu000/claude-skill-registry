---
description: Configures and builds YARS with optimizations for performance testing and benchmarking
version: 1.0.0
allowed-tools: [Bash]
---

# Release Build

This skill creates an optimized release build of YARS for performance testing and benchmarking.

## Usage

Automatically invoked when:
- User asks for a release or optimized build
- Running performance benchmarks
- Preparing for final validation tests
- Need maximum simulation speed

## Steps

```bash
# Navigate to build directory
cd build

# Configure for release mode
cmake -DCMAKE_BUILD_TYPE=Release ..

# Build with parallel jobs
make -j4
```

## Success Criteria

- ✅ CMake configures with Release build type
- ✅ Compilation includes optimizations (-O3 or similar)
- ✅ Debug symbols stripped or minimal
- ✅ Binary ready for performance testing

## Notes

- Release builds are faster but harder to debug
- Full compiler optimizations enabled
- Use this for performance benchmarks and production use
- To switch back to debug, use the debug-build skill
- Default build type if not specified
