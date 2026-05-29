---
name: windows-boundaries
description: Windows security boundary attacks — kernel/user boundary, sandbox escape, AppContainer/LPAC bypass, COM/RPC boundary, integrity levels, PPL exploitation
metadata:
  type: offensive
  phase: exploitation
kill_chain:
  phase: [exploit, install]
  step: [4, 5]
  attck_tactics: [TA0002, TA0004]
depends_on: [privesc-windows, exploit-development]
feeds_into: [red-team-ops]
inputs: [sandbox_config, kernel_info]
outputs: [boundary_escape, elevated_access]
  ---

# Windows Security Boundaries

## When to Activate

- Planning privilege escalation paths through security boundaries
- Sandbox escape research (browser, Office, AppContainer)
- Understanding Windows security architecture for exploitation
- Kernel/user boundary crossing

## Security Boundary Taxonomy

```
┌─────────────────────────────────────────────────────┐
│                    VTL1 (Secure World)               │
│  Credential Guard, HVCI, Secure Kernel              │
├─────────────────────────────────────────────────────┤
│                    VTL0 (Normal World)               │
│  ┌───────────────────────────────────────────────┐  │
│  │              Kernel Mode (Ring 0)              │  │
│  │  ntoskrnl, win32k, drivers                    │  │
│  ├───────────────────────────────────────────────┤  │
│  │              User Mode (Ring 3)               │  │
│  │  ┌─────────────────────────────────────────┐  │  │
│  │  │  High Integrity (Admin)                 │  │  │
│  │  │  ┌───────────────────────────────────┐  │  │  │
│  │  │  │  Medium Integrity (Standard User) │  │  │  │
│  │  │  │  ┌─────────────────────────────┐  │  │  │  │
│  │  │  │  │  Low Integrity              │  │  │  │  │
│  │  │  │  │  ┌───────────────────────┐  │  │  │  │  │
│  │  │  │  │  │  AppContainer/LPAC   │  │  │  │  │  │
│  │  │  │  │  │  (Untrusted)         │  │  │  │  │  │
│  │  │  │  │  └───────────────────────┘  │  │  │  │  │
│  │  │  │  └─────────────────────────────┘  │  │  │  │
│  │  │  └───────────────────────────────────┘  │  │  │
│  │  └─────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

## Kernel/User Boundary

### Attack Surface
- System calls (ntoskrnl, win32k)
- IOCTLs to kernel drivers
- Shared memory sections
- GDI/DirectX objects

### Exploitation Vectors
```c
// win32k.sys — historically most exploited Windows kernel component
// Attack: trigger vulnerability via GDI/USER syscalls from user mode
// Common bug classes: UAF in window objects, integer overflow in font parsing

// Driver IOCTLs — third-party drivers often vulnerable
// Attack: send crafted IOCTL to driver device object
HANDLE hDevice = CreateFileA("\\\\.\\VulnDriver", GENERIC_READ|GENERIC_WRITE, 0, NULL, OPEN_EXISTING, 0, NULL);
DeviceIoControl(hDevice, IOCTL_CODE, inputBuf, inputSize, outputBuf, outputSize, &bytesReturned, NULL);

// BYOVD (Bring Your Own Vulnerable Driver)
// Load known-vulnerable signed driver, exploit it for kernel R/W
// Popular targets: RTCore64.sys, dbutil_2_3.sys, ene.sys, gdrv.sys
```

### Kernel Exploitation Primitives
```
1. Arbitrary Read → leak kernel addresses (bypass KASLR)
2. Arbitrary Write → overwrite token privileges, disable PPL
3. Common targets:
   - EPROCESS.Token → steal SYSTEM token
   - EPROCESS.Protection → disable PPL
   - PreviousMode → set to KernelMode for unrestricted syscalls
