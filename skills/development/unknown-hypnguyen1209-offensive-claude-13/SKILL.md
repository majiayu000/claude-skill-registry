---
name: malware-analysis
description: Static/dynamic malware analysis, YARA rules, sandbox evasion detection, behavioral profiling, unpacking, anti-analysis bypass
metadata:
  type: defensive
  phase: analysis
  tools: ida, ghidra, x64dbg, procmon, wireshark, yara, capa, pestudio, floss, cuckoo, any.run
---

# Malware Analysis

## When to Activate

- Analyzing suspicious binaries or scripts
- Writing detection signatures (YARA, Snort, Sigma)
- Understanding malware capabilities and C2 protocols
- Unpacking protected/obfuscated samples
- Incident response — determining scope of compromise
- Threat intelligence — attributing samples to threat actors

## Static Analysis

### Initial Triage
```bash
# File identification
file sample.exe
sha256sum sample.exe
ssdeep sample.exe  # fuzzy hash for similarity

# PE analysis
pestudio sample.exe  # GUI: imports, strings, indicators
python3 -c "import pefile; pe=pefile.PE('sample.exe'); print(pe.dump_info())"

# Strings
floss sample.exe  # FLARE Obfuscated String Solver (decodes obfuscated strings)
strings -n 8 sample.exe | grep -iE '(http|ftp|cmd|powershell|reg|schtask|wmic)'

# Capability detection
capa sample.exe  # maps to MITRE ATT&CK techniques
# Output: persistence/registry, defense-evasion/process-injection, etc.

# Import analysis
python3 -c "
import pefile
pe = pefile.PE('sample.exe')
for entry in pe.DIRECTORY_ENTRY_IMPORT:
    print(entry.dll.decode())
    for imp in entry.imports:
        print(f'  {imp.name.decode() if imp.name else hex(imp.ordinal)}')
"
```

### Suspicious Indicators
```
# High-confidence malicious:
- VirtualAlloc + WriteProcessMemory + CreateRemoteThread (process injection)
- NtUnmapViewOfSection + NtMapViewOfSection (process hollowing)
- SetWindowsHookEx (keylogger/hooking)
- CryptEncrypt with hardcoded key (ransomware)
- InternetOpen + InternetConnect + HttpSendRequest (C2 communication)
- RegSetValueEx on Run keys (persistence)
- CreateToolhelp32Snapshot + Process32First (process enumeration)

# Packing indicators:
- High entropy sections (>7.0)
- Few imports (only LoadLibrary/GetProcAddress)
- Section names: UPX, .packed, .vmp, .themida
- Entry point in non-standard section
```

## Dynamic Analysis

### Sandbox Setup
```bash
# Isolated VM with:
# - Snapshot before execution
# - Network capture (inetsim for fake services)
# - Process monitoring (procmon, API Monitor)
# - File system monitoring (sysmon)
# - Registry monitoring

# Inetsim (fake internet services)
inetsim --config /etc/inetsim/inetsim.conf

# FakeDNS
python3 fakedns.py -c 192.168.1.100  # redirect all DNS to analysis host
```

### Behavioral Analysis
```bash
# Process Monitor filters:
# - Process Name contains sample.exe
# - Operation is WriteFile, RegSetValue, Process Create
# - Path contains \Run, \Services, \Tasks

# Network capture
tcpdump -i eth0 -w capture.pcap
# Analyze: DNS queries, HTTP requests, raw TCP connections

# API tracing
# x64dbg: set breakpoints on key APIs
# API Monitor: filter by category (Registry, File, Network, Process)
```

### Anti-Analysis Detection
```
# Common evasion techniques to identify:
- Sleep calls (extended delays to timeout sandboxes)
- Environment checks (VM artifacts, debugger presence, sandbox usernames)
- Timing attacks (rdtsc differences)
- Mouse movement/click checks
- Domain-joined check
- Minimum RAM/CPU/disk checks
- Specific file/registry checks (sandbox artifacts)
- Network connectivity checks before detonation
```

## YARA Rule Writing

```yara
rule APT_Backdoor_CustomRAT {
    meta:
        author = "analyst"
        description = "Custom RAT used by threat actor"
        date = "2026-05-19"
        hash = "abc123..."
        
    strings:
        $magic = { 4D 5A 90 00 }  // MZ header
        $str1 = "cmd.exe /c" ascii wide
        $str2 = "/api/beacon" ascii
        $mutex = "Global\\CustomMutex" ascii
        $key = { 41 42 43 44 45 46 47 48 }  // XOR key
        
        // API hashing pattern
        $api_hash = { 68 ?? ?? ?? ?? E8 ?? ?? ?? ?? }  // push hash; call resolve
        
    condition:
        $magic at 0 and
        (2 of ($str*)) and
        ($api_hash or $key) and
        filesize < 500KB
}

// Rule quality checklist:
// - Specific enough to avoid FP (test against goodware corpus)
// - Targets unique/stable features (not easily modified strings)
// - Includes metadata for context
// - Performance: avoid expensive regex, prefer hex patterns
// - Test with: yara -r rule.yar /path/to/samples/
```

## Unpacking

### Common Packers
```
# UPX
upx -d packed.exe -o unpacked.exe

# Custom packers — manual unpacking:
# 1. Set breakpoint on VirtualAlloc/VirtualProtect
# 2. Run until unpacking stub allocates RWX memory
# 3. Set hardware breakpoint on allocated region
# 4. Continue until code is written and executed
# 5. At OEP: dump process memory
# 6. Fix IAT with Scylla/ImportREC

# .NET obfuscation (ConfuserEx, .NET Reactor)
de4dot sample.exe -o cleaned.exe
# Then: dnSpy for decompilation

# JavaScript/PowerShell deobfuscation
# Replace eval/IEX with console.log/Write-Output
# Iteratively decode layers
```

## C2 Protocol Analysis

```
# Identify C2 communication:
# 1. Capture network traffic during execution
# 2. Identify beaconing patterns (regular intervals)
# 3. Decode protocol:
#    - HTTP: check User-Agent, URI patterns, POST data encoding
#    - DNS: subdomain encoding (hex, base32, base64)
#    - Custom TCP: identify magic bytes, encryption, structure

# Common C2 frameworks signatures:
# Cobalt Strike: /submit.php, cookie with base64 metadata, 60s default sleep
# Metasploit: stage URI pattern /[A-Za-z0-9]{4}
# Sliver: mTLS, HTTP with specific headers
# Havoc: custom protocol over HTTP/S
```

## Reporting Template

```markdown
## Sample: [hash]
### Classification: [family/type]
### Capabilities:
- [ ] Persistence mechanism
- [ ] C2 communication
- [ ] Data exfiltration
- [ ] Lateral movement
- [ ] Credential theft
- [ ] Encryption/ransomware
### IOCs:
- Hashes: [MD5, SHA256, imphash, ssdeep]
- Network: [domains, IPs, URLs, User-Agents]
- Host: [mutexes, files created, registry keys]
- YARA: [rule name]
### MITRE ATT&CK Mapping:
- T1055 - Process Injection
- T1547.001 - Registry Run Keys
- [...]
```
