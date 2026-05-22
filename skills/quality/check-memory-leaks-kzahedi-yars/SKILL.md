---
description: Runs valgrind memory leak detection on YARS to identify memory issues
version: 1.0.0
allowed-tools: [Bash, Read]
---

# Check Memory Leaks

This skill uses valgrind to detect memory leaks and memory errors in YARS.

## Usage

Automatically invoked when:
- User asks to check for memory leaks
- After refactoring memory management
- During observer pattern removal work
- Before major releases or commits

## Steps

```bash
# Navigate to build directory
cd build

# Ensure debug build for better stack traces
cmake -DCMAKE_BUILD_TYPE=Debug .. && make -j4

# Run valgrind with leak check
valgrind --leak-check=full \
         --show-leak-kinds=all \
         --track-origins=yes \
         --verbose \
         --log-file=valgrind-output.txt \
         ./bin/yars --iterations 100 --xml ../xml/braitenberg.xml

# Display results
cat valgrind-output.txt
```

## Success Criteria

- ✅ No definite memory leaks detected
- ✅ No invalid memory accesses
- ✅ All heap blocks properly freed
- ✅ Clean valgrind summary

## Analysis

Valgrind reports to watch for:
- **Definitely lost**: Critical leaks that must be fixed
- **Indirectly lost**: Memory leaked due to parent structure
- **Possibly lost**: May indicate real leaks
- **Still reachable**: Memory not freed at exit (less critical)
- **Invalid reads/writes**: Memory access errors

## Notes

- Valgrind significantly slows execution (10-30x slower)
- Use fewer iterations (100-500) to keep runtime reasonable
- Debug build provides better stack traces
- Some false positives possible from external libraries
- Focus on "definitely lost" and "invalid" errors first
