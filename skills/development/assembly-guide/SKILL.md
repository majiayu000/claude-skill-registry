---
name: assembly-guide
description: |
  Assembly language guardrails, patterns, and best practices for AI-assisted development.
  Use when working with assembly files (.asm, .s, .S), or when the user mentions Assembly/x86/ARM.
  Provides calling convention guidelines, register usage patterns, and debugging techniques
  specific to this project's coding standards.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: language
  language: assembly
  extensions: ".asm,.s,.S"
---

# Assembly Guide

> Applies to: x86-64 (System V ABI), ARM64 (AAPCS), NASM, GAS syntax

## Core Principles

1. **Clarity Over Cleverness**: Comment every instruction's purpose; assembly lacks self-documentation
2. **ABI Compliance**: Follow calling conventions precisely for interoperability with C/system code
3. **Minimal Register Pressure**: Preserve callee-saved registers, minimize spills to stack
4. **Correctness First**: Get it working correctly, then profile, then optimize with SIMD
5. **Structured Layout**: Use consistent label naming, section organization, and macro definitions

## Guardrails

### Architecture Selection

- Declare target architecture at the top of every file
- x86-64: default for Linux/macOS server and desktop workloads
- ARM64: default for Apple Silicon, mobile, and embedded Linux
- Never mix architecture-specific code without `%ifdef` / `.ifdef` guards

### Calling Conventions

- **x86-64 System V ABI** (Linux, macOS, BSD):
  - Arguments: `rdi`, `rsi`, `rdx`, `rcx`, `r8`, `r9` (integer/pointer, in order)
  - Floating-point arguments: `xmm0`-`xmm7`
  - Return value: `rax` (integer), `xmm0` (float)
  - Caller-saved (volatile): `rax`, `rcx`, `rdx`, `rsi`, `rdi`, `r8`-`r11`
  - Callee-saved (non-volatile): `rbx`, `rbp`, `r12`-`r15`
  - Stack must be 16-byte aligned before `call` instruction
- **ARM64 AAPCS** (Linux, macOS):
  - Arguments: `x0`-`x7` (integer/pointer), `d0`-`d7` (float)
  - Return value: `x0` (integer), `d0` (float)
  - Callee-saved: `x19`-`x28`, `x29` (frame pointer), `x30` (link register)
  - Stack must be 16-byte aligned at all times

### Register Usage

- Document which registers hold which logical values at function entry
- Never clobber callee-saved registers without saving and restoring them
- Use `rbp` / `x29` as frame pointer for debuggability (omit only in leaf functions)
- Reserve scratch registers for temporaries; name them in comments
- Zero-extend results when returning values smaller than 64 bits

### Stack Management

- Always maintain 16-byte stack alignment on x86-64 and ARM64
- Allocate local variables by subtracting from `rsp` / `sp` in the prologue
- Deallocate in the epilogue before `ret` (never leave the stack dirty)
- Use red zone (128 bytes below `rsp`) only in leaf functions on System V ABI
- Never write below the stack pointer outside the red zone

### Documentation

- File header: purpose, target architecture, assembler syntax, author
- Function header: C-style prototype comment, argument register mapping, return value
- Inline comments: explain the *why*, not the *what* (avoid `; increment counter`)
- Label naming: `module_function_sublabel` (e.g., `crypto_sha256_loop`)
- Constants: use `equ` / `.equ` directives with descriptive names

## Key Patterns

### x86-64 Function with Frame Pointer

```nasm
; long compute(long x, long y, long z)
; Args: rdi = x, rsi = y, rdx = z
; Returns: rax = x * y + z
global compute
compute:
    push    rbp                 ; save frame pointer
    mov     rbp, rsp            ; establish stack frame
    mov     rax, rdi            ; rax = x
    imul    rax, rsi            ; rax = x * y
    add     rax, rdx            ; rax = x * y + z
    pop     rbp                 ; restore frame pointer
    ret
```

### ARM64 AAPCS Function

```asm
// int64_t multiply_add(int64_t a, int64_t b, int64_t c)
// Args: x0 = a, x1 = b, x2 = c  |  Returns: x0 = a * b + c
    .global multiply_add
multiply_add:
    stp     x29, x30, [sp, #-16]!  // save fp and lr
    mov     x29, sp                 // establish stack frame
    mul     x0, x0, x1              // x0 = a * b
    add     x0, x0, x2              // x0 = a * b + c
    ldp     x29, x30, [sp], #16     // restore fp and lr
    ret
```

