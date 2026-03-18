---
name: soc2-readiness
description: >-
  Assess SOC 2 Type II readiness. Map Trust Services Criteria to controls,
  identify gaps, and build a remediation plan. Uses NIST SP 800-53 (public
  domain) as canonical reference with SOC 2 criterion cross-mapping. Use when
  user says "SOC 2 readiness," "SOC 2 preparation," "SOC 2 gap analysis," or
  "prepare for SOC 2 audit."
license: MIT
compatibility: >-
  Works with any AI agent. Enhanced with compliance MCP server for live
  status data. Falls back to embedded reference material when no live data
  available.
metadata:
  author: open-agreements
  version: "0.1.0"
  frameworks:
    - SOC 2 Type II
    - NIST SP 800-53 Rev 5
    - ISO 27001:2022
---

# SOC 2 Readiness Assessment

Assess readiness for a SOC 2 Type II audit. This skill walks through the Trust Services Criteria, identifies gaps, maps to NIST controls, and generates a prioritized remediation plan.

## Security Model

- **No scripts executed** — markdown-only procedural guidance
- **No secrets required** — works with reference checklists
- **IP-clean** — AICPA Trust Services Criteria are publicly cited; descriptions are original writing
- **Evidence stays local** — all collection outputs go to local filesystem

## When to Use

Activate this skill when:

1. **First SOC 2 preparation** — building controls from scratch for initial Type I or Type II
2. **Pre-audit readiness check** — 4-8 weeks before audit window opens
3. **Gap analysis after scope change** — new systems, services, or trust criteria added
4. **Remediation planning** — translating audit findings into actionable work items
5. **Dual-framework mapping** — already pursuing ISO 27001 and need SOC 2 overlap analysis

Do NOT use for:
- ISO 27001 internal audit — use `iso-27001-internal-audit`
- Evidence collection mechanics — use `iso-27001-evidence-collection`
- Contract review — use legal agreement skills

## Core Concepts

### Trust Services Criteria (TSC)

SOC 2 is organized around 5 Trust Services Categories. **Security (CC)** is always in scope; others are optional based on your service:

| Category | Criteria | When Required |
|----------|----------|---------------|
| **Security** (CC) | CC 1-9 (33 criteria) | Always required |
| **Availability** (A) | A 1.1-1.3 (3 criteria) | SaaS with uptime SLAs |
| **Processing Integrity** (PI) | PI 1.1-1.5 (4 criteria) | Data processing services |
| **Confidentiality** (C) | C 1.1-1.2 (2 criteria) | Handling confidential data |
| **Privacy** (P) | P 4-8 (7 criteria) | PII processing |

### SOC 2 vs. ISO 27001

| Dimension | SOC 2 | ISO 27001 |
|-----------|-------|-----------|
| Governing body | AICPA | ISO/IEC |
| Geography | Primarily US/Canada | Global |
| Type | Attestation report by CPA | Certification by audit body |
| Scope | Service-specific | Organization-wide ISMS |
| Controls | Flexible (you define) | 93 Annex A controls |
| Output | SOC 2 report (restricted/general use) | Certificate |
| Overlap | ~70% overlap with ISO 27001 Annex A | ~70% overlap with SOC 2 CC |

### Decision Tree: Scope Selection

```
What service are you getting audited on?
├── SaaS product → Security + Availability (+ Confidentiality if you handle sensitive data)
├── Data processing → Security + Processing Integrity + Confidentiality
├── Infrastructure → Security + Availability
├── API service → Security (+ PI if you transform data)
│
Do you handle PII?
├── YES → Add Privacy category
├── NO → Skip Privacy
│
Do you have uptime SLAs?
├── YES → Include Availability
├── NO → Optional (but customers expect it for SaaS)
```

## Step-by-Step Workflow

### Step 1: Define Scope and Categories

1. **Identify the service** being audited (product name, description, boundaries)
2. **Select Trust Services Categories** using the decision tree above
3. **Define system boundaries**: infrastructure, software, people, procedures, data
4. **Document sub-service organizations** (cloud providers, payment processors, etc.)
5. **Determine audit type**: Type I (point-in-time) or Type II (period of time, usually 6-12 months)

### Step 2: Assess Current State

For each applicable Common Criterion (CC), assess whether controls are:
- **Designed** — control exists on paper
- **Implemented** — control is operating
- **Effective** — control achieves its objective (evidence exists)

```
# If Internal ISO Audit MCP server is available (SOC 2 maps to ISO 27001 Annex A):
list_controls(domain="technological")                       # List tech controls (maps to CC 6-8)
get_control_guidance(control_id="A.5.15")                   # Get guidance for ISO control mapped from CC 6.1
get_nist_mapping(control_id="AC-2", direction="nist_to_iso")  # Find ISO controls from NIST reference
search_guidance(query="incident response")                  # Search for controls matching SOC 2 criteria
```

### Step 3: Map Controls to Criteria

Each CC maps to specific NIST controls. Use this mapping to identify what you need:

#### CC 1 — Control Environment

