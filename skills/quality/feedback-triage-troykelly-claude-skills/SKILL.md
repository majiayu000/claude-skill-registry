---
name: feedback-triage
description: Use when receiving UAT feedback, bug reports, user testing results, stakeholder feedback, QA findings, or any batch of issues to investigate. Investigates each item BEFORE creating issues, classifies by type and priority, creates well-formed GitHub issues with proper project board integration.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - mcp__github__*
model: opus
---

# Feedback Triage

## Overview

Process raw feedback into actionable, well-documented GitHub issues. Every feedback item is investigated before issue creation.

**Core principle:** Investigate first, issue second. Never create an issue without understanding what you're documenting.

**Announce at start:** "I'm using feedback-triage to investigate and create issues from this feedback."

## When to Use This Skill

Use this skill when you receive:

| Trigger | Examples |
|---------|----------|
| **UAT feedback** | "We have bugs from UAT testing..." |
| **User testing results** | "Users reported the following issues..." |
| **Bug reports** | "Here are the errors we found..." |
| **Stakeholder feedback** | "The client wants these changes..." |
| **QA findings** | "QA discovered these problems..." |
| **Support escalations** | "Support tickets about..." |
| **Production incidents** | "These errors are occurring in prod..." |
| **Feature requests batch** | "Users have requested..." |
| **UX review findings** | "The UX review identified..." |

**Key indicators:**
- Multiple items in one message
- Raw feedback that needs investigation
- Error logs, curl commands, or screenshots
- Requests to "create issues" from feedback
- Phrases like "bugs to resolve", "issues from UAT", "feedback to triage"

## The Triage Protocol

**Flow:** Verify project board → Parse items → For each: Investigate → Classify → Create issue → Add to project board

## Step 0: Project Board Readiness (GATE)

**Before any triage, verify project board infrastructure is ready.**

```bash
# Verify environment variables
if [ -z "$GITHUB_PROJECT_NUM" ]; then
  echo "BLOCKED: GITHUB_PROJECT_NUM not set"
  exit 1
fi

if [ -z "$GH_PROJECT_OWNER" ]; then
  echo "BLOCKED: GH_PROJECT_OWNER not set"
  exit 1
fi

# Verify project is accessible
gh project view "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" --format json > /dev/null 2>&1
```

**Skill:** `project-board-enforcement`

---

## Step 1: Parse Feedback into Items

### Identify Distinct Items

Read through the feedback and identify each distinct item. Look for:

- Separate headings or sections
- Numbered lists
- Different error messages or behaviors
- Distinct feature requests or changes

### Create Tracking List

```bash
# Use TodoWrite to track each item
# Example: 3 items from UAT feedback
TodoWrite:
- [ ] Investigate: Family page error (API 500)
- [ ] Investigate: Terminology issue (Children vs Care Recipients)
- [ ] Investigate: Cannot add care recipient (API 500)
```

### Item Summary Table

Create a summary table for the user:

```markdown
## Feedback Items Identified

| # | Summary | Type (Preliminary) | Severity |
|---|---------|-------------------|----------|
| 1 | Family page error | Bug | High |
| 2 | Terminology needs review | UX/Research | Medium |
| 3 | Cannot add care recipient | Bug | High |

I will investigate each item before creating issues.
```

---

## Step 2: Investigate Each Item

**CRITICAL: Never create an issue without investigation. Understanding comes first.**

### Investigation Protocol by Item Type

#### For API Errors / Bugs

```markdown
## Investigation: [Item Title]

### 1. Error Analysis
- Error code: [e.g., INTERNAL_ERROR, 500, 404]
- Error message: [exact message]
- Request endpoint: [URL]
- Request method: [GET/POST/etc.]

### 2. Reproduction
- Can reproduce: [Yes/No]
- Reproduction steps:
  1. [Step 1]
  2. [Step 2]

### 3. Code Investigation
- Relevant files: [paths]
- Likely cause: [hypothesis after code review]
- Related code: [functions/modules involved]

### 4. Impact Assessment
- Users affected: [All/Some/Specific conditions]
- Functionality blocked: [What can't users do?]
- Workaround exists: [Yes/No - describe if yes]

### 5. Classification
- Type: Bug
- Severity: [Critical/High/Medium/Low]
- Priority: [Critical/High/Medium/Low]
```

