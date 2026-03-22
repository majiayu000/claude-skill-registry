---
name: start-issue
description: |
  Start working on a GitHub issue with automated branch creation and planning.
  TRIGGER when: user wants to begin work on an issue (e.g., "start issue #23", "begin working on #45", "work on that bug", "let's tackle the auth issue").
  Also trigger when user mentions starting, picking up, or beginning any GitHub issue by number or description.
version: "2.2.0"
  DO NOT TRIGGER when: user just wants to view/list issues (use /issue instead), or close/finish issues (use /finish-issue).
---

# Start Issue - Begin Work on GitHub Issue

Automate the setup for working on a GitHub issue: fetch details, create branch, generate plan, and prepare environment.

## Overview

This skill handles the complete workflow to start working on a GitHub issue:

**What it does:**
1. Fetches issue details from GitHub (or creates new issue with `--create`)
2. Creates a feature branch with smart naming: `feature/{number}-{kebab-case-title}`
3. **Creates git worktree** for parallel development: `{repo}-{number}-{title}` (NEW)
4. **Switches to worktree directory** for isolated development environment (NEW)
5. Generates an implementation plan from the issue body
6. Syncs with main branch and sets up dependencies
7. Shows clear next steps to begin coding

**Why it's needed:**
Starting work on an issue involves many manual steps (fetch issue, create branch, push, write plan, sync). This skill automates the entire flow in ~30 seconds, ensuring consistency and saving 5-10 minutes of manual work.

**When to use:**
- User says "start issue #N" or similar phrasing
- User wants to "work on", "begin", "pick up" an issue
- User wants to create and immediately start work on a new issue

Pairs with `/finish-issue` for complete issue lifecycle management.

## Arguments

```
$ARGUMENTS = "[issue-number] [options]" or "--create \"title\" [options]"
```

**Common usage:**
```bash
/start-issue #23
/start-issue #23 --no-plan
/start-issue --create "Fix login button" --label bug,P0
/start-issue #23 --branch-prefix fix
```

**Options:**
- `--create "title"` - Create new issue and start work
- `--label bug,P0` - Add labels when creating (use with --create)
- `--no-plan` - Skip plan generation
- `--no-worktree` - Skip worktree creation (use traditional branch switching) (NEW)
- `--branch-prefix fix` - Use custom prefix instead of "feature"
- `--dry-run` - Preview actions without executing
- `--force` - Override safety checks

## AI Execution Instructions

**CRITICAL: Worktree creation and task management**

When executing `/start-issue`, AI MUST follow this pattern:

### Step 1: Create 9 Workflow Tasks

```python
tasks = [
    TaskCreate(
        subject="Validate environment",
        description="Check not on feature branch, no uncommitted changes, gh authenticated",
        activeForm="Validating environment..."
    ),
    TaskCreate(
        subject="Fetch or create issue",
        description="Use gh issue view or gh issue create",
        activeForm="Fetching issue details..."
    ),
    TaskCreate(
        subject="Prepare branch name",
        description="Convert title to kebab-case: feature/{N}-{title}",
        activeForm="Preparing branch name..."
    ),
    TaskCreate(
        subject="Create git worktree + branch",
        description="Create worktree in ../{repo}-{N}-{title} unless --no-worktree",
        activeForm="Creating worktree..."
    ),
    TaskCreate(
        subject="Push branch to remote",
        description="Push new branch with -u flag",
        activeForm="Pushing branch..."
    ),
    TaskCreate(
        subject="Generate implementation plan",
        description="Create .claude/plans/active/issue-{N}-plan.md in worktree",
        activeForm="Generating plan..."
    ),
    TaskCreate(
        subject="Create todo list from plan",
        description="Parse plan tasks and create todos with TaskCreate",
        activeForm="Creating todos..."
    ),
    TaskCreate(
        subject="Sync and setup",
        description="Fetch origin, merge main, npm install if needed",
        activeForm="Syncing with main..."
    ),
    TaskCreate(
        subject="Report success with worktree info",
        description="Show next steps with CRITICAL worktree path instructions",
        activeForm="Finalizing setup..."
    )
]
```

