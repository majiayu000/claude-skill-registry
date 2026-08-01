---
name: incident-response
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: incident-response
description: >-
  Incident response operations including volatile evidence collection (memory, disk,
  network), forensic tools (Volatility, KAPE, dc3dd), IR runbooks, triage procedures,
  timeline reconstruction, containment strategies, eradication, and post-incident
  analysis with after-action reports.
domain: cybersecurity
subdomain: incident-response
tags:
  - forensics
  - dfir
  - triage
  - ioc
  - memory-forensics
  - timeline-analysis
  - evidence-collection
  - containment
  - eradication
version: "1.1"
author: defconxt
license: AGPL-3.0
compatibility: Designed for Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, and any agentskills.io-compatible agent.
metadata:
  mitre-attack: ["T1070", "T1036", "T1059", "T1486"]
  nist-csf: ["RS.RP-1", "RS.AN-1", "RS.AN-3", "RS.MI-1", "RS.MI-2"]
  frameworks: ["NIST SP 800-61", "RFC 3227", "SANS IR Process"]
---
<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
<!-- CIPHER is a trademark of defconxt. -->

---
name: incident-response
description: >
  DFIR and incident response skill for CIPHER. Activates on incident triage,
  forensic artifact collection, evidence preservation, memory acquisition,
  containment procedures, timeline reconstruction, and post-incident analysis.
  Trigger keywords: DFIR, forensics, triage, IOC, compromise, breach,
  exfiltration, ransomware response, containment, eradication, evidence,
  memory acquisition, Wireshark, Chainsaw, Hayabusa, Volatility.
domain: cybersecurity
subdomain: incident-response
tags:
  - forensics
  - dfir
  - triage
  - ioc
  - memory-forensics
  - network-forensics
  - timeline-analysis
  - containment
  - evidence-preservation
  - ransomware
version: "1.1"
author: defconxt
license: AGPL-3.0
compatibility: Designed for Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, and any agentskills.io-compatible agent.
metadata:
  mitre-attack:
    - T1059   # Command and Scripting Interpreter
    - T1003   # OS Credential Dumping
    - T1078   # Valid Accounts
    - T1021   # Remote Services
    - T1190   # Exploit Public-Facing Application
    - T1486   # Data Encrypted for Impact (Ransomware)
    - T1053   # Scheduled Task/Job
    - T1543   # Create or Modify System Process
    - T1547   # Boot or Logon Autostart Execution
    - T1070   # Indicator Removal
---

# SKILL: Incident Response

## When to Use

Activate this skill when the operator:
- Describes an **active incident** or asks for triage guidance
- Requests **IR runbooks** (ransomware, AD compromise, cloud compromise)
- Needs **forensic artifact** locations (Windows, Linux, macOS)
- Asks about **evidence collection**, memory acquisition, or disk imaging
- Wants **timeline reconstruction** (Plaso, MFT, EVTX correlation)
- Needs **containment** or **eradication** procedures
- Asks about **Wireshark/tshark** analysis or network forensics
- Discusses **post-incident** analysis, after-action reports, or detection gaps

Do NOT use for: threat modeling (use security-architecture), detection rule
writing (use detection-engineering), or red team operations (use offensive skill).

## Prerequisites

| Tool | Purpose | Install |
|------|---------|---------|
| Volatility 3 | Memory analysis | `pip install volatility3` |
| winpmem / LiME / AVML | Memory acquisition | Platform-specific |
| Chainsaw | Fast EVTX triage | GitHub release binary |
| Hayabusa | EVTX timeline CSV | GitHub release binary |
| Plaso (log2timeline) | Multi-source timeline | `pip install plaso` |
| MFTECmd | MFT/NTFS parser | Eric Zimmerman tools |
| tshark / Wireshark | Network forensics | Package manager |
| YARA / LOKI | IOC scanning | `pip install yara-python` |
| UAC | Linux artifact collector | GitHub clone |
| System Informer | Live Windows process analysis | GitHub release |



### Example: Volatile Evidence Collection

```bash
# Collect volatile evidence in order of volatility (RFC 3227)
# 1. Network connections
ss -tulnp > /evidence/network-connections.txt

# 2. Running processes
ps auxf > /evidence/processes.txt

# 3. Open files
lsof -nP > /evidence/open-files.txt

# 4. Logged-in users
w > /evidence/users.txt
last -25 >> /evidence/users.txt

# 5. Generate hash manifest
sha256sum /evidence/*.txt > /evidence/manifest.sha256
```

