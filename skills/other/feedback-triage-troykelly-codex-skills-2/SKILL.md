---
name: feedback-triage
description: Use when receiving UAT feedback, bug reports, user testing results, stakeholder feedback, QA findings, or any batch of issues to investigate. Investigates each item BEFORE creating issues, classifies by type and priority, creates well-formed GitHub issues with proper project board integration.
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

```
┌─────────────────────────────────────────────────────────────────────┐
│                      FEEDBACK RECEIVED                               │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│               STEP 0: PROJECT BOARD READINESS (GATE)                │
│  Verify GITHUB_PROJECT_NUM and GH_PROJECT_OWNER are set             │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    STEP 1: PARSE INTO ITEMS                         │
│  Identify distinct feedback items                                   │
│  Create TodoWrite entry for each item                               │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
            ┌─────────────────────────────────────────┐
            │         FOR EACH FEEDBACK ITEM          │
            └─────────────────────┬───────────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        ▼                         ▼                         ▼
  ┌───────────┐           ┌─────────────┐           ┌─────────────┐
  │INVESTIGATE│           │  CLASSIFY   │           │   CREATE    │
  │           │──────────▶│             │──────────▶│   ISSUE     │
  │ Research  │           │ Type+Priority│          │ Best Practice│
  └───────────┘           └─────────────┘           └──────┬──────┘
                                                          │
                                                          ▼
                                                   ┌─────────────┐
                                                   │ ADD TO      │
                                                   │ PROJECT     │
                                                   │ BOARD       │
                                                   └─────────────┘
```

## Step 0: Project Board Readiness (GATE)

**Before any triage, verify project board infrastructure is ready.**

```bash
# Derive defaults from GITHUB_PROJECT if provided
if [ -z "$GITHUB_PROJECT_NUM" ] && [ -n "$GITHUB_PROJECT" ]; then
  NUM_CANDIDATE=$(echo "$GITHUB_PROJECT" | sed -E 's#.*/projects/([0-9]+).*#\1#')
  if [ -n "$NUM_CANDIDATE" ] && [ "$NUM_CANDIDATE" != "$GITHUB_PROJECT" ]; then
    export GITHUB_PROJECT_NUM="$NUM_CANDIDATE"
    echo "Derived GITHUB_PROJECT_NUM=$GITHUB_PROJECT_NUM from GITHUB_PROJECT"
  fi
fi

if [ -z "$GH_PROJECT_OWNER" ] && [ -n "$GITHUB_OWNER" ]; then
  export GH_PROJECT_OWNER="$GITHUB_OWNER"
  echo "Derived GH_PROJECT_OWNER=$GH_PROJECT_OWNER from GITHUB_OWNER"
fi

if [ -z "$GH_PROJECT_OWNER" ] && [ -n "$GITHUB_PROJECT" ]; then
  OWNER_CANDIDATE=$(echo "$GITHUB_PROJECT" | sed -E 's#https://github.com/(orgs|users)/([^/]+)/projects/[0-9]+#\2#')
  if [ -n "$OWNER_CANDIDATE" ] && [ "$OWNER_CANDIDATE" != "$GITHUB_PROJECT" ]; then
    export GH_PROJECT_OWNER="$OWNER_CANDIDATE"
    echo "Derived GH_PROJECT_OWNER=$GH_PROJECT_OWNER from GITHUB_PROJECT"
  fi
fi

if [ -z "$GH_PROJECT_OWNER" ]; then
  REMOTE_URL=$(git remote get-url origin 2>/dev/null || true)
  OWNER_CANDIDATE=$(echo "$REMOTE_URL" | sed -E 's#(git@|https://)github.com[:/]+([^/]+)/[^/]+(\.git)?#\2#')
  if [ -n "$OWNER_CANDIDATE" ] && [ "$OWNER_CANDIDATE" != "$REMOTE_URL" ]; then
    export GH_PROJECT_OWNER="$OWNER_CANDIDATE"
    echo "Derived GH_PROJECT_OWNER=$GH_PROJECT_OWNER from git remote"
  fi
fi

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

### Issue Template: Bug

```bash
gh issue create \
  --title "[Bug] [Concise description of the problem]" \
  --body "## Summary

[One-sentence description of the bug]

## Environment

- **URL:** [affected URL]
- **Environment:** [Production/Staging/Local]
- **Browser/Client:** [if relevant]

## Steps to Reproduce

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Expected Behavior

[What should happen]

## Actual Behavior

[What actually happens]

## Error Details

