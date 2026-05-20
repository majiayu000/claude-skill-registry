---
name: commit-with-validation
description: Create single atomic commit with proper message format, issue linking, and pre-commit hook validation for WescoBar workflows
---

# Commit with Validation

## Purpose

Create a single atomic commit with standardized message format, proper GitHub issue linking, and pre-commit hook execution, following WescoBar git discipline.

## When to Use

- Conductor workflow Phase 4, Step 2 (after all quality gates pass)
- After completing feature implementation
- Before creating pull request
- When all tests pass and audit score ≥ 8.0

## Commit Message Format

```
<type>: <subject>

<body>

Fixes #<issue-number>

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Types

- `feat` - New feature
- `fix` - Bug fix
- `refactor` - Code restructuring
- `test` - Test additions/changes
- `docs` - Documentation changes
- `chore` - Build/tooling changes

## Instructions

### Step 1: Validate Pre-Requisites

```bash
echo "→ Validating commit prerequisites..."

# Check we're on a feature branch
CURRENT_BRANCH=$(git branch --show-current)
if [[ ! "$CURRENT_BRANCH" =~ ^feature/ ]]; then
  echo "❌ Error: Not on feature branch (current: $CURRENT_BRANCH)"
  exit 1
fi

# Check there are staged or unstaged changes
if [ -z "$(git status --porcelain)" ]; then
  echo "❌ Error: No changes to commit"
  exit 1
fi

# Extract issue number from branch name
if [[ "$CURRENT_BRANCH" =~ feature/issue-([0-9]+) ]]; then
  ISSUE_NUMBER="${BASH_REMATCH[1]}"
  echo "✅ Issue number from branch: #$ISSUE_NUMBER"
else
  echo "⚠️ Warning: Cannot extract issue number from branch"
  echo "Enter issue number manually:"
  read ISSUE_NUMBER
fi
```

### Step 2: Build Commit Message

```bash
# Get commit type
echo "Select commit type:"
echo "  1. feat - New feature"
echo "  2. fix - Bug fix"
echo "  3. refactor - Code restructuring"
echo "  4. test - Tests"
echo "  5. docs - Documentation"
read -p "Choose (1-5): " TYPE_CHOICE

case $TYPE_CHOICE in
  1) COMMIT_TYPE="feat" ;;
  2) COMMIT_TYPE="fix" ;;
  3) COMMIT_TYPE="refactor" ;;
  4) COMMIT_TYPE="test" ;;
  5) COMMIT_TYPE="docs" ;;
  *) COMMIT_TYPE="feat" ;;
esac

# Get subject (from issue title or manual)
ISSUE_TITLE=$1  # Optional parameter

if [ -n "$ISSUE_TITLE" ]; then
  SUBJECT="$ISSUE_TITLE"
else
  echo "Enter commit subject:"
  read SUBJECT
fi

# Get body details (from implementation summary or manual)
IMPLEMENTATION_SUMMARY=$2  # Optional parameter

if [ -n "$IMPLEMENTATION_SUMMARY" ]; then
  BODY="$IMPLEMENTATION_SUMMARY"
else
  echo "Enter commit body (implementation details):"
  read BODY
fi
```

### Step 3: Format Commit Message

```bash
# Build commit message using heredoc
COMMIT_MESSAGE=$(cat <<EOF
${COMMIT_TYPE}: ${SUBJECT}

${BODY}

Fixes #${ISSUE_NUMBER}

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)

# Preview commit message
echo ""
echo "=== Commit Message Preview ==="
echo "$COMMIT_MESSAGE"
echo "============================="
echo ""
```

### Step 4: Stage All Changes

```bash
echo "→ Staging all changes..."

# Stage all changes (modified, new, deleted)
git add .

# Show what will be committed
echo ""
echo "Files to be committed:"
git diff --cached --name-status
echo ""

# Count changes
FILES_CHANGED=$(git diff --cached --name-only | wc -l)
echo "Total files: $FILES_CHANGED"
```

### Step 5: Validate Pre-Commit Requirements

```bash
# CRITICAL: Verify no --no-verify flag will be used
echo "⚠️ Pre-commit hooks will run (--no-verify is FORBIDDEN)"

# Check if pre-commit hooks exist
if [ -f .git/hooks/pre-commit ]; then
  echo "✅ Pre-commit hook found - will execute"
  HAS_HOOKS=true
else
  echo "ℹ️ No pre-commit hooks configured"
  HAS_HOOKS=false
fi
```

### Step 6: Create Commit

```bash
echo "→ Creating commit..."

# Create commit with message (hooks run automatically)
# NEVER use --no-verify (FORBIDDEN per CLAUDE.md)
if git commit -m "$COMMIT_MESSAGE"; then
  COMMIT_HASH=$(git rev-parse --short HEAD)
  echo "✅ Commit created: $COMMIT_HASH"
  COMMIT_SUCCESS=true
else
  COMMIT_EXIT_CODE=$?
  echo "❌ Commit failed (exit code: $COMMIT_EXIT_CODE)"
  COMMIT_SUCCESS=false
fi
```

### Step 7: Handle Pre-Commit Hook Failures

```bash
if [ "$COMMIT_SUCCESS" = false ]; then
  echo ""
  echo "⚠️ Pre-commit hooks may have failed or rejected commit"
  echo ""
  echo "Common causes:"
  echo "  - Linting errors"
  echo "  - Formatting issues"
  echo "  - Type errors"
  echo "  - Test failures"
  echo ""
  echo "Actions:"
  echo "  1. Check hook output above"
  echo "  2. Fix issues"
  echo "  3. Re-run commit-with-validation"
  echo ""
  echo "❌ DO NOT use --no-verify to bypass hooks"

  exit $COMMIT_EXIT_CODE