#### For UX/Feature Feedback

```markdown
## Investigation: [Item Title]

### 1. Current Behavior
- What exists now: [description]
- Where it appears: [URLs/screens]
- Current implementation: [code locations]

### 2. Requested Change
- What's being asked for: [description]
- User impact: [how this affects users]
- Business context: [why this matters]

### 3. Scope Analysis
- Files affected: [list]
- Complexity: [Low/Medium/High]
- Dependencies: [other features/systems]

### 4. Design Considerations
- Options identified:
  1. [Option A] - [pros/cons]
  2. [Option B] - [pros/cons]
- Recommendation: [if clear]
- Needs: [Design input / Product decision / Research]

### 5. Classification
- Type: Feature / Research / UX Enhancement
- Priority: [Critical/High/Medium/Low]
```

#### For Production Incidents

```markdown
## Investigation: [Item Title]

### 1. Incident Details
- First reported: [timestamp]
- Frequency: [One-time/Intermittent/Constant]
- Environment: [Production/Staging/etc.]

### 2. Error Analysis
- Error logs: [key log entries]
- Stack trace: [if available]
- Affected service: [component/service name]

### 3. Impact Assessment
- Users affected: [count/percentage]
- Revenue impact: [if applicable]
- SLA implications: [if applicable]

### 4. Root Cause Analysis
- Hypothesis: [likely cause]
- Evidence: [supporting data]
- Related changes: [recent deployments/changes]

### 5. Classification
- Type: Bug
- Severity: Critical / High
- Priority: Critical / High
```

### Investigation Checklist

For each item, verify:

- [ ] Error/behavior understood
- [ ] Code reviewed (if applicable)
- [ ] Scope assessed
- [ ] Impact evaluated
- [ ] Type determined (Bug/Feature/Research/etc.)
- [ ] Priority determined
- [ ] Ready to create issue

---

## Step 3: Classify Each Item

### Type Classification

| Type | When to Use | Project Board Type |
|------|-------------|-------------------|
| **Bug** | Something broken, not working as designed | Bug |
| **Feature** | New capability, clear requirements | Feature |
| **Research** | Needs exploration, design thinking, options analysis | Research |
| **Spike** | Time-boxed technical investigation | Spike |
| **Chore** | Maintenance, cleanup, non-user-facing | Chore |
| **UX Enhancement** | Improving existing user experience | Feature |

### Priority Classification

| Priority | Criteria | Response |
|----------|----------|----------|
| **Critical** | Production down, data loss, security breach | Immediate |
| **High** | Major feature broken, significant user impact, blocking | This sprint |
| **Medium** | Feature degraded, workaround exists, important but not blocking | Next sprint |
| **Low** | Minor issue, cosmetic, nice-to-have | Backlog |

### Severity vs Priority

- **Severity** = How bad is the problem? (Technical assessment)
- **Priority** = How soon should we fix it? (Business decision)

A low-severity bug affecting a VIP customer may be high priority.
A high-severity bug on a deprecated feature may be low priority.

---

## Step 4: Create Well-Formed Issues

### Issue Templates

**Bug:** `[Bug] <description>` - Include: Summary, Environment, Steps to Reproduce, Expected/Actual Behavior, Error Details, Investigation Findings (files, cause, impact), Acceptance Criteria, Source.

**Feature:** `[Feature] <description>` - Include: Summary, Background, Current/Proposed Behavior, User Story, Scope Analysis (files, complexity), Acceptance Criteria, Out of Scope.

**Research:** `[Research] <topic>` - Include: Summary, Background, Questions to Answer, Scope, Time Box, Deliverables, Acceptance Criteria.

