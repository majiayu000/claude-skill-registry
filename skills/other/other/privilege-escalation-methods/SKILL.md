---
name: Privilege Escalation Methods
description: This skill should be used when the user asks to "escalate privileges", "get root access", "become administrator", "privesc techniques", "abuse sudo", "exploit SUID binaries", "Kerberoasting", "pass-the-ticket", "token impersonation", or needs guidance on post-exploitation privilege escalation for Linux or Windows systems.
metadata:
  author: zebbern
  version: 4.1.0-fractal
---

# Privilege Escalation Methods

## Purpose

Provide comprehensive techniques for escalating privileges from a low-privileged user to root/administrator access on compromised Linux and Windows systems. Essential for penetration testing post-exploitation phase and red team operations.

## Inputs/Prerequisites

- Initial low-privilege shell access on target system
- Kali Linux or penetration testing distribution
- Tools: Mimikatz, PowerView, PowerUpSQL, Responder, Impacket, Rubeus
- Understanding of Windows/Linux privilege models
- For AD attacks: Domain user credentials and network access to DC

## Outputs/Deliverables

- Root or Administrator shell access
- Extracted credentials and hashes
- Persistent access mechanisms
- Domain compromise (for AD environments)

---

## Core Techniques

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [Linux Privilege Escalation](./sub-skills/linux-privilege-escalation.md)
### 2. [Windows Privilege Escalation](./sub-skills/windows-privilege-escalation.md)
### 3. [Active Directory Attacks](./sub-skills/active-directory-attacks.md)
### 4. [Credential Harvesting](./sub-skills/credential-harvesting.md)
### 5. [Example 1: Linux Sudo to Root](./sub-skills/example-1-linux-sudo-to-root.md)
### 6. [Example 2: Windows Kerberoasting](./sub-skills/example-2-windows-kerberoasting.md)