```

## Integrity Level Boundaries

### Levels
| Level | Value | Examples |
|-------|-------|----------|
| System | 0x4000 | SYSTEM services |
| High | 0x3000 | Elevated admin processes |
| Medium | 0x2000 | Standard user processes |
| Low | 0x1000 | Protected Mode IE, some sandboxes |
| Untrusted | 0x0000 | AppContainer processes |

### Crossing Boundaries
```powershell
# Check integrity level
whoami /groups | findstr "Mandatory"

# Medium → High: UAC bypass (see privesc-windows skill)
# Low → Medium: exploit vulnerability in medium-integrity process
# AppContainer → Low: sandbox escape
```

## AppContainer / LPAC Sandbox

### What's Restricted
- No access to user's files (except broker-mediated)
- No network access without explicit capability
- No registry access outside own hive
- No inter-process communication without broker
- LPAC (Less Privileged AppContainer): even more restricted — no access to named objects

### Escape Vectors
```
1. Broker vulnerabilities — the broker process mediates access
   - File picker broker (allows file access)
   - Print broker
   - Clipboard broker
   
2. Kernel vulnerabilities — AppContainer is userland enforcement
   - win32k syscalls still accessible (reduced but not eliminated)
   - Kernel bug = full escape
   
3. COM object abuse — some COM servers run at higher integrity
   - Find COM objects accessible from AppContainer
   - Exploit logic bugs in COM server
   
4. Named pipe/ALPC — if broker exposes pipe without proper ACL
   
5. Capability abuse — overly permissive capabilities granted
   - internetClient, privateNetworkClientServer
   - documentsLibrary, picturesLibrary
```

### Browser Sandbox Escape (Chromium/Edge)
```
Renderer (AppContainer/Untrusted) → Browser Process (Medium)
Attack surface:
- Mojo IPC interface bugs
- Shared memory corruption
- GPU process as intermediate target
- PDF/extension process boundaries

Typical chain:
1. Renderer RCE (V8 bug, type confusion)
2. Sandbox escape (Mojo IPC bug, win32k bug)
3. Privilege escalation (kernel bug or UAC bypass)
```

## COM/RPC Boundaries

### COM Elevation
```c
// COM objects that auto-elevate (no UAC prompt):
// CMSTPLUA: {3E5FC7F9-9A51-4367-9063-A120244FBEC7}
// ICMLuaUtil interface — can launch elevated processes

// Exploit: instantiate elevated COM object, call methods
CoInitialize(NULL);
IID iid_ICMLuaUtil = {0x6EDD6D74, 0xC007, 0x4E75, {0xB7, 0x6A, 0xE5, 0x74, 0x09, 0x95, 0xE2, 0x4C}};
CLSID clsid_CMSTPLUA = {0x3E5FC7F9, 0x9A51, 0x4367, {0x90, 0x63, 0xA1, 0x20, 0x24, 0x4F, 0xBE, 0xC7}};
// CoCreateInstance with CLSCTX_LOCAL_SERVER → runs elevated
```

### RPC Attack Surface
```bash
# Enumerate RPC interfaces
rpcdump.py target_ip
# Or: RpcView tool for local enumeration