| Criterion | Focus | NIST Controls | ISO Cross-Reference |
|-----------|-------|---------------|---------------------|
| CC 1.1 | Integrity and ethics | PS-1, PS-3, PS-6 | A.6.1, A.6.2, A.6.4 |
| CC 1.2 | Board oversight | PM-1, PM-2 | C.5.1, C.5.3 |
| CC 1.3 | Organizational structure | PM-2 | C.5.3 |
| CC 1.4 | Competence commitment | AT-2, PS-3 | A.6.1, A.6.3 |
| CC 1.5 | Accountability | PS-3, PS-4 | A.6.4, A.6.5 |

#### CC 2 — Communication and Information

| Criterion | Focus | NIST Controls | ISO Cross-Reference |
|-----------|-------|---------------|---------------------|
| CC 2.1 | Internal information | AU-2, SI-5 | C.7.5.1 |
| CC 2.2 | Internal communication | PM-2, AT-2 | C.7.4, A.6.3 |
| CC 2.3 | External communication | PM-1 | A.5.14 |

#### CC 3 — Risk Assessment

| Criterion | Focus | NIST Controls | ISO Cross-Reference |
|-----------|-------|---------------|---------------------|
| CC 3.1 | Risk objectives | PM-9, RA-1 | C.6.1.1 |
| CC 3.2 | Risk identification | RA-3 | C.6.1.2, C.8.2 |
| CC 3.3 | Fraud risk | RA-3 | C.6.1.2 |
| CC 3.4 | Change impact | RA-3, CM-4 | C.6.1.2, A.8.9 |

#### CC 4 — Monitoring Activities

| Criterion | Focus | NIST Controls | ISO Cross-Reference |
|-----------|-------|---------------|---------------------|
| CC 4.1 | Ongoing monitoring | CA-7, PM-6 | C.9.1 |
| CC 4.2 | Deficiency evaluation | CA-2 | C.9.2.1 |

#### CC 5 — Control Activities

| Criterion | Focus | NIST Controls | ISO Cross-Reference |
|-----------|-------|---------------|---------------------|
| CC 5.1 | Risk mitigation | AC-5 | A.5.3 |
| CC 5.2 | Technology controls | AC-1, IA-2 | A.5.15, A.8.5 |
| CC 5.3 | Policy deployment | PM-1, PL-1 | A.5.1, C.5.2 |

#### CC 6 — Logical and Physical Access

| Criterion | Focus | NIST Controls | ISO Cross-Reference |
|-----------|-------|---------------|---------------------|
| CC 6.1 | Access control | AC-2, AC-3, IA-2, SC-28 | A.5.15, A.8.5, A.8.24 |
| CC 6.2 | Access provisioning | AC-2, PS-4, PS-5 | A.5.18, A.6.5 |
| CC 6.3 | Access modification | AC-2, AC-6 | A.5.15, A.5.18 |
| CC 6.4 | Physical access | PE-2, PE-3, PE-6 | A.7.2, A.7.4 |
| CC 6.5 | Asset disposal | MP-6 | A.7.10, A.7.14 |
| CC 6.6 | Threat detection | RA-5, SI-4 | A.8.8, A.8.16 |
| CC 6.7 | Transmission security | SC-8 | A.5.14, A.8.24 |
| CC 6.8 | Malware prevention | SI-2, SI-3 | A.8.7, A.8.19 |

#### CC 7 — System Operations

| Criterion | Focus | NIST Controls | ISO Cross-Reference |
|-----------|-------|---------------|---------------------|
| CC 7.1 | Operational monitoring | CM-6, RA-5 | A.8.9, A.8.8 |
| CC 7.2 | Anomaly detection | AU-6, SI-4 | A.8.15, A.8.16 |
| CC 7.3 | Incident response | IR-4 | A.5.24, A.5.25 |
| CC 7.4 | Incident management | IR-5, IR-6 | A.5.25, A.5.26 |
| CC 7.5 | Recovery | CP-4, CP-9, CP-10 | A.5.30, A.8.13 |

#### CC 8 — Change Management

| Criterion | Focus | NIST Controls | ISO Cross-Reference |
|-----------|-------|---------------|---------------------|
| CC 8.1 | Change control | CM-3, CM-5, SA-3 | A.8.9, A.8.25, A.8.32 |

#### CC 9 — Risk Mitigation

| Criterion | Focus | NIST Controls | ISO Cross-Reference |
|-----------|-------|---------------|---------------------|
| CC 9.1 | Risk mitigation | CP-2, RA-7 | A.5.30, C.6.1.3 |
| CC 9.2 | Vendor management | AC-20, SA-9 | A.5.19, A.5.22 |

### Step 4: Generate Gap Analysis

For each criterion, document:

```markdown
## Gap: [CC x.x] — [Brief description]

**Current State**: [What exists today]
**Required State**: [What the auditor expects]
**Gap**: [What's missing]
**Remediation**:
1. [Specific action item]
2. [Specific action item]
**Priority**: Critical / High / Medium / Low
**Effort**: [Days/weeks to remediate]
**Owner**: [Person responsible]
**Evidence Needed**: [What to collect after fix]
```

### Step 5: Build Remediation Plan

