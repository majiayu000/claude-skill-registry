---
name: threat-hunting
description: Proactive threat hunting, IOC extraction, MITRE ATT&CK mapping, behavioral anomaly detection, log analysis correlation
metadata:
  type: defensive
  phase: detection
  tools: splunk, elasticsearch, sigma, yara, osquery, velociraptor, sysmon
kill_chain:
  phase: [report]
  step: [8]
  attck_tactics: [TA0043]
depends_on: [red-team-ops, incident-response]
feeds_into: []
inputs: [finding_records, log_data, ioc_list]
outputs: [sigma_rules, attck_navigator_export, detection_report]
---

# Threat Hunting & Detection

## When to Activate

- Proactive threat hunting across infrastructure
- Correlating security events across multiple sources
- Detecting anomalous behavior patterns
- Mapping attacks to MITRE ATT&CK framework
- Writing detection rules (Sigma, YARA, Snort)
- Incident response triage

## MITRE ATT&CK Mapping

### Common Techniques to Hunt

| Tactic | Technique | Detection Focus |
|--------|-----------|----------------|
| Initial Access | Phishing, Exploit Public-Facing App | Email gateways, web WAF logs |
| Execution | PowerShell, WMI, Scheduled Tasks | PS logs, Sysmon Event ID 1 |
| Persistence | Registry Run Keys, Scheduled Tasks | Registry monitoring, task scheduler logs |
| Privilege Escalation | Token Manipulation, Exploitation | Access token changes, exploit indicators |
| Defense Evasion | Obfuscated Files, Indicator Removal | File entropy analysis, log gap detection |
| Credential Access | LSASS Memory, OS Credential Dumping | LSASS access patterns, dump file creation |
| Discovery | Network Share Discovery, System Info Discovery | Net commands, systeminfo execution |
| Lateral Movement | SMB/Windows Admin Shares, WMI | SMB connection patterns, remote WMI calls |
| Collection | Data Staged, Archive Collected Data | Unusual archive operations, staging directories |
| Exfiltration | Exfiltration Over C2, DNS | DNS query volume anomalies, C2 beacon patterns |

## Log Analysis & Correlation

### Key Event Sources
```
# Windows (Sysmon)
Event ID 1: Process creation
Event ID 3: Network connection
Event ID 7: Image loaded
Event ID 11: File creation
Event ID 12: Registry object added/modified
Event ID 13: Registry value set
Event ID 15: File creation stream hash
Event ID 17: Pipe created
Event ID 22: DNS query
Event ID 25: Process tampering

# Linux (auditd)
type=EXECVE: Command execution
type=CONNECT: Network connections
type=PATH: File access
type=SYSCALL: System calls (esp. ptrace, execve)

# Network (Zeek/Suricata)
DNS queries and responses
HTTP requests and responses
SSL/TLS certificate analysis
File extraction and hashing
```

### Correlation Queries
```sql
-- Splunk: PowerShell encoded command
index=security EventCode=4688 
| where match(Process_Command_Line, "powershell.*-enc") 
| stats count by Computer, User, _time
| where count > 3

-- Splunk: Lateral movement via PsExec
index=security EventCode=7045 Service_Name="PSEXESVC"
| stats count by Computer, User
| where count > 1

-- Sigma equivalent
detection:
    selection:
        EventID: 4688
        CommandLine|contains|all:
            - 'powershell'
            - '-enc'
            - '-encodedcommand'
    condition: selection
```

## Behavioral Anomaly Detection

### Baselines
```
# Normal user behavior:
- Login times and duration
- Common processes and commands
- Network destinations and volumes
- File access patterns

# Anomaly indicators:
- Processes running at unusual hours
- New network destinations (never before seen)
- Sudden increase in data access volume
- Commands that deviate from user's normal pattern
- Service installations on workstations
```

