---
name: make-doom-for-mips
description: Guidance for cross-compiling complex C programs (like Doom) to run on custom MIPS virtual machines or emulators. This skill should be used when tasked with building software for non-standard MIPS targets that use custom syscall interfaces, require freestanding compilation (-nostdlib), or involve running binaries in JavaScript/custom VM environments.
---

# Cross-Compiling Complex C Programs for Custom MIPS VMs

## Overview

This skill provides guidance for cross-compiling complex C codebases (such as Doom) to run on custom MIPS virtual machines or emulators. The primary challenge is bridging the gap between standard C library expectations and a custom runtime environment with its own syscall interface, memory layout, and instruction support.

## Critical First Steps: Understanding the Target Environment

Before writing any code, thoroughly analyze the target VM to understand its requirements:

### 1. Analyze the VM's Syscall Interface

Read the VM source code to extract the exact syscall interface:
- Identify syscall numbers (e.g., SYS_read=0, SYS_write=1, etc.)
- Understand the calling convention (which registers hold arguments and return values)
- Document all supported syscalls and their signatures
- Note any custom syscalls specific to the VM

### 2. Determine Endianness and ABI

Verify the target architecture details by examining the VM source:
- Endianness (little-endian vs big-endian MIPS)
- Floating-point support (hardware vs soft-float)
- Word size (32-bit vs 64-bit)
- ABI variant (o32, n32, n64)

### 3. Understand Memory Layout

From the VM source, extract:
- Expected entry point address
- Stack location and size
- Heap boundaries
- Text/data segment placement
- Any memory-mapped I/O regions

### 4. Identify Supported Instructions

Check for instruction limitations:
- Floating-point instruction support
- Privileged instructions
- Branch delay slot handling
- Any unimplemented instructions that will cause VM termination

## Systematic Approach to Freestanding Compilation

### Phase 1: Comprehensive Header Analysis

Before compiling, scan all source files to identify required headers:

```bash
# Find all included headers
grep -rh '#include' src/ | sort -u
```

Create stub headers for ALL identified system headers upfront rather than reactively fixing one error at a time. Common headers needed for complex C programs:
- `<stdio.h>`, `<stdlib.h>`, `<string.h>`, `<stdint.h>`
- `<limits.h>`, `<stddef.h>`, `<stdarg.h>`
- `<ctype.h>`, `<math.h>`, `<time.h>`
- `<errno.h>`, `<assert.h>`, `<fcntl.h>`
- `<unistd.h>`, `<sys/types.h>`, `<sys/stat.h>`

### Phase 2: Standard Library Implementation

Create a comprehensive stdlib replacement with COMPLETE implementations:

**Critical functions that must work correctly (not return 0 or stub):**
- `printf`, `fprintf`, `sprintf`, `snprintf` - Used for debug output and parsing
- `sscanf`, `fscanf` - Used for configuration parsing
- `malloc`, `free`, `realloc` - Memory management
- `memcpy`, `memset`, `memmove`, `strlen`, `strcmp`, `strcpy` - String/memory operations
- `atoi`, `atol`, `strtol` - Number parsing
- `fopen`, `fread`, `fwrite`, `fclose`, `fseek`, `ftell` - File I/O

**Warning signs of incomplete implementations:**
- Functions returning 0 unconditionally
- Empty function bodies
- "TODO" or stub comments
- Missing format specifier handling in printf-family functions

### Phase 3: Linker Script Configuration

Create a linker script that matches the VM's expectations:
- Entry point symbol must match what the VM looks for
- Section addresses must align with VM memory layout
- Stack initialization must be included in startup code
- Verify `.text`, `.data`, `.bss`, `.rodata` placement

## Verification Strategies

### 1. Syscall Verification

After implementing syscalls, verify each one works:
```c
// Test write syscall
const char *msg = "Syscall test\n";
write(1, msg, strlen(msg));

// Test read syscall
char buf[100];
int n = read(0, buf, sizeof(buf));

// Test file operations
int fd = open("/path/to/file", O_RDONLY);
// etc.
```

### 2. Entry Point Verification