\`\`\`
[Error message, status code, or log output]
\`\`\`

## Investigation Findings

### Code Analysis
- **Affected files:** [list of files]
- **Likely cause:** [hypothesis]
- **Related code:** [functions/modules]

### Impact
- **Users affected:** [scope]
- **Functionality blocked:** [what can't users do]
- **Workaround:** [if any]

## Acceptance Criteria

- [ ] Error no longer occurs
- [ ] [Specific behavior restored]
- [ ] Tests added to prevent regression

## Technical Notes

[Any additional technical context from investigation]

---
**Source:** UAT Feedback / User Report / Support Ticket
**Reported:** [DATE]"
```

### Issue Template: Feature / UX Enhancement

```bash
gh issue create \
  --title "[Feature] [Clear description of the feature]" \
  --body "## Summary

[One-sentence description of what this feature does]

## Background

[Why this is needed - user feedback, business requirement, etc.]

## Current Behavior

[What exists today, if anything]

## Proposed Behavior

[What should happen after implementation]

## User Story

As a [type of user], I want [goal] so that [benefit].

## Investigation Findings

### Scope Analysis
- **Files affected:** [list]
- **Complexity:** [Low/Medium/High]
- **Dependencies:** [related features/systems]

### Design Considerations
[Options considered, recommendations, questions]

## Acceptance Criteria

- [ ] [Specific, verifiable criterion 1]
- [ ] [Specific, verifiable criterion 2]
- [ ] [Specific, verifiable criterion 3]

## Out of Scope

- [What this issue will NOT address]

## Technical Notes

[Implementation hints, patterns to follow, etc.]

---
**Source:** UAT Feedback / User Request / Stakeholder Input
**Requested:** [DATE]"
```

### Issue Template: Research / Spike

```bash
gh issue create \
  --title "[Research] [What needs to be understood]" \
  --body "## Summary

[One-sentence description of what needs to be researched]

## Background

[Why this research is needed]

## Questions to Answer

1. [Question 1]
2. [Question 2]
3. [Question 3]

## Investigation Context

[What was discovered during initial triage that prompted this research]

## Scope

### In Scope
- [Topic 1]
- [Topic 2]

### Out of Scope
- [Not covering X]

## Deliverables

- [ ] Document with findings
- [ ] Recommendations for next steps
- [ ] [Specific output, e.g., design options, architecture diagram]

## Time Box

[Suggested time limit: e.g., 4 hours, 1 day]

## Acceptance Criteria

- [ ] All questions answered with evidence
- [ ] Recommendations documented
- [ ] Next steps identified (issues to create)

---
**Source:** UAT Feedback / Triage Investigation
**Created:** [DATE]"
```

---

## Step 5: Add to Project Board (MANDATORY)

**Every issue MUST be added to the project board with correct fields.**

```bash
# After creating issue, add to project
ISSUE_URL=$(gh issue view [ISSUE_NUMBER] --json url -q '.url')
gh project item-add "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" --url "$ISSUE_URL"

# Get item ID
ITEM_ID=$(gh project item-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
  --format json | jq -r ".items[] | select(.content.number == [ISSUE_NUMBER]) | .id")

# Get field IDs
PROJECT_ID=$(gh project list --owner "$GH_PROJECT_OWNER" --format json | \
  jq -r ".projects[] | select(.number == $GITHUB_PROJECT_NUM) | .id")

STATUS_FIELD_ID=$(gh project field-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
  --format json | jq -r '.fields[] | select(.name == "Status") | .id')

TYPE_FIELD_NAME="Type"
if ! gh project field-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" --format json | jq -e '.fields[] | select(.name == "Type")' >/dev/null 2>&1; then
  if gh project field-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" --format json | jq -e '.fields[] | select(.name == "Issue Type")' >/dev/null 2>&1; then
    TYPE_FIELD_NAME="Issue Type"
  fi
fi

TYPE_FIELD_ID=$(gh project field-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
  --format json | jq -r --arg type_field "$TYPE_FIELD_NAME" '.fields[] | select(.name == $type_field) | .id')

PRIORITY_FIELD_ID=$(gh project field-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
  --format json | jq -r '.fields[] | select(.name == "Priority") | .id')

# Set Status = Ready (or Backlog for lower priority)
READY_OPTION_ID=$(gh project field-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
  --format json | jq -r '.fields[] | select(.name == "Status") | .options[] | select(.name == "Ready") | .id')

gh project item-edit --project-id "$PROJECT_ID" --id "$ITEM_ID" \
  --field-id "$STATUS_FIELD_ID" --single-select-option-id "$READY_OPTION_ID"

# Set Type (Bug, Feature, Research, etc.)
TYPE_OPTION_ID=$(gh project field-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
  --format json | jq -r --arg type_field "$TYPE_FIELD_NAME" --arg type_value "[TYPE]" '.fields[] | select(.name == $type_field) | .options[] | select(.name == $type_value) | .id')

gh project item-edit --project-id "$PROJECT_ID" --id "$ITEM_ID" \
  --field-id "$TYPE_FIELD_ID" --single-select-option-id "$TYPE_OPTION_ID"

# Set Priority
PRIORITY_OPTION_ID=$(gh project field-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
  --format json | jq -r ".fields[] | select(.name == \"Priority\") | .options[] | select(.name == \"[PRIORITY]\") | .id")

gh project item-edit --project-id "$PROJECT_ID" --id "$ITEM_ID" \
  --field-id "$PRIORITY_FIELD_ID" --single-select-option-id "$PRIORITY_OPTION_ID"

# Verify
echo "Issue #[ISSUE_NUMBER] added to project with Status=Ready, Type=[TYPE], Priority=[PRIORITY]"
```

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

