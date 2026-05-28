---
name: threat-hunting
description: Proactive threat hunting, IOC extraction, MITRE ATT&CK mapping, behavioral anomaly detection, log analysis correlation
metadata:
  type: defensive
  phase: detection
  tools: splunk, elasticsearch, sigma, yara, osquery, velociraptor, sysmon
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