# Common targets:
# - Print Spooler RPC (PrintNightmare)
# - Task Scheduler RPC
# - EFSRPC (PetitPotam)
# - MS-DRSR (DCSync)
```

## Hyper-V / VBS Boundary

### VTL0 → VTL1 (Secure World)
```
- VTL1 runs Secure Kernel, Credential Guard, HVCI
- VTL0 cannot read/write VTL1 memory
- Escape requires: Hyper-V vulnerability (extremely rare, high bounty)
- Attack surface: hypercalls, synthetic interrupts, VMBUS
```

### VM Escape (Guest → Host)
```
- Hyper-V attack surface: VMBus, synthetic devices, RemoteFX
- VMware: SVGA, HGFS, backdoor interface
- VirtualBox: 3D acceleration, shared folders, guest additions
- QEMU/KVM: virtio devices, SPICE, USB passthrough
```

## Practical Boundary Crossing Chains

### Browser → SYSTEM
```
1. V8 type confusion → renderer RCE (Untrusted integrity)
2. Mojo IPC bug → sandbox escape to browser process (Medium)
3. BYOVD or kernel bug → SYSTEM
```

### Office Macro → Domain Admin
```
1. VBA macro execution (Medium integrity)
2. AMSI bypass + download Stage 1
3. Credential harvesting or Kerberoast
4. Lateral movement → Domain Controller
5. DCSync → Domain Admin
```

### Phishing → Kernel
```
1. HTML smuggling → ISO → DLL sideload (Medium)
2. UAC bypass → High integrity
3. Load vulnerable driver (BYOVD)
4. Kernel R/W primitive → disable PPL, steal SYSTEM token
```

## Advanced: Browser Sandbox Escape

### Chromium Sandbox Architecture
```
// Chromium uses multi-process architecture:
// - Browser process: full privileges, manages tabs
// - Renderer process: sandboxed (AppContainer on Windows)
// - GPU process: limited sandbox
// - Network process: limited sandbox
//
// Sandbox restrictions (renderer):
// - No filesystem access (except via IPC to browser)
// - No network access (except via IPC)
// - No process creation
// - Limited Windows API access
// - AppContainer integrity level (below Low)

// Escape path: Renderer RCE → IPC bug → Browser process
// IPC mechanism: Mojo (Chromium's IPC framework)
// Attack surface: every Mojo interface exposed to renderer
```

### Mojo IPC Exploitation
```c
// Mojo interfaces define the renderer→browser attack surface
// Each interface = potential sandbox escape if mishandled

// Common vulnerability patterns:
// 1. Type confusion in Mojo message deserialization
// 2. UAF when interface pointer outlives backing object
// 3. Race condition between validation and use
// 4. Missing origin checks (renderer claims wrong origin)

// Exploitation:
// 1. Achieve renderer RCE (V8 type confusion, JIT bug)
// 2. Enumerate available Mojo interfaces
// 3. Fuzz or audit interface implementations in browser process
// 4. Trigger bug → code execution in browser process (Medium integrity)
// 5. From browser process: full system access or further escalation

// Historical examples:
// CVE-2019-5786: FileReader UAF → renderer RCE → Mojo escape
// CVE-2021-21224: V8 type confusion → Mojo IPC → sandbox escape
// CVE-2022-0609: Animation UAF → full chain
```

### Windows Sandbox Escape Techniques
```c
// AppContainer escape vectors:
// 1. Kernel vulnerability (win32k, ntoskrnl)
//    - AppContainer can still make syscalls
//    - win32k attack surface reduced but not eliminated
//    - Kernel bug → SYSTEM (bypasses all userland sandboxes)

// 2. Named object abuse
//    - Some named objects accessible from AppContainer
//    - If higher-privilege process opens object with weak DACL
//    - AppContainer can interact with it

// 3. ALPC/RPC to privileged services
//    - Some RPC endpoints accessible from AppContainer
//    - Vulnerability in RPC handler → escape
//    - Example: Print Spooler accessible from some sandboxes

// 4. Token manipulation
//    - If sandbox has SeImpersonatePrivilege (rare)
//    - Potato-style attacks work from sandbox
//    - Usually sandboxes strip this privilege

// 5. Shared memory / mapped sections
//    - If shared section has weak permissions
//    - Corrupt data used by higher-privilege process
//    - Example: shared font cache corruption → win32k exploit
```

## Advanced: PPL (Protected Process Light) Exploitation

### PPL Architecture
```c
// PPL levels (highest to lowest):
// - PPL-Windows: OS critical processes
// - PPL-WinTcb: Windows Trusted Computer Base
// - PPL-Antimalware: AV/EDR processes (MsMpEng.exe, CrowdStrike)
// - PPL-Lsa: LSASS (when RunAsPPL enabled)
// - PP-Authenticode: signed processes
//
// PPL prevents:
// - OpenProcess with PROCESS_VM_READ/WRITE
// - Debugging (DebugActiveProcess)
// - Thread injection (CreateRemoteThread)
// - Memory reading (ReadProcessMemory)
// - DLL injection
//
// Even SYSTEM cannot open PPL process with full access
```

### PPL Bypass Techniques
```c
// 1. BYOVD → kernel R/W → modify EPROCESS.Protection field
//    Set Protection.Level = 0 → process is no longer protected
//    Then: normal OpenProcess/ReadProcessMemory works
BYTE protection_offset = 0x87A;  // Offset varies by Windows version
WriteKernelMemory(eprocess + protection_offset, 0, 1);  // Clear protection

