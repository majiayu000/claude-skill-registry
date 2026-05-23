---
name: incident-response
description: IR playbook execution — evidence collection, timeline analysis, memory forensics, disk forensics, containment strategies, post-incident reporting
metadata:
  type: defensive
  phase: response
  tools: volatility3, autopsy, sleuthkit, plaso, chainsaw, hayabusa, velociraptor
---

# Incident Response

## When to Activate

- Active security incident requiring investigation
- Memory forensics and artifact extraction
- Disk forensics and timeline reconstruction
- Malware containment and eradication
- Post-incident analysis and reporting

## IR Phases

### 1. Identification & Scoping
```bash
# Determine scope of compromise
# Key questions:
# - What systems are affected?
# - What's the initial access vector?
# - How long has the attacker been present?
# - What data may be compromised?
# - Is the attacker still active?

# Quick triage
chainsaw hunt /path/to/evtx/ -s sigma/ --mapping mappings/sigma-event-log-all.yml
hayabusa csv-timeline -d /path/to/evtx/ -o timeline.csv
```

### 2. Evidence Collection
```bash
# Memory acquisition (before anything else!)
# Windows: winpmem, DumpIt, FTK Imager
# Linux: LiME (insmod lime.ko "path=/evidence/mem.lime format=lime")

# Disk imaging
dd if=/dev/sda of=/evidence/disk.img bs=4M status=progress
# Or: FTK Imager, dc3dd for forensic imaging

# Log collection
# Windows: Event logs, Sysmon, PowerShell logs
# Linux: /var/log/auth.log, /var/log/syslog, journalctl
# Network: PCAP, NetFlow, DNS logs, proxy logs
# Cloud: CloudTrail, Azure Activity Log, GCP Audit Log

# Volatile data (collect before shutdown)
# - Running processes (ps aux / tasklist)
# - Network connections (netstat -anp / Get-NetTCPConnection)
# - Logged-in users (w / query user)
# - Open files (lsof / handle.exe)
# - Loaded modules (lsmod / listdlls)
```

### 3. Memory Forensics (Volatility 3)
```bash
# Process analysis
vol3 -f mem.raw windows.pslist
vol3 -f mem.raw windows.pstree
vol3 -f mem.raw windows.cmdline
vol3 -f mem.raw windows.netscan

# Malware detection
vol3 -f mem.raw windows.malfind  # injected code
vol3 -f mem.raw windows.hollowprocesses  # process hollowing
vol3 -f mem.raw windows.svcscan  # suspicious services

# Credential extraction
vol3 -f mem.raw windows.hashdump
vol3 -f mem.raw windows.lsadump
vol3 -f mem.raw windows.cachedump

# File extraction
vol3 -f mem.raw windows.dumpfiles --pid PID
vol3 -f mem.raw windows.filescan | grep -i "suspicious"

# Linux memory
vol3 -f mem.raw linux.pslist
vol3 -f mem.raw linux.bash  # bash history from memory
vol3 -f mem.raw linux.check_syscall  # rootkit detection
```

### 4. Timeline Analysis
```bash
# Plaso/log2timeline (super timeline)
log2timeline.py /evidence/timeline.plaso /evidence/disk.img
psort.py -o l2tcsv /evidence/timeline.plaso -w timeline.csv

# Filter timeline around incident window
psort.py -o l2tcsv /evidence/timeline.plaso \
  --slice "2026-05-15T00:00:00" --slice_size 72 \
  -w incident_window.csv

# Key artifacts for timeline:
# - $MFT (file creation/modification)
# - Prefetch (program execution)
# - Amcache (program installation)
# - ShimCache (program execution)
# - USN Journal (file changes)
# - Event logs (logon, process creation, service install)
# - Browser history (initial access)
# - Registry (persistence, configuration)
```

### 5. Containment
```bash
# Network isolation
# - Block C2 IPs/domains at firewall
# - Isolate affected hosts (VLAN change, host firewall)
# - Disable compromised accounts
# - Revoke compromised credentials/tokens

# Endpoint containment
# - Kill malicious processes
# - Remove persistence mechanisms
# - Block malicious hashes (AppLocker, WDAC)
# - Deploy EDR containment (isolate host)

# Cloud containment
# - Revoke IAM keys
# - Disable compromised service accounts
# - Block malicious IPs in security groups
# - Enable enhanced logging
```

### 6. Eradication & Recovery
```bash
# Remove all attacker artifacts:
# - Malware binaries
# - Persistence mechanisms (registry, scheduled tasks, services)
# - Backdoor accounts
# - Modified system files
# - Webshells

# Verify clean state:
# - Full AV/EDR scan
# - Integrity check against known-good baseline
# - Review all persistence locations
# - Check for additional backdoors

# Recovery:
# - Restore from clean backups (pre-compromise)
# - Rebuild compromised systems
# - Reset all credentials
# - Patch exploited vulnerabilities
# - Enhance monitoring
```

## IOC Extraction

```bash
# Network IOCs
# - C2 IP addresses and domains
# - User-Agent strings
# - JA3/JA4 hashes
# - URI patterns
# - DNS query patterns

# Host IOCs
# - File hashes (MD5, SHA256)
# - File paths and names
# - Registry keys/values
# - Mutex names
# - Service names
# - Scheduled task names
# - Named pipes

# Behavioral IOCs
# - Process trees (parent-child relationships)
# - Command-line patterns
# - Network connection patterns
# - File access patterns
```

## Reporting Template

```markdown
## Incident Report: [Title]
### Executive Summary
[1-2 paragraphs: what happened, impact, current status]

### Timeline
| Time (UTC) | Event | Source | Details |
|------------|-------|--------|---------|
| ... | ... | ... | ... |

### Attack Chain (MITRE ATT&CK)
- Initial Access: [technique]
- Execution: [technique]
- Persistence: [technique]
- ...

### Affected Systems
| Host | Role | Compromise Level | Status |
|------|------|-----------------|--------|
| ... | ... | ... | ... |

### IOCs
[Structured list of all indicators]

### Root Cause
[What allowed the attack to succeed]

### Recommendations
1. Immediate actions
2. Short-term improvements
3. Long-term strategic changes

### Lessons Learned
[What went well, what didn't, process improvements]
```