### Step 2: Worktree Creation Logic

**Default behavior** (unless --no-worktree):
```python
# MUST create worktree in parent directory
worktree_dir = f"../{repo_name}-{issue_number}-{kebab_title}"

# Create worktree AND branch atomically
Bash(f'git worktree add "{worktree_dir}" -b "{branch_name}"')

# Switch to worktree directory
Bash(f'cd "{worktree_dir}"')

# Push branch to remote
Bash(f'git -C "{worktree_dir}" push -u origin "{branch_name}"')
```

**Critical**:
- Worktree directory is in PARENT of main repo (not inside it)
- Branch creation happens WITH worktree (not separately)
- All subsequent operations use worktree path

### Step 3: Plan Generation in Worktree

```python
# MUST write plan to worktree, not main repo
plan_file = f"{worktree_dir}/.claude/plans/active/issue-{issue_number}-plan.md"

# Plan MUST include worktree metadata
plan_content = f"""
# Issue #{issue_number}: {title}

**GitHub**: {issue_url}
**Branch**: {branch_name}
**Worktree**: {worktree_dir}  # CRITICAL - for subsequent skills
**Started**: {date}

...
"""

Write(plan_file, plan_content)
```

### Step 4: Success Message Format

**Output mode detection**:
- **Auto mode** (called by /work-issue): Minimal 3-line output
- **Interactive mode** (direct invocation): Concise summary ≤20 lines

**Auto mode output** (when called by /work-issue):
```python
# Detect if called by work-issue (check for .claude/.work-issue-state.json)
is_auto_mode = os.path.exists('.claude/.work-issue-state.json')

if is_auto_mode:
    print(f"""✅ Issue #{issue_number} started
Branch: {branch_name} | Worktree: {worktree_dir}
Plan: {worktree_dir}/.claude/plans/active/issue-{issue_number}-plan.md""")
else:
    # Interactive mode - show full context
    print(f"""
🎉 Ready to work on Issue #{issue_number}!

Worktree created: {worktree_dir}
Branch: {branch_name}

IMPORTANT CONTEXT FOR CLAUDE:

All subsequent operations for issue #{issue_number} MUST use the worktree path:
  {worktree_dir}

DO NOT use relative paths or the main repository directory.
Always use absolute paths with the worktree directory shown above.

Examples of CORRECT usage:
  Read: Read {worktree_dir}/.claude/plans/active/issue-{issue_number}-plan.md
  Edit: Edit {worktree_dir}/.claude/skills/...
  Git: git -C {worktree_dir} status

Examples of INCORRECT usage (DO NOT DO THIS):
  ❌ Read .claude/plans/active/issue-{issue_number}-plan.md
  ❌ Edit /Users/woo/dev/ai-dev/.claude/skills/...
  ❌ git status  # Missing -C flag
""")
```

### Step 5: Task Updates During Execution

```python
# Mark each task in_progress before execution
TaskUpdate(tasks[0], status="in_progress")
validate_environment()
TaskUpdate(tasks[0], status="completed")

TaskUpdate(tasks[1], status="in_progress")
issue = fetch_issue(issue_number)
TaskUpdate(tasks[1], status="completed")

# ... continue for all 9 tasks
```

## Workflow Steps

Copy this checklist to track progress:

```
Task Progress:
- [ ] Step 1: Validate environment
- [ ] Step 2: Fetch or create issue
- [ ] Step 3: Prepare branch name
- [ ] Step 4: Create git worktree + branch (unless --no-worktree)
- [ ] Step 5: Push branch to remote
- [ ] Step 6: Generate implementation plan
- [ ] Step 7: Create todo list from plan
- [ ] Step 8: Sync and setup
- [ ] Step 9: Report success with worktree info
```

Execute these steps in sequence:

### 1. Validate Environment

Check that it's safe to start:
- Not already on a feature branch (must be on main or similar)
- No uncommitted changes (or user confirms stash/commit)
- GitHub CLI is authenticated

If validation fails, show clear error with options to resolve.

