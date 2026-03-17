---
name: detection-engineer
description: Create detection rules and hunting queries from malware analysis findings. Use when you need to write Sigma rules for SIEM, Suricata rules for network IDS, defang IOCs for safe sharing, or convert analysis findings into actionable detection content for SOC teams and threat hunters.
---

# Detection Engineer

Transform malware analysis findings into production-ready detection rules, hunting queries, and operationalized IOCs.

## When to Use This Skill

Use this skill when you need to:
- Create YARA rules from malware samples (already covered in malware-report-writer)
- Write **Sigma rules** for SIEM detection (Splunk, Elastic, QRadar)
- Create **Suricata/Snort rules** for network IDS/IPS
- Generate **hunting queries** for EDR platforms
- **Defang IOCs** for safe documentation and sharing
- Convert IOCs to **standard formats** (STIX, OpenIOC, CSV)
- Assess **IOC confidence levels** and volatility
- Create **detection logic** from behavioral analysis
- Write **threat hunting hypotheses**

## IOC Management & Defanging

### Why Defang IOCs?

**Problem:** Live IOCs in reports can be:
- Accidentally clicked (execute malware)
- Automatically crawled by bots
- Trigger security tools (email filters, DLP)

**Solution:** Defang (neutralize) IOCs for safe sharing.

### Defanging Patterns

```bash
# URLs
http://malicious.com/payload.exe
→ hxxp://malicious[.]com/payload[.]exe

https://evil.tk/login
→ hxxps://evil[.]tk/login

# Domains
malicious.com
→ malicious[.]com

c2-server.example.org
→ c2-server[.]example[.]org

# IPs
192.168.1.100
→ 192[.]168[.]1[.]100

10.0.0.50
→ 10[.]0[.]0[.]50

# Email addresses
attacker@evil.com
→ attacker[@]evil[.]com

phishing@malware.tk
→ phishing[@]malware[.]tk

# File paths (optional)
C:\Windows\System32\malware.exe
→ C:\Windows\System32\malware[.]exe
```

### Automated Defanging

**Tool: ioc-fanger (Python)**
```bash
# Install
pip install ioc-fanger

# Defang
echo "http://malicious.com" | fanger --defang
# Output: hxxp://malicious[.]com

# Refang (restore for testing)
echo "hxxp://malicious[.]com" | fanger --fang
# Output: http://malicious.com
```

**Manual sed/awk:**
```bash
# Defang URLs and domains
echo "http://malicious.com/payload.exe" | sed 's/http:/hxxp:/g; s/\./[.]/g'

# Defang IPs
echo "192.168.1.100" | sed 's/\./[.]/g'

# Defang emails
echo "attacker@evil.com" | sed 's/@/[@]/g; s/\./[.]/g'
```

### IOC Confidence & Volatility Assessment

| IOC Type | Confidence | Volatility | Reasoning |
|----------|------------|------------|-----------|
| **File Hash (SHA256)** | High | Static | Unique to sample, won't change |
| **Mutex Name** | High | Static | Hardcoded in malware |
| **PDB Path** | High | Static | Compilation artifact |
| **Registry Key** | High | Static | Persistence mechanism |
| **Certificate Hash** | High | Static | Code signing certificate |
| **IP Address** | Medium | Dynamic | Can change (DGA, fast-flux, hosting) |
| **Domain (C2)** | Medium | Dynamic | May rotate frequently |
| **URL Path** | Low-Medium | Dynamic | Often dynamic or timestamped |
| **User-Agent** | Low | Dynamic | Common strings, high FP rate |
| **File Path** | Medium | Static | May vary by environment |
| **Process Name** | Low | Dynamic | Easily changed by attacker |

