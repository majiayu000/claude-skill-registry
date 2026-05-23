---
document_name: "issue-management.skill.md"
location: ".claude/skills/issue-management.skill.md"
codebook_id: "CB-SKILL-ISSUEMGMT-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for creating and managing GitHub issues"
skill_metadata:
  category: "product-management"
  complexity: "simple"
  estimated_time: "5-15 min per issue"
  prerequisites:
    - "GitHub repository access"
    - "Issue templates"
category: "skills"
status: "active"
tags:
  - "skill"
  - "github"
  - "issues"
  - "product-management"
ai_parser_instructions: |
  This skill defines procedures for GitHub issue management.
  Section markers: === SECTION ===
  Procedure markers: === PROCEDURE: NAME ===
---

# Issue Management Skill

=== PURPOSE ===

This skill provides procedures for creating and managing GitHub issues. All issues MUST use standardized templates and follow labeling conventions.

---

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(product-manager) @ref(CB-AGENT-PM-001) | Primary skill for issue creation |

---

=== PREREQUISITES ===

Before using this skill:
- [ ] GitHub repository access
- [ ] Issue templates available (@ref(CB-TPL-ISSUE-BUG-001), etc.)
- [ ] Label definitions (@ref(CB-TPL-LABELS-001))

---

=== PROCEDURE: Bug Report ===

**Template:** @ref(CB-TPL-ISSUE-BUG-001)

**Steps:**
1. Use Bug Report template
2. Fill in all required sections:
   - Title: Clear, descriptive summary
   - Environment: OS, browser, version
   - Steps to Reproduce: Numbered, specific steps
   - Expected Behavior: What should happen
   - Actual Behavior: What actually happens
   - Screenshots: If applicable
3. Apply labels:
   - `type: bug`
   - Priority label (`priority: high/medium/low`)
   - Component label
4. Link to related issues if any

---

=== PROCEDURE: Feature Request ===

**Template:** @ref(CB-TPL-ISSUE-FEATURE-001)

**Steps:**
1. Use Feature Request template
2. Fill in all required sections:
   - Title: Feature name/summary
   - User Story: As a [user], I want [goal], so that [benefit]
   - Acceptance Criteria: Checkbox list
   - Priority: Business justification
   - Dependencies: Related features/issues
3. Apply labels:
   - `type: feature`
   - Priority label
   - Component label
4. Link to epic if applicable

---

=== PROCEDURE: Task ===

**Template:** @ref(CB-TPL-ISSUE-TASK-001)

**Steps:**
1. Use Task template
2. Fill in all required sections:
   - Title: Task description
   - Description: What needs to be done
   - Subtasks: Checkbox list of steps
   - Definition of Done: Clear completion criteria
3. Apply labels:
   - `type: task` or `type: chore`
   - Component label
4. Assign to appropriate developer

---

=== PROCEDURE: Epic ===

**Template:** @ref(CB-TPL-ISSUE-EPIC-001)

**Steps:**
1. Use Epic template
2. Fill in all required sections:
   - Title: Epic name
   - Overview: High-level description
   - Goals: What this epic achieves
   - Child Issues: List of related issues
   - Success Metrics: How to measure completion
3. Apply labels:
   - `type: epic`
   - Priority label
4. Link to milestone

---

=== PROCEDURE: Issue Triage ===

**Purpose:** Process and prioritize incoming issues

**Steps:**
1. Review new issues daily
2. Verify completeness (all template sections filled)
3. Request clarification if needed
4. Assign priority label
5. Assign component label
6. Link to epic/milestone if applicable
7. Add to project board

**Priority Definitions:**
- `priority: critical` - Production down, security issue
- `priority: high` - Major feature blocked, significant bug
- `priority: medium` - Normal priority work
- `priority: low` - Nice to have, minor issues

---

=== PROCEDURE: Backlog Grooming ===

**Purpose:** Maintain healthy backlog

**Steps:**
1. Review issues older than 30 days
2. Close stale issues with explanation
3. Update priorities based on current goals
4. Break down large issues
5. Remove duplicates
6. Ensure all issues have labels

**Frequency:** Weekly

---

=== ANTI-PATTERNS ===

### Vague Titles
**Problem:** "Bug" or "Fix issue"
**Solution:** Specific, descriptive titles: "Login fails with special characters in password"

### Missing Reproduction Steps
**Problem:** Bugs without steps to reproduce
**Solution:** Always require numbered, specific steps

### Orphan Issues
**Problem:** Issues not linked to epics or milestones
**Solution:** Every feature/bug should have context

### Label Inconsistency
**Problem:** Missing or incorrect labels
**Solution:** Use triage procedure for all issues

---

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(requirements-gathering) | Requirements become issues |
| @skill(roadmap-planning) | Issues feed roadmap |
