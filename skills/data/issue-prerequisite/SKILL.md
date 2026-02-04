---
name: issue-prerequisite
description: Use before starting ANY work - hard gate ensuring a GitHub issue exists, creating one if needed through user questioning
---

# Issue Prerequisite

## Overview

No work without a GitHub issue. This is a hard gate.

**Core principle:** Every task, regardless of size, must have a corresponding GitHub issue.

**Announce at start:** "I'm checking for a GitHub issue before proceeding with any work."

## The Gate

```
┌─────────────────────────────────────┐
│         WORK REQUESTED              │
└─────────────────┬───────────────────┘
                  │
                  ▼
        ┌─────────────────┐
        │ Issue provided? │
        └────────┬────────┘
                 │
       ┌─────────┴─────────┐
       │                   │
      Yes                  No
       │                   │
       ▼                   ▼
  ┌─────────┐      ┌─────────────┐
  │ Verify  │      │ Ask user or │
  │ issue   │      │ create issue│
  │ exists  │      └──────┬──────┘
  └────┬────┘             │
       │                  │
       ▼                  ▼
  ┌──────────────────────────────┐
  │     Issue confirmed?         │
  │   (exists and accessible)    │
  └─────────────┬────────────────┘
                │
       ┌────────┴────────┐
       │                 │
      Yes                No
       │                 │
       ▼                 ▼
   PROCEED            STOP
   WITH WORK       (Cannot proceed)
```

## When Issue is Provided

Verify the issue exists and is accessible:

```bash
# Verify issue exists
gh issue view [ISSUE_NUMBER] --json number,title,state,body

# Check issue is in the correct repository
gh issue view [ISSUE_NUMBER] --json url
```

**If issue doesn't exist or is inaccessible:**
- Report error to user
- Do not proceed

## When No Issue is Provided

**Do not stop to ask for an issue number if the project board already contains the answer.**

Before asking the user:
1. Scan the project board for `Ready` or `In Progress` items matching the request (keywords, title, area).
2. If exactly one candidate fits, use it and proceed.
3. If none fit, create a new issue from the request + repo docs (README, FEATURES.md, BRANDING.md, docs, Storybook) without asking.
4. Only ask the user if multiple candidates exist or critical details are genuinely missing after repo review.

Suggested query:

```bash
# List Ready + In Progress issues with titles
gh project item-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" --format json | \
  jq -r '.items[] | select(.status.name == "Ready" or .status.name == "In Progress") | "\(.content.number) \(.content.title)"'
```

### Option 1: User has existing issue

Ask only if multiple candidates exist: "Which GitHub issue number should I use for this work?"

### Option 2: Need to create issue

If creation is required and details are missing after repo review, gather information to create an issue:

```markdown
I need to create a GitHub issue before starting this work.

**Please provide or confirm:**

1. **Title:** [What should this issue be called?]

2. **Description:** [What should this issue deliver?]

3. **Acceptance Criteria:**
   - [ ] [First verifiable behavior]
   - [ ] [Second verifiable behavior]

4. **Type:** Feature / Bug / Chore / Research / Spike

5. **Priority:** Critical / High / Medium / Low
```

### Creating the Issue

Once information is gathered:

```bash
# Create the issue
ISSUE_URL=$(gh issue create \
  --title "[Type] Title here" \
  --body "## Description

[Description]

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Verification Steps

1. Step 1
2. Step 2

## Technical Notes

[Any technical context]" 2>&1 | tail -1)

ISSUE_NUMBER=$(echo "$ISSUE_URL" | grep -oE '[0-9]+$')
echo "Created issue #$ISSUE_NUMBER"
```

### Adding to Project Board (MANDATORY)

**This step is NOT optional. It is a gate.**

```bash
# Add to project - REQUIRED
gh project item-add "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" --url "$ISSUE_URL"

if [ $? -ne 0 ]; then
  echo "ERROR: Failed to add issue to project. Cannot proceed."
  echo "Issue #$ISSUE_NUMBER exists but is NOT tracked in project board."
  exit 1
fi

# Get the item ID - REQUIRED for field updates
ITEM_ID=$(gh project item-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
  --format json | jq -r ".items[] | select(.content.number == $ISSUE_NUMBER) | .id")

if [ -z "$ITEM_ID" ] || [ "$ITEM_ID" = "null" ]; then
  echo "ERROR: Issue added but item ID not found. Cannot set fields."
  exit 1
fi

echo "Issue #$ISSUE_NUMBER added to project with item ID: $ITEM_ID"
```