### 2. Fetch or Create Issue

**For existing issue:**
```bash
gh issue view $ISSUE_NUMBER --json number,title,body,state
```

Extract issue title, body, and verify it's open (warn if closed).

**For --create flag:**
```bash
gh issue create --title "$TITLE" --label "$LABELS" --body "$BODY"
```

Parse the `--create "title"` and optional `--label`, `--body` from arguments.

### 3. Prepare Branch Name

Generate branch name from issue title:
- Convert to kebab-case: "Fix Login Bug" → "fix-login-bug"
- Truncate to 50 chars if needed
- Construct: `{prefix}/{number}-{kebab-title}` (default prefix: "feature")

Check if branch exists remotely; if yes, show options (checkout existing, delete and recreate, use different prefix).

**No branch creation yet** - the branch will be created by worktree in Step 4.

### 4. Create Git Worktree (unless --no-worktree)

Create an isolated worktree directory AND branch in one atomic operation:

**Default behavior** (create worktree + branch):
```bash
WORKTREE_DIR="../${REPO_NAME}-${ISSUE_NUMBER}-${KEBAB_TITLE}"
git worktree add "$WORKTREE_DIR" -b "$BRANCH_NAME"  # Creates branch AND worktree
cd "$WORKTREE_DIR"
git push -u origin "$BRANCH_NAME"  # Push new branch to remote
```

**Worktree naming convention:**
- Pattern: `{repo-name}-{issue-number}-{kebab-title}`
- Example: `ai-dev-116-fix-start-issue`
- Location: Parent directory of main repo

**If --no-worktree flag is set:**
```bash
# Fallback: checkout branch in current directory
git checkout "$BRANCH_NAME"
```

**Why use worktrees?**
- ✅ **Parallel development** - Work on multiple issues simultaneously
- ✅ **Clean main directory** - Original repo stays on main branch
- ✅ **Isolated environments** - Each issue in separate directory
- ✅ **No branch conflicts** - Switch between issues instantly

**After worktree creation:**
- Switch to worktree directory: `cd $WORKTREE_DIR`
- Worktree path is recorded in plan metadata (see Step 6)
- Subsequent operations use worktree path automatically
- Use `git worktree list` to see all active worktrees

### 5. Push Branch to Remote

After worktree + branch creation, push to remote:

```bash
cd "$WORKTREE_DIR"  # Already in worktree
git push -u origin "$BRANCH_NAME"
```

**Why push immediately?**
- ✅ Branch is tracked remotely
- ✅ Enables PR creation later
- ✅ Backup of branch created
- ✅ Team can see active work

**If --no-worktree** (fallback to traditional branch):
- Branch already pushed in create_branch()
- Skip this step

### 6. Generate Implementation Plan (unless --no-plan)

Create `.claude/plans/active/issue-{number}-plan.md` with:

**Structure:**
```markdown
# Issue #{number}: {title}

**GitHub**: [link]
**Branch**: {branch-name}
**Worktree**: {worktree-path} (if created)
**Started**: {date}

## Context
{issue body}

## Tasks
{extracted from issue body - look for checkboxes, numbered lists}

## Acceptance Criteria
{extracted from issue body - look for "Acceptance Criteria" section}

## Progress
- [ ] Plan reviewed
- [ ] Implementation started
- [ ] Tests added
- [ ] Ready for review

## Next Steps
1. Review this plan
2. Get first task: /next
3. Start implementation
4. When done: /finish-issue #{number}
```

**Why generate plans:** Plans create a single source of truth, make progress trackable, and give Claude context about the full scope of work.

### 7. Create Todo List from Plan

Parse the plan's `## Tasks` section and create Claude Code todos:

```
For each task in plan:
1. Use TaskCreate with subject, description, activeForm
2. Add blockedBy dependencies for sequential tasks
3. Enables visual progress tracking in Claude Code UI
```

**Example:** Plan with "Read legacy skill", "Create SKILL.md", "Add LICENSE.txt" becomes 3 linked todos.

### 8. Sync and Setup

