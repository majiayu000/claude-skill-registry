---
name: check-history
description: ⚠️ MANDATORY - YOU MUST invoke this skill at the start of EVERY task. Reviews git history, status, and context before starting any work. Runs parallel git commands to understand current state, recent changes, and related work. NEVER gather git context manually.
version: 1.0.1
---

# Git History Context Skill

## ⚠️ MANDATORY SKILL - YOU MUST INVOKE THIS

## Purpose

This skill gathers comprehensive git context before starting any work. It helps understand the current state of the repository, recent changes, and identify related previous work.

**CRITICAL:** You MUST invoke this skill - NEVER gather git context manually with individual git commands.

## 🚫 NEVER DO THIS

- ❌ Running `git status` manually
- ❌ Running `git diff` manually
- ❌ Running `git log` manually
- ❌ Gathering git context with individual commands

**If you need git context, invoke this skill. Manual execution is FORBIDDEN.**

---

## ⚠️ SKILL GUARD - READ BEFORE USING BASH TOOL

**Before using Bash tool for git commands, answer these questions:**

### ❓ Are you about to run `git status`?

→ **STOP.** Invoke check-history skill instead.

### ❓ Are you about to run `git diff`?

→ **STOP.** Invoke check-history skill instead.

### ❓ Are you about to run `git log`?

→ **STOP.** Invoke check-history skill instead.

### ❓ Are you gathering git context at the start of a task?

→ **STOP.** Invoke check-history skill instead.

### ❓ Are you about to run multiple git commands in parallel (git status & git diff & git log)?

→ **STOP.** Invoke check-history skill instead.

**IF YOU PROCEED WITH BASH FOR THESE GIT COMMANDS, YOU ARE VIOLATING YOUR CORE DIRECTIVE.**

This skill runs these commands for you, in parallel, with proper analysis. Use it.

---

## Workflow

### Step 1: Run Parallel Git Status Commands

Execute these commands in parallel for efficiency:

```bash
git status & git diff & git log --oneline -10 &
```

**What to look for:**

- Current branch name
- Uncommitted changes (staged or unstaged)
- Untracked files
- Recent commit messages and their scope
- Commit patterns and conventions in use

### Step 2: Analyze Current State

Based on the parallel command output:

1. **Branch Status:**
   - Verify branch name follows `mriley/` prefix convention
   - Check if branch is ahead/behind remote
   - Note if on main/master vs feature branch

2. **Working Directory State:**
   - Identify any uncommitted changes
   - Note files that might conflict with planned work
   - Check for untracked files that might be relevant

3. **Recent Work:**
   - Review last 10 commits for context
   - Identify patterns in commit messages
   - Note any related work or recent changes in relevant areas

### Step 3: Search for Related Work (If Applicable)

If the task relates to a specific feature, bug, or area:

```bash
git log --grep="<keyword>" --oneline -10
```

**Example keywords:**

- Feature names (e.g., "auth", "parser", "api")
- Bug identifiers (e.g., "fix", "bug", "issue")
- Scope identifiers from conventional commits

### Step 4: Get Detailed Context (If Needed)

For more detailed information about recent changes:

```bash
git show --name-only HEAD                  # Files changed in last commit
git diff --name-only origin/main           # Files changed vs main branch
git log --graph --oneline -10              # Visual commit graph
```

### Step 5: Generate Context Summary

Provide a concise summary including:

1. **Current State:**
   - Branch: `<branch-name>`
   - Status: Clean working directory / Has uncommitted changes
   - Position: Up to date / Ahead by N commits / Behind by N commits

2. **Recent Activity:**
   - Last 3-5 relevant commits with their scope and purpose
   - Any ongoing work that might be related

3. **Relevant History:**
   - Related previous work (if found via grep)
   - Patterns or conventions observed

4. **Recommendations:**
   - Any concerns or conflicts to address
   - Suggested next steps based on current state

## Example Output

```
Git Context Summary:
==================

Current State:
- Branch: mriley/feat/user-authentication
- Status: Clean working directory
- Position: Ahead of origin/main by 2 commits

Recent Activity:
1. feat(auth): add JWT token generation (3 hours ago)
2. feat(auth): implement user login endpoint (5 hours ago)
3. test(auth): add unit tests for password hashing (1 day ago)

Relevant History:
- Found 3 commits related to "auth" in past week
- Project consistently uses conventional commits with scope
- Security-focused: all auth changes include tests

Recommendations:
- Safe to proceed with auth-related work
- Follow existing pattern: feature + tests in same commit
- Consider reviewing recent auth commits for context
```

## Error Handling

### If git command fails:

- Verify we're in a git repository
- Check git is installed and accessible
- Report error to user with specific command that failed

### If not in a git repo:

- Note this is not a git repository
- Skip git-specific checks
- Proceed with file system context if needed

## Integration with Other Skills

This skill should be invoked by:

- **`sparc-plan`** - Before creating implementation plans
- **`safe-commit`** - To understand what's being committed
- **`create-pr`** - To generate meaningful PR descriptions

## Best Practices

1. **Always run parallel commands** - Don't run git commands sequentially
2. **Be concise** - Summarize, don't dump raw git output
3. **Focus on relevance** - Highlight information relevant to the current task
4. **Note patterns** - Identify conventions and patterns in commit history
5. **Flag concerns** - Highlight any potential conflicts or issues early

---

## Related Commands

- **`/quick-status`** - Quick visual git dashboard (lighter weight alternative for simple status checks)
- **`/review-branch`** - Full branch code review against main
