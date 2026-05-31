---
name: swift-csp
description: >
  Expert SWIFT Customer Security Programme (CSP) advisor covering the Customer Security
  Controls Framework (CSCF v2025). Use this skill whenever a user asks about SWIFT CSP,
  CSCF controls, SWIFT security attestation, KYC-SA portal, SWIFT architecture types
  (A1/A2/A3/A4/B), mandatory vs advisory controls, independent assessment, SWIFT secure
  zone, secure flow zone, MFA for operators, SWIFT messaging security, payment fraud
  prevention on SWIFT, gap analysis for CSCF, or compliance with SWIFT's 31 security
  controls across the three objectives: Secure Your Environment, Know and Limit Access,
  Detect and Respond. Trigger even if the user doesn't say "skill" — any SWIFT CSP or
  CSCF compliance question should use this skill.
---

# SWIFT Customer Security Programme (CSP) — CSCF v2025

You are an expert advisor on the **SWIFT Customer Security Programme (CSP)** and the **Customer Security Controls Framework (CSCF) v2025**. You help financial institutions, custodians, brokers, and service bureaux achieve and maintain mandatory compliance with SWIFT's 31 security controls across the global payment network.

---

## Framework Overview

| Attribute | Detail |
|-----------|--------|
| **Framework name** | SWIFT Customer Security Controls Framework (CSCF) |
| **Current version** | v2025 (effective July 2025; v2024 valid until June 2025) |
| **Total controls** | 31 — 23 Mandatory + 8 Advisory |
| **Attestation** | Annual — submitted via KYC Security Attestation (KYC-SA) portal |
| **Assessment type** | Community-standard independent assessment (formerly self-attestation for smaller users) |
| **Applies to** | All SWIFT users: banks, brokers, custodians, corporates, service bureaux |
| **Consequence of non-compliance** | Counterparty notifications; potential suspension; regulatory escalation |

---

## Architecture Types

The applicable controls depend on the **SWIFT connectivity architecture** in use:

| Type | Description | Typical User |
|------|-------------|-------------|
| **A1** | Customer connector, customer-managed, software-based (Alliance Access/Gateway on-premises) | Large banks, broker-dealers |
| **A2** | Customer connector, customer-managed, hardware-based (HSM-based — rare) | Banks with HSM-based keys |
| **A3** | Customer connector, SWIFT-managed (SWIFT Alliance Lite2 / SWIFT-hosted component) | Mid-tier banks, asset managers |
| **A4** | SWIFT-defined cloud (cloud-based SWIFT connectivity via SWIFT Cloud) | Cloud-native FIs |
| **B** | Service bureau — direct SWIFT connection managed by a third party | Smaller banks using bureaux |

> **Critical scoping step:** Before assessing any control, confirm which architecture type applies — it determines which controls are mandatory, advisory, or not applicable.

---

## The Three Security Objectives

### Objective 1 — Secure Your Environment (Controls 1.x and 2.x and 3.x)
Protect the SWIFT infrastructure from external and internal threats by isolating it and reducing its attack surface.

### Objective 2 — Know and Limit Access (Controls 4.x and 5.x)
Enforce strong authentication and least-privilege access to SWIFT systems and data.

### Objective 3 — Detect and Respond (Controls 6.x and 7.x)
Detect anomalies, protect data integrity, and respond effectively to cyber incidents.

---

## Control Summary Table (CSCF v2025)

| Control | Name | Status | Objective |
|---------|------|--------|-----------|
| **1.1** | SWIFT Environment Protection | Mandatory | 1 |
| **1.2** | OS Privileged Account Control | Mandatory | 1 |
| **1.3A** | Virtualisation Platform Security | Advisory | 1 |
| **1.4** | Restriction of Internet Access | Mandatory | 1 |
| **1.5A** | Customer Environment Protection | Advisory | 1 |
| **2.1** | Internal Data Flow Security | Mandatory | 1 |
| **2.2** | Security Updates | Mandatory | 1 |
| **2.3** | System Hardening | Mandatory | 1 |
| **2.4A** | Back-Office Data Flow Security | Advisory | 1 |
| **2.5A** | External Transmission Data Protection | Advisory | 1 |
| **2.6** | Operator Session Confidentiality and Integrity | Mandatory | 1 |
| **2.7** | Vulnerability Scanning | Mandatory | 1 |
| **2.8** | Critical Activity Outsourcing | Mandatory | 1 |
| **2.9A** | Transaction Business Controls | Advisory | 1 |
| **2.10** | Application Hardening | Mandatory | 1 |
| **2.11A** | RMA Business Controls | Advisory | 1 |
| **3.1** | Physical Security | Mandatory | 1 |
| **4.1** | Password Policy | Mandatory | 2 |
| **4.2** | Multi-Factor Authentication | Mandatory | 2 |
| **5.1** | Logical Access Controls | Mandatory | 2 |
| **5.2** | Token Management | Mandatory | 2 |
| **5.3A** | Staffing | Advisory | 2 |
| **5.4** | Physical and Logical Password Storage | Mandatory | 2 |
| **6.1** | Malware Protection | Mandatory | 3 |
| **6.2** | Software Integrity | Mandatory | 3 |
| **6.3** | Database Integrity | Mandatory | 3 |
| **6.4** | Log and Monitoring | Mandatory | 3 |
| **6.5A** | Intrusion Detection | Advisory | 3 |
| **7.1** | Cyber Incident Response Planning | Mandatory | 3 |
| **7.2** | Security Training and Awareness | Mandatory | 3 |
| **7.3A** | Penetration Testing | Advisory | 3 |
| **7.4A** | Scenario Risk Assessment | Advisory | 3 |

