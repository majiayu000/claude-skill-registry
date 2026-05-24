---
name: project-status-sync
description: Use to keep GitHub Project fields synchronized with actual work state - updates status, verification, criteria counts, and other project-specific fields
allowed-tools:
  - Bash
  - mcp__github__*
model: opus
---

# Project Status Sync

## Overview

Keep GitHub Project fields in sync with actual work state.

**Core principle:** Project fields are the dashboard. Keep them accurate.

**This skill is used throughout work, called by other skills.**

## Required Environment

```bash
# Must have GITHUB_PROJECT set
echo $GITHUB_PROJECT
# Example: https://github.com/users/troykelly/projects/4
```

## Project Field Reference

### Standard Fields

| Field | Type | Values | Updated When |
|-------|------|--------|--------------|
| Status | Single select | Backlog, Ready, In Progress, In Review, Done, Blocked | Work state changes |
| Verification | Single select | Not Verified, Failing, Partial, Passing | Verification runs |
| Criteria Met | Number | 0-N | Criteria checked off |
| Criteria Total | Number | N | Issue created/updated |
| Priority | Single select | Critical, High, Medium, Low | Priority changes |
| Type | Single select | Feature, Bug, Chore, Research, Spike | Issue created |
| Last Verified | Date | ISO date | Verification runs |
| Verified By | Text | agent/human/ci | Verification runs |

## Getting Project IDs

To update project fields, you need various IDs:

```bash
# Get project number from URL
# https://github.com/users/troykelly/projects/4 → PROJECT_NUMBER=4

# Get project ID
gh project list --owner @me --format json | jq -r '.projects[] | select(.number == 4) | .id'

# Get field IDs
gh project field-list [PROJECT_NUMBER] --owner @me --format json

# Get item ID for a specific issue
gh project item-list [PROJECT_NUMBER] --owner @me --format json | \
  jq -r '.items[] | select(.content.number == [ISSUE_NUMBER]) | .id'
```

## Status Transitions

### Valid Transitions

```
Backlog ──► Ready ──► In Progress ──► In Review ──► Done
    │         │            │              │
    │         │            │              │
    └─────────┴────────────┴──────────────┴──► Blocked
                                               │
                                               ▼
                                        (any previous state)
```

### When to Transition

| From | To | Trigger |
|------|-----|---------|
| Backlog | Ready | Dependencies cleared, ready to work |
| Ready | In Progress | Work begins on issue |
| In Progress | In Review | PR created |
| In Review | Done | PR merged, verification passes |
| Any | Blocked | Blocker encountered |
| Blocked | Previous | Blocker resolved |

## Updating Fields

### Update Status

```bash
# First, get the field ID for Status
STATUS_FIELD_ID=$(gh project field-list [PROJECT_NUMBER] --owner @me --format json | \
  jq -r '.fields[] | select(.name == "Status") | .id')

# Get the option ID for the desired status
OPTION_ID=$(gh project field-list [PROJECT_NUMBER] --owner @me --format json | \
  jq -r '.fields[] | select(.name == "Status") | .options[] | select(.name == "In Progress") | .id')

# Get the item ID for the issue
ITEM_ID=$(gh project item-list [PROJECT_NUMBER] --owner @me --format json | \
  jq -r '.items[] | select(.content.number == [ISSUE_NUMBER]) | .id')

# Update the field
gh project item-edit --project-id [PROJECT_ID] --id $ITEM_ID \
  --field-id $STATUS_FIELD_ID --single-select-option-id $OPTION_ID
```

### Update Verification Status

```bash
# Similar pattern for Verification field
VERIFICATION_FIELD_ID=$(gh project field-list [PROJECT_NUMBER] --owner @me --format json | \
  jq -r '.fields[] | select(.name == "Verification") | .id')

PASSING_OPTION_ID=$(gh project field-list [PROJECT_NUMBER] --owner @me --format json | \
  jq -r '.fields[] | select(.name == "Verification") | .options[] | select(.name == "Passing") | .id')

gh project item-edit --project-id [PROJECT_ID] --id $ITEM_ID \
  --field-id $VERIFICATION_FIELD_ID --single-select-option-id $PASSING_OPTION_ID
```

### Update Number Fields

```bash
# Update Criteria Met
CRITERIA_MET_FIELD_ID=$(gh project field-list [PROJECT_NUMBER] --owner @me --format json | \
  jq -r '.fields[] | select(.name == "Criteria Met") | .id')

gh project item-edit --project-id [PROJECT_ID] --id $ITEM_ID \
  --field-id $CRITERIA_MET_FIELD_ID --number 3
```

### Update Date Fields

```bash
# Update Last Verified
LAST_VERIFIED_FIELD_ID=$(gh project field-list [PROJECT_NUMBER] --owner @me --format json | \
  jq -r '.fields[] | select(.name == "Last Verified") | .id')

gh project item-edit --project-id [PROJECT_ID] --id $ITEM_ID \
  --field-id $LAST_VERIFIED_FIELD_ID --date "$(date -u +%Y-%m-%d)"
```

### Update Text Fields

```bash
# Update Verified By
VERIFIED_BY_FIELD_ID=$(gh project field-list [PROJECT_NUMBER] --owner @me --format json | \
  jq -r '.fields[] | select(.name == "Verified By") | .id')

gh project item-edit --project-id [PROJECT_ID] --id $ITEM_ID \
  --field-id $VERIFIED_BY_FIELD_ID --text "agent"
```

## Batch Updates

After verification, update multiple fields at once:

```bash
# After verification completes, update:
# - Verification status
# - Criteria Met count
# - Last Verified date
# - Verified By

PROJECT_ID="[PROJECT_ID]"
ITEM_ID="[ITEM_ID]"

# Update verification status
gh project item-edit --project-id $PROJECT_ID --id $ITEM_ID \
  --field-id $VERIFICATION_FIELD_ID --single-select-option-id $PASSING_OPTION_ID

# Update criteria met
gh project item-edit --project-id $PROJECT_ID --id $ITEM_ID \
  --field-id $CRITERIA_MET_FIELD_ID --number 4

# Update last verified
gh project item-edit --project-id $PROJECT_ID --id $ITEM_ID \
  --field-id $LAST_VERIFIED_FIELD_ID --date "$(date -u +%Y-%m-%d)"

# Update verified by
gh project item-edit --project-id $PROJECT_ID --id $ITEM_ID \
  --field-id $VERIFIED_BY_FIELD_ID --text "agent"
```

## Verification to Status Mapping

| Verification | Recommended Status |
|--------------|-------------------|
| Not Verified | In Progress (still working) |
| Failing | In Progress (needs fixes) |
| Partial | In Progress (needs work) |
| Passing | In Review (ready for PR review) |

## Adding Issues to Project

When a new issue is created, add it to the project:

```bash
# Add issue to project
gh project item-add [PROJECT_NUMBER] --owner @me --url [ISSUE_URL]

# Then set initial field values
# Status: Backlog or Ready
# Priority: as specified
# Type: as specified
# Criteria Total: count from issue
# Verification: Not Verified
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Can't find project | Check GITHUB_PROJECT env var is set correctly |
| Field not found | Verify field exists in project (may need to create) |
| Permission denied | Check gh auth has correct scopes |
| Item not in project | Add issue to project first with item-add |

## Integration

This skill is called by:
- `issue-lifecycle` - Status transitions
- `acceptance-criteria-verification` - Verification field updates
- `issue-prerequisite` - Initial field setup
- `issue-decomposition` - Adding sub-issues to project
