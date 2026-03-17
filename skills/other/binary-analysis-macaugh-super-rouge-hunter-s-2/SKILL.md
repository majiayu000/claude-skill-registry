---
name: Binary Analysis and Reverse Engineering
description: Systematic approach to analyzing compiled binaries, understanding program behavior, and identifying vulnerabilities without source code access
when_to_use: When analyzing closed-source software, malware analysis, understanding proprietary protocols, or assessing compiled applications for security vulnerabilities
version: 1.0.0
languages: assembly, c, python
---

# Binary Analysis and Reverse Engineering

## Overview

Binary analysis examines compiled executables without access to source code. This skill combines static analysis (disassembly, decompilation) with dynamic analysis (debugging, tracing) to understand program behavior, identify vulnerabilities, and reverse engineer functionality.

**Core principle:** Combine static and dynamic analysis. Static reveals structure; dynamic reveals behavior.

## When to Use

- Analyzing closed-source software for vulnerabilities
- Malware analysis and understanding
- Reverse engineering proprietary protocols
- Understanding third-party libraries or dependencies
- CTF challenges and security research
- Verifying security claims of binary-only software

## Analysis Workflow

### Phase 1: Initial Assessment

**Goal:** Understand what you're analyzing and gather basic information.

```bash
# File type and architecture
file binary
# ELF 64-bit LSB executable, x86-64, dynamically linked

# Strings (quick insight into functionality)
strings binary | less

# Dependencies
ldd binary
# Check for linked libraries

# Security features
checksec binary
# RELRO, Stack Canary, NX, PIE, FORTIFY

# Basic metadata
readelf -h binary  # ELF headers
objdump -p binary  # Program headers
```

### Phase 2: Static Analysis

**Goal:** Understand program structure without execution.

#### Disassembly

```bash
# Linear disassembly
objdump -d binary > disassembly.txt

# Intelligent disassembly with Ghidra
# 1. Import binary into Ghidra
# 2. Analyze with default options
# 3. Review function list, strings, cross-references

# IDA Pro (commercial but powerful)
# - Advanced decompilation
# - Cross-references
# - Graph view
```

#### Function Analysis

```python
# Using radare2
"""
$ r2 binary
[0x00001000]> aa   # Analyze all
[0x00001000]> afl  # List functions
[0x00001000]> pdf @ main  # Disassemble main
[0x00001000]> VV @ main   # Visual graph mode
"""

# Common patterns to look for:
# - Entry point and main function
# - Vulnerable functions (strcpy, gets, sprintf)
# - Cryptographic operations
# - Network operations (socket, connect, send)
# - File operations (fopen, read, write)
# - Privilege operations (setuid, system)
```

#### Control Flow Analysis

```python
"""
Analyze program flow:

1. Identify entry point
2. Follow execution paths
3. Identify decision points (if/else, switch)
4. Map loops and recursion
5. Identify error handling
6. Find return points

Key questions:
- What are the main code paths?
- Where does user input enter?
- What validation occurs?
- Where are dangerous operations?
"""
```

### Phase 3: Dynamic Analysis

**Goal:** Observe actual program behavior during execution.

#### Debugging with GDB

```bash
# Start GDB
gdb ./binary

# Set breakpoints
(gdb) break main
(gdb) break *0x401234  # Specific address

# Run with arguments
(gdb) run arg1 arg2

# Examine registers
(gdb) info registers

# Examine memory
(gdb) x/10x $rsp      # 10 hex words at stack pointer
(gdb) x/s 0x404000    # String at address

# Step through code
(gdb) stepi           # Step one instruction
(gdb) nexti           # Step over function call
(gdb) continue        # Continue to next breakpoint

# Display on each step
(gdb) display/i $pc   # Show current instruction
(gdb) display/x $rax  # Show RAX register
```

#### Enhanced GDB with PEDA/GEF/pwndbg

```bash
# Install PEDA
git clone https://github.com/longld/peda.git ~/peda
echo "source ~/peda/peda.py" >> ~/.gdbinit

# Or GEF (recommended)
bash -c "$(curl -fsSL https://gef.blah.cat/sh)"

# Enhanced features:
# - Color coding
# - Automatic display of registers, stack, code
# - Pattern creation/offset calculation
# - ROP gadget search
# - Heap analysis
```

