---
name: vulnerable-secret
description: This skill provides guidance for extracting secrets from vulnerable executables. It should be used when tasks involve binary analysis, reverse engineering executables to find hidden flags/secrets, or exploiting buffer overflows and other vulnerabilities to extract protected data. Applicable to CTF challenges, security research, and authorized penetration testing scenarios.
---

# Vulnerable Secret Extraction

## Overview

This skill guides the analysis and exploitation of vulnerable executables to extract hidden secrets, flags, or keys. It covers both static analysis (disassembly, string extraction) and dynamic analysis (exploitation, fuzzing) approaches.

## Initial Assessment

Before beginning analysis, perform these essential checks:

### 1. Tool Availability Check

Run a comprehensive tool check early to plan the analysis strategy:

```bash
# Check for available analysis tools
which objdump readelf strings nm gdb ltrace strace file hexdump xxd 2>/dev/null
```

Document which tools are available and adjust the approach accordingly. Missing tools significantly constrain analysis options.

### 2. Binary Identification

Identify the executable type and characteristics:

```bash
file <executable>           # File type, architecture, linking
readelf -h <executable>     # ELF header details
readelf -S <executable>     # Section headers
```

### 3. Initial String Extraction

Extract and examine strings for clues about the challenge:

```bash
strings <executable> | head -100              # Overview of strings
strings <executable> | grep -i flag           # Search for flag patterns
strings <executable> | grep -i secret         # Search for secret patterns
strings <executable> | grep -i password       # Search for password patterns
strings <executable> | grep -iE "auth|bypass" # Authentication-related strings
```

**Important**: Try multiple case variations and partial matches before concluding strings don't contain the target.

## Analysis Approaches

Choose the approach based on available tools and initial findings.

### Approach 1: Dynamic Analysis (Preferred When Tools Available)

If debugging tools (gdb, ltrace, strace) are available, start with dynamic analysis:

1. **Determine program behavior**: Run the executable to understand expected input/output
2. **Trace system calls**: Use strace to observe file operations and system interactions
3. **Trace library calls**: Use ltrace to observe function calls (especially crypto functions)
4. **Debug interactively**: Use gdb to set breakpoints and examine memory at runtime

### Approach 2: Static Analysis (When Dynamic Tools Unavailable)

When debugging tools are unavailable, use static analysis:

1. **Disassemble critical sections**:
   ```bash
   objdump -d <executable> | less
   objdump -d <executable> -M intel   # Intel syntax may be clearer
   ```

2. **Examine symbol tables**:
   ```bash
   nm <executable>                     # List symbols
   readelf -s <executable>             # Symbol table details
   ```

3. **Look for encoded data sections**:
   ```bash
   readelf -x .rodata <executable>     # Read-only data section
   readelf -x .data <executable>       # Data section
   ```

### Approach 3: Exploitation (When Vulnerability Is Indicated)

If strings or symbols suggest a specific vulnerability (e.g., "buffer overflow", "gets", "strcpy"):

1. **Identify the vulnerability type** from function names and strings
2. **Analyze the vulnerable function** in disassembly
3. **Craft appropriate exploit input**
4. **Test incrementally** with varying payload sizes

## Common Encoding Detection

### XOR Encoding

Signs of XOR encoding in disassembly:
- `xor` instructions in loops
- Single-byte key applied repeatedly
- Data section bytes that don't decode as ASCII directly

To decode XOR-encoded data:
```python
# Example: XOR decode with known key
encoded = bytes.fromhex("HEXDATA")
key = 0xNN  # Single byte key
decoded = bytes([b ^ key for b in encoded])
print(decoded.decode())
```

### Other Encodings

- **Base64**: Look for `=` padding, character set A-Za-z0-9+/
- **Hex strings**: Pairs of 0-9A-Fa-f characters
- **ROT13/Caesar**: Alphabetic shifts

## Verification Strategies

### Data Extraction Verification

Before processing extracted data:
1. **Clean the data**: Remove spaces, newlines, and formatting artifacts from tool output
2. **Validate format**: Ensure hex strings have even length, Base64 has valid characters
3. **Check boundaries**: Verify start and end markers of extracted data

### Solution Verification

After extracting a potential secret:
1. **Format validation**: Confirm it matches expected format (e.g., `FLAG{...}`, `CTF{...}`)
2. **Character check**: Ensure decoded content contains only expected characters
3. **Completeness check**: Verify the secret appears complete (proper opening/closing braces)

## Common Pitfalls

### 1. Ignoring Intended Solution Path

When strings suggest a specific vulnerability type (e.g., flag contains "buffer_overflow"):
- **Always attempt the intended exploitation path** before falling back to static analysis
- The pedagogical value and completeness of the solution may depend on proper exploitation

### 2. Data Extraction Errors

When copying hex data from tool output:
- **Remove all whitespace** before processing
- **Verify byte boundaries** (even number of hex characters)
- **Double-check copy-paste accuracy** before running decode commands

### 3. Incomplete Exploration

Before moving to complex analysis:
- Try **multiple grep patterns** with case variations
- Examine **authentication bypass** conditions shown in strings
- Check for **multiple encoded sections** (not just the first one found)

### 4. Tool Output Assumptions

When analyzing disassembly:
- **Document what is observed vs. inferred**
- **Reference specific addresses** only when they appear in actual output
- **Verify assumptions** about program flow before acting on them

### 5. Missing Validation Steps

Always verify:
- Output file permissions and existing content
- Extracted flag format before writing to results
- Whether there may be additional encoded data

## Workflow Summary

```
1. Check tool availability
2. Identify binary type and characteristics
3. Extract and analyze strings
4. If vulnerability indicated → attempt exploitation
5. If exploitation fails/unavailable → use static analysis
6. Identify encoding (XOR, Base64, etc.)
7. Clean extracted data carefully
8. Decode and verify format
9. Validate completeness before writing results
```

## References

For detailed guidance on specific analysis techniques, see `references/binary_analysis_guide.md`.
