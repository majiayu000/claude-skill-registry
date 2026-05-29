---
name: project-board-enforcement
description: MANDATORY for all work - the project board is THE source of truth. This skill provides verification functions and gates that other skills MUST call. No work proceeds without project board compliance.
allowed-tools:
  - Bash
  - mcp__github__*
model: opus
---

# Project Board Enforcement

## Overview

The GitHub Project board is THE source of truth for all work state. Not labels. Not comments. Not memory. The project board.

**Core principle:** If it's not in the project board with correct fields, it doesn't exist.

**This skill is called by other skills at gate points. It is not invoked directly.**

## API Optimization Requirement

**CRITICAL:** All read operations MUST use cached data from `github-api-cache`.

The following environment variables MUST be set before using this skill:
- `GH_CACHE_ITEMS` - Cached project items JSON
- `GH_CACHE_FIELDS` - Cached project fields JSON
- `GH_PROJECT_ID` - Project node ID
- `GH_STATUS_FIELD_ID` - Status field ID
- `GH_STATUS_*_ID` - Status option IDs

If these are not set, invoke `session-start` first to initialize the cache.

## The Rule

**Every issue, epic, and initiative MUST be in the project board BEFORE work begins.**

This is not optional. This is not a suggestion. This is a hard gate.

## Required Environment

```bash
# These MUST be set. Work cannot proceed without them.
echo $GITHUB_PROJECT      # Full URL: https://github.com/users/USER/projects/N
echo $GITHUB_PROJECT_NUM  # Just the number: N
echo $GH_PROJECT_OWNER    # Owner: @me or org name
```

If any are missing, stop and configure them before proceeding.

## Project Field Requirements

### Mandatory Fields

Every project MUST have these fields configured:

| Field | Type | Required Values |
|-------|------|-----------------|
| Status | Single select | Backlog, Ready, In Progress, In Review, Done, Blocked |
| Type | Single select | Feature, Bug, Chore, Research, Spike, Epic, Initiative |
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

**All read operations use cached data (0 API calls). Only writes require API calls.**

### Verify Issue in Project

**GATE FUNCTION** - Called before any work begins. **0 API calls (uses cache).**

```bash
verify_issue_in_project() {
  local issue=$1

  # Get project item ID FROM CACHE (0 API calls)
  ITEM_ID=$(echo "$GH_CACHE_ITEMS" | jq -r ".items[] | select(.content.number == $issue) | .id")

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

**GATE FUNCTION** - Called before work proceeds past issue check. **0 API calls (uses cache).**

```bash
verify_status_set() {
  local issue=$1
  local item_id=$2

  # Get current status FROM CACHE (0 API calls)
  STATUS=$(echo "$GH_CACHE_ITEMS" | jq -r ".items[] | select(.id == \"$item_id\") | .status.name")

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

**Called by issue-prerequisite after issue creation. 1 API call + cache refresh.**

```bash
add_issue_to_project() {
  local issue_url=$1

  # Add to project (1 API call - unavoidable write)
  gh project item-add "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" --url "$issue_url"

  if [ $? -ne 0 ]; then
    echo "ERROR: Failed to add issue to project."
    return 1
  fi

  # Refresh cache after adding (1 API call)
  export GH_CACHE_ITEMS=$(gh project item-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" --format json)

  # Get the item ID from refreshed cache
  local issue_num=$(echo "$issue_url" | grep -oE '[0-9]+$')
  ITEM_ID=$(echo "$GH_CACHE_ITEMS" | jq -r ".items[] | select(.content.number == $issue_num) | .id")

  echo "$ITEM_ID"
  return 0
}
```

### Set Project Status

**Called at every status transition. 1 API call (uses cached IDs).**

```bash
set_project_status() {
  local item_id=$1
  local new_status=$2  # Backlog, Ready, In Progress, In Review, Done, Blocked

  # Use cached IDs (0 API calls for lookups)
  # GH_PROJECT_ID, GH_STATUS_FIELD_ID set by session-start

  # Get option ID from cache
  local option_id
  case "$new_status" in
    "Backlog")     option_id="$GH_STATUS_BACKLOG_ID" ;;
    "Ready")       option_id="$GH_STATUS_READY_ID" ;;
    "In Progress") option_id="$GH_STATUS_IN_PROGRESS_ID" ;;
    "In Review")   option_id="$GH_STATUS_IN_REVIEW_ID" ;;
    "Done")        option_id="$GH_STATUS_DONE_ID" ;;
    "Blocked")     option_id="$GH_STATUS_BLOCKED_ID" ;;
    *)
      # Fallback: look up from cached fields (0 API calls)
      option_id=$(echo "$GH_CACHE_FIELDS" | jq -r ".fields[] | select(.name == \"Status\") | .options[] | select(.name == \"$new_status\") | .id")
      ;;
  esac

  if [ -z "$option_id" ] || [ "$option_id" = "null" ]; then
    echo "ERROR: Status '$new_status' not found in project."
    return 1
  fi

  # Single API call to update status
  gh project item-edit --project-id "$GH_PROJECT_ID" --id "$item_id" \
    --field-id "$GH_STATUS_FIELD_ID" --single-select-option-id "$option_id"

  return $?
}
```

### Set Project Type

**Called when creating issues. 1 API call (uses cached IDs).**

```bash
set_project_type() {
  local item_id=$1
  local type=$2  # Feature, Bug, Chore, Research, Spike, Epic, Initiative

  # Get type field ID and option from cache (0 API calls)
  local type_field_id=$(echo "$GH_CACHE_FIELDS" | jq -r '.fields[] | select(.name == "Type") | .id')
  local option_id=$(echo "$GH_CACHE_FIELDS" | jq -r ".fields[] | select(.name == \"Type\") | .options[] | select(.name == \"$type\") | .id")

  if [ -z "$option_id" ] || [ "$option_id" = "null" ]; then
    echo "ERROR: Type '$type' not found in project."
    return 1
  fi

  # Single API call to update type
  gh project item-edit --project-id "$GH_PROJECT_ID" --id "$item_id" \
    --field-id "$type_field_id" --single-select-option-id "$option_id"
}
```

## State Queries via Project Board

**All queries use cached data. 0 API calls.**

### Get Issues by Status

**USE THIS instead of label queries. 0 API calls (uses cache).**

```bash
get_issues_by_status() {
  local status=$1  # Ready, In Progress, etc.

  # Use cached data (0 API calls)
  echo "$GH_CACHE_ITEMS" | jq -r ".items[] | select(.status.name == \"$status\") | .content.number"
}

# Examples:
# get_issues_by_status "Ready"
# get_issues_by_status "In Progress"
# get_issues_by_status "Blocked"
```

### Get Issues by Type

**0 API calls (uses cache).**

```bash
get_issues_by_type() {
  local type=$1  # Epic, Feature, etc.

  echo "$GH_CACHE_ITEMS" | jq -r ".items[] | select(.type.name == \"$type\") | .content.number"
}
```

### Get Epic Children

**0 API calls (uses cache).**

```bash
get_epic_children() {
  local epic_num=$1

  echo "$GH_CACHE_ITEMS" | jq -r ".items[] | select(.epic == \"#$epic_num\") | .content.number"
}
```

### Count by Status

**0 API calls (uses cache).**

```bash
count_by_status() {
  local status=$1

  echo "$GH_CACHE_ITEMS" | jq "[.items[] | select(.status.name == \"$status\")] | length"
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

**Valid transitions:**
```
Backlog → Ready → In Progress → In Review → Done
   ↓        ↓          ↓            ↓
   └────────┴──────────┴────────────┴──→ Blocked
                                            ↓
                                    (return to previous)
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
      echo "INVALID_TRANSITION: $current → $target"
      return 1 ;;
  esac
}
```

## Labels vs Project Board

**WRONG:** Using labels for state (`status:in-progress`)
**RIGHT:** Using project board Status field

Labels are only for supplementary info: `epic`, `epic-[name]`, `spawned-from:#N`, `review-finding`