## Example: Processing UAT Feedback

### Input Received

```markdown
We have some bugs to resolve from UAT.

## Family Page has error
`https://stage.kin.life/family`
Displays: Something went wrong on our end.
[curl command and error response]

## Family Page refers to "Children" - not Care Recipients
Need better terminology, research required.

## Family Page unable to add care recipient
[curl command and error response]
```

### Triage Process

**Step 1: Parse into items**
- Item 1: Family page 500 error on load
- Item 2: Terminology issue (Children vs Care Recipients)
- Item 3: Cannot add care recipient (500 error)

**Step 2: Investigate each**

*Item 1 Investigation:*
- API endpoint: `/api/v1/children?limit=50`
- Error: `INTERNAL_ERROR`
- Code review: Check children service, database queries
- Impact: Users cannot view family page at all

*Item 2 Investigation:*
- Current: Hardcoded "Children" but button says "care recipient"
- Request: More inclusive language for diverse care relationships
- Scope: UI changes, possibly data model changes
- Needs: UX research, product decision

*Item 3 Investigation:*
- API endpoint: `POST /api/v1/children`
- Payload: Valid care recipient data
- Error: `INTERNAL_ERROR`
- Code review: Check creation endpoint, validation, database writes
- Impact: Users cannot add any care recipients

**Step 3: Classify**

| Item | Type | Priority | Reasoning |
|------|------|----------|-----------|
| 1 | Bug | High | Core functionality broken |
| 2 | Research | Medium | UX improvement, not blocking |
| 3 | Bug | High | Core functionality broken |

**Step 4: Create issues** (using templates above)

**Step 5: Add to project board** (with Type, Priority, Status)

**Step 6: Summary report** (as shown above)

---

## Best Practices for Issue Quality

### Title Conventions

| Type | Format | Example |
|------|--------|---------|
| Bug | `[Bug] <What is broken>` | `[Bug] Family page returns 500 error` |
| Feature | `[Feature] <What it does>` | `[Feature] Add person to Kin Circle` |
| Research | `[Research] <What to investigate>` | `[Research] Inclusive terminology for care relationships` |
| Spike | `[Spike] <Technical question>` | `[Spike] Evaluate API caching strategies` |

### Acceptance Criteria Quality

**Good criteria are:**
- Specific and verifiable
- Written as checkboxes
- Focused on behavior, not implementation
- Testable

**Bad:**
- [ ] Fix the bug
- [ ] Make it work

**Good:**
- [ ] GET `/api/v1/children` returns 200 with valid data
- [ ] Family page displays list of care recipients
- [ ] Error state shows user-friendly message with retry option

### Investigation Documentation

Always document:
- What you found
- Where you looked
- What the likely cause is
- What the impact is

This saves time when implementation begins.

---

## Handling Unclear Feedback

### When Feedback is Vague

If feedback lacks detail:

1. **Ask clarifying questions** before creating issue
2. **Create Research issue** to gather more information
3. **Document what IS known** in the issue

### Clarification Template

```markdown
Before I create issues for this feedback, I need clarification:

1. **[Item 1]:** [Question about scope/expected behavior/reproduction]
2. **[Item 2]:** [Question about priority/business context]

Once clarified, I'll complete the investigation and create properly-formed issues.
```

### When to Create Research Issues

Create a Research issue instead of Bug/Feature when:
- Requirements are unclear
- Multiple solutions exist
- Design decisions needed
- User research required
- Technical feasibility unknown

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