**Label IOCs appropriately:**
```markdown
### Network Indicators (Medium Confidence - Dynamic)
- Domain: malicious[.]com (C2 server - may rotate)
- IP: 192[.]168[.]1[.]100 (C2 IP - may change)

### Host Indicators (High Confidence - Static)
- Mutex: Global\UniqueMalwareMutex
- Registry: HKCU\Software\Microsoft\Windows\CurrentVersion\Run\Malware
- File Hash: abc123... (SHA256)
```

---

## Sigma Rule Creation (SIEM Detection)

### What is Sigma?

Sigma is a **generic signature format for SIEM systems**. Write once, convert to Splunk/Elastic/QRadar/ArcSight queries.

**Official Repo:** https://github.com/SigmaHQ/sigma

### Sigma Rule Structure

```yaml
title: Short Descriptive Title
id: unique-uuid-for-this-rule
status: experimental | test | stable
description: Detailed description of what this detects
references:
    - https://attack.mitre.org/techniques/T1059/001/
author: Your Name
date: 2025-10-26
tags:
    - attack.execution
    - attack.t1059.001
logsource:
    category: process_creation  # or network_connection, file_event, etc.
    product: windows
detection:
    selection:
        Image|endswith: '\powershell.exe'
        CommandLine|contains|all:
            - 'DownloadString'
            - 'Invoke-Expression'
    condition: selection
falsepositives:
    - Legitimate administrative scripts
level: high  # informational, low, medium, high, critical
```

### Common Sigma Logsources

| Category | Product | Event Source | Use Case |
|----------|---------|--------------|----------|
| `process_creation` | windows | Sysmon Event ID 1, Security 4688 | Process execution |
| `network_connection` | windows | Sysmon Event ID 3 | Network activity |
| `file_event` | windows | Sysmon Event ID 11 | File creation |
| `registry_event` | windows | Sysmon Event ID 12/13/14 | Registry modifications |
| `image_load` | windows | Sysmon Event ID 7 | DLL loading |
| `create_remote_thread` | windows | Sysmon Event ID 8 | Process injection |
| `dns_query` | windows | Sysmon Event ID 22 | DNS queries |

### Sigma Modifiers

**String Matching:**
- `|contains` - String contains value
- `|startswith` - String starts with value
- `|endswith` - String ends with value
- `|all` - All values must be present
- `|re` - Regular expression match

**Examples:**
```yaml
# Contains any
CommandLine|contains:
    - 'powershell'
    - 'cmd.exe'

# Contains all
CommandLine|contains|all:
    - 'Invoke-WebRequest'
    - '-OutFile'

# Ends with
Image|endswith: '\rundll32.exe'

# Starts with
CommandLine|startswith: 'C:\Windows\System32\'

# Regex
CommandLine|re: '.*\\\\AppData\\\\Local\\\\Temp\\\\[a-z]{8}\.exe'
```

### Example 1: PowerShell Download Cradle

```yaml
title: Suspicious PowerShell Download and Execute
id: 12345678-1234-1234-1234-123456789abc
status: experimental
description: Detects PowerShell downloading content and executing it via Invoke-Expression
references:
    - https://attack.mitre.org/techniques/T1059/001/
    - https://attack.mitre.org/techniques/T1105/
author: Analyst Name
date: 2025-10-26
tags:
    - attack.execution
    - attack.t1059.001
    - attack.command_and_control
    - attack.t1105
logsource:
    category: process_creation
    product: windows
detection:
    selection:
        Image|endswith:
            - '\powershell.exe'
            - '\pwsh.exe'
        CommandLine|contains|all:
            - 'DownloadString'
            - 'IEX'
    condition: selection
falsepositives:
    - Legitimate software deployment scripts
    - Administrative automation
level: high
```

### Example 2: Suspicious Registry Run Key

