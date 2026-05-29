---
name: incident-response
description: IR playbook execution — evidence collection, timeline analysis, memory forensics, disk forensics, containment strategies, post-incident reporting
metadata:
  type: defensive
  phase: response
  tools: volatility3, autopsy, sleuthkit, plaso, chainsaw, hayabusa, velociraptor
kill_chain:
  phase: [report]
  step: [8]
  attck_tactics: []
depends_on: [red-team-ops]
feeds_into: [threat-hunting]
inputs: [memory_dumps, disk_images, log_data]
outputs: [timeline, ioc_list, forensic_report]
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

## Advanced: Memory Forensics Deep Dive

### Volatility 3 Advanced Plugins
```bash
# Rootkit detection
vol3 -f mem.raw windows.ssdt  # System Service Descriptor Table hooks
vol3 -f mem.raw windows.callbacks  # Kernel callback modifications
vol3 -f mem.raw windows.driverirp  # IRP hook detection
vol3 -f mem.raw windows.modscan  # Hidden kernel modules (walk unlinked)

# Process injection detection
vol3 -f mem.raw windows.malfind  # Executable, non-image memory (injected code)
vol3 -f mem.raw windows.hollowprocesses  # Process hollowing detection
vol3 -f mem.raw windows.vadinfo --pid PID  # Virtual Address Descriptor analysis

# Network forensics from memory
vol3 -f mem.raw windows.netstat  # Active and closed connections
vol3 -f mem.raw windows.netscan  # Scan for connection objects

# Registry from memory (may contain keys deleted from disk)
vol3 -f mem.raw windows.registry.hivelist
vol3 -f mem.raw windows.registry.printkey --key "Software\Microsoft\Windows\CurrentVersion\Run"

# Extracting executables from memory
vol3 -f mem.raw windows.pslist --pid PID --dump  # Dump process executable
vol3 -f mem.raw windows.dlllist --pid PID --dump  # Dump loaded DLLs

# Volatility 3 custom plugin for specific IOCs
vol3 -f mem.raw windows.cmdline | grep -i "powershell\|cmd\|certutil"
vol3 -f mem.raw windows.envars --pid PID  # Environment variables
```

### Linux Memory Forensics
```bash
# Linux-specific analysis
vol3 -f mem.raw linux.pslist  # Process list
vol3 -f mem.raw linux.pstree  # Process tree
vol3 -f mem.raw linux.bash  # Bash history from memory
vol3 -f mem.raw linux.lsof  # Open files
vol3 -f mem.raw linux.sockstat  # Network sockets

# Rootkit detection
vol3 -f mem.raw linux.check_syscall  # Syscall table hooks
vol3 -f mem.raw linux.check_modules  # Hidden kernel modules
vol3 -f mem.raw linux.tty_check  # TTY hooks (keystroke capture)
vol3 -f mem.raw linux.hidden_modules  # Modules removed from list

# eBPF program detection (modern rootkits)
vol3 -f mem.raw linux.check_syscall  # eBPF kprobes on syscalls
# Manual: scan for BPF program structures in memory
# Look for: bpf_prog structures, BPF maps
```

### Memory Analysis Methodology
```
# Systematic approach for memory forensics:

# 1. Process Analysis (first pass)
#    - List all processes → identify unknown/suspicious
#    - Check parent-child relationships → spot reparenting
#    - Look for: processes with unusual parents, multiple instances
#      of unique processes, process name typosquatting (svchost vs svch0st)

# 2. Network Analysis (connections from memory)
#    - Active connections → identify C2
#    - Closed connections → historical C2 communication
#    - Listening ports → backdoor services
#    - Correlate: process → network connection → remote IP

# 3. Code Injection Detection
#    - malfind → executable private memory (not backed by file)
#    - hollowprocesses → legitimate process with replaced code
#    - VAD analysis → regions with unusual permissions (RWX)
#    - DLL analysis → DLLs loaded from unusual paths

# 4. Persistence Artifacts
#    - Registry Run keys from memory
#    - Services → compare against known-good baseline
#    - Scheduled tasks → look for new/modified tasks
#    - WMI event subscriptions from memory

# 5. Credential Extraction
#    - LSASS memory → plaintext passwords, hashes, tickets
#    - SAM/SECURITY/SYSTEM hive → local account hashes
#    - Kerberos tickets → lateral movement evidence
```

## Advanced: Disk Forensics Techniques

### NTFS Artifact Analysis
```bash
# $MFT (Master File Table) — every file operation
# Parse with: analyzeMFT, MFTECmd
MFTECmd.exe -f '$MFT' --csv output/ --csvf mft.csv
# Key fields: creation time, modification time, entry modification time, 
# access time, file size, parent directory

# $UsnJrnl (Update Sequence Number Journal) — file change log
MFTECmd.exe -f '$J' --csv output/ --csvf usn.csv
# Shows: file creates, deletes, renames, data changes
# Critical for: tracking file deletion, timestomping detection

# $LogFile (NTFS transaction log)
# Contains: metadata changes for crash recovery
# Useful: recovering deleted file metadata

# Alternate Data Streams (ADS) — hidden data
# Malware often hides in ADS
dir /r /s C:\Users\  # List files with ADS
# Or: streams.exe -s C:\Users\

# Prefetch files — program execution evidence
# C:\Windows\Prefetch\*.pf
PECmd.exe -d C:\Windows\Prefetch\ --csv output/ --csvf prefetch.csv
# Shows: executable name, run count, last 8 execution times, files accessed

# Amcache.hve — application compatibility cache
AmcacheParser.exe -f C:\Windows\AppCompat\Programs\Amcache.hve --csv output/
# Shows: SHA1 hash of executables, full path, first run time

# ShimCache (AppCompatCache) — program execution
AppCompatCacheParser.exe -f SYSTEM --csv output/
# Shows: executable path, last modified time, execution flag
```

