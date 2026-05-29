---
document_name: "usability-review.skill.md"
location: ".claude/skills/usability-review.skill.md"
codebook_id: "CB-SKILL-USABILITY-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for usability review and audit"
skill_metadata:
  category: "design"
  complexity: "intermediate"
  estimated_time: "1-2 hours"
  prerequisites:
    - "UX heuristics knowledge"
    - "Testing methodology"
category: "skills"
status: "active"
tags:
  - "skill"
  - "design"
  - "ux"
  - "usability"
ai_parser_instructions: |
  This skill defines procedures for usability review.
  Used by UX Designer agent.
---

# Usability Review Skill

=== PURPOSE ===

Procedures for conducting usability reviews and heuristic evaluations.

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(ux-designer) @ref(CB-AGENT-UXDESIGN-001) | Primary skill for usability |

=== PROCEDURE: Heuristic Evaluation ===

**Nielsen's 10 Usability Heuristics:**

### 1. Visibility of System Status
- [ ] User knows current location
- [ ] Loading states are indicated
- [ ] Progress is visible for long operations
- [ ] Actions provide feedback

### 2. Match Between System and Real World
- [ ] Language is user-friendly
- [ ] Icons are recognizable
- [ ] Concepts match user mental models
- [ ] Information is logically ordered

### 3. User Control and Freedom
- [ ] Undo is available
- [ ] Cancel is always accessible
- [ ] Users can exit flows
- [ ] Confirmation for destructive actions

### 4. Consistency and Standards
- [ ] UI patterns are consistent
- [ ] Terminology is consistent
- [ ] Platform conventions followed
- [ ] Same actions produce same results

### 5. Error Prevention
- [ ] Constraints prevent invalid input
- [ ] Confirmation before destructive actions
- [ ] Clear input requirements shown
- [ ] Auto-save where appropriate

### 6. Recognition Rather Than Recall
- [ ] Options are visible
- [ ] Labels are descriptive
- [ ] Help is contextual
- [ ] Recent items are accessible

### 7. Flexibility and Efficiency of Use
- [ ] Shortcuts available for experts
- [ ] Personalization options
- [ ] Frequent actions are quick
- [ ] Search is available

### 8. Aesthetic and Minimalist Design
- [ ] Only relevant information shown
- [ ] Visual hierarchy is clear
- [ ] White space is used well
- [ ] No unnecessary elements

### 9. Help Users Recognize and Recover from Errors
- [ ] Error messages are clear
- [ ] Errors explain the problem
- [ ] Solutions are suggested
- [ ] Recovery path is obvious

### 10. Help and Documentation
- [ ] Help is searchable
- [ ] Tasks are focused
- [ ] Steps are concrete
- [ ] Help is contextual

=== PROCEDURE: Review Process ===

**Steps:**
1. Define scope (feature, flow, or full app)
2. Identify user tasks to evaluate
3. Walk through each task
4. Score against heuristics
5. Document findings
6. Prioritize issues
7. Recommend fixes

**Severity Scale:**
| Level | Impact | Priority |
|-------|--------|----------|
| 0 | Not usability issue | None |
| 1 | Cosmetic | Low |
| 2 | Minor | Medium |
| 3 | Major | High |
| 4 | Catastrophic | Critical |

=== PROCEDURE: Review Report ===

```markdown
# Usability Review Report

**Feature:** [Name]
**Reviewer:** @ux-designer
**Date:** YYYY-MM-DD
**Scope:** [Description of what was reviewed]

## Executive Summary
Brief overview of findings and overall assessment.

## Findings

### [SEV-3] Finding Title
**Heuristic:** #4 Consistency
**Location:** /settings/profile
**Issue:** Save button location inconsistent with other forms
**Impact:** Users struggle to find save action
**Recommendation:** Move save button to top-right, consistent with other forms
**Screenshot:** [if applicable]

### [SEV-2] Finding Title
...

## Summary Table
| Severity | Count |
|----------|-------|
| Critical (4) | 0 |
| Major (3) | 2 |
| Minor (2) | 5 |
| Cosmetic (1) | 3 |

## Recommendations
1. Address [critical issue] immediately
2. Fix [major issues] in next sprint
3. Schedule [minor issues] for backlog

## Next Steps
- [ ] Review findings with team
- [ ] Create issues in @ref(CB-AGENT-PM-001) backlog
- [ ] Schedule re-review after fixes
```

=== PROCEDURE: Task Analysis ===

**Task Checklist:**
```markdown
## Task: [Task Name]

### Pre-conditions
- User is logged in
- User has required permissions

### Steps Observed
| Step | Action | Expected | Actual | Pass? |
|------|--------|----------|--------|-------|
| 1 | Click X | Show Y | Shows Y | ✓ |
| 2 | Enter text | Accepts | Error | ✗ |

### Issues Found
- Step 2: Error message unclear
- Step 4: Button is hard to find

### Task Success
- [ ] Completed successfully
- [x] Completed with difficulty
- [ ] Failed to complete

### Time on Task
- Expected: 2 minutes
- Actual: 4.5 minutes
```

=== PROCEDURE: Cognitive Walkthrough ===

**For each action, ask:**
1. Will the user try to achieve the right effect?
2. Will the user notice the correct action is available?
3. Will the user associate the correct action with desired effect?
4. If correct action is performed, will user see progress?

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(user-flows) | Flow context |
| @skill(accessibility) | A11y overlap |
