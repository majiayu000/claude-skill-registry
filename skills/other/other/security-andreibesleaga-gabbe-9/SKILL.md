---
name: compliance-review
description: Regulatory compliance check for SOC2, PCI-DSS, GDPR, HIPAA — checklists, audit trails, access controls
triggers: [compliance, SOC2, PCI-DSS, GDPR, audit trail, regulatory, certification, compliance review]
context_cost: high
---

# Compliance Review Skill

## Goal
Verify that the codebase and system configuration meet applicable regulatory requirements. Produce a gap report with specific remediation actions.

## Steps

1. **Identify applicable regulations**
   - Ask if unclear which regulations apply
   - SOC2 Type II: SaaS products, cloud services (trust criteria: security, availability, confidentiality)
   - PCI-DSS: any system handling payment card data
   - GDPR: processing data of EU residents
   - HIPAA: US healthcare data (PHI — Protected Health Information)
   - ISO 27001: general information security management

2. **Run the applicable checklist**

   ### SOC2 Type II — Trust Service Criteria
   ```
   Security (CC6):
   [ ] CC6.1: Logical access controls — only authorized users access systems
   [ ] CC6.2: Authentication mechanisms (MFA for privileged access)
   [ ] CC6.3: Role-based access control (RBAC) implemented
   [ ] CC6.6: Encryption in transit and at rest
   [ ] CC6.7: Change management process (code review + approval workflow)
   [ ] CC6.8: Vulnerability management (regular scanning + patching policy)

   Availability (A1):
   [ ] A1.1: Uptime SLO defined and monitored
   [ ] A1.2: Backup and restore procedures documented and tested
   [ ] A1.3: Incident response plan exists

   Confidentiality (C1):
   [ ] C1.1: Confidential data identified and classified
   [ ] C1.2: Confidential data encrypted at rest
   [ ] C1.3: Data disposal procedure for end-of-lifecycle
   ```

   ### PCI-DSS v4.0 — Key Requirements
   ```
   [ ] Req 1: Firewall/network security controls installed and documented
   [ ] Req 2: No default passwords or vendor-supplied defaults
   [ ] Req 3: Card data (PAN) never stored in plaintext — tokenize or don't store
   [ ] Req 4: Encryption in transit (TLS 1.2+ for cardholder data)
   [ ] Req 6: Secure development policy — SAST/SCA in CI/CD pipeline
   [ ] Req 7: Least privilege access to cardholder data systems
   [ ] Req 8: MFA for all access to cardholder data environment
   [ ] Req 10: Audit log of all access to cardholder data (90 days online, 1 year archived)
   [ ] Req 11: Vulnerability scanning and penetration testing schedule
   [ ] Req 12: Incident response plan for data breach
   ```

   ### HIPAA — Key Safeguards
   ```
   Technical Safeguards:
   [ ] Access controls: unique user IDs, automatic logoff, encryption/decryption of PHI
   [ ] Audit controls: hardware/software activity logs for systems containing PHI
   [ ] Integrity controls: PHI not improperly altered or destroyed (checksums)
   [ ] Transmission security: PHI encrypted in transit

   Administrative Safeguards:
   [ ] Security officer designated
   [ ] Risk analysis documented and current
   [ ] Workforce training on security policies
   [ ] Business associate agreements (BAA) with all PHI processors

   Physical Safeguards:
   [ ] Facility access controls documented
   [ ] Workstation security policy
   ```

3. **Check audit trail completeness**
   - Every mutation of regulated data must be logged with: user ID, timestamp, action, record ID
   - Log format: append-only (no updates or deletes to audit log)
   - Log retention: SOC2/PCI = 90 days online + 1 year archived; HIPAA = 6 years; GDPR = per policy
   - Log access: restricted to security/compliance team only
   - Check: does AUDIT_LOG.md cover all regulated data mutations?

4. **Check access control implementation**
   - Least-privilege: each role has minimum necessary permissions
   - Separation of duties: critical operations require multiple approvals
   - MFA: required for admin access and access to regulated data
   - Access reviews: periodic review of who has access to what

5. **Check incident response plan**
   - Is there a documented incident response procedure?
   - Are breach notification timeframes defined? (GDPR: 72 hours; HIPAA: 60 days)
   - Is there a contact list for regulatory notification?
   - Has the plan been tested (tabletop exercise)?

6. **Generate compliance gap report**
   ```markdown
   ## Compliance Gap Report

   ### Scope: SOC2 Type II
   Date: [date]
   Auditor: [agent/human]

   ### Passed Controls: [N]/[total]

   ### Gaps Found

   #### Critical Gaps (must remediate before certification)
   - CC6.2: MFA not enforced for admin users
     Remediation: Add MFA requirement to admin login flow
     Owner: [team]
     Target date: [date]

   #### High Gaps
   - CC6.8: No documented vulnerability management process
     Remediation: Create security scanning policy, add to CI/CD

   #### Medium Gaps
   - A1.2: Backup restore procedure not documented
     Remediation: Document and test restore procedure

   ### Compliant Controls
   [list controls that passed]

   ### Next Steps
   1. [priority-ordered remediation list]
   ```

## Constraints
- Never dismiss a compliance gap without documented risk acceptance from human
- Audit logs must be verified as actually append-only (not just policy)
- PCI requirements apply to the ENTIRE cardholder data environment — scope carefully
- Compliance gaps in critical categories are blocking for regulated industries

## Output Format
Compliance gap report at `docs/compliance/[regulation]-gap-report.md` with priority-ordered remediation plan.
