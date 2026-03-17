---
name: commit
description: Quick commit with build verification
argument-hint: "[commit message]"
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
model: sonnet
---

# Quick Commit

Stage and commit changes with build verification.

## Usage
```
/commit "Add velocity display to HUD"
```

## Steps

### 0. Validate changes (NEW)

Run `/validate-changes` to ensure build and tests pass.

If validation fails:
- Report errors clearly
- Abort commit
- Suggest: Fix errors and try again

If validation passes, continue to next step.

### 1. Review changes
```bash
git status
git diff --stat
```

### 2. Check for Issue Reference

```bash
COMMIT_MSG="$ARGUMENTS"

# Check if commit message contains issue reference
if [[ "$COMMIT_MSG" =~ \#[0-9]+ ]]; then
    echo "✓ References issue(s) in commit message"
else
    # No issue reference found
    echo ""
    echo "💡 Consider referencing an issue with #NUMBER"
    echo ""
    echo "Recent open issues:"
    gh issue list --limit 5 2>/dev/null || echo "  (gh CLI not available)"
    echo ""
    echo "Commit message patterns:"
    echo "  - 'Fixes #N' to auto-close issue"
    echo "  - 'Refs #N' to link without closing"
    echo ""
fi

# Check if on issue branch
BRANCH=$(git branch --show-current)
if [[ "$BRANCH" =~ issue-([0-9]+) ]]; then
    ISSUE_NUM=${BASH_REMATCH[1]}
    echo "🔨 Currently on issue branch: issue-$ISSUE_NUM"

    if [[ ! "$COMMIT_MSG" =~ \#$ISSUE_NUM ]]; then
        echo "💡 Suggested: Add 'Refs #$ISSUE_NUM' or 'Fixes #$ISSUE_NUM' to message"
    fi
fi
```

### 3. Stage and commit
```bash
# Build commit message with issue reference reminder
COMMIT_MESSAGE="$ARGUMENTS"

# Add issue reference reminder if not present
if [[ ! "$COMMIT_MESSAGE" =~ \#[0-9]+ ]]; then
    # Check if on issue branch and suggest
    BRANCH=$(git branch --show-current)
    if [[ "$BRANCH" =~ issue-([0-9]+) ]]; then
        ISSUE_NUM=${BASH_REMATCH[1]}
        echo "Add issue reference to commit? (Fixes #$ISSUE_NUM / Refs #$ISSUE_NUM / Skip)"
        # If user adds reference, append to COMMIT_MESSAGE
    fi
fi

# Stage changes (review first with git status above)
git add -A

git commit -m "$(cat <<EOF
$COMMIT_MESSAGE

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

## Commit Message Guidelines
- Start with verb: Add, Fix, Update, Refactor, Remove
- Be specific
- Keep first line under 72 characters
- Reference issues when applicable:
  - `Fixes #N` - Auto-closes issue on merge
  - `Refs #N` - Links without closing
  - Include in body or first line

## Examples

```
Fix racer respawn velocity (Fixes #47)

Add lap counter to HUD (Refs #42)

Refactor collision detection
- Consolidate Bresenham logic
- Add path caching
Refs #35
```