Confirm the entry point matches:
```bash
# Check the ELF entry point
mips-*-readelf -h output.elf | grep Entry

# Verify symbol is at expected address
mips-*-nm output.elf | grep __start
```

### 3. Map File Analysis for Debugging

Generate and use map files to debug crashes:
```bash
# Generate map file during linking
-Wl,-Map=output.map

# When program terminates at specific PC, find the function:
grep "0x40b7b0" output.map
```

### 4. Incremental Testing

Test components in isolation before full integration:
1. Minimal "hello world" to verify basic execution
2. Memory allocation test program
3. File I/O test program
4. Individual library function tests
5. Finally, the full application

## Common Pitfalls and Solutions

### Pitfall 1: ABI Mismatch Warnings

**Problem:** Linking soft-float compiled code with hard-float libgcc produces warnings:
```
warning: linking soft-float module with hard-float module
```

**Impact:** Can cause runtime crashes when floating-point values are passed/returned.

**Solution:** Ensure consistent ABI across all compilation units:
```bash
-msoft-float -mfloat-abi=soft
```
Or provide soft-float libgcc, or implement soft-float routines.

### Pitfall 2: Incomplete printf/scanf Implementation

**Problem:** Returning 0 or doing nothing in printf-family functions.

**Impact:** Configuration parsing fails silently; debug output disappears.

**Solution:** Implement at least these format specifiers:
- `%d`, `%i`, `%u`, `%x`, `%X` - integers
- `%s` - strings
- `%c` - characters
- `%p` - pointers
- Width and precision modifiers

### Pitfall 3: Missing Function Implementations

**Problem:** Compiler warnings about implicit function declarations.

**Impact:** Undefined behavior at runtime; usually crashes.

**Solution:** Treat ALL implicit declaration warnings as errors:
```bash
-Werror=implicit-function-declaration
```

### Pitfall 4: Incorrect Syscall Numbers

**Problem:** Using standard Linux syscall numbers when VM uses different numbers.

**Impact:** Wrong operations executed; silent corruption or crashes.

**Solution:** Extract exact syscall numbers from VM source before implementation.

### Pitfall 5: Premature Termination Without Investigation

**Problem:** Program terminates early; assuming it's due to missing data files.

**Impact:** Real bugs (unimplemented instructions, invalid memory access, failed syscalls) go undiagnosed.

**Solution:** Always investigate termination:
1. Check the PC address in the map file
2. Examine the VM's termination handling code
3. Add instrumentation to log syscalls and critical operations
4. Verify data files are accessible at expected paths

### Pitfall 6: Reactive Header Creation

**Problem:** Creating stub headers one-by-one as compilation errors appear.

**Impact:** Slow iteration; easy to miss dependencies.

**Solution:** Analyze all includes upfront and create comprehensive stubs before first compile attempt.

## Debugging Strategies

### When the Binary Terminates Early

1. **Get the termination address** from VM output
2. **Look up address in map file** to identify the function
3. **Check for unimplemented instructions** at that location
4. **Verify syscall was valid** if termination is in syscall handler
5. **Check memory access** if termination is in memory operation

### When Output is Missing/Incorrect

1. **Verify write syscall** reaches the correct output
2. **Check file descriptors** are mapped correctly
3. **Trace printf calls** to ensure they reach write syscall
4. **Verify buffer handling** in I/O functions

### When the Program Crashes Silently

1. **Add diagnostic output** at key checkpoints
2. **Implement signal handlers** if VM supports them
3. **Check stack overflow** - increase stack size
4. **Verify heap operations** - add malloc/free tracing

## Compilation Flags Reference

Essential flags for freestanding MIPS compilation:
```bash
-nostdlib              # No standard library
-ffreestanding         # Freestanding environment
-mips32                # MIPS32 instruction set (or appropriate variant)
-EL                    # Little-endian (or -EB for big-endian)
-msoft-float           # Software floating-point
-mno-abicalls          # No PIC/GOT (if VM doesn't support)
-fno-pic               # No position-independent code
-static                # Static linking
-Wl,-Map=output.map    # Generate map file for debugging
```