### Setting Project Fields (MANDATORY)

**All fields must be set before proceeding.**

```bash
# Get project ID
PROJECT_ID=$(gh project list --owner "$GH_PROJECT_OWNER" --format json | \
  jq -r ".projects[] | select(.number == $GITHUB_PROJECT_NUM) | .id")

# Get field IDs
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

# Get option IDs for the values we want to set
READY_OPTION_ID=$(gh project field-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
  --format json | jq -r '.fields[] | select(.name == "Status") | .options[] | select(.name == "Ready") | .id')

TYPE_OPTION_ID=$(gh project field-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
  --format json | jq -r --arg type_field "$TYPE_FIELD_NAME" --arg type_value "[TYPE]" '.fields[] | select(.name == $type_field) | .options[] | select(.name == $type_value) | .id')

PRIORITY_OPTION_ID=$(gh project field-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
  --format json | jq -r ".fields[] | select(.name == \"Priority\") | .options[] | select(.name == \"[PRIORITY]\") | .id")

# Set Status = Ready
gh project item-edit --project-id "$PROJECT_ID" --id "$ITEM_ID" \
  --field-id "$STATUS_FIELD_ID" --single-select-option-id "$READY_OPTION_ID"

# Set Type
gh project item-edit --project-id "$PROJECT_ID" --id "$ITEM_ID" \
  --field-id "$TYPE_FIELD_ID" --single-select-option-id "$TYPE_OPTION_ID"

# Set Priority
gh project item-edit --project-id "$PROJECT_ID" --id "$ITEM_ID" \
  --field-id "$PRIORITY_FIELD_ID" --single-select-option-id "$PRIORITY_OPTION_ID"
```

### Verify Project Board Setup (GATE)

**Do not proceed until verification passes.**

```bash
# Verify all fields are set
VERIFY=$(gh project item-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
  --format json | jq ".items[] | select(.content.number == $ISSUE_NUMBER)")

STATUS=$(echo "$VERIFY" | jq -r '.status.name')
TYPE=$(echo "$VERIFY" | jq -r '.type.name // "unset"')

if [ -z "$STATUS" ] || [ "$STATUS" = "null" ]; then
  echo "GATE FAILED: Status not set for issue #$ISSUE_NUMBER"
  exit 1
fi

echo "VERIFIED: Issue #$ISSUE_NUMBER is in project with Status=$STATUS"
```

## Issue Quality Check

Before proceeding, verify the issue has:

| Required | Check |
|----------|-------|
| Clear title | Describes what will be delivered |
| Description | Explains the work |
| Acceptance criteria | At least one verifiable criterion |
| In GitHub Project | Added with correct status |

If any are missing, update the issue before proceeding.

## "Too Small for an Issue" is False

Common objections and responses:

| Objection | Response |
|-----------|----------|
| "It's just a typo fix" | Issues take 30 seconds. They provide a record. Create one. |
| "It's a one-liner" | One-liners can introduce bugs. Document them. |
| "I'll do it quickly" | Quick work is forgotten work. Track it. |
| "It's obvious what needs doing" | If it's obvious, the issue will be fast to write. |

No exceptions. Every change has an issue.

## Minimum Viable Issue

For truly trivial work, this is the minimum:

```markdown
Title: Fix typo in README.md

## Description
Fix typo: "teh" → "the"

## Acceptance Criteria
- [ ] Typo is corrected
```

That's 30 seconds. There's no excuse.

## After Gate Passes

Once issue is confirmed:

1. Note the issue number for all subsequent work
2. Proceed to next step in `issue-driven-development`
3. Reference issue in all commits and PR

## Checklist

Before proceeding past this gate:

- [ ] Issue number identified
- [ ] Issue exists in GitHub
- [ ] Issue is accessible (correct repo, not archived)
- [ ] Issue has description
- [ ] Issue has at least one acceptance criterion
- [ ] **Issue is in GitHub Project (VERIFIED with ITEM_ID)**
- [ ] **Status field is set (Ready or Backlog)**
- [ ] **Type field is set**
- [ ] **Priority field is set**

**Gate:** Cannot proceed to `issue-driven-development` Step 2 without all checkboxes verified.

**Skill:** `project-board-enforcement`
