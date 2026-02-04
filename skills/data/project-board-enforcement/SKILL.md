---
name: project-board-enforcement
description: MANDATORY for all work - the project board is THE source of truth. This skill provides verification functions and gates that other skills MUST call. No work proceeds without project board compliance.
---

# Project Board Enforcement

## Overview

The GitHub Project board is THE source of truth for all work state. Not labels. Not comments. Not memory. The project board.

**Core principle:** If it's not in the project board with correct fields, it doesn't exist.

**This skill is called by other skills at gate points. It is not invoked directly.**

## The Rule

**Every issue, epic, and initiative MUST be in the project board BEFORE work begins.**

This is not optional. This is not a suggestion. This is a hard gate.

## Required Environment

```bash
# These MUST be set. Work cannot proceed without them.
echo $GITHUB_PROJECT      # Full URL: https://github.com/users/USER/projects/N
echo $GITHUB_PROJECT_NUM  # Just the number: N
echo $GH_PROJECT_OWNER    # Owner: @me or org name

# If GITHUB_PROJECT is set, derive missing values automatically:
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
```

If any are missing, stop and configure them before proceeding.

## Project Field Requirements

### Mandatory Fields

Every project MUST have these fields configured:

| Field | Type | Required Values |
|-------|------|-----------------|
| Status | Single select | Backlog, Ready, In Progress, In Review, Done, Blocked |
| Type (or Issue Type) | Single select | Feature, Bug, Chore, Research, Spike, Epic, Initiative |
| Priority | Single select | Critical, High, Medium, Low |

### Recommended Fields

| Field | Type | Purpose |
|-------|------|---------|
| Verification | Single select | Not Verified, Failing, Partial, Passing |
| Criteria Met | Number | Count of completed acceptance criteria |
| Criteria Total | Number | Total acceptance criteria |
| Last Verified | Date | When verification last ran |
| Epic | Text | Parent epic issue number |
| Initiative | Text | Parent initiative issue number |

## Verification Functions

### Verify Issue in Project

**GATE FUNCTION** - Called before any work begins.

```bash
verify_issue_in_project() {
  local issue=$1

  # Get project item ID
  ITEM_ID=$(gh project item-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
    --format json 2>/dev/null | \
    jq -r ".items[] | select(.content.number == $issue) | .id")

  if [ -z "$ITEM_ID" ] || [ "$ITEM_ID" = "null" ]; then
    echo "BLOCKED: Issue #$issue is not in the project board."
    echo ""
    echo "Add it with:"
    echo "  gh project item-add $GITHUB_PROJECT_NUM --owner $GH_PROJECT_OWNER --url \$(gh issue view $issue --json url -q .url)"
    return 1
  fi

  echo "$ITEM_ID"
  return 0
}
```

### Verify Status Field Set

**GATE FUNCTION** - Called before work proceeds past issue check.

```bash
verify_status_set() {
  local issue=$1
  local item_id=$2

  # Get current status
  STATUS=$(gh project item-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
    --format json 2>/dev/null | \
    jq -r ".items[] | select(.id == \"$item_id\") | .status.name")

  if [ -z "$STATUS" ] || [ "$STATUS" = "null" ]; then
    echo "BLOCKED: Issue #$issue has no Status set in project board."
    echo ""
    echo "Set status before proceeding."
    return 1
  fi

  echo "$STATUS"
  return 0
}
```

### Add Issue to Project

**Called by issue-prerequisite after issue creation.**

```bash
add_issue_to_project() {
  local issue_url=$1

  # Add to project
  gh project item-add "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" --url "$issue_url"

  if [ $? -ne 0 ]; then
    echo "ERROR: Failed to add issue to project."
    return 1
  fi

  # Get the item ID
  local issue_num=$(echo "$issue_url" | grep -oE '[0-9]+$')
  ITEM_ID=$(gh project item-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
    --format json | \
    jq -r ".items[] | select(.content.number == $issue_num) | .id")

  echo "$ITEM_ID"
  return 0
}
```

### Set Project Status

**Called at every status transition.**