### Hunting Hypotheses
```
# Generate and test hunting hypotheses:
1. "If there's credential dumping, we'll see Mimikatz or similar tool execution"
2. "If lateral movement occurs, we'll see new admin share connections"
3. "If data exfiltration happens, we'll see unusual outbound DNS or HTTPS traffic"
4. "If there's persistence, we'll see new scheduled tasks or registry modifications"

# Validate with:
- Historical log analysis (last 30-90 days)
- Endpoint telemetry (processes, network, files)
- Network flow data (NetFlow, PCAP)
- Cloud audit logs (CloudTrail, Azure Activity Log)
```

## Detection Rule Development

### Sigma Rule Template
```yaml
title: Suspicious PowerShell Execution
id: rule-uuid-here
status: experimental
description: Detects PowerShell execution with encoded commands and download cradles
references:
    - https://attack.mitre.org/techniques/T1059/001/
author: analyst
date: 2026/05/19
logsource:
    category: process_creation
    product: windows
detection:
    selection:
        Image|endswith: '\powershell.exe'
    encoded:
        CommandLine|contains:
            - '-enc'
            - '-encodedcommand'
    download:
        CommandLine|contains:
            - 'DownloadString'
            - 'DownloadFile'
            - 'IEX'
            - 'Invoke-Expression'
    condition: selection and (encoded or download)
falsepositives:
    - Legitimate IT automation scripts
    - Software deployment tools
level: high
tags:
    - attack.execution
    - attack.t1059.001
```

### YARA Network Detection
```yara
rule C2_Beacon_Pattern {
    meta:
        description = "Detects C2 beacon traffic patterns"
    strings:
        $beacon_http = /POST \/gate\.php HTTP\/1\.1\r\nHost: [^\r\n]+\r\nUser-Agent: Mozilla\/[\d.]+/
        $beacon_dns = /[a-z0-9]{32,}\.attacker-domain\.(com|net|org)/
    condition:
        $beacon_http or $beacon_dns
}
```

## Advanced: KQL/SPL Hunting Queries

### Splunk (SPL) Advanced Queries
```spl
| Detect credential dumping (LSASS access)
index=sysmon EventCode=10 TargetImage="*lsass.exe"
| where NOT match(SourceImage, "(?i)(csrss|services|svchost|wininit|MsMpEng|CrowdStrike)")
| stats count values(SourceImage) as tools by Computer
| where count > 0

| Detect DCSync (Directory Replication)
index=security EventCode=4662 
| where match(Properties, "(?i)(1131f6aa|1131f6ad|89e95b76)")
| where NOT match(SubjectUserName, "(?i)(\\$|MSOL_)")
| stats count by SubjectUserName, ObjectName

| Detect Kerberoasting
index=security EventCode=4769 TicketEncryptionType=0x17 ServiceName!="krbtgt" ServiceName!="*$"
| stats count dc(ServiceName) as unique_spns by IpAddress, TargetUserName
| where unique_spns > 3

| Detect lateral movement (remote service creation)
index=security EventCode=7045
| where NOT match(Service_File_Name, "(?i)(windows|program files|syswow64)")
| stats count values(Service_File_Name) as services by Computer, SubjectUserName

| Detect pass-the-hash (NTLM type 3 with no type 1/2)
index=security EventCode=4624 LogonType=3 AuthenticationPackageName=NTLM
| where LmPackageName="NTLM V2" AND TargetUserName!="ANONYMOUS LOGON"
| stats count by SourceNetworkAddress, TargetUserName, WorkstationName
| where count > 5

| Detect process injection (Sysmon CreateRemoteThread)
index=sysmon EventCode=8
| where SourceImage!=TargetImage
| where NOT match(SourceImage, "(?i)(csrss|lsass|services|svchost)")
| stats count values(TargetImage) as targets by SourceImage, Computer
```

