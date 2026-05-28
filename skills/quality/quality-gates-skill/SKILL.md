---
document_name: "quality-gates.skill.md"
location: ".claude/skills/quality-gates.skill.md"
codebook_id: "CB-SKILL-QUALGATE-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for quality gate definition and enforcement"
skill_metadata:
  category: "quality"
  complexity: "intermediate"
  estimated_time: "varies"
  prerequisites:
    - "Quality metrics"
category: "skills"
status: "active"
tags:
  - "skill"
  - "quality"
  - "gates"
ai_parser_instructions: |
  This skill defines procedures for quality gates.
---

# Quality Gates Skill

=== PURPOSE ===

Procedures for defining and enforcing quality gates.

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(qa-lead) @ref(CB-AGENT-QA-001) | Primary skill for quality gates |

=== PROCEDURE: Gate Definition ===

**Standard Gates:**

| Gate | Metric | Threshold | Enforcement |
|------|--------|-----------|-------------|
| Coverage | Line coverage | ≥80% | CI/CD |
| Tests | All pass | 100% | CI/CD |
| Linting | No errors | 0 | CI/CD |
| Types | No errors | 0 | CI/CD |
| Security | No critical | 0 | Security Lead |
| Quality | No blockers | 0 | QA Lead |

=== PROCEDURE: Gate Failure ===

**Steps:**
1. Identify failing gate
2. Document failure reason
3. Block PR/deployment
4. Notify responsible party
5. Track remediation

=== PROCEDURE: Gate Exceptions ===

Exceptions require:
- Written justification
- Head Cook approval
- Remediation timeline
- Buildlog entry with `#micro-decision`

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(testing-strategy) | Testing context |
| @skill(quality-review) | Review context |