Use `gh issue create --title "[Type] ..." --body "..."` with appropriate sections from above.

---

## Step 5: Add to Project Board (MANDATORY)

**Every issue MUST be added to the project board with correct fields.**

Use `project-board-enforcement` skill functions:
1. `add_issue_to_project` - Add issue to project
2. `set_project_status` - Set Status (Ready/Backlog)
3. `set_project_type` - Set Type (Bug/Feature/Research)
4. Set Priority field

**Skill:** `project-board-enforcement`

---

## Step 6: Summary Report

After all items are triaged, provide a summary:

```markdown
## Triage Complete

### Issues Created

| # | Issue | Type | Priority | Status |
|---|-------|------|----------|--------|
| 1 | #123 - Family page API error | Bug | High | Ready |
| 2 | #124 - Kin Circle terminology research | Research | Medium | Ready |
| 3 | #125 - Cannot add care recipient | Bug | High | Ready |

### Project Board Status
All issues added to project board with correct fields.

### Recommended Order
1. **#123** - Blocking user access to family page
2. **#125** - Blocking care recipient management
3. **#124** - UX research can proceed in parallel

### Next Steps
- [ ] Assign issues to developers
- [ ] Begin work using `issue-driven-development`
- [ ] Or request immediate resolution
```

---

## Best Practices

**Title formats:** `[Bug] <what's broken>`, `[Feature] <what it does>`, `[Research] <what to investigate>`, `[Spike] <technical question>`

**Good acceptance criteria:** Specific, verifiable, behavior-focused, testable checkboxes.

**If feedback is vague:** Ask clarifying questions OR create Research issue. Document what IS known.

---

## Integration with Other Skills

### This skill flows TO:

| Skill | When |
|-------|------|
| `issue-driven-development` | After issues created, to begin resolution |
| `issue-decomposition` | If a feedback item is too large for one issue |
| `epic-management` | If feedback items should be grouped as epic |

### This skill uses:

| Skill | For |
|-------|-----|
| `project-board-enforcement` | Adding issues to project board |
| `pre-work-research` | Investigation patterns |
| `issue-prerequisite` | Issue quality standards |

---

## Memory Integration

Store triage sessions in knowledge graph:

```bash
mcp__memory__create_entities([{
  "name": "Triage-[DATE]-[SOURCE]",
  "entityType": "FeedbackTriage",
  "observations": [
    "Source: UAT / User Report / etc.",
    "Date: [DATE]",
    "Items received: [COUNT]",
    "Issues created: #X, #Y, #Z",
    "Types: [Bug: N, Feature: N, Research: N]",
    "High priority: [COUNT]"
  ]
}])
```

---

## Checklist

### Before Starting Triage

- [ ] Project board readiness verified (GITHUB_PROJECT_NUM, GH_PROJECT_OWNER)
- [ ] Feedback source identified
- [ ] All items parsed and listed

### For Each Item

- [ ] **Investigation complete** (not skipped)
- [ ] Error/behavior understood
- [ ] Code reviewed (for bugs)
- [ ] Scope assessed
- [ ] Impact evaluated
- [ ] Type classified (Bug/Feature/Research/etc.)
- [ ] Priority assigned
- [ ] Issue created with full template
- [ ] **Added to project board**
- [ ] **Status field set** (Ready or Backlog)
- [ ] **Type field set**
- [ ] **Priority field set**

### After All Items

- [ ] Summary report provided
- [ ] All issues in project board verified
- [ ] Recommended priority order given
- [ ] Memory updated
- [ ] Ready for resolution (if requested)

**Gate:** No issue is created without investigation. No issue is left outside the project board.

---

## Proceeding to Resolution

If the user requests resolution after triage:

```markdown
Issues have been created and prioritized.

**To resolve these issues:**

1. I will work through them using `issue-driven-development`
2. Starting with highest priority: #[N]
3. Each issue will follow the full development process

Shall I proceed with resolution, or should these be assigned for later work?
```

If proceeding, invoke `issue-driven-development` for each issue in priority order.