```yaml
title: Malware Persistence via Registry Run Key
id: 23456789-2345-2345-2345-234567890abc
status: stable
description: Detects creation of registry Run key pointing to suspicious locations
references:
    - https://attack.mitre.org/techniques/T1547/001/
author: Analyst Name
date: 2025-10-26
tags:
    - attack.persistence
    - attack.t1547.001
logsource:
    category: registry_event
    product: windows
detection:
    selection:
        EventType: SetValue
        TargetObject|contains: '\Software\Microsoft\Windows\CurrentVersion\Run\'
        Details|contains:
            - '\AppData\Local\Temp\'
            - '\Users\Public\'
            - '\ProgramData\'
            - '%TEMP%'
    condition: selection
falsepositives:
    - Legitimate software installations
level: medium
```

### Example 3: Network Connection to Malicious IP

```yaml
title: Network Connection to Known C2 Server
id: 34567890-3456-3456-3456-345678901abc
status: experimental
description: Detects network connection to known malware C2 IP address
references:
    - Internal malware analysis report
author: Analyst Name
date: 2025-10-26
tags:
    - attack.command_and_control
    - attack.t1071
logsource:
    category: network_connection
    product: windows
detection:
    selection:
        DestinationIp:
            - '192.168.56.101'  # Replace with actual C2 IP
            - '10.0.0.50'
        DestinationPort:
            - 443
            - 8080
    condition: selection
falsepositives:
    - Rare, should be investigated
level: high
```

### Example 4: Suspicious File Creation

```yaml
title: Malware Dropping Files to Suspicious Location
id: 45678901-4567-4567-4567-456789012abc
status: experimental
description: Detects file creation in common malware drop locations
references:
    - https://attack.mitre.org/techniques/T1105/
author: Analyst Name
date: 2025-10-26
tags:
    - attack.defense_evasion
    - attack.t1105
logsource:
    category: file_event
    product: windows
detection:
    selection:
        TargetFilename|contains:
            - '\AppData\Local\Temp\'
            - '\Users\Public\'
        TargetFilename|endswith:
            - '.exe'
            - '.dll'
            - '.bat'
            - '.vbs'
    condition: selection
falsepositives:
    - Software installations
    - Temporary file creation by legitimate apps
level: low
```

### Convert Sigma to SIEM Queries

**Using sigmac (legacy) or sigma-cli (modern):**

```bash
# Install sigma-cli
pip install sigma-cli

# Convert to Splunk
sigma convert -t splunk rule.yml

# Convert to Elastic
sigma convert -t elasticsearch rule.yml

# Convert to QRadar
sigma convert -t qradar rule.yml

# Convert to Microsoft Sentinel
sigma convert -t sentinel rule.yml
```

**Example Conversions:**

**Splunk:**
```spl
index=windows EventCode=1
(Image="*\\powershell.exe" OR Image="*\\pwsh.exe")
CommandLine="*DownloadString*" CommandLine="*IEX*"
```

**Elastic:**
```json
{
  "query": {
    "bool": {
      "must": [
        {"wildcard": {"process.executable": "*\\\\powershell.exe"}},
        {"wildcard": {"process.command_line": "*DownloadString*"}},
        {"wildcard": {"process.command_line": "*IEX*"}}
      ]
    }
  }
}
```

### Sigma Rule Best Practices

**Do:**
- Use unique UUIDs (generate with `uuidgen` or online)
- Include MITRE ATT&CK tags
- List realistic false positives
- Test on real data before deployment
- Use specific conditions (avoid over-matching)
- Document references and context
- Set appropriate severity levels

**Don't:**
- Use overly broad conditions
- Forget false positive analysis
- Skip testing
- Hardcode environment-specific values
- Ignore performance impact

---

## Suricata Rule Creation (Network IDS)

### Suricata Rule Structure

```
action protocol src_ip src_port -> dest_ip dest_port (rule_options)
```

**Components:**
- **Action**: alert, drop, reject, pass
- **Protocol**: tcp, udp, icmp, http, dns, tls
- **Src/Dest**: IP ranges, ports, $variables
- **Rule Options**: Keywords that define detection logic

### Example 1: HTTP C2 Traffic

