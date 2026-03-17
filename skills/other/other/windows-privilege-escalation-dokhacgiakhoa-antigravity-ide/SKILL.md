---
name: Windows Privilege Escalation
description: This skill should be used when the user asks to "escalate privileges on Windows," "find Windows privesc vectors," "enumerate Windows for privilege escalation," "exploit Windows misconfigurations," or "perform post-exploitation privilege escalation." It provides comprehensive guidance for discovering and exploiting privilege escalation vulnerabilities in Windows environments.
metadata:
  author: zebbern
  version: 4.1.0-fractal
---

# Windows Privilege Escalation

## Purpose

Provide systematic methodologies for discovering and exploiting privilege escalation vulnerabilities on Windows systems during penetration testing engagements. This skill covers system enumeration, credential harvesting, service exploitation, token impersonation, kernel exploits, and various misconfigurations that enable escalation from standard user to Administrator or SYSTEM privileges.

## Inputs / Prerequisites

- **Initial Access**: Shell or RDP access as standard user on Windows system
- **Enumeration Tools**: WinPEAS, PowerUp, Seatbelt, or manual commands
- **Exploit Binaries**: Pre-compiled exploits or ability to transfer tools
- **Knowledge**: Understanding of Windows security model and privileges
- **Authorization**: Written permission for penetration testing activities

## Outputs / Deliverables

- **Privilege Escalation Path**: Identified vector to higher privileges
- **Credential Dump**: Harvested passwords, hashes, or tokens
- **Elevated Shell**: Command execution as Administrator or SYSTEM
- **Vulnerability Report**: Documentation of misconfigurations and exploits
- **Remediation Recommendations**: Fixes for identified weaknesses

## Core Workflow

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [1. System Enumeration](./sub-skills/1-system-enumeration.md)
### 2. [2. Credential Harvesting](./sub-skills/2-credential-harvesting.md)
### 3. [3. Service Exploitation](./sub-skills/3-service-exploitation.md)
### 4. [4. Token Impersonation](./sub-skills/4-token-impersonation.md)
### 5. [5. Kernel Exploitation](./sub-skills/5-kernel-exploitation.md)
### 6. [6. Additional Techniques](./sub-skills/6-additional-techniques.md)
### 7. [Enumeration Tools](./sub-skills/enumeration-tools.md)
### 8. [Default Writable Folders](./sub-skills/default-writable-folders.md)
### 9. [Common Privilege Escalation Vectors](./sub-skills/common-privilege-escalation-vectors.md)
### 10. [Impersonation Privilege Exploits](./sub-skills/impersonation-privilege-exploits.md)
### 11. [Operational Boundaries](./sub-skills/operational-boundaries.md)
### 12. [Detection Considerations](./sub-skills/detection-considerations.md)
### 13. [Legal Requirements](./sub-skills/legal-requirements.md)
### 14. [Example 1: Service Binary Path Exploitation](./sub-skills/example-1-service-binary-path-exploitation.md)
### 15. [Example 2: AlwaysInstallElevated Exploitation](./sub-skills/example-2-alwaysinstallelevated-exploitation.md)
### 16. [Example 3: JuicyPotato Token Impersonation](./sub-skills/example-3-juicypotato-token-impersonation.md)
### 17. [Example 4: Unquoted Service Path](./sub-skills/example-4-unquoted-service-path.md)
### 18. [Example 5: Credential Harvesting from Registry](./sub-skills/example-5-credential-harvesting-from-registry.md)
