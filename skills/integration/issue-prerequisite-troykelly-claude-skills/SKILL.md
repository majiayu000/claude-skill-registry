---
name: issue-prerequisite
description: Use before starting ANY work - hard gate ensuring a GitHub issue exists, creating one if needed through user questioning
allowed-tools:
  - mcp__github__*
model: opus
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

### Option 1: User has existing issue

Ask: "What's the GitHub issue number for this work?"

### Option 2: Need to create issue

Gather information to create an issue:

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

**Uses cached IDs from `github-api-cache`. API calls: 1 (add) + 1 (refresh cache).**

```bash
# Add to project - REQUIRED (1 API call)
gh project item-add "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" --url "$ISSUE_URL"

if [ $? -ne 0 ]; then
  echo "ERROR: Failed to add issue to project. Cannot proceed."
  echo "Issue #$ISSUE_NUMBER exists but is NOT tracked in project board."
  exit 1
fi

# Refresh cache after adding (1 API call)
export GH_CACHE_ITEMS=$(gh project item-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" --format json)

# Get the item ID from refreshed cache (0 API calls)
ITEM_ID=$(echo "$GH_CACHE_ITEMS" | jq -r ".items[] | select(.content.number == $ISSUE_NUMBER) | .id")

if [ -z "$ITEM_ID" ] || [ "$ITEM_ID" = "null" ]; then
  echo "ERROR: Issue added but item ID not found. Cannot set fields."
  exit 1
fi

echo "Issue #$ISSUE_NUMBER added to project with item ID: $ITEM_ID"
```

### Setting Project Fields (MANDATORY)

**All fields must be set before proceeding.**

**Uses cached IDs - 0 API calls for lookups, 3 API calls for field updates.**

```bash
# Use cached IDs (0 API calls) - set by session-start via github-api-cache
# GH_PROJECT_ID, GH_STATUS_FIELD_ID, GH_STATUS_READY_ID already available

# Get Type and Priority field IDs from cache (0 API calls)
TYPE_FIELD_ID=$(echo "$GH_CACHE_FIELDS" | jq -r '.fields[] | select(.name == "Type") | .id')
PRIORITY_FIELD_ID=$(echo "$GH_CACHE_FIELDS" | jq -r '.fields[] | select(.name == "Priority") | .id')

# Get option IDs from cache (0 API calls)
TYPE_OPTION_ID=$(echo "$GH_CACHE_FIELDS" | jq -r ".fields[] | select(.name == \"Type\") | .options[] | select(.name == \"[TYPE]\") | .id")
PRIORITY_OPTION_ID=$(echo "$GH_CACHE_FIELDS" | jq -r ".fields[] | select(.name == \"Priority\") | .options[] | select(.name == \"[PRIORITY]\") | .id")

# Set Status = Ready (1 API call)
gh project item-edit --project-id "$GH_PROJECT_ID" --id "$ITEM_ID" \
  --field-id "$GH_STATUS_FIELD_ID" --single-select-option-id "$GH_STATUS_READY_ID"

# Set Type (1 API call)
gh project item-edit --project-id "$GH_PROJECT_ID" --id "$ITEM_ID" \
  --field-id "$TYPE_FIELD_ID" --single-select-option-id "$TYPE_OPTION_ID"

# Set Priority (1 API call)
gh project item-edit --project-id "$GH_PROJECT_ID" --id "$ITEM_ID" \
  --field-id "$PRIORITY_FIELD_ID" --single-select-option-id "$PRIORITY_OPTION_ID"
```

### Verify Project Board Setup (GATE)

**Do not proceed until verification passes.**

**Refresh cache and verify (1 API call).**

```bash
# Refresh cache and verify (1 API call)
export GH_CACHE_ITEMS=$(gh project item-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" --format json)
VERIFY=$(echo "$GH_CACHE_ITEMS" | jq ".items[] | select(.content.number == $ISSUE_NUMBER)")

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
