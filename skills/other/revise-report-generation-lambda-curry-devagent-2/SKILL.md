---
name: Revise Report Generation
description: >-
  Generates structured revise reports for Epics by aggregating task comments and learnings.
  Use when: (1) An Epic is completed or substantially progressed,
  (2) You want to consolidate "Revision Learning" comments from multiple tasks,
  (3) You need a traceability report linking tasks to commits.
---

# Revise Report Generation

Generates structured revise reports to capture insights, learnings, and traceability from Beads Epics.

## Prerequisites

- Beads Epic ID (e.g., `bd-1234`)
- Beads CLI (`bd`) installed and configured
- Tasks within the Epic populated with comments (specifically "Revision Learning" and "Commit")
- Confirm there are no open follow-up tasks created from PR review comments (final review should create these first, and revise report runs only after they are closed)

## Report Structure

### Epic Revise Report

**1. Epic Summary**
- Status of the Epic and child tasks.
- Overall completion rate.

**2. Traceability Matrix**
- Table mapping Task ID -> Title -> Status -> Commit Hash.

**3. Evidence & Screenshots**
- Screenshot directory location and count.
- Key screenshots with descriptions and links.
- Evidence organization by task.

**4. Improvement Recommendations**
- **Documentation:** Missing docs, outdated content, gaps in onboarding.
- **Process:** Workflow friction, automation opportunities, quality gate improvements.
- **Rules & Standards:** Cursor rules updates, coding standards violations, pattern inconsistencies.
- **Tech Architecture:** Code structure issues, dependency concerns, technical debt, performance considerations.

**5. Action Items**
- Prioritized, actionable steps to address improvements (Critical, High, Medium, Low).

## Report Generation Process

### Step 1: Data Gathering

**Command:** `bd list --parent <EpicID> --json`
- Retrieves all child tasks.
- Ensure any PR review follow-up tasks are closed before proceeding.

**For each task:** `bd comments <TaskID> --json`
- Retrieves all comments.
- **Filter:** Look for comments starting with:
    - `Revision Learning:` (may include structured format with Category, Priority, Issue, Recommendation)
    - `Commit:`
    - `Screenshots captured:` (screenshot paths)
    - `Quality gates failed` (to track rework)

### Step 2: Analysis & Categorization

**Traceability:**
- Extract Commit Hash and Subject from `Commit:` comments.
- If missing, flag as "Missing Traceability".

**Learning Categorization:**
- Parse text after `Revision Learning:`.
- **Structured Format Support:** If learning includes structured fields:
    - Extract `Category:` (Documentation|Process|Rules|Architecture)
    - Extract `Priority:` (Critical|High|Medium|Low)
    - Extract `Issue:` (description)
    - Extract `Recommendation:` (actionable improvement)
    - Extract `Files/Rules Affected:` (references)
- **Auto-Classification:** If not structured, classify into:
    - **Documentation:** Missing context, unclear specs, outdated docs, onboarding gaps.
    - **Process:** Instructions, prompting, workflow steps, automation opportunities, quality gates.
    - **Rules & Standards:** Cursor rules, coding standards, pattern inconsistencies, best practices.
    - **Tech Architecture:** Coding patterns, libraries, APIs, code structure, dependencies, technical debt, performance.

**Screenshot Collection:**
- Extract screenshot paths from `Screenshots captured:` comments.
- Group screenshots by task ID.
- Verify screenshot files exist in project directory.
- Count total screenshots and identify key screenshots for inclusion.

### Step 3: Report Construction

**Filename:** `YYYY-MM-DD_revise-report-epic-<EpicID>.md` or `YYYY-MM-DD_<epic-id>-improvements.md`
**Location:** `.devagent/workspace/reviews/`

**Template:**
```markdown
# Epic Revise Report - <Epic Title>

**Date:** YYYY-MM-DD
**Epic ID:** <EpicID>
**Status:** <EpicStatus>

## Executive Summary
<2-3 sentence overview of the epic's execution and key takeaways>

## Traceability Matrix

| Task ID | Title | Status | Commit |
| :--- | :--- | :--- | :--- |
| bd-xxxx.1 | Implement Feature X | closed | `a1b2c3d` - feat: ... |
| bd-xxxx.2 | Fix Bug Y | in_progress | *Pending* |

## Evidence & Screenshots

- **Screenshot Directory**: `.devagent/workspace/reviews/<epic-id>/screenshots/`
- **Screenshots Captured**: [count] screenshots across [count] tasks
- **Key Screenshots**:
  - [Task ID]: [description] - `screenshots/[filename].png`
  - [Task ID]: [description] - `screenshots/[filename].png`

## Improvement Recommendations

### Documentation
- [ ] **[Priority] Missing**: [description] - [impact] - [files affected]
- [ ] **[Priority] Outdated**: [description] - [current state] - [needs update to]
- [ ] **[Priority] Gap**: [description] - [impact] - [recommendation]

### Process
- [ ] **[Priority] Workflow**: [friction point] - [suggestion] - [benefit]
- [ ] **[Priority] Automation**: [opportunity] - [implementation approach] - [benefit]
- [ ] **[Priority] Quality Gate**: [issue] - [recommendation] - [impact]

### Rules & Standards
- [ ] **[Priority] Cursor Rule**: [rule file] - [issue] - [recommended change]
- [ ] **[Priority] Pattern**: [pattern name] - [inconsistency] - [standard to apply]
- [ ] **[Priority] Coding Standard**: [violation] - [recommendation] - [files affected]

### Tech Architecture
- [ ] **[Priority] Structure**: [issue] - [current approach] - [recommended approach]
- [ ] **[Priority] Dependency**: [concern] - [risk] - [mitigation]
- [ ] **[Priority] Technical Debt**: [issue] - [impact] - [recommendation]
- [ ] **[Priority] Performance**: [concern] - [current state] - [optimization approach]

## Action Items
1. [ ] **[Priority]** <Action Item> - [from category]
2. [ ] **[Priority]** <Action Item> - [from category]
```

## Validation

- Ensure every "Revision Learning" is captured.
- Ensure every "Commit" is linked.
- Verify Action Items are actionable.
