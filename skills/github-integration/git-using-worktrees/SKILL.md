---
name: git-using-worktrees
description: Use when starting feature work that needs isolation from current workspace or before executing implementation plans - creates isolated git worktrees in sibling directories with self-contained naming, pre-flight verification, and environment validation
---

# Using Git Worktrees

## Overview

Git worktrees create isolated workspaces sharing the same repository, allowing work on multiple branches simultaneously without switching. This skill sets up verified, working worktrees with clean git state and passing tests before ANY implementation begins.

**Core principle:** Pre-flight verification + systematic naming + environment validation = reliable isolation.

**Announce at start:** "I'm using the using-git-worktrees skill to set up an isolated workspace."

## Quick Start (Preferred)

Use the setup script for single-command worktree creation:

```bash
.claude/scripts/setup-worktree.sh <scope> <feature>
```

**Examples:**

```bash
.claude/scripts/setup-worktree.sh continuous-learning phase3-visibility
.claude/scripts/setup-worktree.sh ptsf-tools event-qr-codes
.claude/scripts/setup-worktree.sh citation-manager ast-refactor
```

The script handles all phases automatically:
- Pre-flight checks (clean git, passing tests)
- Cleanup of existing worktree (if any)
- Worktree + branch creation
- Dependency installation
- Test validation

**Output:** Worktree path and branch name for use in subsequent commands.

## When to Use

**Use this skill:**
- Before executing ANY implementation plan
- When user says "start implementing", "begin development", "execute the plan"
- Before starting feature work that needs isolation from current workspace
- When switching from design/planning to implementation phase

**Do NOT use this skill:**
- For exploratory prototypes in current directory
- For documentation-only changes
- When explicitly told to work in current directory

## Naming Convention

Worktrees use **self-contained naming** that includes repository context:

```text
{repo}.worktree.{scope}.{feature}
```

**Components:**
- `repo`: Repository name from `basename $(git rev-parse --show-toplevel)`
- `scope`: Package/area being worked on (e.g., `ptsf-tools`, `citation-manager`, `core`)
- `feature`: Feature name from plan file or user input (kebab-case)

**Examples:**
- `cc-workflows.worktree.ptsf-tools.event-qr-codes`
- `cc-workflows.worktree.citation-manager.ast-refactor`
- `myapp.worktree.core.user-auth`

**Branch name:** Same as worktree directory name, but use forward slashes for namespacing:
- Directory: `cc-workflows.worktree.ptsf-tools.event-qr-codes`
- Branch: `ptsf-tools/event-qr-codes`

## Location

Worktrees are created as **sibling directories** to the main repository:

```bash
# Structure
~/projects/
  ├── cc-workflows/                                          # Main repo
  ├── cc-workflows.worktree.ptsf-tools.event-qr-codes/     # Worktree 1
  └── cc-workflows.worktree.citation-manager.ast-refactor/  # Worktree 2
```

**Why sibling directories:**
- Self-contained naming prevents collisions
- Outside repository (no .gitignore concerns)
- Enables concurrent work on multiple features
- Clear visual separation from main repo

## Mandatory Workflow

**EVERY step is required. NO exceptions. NO skipping due to time pressure, exhaustion, authority, or urgency.**

### Phase 1: Pre-Flight Checks

**CRITICAL:** Must verify clean state and passing tests BEFORE creating worktree.

1. **Check git status in current directory**

   ```bash
   git status
   ```

   - If dirty: STOP. Must commit or stash first
   - NO "we'll handle it later" - dirty state = merge conflicts later
   - NO "user already committed" assumption - VERIFY with git status

2. **Verify tests pass in current directory**

   ```bash
   npm test
   ```

   - If tests fail: STOP. Fix tests before creating worktree
   - NO "we can skip tests" - broken tests now = broken worktree
   - NO "senior engineer says skip" - engineers are fallible, tests are not

### Phase 2: Determine Naming

1. **Extract repository name**

   ```bash
   repo=$(basename "$(git rev-parse --show-toplevel)")
   # Example: cc-workflows
   ```

2. **Determine scope and feature**

   **From plan file path (if provided):**

   ```bash
   # If PLAN_FILE_PATH set, extract scope and feature
   # Example path: /path/to/packages/ptsf-tools/plans/event-qr-codes.md
   # Extracts: scope=ptsf-tools, feature=event-qr-codes

   if [[ -n "$PLAN_FILE_PATH" ]]; then
     # Try to extract scope from path (e.g., packages/ptsf-tools or tools/citation-manager)
     scope=$(echo "$PLAN_FILE_PATH" | grep -oP '(?:packages|tools)/\K[^/]+' | head -1)

     # Extract feature from plan filename (remove .md, convert to kebab-case)
     feature=$(basename "$PLAN_FILE_PATH" .md | tr '_' '-')
   fi
   ```

   **From user input (if no plan file):**
   - Ask for scope: "Which area/package is this for?" (e.g., ptsf-tools, core, api)
   - Ask for feature: "What feature are you implementing?" (e.g., event-qr-codes, user-auth)

