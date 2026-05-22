---
document_name: "testing-strategy.skill.md"
location: ".claude/skills/testing-strategy.skill.md"
codebook_id: "CB-SKILL-TESTSTRAT-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for defining testing strategy"
skill_metadata:
  category: "quality"
  complexity: "intermediate"
  estimated_time: "varies"
  prerequisites:
    - "Project requirements"
category: "skills"
status: "active"
tags:
  - "skill"
  - "quality"
  - "testing"
ai_parser_instructions: |
  This skill defines procedures for testing strategy.
---

# Testing Strategy Skill

=== PURPOSE ===

Procedures for defining and implementing testing strategy.

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(qa-lead) @ref(CB-AGENT-QA-001) | Primary skill for testing strategy |

=== PROCEDURE: Test Pyramid ===

**Levels (bottom to top):**
1. **Unit Tests** (70%) - Fast, isolated, many
2. **Integration Tests** (20%) - Component interaction
3. **E2E Tests** (10%) - Full user flows, few

=== PROCEDURE: Coverage Requirements ===

**Thresholds:**
- Line coverage: 80%
- Branch coverage: 75%
- Function coverage: 80%

**Critical Paths:** 100% coverage required

=== PROCEDURE: Test Types ===

| Type | Purpose | When |
|------|---------|------|
| Unit | Individual functions | Every PR |
| Integration | Component interaction | Every PR |
| E2E | User flows | Release |
| Performance | Speed/load | Release |
| Security | Vulnerabilities | Release |

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(quality-review) | Review tests |
| @skill(quality-gates) | Enforce coverage |
