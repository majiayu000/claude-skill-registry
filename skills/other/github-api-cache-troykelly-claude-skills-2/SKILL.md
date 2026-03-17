---
name: github-api-cache
description: MANDATORY before any GitHub project operations - caches project metadata to prevent rate limit exhaustion. Called by session-start. Other skills MUST use cached data.
allowed-tools:
  - Bash
  - mcp__github__*
model: opus
---

# GitHub API Cache

## Overview

Cache GitHub project metadata ONCE at session start. All subsequent operations use cached data.

**Core principle:** Fetch once, extract many. Never repeat API calls for the same data.

**This skill is called by `session-start` and provides cached data to all other skills.**

## The Problem

GitHub GraphQL API has a 5,000 point/hour limit. Without caching:
- `gh project item-list` = 1 call per invocation
- `gh project field-list` = 1 call per invocation
- `gh project list` = 1 call per invocation

A typical session startup was consuming 3,500+ of 5,000 points through repeated calls.

## The Solution

Fetch project metadata ONCE and cache in environment variables. All skills use cached data.

## Rate Limit Check

Before any bulk operations, check available quota:

```bash
check_github_rate_limits() {
  local graphql_remaining=$(gh api rate_limit --jq '.resources.graphql.remaining')
  local graphql_reset=$(gh api rate_limit --jq '.resources.graphql.reset')
  local rest_remaining=$(gh api rate_limit --jq '.resources.core.remaining')

  echo "GraphQL: $graphql_remaining remaining"
  echo "REST: $rest_remaining remaining"

  if [ "$graphql_remaining" -lt 100 ]; then
    local now=$(date +%s)
    local wait_seconds=$((graphql_reset - now + 10))
    echo "WARNING: GraphQL rate limit low. Resets in $wait_seconds seconds."
    return 1
  fi
  return 0
}
```

## Session Initialization (2 API Calls Total)

Run this ONCE at session start. Store results in environment.

```bash
# === GitHub API Cache Initialization ===
# Cost: 2 GraphQL API calls (field-list + item-list)

echo "Caching GitHub project metadata..."

# Verify environment
if [ -z "$GITHUB_PROJECT_NUM" ] || [ -z "$GH_PROJECT_OWNER" ]; then
  echo "ERROR: GITHUB_PROJECT_NUM and GH_PROJECT_OWNER must be set"
  exit 1
fi

# CALL 1: Cache all project fields
export GH_CACHE_FIELDS=$(gh project field-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" --format json)

# CALL 2: Cache all project items
export GH_CACHE_ITEMS=$(gh project item-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" --format json)

# Extract field IDs from cached data (NO API CALLS)
export GH_STATUS_FIELD_ID=$(echo "$GH_CACHE_FIELDS" | jq -r '.fields[] | select(.name == "Status") | .id')
export GH_TYPE_FIELD_ID=$(echo "$GH_CACHE_FIELDS" | jq -r '.fields[] | select(.name == "Type") | .id // empty')
export GH_PRIORITY_FIELD_ID=$(echo "$GH_CACHE_FIELDS" | jq -r '.fields[] | select(.name == "Priority") | .id // empty')

# Extract status option IDs from cached data (NO API CALLS)
export GH_STATUS_BACKLOG_ID=$(echo "$GH_CACHE_FIELDS" | jq -r '.fields[] | select(.name == "Status") | .options[] | select(.name == "Backlog") | .id')
export GH_STATUS_READY_ID=$(echo "$GH_CACHE_FIELDS" | jq -r '.fields[] | select(.name == "Status") | .options[] | select(.name == "Ready") | .id')
export GH_STATUS_IN_PROGRESS_ID=$(echo "$GH_CACHE_FIELDS" | jq -r '.fields[] | select(.name == "Status") | .options[] | select(.name == "In Progress") | .id')
export GH_STATUS_IN_REVIEW_ID=$(echo "$GH_CACHE_FIELDS" | jq -r '.fields[] | select(.name == "Status") | .options[] | select(.name == "In Review") | .id')
export GH_STATUS_DONE_ID=$(echo "$GH_CACHE_FIELDS" | jq -r '.fields[] | select(.name == "Status") | .options[] | select(.name == "Done") | .id')
export GH_STATUS_BLOCKED_ID=$(echo "$GH_CACHE_FIELDS" | jq -r '.fields[] | select(.name == "Status") | .options[] | select(.name == "Blocked") | .id')

# Get project ID (needed for item-edit) - extract from cached fields response
# Note: If project ID not available in fields, this requires 1 additional call
export GH_PROJECT_ID=$(gh project list --owner "$GH_PROJECT_OWNER" --format json --limit 100 | \
  jq -r ".projects[] | select(.number == $GITHUB_PROJECT_NUM) | .id")

echo "Cached: $(echo "$GH_CACHE_ITEMS" | jq '.items | length') project items"
echo "GraphQL calls used: 3"
```

## Cached Data Access Functions

These functions use ONLY cached data. NO API calls.

### Get Item ID from Issue Number

```bash
get_cached_item_id() {
  local issue_num=$1
  echo "$GH_CACHE_ITEMS" | jq -r ".items[] | select(.content.number == $issue_num) | .id"
}
```

### Get Item Status from Issue Number

```bash
get_cached_status() {
  local issue_num=$1
  echo "$GH_CACHE_ITEMS" | jq -r ".items[] | select(.content.number == $issue_num) | .status.name"
}
```

### Get Issues by Status

```bash
get_cached_issues_by_status() {
  local status=$1
  echo "$GH_CACHE_ITEMS" | jq -r ".items[] | select(.status.name == \"$status\") | .content.number"
}
```

