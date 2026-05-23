---
name: setting-up-implementation-worktree
description: Use when starting implementation work that needs isolation, before executing implementation plans, or when user says to begin development - creates clean worktree with verified environment, committed state, installed dependencies, and passing tests before ANY implementation begins
---

# Setting Up Implementation Worktree

## Overview

Before writing a single line of implementation code, create an isolated worktree with a verified, working environment. No shortcuts. No assumptions. No "we'll handle it later."

**CRITICAL ASSUMPTION:** This skill creates a FRESH worktree starting from scratch. If a worktree already exists for the current branch, it will be REMOVED and recreated. This ensures a clean baseline every time.

**IMPORTANT: Worktrees are for development work, not production deployment.** This skill verifies that the development environment works (tests pass, dependencies install correctly) but does NOT require production builds to succeed. Production build issues (like SSR incompatibilities) are irrelevant for development-focused worktrees. The worktree must support iterative development and testing, not production readiness.

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

## Mandatory Checklist

**EVERY step is required. NO exceptions. NO skipping due to time pressure, exhaustion, authority, or urgency.**

### Phase 1: Pre-Flight Checks

1. **Check git status in current directory**

   ```bash
   git status
   ```

   - If dirty: STOP. Must commit or stash first using `create-git-commit` skill
   - NO "we'll handle it later" - dirty state = merge conflicts later
   - NO "user already committed" assumption - VERIFY with git status

2. **Verify tests pass in current directory**

   ```bash
   npm test
   ```

   - If tests fail: STOP. Fix tests before creating worktree
   - NO "we can skip tests" - broken tests now = broken worktree
   - NO "senior engineer says skip" - engineers are fallible, tests are not

### Phase 1.5: Clean Up Existing Worktrees

**ASSUMPTION:** We start from scratch. If a worktree already exists, remove it completely.

1. **Check for existing worktrees for current branch**

   ```bash
   current_branch=$(git branch --show-current)
   worktree_branch="${current_branch}-worktree"
   git worktree list | grep "$worktree_branch"
   ```

2. **If worktree exists, remove it completely**

   ```bash
   # Remove worktree directory and entry
   git worktree remove .worktrees/$worktree_branch --force

   # Delete the branch
   git branch -D $worktree_branch
   ```

   - ALWAYS clean up completely before creating new worktree
   - NO "reuse existing worktree" - fresh start every time
   - NO "preserve work in progress" - commit to main branch first

### Phase 2: Worktree Creation

1. **Create worktree using `using-git-worktrees` skill**
   - Follow that skill's process exactly
   - Let it handle directory selection and safety verification
   - NO manual worktree creation - use the skill

### Phase 3: Environment Verification

**Note:** The `using-git-worktrees` skill already ran npm install. This phase VERIFIES it worked correctly.

1. **Verify dependencies installed correctly**

   ```bash
   npm list --depth=0
   ```

   - Check for missing peer dependencies
   - Check for installation errors
   - NO assumptions - VERIFY that the MECHANISM skill did its job

### Phase 4: Test Validation

1. **Run tests in NEW worktree**

   ```bash
   npm test
   ```

   - Tests MUST pass before ANY implementation
   - If tests fail: debug and fix, don't proceed
   - NO "we'll fix test failures later" - later = never

### Phase 5: Ready State Confirmation

1. **Confirm ready state to user**
   - Report worktree location
   - Report all checks passed
   - Report ready to begin implementation
   - DO NOT begin implementation without explicit user confirmation

## Common Rationalizations

When you're tempted to skip a step, you're rationalizing. Here are the excuses from baseline testing and why they're wrong:

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
| "Production build is failing, can't create worktree" | Worktrees are for development. Tests verify dev environment works. | Production builds are irrelevant for dev worktrees. |
| "We should fix the build issue before proceeding" | Build issues don't affect dev workflow if tests pass. | Tests passing = dev environment works. Proceed. |

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

**Production Build Confusion:**
- "Build must pass before creating worktree"
- "Can't proceed until production build works"
- "SSR/build errors block worktree creation"

**Remember:** Worktrees verify DEV environment (tests), NOT production builds. If tests pass, dev environment works.

**When you catch yourself thinking these:** STOP. Read the rationalization table. Follow the checklist exactly.

## Implementation

### Step-by-Step Process

#### Step 1: Pre-Flight in Current Directory

```bash
# Check for uncommitted changes
git status

# If dirty, use create-git-commit skill to commit
# (See ~/.claude/skills/create-git-commit/SKILL.md)

# Verify tests pass
npm test
```

#### Step 1.5: Clean Up Existing Worktrees

```bash
# Get current branch and worktree branch name
current_branch=$(git branch --show-current)
worktree_branch="${current_branch}-worktree"

# Check if worktree exists
if git worktree list | grep -q "$worktree_branch"; then
  echo "Existing worktree found. Cleaning up..."

  # Remove worktree (--force handles uncommitted changes)
  git worktree remove .worktrees/$worktree_branch --force

  # Delete the branch
  git branch -D $worktree_branch

  echo "Cleanup complete. Ready for fresh worktree."
fi
```

#### Step 2: Create Worktree

Use the `using-git-worktrees` skill to create the worktree:
- Invoke: `~/.claude/skills/using-git-worktrees/SKILL.md`
- Let it handle directory selection and safety checks
- It will create the worktree and switch you to it

#### Step 3: Verify Environment

```bash
# You are now in the new worktree directory
# The using-git-worktrees skill has placed you here and run npm install

# Verify dependencies installed correctly (MANDATORY - do not skip)
npm list --depth=0
```

#### Step 4: Validate Environment

```bash
# Run tests (MANDATORY - do not skip)
npm test

# All checks must pass. If any fail, debug and fix before proceeding.
```

#### Step 5: Confirm Ready

Report to user:

```text
Worktree setup complete:
- Location: /path/to/worktree
- Branch: feature-branch-name
- Dependencies: installed and verified
- Tests: passing

Ready to begin implementation.
```

**DO NOT** begin implementation without user confirmation.

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

### Mistake 4: Deferring to authority over checklist
**Symptom:** "Senior engineer says skip tests, so I did"
**Fix:** Authority is fallible. Checklist is not. Follow the checklist.

### Mistake 5: Sympathizing with user exhaustion
**Symptom:** "User is tired, I'll skip steps to help"
**Fix:** Shortcuts = more work later. Follow the checklist to ACTUALLY help.

### Mistake 6: Assuming environment works
**Symptom:** "It should work since it worked in main directory"
**Fix:** "Should" is not verification. Run the checks. Verify everything.

## Related Skills

- **using-git-worktrees**: Core worktree creation and management
- **create-git-commit**: Committing dirty state before worktree creation
- **test-driven-development**: What to do after environment is verified

## Success Criteria

You have successfully completed this skill when:

1. ✅ Git status shows clean state (before and after worktree creation)
2. ✅ Tests pass in original directory
3. ✅ Worktree created using `using-git-worktrees` skill
4. ✅ Dependencies installed in new worktree
5. ✅ Tests pass in new worktree
6. ✅ Ready state confirmed to user
7. ✅ NO steps skipped due to time, authority, exhaustion, or assumptions

If ANY check fails: STOP. Debug. Fix. Then continue checklist.

**Remember:** Every shortcut now = compound problems later. Follow the checklist. Every. Single. Time.
