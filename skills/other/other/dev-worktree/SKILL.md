---
name: dev-worktree
description: This skill should be used when the user asks to "create an isolated worktree", "set up worktree for feature", "create a feature branch worktree", or needs workspace isolation with automatic dependency setup and test verification.
user-invocable: false
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

Co-Authored-By: Claude <noreply@anthropic.com>"
fi
```

**Description:** dev-worktree: check if .worktrees is gitignored and add if missing

### Step 2: Determine Branch Name

Extract from `.planning/PLAN.md` first line or infer from feature name:

**Run:**
```bash
# Extract from PLAN.md if exists
feature_name=$(grep -m1 '^# ' .planning/PLAN.md 2>/dev/null | sed 's/^# //' | tr '[:upper:] ' '[:lower:]-' | sed 's/[^a-z0-9-]//g')

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

### Step 5: Verify Clean Baseline (MANDATORY)

<EXTREMELY-IMPORTANT>
**You MUST run tests to verify baseline. This is not optional.**

A worktree without a verified baseline is a trap. You will not know if failures are yours or pre-existing.

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

**If tests fail:** Report failures and note that baseline has issues. Do NOT proceed silently.
**If tests pass:** Report clean baseline.

### Rationalization Prevention (Baseline Verification)

| Thought | Reality |
|---------|---------|
| "Tests will pass, they passed on main" | Worktree setup can break things. Verify. |
| "Baseline check takes too long" | Debugging pre-existing failures takes longer. Run now. |
| "I'll notice if something is broken later" | You won't know if the failure is yours or inherited. Run now. |
| "Dependencies installed fine, should be good" | Install success != test success. Run tests. |
| "Main branch is green, worktree will be too" | Worktree has different env, paths, symlinks. Verify independently. |

### Drive-Aligned Framing

**Claiming clean baseline without running tests is NOT HELPFUL — every failure becomes ambiguous and you can't tell if bugs are yours or inherited.** Your assumption is not verification.

### Why Skipping Hurts the Thing You Care About Most

| Your Drive | Why You Skip | What Actually Happens | The Drive You Failed |
|------------|-------------|----------------------|---------------------|
| **Helpfulness** | "Skip baseline to start faster" | Broken baseline infects all work, every failure is ambiguous | **Anti-helpful** |
| **Competence** | "I know the codebase well enough" | Your mental model is stale. The worktree reveals conflicts you didn't anticipate. | **Incompetent** |
| **Efficiency** | "Skip worktree setup to save time" | Merge conflicts later cost 10x the setup time | **Anti-efficient** |
</EXTREMELY-IMPORTANT>

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
