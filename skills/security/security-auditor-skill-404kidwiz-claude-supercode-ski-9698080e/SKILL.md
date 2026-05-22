---
name: security-auditor
description: Expert in compliance frameworks (SOC2, ISO 27001), automated auditing, and risk management.
---

# Security Auditor

## Purpose

Provides security compliance and audit expertise specializing in SOC 2, ISO 27001, and regulatory frameworks. Evaluates organizational security posture through automated evidence collection, gap analysis, and audit preparation.

## When to Use

- Preparing for a SOC 2 Type I or Type II audit
- Aligning infrastructure with ISO 27001 / HIPAA / PCI-DSS standards
- Automating evidence collection (Drata, Vanta, Secureframe)
- Conducting a Third-Party Risk Assessment (Vendor Review)
- Performing a Cloud Security Posture Review (CSPM)
- Designing internal audit programs

## Examples

### Example 1: SOC 2 Type II Preparation

**Scenario:** A SaaS startup preparing for their first SOC 2 Type II audit.

**Implementation:**
1. Conducted gap analysis against SOC 2 criteria
2. Designed and implemented 45 security controls
3. Automated evidence collection for all criteria
4. Created comprehensive documentation package
5. Ran 3 months of observation period

**Results:**
- Passed SOC 2 Type II with zero non-conformities
- Audit duration reduced from 6 months to 3 months
- Evidence collection automated (90% less manual effort)
- Customer confidence increased significantly

### Example 2: ISO 27001 Implementation

**Scenario:** An enterprise implementing ISO 27001 for market access.

**Implementation:**
1. Conducted risk assessment following ISO methodology
2. Created Statement of Applicability (SoA)
3. Implemented 82 controls from Annex A
4. Established ISMS governance structure
5. Conducted internal audit and management review

**Results:**
- ISO 27001 certification achieved in 8 months
- Security posture improved across organization
- Access to new markets requiring certification
- Insurance premiums reduced by 15%

### Example 3: Third-Party Risk Assessment

**Scenario:** Assessing 100+ vendors for security and compliance.

**Implementation:**
1. Developed tiered assessment approach by risk criticality
2. Created standardized security questionnaire
3. Implemented continuous monitoring for critical vendors
4. Established vendor risk scoring methodology
5. Created remediation tracking and escalation

**Results:**
- 100% vendors assessed
- 12 high-risk vendors requiring remediation
- Clear risk appetite established for vendors
- Vendor-related security incidents reduced by 80%

## Best Practices

### Audit Preparation

- **Early Start**: Begin preparation 6+ months before audit
- **Gap Analysis**: Understand current state vs. requirements
- **Control Design**: Implement controls before trying to operate them
- **Automation**: Automate evidence collection where possible

### Evidence Management

- **Continuous Collection**: Don't wait for audit to collect evidence
- **Centralized Storage**: Organized evidence repository
- **完整性**: Ensure evidence accuracy and completeness
- **Accessibility**: Easy to retrieve and present

### Control Testing

- **Operating Effectiveness**: Test that controls work as designed
- **Sample Size**: Appropriate sampling methodology
- **Documentation**: Clear testing procedures and results
- **Remediation**: Track and resolve control deficiencies

### Compliance Monitoring

- **Continuous**: Monitor compliance, not just at audit time
- **Metrics**: Track compliance KPIs
- **Trends**: Identify patterns and emerging issues
- **Reporting**: Regular compliance status updates

---
---

## 2. Decision Framework

### Compliance Framework Selection

```
What is the business goal?
│
├─ **B2B SaaS Sales?**
│  ├─ US Market? → **SOC 2** (Trust Services Criteria)
│  └─ International? → **ISO 27001** (ISMS)
│
├─ **Regulated Industry?**
│  ├─ Healthcare (US)? → **HIPAA**
│  ├─ Payments? → **PCI-DSS**
│  └─ EU Personal Data? → **GDPR**
│
└─ **Federal/Gov?**
   ├─ US Federal? → **FedRAMP**
   └─ Defense? → **CMMC**
```

### Audit Strategy

| Type | Frequency | Depth | Output |
|------|-----------|-------|--------|
| **Gap Analysis** | Once (Start) | High (Design) | Remediation Roadmap |
| **Internal Audit** | Quarterly | Medium (Sampling) | Internal Report & CAPA |
| **Continuous** | Real-time | High (Automated) | Dashboard / Alerts |
| **External Audit** | Annual | High (Evidence) | Attestation Report |

**Red Flags → Escalate to `security-engineer` or `legal-advisor`:**
- "Just check the box" mentality (Security theater)
- Storing evidence in personal drives (Chain of custody risk)
- Falsifying evidence (Fraud)
- Missing legal basis for data processing (GDPR violation)

---
---

## 3. Core Workflows

### Workflow 1: SOC 2 Readiness Assessment

**Goal:** Identify gaps before the external auditor arrives.

**Steps:**

1.  **Scope Definition**
    -   Define the "System Description".
    -   Identify Trust Services Criteria (TSC): Security (Mandatory), Availability, Confidentiality, Processing Integrity, Privacy.

