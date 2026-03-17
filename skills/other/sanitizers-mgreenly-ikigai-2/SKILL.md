---
name: sanitizers
description: Sanitizers skill for the ikigai project
---

# Sanitizers

## Description
Interpreting AddressSanitizer, UndefinedBehaviorSanitizer, and ThreadSanitizer output.

## Build Modes

```bash
make BUILD=sanitize check   # ASan + UBSan
make BUILD=tsan check       # ThreadSanitizer (incompatible with ASan)
```

## AddressSanitizer (ASan)

Detects buffer overflows, use-after-free, use-after-return, memory leaks.

### Sample Output
```
==12345==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x...
READ of size 4 at 0x... thread T0
    #0 0x... in function_name file.c:42
    #1 0x... in caller file.c:100

0x... is located 0 bytes to the right of 100-byte region [0x...,0x...)
allocated by thread T0 here:
    #0 0x... in malloc (...)
    #1 0x... in allocate_buffer file.c:30
```

### Error Types
- **heap-buffer-overflow** - Read/write past heap allocation
- **stack-buffer-overflow** - Read/write past stack buffer
- **global-buffer-overflow** - Read/write past global
- **heap-use-after-free** - Accessing freed heap memory
- **stack-use-after-return** - Accessing returned stack frame
- **double-free** - Freeing already-freed memory

### Environment Variables
```bash
ASAN_OPTIONS=detect_leaks=1:abort_on_error=1 ./ikigai
```
- `detect_leaks=1` - Enable leak detection
- `abort_on_error=1` - Abort on first error (for core dumps)
- `halt_on_error=0` - Continue after error
- `print_stats=1` - Print memory stats

## UndefinedBehaviorSanitizer (UBSan)

Detects undefined behavior: integer overflow, null dereference, alignment issues.

### Sample Output
```
file.c:42:15: runtime error: signed integer overflow:
2147483647 + 1 cannot be represented in type 'int'
```

### Error Types
- **signed integer overflow** - Arithmetic overflow
- **null pointer passed** - NULL where non-null expected
- **load of misaligned address** - Alignment violation
- **member access within null pointer** - NULL struct dereference
- **division by zero** - Self-explanatory
- **shift exponent is negative** - Invalid shift

### Environment Variables
```bash
UBSAN_OPTIONS=print_stacktrace=1:halt_on_error=1 ./ikigai
```

## ThreadSanitizer (TSan)

Detects data races and deadlocks.

### Sample Output
```
WARNING: ThreadSanitizer: data race (pid=12345)
  Write of size 4 at 0x... by thread T1:
    #0 function_name file.c:42
  Previous read of size 4 at 0x... by main thread:
    #0 other_function file.c:100
  Location is global 'shared_var' of size 4 at 0x...
```

### Error Types
- **data race** - Unsynchronized access to shared data
- **lock-order-inversion** - Potential deadlock
- **thread leak** - Thread not joined

### Environment Variables
```bash
TSAN_OPTIONS=halt_on_error=1:second_deadlock_stack=1 ./ikigai
```

## Debugging Workflow

1. Run with sanitizer enabled
2. Read error message top-to-bottom
3. First stack trace = where error detected
4. Second stack trace = where memory allocated/related operation
5. Fix root cause, not symptom

## Limitations

- ASan and TSan are **mutually exclusive** (can't use both)
- Sanitizers add ~2x memory overhead, ~2x slowdown
- Some false positives possible with complex code

## References

- ASan docs: https://clang.llvm.org/docs/AddressSanitizer.html
- UBSan docs: https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html
- TSan docs: https://clang.llvm.org/docs/ThreadSanitizer.html