```
alert http $HOME_NET any -> $EXTERNAL_NET any (
    msg:"ET MALWARE Suspicious C2 Checkin";
    flow:established,to_server;
    content:"POST"; http_method;
    content:"/api/checkin"; http_uri;
    http.user_agent; content:"Mozilla/4.0 (compatible|3b| MSIE 6.0)";
    sid:1000001;
    rev:1;
    metadata:created_at 2025_10_26;
)
```

**Breakdown:**
- `alert http` - Alert on HTTP traffic
- `$HOME_NET any -> $EXTERNAL_NET any` - Outbound traffic
- `flow:established,to_server` - Established connection to server
- `content:"POST"; http_method` - HTTP POST request
- `content:"/api/checkin"; http_uri` - Specific URI path
- `http.user_agent; content:"..."` - Specific User-Agent
- `sid:1000001` - Signature ID (use 1000000+ for custom rules)
- `rev:1` - Revision number

### Example 2: DNS C2 Communication

```
alert dns $HOME_NET any -> any 53 (
    msg:"ET MALWARE Suspicious DGA Domain Query";
    dns.query; content:".tk"; nocase;
    sid:1000002;
    rev:1;
    metadata:created_at 2025_10_26;
)
```

### Example 3: TLS C2 with SNI

```
alert tls $HOME_NET any -> $EXTERNAL_NET 443 (
    msg:"ET MALWARE Known C2 Server Certificate";
    tls.sni; content:"malicious.com";
    tls.cert_subject; content:"CN=Evil Corp";
    sid:1000003;
    rev:1;
    metadata:created_at 2025_10_26;
)
```

### Example 4: Malware Download

```
alert http $HOME_NET any -> $EXTERNAL_NET any (
    msg:"ET MALWARE Executable Download from Suspicious TLD";
    flow:established,to_server;
    http.uri; content:".exe"; endswith;
    http.host; content:".tk"; endswith;
    sid:1000004;
    rev:1;
    metadata:created_at 2025_10_26;
)
```

### Suricata HTTP Keywords

- `http.method` - GET, POST, PUT, etc.
- `http.uri` - Request URI path
- `http.host` - Host header
- `http.user_agent` - User-Agent string
- `http.request_body` - POST data
- `http.response_body` - Response content
- `http.header` - Any HTTP header
- `http.stat_code` - Response code (200, 404, etc.)

### Suricata DNS Keywords

- `dns.query` - DNS query name
- `dns.opcode` - DNS operation code
- `dns.rcode` - DNS response code

### Suricata TLS Keywords

- `tls.sni` - Server Name Indication
- `tls.cert_subject` - Certificate subject
- `tls.cert_issuer` - Certificate issuer
- `tls.cert_serial` - Certificate serial number
- `tls.version` - TLS version

### Testing Suricata Rules

```bash
# Test rule syntax
suricata -T -c /etc/suricata/suricata.yaml -S custom.rules

# Run on PCAP
suricata -r sample_traffic.pcapng -S custom.rules -l /var/log/suricata/

# Check alerts
cat /var/log/suricata/fast.log
```

### Suricata Best Practices

**Do:**
- Use flow keywords (established, to_server, to_client)
- Anchor strings with content modifiers (startswith, endswith)
- Use fast_pattern for performance
- Test against PCAPs before deployment
- Use metadata for rule management
- Include revision tracking

**Don't:**
- Write overly broad rules (high false positive rate)
- Use regex unless necessary (performance impact)
- Forget to test on benign traffic
- Use conflicting SIDs (must be unique)
- Skip documentation in msg field

---

## Hunting Queries

### Splunk Hunting Queries

**Hunt for PowerShell Download Cradles:**
```spl
index=windows EventCode=1
(Image="*\\powershell.exe" OR Image="*\\pwsh.exe")
(CommandLine="*DownloadString*" OR CommandLine="*DownloadFile*" OR CommandLine="*Invoke-WebRequest*")
| table _time, ComputerName, User, CommandLine
| sort -_time
```

