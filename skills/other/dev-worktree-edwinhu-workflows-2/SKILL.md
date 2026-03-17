---
name: dev-worktree
description: This skill should be used when the user asks to "create an isolated worktree", "set up worktree for feature", "create a feature branch worktree", or needs workspace isolation with automatic dependency setup and test verification.
---

# Create Development Worktree

Create an isolated git worktree for feature work, ensuring workspace isolation and clean baseline.

## The Process

### Step 1: Ensure .worktrees/ is Gitignored

**CRITICAL:** Verify worktree directory is gitignored to prevent accidental commits.

**Run:**
```bash
if ! git check-ignore -q .worktrees 2>/dev/null; then
  echo "Adding .worktrees/ to .gitignore"
  echo ".worktrees/" >> .gitignore
  git add .gitignore
  git commit -m "chore: add .worktrees/ to gitignore

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
fi
```

**Description:** dev-worktree: check if .worktrees is gitignored and add if missing

### Step 2: Determine Branch Name

Extract from `.claude/PLAN.md` first line or infer from feature name:

**Run:**
```bash
# Extract from PLAN.md if exists
feature_name=$(grep -m1 '^# ' .claude/PLAN.md 2>/dev/null | sed 's/^# //' | tr '[:upper:] ' '[:lower:]-' | sed 's/[^a-z0-9-]//g')

# Or ask user if needed
```

**Description:** dev-worktree: extract or prompt for feature name

Branch name format: `feature/${feature_name}`

### Step 3: Create Worktree

**Run:**
```bash
# Create worktree with new branch
git worktree add .worktrees/${feature_name} -b feature/${feature_name}

# Change to worktree directory
cd .worktrees/${feature_name}
```

**Description:** dev-worktree: create isolated git worktree with feature branch

### Step 4: Run Project Setup

Auto-detect and run setup based on project files:

**Run:**
```bash
# Node.js
if [ -f package.json ]; then
  npm install
fi

# Python
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
fi
if [ -f pyproject.toml ]; then
  poetry install || pip install -e .
fi
if [ -f pixi.toml ]; then
  pixi install
fi

# Rust
if [ -f Cargo.toml ]; then
  cargo build
fi

# Go
if [ -f go.mod ]; then
  go mod download
fi
```

**Description:** dev-worktree: auto-detect project type and install dependencies

### Step 5: Verify Clean Baseline (Optional)

Run tests to verify baseline if project has test suite:

**Run:**
```bash
# Examples - auto-detect test command
if [ -f package.json ] && grep -q '"test"' package.json; then
  npm test
elif [ -f Cargo.toml ]; then
  cargo test
elif [ -f pytest.ini ] || [ -f pyproject.toml ]; then
  pytest
elif [ -f go.mod ]; then
  go test ./...
fi
```

**Description:** dev-worktree: auto-detect and run project test suite

**If tests fail:** Report failures and note that baseline has issues.
**If tests pass:** Report clean baseline.

### Step 6: Report Ready

Report completion status:

```
✓ Worktree created: .worktrees/${feature_name}
✓ Branch: feature/${feature_name}
✓ Dependencies installed
✓ Tests passing (or note if failed)

Ready for implementation.
```

## Safety Checks

**Execute before creating worktree:**
- Verify .worktrees/ is gitignored
- Add to .gitignore if missing
- Commit gitignore change

**Execute after creating worktree:**
- Run project setup (npm install, etc.)
- Verify clean baseline with tests
- Report status

## Red Flags

**Critical - Never deviate from these rules:**
- Do not create worktree without verifying gitignore
- Do not skip project setup commands
- Do not proceed without reporting test status

**Critical - Always follow these rules:**
- Verify .worktrees/ is ignored before creating
- Auto-detect project type and run appropriate setup
- Report test baseline status

## Common Patterns

### Node.js Project
```bash
# .worktrees/ gitignored → create worktree → npm install → npm test
```

### Python Project
```bash
# .worktrees/ gitignored → create worktree → pixi install → pytest
```

### Rust Project
```bash
# .worktrees/ gitignored → create worktree → cargo build → cargo test
```

## Workflow Transition

After worktree creation, the workspace is ready. Proceed to dev-implement to start implementing tasks.

Current working directory: `.worktrees/${feature_name}`

All implementation work happens here, keeping main workspace clean.
