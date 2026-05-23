---
name: vermillion-hunter
description: 'Overview'
version: 1.0.0
---


## Overview

Frida-based dynamic instrumentation for identifying Windows "features" exploitable for:
- **DLL Sideloading** (T1574.002)
- **COM Hijacking** (T1546.015)

WFH Dridex variant: ~966 validated sideloads vs 96 from original.

---

## MITRE ATT&CK Mapping

### T1574.002 - DLL Side-Loading

| Tactic | ID | Description |
|--------|-----|-------------|
| Persistence | TA0003 | Maintain access via trusted process |
| Privilege Escalation | TA0004 | Inherit elevated token |
| Defense Evasion | TA0005 | Execute under signed binary |

**Hooked APIs:**
```
LoadLibraryW(LPCWSTR lpLibFileName)
LoadLibraryExW(LPCWSTR lpLibFileName, HANDLE hFile, DWORD dwFlags)
GetProcAddress(HMODULE hModule, LPCSTR lpProcName)
```

**Attack Chain:**
```
1. Identify signed exe with weak DLL reference
2. Copy exe to attacker-controlled directory
3. Place malicious DLL with expected name
4. Execute → DLL loads in trusted context
```

### T1546.015 - COM Hijacking

| Tactic | ID | Description |
|--------|-----|-------------|
| Persistence | TA0003 | Survive reboots via registry |
| Privilege Escalation | TA0004 | Hijack elevated COM server |

**Hooked APIs:**
```
RegQueryValueExW → CLSID\{GUID}\InProcServer32
```

**Attack Chain:**
```
1. Monitor COM object instantiation
2. Create HKCU shadow of HKLM CLSID entry
3. Point InProcServer32 to malicious DLL
4. Application loads attacker DLL on COM call
```

---

## Usage Patterns

### DLL Sideloading Detection
```bash
# Single target
python wfh.py -t .\mspaint.exe -m dll

# Batch (copy exes to WFH dir first)
python wfh.py -t * -m dll

# Verbose with timeout
python wfh.py -t * -m dll -v -timeout 30
```

### COM Hijacking Detection
```bash
python wfh.py -t "C:\Program Files\Internet Explorer\iexplore.exe" -m com -v
```

### WFH Dridex (Enhanced)
```bash
# Requires MinGW G++ in PATH
python wfh_dridex.py
# Outputs: results.csv with validated sideloads
```

### Bulk Windows Binary Scan
```powershell
# Copy all signed Windows binaries
Get-ChildItem c:\ -File | ForEach-Object {
    if($_ -match '.+?exe$') {Get-AuthenticodeSignature $_.fullname}
} | Where {$_.IsOSBinary} | ForEach-Object {Copy-Item $_.path .}

# Hunt
python wfh.py -t * -m dll
python wfh.py -t * -m com
```

---

## High-Value Targets

| Executable | Sideloadable DLLs |
|------------|-------------------|
| mspaint.exe | gdiplus.dll, MSFTEDIT.DLL, PROPSYS.dll, WINMM.dll, MFC42u.dll |
| charmap.exe | MSFTEDIT.DLL, GetUName.dll |
| iexplore.exe | ie_to_edge_bho_64.dll, Windows.Storage.dll |

Full System32 results: [WFH_Dridex_System32_08172022.csv](https://github.com/ConsciousHacker/WFH/blob/main/examples/WFH_Dridex_System32_08172022.csv)

---

## Defensive Countermeasures

### Detection Tools

| Tool | Purpose |
|------|---------|
| [SideLoadHunter](https://github.com/XForceIR/SideLoadHunter) | Sysmon + PowerShell profiling |
| [HijackLibs](https://hijacklibs.net/) | Known sideload database (507 WFH contributions) |

### Sysmon Detection Rules

```xml
<!-- DLL Sideloading: Signed exe from non-standard path -->
<RuleGroup name="DLL Sideload" groupRelation="and">
  <ImageLoad onmatch="include">
    <ImageLoaded condition="contains">\Users\</ImageLoaded>
    <Signed condition="is">true</Signed>
  </ImageLoad>
</RuleGroup>

<!-- COM Hijack: HKCU InProcServer32 modification -->
<RuleGroup name="COM Hijack" groupRelation="or">
  <RegistryEvent onmatch="include">
    <TargetObject condition="contains">CLSID</TargetObject>
    <TargetObject condition="contains">InProcServer32</TargetObject>
  </RegistryEvent>
</RuleGroup>
```

### Detection Signals

| Signal | Indicator |
|--------|-----------|
| Path Anomaly | Signed exe running from %TEMP%, Downloads, user dirs |
| DLL Location | Non-System32 DLL loaded by Windows binary |
| Registry Shadow | HKCU COM registration duplicating HKLM entry |
| Manifest Weakness | LoadLibrary with filename-only (no full path) |

---

## GF(3) Integration

```
Skill Trit: MINUS (-1) = Validator/Constrainer
Color Hue: Vermillion (0-60° warm, warning spectrum)
Conservation: Pairs with PLUS skill for balanced execution
```

**Triad Assignment:**
- MINUS: vermillion-hunter (detect vulnerabilities)
- ERGODIC: defense-synthesis (correlate findings)
- PLUS: exploit-executor (validate exploitability)

---

## Dependencies

```
pip install frida frida-tools
# For WFH Dridex:
# MinGW G++ 64-bit with g++.exe in PATH
```

---

## References

- [IBM X-Force Blog: DLL Sideloading with Frida](https://securityintelligence.com/x-force/windows-features-dll-sideloading/)
- [MITRE T1574.002](https://attack.mitre.org/techniques/T1574/002/)
- [MITRE T1546.015](https://attack.mitre.org/techniques/T1546/015/)
- [Dridex Loader Analysis](https://blog.lexfo.fr/dridex-malware.html)
- [WWHF 2022 Presentation](https://github.com/ConsciousHacker/WFH/blob/main/Hunting_For_Windows_Features_And_How_To_Use_Them_WWHF_2022.pdf)