fi
```

### Step 8: Handle Hook Auto-Fixes

```bash
# If hooks modified files (e.g., prettier, eslint --fix)
if [ -n "$(git status --porcelain)" ]; then
  echo "⚠️ Pre-commit hooks modified files"
  echo ""
  echo "Modified files:"
  git status --short
  echo ""

  # Check if we should amend (ONLY if safe)
  LAST_COMMIT_AUTHOR=$(git log -1 --format='%an %ae')
  CURRENT_USER="$(git config user.name) $(git config user.email)"

  if [ "$LAST_COMMIT_AUTHOR" = "$CURRENT_USER" ]; then
    # Check not pushed
    if git status | grep -q "Your branch is ahead"; then
      echo "Options:"
      echo "  1. Amend last commit (add hook fixes)"
      echo "  2. Create new commit with hook fixes"
      read -p "Choose (1/2): " AMEND_CHOICE

      if [ "$AMEND_CHOICE" = "1" ]; then
        git add .
        git commit --amend --no-edit
        echo "✅ Commit amended with hook fixes"
      else
        git add .
        git commit -m "chore: Apply pre-commit hook fixes"
        echo "✅ Created separate commit for hook fixes"
      fi
    else
      echo "⚠️ Commit already pushed - creating new commit for fixes"
      git add .
      git commit -m "chore: Apply pre-commit hook fixes"
    fi
  else
    echo "⚠️ Last commit not by you - creating new commit"
    git add .
    git commit -m "chore: Apply pre-commit hook fixes"
  fi
fi
```

### Step 9: Verify Commit

```bash
echo ""
echo "=== Commit Summary ==="
git log -1 --stat
echo "======================"

# Return commit info
COMMIT_HASH=$(git rev-parse HEAD)
COMMIT_SHORT_HASH=$(git rev-parse --short HEAD)

echo ""
echo "✅ Commit successful"
echo "   Hash: $COMMIT_SHORT_HASH"
echo "   Message: ${COMMIT_TYPE}: ${SUBJECT}"
echo "   Issue: #${ISSUE_NUMBER}"
echo "   Files: $FILES_CHANGED"
```

## Output Format

### Success

```json
{
  "status": "success",
  "commit": {
    "hash": "a1b2c3d",
    "type": "feat",
    "subject": "Add user dark mode preference toggle",
    "issue": 137,
    "filesChanged": 12,
    "hookRan": true,
    "hookModified": false
  }
}
```

### Hooks Modified Files

```json
{
  "status": "success",
  "commit": {
    "hash": "a1b2c3d",
    "amended": true,
    "hookModified": true,
    "hookChanges": ["Prettier formatted 3 files", "ESLint fixed 2 issues"]
  }
}
```

### Commit Failed (Hooks Rejected)

```json
{
  "status": "error",
  "error": "Pre-commit hooks rejected commit",
  "issues": [
    "Linting errors in src/components/Settings.tsx",
    "TypeScript errors in src/types/index.ts"
  ],
  "action": "Fix issues and retry - DO NOT use --no-verify"
}
```

## Integration with Conductor

Used in conductor Phase 4, Step 2:

```markdown
### Phase 4: PR Creation and Documentation

**Step 2: Create SINGLE Atomic Commit**

⚠️ CRITICAL: This is the ONLY commit step in entire workflow.

Use `commit-with-validation` skill:
- Input: issue_number, issue_title, implementation_summary
- Pre-commit hooks: Will run automatically
- Validation: Tests, audit, build already passed (Phase 3)

Expected result:
- Single atomic commit with all changes
- Proper issue linking: Fixes #137
- Pre-commit hooks executed successfully
- Commit pushed to feature branch (not yet - push separately)

If hooks fail:
  → Fix issues
  → Re-run commit-with-validation
  → NEVER use --no-verify

If hooks modify files:
  → Option to amend commit (if safe)
  → Or create separate hook-fixes commit
```

## Git Discipline Rules

From CLAUDE.md:

### ✅ MUST Do

- Let pre-commit hooks run (they run automatically)
- Create single atomic commit per feature
- Use proper issue linking: `Fixes #123`
- Include co-authoring attribution
- Check authorship before amending

### ❌ NEVER Do

- `git commit --no-verify` (FORBIDDEN)
- Force push to main/development (destructive)
- Amend commits already pushed
- Amend other developers' commits
- Bypass hooks or validation

## Related Skills

- `create-pull-request` - PR creation after commit
- `push-with-retry` - Push commit with retry logic
- `quality-gate` - Pre-commit validation

## Best Practices

1. **One commit per feature** - Atomic changes only
2. **Run quality gates first** - Commit only after validation passes
3. **Let hooks run** - Never bypass with --no-verify
4. **Check authorship** - Before amending commits
5. **Use heredoc for messages** - Ensures proper formatting
6. **Link issues properly** - `Fixes #123` exact format

## Notes

- This is the ONLY commit point in conductor workflow
- All quality validation happens before this step
- Pre-commit hooks must succeed (no bypass)
- Amend only if safe (not pushed, your commit)
- Commit message format is standardized for consistency