### Evidence of Execution
```bash
# Windows:
# 1. Prefetch: C:\Windows\Prefetch\PROGRAM.EXE-HASH.pf
# 2. Amcache: HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags
# 3. ShimCache: HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatibility
# 4. BAM/DAM: HKLM\SYSTEM\CurrentControlSet\Services\bam\State\UserSettings\SID
# 5. UserAssist: HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\UserAssist
# 6. SRUM (System Resource Usage Monitor): C:\Windows\System32\sru\SRUDB.dat
#    Contains: network usage per app, bytes sent/received, execution time

# Linux:
# 1. /var/log/auth.log — authentication and sudo
# 2. /var/log/wtmp — login records (last -f /var/log/wtmp)
# 3. ~/.bash_history — command history
# 4. /var/log/audit/audit.log — auditd records
# 5. /proc filesystem (live analysis) — current process info
# 6. /tmp, /var/tmp, /dev/shm — common staging directories
```

## Advanced: Cloud Incident Response

### AWS IR
```bash
# Immediate containment:
# 1. Disable compromised IAM keys
aws iam update-access-key --access-key-id AKIAEXAMPLE --status Inactive --user-name compromised_user
# 2. Attach deny-all policy
aws iam put-user-policy --user-name compromised_user --policy-name DenyAll \
  --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Deny","Action":"*","Resource":"*"}]}'

# Evidence collection:
# CloudTrail logs (last 90 days by default)
aws cloudtrail lookup-events --lookup-attributes AttributeKey=Username,AttributeValue=attacker \
  --start-time 2026-05-01 --end-time 2026-05-28

# VPC Flow Logs
aws ec2 describe-flow-logs
aws logs get-log-events --log-group-name /vpc/flow-logs --log-stream-name eni-xxx

# GuardDuty findings
aws guardduty list-findings --detector-id xxx
aws guardduty get-findings --detector-id xxx --finding-ids id1 id2

# S3 access logs
aws s3api get-bucket-logging --bucket target-bucket

# EC2 instance forensics
# 1. Snapshot the volume
aws ec2 create-snapshot --volume-id vol-xxx --description "IR evidence"
# 2. Launch forensic workstation
# 3. Attach snapshot as secondary volume
# 4. Analyze offline (don't modify original)

# Lambda investigation
aws lambda get-function --function-name compromised_function
# Check: environment variables, layers, last modified, code
aws cloudwatch logs get-log-events --log-group-name /aws/lambda/function_name
```

### Azure IR
```bash
# Azure Activity Log (90 days)
az monitor activity-log list --start-time 2026-05-01 --query "[?authorization.action=='Microsoft.Compute/virtualMachines/write']"

# Azure AD Sign-in Logs
az ad audit list --filter "createdDateTime ge 2026-05-01"

# Azure Sentinel incidents
# KQL for hunting:
SigninLogs
| where ResultType != 0  # Failed sign-ins
| where UserPrincipalName == "compromised@domain.com"
| summarize count() by IPAddress, Location, bin(TimeGenerated, 1h)

# Containment:
# Disable user
az ad user update --id USER_ID --account-enabled false
# Revoke sessions
az rest --method POST --uri "https://graph.microsoft.com/v1.0/users/USER_ID/revokeSignInSessions"
# Block IP
az network nsg rule create --name BlockAttacker --nsg-name NSG --priority 100 \
  --access Deny --source-address-prefixes ATTACKER_IP --direction Inbound
```

## Advanced: Rootkit Detection

### User-Mode Rootkit Detection
```bash
# Cross-reference multiple data sources:
# 1. Compare process list: pslist vs psscan (Volatility)
#    Discrepancy → process hiding (DKOM — Direct Kernel Object Manipulation)

# 2. Compare DLL lists: ldrmodules
#    Modules in memory but not in PEB lists → hidden DLLs

# 3. File system comparison:
#    MFT entries vs directory listing → hidden files
#    Compare: raw NTFS parse vs OS API results

# 4. Hook detection:
#    Compare IAT/EAT of loaded modules against clean copy
#    Inline hooks: compare function prologues against on-disk version
#    Syscall hooks: compare SSDT against known-good values
```

### Kernel-Mode Rootkit Detection
```bash
# SSDT (System Service Descriptor Table) hooks
vol3 -f mem.raw windows.ssdt
# Compare syscall addresses against ntoskrnl.exe export range
# If address outside ntoskrnl → hooked

# IRP (I/O Request Packet) hooks
vol3 -f mem.raw windows.driverirp
# Check major function pointers for each driver
# Hooks redirect I/O operations (hide files, network connections)

# Callback modifications
vol3 -f mem.raw windows.callbacks
# EDR/security callbacks removed by rootkit
# Look for: empty callback arrays, callbacks pointing to rootkit driver

# IDT (Interrupt Descriptor Table) hooks
# Rare but powerful — intercepts hardware interrupts
# Compare IDT entries against expected kernel addresses

# Timer-based detection
# Rootkits may install timer objects for periodic activity
vol3 -f mem.raw windows.timers

# Cross-reference: loaded drivers vs modules on disk
vol3 -f mem.raw windows.driverscan  # Scan for driver objects
vol3 -f mem.raw windows.modules  # Linked module list
# Difference → hidden kernel modules
```