**Hunt for Suspicious Registry Run Keys:**
```spl
index=windows EventCode=13
TargetObject="*\\Software\\Microsoft\\Windows\\CurrentVersion\\Run*"
(Details="*\\AppData\\Local\\Temp\\*" OR Details="*\\Users\\Public\\*" OR Details="*\\ProgramData\\*")
| table _time, ComputerName, TargetObject, Details
| sort -_time
```

**Hunt for Outbound Connections to Rare Destinations:**
```spl
index=network
| stats count by dest_ip
| where count < 5
| join dest_ip [search index=network]
| table _time, src_ip, dest_ip, dest_port, bytes_out
```

### Elastic (KQL) Hunting Queries

**Hunt for Process Injection:**
```
event.code:8 AND
winlog.event_data.TargetImage:(*\\explorer.exe OR *\\svchost.exe) AND
NOT winlog.event_data.SourceImage:C\\:\\Windows\\System32\\*
```

**Hunt for Suspicious File Creations:**
```
event.code:11 AND
file.path:(*\\AppData\\Local\\Temp\\*.exe OR *\\Users\\Public\\*.exe) AND
NOT process.executable:(*\\Windows\\System32\\* OR *\\Program Files\\*)
```

### EDR Hunting (Generic Pseudocode)

**Hunt for Credential Access:**
```
Process = "lsass.exe" AND
AccessMask IN (0x1010, 0x1410, 0x1438) AND
SourceImage NOT IN (known_good_processes)
```

**Hunt for Lateral Movement:**
```
Process = "psexec.exe" OR
Process = "wmic.exe" OR
(Process = "powershell.exe" AND CommandLine CONTAINS "Invoke-Command")
```

---

## IOC Formats & Standards

### STIX (Structured Threat Information Expression)

**STIX 2.1 Example:**
```json
{
  "type": "indicator",
  "spec_version": "2.1",
  "id": "indicator--12345678-1234-1234-1234-123456789abc",
  "created": "2025-10-26T12:00:00.000Z",
  "modified": "2025-10-26T12:00:00.000Z",
  "name": "Malicious Domain: malicious.com",
  "description": "C2 domain for Malware Family X",
  "pattern": "[domain-name:value = 'malicious.com']",
  "pattern_type": "stix",
  "valid_from": "2025-10-26T12:00:00.000Z",
  "labels": ["malicious-activity"]
}
```

### CSV Format (Simple)

```csv
ioc_type,ioc_value,confidence,description,first_seen
domain,malicious.com,high,C2 server,2025-10-26
ip,192.168.1.100,medium,C2 IP address,2025-10-26
sha256,abc123...,high,Malware sample hash,2025-10-26
mutex,Global\M12345,high,Mutex name,2025-10-26
registry,HKCU\Software\...\Run,high,Persistence key,2025-10-26
```

### OpenIOC Format

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ioc xmlns="http://schemas.mandiant.com/2010/ioc">
  <short_description>Malware Family X IOCs</short_description>
  <description>IOCs from analysis of Malware Family X</description>
  <authored_by>Analyst Name</authored_by>
  <authored_date>2025-10-26T12:00:00</authored_date>
  <definition>
    <Indicator operator="OR">
      <IndicatorItem>
        <Context document="FileItem" search="FileItem/Md5sum"/>
        <Content type="md5">abc123...</Content>
      </IndicatorItem>
      <IndicatorItem>
        <Context document="Network" search="Network/DNS"/>
        <Content type="string">malicious.com</Content>
      </IndicatorItem>
    </Indicator>
  </definition>