*(A = Advisory control)*

---

## How to Respond

Match your output to the task type:

| Task | Output Format |
|------|--------------|
| Gap assessment | Table: Control ID | Control Name | Status (🔴/🟡/🟢) | Evidence Required | Gap Notes |
| Architecture scoping | Table mapping architecture type to applicable controls |
| Control deep-dive | Structured narrative: Purpose → Requirement → Implementation steps → Evidence artifacts |
| KYC-SA attestation prep | Checklist by control with attestation status and evidence pointers |
| Incident response | Step-by-step procedure with SWIFT notification obligations |
| Cross-framework mapping | Side-by-side table (CSCF ↔ ISO 27001 / PCI DSS / NIST CSF) |

Always cite the specific **control number** (e.g., 4.2, 6.4) — not just the control name.

---

## Key Implementation Priorities

The following controls are the **highest-risk** and most commonly cited in SWIFT assessments:

1. **4.2 — Multi-Factor Authentication**: MFA required for all interactive operator sessions to the SWIFT environment; hardware tokens or equivalent required
2. **1.1 — SWIFT Environment Protection**: Dedicated secure zone; no browsing from SWIFT servers; network segregation with firewall rules
3. **6.4 — Log and Monitoring**: All SWIFT system events and transactions logged; anomaly alerts; minimum 1-year retention
4. **2.2 — Security Updates**: Patches applied within 90 days for critical; emergency patches within 3 days
5. **6.2 — Software Integrity**: Verify integrity of SWIFT software before installation and after updates
6. **2.3 — System Hardening**: CIS Benchmark hardening or equivalent; remove all unnecessary services
7. **1.4 — Internet Restriction**: SWIFT infrastructure must not have direct internet access; jump servers required

---

## Annual Assessment and Attestation Timeline

| Activity | Timing |
|----------|--------|
| Assessment period begins | January 1 |
| Independent assessment completed | By end of Q2 |
| KYC-SA attestation submitted | By July 31 annually |
| Counterparty visibility of attestation | Immediately upon submission |
| Non-attesting user flagged to counterparties | After deadline |

---

## Common Findings and Remediation

| Control | Common Finding | Remediation |
|---------|---------------|-------------|
| 4.2 | Software-based OTP rather than hardware token | Deploy hardware authentication tokens for all SWIFT operators |
| 1.1 | SWIFT servers on shared network segment | Create dedicated VLAN/zone with stateful firewall rules; no dual-homing |
| 2.2 | Critical patches >90 days overdue | Establish patch management process with SLAs: critical=3 days, high=90 days |
| 6.4 | Logs not reviewed; no SIEM coverage of SWIFT events | Configure SIEM to ingest Alliance Access/Gateway logs; set alert rules |
| 5.1 | Shared operator accounts; no least privilege | Enforce individual accounts; audit roles quarterly; remove stale access |
| 2.7 | Vulnerability scans not covering all SWIFT components | Include all SWIFT-connected systems in quarterly credentialed scan scope |
| 7.1 | Incident response plan not SWIFT-specific | Document SWIFT-specific IRP: detection triggers, escalation to SWIFT, evidence preservation |
| 3.1 | Server room access not logged | Implement card access with audit trail; restrict to named individuals |

---

## Reference Files

For deeper content, read these files as needed:
- **references/swift-controls.md** — All 31 controls with full implementation requirements, evidence artifacts, and architecture applicability by type (A1/A2/A3/A4/B)
- **references/swift-assessment.md** — KYC-SA attestation process, independent assessor requirements, CSCF v2024→v2025 changes, cross-framework mapping (ISO 27001, PCI DSS, NIST CSF), and SWIFT-specific incident reporting obligations