3. **Construct names**

   ```bash
   worktree_dir="${repo}.worktree.${scope}.${feature}"
   branch_name="${scope}/${feature}"

   # Example results:
   # worktree_dir: cc-workflows.worktree.ptsf-tools.event-qr-codes
   # branch_name: ptsf-tools/event-qr-codes
   ```

### Phase 3: Clean Up Existing Worktree

**ASSUMPTION:** We start from scratch for this specific feature. Remove existing worktree if present.

1. **Check for existing worktree**

   ```bash
   git worktree list | grep "$worktree_dir"
   ```

2. **If worktree exists, remove it completely**

   ```bash
   # Get parent directory (where worktree siblings live)
   parent_dir=$(dirname "$(git rev-parse --show-toplevel)")

   # Remove worktree
   git worktree remove "$parent_dir/$worktree_dir" --force 2>/dev/null || true

   # Delete the branch
   git branch -D "$branch_name" 2>/dev/null || true
   ```

   - ALWAYS clean up completely before creating new worktree
   - NO "reuse existing worktree" - fresh start every time
   - NO "preserve work in progress" - commit to feature branch first

### Phase 4: Create Worktree

1. **Create worktree in sibling directory**

   ```bash
   # Get parent directory
   parent_dir=$(dirname "$(git rev-parse --show-toplevel)")
   worktree_path="$parent_dir/$worktree_dir"

   # Create worktree with new branch
   git worktree add "$worktree_path" -b "$branch_name"

   # Change to worktree directory
   cd "$worktree_path"
   ```

2. **Verify creation**

   ```bash
   git worktree list
   git branch --show-current  # Should show: ptsf-tools/event-qr-codes
   pwd                         # Should show: .../cc-workflows.worktree.ptsf-tools.event-qr-codes
   ```

### Phase 5: Environment Setup

Auto-detect and run appropriate setup based on project files:

```bash
# Node.js
if [ -f package.json ]; then
  npm install
fi

# Rust
if [ -f Cargo.toml ]; then
  cargo build
fi

# Python
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
fi
if [ -f pyproject.toml ]; then
  poetry install
fi

# Go
if [ -f go.mod ]; then
  go mod download
fi
```

### Phase 6: Verify Dependencies

```bash
# For Node.js projects
npm list --depth=0

# Check for missing peer dependencies or installation errors
# NO assumptions - VERIFY installation worked
```

### Phase 7: Test Validation

**Tests MUST pass before ANY implementation.**

```bash
npm test
```

- If tests fail: debug and fix, don't proceed
- NO "we'll fix test failures later" - later = never
- Tests verify the environment works correctly

### Phase 8: Ready State Confirmation

```text
Worktree setup complete:
- Location: /path/to/parent/cc-workflows.worktree.ptsf-tools.event-qr-codes
- Branch: ptsf-tools/event-qr-codes
- Dependencies: installed and verified
- Tests: passing

Ready to begin implementation.
```

**DO NOT** begin implementation without explicit user confirmation.

## Common Rationalizations - STOP and Follow Skill

When you're tempted to skip a step, you're rationalizing. Here are common excuses and why they're wrong:

| Excuse | Reality | Counter |
|--------|---------|---------|
| "We can handle committing later because implementation is urgent" | Dirty state = merge conflicts later. Commit NOW. | Time pressure is not an excuse. Follow the checklist. |
| "Since you've already done npm install, we don't need to run it again" | Worktrees are isolated. Each needs its own node_modules. | Sunk cost fallacy. Install dependencies NOW. |
| "Following senior engineer's guidance to skip tests" | Authority is not infallible. Tests verify environment works. | Tests are mandatory. No authority overrides this. |
| "I understand you're tired, so I'll minimize steps" | Sympathy = shortcuts = broken environment = more work later. | Exhaustion is not an excuse. Follow the checklist. |
| "It should work / we can fix errors later" | Assumptions fail. Errors compound. Verify NOW. | "Should" is not verification. Test NOW. |
| "Tests are probably fine since they passed before" | Environments drift. Dependencies change. Verify NOW. | Probably = assumption. Run tests NOW. |
| "We'll validate the environment after we start implementing" | Broken environment wastes implementation time. Verify BEFORE. | Defer = never. Validate NOW. |
| "Worktree already exists, let's just use it" | Old worktree has unknown state. Clean baseline required. | Delete and recreate. Fresh start every time. |
| "Can we save the work in the existing worktree?" | Commit to parent branch first if work is valuable. | Always start from scratch. No exceptions. |
| "User might want different naming" | Consistent naming prevents confusion. | Self-contained naming is mandatory. |
| "Should ask to be flexible" | Consistency > flexibility for worktrees. | Follow the naming pattern. No exceptions. |

## Red Flags - STOP Immediately

If you think ANY of these, you are rationalizing and MUST stop:

