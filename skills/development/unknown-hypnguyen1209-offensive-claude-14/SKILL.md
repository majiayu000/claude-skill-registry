---
name: windows-boundaries
description: Windows security boundary attacks — kernel/user boundary, sandbox escape, AppContainer/LPAC bypass, COM/RPC boundary, integrity levels, PPL exploitation
metadata:
  type: offensive
  phase: exploitation
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