### Get All Items with Status

```bash
get_cached_items_summary() {
  echo "$GH_CACHE_ITEMS" | jq -r '.items[] | {number: .content.number, title: .content.title, status: .status.name}'
}
```

### Check if Issue is in Project

```bash
is_issue_in_project() {
  local issue_num=$1
  local item_id=$(get_cached_item_id "$issue_num")
  [ -n "$item_id" ] && [ "$item_id" != "null" ]
}
```

## Cache Refresh

Only refresh cache when you KNOW data has changed:

```bash
refresh_items_cache() {
  # Cost: 1 API call
  export GH_CACHE_ITEMS=$(gh project item-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" --format json)
  echo "Items cache refreshed"
}
```

## Write Operations (Still Require API Calls)

Write operations cannot be cached. Use sparingly.

### Set Project Status (1 API call)

```bash
set_status_cached() {
  local item_id=$1
  local status_option_id=$2  # Use GH_STATUS_*_ID variables

  gh project item-edit --project-id "$GH_PROJECT_ID" --id "$item_id" \
    --field-id "$GH_STATUS_FIELD_ID" --single-select-option-id "$status_option_id"
}

# Example: Set to "In Progress"
# set_status_cached "$ITEM_ID" "$GH_STATUS_IN_PROGRESS_ID"
```

### Add Issue to Project (1 API call + cache refresh)

```bash
add_issue_to_project_cached() {
  local issue_url=$1

  gh project item-add "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" --url "$issue_url"

  # Refresh items cache after add
  refresh_items_cache
}
```

## Anti-Patterns (NEVER DO)

### Repeated Field Lookups

```bash
# WRONG: 3 API calls for same data
STATUS_FIELD=$(gh project field-list ... | jq '.fields[] | select(.name == "Status")')
TYPE_FIELD=$(gh project field-list ... | jq '.fields[] | select(.name == "Type")')
PRIORITY_FIELD=$(gh project field-list ... | jq '.fields[] | select(.name == "Priority")')

# RIGHT: 0 API calls (uses cached data)
STATUS_FIELD=$(echo "$GH_CACHE_FIELDS" | jq '.fields[] | select(.name == "Status")')
TYPE_FIELD=$(echo "$GH_CACHE_FIELDS" | jq '.fields[] | select(.name == "Type")')
PRIORITY_FIELD=$(echo "$GH_CACHE_FIELDS" | jq '.fields[] | select(.name == "Priority")')
```

### Polling Item List in Loops

```bash
# WRONG: N API calls for N items
for issue in 1 2 3 4 5; do
  gh project item-list ... | jq ".items[] | select(.content.number == $issue)"
done

# RIGHT: 0 API calls (uses cached data)
for issue in 1 2 3 4 5; do
  echo "$GH_CACHE_ITEMS" | jq ".items[] | select(.content.number == $issue)"
done
```

### Re-fetching Field IDs

```bash
# WRONG: API call every time you need to update status
STATUS_FIELD_ID=$(gh project field-list ... | jq -r '.fields[] | select(.name == "Status") | .id')

# RIGHT: Use cached environment variable
echo "$GH_STATUS_FIELD_ID"
```

## REST API for Simple Operations

When you need data not in the cache, prefer REST API (separate rate limit):

```bash
# REST API - uses separate 5,000/hour limit
gh api "repos/$OWNER/$REPO/issues/$ISSUE_NUM"
gh api "repos/$OWNER/$REPO/issues/$ISSUE_NUM/comments"

# MCP tools also use REST
mcp__github__get_issue(...)
mcp__github__list_issues(...)
```

## Environment Variables Reference

After initialization, these are available:

| Variable | Contents |
|----------|----------|
| `GH_CACHE_FIELDS` | Full project fields JSON |
| `GH_CACHE_ITEMS` | Full project items JSON |
| `GH_PROJECT_ID` | Project node ID |
| `GH_STATUS_FIELD_ID` | Status field ID |
| `GH_TYPE_FIELD_ID` | Type field ID |
| `GH_PRIORITY_FIELD_ID` | Priority field ID |
| `GH_STATUS_BACKLOG_ID` | Backlog option ID |
| `GH_STATUS_READY_ID` | Ready option ID |
| `GH_STATUS_IN_PROGRESS_ID` | In Progress option ID |
| `GH_STATUS_IN_REVIEW_ID` | In Review option ID |
| `GH_STATUS_DONE_ID` | Done option ID |
| `GH_STATUS_BLOCKED_ID` | Blocked option ID |

## API Cost Summary

| Operation | Before Caching | After Caching |
|-----------|----------------|---------------|
| Session init | 20-50 calls | 3 calls |
| Check issue status | 1 call | 0 calls |
| Get field IDs | 3 calls | 0 calls |
| Query by status | 1 call | 0 calls |
| Set status | 4 calls | 1 call |
| Sync verification | 10+ calls | 0 calls |

## Integration

This skill is called by:
- `session-start` - Initializes cache at session start

This skill's cached data is used by:
- `project-board-enforcement` - All verification functions
- `issue-driven-development` - Status updates and checks
- `issue-prerequisite` - Adding issues to project
- `epic-management` - Epic operations
- `autonomous-orchestration` - State queries

## Checklist

Before any GitHub project operation:

- [ ] Cache initialized (GH_CACHE_ITEMS exists and is not empty)
- [ ] Rate limit checked if bulk operation
- [ ] Using cached data for reads
- [ ] Only making API calls for writes
- [ ] Refreshing cache after writes that add items