### KQL (Microsoft Sentinel / Defender)
```kql
// Detect encoded PowerShell execution
DeviceProcessEvents
| where FileName =~ "powershell.exe"
| where ProcessCommandLine has_any ("-enc", "-encodedcommand", "frombase64")
| where ProcessCommandLine !has "Microsoft" // exclude legit
| project Timestamp, DeviceName, AccountName, ProcessCommandLine
| summarize count() by DeviceName, AccountName, bin(Timestamp, 1h)
| where count_ > 3

// Detect LSASS credential access
DeviceProcessEvents
| where FileName =~ "lsass.exe"
| join kind=inner (
    DeviceFileEvents | where ActionType == "FileCreated" | where FileName endswith ".dmp"
) on DeviceId
| project Timestamp, DeviceName, InitiatingProcessFileName

// Detect suspicious named pipe creation (C2 indicators)
DeviceEvents
| where ActionType == "NamedPipeEvent"
| where AdditionalFields has_any ("\\msagent_", "\\MSSE-", "\\postex_", "\\status_")
| summarize count() by DeviceName, PipeName=tostring(parse_json(AdditionalFields).PipeName)

// Detect Kerberos ticket anomalies (Golden/Silver ticket)
IdentityQueryEvents
| where ActionType == "LDAP query"
| where QueryTarget has "krbtgt"
| join kind=inner (
    IdentityLogonEvents | where LogonType == "Kerberos"
    | where isempty(AccountDomain) or AccountDomain != DeviceName
) on AccountName
| project Timestamp, AccountName, DeviceName, QueryTarget

// Hunt for living-off-the-land binaries (LOLBins)
let lolbins = dynamic(["certutil.exe","mshta.exe","regsvr32.exe","rundll32.exe",
    "msiexec.exe","wmic.exe","cmstp.exe","msxsl.exe","ieexec.exe"]);
DeviceProcessEvents
| where FileName in~ (lolbins)
| where ProcessCommandLine has_any ("http","ftp","\\\\","base64","-decode","/i:")
| project Timestamp, DeviceName, FileName, ProcessCommandLine, AccountName
```

## Advanced: Behavioral Detection Patterns

### Process Behavior Profiling
```yaml
# Detect anomalous process behavior via baseline deviation

# Baseline: normal parent-child relationships
normal_trees:
  - explorer.exe → chrome.exe, outlook.exe, teams.exe
  - services.exe → svchost.exe, spoolsv.exe
  - svchost.exe → WerFault.exe, RuntimeBroker.exe
  - winlogon.exe → userinit.exe → explorer.exe

# Anomalous (hunt for these):
suspicious_trees:
  - winword.exe → cmd.exe → powershell.exe  # macro execution
  - outlook.exe → powershell.exe  # phishing payload
  - svchost.exe → cmd.exe → whoami.exe  # post-exploitation
  - w3wp.exe → cmd.exe  # webshell
  - sqlservr.exe → cmd.exe → certutil.exe  # SQL injection → download
  - wmiprvse.exe → powershell.exe  # WMI lateral movement

# Process creation frequency anomaly:
# If process X normally runs 0-2 times/day but suddenly runs 50 times → investigate
# Especially: net.exe, nltest.exe, dsquery.exe, csvde.exe (AD recon)
```

### Network Behavior Anomalies
```yaml
# DNS-based detection
dns_anomalies:
  - query_length > 50 chars  # DNS tunneling (iodine, dnscat2)
  - TXT record queries to unusual domains  # C2 over DNS
  - high volume queries to single domain  # beaconing
  - queries to newly registered domains (< 30 days)  # DGA or fresh C2
  - NXDOMAIN spike from single host  # DGA enumeration

# Beaconing detection (C2 callback patterns)
beaconing_indicators:
  - Regular interval connections (±jitter) to same destination
  - Consistent payload sizes in both directions
  - Connections to IP addresses (no DNS resolution)
  - TLS connections with self-signed or unusual certificates
  - JA3/JA4 hash matching known C2 frameworks

# Detection formula:
# Calculate inter-arrival times between connections to same dest
# If standard_deviation / mean < 0.3 → likely beaconing
# Human traffic: irregular, bursty
# C2 traffic: regular, consistent
```