#### System Call Tracing

```bash
# Trace system calls
strace ./binary

# Trace with details
strace -v -s 1024 ./binary

# Trace specific syscalls
strace -e trace=open,read,write ./binary

# Trace library calls
ltrace ./binary

# Follow child processes
strace -f ./binary
```

#### Dynamic Instrumentation

```python
# Using Frida for runtime instrumentation
import frida
import sys

def on_message(message, data):
    print(f"[*] {message}")

# Attach to process
session = frida.attach("target_process")

# JavaScript to inject
script_code = """
Interceptor.attach(Module.findExportByName(null, 'strcmp'), {
    onEnter: function(args) {
        console.log('[*] strcmp called');
        console.log('    arg1: ' + Memory.readUtf8String(args[0]));
        console.log('    arg2: ' + Memory.readUtf8String(args[1]));
    },
    onLeave: function(retval) {
        console.log('    return: ' + retval);
    }
});
"""

script = session.create_script(script_code)
script.on('message', on_message)
script.load()
sys.stdin.read()
```

### Phase 4: Vulnerability Identification

**Common Vulnerability Patterns:**

#### Buffer Overflow

```asm
; Look for unsafe string operations
call strcpy     ; No bounds checking
call gets       ; Always unsafe
call sprintf    ; No bounds checking

; Check for:
; - Fixed-size buffers
; - User-controlled input
; - No size validation
```

#### Format String

```asm
; User input directly to printf
mov rdi, [user_input]
call printf     ; Dangerous if user_input has format specifiers
```

#### Use After Free

```asm
; Pattern:
call free       ; Free memory
; ... later ...
mov rax, [ptr]  ; Use freed pointer
```

#### Integer Overflow

```asm
; Look for:
; - Size calculations
; - Loop counters
; - Memory allocation sizes

imul eax, [count], 8  ; Can overflow
call malloc           ; Allocates wrong size
```

### Phase 5: Exploit Development

See skills/exploitation/exploit-dev-workflow for detailed exploitation process.

## Tool Ecosystem

### Disassemblers/Decompilers

**Ghidra (Free)**
```bash
# NSA's reverse engineering suite
# Features:
# - Decompiler (C-like output)
# - Cross-references
# - Scripting (Python/Java)
# - Collaborative analysis

# Download from: https://ghidra-sre.org/
```

**IDA Pro (Commercial)**
- Industry standard
- Best-in-class decompiler (Hex-Rays)
- Extensive plugin ecosystem
- IDA Free available with limitations

**Binary Ninja (Commercial)**
- Modern UI
- Medium-level IL
- Good API for automation
- Active development

**radare2 (Free)**
```bash
# Command-line focused
# Steep learning curve but powerful

# Basic workflow
r2 binary
[0x00001000]> aa        # Analyze
[0x00001000]> afl       # Functions
[0x00001000]> s main    # Seek to main
[0x00001000]> pdf       # Disassemble
[0x00001000]> VV        # Visual graph
```

### Debuggers

**GDB with Extensions**
- PEDA - Python Exploit Development Assistance
- GEF - GDB Enhanced Features
- pwndbg - Exploit development focused

**WinDbg (Windows)**
- Microsoft's debugger
- Kernel and user-mode debugging
- Essential for Windows analysis

**x64dbg (Windows)**
- Modern UI
- Plugin support
- Good for malware analysis

### Dynamic Analysis

**Frida**
- Dynamic instrumentation
- JavaScript API
- Cross-platform
- Runtime modification

**PIN/DynamoRIO**
- Dynamic binary instrumentation frameworks
- Research-grade tools
- Performance analysis

**Valgrind**
```bash
# Memory debugging
valgrind --leak-check=full ./binary

# Memory profiling
valgrind --tool=massif ./binary
```

## Common Analysis Scenarios

### Scenario 1: Finding Hardcoded Credentials

```bash
# Search strings
strings binary | grep -i "password\|secret\|key"

# In Ghidra:
# 1. Window -> Defined Strings
# 2. Search for interesting patterns
# 3. Check cross-references to see usage
```

### Scenario 2: Understanding Network Protocol