</ioc>
```

---

## Detection Logic Development

### From Analysis to Detection

**Step 1: Identify Unique Behaviors**
From dynamic analysis, extract behaviors that are:
- Uncommon in legitimate software
- Hard for attackers to change
- Observable in logs/network traffic

**Step 2: Map to Data Sources**

| Behavior | Data Source | Detection Method |
|----------|-------------|------------------|
| Process injection | Sysmon Event ID 8 | Sigma rule |
| C2 beacon | Network logs, proxy | Suricata rule |
| Registry persistence | Sysmon Event ID 13 | Sigma rule |
| File drop | Sysmon Event ID 11 | Sigma rule + YARA |
| DNS query (DGA) | DNS logs | Suricata rule |

**Step 3: Write Detection Rule**

Choose appropriate rule type:
- **Host-based** → Sigma rule (SIEM/EDR)
- **Network-based** → Suricata rule (IDS/IPS)
- **File-based** → YARA rule (scanning)

**Step 4: Test & Validate**

- Test on malware sample (must alert)
- Test on benign samples (must not alert)
- Adjust thresholds/conditions
- Document false positive scenarios

**Step 5: Deploy & Tune**

- Deploy to pilot environment
- Monitor alert volume
- Investigate false positives
- Tune rule based on feedback
- Document tuning changes

---

## Quality Checklist

Before finalizing detection content:

**Sigma Rules:**
- [ ] Unique UUID assigned
- [ ] MITRE ATT&CK tags included
- [ ] Tested on sample data
- [ ] False positives documented
- [ ] Appropriate severity level set
- [ ] References included
- [ ] Logsource correctly specified

**Suricata Rules:**
- [ ] Unique SID assigned (1000000+)
- [ ] Tested on PCAP
- [ ] Flow keywords used (performance)
- [ ] Metadata included
- [ ] No syntax errors (suricata -T)
- [ ] Tested on benign traffic
- [ ] Message clearly describes detection

**IOCs:**
- [ ] All IOCs defanged properly
- [ ] Confidence levels assigned
- [ ] Volatility assessed
- [ ] Context provided for each IOC
- [ ] No environment-specific artifacts
- [ ] Timestamps included (UTC)
- [ ] Format standardized (CSV/STIX/OpenIOC)

**Hunting Queries:**
- [ ] Query tested and returns results
- [ ] Performance acceptable (<30s)
- [ ] Results actionable
- [ ] False positive rate acceptable
- [ ] Query documented (purpose, expected results)

---

## Integration with Malware Reports

Detection content appears in multiple report sections:

**IOCs Section:**
- Defanged IOCs grouped by type
- Confidence ratings
- Context for each indicator

**Detection Rules Section:**
- YARA rules (from malware-report-writer skill)
- Sigma rules (from this skill)
- Suricata rules (from this skill)

**Remediation Section:**
- Hunting queries for IR teams
- Detection deployment guidance
- IOC search instructions

**Appendix:**
- IOC export files (CSV, STIX)
- Sigma rule files (.yml)
- Suricata rule files (.rules)

---

## Tool Quick Reference

| Task | Tool | Command |
|------|------|---------|
| **Defang IOCs** | ioc-fanger | `echo "http://evil.com" \| fanger --defang` |
| **Convert Sigma** | sigma-cli | `sigma convert -t splunk rule.yml` |
| **Test Suricata** | suricata | `suricata -T -S rules.rules` |
| **Generate UUID** | uuidgen | `uuidgen` (Linux/Mac) or online |
| **Validate STIX** | stix2-validator | `stix2_validator file.json` |

---

## Example Usage

**User request:** "Help me create detection rules for this ransomware that encrypts files with .locked extension"

**Workflow:**
1. **Defang IOCs** from analysis (C2 domain, IP, file paths)
2. **Create Sigma rule** for file encryption behavior (Sysmon Event ID 11)
3. **Create Suricata rule** for C2 communication pattern
4. **Generate hunting query** to find encrypted files across environment
5. **Export IOCs** in CSV format for SOC import
6. **Document** all rules with context and testing notes
7. **Provide** deployment guidance for blue team
