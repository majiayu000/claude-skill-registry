---
name: create-feature-branch
description: Create properly named feature branch from development with remote tracking, following WescoBar naming conventions and git best practices
---

# Create Feature Branch

## Purpose

Create a feature branch with proper naming convention, sync with remote development branch, and set up remote tracking for WescoBar workflows.

## When to Use

- Conductor workflow Phase 2, Step 1 (Branch Setup)
- Before starting implementation of new feature
- When picking up GitHub issue
- As first step in feature development workflow

## Naming Convention

```
feature/issue-<NUMBER>-<short-description>
```

**Examples:**
- `feature/issue-137-dark-mode`
- `feature/issue-42-character-portraits`
- `feature/issue-89-gemini-caching`

**Rules:**
- Always start with `feature/`
- Include `issue-<NUMBER>` for GitHub issue linking
- Use kebab-case for description
- Keep description under 40 characters
- Use descriptive but concise naming

## Instructions

### Step 1: Validate Inputs

```bash
ISSUE_NUMBER=$1
ISSUE_TITLE=$2  # Optional: for auto-generating description

if [ -z "$ISSUE_NUMBER" ]; then
  echo "❌ Error: Issue number required"
  exit 1
fi

# Validate issue number is numeric
if ! [[ "$ISSUE_NUMBER" =~ ^[0-9]+$ ]]; then
  echo "❌ Error: Issue number must be numeric"
  exit 1
fi
```

### Step 2: Generate Branch Name

```bash
# Generate short description from issue title if provided
if [ -n "$ISSUE_TITLE" ]; then
  # Convert to lowercase, replace spaces with hyphens, remove special chars
  SHORT_DESC=$(echo "$ISSUE_TITLE" | \
    tr '[:upper:]' '[:lower:]' | \
    sed 's/[^a-z0-9 ]//g' | \
    tr -s ' ' '-' | \
    cut -d'-' -f1-5)  # Keep first 5 words max
else
  # Manual description required
  echo "Enter short description (kebab-case):"
  read SHORT_DESC
fi

BRANCH_NAME="feature/issue-${ISSUE_NUMBER}-${SHORT_DESC}"

echo "Branch name: $BRANCH_NAME"
```

### Step 3: Check if Branch Already Exists

```bash
# Check local branches
if git rev-parse --verify "$BRANCH_NAME" 2>/dev/null; then
  echo "⚠️ Branch already exists locally: $BRANCH_NAME"
  echo "Options:"
  echo "  1. Checkout existing branch"
  echo "  2. Create new branch with different name"
  echo "  3. Delete and recreate"

  read -p "Choose (1/2/3): " CHOICE

  case $CHOICE in
    1)
      git checkout "$BRANCH_NAME"
      echo "✅ Checked out existing branch"
      exit 0
      ;;
    2)
      echo "Enter new description:"
      read NEW_DESC
      BRANCH_NAME="feature/issue-${ISSUE_NUMBER}-${NEW_DESC}"
      ;;
    3)
      git branch -D "$BRANCH_NAME"
      echo "Deleted existing branch - will recreate"
      ;;
  esac
fi

# Check remote branches
if git ls-remote --heads origin "$BRANCH_NAME" | grep -q "$BRANCH_NAME"; then
  echo "⚠️ Branch exists on remote: $BRANCH_NAME"
  echo "Fetching remote branch..."
  git fetch origin "$BRANCH_NAME"
  git checkout --track "origin/$BRANCH_NAME"
  echo "✅ Checked out remote branch"
  exit 0
fi
```

### Step 4: Sync with Development

```bash
echo "→ Syncing with development branch..."

# Checkout development
git checkout development

# Pull latest changes
if ! git pull origin development; then
  echo "❌ Error: Failed to pull latest development"
  echo "Resolve conflicts and try again"
  exit 1
fi

echo "✅ Development branch up to date"
```

### Step 5: Create Feature Branch

```bash
echo "→ Creating feature branch: $BRANCH_NAME"

# Create and checkout new branch
if ! git checkout -b "$BRANCH_NAME"; then
  echo "❌ Error: Failed to create branch"
  exit 1
fi

echo "✅ Feature branch created"
```