### SIMD / SSE2 (4 floats per iteration)

```nasm
; void add_f32(float *dst, const float *a, const float *b, size_t n)
; Args: rdi = dst, rsi = a, rdx = b, rcx = n
global add_f32
add_f32:
    shr     rcx, 2              ; n /= 4
.loop:
    test    rcx, rcx
    jz      .done
    movups  xmm0, [rsi]        ; load 4 floats from a
    addps   xmm0, [rdx]        ; add 4 floats from b
    movups  [rdi], xmm0        ; store result
    add     rsi, 16
    add     rdx, 16
    add     rdi, 16
    dec     rcx
    jnz     .loop
.done:
    ret
```

### Linux x86-64 Syscall Interface

```nasm
; Syscall: rax = number, args in rdi/rsi/rdx/r10/r8/r9, return in rax
; Note: r10 replaces rcx (clobbered by syscall instruction)
SYS_WRITE equ 1
SYS_EXIT  equ 60

section .data
    msg db "Hello, world!", 10
    msg_len equ $ - msg

section .text
global _start
_start:
    mov     rax, SYS_WRITE      ; write(stdout, msg, msg_len)
    mov     rdi, 1               ; fd = STDOUT
    lea     rsi, [rel msg]       ; RIP-relative for PIC
    mov     rdx, msg_len
    syscall
    mov     rax, SYS_EXIT        ; exit(0)
    xor     edi, edi
    syscall
```

### Position-Independent Code (PIC)

```nasm
default rel                     ; all memory refs become RIP-relative

section .data
    counter dq 0

section .text
global get_counter
get_counter:
    mov     rax, [counter]      ; RIP-relative with default rel
    ret

global increment_counter
increment_counter:
    lock inc qword [counter]    ; atomic increment (thread-safe)
    mov     rax, [counter]
    ret
```

## Debugging

### GDB Commands

```bash
gdb ./program
(gdb) layout asm                # show disassembly window
(gdb) layout regs               # show registers window
(gdb) stepi                     # step one instruction
(gdb) nexti                     # step over call
(gdb) info registers            # print all register values
(gdb) p/x $rax                  # print rax in hex
(gdb) x/4gx $rsp               # examine 4 quad-words at stack pointer
(gdb) break *0x401000           # break at address
(gdb) display/i $pc             # show current instruction after each step
(gdb) set disassembly-flavor intel
```

### objdump & strace

```bash
objdump -d -M intel program     # disassemble with Intel syntax
objdump -h program              # show section headers
objdump -t program              # show symbol table
objdump -r program.o            # show relocations (PIC debugging)

strace ./program                # trace all syscalls
strace -e trace=write,read ./program  # filter specific syscalls
```

## Tooling

### Assemblers & Linkers

```bash
# NASM (Intel syntax)
nasm -f elf64 -g -F dwarf program.asm -o program.o   # Linux
nasm -f macho64 program.asm -o program.o              # macOS

# GAS (AT&T syntax, supports .intel_syntax)
as --64 -g program.s -o program.o

# LLVM
clang -c program.s -o program.o

# Linking
ld -o program program.o               # bare metal (no libc)
gcc -o program program.o              # with libc (C interop)
gcc -shared -o libfoo.so foo.o        # shared library (requires PIC)
```

### Verification

```bash
nm program.o                    # verify symbol visibility
nm -u program.o                 # check undefined references
readelf -S program.o            # verify section layout
# In GDB: p/x $rsp & 0xf       # should be 0x0 at call boundaries
```

## References

For detailed patterns and code examples, see:

- [references/patterns.md](references/patterns.md) -- Prologue/epilogue, syscall examples, SIMD patterns

## External References

- [x86-64 System V ABI Specification](https://gitlab.com/x86-psABIs/x86-64-ABI)
- [ARM Architecture Reference Manual](https://developer.arm.com/documentation/ddi0487/latest)
- [NASM Documentation](https://www.nasm.us/doc/)
- [GAS Manual (GNU Assembler)](https://sourceware.org/binutils/docs/as/)
- [Intel Intrinsics Guide (SSE/AVX)](https://www.intel.com/content/www/us/en/docs/intrinsics-guide/index.html)
- [Linux Syscall Table (x86-64)](https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/)
- [Agner Fog's Optimization Manuals](https://www.agner.org/optimize/)
- [Felix Cloutier x86 Instruction Reference](https://www.felixcloutier.com/x86/)