Ensure working directory is ready:
```bash
git fetch origin
git merge origin/main
```

If `package.json` exists and `node_modules` is stale, run `npm install`.

Optionally run quick health check (don't block on failure).

### 9. Report Success

Show clear next steps with worktree information:

**If worktree was created:**
```
🎉 Ready to work on Issue #{number}!

Worktree created: {worktree-path}
Branch: {branch-name}

IMPORTANT CONTEXT FOR CLAUDE:

All subsequent operations for issue #{number} MUST use the worktree path:
  {worktree-path}

DO NOT use relative paths or the main repository directory.
Always use absolute paths with the worktree directory shown above.

Examples of CORRECT usage:
  Read: Read {worktree-path}/.claude/plans/active/issue-{number}-plan.md
  Edit: Edit {worktree-path}/.claude/skills/...
  Write: Write {worktree-path}/src/...
  Git: git -C {worktree-path} status
  Git: git -C {worktree-path} add .
  Git: git -C {worktree-path} commit -m "..."

Examples of INCORRECT usage (DO NOT DO THIS):
  ❌ Read .claude/plans/active/issue-{number}-plan.md  # Wrong - relative path
  ❌ Edit /Users/woo/dev/ai-dev/.claude/skills/...     # Wrong - main repo
  ❌ git status                                         # Wrong - no -C flag

Next steps:
  1. Review plan: cat {worktree-path}/.claude/plans/active/issue-{number}-plan.md
  2. Get first task: /next
  3. Start coding (use worktree path for all operations)!
  4. When done: /finish-issue #{number}

Current status:
  Main repo: {main-repo-path} (still on main branch)
  Worktree: {worktree-path} (on {branch-name})
  Plan: {worktree-path}/.claude/plans/active/issue-{number}-plan.md
```

**If --no-worktree was used:**
```
🎉 Ready to work on Issue #{number}!

Next steps:
  1. Review plan: cat .claude/plans/active/issue-{number}-plan.md
  2. Get first task: /next
  3. Start coding!
  4. When done: /finish-issue #{number}

Current status:
  Branch: {branch-name}
  Plan: .claude/plans/active/issue-{number}-plan.md
```

## Error Handling

Handle common failure scenarios gracefully:

**Already on feature branch:**
```
❌ Already on feature branch: feature/11-other-task

Options:
  1. Finish current work: /finish-issue #11
  2. Switch to main: git checkout main && /start-issue #23
  3. Force: /start-issue #23 --force
```

**Uncommitted changes:**
```
⚠️ Uncommitted changes detected

Options:
  1. Commit: git add . && git commit -m "WIP"
  2. Stash: git stash && /start-issue #23
  3. Force: /start-issue #23 --force
```

**Issue not found:**
```
❌ Issue #999 not found

Check:
  1. Issue number correct?
  2. Repository correct? Run: gh repo view
  3. Authentication valid? Run: gh auth status
```

**Branch already exists:**
```
⚠️ Branch feature/23-fix-bug already exists

Options:
  1. Checkout existing: git checkout feature/23-fix-bug
  2. Delete and recreate: git branch -D feature/23-fix-bug && /start-issue #23
  3. Use different prefix: /start-issue #23 --branch-prefix v2
```

## Examples

### Example 1: Start Existing Issue

**User says:**
> "hey can you start working on issue #37? i think it's about project cleanup"

**What happens:**
1. Fetch issue #37 details
2. Create branch: `feature/37-project-cleanup`
3. Generate plan at `.claude/plans/active/issue-37-plan.md`
4. Sync with main
5. Show ready message

**Time:** ~30 seconds

### Example 2: Create and Start New Issue

**User says:**
> "i found a bug - the login button is misaligned on mobile. create an issue and start work on it, label it bug and P1"

**What happens:**
1. Create issue: "Login button misaligned on mobile" with labels bug,P1
2. Get new issue number (e.g., #42)
3. Create branch: `feature/42-login-button-misaligned-mobile`
4. Generate plan
5. Ready to code

**Time:** ~45 seconds

### Example 3: Bugfix with Custom Prefix

**User says:**
> "start issue #48 but use 'fix' as the branch prefix since it's a bugfix"

**What happens:**
1. Fetch issue #48
2. Create branch: `fix/48-{title}` (not feature/)
3. Generate plan
4. Ready to code

**Time:** ~30 seconds

### Example 4: Skip Plan Generation

**User says:**
> "start issue #23 but skip the plan, I already know what to do"

**What happens:**
1. Fetch issue #23
2. Create branch
3. Skip plan generation
4. Ready to code (use /plan later if needed)

**Time:** ~15 seconds

## Integration

**Pairs with /finish-issue:**
```
/start-issue #23    # ← Start (30 sec)
# ... implement ...
/finish-issue #23   # ← Finish and close (2-3 min)
```

**Workflow integration:**
```
/issue list         # Browse open issues
/start-issue #23    # Begin work
/next               # Get first task from plan
# ... code ...
/review             # Self-review
/finish-issue #23   # Complete
```

**Plan file location:**
- Created: `.claude/plans/active/issue-{number}-plan.md`
- Used by: `/next` (get current task)
- Archived by: `/finish-issue` (moved to `.claude/plans/archive/`)

## Performance

- **Average time:** 30 seconds (with plan)
- **Without plan:** 15 seconds
- **With --create:** 45 seconds

Fast because:
- Minimal GitHub API calls
- Parallel operations where possible
- Skip npm install if node_modules is fresh

## Best Practices

1. **Start from main** - Ensures clean branch point
2. **Review issue first** - Understand scope before starting
3. **Let plan generate** - Auto-extraction saves time
4. **Use descriptive issue titles** - Branch names come from titles
5. **Follow workflow** - start → next → code → finish

## Task Management

**After each step completion**, update progress:

```
Step 1 done (Environment validated) → Use TaskUpdate if created
Step 2 done (Issue fetched) → Update task status
Step 3 done (Branch created without checkout) → Update task status
Step 4 done (Worktree created) → Update task status
Step 5 done (Plan generated) → Update task status
Step 6 done (Todos created) → Update task status
Step 7 done (Environment synced) → Update task status
Step 8 done (Success reported) → Mark workflow complete
```

This provides real-time visibility of progress.

## Final Verification

**Quick checklist before completion:**

```
- [ ] Branch created and pushed (without checkout)
- [ ] Worktree created (unless --no-worktree)
- [ ] Plan file exists in worktree (unless --no-plan)
- [ ] Worktree path recorded in plan metadata
- [ ] Todo list created from plan
- [ ] Synced with origin/main
- [ ] Ready message displayed with worktree info
- [ ] User knows to use worktree path for operations
```

If any critical item missing, troubleshoot before declaring success.

## Workflow Skills Requirements

This is a **workflow skill** and must follow the standard pattern:

1. **TaskCreate** at start - Create todo list for progress tracking
2. **TaskUpdate** during execution - Mark tasks in_progress → completed
3. **Verification checklist** - Final validation before completion

**See**: [WORKFLOW_PATTERNS.md](../WORKFLOW_PATTERNS.md) for complete implementation guide

## Related Skills

- **/eval-plan** - Validate plan before execution (Phase 1.5 - recommended next step)
- **/execute-plan** - Execute implementation plan (Phase 2 after eval-plan)
- **/finish-issue** - Complete issue workflow (Phase 4 - final step)
- **/work-issue** - Complete lifecycle with checkpoints (calls this skill)
- **/issue** - Issue management (list, view, close)
- **/plan** - Custom planning (if auto-plan isn't enough)
- **/next** - Get next task from plan

---

**Version:** 2.2.0
**Pattern:** Tool-Reference (guides Claude through workflow)
**Compliance:** ADR-001 ✅ | WORKFLOW_PATTERNS.md ✅
**Last Updated:** 2026-03-18
**Changelog:**
- v2.2.0: Added mode-aware output (2-3 lines auto, ≤20 lines interactive) (Issue #263)
- v2.1.0: Added worktree support
- v2.0.0: Initial worktree implementation