### Step 6: Push to Remote with Tracking

```bash
echo "→ Pushing to remote with tracking..."

# Push with upstream tracking
if ! git push -u origin "$BRANCH_NAME"; then
  echo "❌ Error: Failed to push to remote"
  echo "Branch created locally but not on remote"
  exit 1
fi

echo "✅ Branch pushed to remote with tracking"
```

### Step 7: Verify Setup

```bash
# Verify current branch
CURRENT_BRANCH=$(git branch --show-current)

if [ "$CURRENT_BRANCH" = "$BRANCH_NAME" ]; then
  echo ""
  echo "✅ Feature Branch Setup Complete"
  echo "   Branch: $BRANCH_NAME"
  echo "   Tracking: origin/$BRANCH_NAME"
  echo "   Base: development"
  echo ""
  echo "Ready for implementation!"
else
  echo "⚠️ Warning: Not on expected branch"
  echo "   Expected: $BRANCH_NAME"
  echo "   Actual: $CURRENT_BRANCH"
fi
```

## Output Format

### Success

```json
{
  "status": "success",
  "branch": {
    "name": "feature/issue-137-dark-mode",
    "issue": 137,
    "base": "development",
    "remote": "origin/feature/issue-137-dark-mode",
    "tracking": true
  },
  "message": "Feature branch created and pushed to remote"
}
```

### Branch Already Exists

```json
{
  "status": "success",
  "branch": {
    "name": "feature/issue-137-dark-mode",
    "existed": true,
    "action": "checked_out"
  },
  "message": "Existing branch checked out"
}
```

## Integration with Conductor

Used in conductor Phase 2, Step 1:

```markdown
### Phase 2: Branch Setup and Implementation

**Step 1: Create Feature Branch**

**RESUMPTION CHECK**: If feature branch already exists, SKIP this step.

Use `create-feature-branch` skill:
- Input: issue_number, issue_title (from Phase 1)
- Output: branch_name, tracking status

Expected result:
- Branch created: `feature/issue-137-dark-mode`
- Checked out and ready
- Remote tracking set up
- Base: development (latest)

Record branch name for PR creation in Phase 4.
```

## Error Handling

### Development Branch Pull Fails

```bash
if ! git pull origin development; then
  echo "❌ Merge conflicts in development branch"
  echo "Action required:"
  echo "  1. Resolve conflicts manually"
  echo "  2. Run: git merge --continue"
  echo "  3. Re-run create-feature-branch"
  exit 1
fi
```

### Remote Push Fails (Network)

```bash
# Retry with exponential backoff (from CLAUDE.md)
for i in {1..4}; do
  if git push -u origin "$BRANCH_NAME"; then
    break
  else
    if [ $i -lt 4 ]; then
      DELAY=$((2 ** i))
      echo "⏳ Push failed, retrying in ${DELAY}s..."
      sleep $DELAY
    else
      echo "❌ Push failed after 4 attempts"
      exit 1
    fi
  fi
done
```

### Branch Name Too Long

```bash
if [ ${#BRANCH_NAME} -gt 80 ]; then
  echo "⚠️ Branch name too long: ${#BRANCH_NAME} characters"
  echo "Truncating description..."
  SHORT_DESC=$(echo "$SHORT_DESC" | cut -c1-40)
  BRANCH_NAME="feature/issue-${ISSUE_NUMBER}-${SHORT_DESC}"
fi
```

## Related Skills

- `check-resume-branch` - Check if branch exists for resumption
- `push-with-retry` - Retry logic for network failures
- `commit-with-validation` - Atomic commit before PR

## Best Practices

1. **Always sync development first** - Ensures latest base
2. **Use descriptive names** - But keep under 80 chars
3. **Set up remote tracking** - Enables `git push` without args
4. **Verify branch created** - Check `git branch --show-current`
5. **Handle existing branches** - Don't overwrite without confirmation
6. **Retry on network failures** - Use exponential backoff

## Notes

- Branch naming follows WescoBar convention
- Remote tracking simplifies push workflow
- Development is the base branch (not main/master)
- Branch name includes issue number for PR auto-linking
- Supports resumption by checking for existing branches