2.  **Control Mapping**
    -   *Control:* "Change Management".
    -   *Evidence Needed:* PRs require approval, CI/CD logs.
    -   *Current State:* "Developers push to main." → **GAP**.

3.  **Remediation Plan**
    -   Task: Enable "Branch Protection" on GitHub.
    -   Task: Implement SSO (Okta/Google Workspace).
    -   Task: Encrypt database at rest (AWS RDS KMS).

4.  **Policy Generation**
    -   Draft "Information Security Policy".
    -   Draft "Incident Response Plan".
    -   Draft "Access Control Policy".

---
---

### Workflow 3: Vendor Risk Assessment

**Goal:** Approve a new sub-processor (e.g., AI API provider).

**Steps:**

1.  **Intake**
    -   Request: "We want to use OpenAI API."
    -   Data Classification: "Confidential (Customer PII)".

2.  **Review**
    -   Request SOC 2 Type II report from vendor.
    -   Review "Bridge Letter" (if report is old).
    -   Review "Exceptions" in the report (Did they fail anything?).

3.  **Decision**
    -   **Approve:** Risks managed.
    -   **Mitigate:** "Yes, but turn off data retention option."
    -   **Reject:** "Security posture insufficient for PII."

---
---

## 5. Anti-Patterns & Gotchas

### ❌ Anti-Pattern 1: "Set and Forget" Compliance

**What it looks like:**
-   Passing the audit in January.
-   Disabling security controls in February to "move faster".
-   Panicking next December.

**Why it fails:**
-   Type II audits cover a *period of time* (e.g., Jan 1 - Dec 31).
-   Auditor will ask for samples from July. You will fail.

**Correct approach:**
-   **Continuous Compliance:** Treat compliance as a product feature. Monitor daily.

### ❌ Anti-Pattern 2: Over-Scoping

**What it looks like:**
-   Including the "Marketing Website" (Wordpress) in the SOC 2 scope for the "Banking App".

**Why it fails:**
-   Wasted effort securing non-critical assets.
-   Audit becomes expensive and slow.

**Correct approach:**
-   **Network Segmentation:** Isolate the CDE (Cardholder Data Environment) or Prod environment. Scope *only* the critical environment.

### ❌ Anti-Pattern 3: Manual Screenshots

**What it looks like:**
-   Taking 500 screenshots of Jira tickets to prove "Change Management".

**Why it fails:**
-   Unmaintainable.
-   Screenshots can be faked.

**Correct approach:**
-   **Export Logs:** JSON/CSV exports from systems.
-   **Read-only Access:** Give the auditor read-only access to the tool (Jira/AWS) to verify themselves.

---
---

## 7. Quality Checklist

**Preparation:**
-   [ ] **Scope:** Clearly defined (System Description).
-   [ ] **Controls:** Mapped to framework (SOC 2 / ISO).
-   [ ] **Policies:** Reviewed and approved by management in the last 12 months.

**Evidence:**
-   [ ] **Completeness:** Covers the entire audit period.
-   [ ] **Accuracy:** Generated directly from systems (not manually edited).
-   [ ] **Organization:** Stored in structured folders (e.g., Box/Google Drive/Vanta).

**Vendor Risk:**
-   [ ] **Critical Vendors:** Reviewed annually.
-   [ ] **Contracts:** DPAs (Data Processing Agreements) signed.

**HR Security:**
-   [ ] **Onboarding:** Background checks completed (where legal).
-   [ ] **Offboarding:** Access revoked within SLA (e.g., 24 hours).

## Anti-Patterns

### Audit Process Anti-Patterns

- **Point-in-Time Snapshot**: Assessing controls only at audit time - continuous monitoring
- **Evidence Fabrication**: Creating evidence rather than demonstrating controls - build real compliance
- **Scope Shrinking**: Minimizing audit scope to reduce findings - address root causes
- **Checkbox Mentality**: Treating compliance as form-filling - focus on security outcomes

### Evidence Anti-Patterns

- **Last Minute Rush**: Collecting evidence only when auditors arrive - automate evidence collection
- **Incomplete Evidence**: Partial evidence raising more questions - comprehensive documentation
- **Outdated Evidence**: Using evidence from old systems - maintain current evidence
- **Inaccessible Evidence**: Evidence that can't be located - organize and index systematically

### Control Assessment Anti-Patterns

- **Paper Controls**: Policies only in documentation - implement technical enforcement
- **Over-Complex Controls**: Controls too complex to operate - balance security and operability
- **Control Gaps**: Leaving security domains uncovered - comprehensive control coverage
- **Control Redundancy**: Overlapping controls without coordination - rationalize control portfolio

### Remediation Anti-Patterns

- **Temporary Fixes**: Bandages instead of permanent solutions - implement root cause fixes
- **Finding Chasing**: Prioritizing by audit severity not risk - assess actual business risk
- **Remediation Debt**: Accumulated findings without resolution - maintain remediation backlog
- **Siloed Remediation**: Fixing in isolation without systemic improvement - prevent recurrence
