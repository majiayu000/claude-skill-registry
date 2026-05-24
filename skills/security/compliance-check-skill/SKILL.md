---
document_name: "compliance-check.skill.md"
location: ".claude/skills/compliance-check.skill.md"
codebook_id: "CB-SKILL-COMPLIANCE-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for compliance verification"
skill_metadata:
  category: "security"
  complexity: "advanced"
  estimated_time: "varies"
  prerequisites:
    - "Compliance requirements"
category: "skills"
status: "active"
tags:
  - "skill"
  - "security"
  - "compliance"
ai_parser_instructions: |
  This skill defines procedures for compliance checking.
---

# Compliance Check Skill

=== PURPOSE ===

Procedures for verifying compliance with security standards.

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(security-lead) @ref(CB-AGENT-SECURITY-001) | Primary skill for compliance |

=== PROCEDURE: Compliance Audit ===

**Common Standards:**
- OWASP Top 10
- GDPR (data protection)
- SOC 2 (security controls)
- PCI DSS (payment data)

**Steps:**
1. Identify applicable standards
2. Map requirements to controls
3. Verify implementation
4. Document evidence
5. Report gaps

=== PROCEDURE: Evidence Collection ===

For each control:
- Control description
- Implementation status
- Evidence (screenshots, logs, configs)
- Gap (if any)
- Remediation plan

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(security-review) | Security context |
| @skill(vulnerability-assessment) | Vulnerability context |