### Example: Windows Event Log Triage

```powershell
# Failed logins (Event ID 4625)
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4625} -MaxEvents 100 |
  Select-Object TimeCreated, @{N='User';E={$_.Properties[5].Value}},
  @{N='Source';E={$_.Properties[19].Value}} | Format-Table

# New service installations (Event ID 7045)
Get-WinEvent -FilterHashtable @{LogName='System'; Id=7045} -MaxEvents 50 |
  Select-Object TimeCreated, @{N='Service';E={$_.Properties[0].Value}} | Format-Table
```


## Quick Reference

| Task | Command |
|------|---------|
| Memory (Windows) | `winpmem_mini_x64.exe mem.raw` |
| Memory (Linux, LiME) | `insmod lime.ko "path=/tmp/mem.lime format=lime"` |
| Memory (Linux, AVML) | `avml /tmp/mem.lime` |
| Disk image | `dd if=/dev/sda bs=512 \| gzip > disk.img.gz` |
| Hash evidence | `sha256sum mem.raw > mem.raw.sha256` |
| Process list (Linux) | `ps auxf && cat /proc/*/status 2>/dev/null \| grep -E "Name\|Pid\|PPid"` |
| Network connections | `ss -tulnp` (Linux) / `netstat -anob` (Windows) |
| Windows event logs | `wevtutil qe Security /count:1000 /rd:true /format:text` |
| Chainsaw EVTX triage | `chainsaw hunt /path/to/evtx --sigma rules/ --mapping mappings/sigma-event-logs-all.yml` |
| Hayabusa timeline | `hayabusa csv-timeline -d /path/to/evtx -o timeline.csv` |
| Volatility pslist | `vol.py -f mem.raw windows.pslist` + `windows.psscan` |
| tshark C2 beacons | `tshark -r capture.pcap -Y "tcp.flags.syn==1 && !tcp.flags.ack==1" -T fields -e ip.dst \| sort \| uniq -c \| sort -rn` |
| Linux artifact collection | `./uac -p /tmp/uac-output` |

## Workflow

### Phase 1 — Volatile Evidence Collection

**Collect volatile data before ANYTHING else.** NIST 800-86 order:

> running processes → network connections → logged-in users → loaded modules → ARP cache

Full collection scripts (Linux + Windows) and memory acquisition commands:

→ **[references/volatile-evidence.md](references/volatile-evidence.md)**

### Phase 2 — Forensic Analysis & Artifact Collection

Memory analysis with Volatility 3, live process analysis with System Informer,
forensic artifact locations (Windows/Linux/macOS), network forensics with
tshark/Wireshark (display filters, capture filters, attack pattern filters),
timeline reconstruction (Plaso, MFT, EVTX correlation), containment strategies
(network isolation, account containment), IOC scanning (YARA, LOKI, Fenrir),
and post-incident after-action report structure.

→ **[references/forensics-tools.md](references/forensics-tools.md)**

### Phase 3 — Incident Runbooks & Response Chains

Scenario-specific runbooks and operational key chains:

- **Ransomware Response** — triage, containment, evidence preservation, pre-ransomware IOCs
- **Active Directory Compromise** — DCSync detection, golden ticket, krbtgt rotation
- **Cloud Account Compromise (AWS)** — CloudTrail investigation, IAM containment, DenyAll policy
- **Key Chain: Initial Triage → Scoped Compromise** (first 2 hours)
- **Key Chain: Evidence Collection → Forensic Package**
- **Key Chain: Containment → Eradication Pipeline**

→ **[references/ir-runbooks.md](references/ir-runbooks.md)**

## Verification

After completing an IR engagement, confirm:

- [ ] Volatile data collected BEFORE any reboot or disk modification
- [ ] All evidence hashed (SHA-256) with chain of custody documented
- [ ] Memory image acquired and verified (hash match)
- [ ] Event logs exported to write-protected location
- [ ] Timeline normalized to UTC from all log sources
- [ ] Patient zero identified with earliest compromise evidence
- [ ] All persistence mechanisms catalogued and removed
- [ ] Credentials rotated (compromised → service → privileged → krbtgt if AD)
- [ ] Initial access vector patched before systems restored
- [ ] After-action report includes detection gap analysis mapped to ATT&CK
- [ ] SIEM rules updated to cover observed TTPs

---
v1.1 | Validated: 2026-03-13
