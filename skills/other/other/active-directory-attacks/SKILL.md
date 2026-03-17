---
name: Active Directory Attacks
description: This skill should be used when the user asks to "attack Active Directory", "exploit AD", "Kerberoasting", "DCSync", "pass-the-hash", "BloodHound enumeration", "Golden Ticket", "Silver Ticket", "AS-REP roasting", "NTLM relay", or needs guidance on Windows domain penetration testing.
metadata:
  author: zebbern
  version: 4.1.0-fractal
---

# Active Directory Attacks

## Purpose

Provide comprehensive techniques for attacking Microsoft Active Directory environments. Covers reconnaissance, credential harvesting, Kerberos attacks, lateral movement, privilege escalation, and domain dominance for red team operations and penetration testing.

## Inputs/Prerequisites

- Kali Linux or Windows attack platform
- Domain user credentials (for most attacks)
- Network access to Domain Controller
- Tools: Impacket, Mimikatz, BloodHound, Rubeus, CrackMapExec

## Outputs/Deliverables

- Domain enumeration data
- Extracted credentials and hashes
- Kerberos tickets for impersonation
- Domain Administrator access
- Persistent access mechanisms

---

## Essential Tools

| Tool | Purpose |
|------|---------|
| BloodHound | AD attack path visualization |
| Impacket | Python AD attack tools |
| Mimikatz | Credential extraction |
| Rubeus | Kerberos attacks |
| CrackMapExec | Network exploitation |
| PowerView | AD enumeration |
| Responder | LLMNR/NBT-NS poisoning |

---

## Core Workflow

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [Step 1: Kerberos Clock Sync](./sub-skills/step-1-kerberos-clock-sync.md)
### 2. [Step 2: AD Reconnaissance with BloodHound](./sub-skills/step-2-ad-reconnaissance-with-bloodhound.md)
### 3. [Step 3: PowerView Enumeration](./sub-skills/step-3-powerview-enumeration.md)
### 4. [Password Spraying](./sub-skills/password-spraying.md)
### 5. [Kerberoasting](./sub-skills/kerberoasting.md)
### 6. [AS-REP Roasting](./sub-skills/as-rep-roasting.md)
### 7. [DCSync Attack](./sub-skills/dcsync-attack.md)
### 8. [Pass-the-Ticket (Golden Ticket)](./sub-skills/pass-the-ticket-golden-ticket.md)
### 9. [Silver Ticket](./sub-skills/silver-ticket.md)
### 10. [Pass-the-Hash](./sub-skills/pass-the-hash.md)
### 11. [OverPass-the-Hash](./sub-skills/overpass-the-hash.md)
### 12. [Responder + ntlmrelayx](./sub-skills/responder-ntlmrelayx.md)
### 13. [SMB Signing Check](./sub-skills/smb-signing-check.md)
### 14. [ESC1 - Misconfigured Templates](./sub-skills/esc1-misconfigured-templates.md)
### 15. [ESC8 - Web Enrollment Relay](./sub-skills/esc8-web-enrollment-relay.md)
### 16. [ZeroLogon (CVE-2020-1472)](./sub-skills/zerologon-cve-2020-1472.md)
### 17. [PrintNightmare (CVE-2021-1675)](./sub-skills/printnightmare-cve-2021-1675.md)
### 18. [samAccountName Spoofing (CVE-2021-42278/42287)](./sub-skills/samaccountname-spoofing-cve-2021-4227842287.md)
### 19. [Example 1: Domain Compromise via Kerberoasting](./sub-skills/example-1-domain-compromise-via-kerberoasting.md)
### 20. [Example 2: NTLM Relay to LDAP](./sub-skills/example-2-ntlm-relay-to-ldap.md)