**Time Pressure Signals:**
- "X is urgent, we can skip Y"
- "This step will take too long"
- "We're under deadline pressure"

**Authority Signals:**
- "Senior engineer says skip tests"
- "Following [authority]'s guidance to skip X"
- "They know better than the checklist"

**Exhaustion/Sympathy Signals:**
- "User is tired, minimize steps"
- "They're frustrated, let's move faster"
- "I'll reduce steps to help them"

**Sunk Cost Signals:**
- "Already did X, no need to do Y"
- "This is duplicate work"
- "Waste of time to repeat X"

**Assumption Signals:**
- "Should work"
- "Probably fine"
- "We can fix it later"
- "Errors are minor"

**When you catch yourself thinking these:** STOP. Read the rationalization table. Follow the checklist exactly.

## Common Mistakes

### Mistake 1: Skipping git status check
**Symptom:** "I assumed current directory was clean"
**Fix:** ALWAYS run git status. NEVER assume.

### Mistake 2: Skipping npm install in worktree
**Symptom:** "node_modules not found" or "Cannot find module 'X'"
**Fix:** Worktrees are isolated. ALWAYS npm install in new worktree.

### Mistake 3: Skipping test validation
**Symptom:** Tests fail mid-implementation, wasting time
**Fix:** Run tests BEFORE implementation. Broken tests = stop and fix.

### Mistake 4: Using child directory pattern
**Symptom:** Created `.worktrees/feature-name` instead of sibling
**Fix:** Use parent directory: `../repo.worktree.scope.feature`

### Mistake 5: Inconsistent naming
**Symptom:** Branch name doesn't match worktree directory pattern
**Fix:** Directory uses dots, branch uses slashes (both follow same structure)

### Mistake 6: Skipping cleanup
**Symptom:** "git worktree add failed: 'path' already exists"
**Fix:** Always remove existing worktree completely before creating new one

## Example Workflow

```text
You: I'm using the using-git-worktrees skill to set up an isolated workspace.

[Phase 1: Pre-flight Checks]
$ git status
# clean

$ npm test
# all tests pass

[Phase 2: Determine Naming]
$ repo=$(basename "$(git rev-parse --show-toplevel)")
# repo: cc-workflows

# From plan file: /path/to/packages/ptsf-tools/plans/event-qr-codes.md
# scope: ptsf-tools
# feature: event-qr-codes

$ worktree_dir="cc-workflows.worktree.ptsf-tools.event-qr-codes"
$ branch_name="ptsf-tools/event-qr-codes"

[Phase 3: Clean Up]
$ git worktree list | grep "cc-workflows.worktree.ptsf-tools.event-qr-codes"
# (none found)

[Phase 4: Create Worktree]
$ parent_dir=$(dirname "$(git rev-parse --show-toplevel)")
$ worktree_path="$parent_dir/cc-workflows.worktree.ptsf-tools.event-qr-codes"
$ git worktree add "$worktree_path" -b "ptsf-tools/event-qr-codes"
$ cd "$worktree_path"

[Phase 5: Environment Setup]
$ npm install
# dependencies installed

[Phase 6: Verify Dependencies]
$ npm list --depth=0
# all dependencies present

[Phase 7: Test Validation]
$ npm test
# all tests pass

[Phase 8: Report]
Worktree setup complete:
- Location: /Users/dev/projects/cc-workflows.worktree.ptsf-tools.event-qr-codes
- Branch: ptsf-tools/event-qr-codes
- Dependencies: installed and verified
- Tests: passing

Ready to begin implementation.
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| Dirty git state | STOP. Commit or stash first |
| Tests failing | STOP. Fix tests before creating worktree |
| No plan file | Ask user for scope and feature |
| Worktree exists | Remove completely, then recreate |
| Dependencies fail | Debug and fix, don't proceed |
| Tests fail in worktree | Debug and fix, don't proceed |
| No package.json/Cargo.toml | Skip dependency install |

## Integration

**Called by:**
- **writing-plans** - REQUIRED when design is approved and implementation follows
- **executing-plans** or **subagent-driven-development** - Sets up environment for plan execution
- Any skill needing isolated workspace

**Pairs with:**
- **git-finishing-a-development-branch** - REQUIRED for cleanup after work complete
- **test-driven-development** - What to do after environment is verified

## Success Criteria

All must be true before implementation begins:

1. ✅ Git status shows clean state before setup
2. ✅ Tests pass in original directory (Phase 1)
3. ✅ Worktree created in sibling directory with self-contained name
4. ✅ Branch name uses forward slashes: `{scope}/{feature}`
5. ✅ Dependencies installed in new worktree
6. ✅ Tests pass in new worktree
7. ✅ Ready state confirmed to user
8. ✅ NO steps skipped due to time, authority, exhaustion, or assumptions

If ANY check fails: STOP. Debug. Fix. Then continue checklist.

**Remember:** Every shortcut now = compound problems later. Follow the checklist. Every. Single. Time.