// 2. PPLdump (abuse PPL-signed DLL)
//    Load DLL signed with PPL-compatible certificate
//    DLL runs inside PPL process → can read its memory
//    Dump LSASS from within PPL context

// 3. PPLKiller (vulnerable driver)
//    Use signed driver with R/W primitive
//    Modify EPROCESS.SignatureLevel and Protection
//    Process becomes unprotected → dump normally

// 4. Mimikatz driver (mimidrv.sys)
//    Mimikatz's own signed driver
//    Removes PPL protection from LSASS
//    Then: sekurlsa::logonpasswords works

// 5. Userland exploit in PPL process
//    If PPL process has vulnerability (e.g., DLL hijack)
//    Exploit it → code execution within PPL context
//    From inside: full access to PPL memory
```

## Advanced: COM/RPC Boundary Attacks

### COM Activation Attacks
```c
// COM objects can be activated cross-process and cross-integrity
// If COM server runs at higher integrity → potential escalation

// Attack: find COM object that:
// 1. Runs as SYSTEM or high integrity
// 2. Exposes dangerous methods (file write, command exec)
// 3. Accessible from medium/low integrity

// Discovery:
// OleViewDotNet — enumerate COM objects, check permissions
// Look for: LaunchPermission allows Everyone/Users
// Check: methods that take file paths or command strings

// Historical: CMSTPLUA, ICMLuaUtil (UAC bypass via COM)
// These COM objects auto-elevate and expose ShellExec methods
```

### RPC Interface Exploitation
```c
// Windows RPC: thousands of interfaces, many accessible remotely
// Each interface = potential attack surface

// Enumeration:
// rpcdump.py — list RPC interfaces on target
// RpcView — GUI tool for local RPC interface analysis
// NtObjectManager — PowerShell module for RPC analysis

// Attack methodology:
// 1. Enumerate interfaces (rpcdump, ifids)
// 2. Identify interesting interfaces (file ops, process creation)
// 3. Check access permissions (who can call?)
// 4. Fuzz interface methods
// 5. Exploit: type confusion, buffer overflow, logic bugs

// PetitPotam (MS-EFSRPC): RPC interface that coerces NTLM auth
// PrinterBug (MS-RPRN): RPC interface that coerces NTLM auth
// Both: accessible remotely with domain user credentials
```

## Advanced: Integrity Level Escalation

### Medium → High (UAC Bypass Catalog)
```powershell
# Auto-elevating binaries (Microsoft-signed, manifest has autoElevate=true):
# fodhelper.exe, computerdefaults.exe, sdclt.exe, slui.exe
# eventvwr.exe, cmstp.exe, wsreset.exe, changepk.exe

# Technique: registry key hijacking
# These binaries read HKCU registry before executing
# Attacker writes command to HKCU → binary auto-elevates → executes attacker command

# Example: fodhelper.exe
# Reads: HKCU\Software\Classes\ms-settings\Shell\Open\command
# Write payload there → run fodhelper → payload runs elevated

# Environment variable abuse:
# Some auto-elevate binaries use %SYSTEMROOT% or %WINDIR%
# If attacker can control env var → DLL hijack in fake system directory
```

### Low → Medium
```c
// Low integrity → Medium integrity is a security boundary
// Escape vectors:
// 1. Exploit vulnerability in medium-integrity process
// 2. Abuse shared resources (clipboard, drag-drop)
// 3. Exploit broker process (if application uses broker pattern)
// 4. Kernel vulnerability (bypasses all integrity levels)
// 5. Time-of-check-time-of-use on shared files
```