### Sigma Rules for Advanced Threats
```yaml
title: Potential DCSync Attack
id: 5a6c7e3b-8d4f-4a2e-9c1b-7f3e8d2a1b4c
status: stable
description: Detects replication requests from non-DC sources
logsource:
    product: windows
    service: security
detection:
    selection:
        EventID: 4662
        Properties|contains:
            - '1131f6aa-9c07-11d1-f79f-00c04fc2dcd2'  # DS-Replication-Get-Changes
            - '1131f6ad-9c07-11d1-f79f-00c04fc2dcd2'  # DS-Replication-Get-Changes-All
    filter:
        SubjectUserName|endswith: '$'
        SubjectUserName|contains: 'DC'
    condition: selection and not filter
level: critical
tags:
    - attack.credential_access
    - attack.t1003.006
---
title: Suspicious LSASS Access (Credential Dumping)
id: 7b2e4f1a-9c3d-4e5f-8a6b-1c2d3e4f5a6b
logsource:
    product: windows
    category: process_access
detection:
    selection:
        TargetImage|endswith: '\lsass.exe'
        GrantedAccess|contains:
            - '0x1010'   # PROCESS_QUERY_LIMITED_INFORMATION + PROCESS_VM_READ
            - '0x1410'   # + PROCESS_QUERY_INFORMATION
            - '0x1438'   # Full access for dump
            - '0x143a'
    filter_system:
        SourceImage|startswith:
            - 'C:\Windows\System32\'
            - 'C:\Program Files\Windows Defender\'
    condition: selection and not filter_system
level: high
---
title: Cobalt Strike Named Pipe Pattern
id: 3e8f2a1b-4c5d-6e7f-8a9b-0c1d2e3f4a5b
logsource:
    product: windows
    category: pipe_created
detection:
    selection:
        PipeName|re: '\\\\(MSSE-|msagent_|postex_|status_|mojo\.\d+\.\d+\.\d+)'
    condition: selection
level: critical
```

## Advanced: Purple Team Exercises

### Atomic Red Team Integration
```bash
# Execute specific ATT&CK techniques and validate detection

# T1003.001 — LSASS Memory Dump
Invoke-AtomicTest T1003.001 -TestNumbers 1,2,3
# Validate: Sysmon Event 10 (ProcessAccess to lsass) fires
# Validate: EDR alert generated within 60 seconds

# T1059.001 — PowerShell Execution
Invoke-AtomicTest T1059.001 -TestNumbers 1
# Validate: PowerShell ScriptBlock logging captures payload
# Validate: Sigma rule "Suspicious PowerShell Execution" triggers

# T1053.005 — Scheduled Task Persistence
Invoke-AtomicTest T1053.005 -TestNumbers 1
# Validate: Event ID 4698 (task created) logged
# Validate: Task with suspicious binary path flagged

# Detection gap analysis:
# Run all techniques → check which have NO detection
# Priority: techniques with no detection + high impact = critical gap
```

### Detection Coverage Matrix
```
| ATT&CK Technique | Sysmon | EDR | SIEM Rule | Network | Gap? |
|-------------------|--------|-----|-----------|---------|------|
| T1003.001 LSASS  | Event10| Yes | Sigma     | N/A     | No   |
| T1059.001 PS     | Event1 | Yes | SPL query | N/A     | No   |
| T1021.002 SMB    | Event3 | Yes | Sigma     | Zeek    | No   |
| T1071.001 HTTP C2| N/A    | Partial| N/A    | JA3     | Yes  |
| T1055.012 Hollow | Event25| Yes | N/A       | N/A     | Partial|
| T1134.001 Token  | N/A    | Partial| N/A    | N/A     | Yes  |
```
