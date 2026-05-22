---
description: Configures and builds YARS with debug symbols for debugging with valgrind or gdb
version: 1.0.0
allowed-tools: [Bash]
---

# Debug Build

This skill creates a debug build of YARS with full debug symbols for debugging sessions.

## Usage

Automatically invoked when:
- User asks for a debug build
- Preparing to use valgrind or gdb
- Need to debug crashes or memory issues
- Investigating specific runtime behavior

## Steps

```bash
# Navigate to build directory
cd build

# Configure for debug mode
cmake -DCMAKE_BUILD_TYPE=Debug ..

# Build with parallel jobs
make -j4
```

## Success Criteria

- ✅ CMake configures with Debug build type
- ✅ Compilation includes debug symbols (-g flag)
- ✅ No optimizations that would interfere with debugging
- ✅ Binary ready for valgrind/gdb usage

## Notes

- Debug builds are larger and slower than release builds
- Optimizations are disabled for better debugging experience
- Use this before running memory leak checks or debuggers
- To switch back to release, use the release-build skill
