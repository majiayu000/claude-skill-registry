---
document_name: "requirements-gathering.skill.md"
location: ".claude/skills/requirements-gathering.skill.md"
codebook_id: "CB-SKILL-REQGATHER-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for gathering and documenting requirements"
skill_metadata:
  category: "product-management"
  complexity: "intermediate"
  estimated_time: "varies"
  prerequisites:
    - "Access to stakeholders"
    - "Understanding of project goals"
category: "skills"
status: "active"
tags:
  - "skill"
  - "requirements"
  - "product-management"
ai_parser_instructions: |
  This skill defines procedures for requirements gathering.
  Section markers: === SECTION ===
  Procedure markers: === PROCEDURE: NAME ===
---

# Requirements Gathering Skill

=== PURPOSE ===

This skill provides procedures for gathering, documenting, and managing requirements. Used by the Product Manager agent for all requirements-related work.

---

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(product-manager) @ref(CB-AGENT-PM-001) | Primary skill for requirements work |

---

=== PREREQUISITES ===

Before using this skill:
- [ ] Access to stakeholders or their documented feedback
- [ ] Understanding of project goals (@ref(CB-BIZ-GOALS-001))
- [ ] Familiarity with user story format

---

=== PROCEDURE: User Story Creation ===

**Purpose:** Create well-formed user stories with acceptance criteria

**Steps:**
1. Identify the user persona (who)
2. Identify the action/goal (what)
3. Identify the benefit (why)
4. Write in format: "As a [persona], I want [goal], so that [benefit]"
5. Define acceptance criteria (Given/When/Then format)
6. Add priority and size estimates
7. Link to related requirements

**Output Format:**
```markdown
## User Story: [Title]

**As a** [user persona]
**I want** [goal/action]
**So that** [benefit/value]

### Acceptance Criteria
- [ ] Given [context], when [action], then [outcome]
- [ ] Given [context], when [action], then [outcome]

### Priority: [High/Medium/Low]
### Size: [S/M/L/XL]
### Related: [links to requirements or issues]
```

---

=== PROCEDURE: Requirements Document ===

**Purpose:** Create comprehensive requirements documentation

**Steps:**
1. Define document scope and context
2. List stakeholders and their interests
3. Document functional requirements
4. Document non-functional requirements
5. Define constraints and assumptions
6. Create traceability matrix
7. Get stakeholder sign-off

**Location:** `devdocs/business/requirements/[feature-name].md`

---

=== PROCEDURE: Stakeholder Interview ===

**Purpose:** Extract requirements from stakeholder conversations

**Steps:**
1. Prepare interview questions
2. Document current pain points
3. Identify desired outcomes
4. Clarify priorities
5. Document assumptions
6. Summarize and validate understanding
7. Follow up on unclear points

**Questions to Ask:**
- What problem are you trying to solve?
- Who are the primary users?
- What does success look like?
- What are the must-haves vs nice-to-haves?
- What are the constraints (time, budget, technical)?

---

=== PROCEDURE: Requirements Prioritization ===

**Purpose:** Prioritize requirements using MoSCoW method

**Categories:**
- **Must Have:** Critical, non-negotiable
- **Should Have:** Important but not critical
- **Could Have:** Desirable but not necessary
- **Won't Have:** Out of scope for this release

**Steps:**
1. List all requirements
2. Categorize each using MoSCoW
3. Validate with stakeholders
4. Document rationale for each priority
5. Review and adjust as needed

---

=== ANTI-PATTERNS ===

### Vague Requirements
**Problem:** Requirements like "make it faster" or "improve UX"
**Solution:** Always quantify: "reduce load time to under 2 seconds"

### Assumed Context
**Problem:** Not documenting assumptions
**Solution:** Explicitly state all assumptions

### Missing Acceptance Criteria
**Problem:** User stories without clear done criteria
**Solution:** Every story must have Given/When/Then criteria

### Scope Creep
**Problem:** Requirements expanding without documentation
**Solution:** Document all changes with rationale

---

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(issue-management) | Requirements become issues |
| @skill(roadmap-planning) | Requirements feed roadmap |
| @skill(user-flows) | UX informs requirements |
