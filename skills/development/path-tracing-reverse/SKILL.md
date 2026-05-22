---
name: path-tracing-reverse
description: This skill provides guidance for reverse engineering compiled binaries to produce equivalent source code. It applies when tasks require analyzing executables, extracting algorithms and constants, and recreating identical program behavior in source form. Use when the goal is byte-for-byte or pixel-perfect reproduction of binary output.
---

# Path Tracing Reverse Engineering

## Overview

This skill guides the systematic reverse engineering of compiled binaries to produce functionally identical source code. The primary challenge is achieving exact output reproduction, not approximate similarity. Common applications include recreating graphics programs (ray tracers, path tracers), understanding proprietary algorithms, and recovering lost source code.

## Critical Success Criteria

Before beginning, establish clear success criteria:

1. **Exact output match**: "identical" means byte-for-byte identical, not visually similar
2. **File size parity**: Output files must match in size (header + data)
3. **Checksum verification**: Use `md5sum` or `sha256sum` to verify exact matches
4. **No tolerance for approximation**: A 99% match is still a failure if 100% is required

## Systematic Approach

### Phase 1: Output Format Analysis

Start with the output format before analyzing the algorithm. Mismatched output formatting causes file size differences that are independent of algorithmic correctness.

1. **Capture reference output**:
   ```bash
   ./mystery > reference_output.ppm
   ls -la reference_output.ppm  # Note exact file size
   xxd reference_output.ppm | head -20  # Examine header bytes
   ```

2. **Analyze header format**:
   - For PPM: Check exact spacing, newlines, and number formatting
   - Compare: `P6\n800 600\n255\n` vs `P6 800 600 255\n`
   - Whitespace differences affect file size

3. **Verify pixel data layout**:
   ```bash
   xxd -s 15 reference_output.ppm | head  # Skip header, view raw pixels
   ```

### Phase 2: Binary Analysis Setup

Create a systematic disassembly workspace:

1. **Extract symbol information**:
   ```bash
   nm ./mystery | grep -E "^[0-9a-f]+ T" > functions.txt
   strings ./mystery > strings.txt
   objdump -t ./mystery > symbols.txt
   ```

2. **Generate complete disassembly**:
   ```bash
   objdump -d ./mystery > disassembly.txt
   objdump -s -j .rodata ./mystery > rodata.txt  # Read-only data
   objdump -s -j .data ./mystery > data.txt      # Initialized data
   ```

3. **Identify main algorithm structure**:
   ```bash
   objdump -d ./mystery | grep -A 50 "<main>:" > main_function.txt
   ```

### Phase 3: Constant Extraction

Extract ALL constants systematically before writing any code:

1. **Float constants**: Located in `.rodata` section
   ```python
   import struct
   # Convert hex bytes to float
   hex_bytes = bytes.fromhex('0000803f')  # Example: 1.0f
   value = struct.unpack('<f', hex_bytes)[0]
   ```

2. **Integer constants**: Often embedded in instructions
   ```bash
   grep -E "mov.*\$0x" disassembly.txt  # Find immediate values
   ```

3. **Create constant catalog**: Document every constant with its:
   - Memory address
   - Raw hex value
   - Decoded value (int/float/double)
   - Suspected purpose

### Phase 4: Algorithm Reconstruction

Reconstruct the algorithm methodically:

1. **Map function call graph**:
   - Identify all `call` instructions in main
   - Trace each called function
   - Document parameters and return values

2. **Trace data flow**:
   - Follow register usage through functions
   - Identify loop structures (counters, bounds)
   - Map memory accesses to array/struct operations

3. **Handle floating-point operations**:
   - Check if code uses SSE/AVX or x87 FPU
   - Note precision: `float` (32-bit) vs `double` (64-bit)
   - SSE: `movss`, `addss`, `mulss` = single precision
   - SSE: `movsd`, `addsd`, `mulsd` = double precision

### Phase 5: Incremental Verification