```bash
set_project_status() {
  local item_id=$1
  local new_status=$2  # Backlog, Ready, In Progress, In Review, Done, Blocked

  # Get project ID and field IDs (cache these in practice)
  PROJECT_ID=$(gh project list --owner "$GH_PROJECT_OWNER" --format json | \
    jq -r ".projects[] | select(.number == $GITHUB_PROJECT_NUM) | .id")

  STATUS_FIELD_ID=$(gh project field-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
    --format json | \
    jq -r '.fields[] | select(.name == "Status") | .id')

  OPTION_ID=$(gh project field-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
    --format json | \
    jq -r ".fields[] | select(.name == \"Status\") | .options[] | select(.name == \"$new_status\") | .id")

  if [ -z "$OPTION_ID" ] || [ "$OPTION_ID" = "null" ]; then
    echo "ERROR: Status '$new_status' not found in project."
    return 1
  fi

  gh project item-edit --project-id "$PROJECT_ID" --id "$item_id" \
    --field-id "$STATUS_FIELD_ID" --single-select-option-id "$OPTION_ID"

  return $?
}
```

### Set Project Type

**Called when creating issues.**

```bash
set_project_type() {
  local item_id=$1
  local type=$2  # Feature, Bug, Chore, Research, Spike, Epic, Initiative

  PROJECT_ID=$(gh project list --owner "$GH_PROJECT_OWNER" --format json | \
    jq -r ".projects[] | select(.number == $GITHUB_PROJECT_NUM) | .id")

  TYPE_FIELD_NAME="Type"
  if ! gh project field-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" --format json | jq -e '.fields[] | select(.name == "Type")' >/dev/null 2>&1; then
    if gh project field-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" --format json | jq -e '.fields[] | select(.name == "Issue Type")' >/dev/null 2>&1; then
      TYPE_FIELD_NAME="Issue Type"
    fi
  fi

  TYPE_FIELD_ID=$(gh project field-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
    --format json | \
    jq -r --arg type_field "$TYPE_FIELD_NAME" '.fields[] | select(.name == $type_field) | .id')

  OPTION_ID=$(gh project field-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
    --format json | \
    jq -r --arg type_field "$TYPE_FIELD_NAME" --arg type_value "$type" '.fields[] | select(.name == $type_field) | .options[] | select(.name == $type_value) | .id')

  gh project item-edit --project-id "$PROJECT_ID" --id "$item_id" \
    --field-id "$TYPE_FIELD_ID" --single-select-option-id "$OPTION_ID"
}
```

## State Queries via Project Board

### Get Issues by Status

**USE THIS instead of label queries.**

```bash
get_issues_by_status() {
  local status=$1  # Ready, In Progress, etc.

  gh project item-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
    --format json | \
    jq -r ".items[] | select(.status.name == \"$status\") | .content.number"
}

# Examples:
# get_issues_by_status "Ready"
# get_issues_by_status "In Progress"
# get_issues_by_status "Blocked"
```

### Get Issues by Type

```bash
get_issues_by_type() {
  local type=$1  # Epic, Feature, etc.

  gh project item-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
    --format json | \
    jq -r ".items[] | select(.type.name == \"$type\") | .content.number"
}
```

### Get Epic Children

```bash
get_epic_children() {
  local epic_num=$1

  gh project item-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
    --format json | \
    jq -r ".items[] | select(.epic == \"#$epic_num\") | .content.number"
}
```

### Count by Status

```bash
count_by_status() {
  local status=$1

  gh project item-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
    --format json | \
    jq "[.items[] | select(.status.name == \"$status\")] | length"
}
```

## Gate Points

These are the points in workflows where project board verification is MANDATORY:

| Workflow Point | Gate | Skill |
|----------------|------|-------|
| Before any work | Issue in project | issue-driven-development Step 1 |
| After issue creation | Add to project, set fields | issue-prerequisite |
| Starting work | Status → In Progress | issue-driven-development Step 6 |
| Creating branch | Verify project membership | branch-discipline |
| PR created | Status → In Review | pr-creation |
| Work complete | Status → Done | issue-driven-development completion |
| Blocked | Status → Blocked | error-recovery |
| Epic created | Add epic to project, set Type=Epic | epic-management |
| Child issue created | Add to project, link to parent | issue-decomposition |

## Transition Rules

### Valid Status Transitions