```bash
# 1. Trace network calls
strace -e trace=network ./binary

# 2. Analyze send/recv calls in disassembly
# 3. Set breakpoints on socket operations
gdb ./binary
(gdb) break send
(gdb) break recv

# 4. Capture actual packets
tcpdump -i lo -w capture.pcap

# 5. Analyze protocol structure
wireshark capture.pcap
```

### Scenario 3: Bypassing License Check

```bash
# 1. Search for error messages
strings binary | grep -i "license\|trial\|expired"

# 2. Find string references in Ghidra
# 3. Understand check logic
# 4. Identify bypass point

# Options:
# - Patch binary (change jump condition)
# - Hook function at runtime (Frida)
# - Modify return value in debugger
```

### Scenario 4: Extracting Encryption Keys

```python
# Dynamic approach - hook crypto functions
"""
Interceptor.attach(Module.findExportByName('libcrypto.so', 'AES_set_encrypt_key'), {
    onEnter: function(args) {
        console.log('[*] AES key:');
        console.log(hexdump(args[0], { length: 32 }));
    }
});
"""

# Static approach - look for key initialization
# - Search for crypto constants (S-boxes, magic numbers)
# - Analyze key derivation functions
# - Check for embedded keys
```

## Practical Tips

### Naming Conventions

```python
# In disassemblers, rename variables/functions for clarity
# Bad:  FUN_00401234(local_10, DAT_00404000)
# Good: validate_input(user_buffer, key_string)

# Document as you analyze
# Add comments explaining complex logic
# Create structure definitions for data
```

### Cross-Reference Analysis

```python
# Follow data flow:
# 1. Find interesting data (strings, constants)
# 2. Find references (where it's used)
# 3. Understand context of use
# 4. Trace back to source

# Example: Password validation
# "Invalid password" string
#   -> Used in check_password()
#   -> Called from login()
#   -> Gets input from get_user_input()
```

### Identifying Compiler Artifacts

```asm
; Stack canary check (GCC)
mov rax, fs:0x28
mov [rbp-0x8], rax
; ... function body ...
mov rdx, [rbp-0x8]
xor rdx, fs:0x28
je .no_corruption
call __stack_chk_fail

; C++ name mangling
_ZN6Class14memberFunctionEi  ; Class1::memberFunction(int)
```

## Anti-Analysis Techniques

**Detection:**
- Debugger detection (ptrace, IsDebuggerPresent)
- Timing checks
- Code obfuscation
- Anti-disassembly tricks

**Countermeasures:**
```python
# Patch debugger checks
# In GDB:
(gdb) break ptrace
(gdb) return 0

# Use stealthy debuggers
# - ScyllaHide (plugin)
# - Custom tools

# Deobfuscation
# - Symbolic execution (angr)
# - Dynamic unpacking
# - Pattern matching
```

## Common Pitfalls

| Mistake | Impact | Solution |
|---------|--------|----------|
| Only static analysis | Miss runtime behavior | Combine static + dynamic |
| Not documenting findings | Lose context | Take detailed notes |
| Analyzing without goal | Waste time | Define specific objectives |
| Ignoring cross-references | Miss important connections | Follow all references |
| Not checking compiler version | Misinterpret artifacts | Identify compiler/flags used |

## Integration with Other Skills

- skills/analysis/zero-day-hunting - Finding vulnerabilities in binaries
- skills/exploitation/exploit-dev-workflow - Exploiting discovered flaws
- skills/analysis/static-vuln-analysis - Source code analysis if available

## Legal and Ethical Considerations

**Authorization Required:**
- Only analyze authorized software
- Respect license agreements
- Don't distribute cracked software
- Follow responsible disclosure

**Legitimate Use Cases:**
- Security research with permission
- Malware analysis for defense
- Own software assessment
- Educational purposes with legal samples

## Success Metrics

- Understanding program functionality
- Identifying security vulnerabilities
- Extracting useful intelligence
- Creating working exploits (if authorized)
- Comprehensive documentation

## References and Further Reading

- "Practical Reverse Engineering" by Dang et al.
- "The IDA Pro Book" by Chris Eagle
- "Practical Binary Analysis" by Dennis Andriesse
- Ghidra documentation and training materials
- Malware analysis books (for dynamic analysis techniques)
- Assembly language references (Intel manuals, x86-64 ABI)
- CTF write-ups for practical examples
