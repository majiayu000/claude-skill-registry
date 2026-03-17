---
name: compliance-audit
description: >-
  Regulatory compliance auditing across GDPR, HIPAA, PCI DSS, SOC 2, and ISO
  frameworks with automated evidence collection and gap analysis. Use when
  conducting compliance assessments, preparing for certifications, or
  implementing regulatory controls.
version: 1.0.0
tags: [compliance, audit, regulatory, security, privacy]
triggers:
  - compliance audit
  - regulatory assessment
  - GDPR compliance
  - HIPAA assessment
  - PCI DSS certification
  - SOC 2 readiness
  - ISO 27001 alignment
  - evidence collection
  - gap analysis
dependencies:
  skills: [secure-coding-practices, owasp-top-10]
  tools: [Read, Write, Bash, Grep, Glob]
token_estimate: ~3000
---

# Compliance Audit

Systematic regulatory compliance auditing with automated evidence collection, control mapping,
gap analysis, and remediation planning across major compliance frameworks.

## When to Use This Skill

- Conducting compliance assessments for GDPR, HIPAA, PCI DSS, SOC 2, or ISO 27001
- Preparing for external audits or certifications
- Building or validating compliance control frameworks
- Automating evidence collection and audit trail maintenance
- Performing gap analysis against regulatory requirements
- Creating remediation plans for compliance deficiencies
- Evaluating third-party vendor compliance posture

## Quick Reference

| Resource | Purpose | Load when |
|----------|---------|-----------|
| `references/frameworks.md` | Key requirements, control mappings, and certification paths for GDPR, HIPAA, PCI DSS, SOC 2, ISO 27001 | Scoping which regulations apply |
| `references/evidence-collection.md` | Automated evidence gathering, artifact organization, retention policies, audit trail patterns | Setting up or running evidence collection |
| `references/gap-analysis.md` | Control mapping methodology, gap identification, risk scoring, remediation planning | Analyzing compliance gaps |

---

## Workflow Overview

```
Phase 1: Scope       → Identify applicable regulations, data types, and geographical scope
Phase 2: Assess      → Map controls, review policies, analyze data flows, test implementations
Phase 3: Evidence    → Collect and organize audit artifacts automatically
Phase 4: Gap Analyze → Identify control gaps, score risks, prioritize findings
Phase 5: Remediate   → Create remediation plans, assign owners, set timelines
Phase 6: Report      → Generate audit-ready documentation and compliance dashboards
Phase 7: Monitor     → Establish continuous compliance monitoring and drift detection
```

---

## Phase 1: Scope the Audit

Determine the regulatory landscape before testing anything.

**Key questions:**
- What data types does the system process (PII, PHI, cardholder data)?
- What jurisdictions apply (EU, US states, industry-specific)?
- What existing controls and certifications are in place?
- What is the audit history and any prior findings?

**Applicability matrix:**

| Framework | Applies when |
|-----------|-------------|
| GDPR | Processing personal data of EU residents |
| HIPAA | Handling protected health information (PHI) |
| PCI DSS | Storing, processing, or transmitting cardholder data |
| SOC 2 | Providing services where trust principles matter |
| ISO 27001 | Organization wants certified ISMS |
| CCPA/CPRA | Collecting California consumer personal information |
| NIST CSF | Federal systems or voluntary cybersecurity framework adoption |

---

## Phase 2: Assess Current State

### Control Inventory

Map existing controls against the applicable framework requirements:

1. Enumerate all technical controls (encryption, access control, logging)
2. Enumerate all administrative controls (policies, training, procedures)
3. Enumerate all physical controls (facility access, media handling)
4. Map each control to specific framework requirements
5. Test control effectiveness through sampling and verification

### Data Flow Analysis

- Map data ingress, processing, storage, and egress points
- Identify data classification for each flow
- Document lawful basis for processing (GDPR)
- Verify data minimization and purpose limitation
- Review cross-border transfer mechanisms

### Policy Review

- Assess policy coverage against framework requirements
- Verify policy distribution and acknowledgment
- Check policy version control and update cadence
- Validate exception management processes

---

## Phase 3: Evidence Collection

Load `references/evidence-collection.md` for detailed patterns.

**Automation priorities:**
1. Configuration exports from cloud providers and infrastructure
2. Access control lists and permission matrices
3. Log retention and monitoring dashboards
4. Vulnerability scan results and patch status
5. Training completion records
6. Incident response test results

**Artifact organization:**

```
evidence/
  {framework}/
    {control-id}/
      artifact-{date}.{ext}
      metadata.yaml           # source, collection method, timestamp
```

---

## Phase 4: Gap Analysis

Load `references/gap-analysis.md` for the full methodology.

For each framework requirement:
1. Map to existing controls (full, partial, or none)
2. Assess implementation effectiveness
3. Score the gap by risk impact and likelihood
4. Categorize as documentation, process, technology, or training gap
5. Prioritize based on risk score and remediation effort

---

## Phase 5: Remediation Planning

For each identified gap:

| Field | Content |
|-------|---------|
| Gap ID | Unique identifier |
| Framework Requirement | Specific clause or control |
| Current State | What exists today |
| Target State | What compliance requires |
| Remediation Action | Specific steps to close the gap |
| Owner | Responsible person/team |
| Priority | P0-P4 based on risk score |
| Timeline | Target completion date |
| Dependencies | Other gaps or actions this depends on |

---

## Phase 6: Reporting

Generate audit-ready documentation:

- **Executive summary**: Compliance posture, key risks, readiness score
- **Technical findings**: Detailed control assessment results
- **Risk matrix**: Heat map of gaps by severity and likelihood
- **Remediation roadmap**: Prioritized timeline with owners
- **Evidence package**: Organized artifacts indexed to controls
- **Compliance attestation**: Framework-specific certification readiness

---

## Phase 7: Continuous Monitoring

Establish ongoing compliance posture management:

- Configure automated scanning for drift detection
- Set alert thresholds for control degradation
- Schedule periodic re-assessment cadence
- Track remediation progress against timelines
- Maintain metric dashboards (control coverage, evidence freshness, audit readiness)

---

## Core Principles

1. **Evidence over assertion** — every compliance claim must be backed by verifiable artifacts
2. **Automate first** — manual evidence collection does not scale and introduces errors
3. **Risk-based prioritization** — address the highest-risk gaps first
4. **Continuous posture** — compliance is a state, not a one-time event
5. **Defense in depth** — layer controls so single-point failures do not cause non-compliance

## Anti-Patterns

- Treating compliance as a checkbox exercise without testing control effectiveness
- Collecting evidence manually when automation is available
- Ignoring gaps because "we've always done it this way"
- Waiting until audit season to gather evidence
- Conflating compliance with security (compliance is a subset)
- Skipping third-party/vendor compliance assessments