Never write the entire solution at once. Verify components individually:

1. **Background/base case first**:
   - Render only the background (sky, ground)
   - Compare specific pixel coordinates
   - Achieve 100% match on background before adding objects

2. **Pixel-by-pixel debugging**:
   ```python
   # Create comparison script
   def compare_pixels(ref_file, test_file):
       with open(ref_file, 'rb') as f1, open(test_file, 'rb') as f2:
           ref = f1.read()
           test = f2.read()

       # Find first difference
       for i, (r, t) in enumerate(zip(ref, test)):
           if r != t:
               pixel = (i - header_size) // 3
               x, y = pixel % width, pixel // width
               print(f"First diff at byte {i}, pixel ({x},{y})")
               print(f"Expected: {r}, Got: {t}")
               return
   ```

3. **Coordinate-specific testing**:
   ```bash
   # Extract specific pixel from PPM
   # At offset = header_size + (y * width + x) * 3
   ```

## Common Pitfalls

### Output Format Errors

- **Whitespace in headers**: PPM allows various separators; match exactly
- **Numeric formatting**: `printf("%d", n)` vs `printf("%3d", n)`
- **Line endings**: Unix LF vs Windows CRLF
- **Trailing content**: Extra newlines or padding

### Floating-Point Mismatches

- **Precision mismatch**: Using `double` when binary uses `float`
- **Rounding modes**: Compiler optimizations may change rounding
- **Order of operations**: `(a + b) + c` vs `a + (b + c)` differs in FP
- **Library differences**: `sin()`, `sqrt()` implementations vary

### Algorithmic Assumptions

- **Premature pattern matching**: Don't assume "ray tracer" means standard formulas
- **Missing components**: Multiple light sources, reflections, ambient terms
- **Coordinate systems**: Left-handed vs right-handed, y-up vs y-down
- **Iteration order**: Row-major vs column-major pixel traversal

### Verification Failures

- **Visual comparison is insufficient**: Images may look identical but differ by 1-2 RGB values
- **Partial matches are failures**: 25% match means 75% wrong
- **File size differences indicate format issues**: Address these first

## Verification Strategy

### Automated Testing Harness

Create this script early and use it consistently:

```bash
#!/bin/bash
# verify.sh - Compile, run, and compare

gcc -static -o reversed mystery.c -lm
./mystery > expected.ppm
./reversed > actual.ppm

echo "File sizes:"
ls -la expected.ppm actual.ppm

echo "Checksums:"
md5sum expected.ppm actual.ppm

if cmp -s expected.ppm actual.ppm; then
    echo "SUCCESS: Files are identical"
else
    echo "FAILURE: Files differ"
    cmp -l expected.ppm actual.ppm | head -20
fi
```

### Progressive Debugging

When outputs differ:

1. **Verify file sizes first** - format issues vs algorithm issues
2. **Find first differing byte** - localize the problem
3. **Convert byte offset to coordinates** - identify which pixel/component
4. **Compare expected vs actual at that location** - understand the discrepancy
5. **Trace the calculation** - work backward to find the bug

### Checkpoint Validation

At each phase, verify:
- [ ] Header format matches exactly
- [ ] Background pixels match (no objects)
- [ ] Object boundaries are correct
- [ ] Lighting/shading values match
- [ ] Final checksum matches

## Tool Reference

Essential tools for binary analysis:

| Tool | Purpose |
|------|---------|
| `objdump -d` | Disassembly |
| `objdump -s -j .rodata` | Read-only data section |
| `nm` | Symbol table |
| `strings` | Embedded strings |
| `xxd` | Hex dump |
| `gdb` | Dynamic analysis |
| `ltrace` | Library call tracing |
| `strace` | System call tracing |

## Resources

This skill includes reference materials to support reverse engineering tasks:

### references/

- `reverse_engineering_checklist.md` - Step-by-step verification checklist
- `float_extraction.md` - Guide to extracting floating-point constants from binaries
