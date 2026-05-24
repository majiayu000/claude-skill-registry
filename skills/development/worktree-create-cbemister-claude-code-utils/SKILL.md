---
name: worktree-create
description: Create a new git worktree for parallel feature development with automatic plan initialization
---

# Create Git Worktree

Create a new git worktree for isolated feature development with automatic plan setup.

## When to Use

Use this when:
- Starting a new feature that will take multiple commits
- Want to work on multiple features in parallel
- Need to keep main branch clean while developing
- Want automatic plan/tracking integration

## Usage

```
/worktree-create feature-name [base-branch]
```

**Arguments:**
- `feature-name` - Name for the feature (will be kebab-cased)
- `base-branch` - Optional, defaults to main/master

## Instructions

### Step 1: Validate Inputs

Check the feature name:
```bash
# Ensure feature name is provided
if [ -z "$1" ]; then
  echo "Error: Feature name required"
  echo "Usage: /worktree-create <feature-name> [base-branch]"
  exit 1
fi

# Convert to kebab-case if needed
FEATURE_NAME=$(echo "$1" | tr '[:upper:]' '[:lower:]' | tr '_' '-' | tr ' ' '-')
```

### Step 2: Determine Base Branch

```bash
# Use provided base or detect default branch
if [ -n "$2" ]; then
  BASE_BRANCH="$2"
else
  # Detect if main or master
  if git show-ref --verify --quiet refs/heads/main; then
    BASE_BRANCH="main"
  elif git show-ref --verify --quiet refs/heads/master; then
    BASE_BRANCH="master"
  else
    echo "Error: Could not determine base branch"
    exit 1
  fi
fi

echo "Base branch: $BASE_BRANCH"
```

### Step 3: Check Current State

```bash
# Ensure we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
  echo "Error: Not in a git repository"
  exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
  echo "Warning: You have uncommitted changes"
  read -p "Continue anyway? (y/n) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
fi

# Fetch latest from remote
echo "Fetching latest from origin..."
git fetch origin
```

### Step 4: Create Worktree Directory Structure

```bash
# Create worktrees directory if it doesn't exist
mkdir -p worktrees

# Create the worktree with new branch
BRANCH_NAME="feature/$FEATURE_NAME"
WORKTREE_PATH="worktrees/$FEATURE_NAME"

echo "Creating worktree: $WORKTREE_PATH"
echo "Branch: $BRANCH_NAME"
echo "Based on: origin/$BASE_BRANCH"

git worktree add "$WORKTREE_PATH" -b "$BRANCH_NAME" "origin/$BASE_BRANCH"
```

### Step 5: Initialize Plan

Create a plan directory and initial plan file:

```bash
# Create plan directory
PLAN_DIR="plans/active/$FEATURE_NAME"
mkdir -p "$PLAN_DIR"

# Create initial plan file
cat > "$PLAN_DIR/plan.md" << 'EOF'
---
title: [Feature Name]
status: planning
worktree: $FEATURE_NAME
created: $(date +%Y-%m-%d)
phases: []
---

# [Feature Name]

## Overview
[Describe what this feature does and why it's needed]

## Success Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Phases

### Phase 1: [Phase Name]
**Status:** Pending

**Tasks:**
- [ ] Task 1
- [ ] Task 2

## Notes
[Any additional context, decisions, or considerations]

## Open Questions
- [ ] Question 1
- [ ] Question 2
EOF

echo "Plan created at: $PLAN_DIR/plan.md"
```

### Step 6: Output Success Message

```bash
echo ""
echo "✅ Worktree created successfully!"
echo ""
echo "📁 Location: $WORKTREE_PATH"
echo "🌿 Branch: $BRANCH_NAME"
echo "📋 Plan: $PLAN_DIR/plan.md"
echo ""
echo "Next steps:"
echo "1. cd $WORKTREE_PATH"
echo "2. Edit $PLAN_DIR/plan.md to define your plan"
echo "3. Start working on your feature"
echo ""
echo "When done:"
echo "- Use /worktree-sync to sync with $BASE_BRANCH"
echo "- Use /worktree-cleanup to remove worktree after merge"
```

## Example Usage

**Create feature worktree:**
```bash
/worktree-create user-authentication
```

Output:
```
Base branch: main
Fetching latest from origin...
Creating worktree: worktrees/user-authentication
Branch: feature/user-authentication
Based on: origin/main
✅ Worktree created successfully!

📁 Location: worktrees/user-authentication
🌿 Branch: feature/user-authentication
📋 Plan: plans/active/user-authentication/plan.md

Next steps:
1. cd worktrees/user-authentication
2. Edit plans/active/user-authentication/plan.md to define your plan
3. Start working on your feature
```

**Create from specific branch:**
```bash
/worktree-create bug-fix develop
```

## Worktree Best Practices

**Naming Conventions:**
- Features: `feature/feature-name`
- Bug fixes: `fix/bug-name`
- Experiments: `experiment/experiment-name`

**When to Use:**
- Long-running features (multiple commits)
- Parallel development (multiple features at once)
- Bug fixes that need context switching
- Code reviews (check out PR in separate worktree)

**When NOT to Use:**
- Quick one-commit fixes (just use regular git)
- Experimental changes you'll discard
- Very simple edits

## Troubleshooting

**Error: "fatal: 'worktrees/X' already exists"**
- Worktree already created
- Solution: `cd worktrees/X` or remove with `/worktree-cleanup X`

**Error: "fatal: invalid reference: origin/main"**
- Remote branch doesn't exist
- Solution: Specify correct base branch or fetch from origin

**Uncommitted changes warning:**
- You have changes in current worktree
- Either commit them or stash before creating new worktree
