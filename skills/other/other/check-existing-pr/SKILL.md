---
name: check-existing-pr
description: Check if pull request already exists for current branch to support workflow resumption and prevent duplicate PR creation
---

# Check Existing PR

## Purpose

Determine if a pull request already exists for the current feature branch to support smart workflow resumption and prevent duplicate PR creation.

## When to Use

- Conductor Phase 4 (before PR creation)
- Workflow resumption checks
- Before deciding to create new PR
- `load-resumption-state` skill

## Instructions

### Step 1: Get Current Branch

```bash
CURRENT_BRANCH=$(git branch --show-current)

if [ -z "$CURRENT_BRANCH" ]; then
  echo "❌ Error: Not in a git repository or detached HEAD"
  exit 1
fi

echo "Checking for PR on branch: $CURRENT_BRANCH"
```

### Step 2: Query GitHub for PRs

```bash
# Check for PR with current branch as head
PR_DATA=$(gh pr list --head "$CURRENT_BRANCH" --json number,title,url,state,isDraft 2>&1)

if [ $? -ne 0 ]; then
  echo "❌ Error: gh CLI failed"
  echo "$PR_DATA"
  exit 1
fi
```

### Step 3: Parse PR Data

```bash
# Check if any PRs returned
PR_COUNT=$(echo "$PR_DATA" | jq '. | length')

if [ "$PR_COUNT" -eq 0 ]; then
  # No PR exists
  PR_EXISTS=false
  echo "ℹ️ No PR found for branch: $CURRENT_BRANCH"

else
  # PR exists
  PR_EXISTS=true

  # Extract PR details (take first if multiple)
  PR_NUMBER=$(echo "$PR_DATA" | jq -r '.[0].number')
  PR_TITLE=$(echo "$PR_DATA" | jq -r '.[0].title')
  PR_URL=$(echo "$PR_DATA" | jq -r '.[0].url')
  PR_STATE=$(echo "$PR_DATA" | jq -r '.[0].state')
  PR_IS_DRAFT=$(echo "$PR_DATA" | jq -r '.[0].isDraft')

  echo "✅ Found PR #$PR_NUMBER: $PR_TITLE"
  echo "   State: $PR_STATE"
  echo "   Draft: $PR_IS_DRAFT"
  echo "   URL: $PR_URL"

  # Warn if multiple PRs
  if [ "$PR_COUNT" -gt 1 ]; then
    echo "⚠️ Multiple PRs found for this branch ($PR_COUNT total)"
  fi
fi
```

### Step 4: Check PR Checks Status (if exists)

```bash
if [ "$PR_EXISTS" = true ]; then
  # Get CI checks status
  CHECKS_DATA=$(gh pr checks $PR_NUMBER --json name,status,conclusion 2>/dev/null)

  if [ -n "$CHECKS_DATA" ]; then
    TOTAL_CHECKS=$(echo "$CHECKS_DATA" | jq '. | length')
    PASSING_CHECKS=$(echo "$CHECKS_DATA" | jq '[.[] | select(.conclusion == "success")] | length')
    FAILING_CHECKS=$(echo "$CHECKS_DATA" | jq '[.[] | select(.conclusion == "failure")] | length')
    PENDING_CHECKS=$(echo "$CHECKS_DATA" | jq '[.[] | select(.status == "in_progress" or .status == "queued")] | length')

    echo "   Checks: $PASSING_CHECKS passing, $FAILING_CHECKS failing, $PENDING_CHECKS pending"

    if [ "$FAILING_CHECKS" -gt 0 ]; then
      CHECKS_PASSING=false
    elif [ "$PENDING_CHECKS" -gt 0 ]; then
      CHECKS_PASSING="pending"
    else
      CHECKS_PASSING=true
    fi
  else
    CHECKS_PASSING="unknown"
  fi
fi
```

### Step 5: Determine Resumption Action

```bash
if [ "$PR_EXISTS" = true ]; then
  # Recommend resumption phase based on PR state
  case "$PR_STATE" in
    OPEN)
      if [ "$CHECKS_PASSING" = true ]; then
        RESUME_PHASE=6
        RESUME_ACTION="Final validation and merge"
      elif [ "$CHECKS_PASSING" = "pending" ]; then
        RESUME_PHASE=5
        RESUME_ACTION="Monitor CI checks"
      else
        RESUME_PHASE=5
        RESUME_ACTION="Fix failing CI checks"
      fi
      ;;

    MERGED)
      RESUME_PHASE="complete"
      RESUME_ACTION="Workflow already complete"
      ;;

    CLOSED)
      RESUME_PHASE="manual"
      RESUME_ACTION="PR closed - manual review needed"
      ;;
  esac
else
  RESUME_PHASE=4
  RESUME_ACTION="Create pull request"
fi
```

## Output Format

### PR Exists

```json
{
  "status": "success",
  "prExists": true,
  "pr": {
    "number": 45,
    "title": "feat: Add user dark mode preference toggle",
    "url": "https://github.com/user/repo/pull/45",
    "state": "OPEN",
    "isDraft": false,
    "checks": {
      "total": 5,
      "passing": 4,
      "failing": 1,
      "pending": 0,
      "status": false
    }
  },
  "resumption": {
    "phase": 5,
    "action": "Fix failing CI checks"
  }
}
```

### No PR

```json
{
  "status": "success",
  "prExists": false,
  "branch": "feature/issue-137-dark-mode",
  "resumption": {
    "phase": 4,
    "action": "Create pull request"
  }
}
```

### PR Merged

```json
{
  "status": "success",
  "prExists": true,
  "pr": {
    "number": 45,
    "state": "MERGED"
  },
  "resumption": {
    "phase": "complete",
    "action": "Workflow already complete"
  }
}
```

## Integration with Load Resumption State

Used by `load-resumption-state` skill:

```markdown
### Step 2: Analyze Git State

If feature branch exists:
  Use `check-existing-pr` skill:
  - Input: (uses current branch)
  - Output: PR status and resumption recommendation

  If PR exists:
    - State OPEN + checks passing → Resume Phase 6
    - State OPEN + checks pending → Resume Phase 5 (monitor)
    - State OPEN + checks failing → Resume Phase 5 (fix)
    - State MERGED → Workflow complete
    - State CLOSED → Manual review needed

  If no PR:
    → Resume Phase 4 (create PR)
```

## Integration with Conductor Phase 4

```markdown
### Phase 4: PR Creation

**RESUMPTION CHECK**: Before creating PR

Use `check-existing-pr` skill to verify no PR exists:

If PR exists:
  ⚠️ Skip PR creation
  → Jump to Phase 5 (Gemini Review)

If no PR:
  ✅ Proceed with PR creation
```

## Related Skills

- `load-resumption-state` - Uses this for resumption logic
- `create-pull-request` - Creates PR if none exists

## Error Handling

### gh CLI Not Available

```json
{
  "status": "error",
  "error": "GitHub CLI (gh) not installed or not authenticated"
}
```

### Branch Not Found

```json
{
  "status": "error",
  "error": "Branch not found on remote",
  "branch": "feature/issue-137-dark-mode"
}
```

## Notes

- Prevents duplicate PR creation
- Critical for workflow resumption
- Returns structured data for decision-making
- Handles edge cases (closed, merged, multiple PRs)