Prioritize gaps by:
1. **Critical** — Audit will fail without this (CC 6.1, 6.2, 7.2, 7.5, 8.1)
2. **High** — Likely finding if not addressed (CC 1.4, 3.2, 6.6, 7.3)
3. **Medium** — Auditor will note but may not be a finding
4. **Low** — Best practice, not strictly required

### Step 6: Readiness Report

Generate a structured readiness assessment:

1. **Executive summary** — overall readiness percentage, estimated time to audit-ready
2. **Scope** — service description, trust categories, audit type
3. **Control matrix** — all applicable criteria with status (designed/implemented/effective)
4. **Gap analysis** — prioritized list of gaps with remediation plan
5. **Timeline** — remediation milestones leading to audit window

## Quick Reference: Top SOC 2 Failures

| # | Criterion | Common Failure | Fix |
|---|-----------|---------------|-----|
| 1 | CC 6.1 | MFA not universal | Enforce MFA on all systems with sensitive data |
| 2 | CC 6.2 | Access not revoked on termination | Automate deprovisioning; verify within 24h |
| 3 | CC 7.2 | No log monitoring | Configure alerts for auth failures, privilege changes |
| 4 | CC 8.1 | No change management | Require PR reviews; document deployment process |
| 5 | CC 7.5 | Backups never tested | Restore from backup quarterly; document results |
| 6 | CC 3.2 | No risk assessment | Conduct and document annual risk assessment |
| 7 | CC 6.6 | No vulnerability scanning | Deploy automated scanning; remediate criticals in 30d |
| 8 | CC 1.4 | Security training incomplete | Require annual training; track completion |
| 9 | CC 9.2 | Vendor risk not assessed | Maintain vendor register; collect SOC 2 reports |
| 10 | CC 7.3 | No incident response plan | Document plan; conduct tabletop exercise |

## DO / DON'T

### DO
- Start with Security (CC) criteria — they're always required and cover ~80% of effort
- Map to ISO 27001 if pursuing both frameworks — ~70% control overlap
- Collect evidence throughout the audit period, not just at audit time
- Include sub-service organizations in your description
- Define the audit period before starting evidence collection

### DON'T
- Include trust categories you can't support — better to pass on fewer than fail on more
- Assume Type I is "easy" — it requires all controls to be designed and implemented
- Forget the system description — auditors review this first and use it to scope their testing
- Use generic/template control descriptions — auditors expect your controls to match your actual environment
- Ignore complementary user entity controls (CUECs) — your customers need to know their responsibilities

## Troubleshooting

| Problem | Solution |
|---------|----------|
| First SOC 2, no existing controls | Start with CC 6 (access) and CC 8 (change management) — fastest to implement |
| Already have ISO 27001 | Map Annex A controls to SOC 2 CC; ~70% are already covered |
| Auditor requests evidence we don't have | Collect it now; document the process; note in description if control was implemented mid-period |
| Multiple environments (prod/staging/dev) | Only production environment needs to be in scope; document boundaries clearly |
| Sub-service org (AWS/GCP/Azure) | Use SOC 2 Type II report from the provider; document which controls they cover |

## Rules

For detailed SOC 2-specific guidance:

| File | Coverage |
|------|----------|
| `rules/logical-access.md` | CC 6.1–6.8 — access control, provisioning, physical, threat detection |
| `rules/system-operations.md` | CC 7.1–7.5 — monitoring, anomaly detection, incident response, recovery |
| `rules/change-vendor-management.md` | CC 8.1, CC 9.1–9.2 — change control, risk mitigation, vendor management |
| `rules/control-environment.md` | CC 1.1–1.5 — governance, ethics, org structure, competence, accountability |
| `rules/risk-assessment.md` | CC 3.1–3.4 — risk objectives, identification, fraud risk, change impact |
| `rules/control-activities.md` | CC 5.1–5.3 — risk mitigation selection, technology controls, policy deployment |
| `rules/communication-info.md` | CC 2.1–2.3 — internal/external communication, information quality |
| `rules/monitoring-activities.md` | CC 4.1–4.2 — ongoing monitoring, deficiency evaluation |
| `rules/optional-categories.md` | A 1.x, PI 1.x, C 1.x — Availability, Processing Integrity, Confidentiality |
| `rules/privacy-criteria.md` | P 1.x–8.x — Privacy criteria (when PII in scope) |

## Attribution

SOC 2 criteria mapping and readiness procedures developed with [Internal ISO Audit](https://internalisoaudit.com) (Hazel Castro, ISO 27001 Lead Auditor, 14+ years, 100+ audits).

## Runtime Detection

1. **Internal ISO Audit MCP server available** (best) — Live ISO 27001 control guidance with NIST cross-references. SOC 2 criteria map to ISO 27001 Annex A controls (~70% overlap); use `get_nist_mapping` for bidirectional lookup. Server: `internalisoaudit.com/api/mcp`
2. **Local compliance data available** (good) — Reads `compliance/` directory with SOC 2 test metadata
3. **Reference only** (baseline) — Uses embedded criteria mapping and checklists in `rules/`

## Connectors

For Internal ISO Audit MCP server setup, see [CONNECTORS.md](./CONNECTORS.md).