## Sync Verification

Detect drift by comparing git branches to project board status:
- Issues with branches should be In Progress or In Review
- In Progress issues should have active branches

Use cached data (`GH_CACHE_ITEMS`) for 0 API calls. Example:

```bash
# Check if branch status matches project board
status=$(echo "$GH_CACHE_ITEMS" | jq -r ".items[] | select(.content.number == $issue) | .status.name")
```

## Error Messages

All project board errors provide actionable fixes:

| Error Code | Message | Fix |
|------------|---------|-----|
| NOT_IN_PROJECT | Issue not in project board | `gh project item-add ...` |
| NO_STATUS | Status field not set | Update Status field |
| INVALID_TRANSITION | Invalid state change | Use valid transition |
| PROJECT_NOT_FOUND | Project not accessible | Verify GITHUB_PROJECT_NUM |

## Integration

This skill is called by:
- `issue-driven-development` - All status transitions
- `issue-prerequisite` - After issue creation
- `epic-management` - Epic and child issue setup
- `autonomous-orchestration` - State queries and updates
- `session-start` - Sync verification
- `work-intake` - Project readiness check

This skill requires cache from:
- `github-api-cache` - Provides GH_CACHE_ITEMS, GH_CACHE_FIELDS, and field IDs

## Checklist for Callers

Before proceeding past any gate:

- [ ] **GitHub API cache initialized** (GH_CACHE_ITEMS, GH_CACHE_FIELDS set)
- [ ] Issue exists in project (verified from cache, not API call)
- [ ] Status field is set
- [ ] Type field is set
- [ ] Priority field is set (for new issues)
- [ ] Epic linkage set (if child of epic)
- [ ] Transition is valid (if changing status)

## API Cost Summary

| Operation | Before Caching | After Caching |
|-----------|----------------|---------------|
| verify_issue_in_project | 1 call | 0 calls |
| verify_status_set | 1 call | 0 calls |
| add_issue_to_project | 2 calls | 2 calls |
| set_project_status | 4 calls | 1 call |
| set_project_type | 3 calls | 1 call |
| get_issues_by_status | 1 call | 0 calls |
| count_by_status | 1 call | 0 calls |
| verify_project_sync (10 branches) | 10 calls | 0 calls |