```
Backlog ──► Ready ──► In Progress ──► In Review ──► Done
    │         │            │              │
    │         │            │              │
    └─────────┴────────────┴──────────────┴──► Blocked
                                               │
                                               ▼
                                        (any previous state)
```

### Transition Enforcement

```bash
validate_transition() {
  local current=$1
  local target=$2

  case "$current→$target" in
    "Backlog→Ready"|"Ready→In Progress"|"In Progress→In Review"|"In Review→Done")
      return 0 ;;
    *"→Blocked")
      return 0 ;;
    "Blocked→Backlog"|"Blocked→Ready"|"Blocked→In Progress")
      return 0 ;;
    *)
      echo "Invalid transition: $current → $target"
      return 1 ;;
  esac
}
```

## Labels vs Project Board

### WRONG - Do Not Use Labels for State

```bash
# WRONG - labels are NOT the source of truth
gh issue list --label "status:pending"
gh issue edit 123 --add-label "status:in-progress"
```

### RIGHT - Use Project Board

```bash
# RIGHT - project board IS the source of truth
get_issues_by_status "Ready"
set_project_status "$ITEM_ID" "In Progress"
```

### When Labels Are Acceptable

Labels are still used for:
- `epic` - Identifying epic issues (supplementary)
- `epic-[name]` - Grouping issues in an epic (supplementary)
- `spawned-from:#N` - Lineage tracking (supplementary)
- `review-finding` - Origin tracking (supplementary)

But **state** (Ready, In Progress, Blocked, etc.) lives in the project board.

## Sync Verification

Run periodically to detect drift:

```bash
verify_project_sync() {
  echo "## Project Board Sync Check"
  echo ""

  # Check for issues with branches but Status != In Progress
  echo "### Issues with branches but not 'In Progress':"
  for branch in $(git branch -r | grep -E 'feature/[0-9]+' | sed 's/.*feature\///' | cut -d- -f1); do
    status=$(gh project item-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
      --format json | \
      jq -r ".items[] | select(.content.number == $branch) | .status.name")

    if [ "$status" != "In Progress" ] && [ "$status" != "In Review" ]; then
      echo "- #$branch: Status='$status' but has active branch"
    fi
  done

  # Check for In Progress issues with no recent activity
  echo ""
  echo "### 'In Progress' issues with no recent commits:"
  for issue in $(get_issues_by_status "In Progress"); do
    branch=$(git branch -r | grep -E "feature/$issue-" | head -1)
    if [ -z "$branch" ]; then
      echo "- #$issue: In Progress but no branch exists"
    fi
  done
}
```

## Error Messages

All project board errors should be clear and actionable:

```bash
project_error() {
  local code=$1
  local context=$2

  case "$code" in
    "NOT_IN_PROJECT")
      echo "BLOCKED: Issue $context is not in the project board."
      echo "Fix: gh project item-add $GITHUB_PROJECT_NUM --owner $GH_PROJECT_OWNER --url \$(gh issue view $context --json url -q .url)"
      ;;
    "NO_STATUS")
      echo "BLOCKED: Issue $context has no Status field set."
      echo "Fix: Update the issue's Status field in the project board."
      ;;
    "INVALID_TRANSITION")
      echo "BLOCKED: Cannot transition $context - invalid state change."
      ;;
    "PROJECT_NOT_FOUND")
      echo "BLOCKED: Project $GITHUB_PROJECT_NUM not found or not accessible."
      echo "Fix: Verify GITHUB_PROJECT_NUM and GH_PROJECT_OWNER are correct."
      ;;
  esac

  return 1
}
```

## Integration

This skill is called by:
- `issue-driven-development` - All status transitions
- `issue-prerequisite` - After issue creation
- `epic-management` - Epic and child issue setup
- `autonomous-orchestration` - State queries and updates
- `session-start` - Sync verification
- `work-intake` - Project readiness check

## Checklist for Callers

Before proceeding past any gate:

- [ ] Issue exists in project (verified, not assumed)
- [ ] Status field is set
- [ ] Type field is set
- [ ] Priority field is set (for new issues)
- [ ] Epic linkage set (if child of epic)
- [ ] Transition is valid (if changing status)
