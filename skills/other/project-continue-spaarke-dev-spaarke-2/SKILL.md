---
description: Continue a project after PR merge or new session with full context loading
tags: [project, continue, resume, context, pr, merge]
techStack: [all]
appliesTo: ["projects/*/", "continue project", "resume project", "pick up where I left off"]
alwaysApply: false
---

# project-continue

> **Category**: Project Lifecycle
> **Last Updated**: January 2026

---

## Purpose

**Tier 2 Orchestrator Skill** - Resume work on an existing project after a PR merge, session break, or context compaction. This skill ensures:

1. Branch and PR status are verified and synced with master
2. Full project context is loaded (CLAUDE.md, plan.md, spec.md, etc.)
3. Work resumes from the correct task with proper state recovery
4. AI coding procedures and ADRs are followed

**Key Difference from task-execute**: This skill handles the **project-level** context setup (branch sync, PR status, all project files), while `task-execute` handles **task-level** context (specific POML file, knowledge files, step-by-step execution).

---

## When to Use

- After merging a PR to master and continuing development
- Starting a new Claude Code session on an existing project
- Resuming after context compaction (`/compact`)
- User says "continue project", "resume project", "pick up where I left off"
- User references a project that has existing artifacts (README.md, tasks/)
- **Trigger phrases**: "continue project", "resume project", "where was I on {project}", "pick up {project}", "continue work on {project}"

---

## Prerequisites

1. **Project exists**: `projects/{project-name}/` folder with at least README.md and tasks/
2. **Git configured**: Repository initialized with remote
3. **On a feature branch** (not master) or worktree exists for the project

---

## Workflow

### Step 1: Identify Project and Branch

```
IDENTIFY project:
  - If user provides project name: Use that
  - If in a worktree: Extract project from worktree path
  - If on a feature branch: Extract project from branch name (feature/{project-name})
  - If ambiguous: Ask user to specify

VERIFY project folder exists:
  - projects/{project-name}/README.md
  - projects/{project-name}/tasks/TASK-INDEX.md

IF project folder missing:
  → ERROR: "Project '{project-name}' not found. Run /project-pipeline to initialize."
  → STOP

IDENTIFY branch/worktree:
  - Check if in a git worktree (git worktree list)
  - If worktree: Note worktree path
  - If not worktree: Check current branch name
```

**Output to User:**
```
📁 Project: {project-name}
🌿 Branch: feature/{project-name}
📍 Location: {path or worktree info}

Checking sync status with master...
```

---

### Step 2: Sync with Master (Adapted from pull-from-github)

**Purpose:** Ensure branch is up-to-date with master to avoid conflicts and incorporate latest changes.

```powershell
# Check for local uncommitted changes
git status --porcelain
```

**Decision tree:**
```
IF has uncommitted changes:
  → WARN: "You have uncommitted changes:"
  → SHOW: modified files list
  → OPTIONS:
    1. "Stash changes, sync with master, restore" (recommended)
    2. "Commit changes first, then sync"
    3. "Continue without syncing" (risk conflicts later)
  → ASK user preference

IF no uncommitted changes:
  → PROCEED with sync
```

**Sync operations:**
```powershell
# Fetch latest from origin
git fetch origin

# Check if behind master
git log HEAD..origin/master --oneline

# Show divergence
git rev-list --left-right --count HEAD...origin/master
```

**If behind master:**
```
📥 Master has {N} new commits since your branch diverged.

Recent master commits:
  abc1234 feat(other): Some other feature
  def5678 fix(api): Bug fix

Options:
1. Merge master into your branch (recommended - preserves history)
2. Rebase onto master (cleaner history, but rewrites commits)
3. Skip sync (continue with current state)

[1/2/3 or skip]
```

**Execute sync (if chosen):**
```powershell
# Option 1: Merge (default)
git merge origin/master --no-edit

# Option 2: Rebase
git pull --rebase origin master

# Handle conflicts if any (delegate to user for manual resolution)
IF conflicts:
  → LIST conflicted files
  → STOP and ask user to resolve manually
  → After resolution: "Ready to continue? [y]"
```

**Output after sync:**
```
✅ Branch synced with master
   - {N} commits merged
   - No conflicts (or: Conflicts resolved)

Ready to load project context.
```

---

### Step 3: Check PR Status (if applicable)

```powershell
# Check if a PR exists for this branch
gh pr list --head $(git branch --show-current) --state open --json number,title,state,checksUrl
```

**If PR exists:**
```
📋 Open PR: #{number} - {title}
   Status: {Draft/Ready for Review}
   CI: {Passing/Failing/Pending}
   URL: {pr-url}

IF CI failing:
  → WARN: "CI is failing. You may want to address CI issues."
  → SHOW: Failed checks summary
  → ASK: "Continue anyway? [y/n]"
```

**If no PR:**
```
ℹ️ No open PR found for this branch.
   Consider creating one for visibility: /push-to-github
```

---

### Step 4: Load Project Context (MANDATORY)

**This step is critical for accurate continuation. Do NOT skip.**

```
LOAD all project files into context:

1. PROJECT ARTIFACTS (required):
   READ: projects/{project-name}/README.md
     → Extract: Project overview, graduation criteria, current status

   READ: projects/{project-name}/CLAUDE.md
     → Extract: Applicable ADRs, key services, skills to use

   READ: projects/{project-name}/plan.md
     → Extract: Phase structure, dependencies, architecture decisions

   READ: projects/{project-name}/spec.md
     → Extract: Requirements, success criteria, scope boundaries

2. TASK STATE (required):
   READ: projects/{project-name}/current-task.md
     → Extract: Active task, completed steps, next action, blockers

   READ: projects/{project-name}/tasks/TASK-INDEX.md
     → Extract: Task status overview, completed/pending counts

3. CODE INVENTORY (if exists):
   IF exists projects/{project-name}/CODE-INVENTORY.md:
     READ: CODE-INVENTORY.md
     → Extract: Files created/modified, key implementations
     → Note: This provides code-level context for continuation

4. RECENT NOTES (if useful):
   SCAN: projects/{project-name}/notes/
     → Check for recent files (modified in last 7 days)
     → Read any that provide implementation context
```

**Context Summary Output:**
```
✅ Project context loaded:

📄 Project Files:
   - README.md: {status from readme}
   - CLAUDE.md: {applicable ADRs count}
   - plan.md: {phase count} phases
   - spec.md: {word count} words

📋 Task State:
   - Active Task: {task-id} - {title}
   - Status: {in-progress/blocked/not-started}
   - Completed: {N}/{total} tasks
   - Next Action: {from current-task.md}

📁 Code Inventory: {Available/Not found}
   {If available: N files documented}

📝 Recent Notes: {count} files in notes/
```

---

### Step 5: Load ADRs and Skills (via adr-aware)

```
EXTRACT applicable ADRs from CLAUDE.md

FOR each ADR referenced:
  READ: .claude/adr/ADR-{XXX}.md (concise version)
  EXTRACT: Key constraints, MUST/MUST NOT rules

LOAD always-apply skills:
  - adr-aware
  - spaarke-conventions
  - script-aware
```

**Output:**
```
📐 ADRs Loaded:
   - ADR-001: Minimal API patterns
   - ADR-013: AI Architecture
   - ADR-015: AI Observability

✅ Always-apply skills active
```

---

### Step 6: Determine Resume Point

```
FROM current-task.md:

IF status == "in-progress":
  → This is a task continuation
  → EXTRACT: Current step, completed steps, files modified
  → REPORT: "Resuming task {id} at step {N}"

IF status == "blocked":
  → EXTRACT: Blocker description
  → REPORT: "Task {id} is blocked: {reason}"
  → ASK: "Blocker resolved? [y/n]"
  → IF yes: Continue task
  → IF no: Ask what user wants to do

IF status == "not-started" or "none":
  → CHECK TASK-INDEX.md for next pending task
  → REPORT: "Next task: {id} - {title}"
  → ASK: "Ready to start task {id}? [y]"

IF status == "completed" (all tasks done):
  → REPORT: "All tasks complete! Run /repo-cleanup to finalize."
```

---

### Step 7: Transition to Task Execution

```
IF ready to work on a task:
  → INVOKE task-execute skill with:
    - Task file path
    - Pre-loaded project context
    - Resume point (if continuing)

  → task-execute will:
    1. Load task-specific knowledge files
    2. Continue from correct step
    3. Track progress in current-task.md
```

**Final Output:**
```
✅ Project continuation ready!

📁 Project: {project-name}
🌿 Branch: feature/{project-name} (synced with master)
📋 PR: #{number} - CI {passing/failing}

📌 Resume Point:
   Task: {task-id} - {title}
   Step: {current step}/{total steps}
   Next: {next action from current-task.md}

Ready to continue. Proceeding with task execution...
```

---

## Guardrails and Best Practices

### Context Budget Awareness

```
BEFORE loading all project files:
  CHECK current context usage

  IF > 50%:
    → WARN: "Context at {X}%. Loading project files may approach limits."
    → SUGGEST: "Consider /compact before loading full context"

  IF > 70%:
    → CRITICAL: "Context too high to safely load project."
    → SUGGEST: "Run /compact first, then /project-continue"
    → STOP
```

### Human Escalation Triggers

**MUST request human input for:**
- Merge conflicts during master sync
- CI failures on PR that block progress
- Blockers noted in current-task.md
- Ambiguous resume points (multiple tasks in-progress)
- Security-sensitive changes detected in git diff

### State Preservation

```
ALWAYS verify current-task.md is accurate:
  - If discrepancy between current-task.md and actual files: WARN user
  - If task marked complete but files don't exist: FLAG as issue
  - If files modified outside task scope: NOTE for user awareness
```

### ADR Compliance

```
BEFORE starting any implementation work:
  - All applicable ADRs must be loaded (Step 5)
  - Any ADR violations from previous work should be flagged
  - New work must follow ADR constraints
```

---

## Error Handling

| Situation | Response |
|-----------|----------|
| Project folder not found | "Project '{name}' not found. Run /project-pipeline to initialize." |
| Not on feature branch | "You're on master. Checkout feature branch: git checkout feature/{name}" |
| Uncommitted changes | Offer stash/commit/skip options (Step 2) |
| Merge conflicts | List conflicts, stop for manual resolution |
| CI failing on PR | Warn user, offer to continue or address first |
| No current-task.md | "Task state missing. Check TASK-INDEX.md for progress." |
| Multiple tasks in-progress | "Ambiguous state. Which task to continue?" |
| Context budget high | Suggest /compact before proceeding |

---

## Examples

### Example 1: Resume After PR Merge

```
User: "continue project ai-document-intelligence-r3"

Agent:
  1. CHECK: Branch exists, worktree at C:/code_files/spaarke (main repo)
  2. SYNC: Fetch origin/master, merge 3 new commits
  3. PR: #96 merged, no open PR (this is post-merge continuation)
  4. LOAD: README, CLAUDE.md, plan.md, spec.md, current-task.md
  5. STATE: Task 045 in-progress, step 3 of 5 complete

Output:
  "✅ Project synced and context loaded.
   Resuming task 045 - Deploy to production
   Step 4: Run smoke tests

   Proceeding..."
```

### Example 2: New Session on Worktree Project

```
User: "where was I on the email automation project?"

Agent:
  1. IDENTIFY: email-to-document-automation project
  2. FIND: Worktree at C:/code_files/spaarke-wt-email-to-document-automation
  3. SYNC: 2 commits behind master, merge completed
  4. PR: #95 open, CI passing
  5. LOAD: All project files
  6. STATE: Task 012 not-started

Output:
  "✅ Email-to-Document Automation project ready.

   Last completed: Task 011 - Implement EML converter
   Next task: 012 - Add attachment handling

   PR #95 is open with passing CI.

   Ready to start task 012? [y]"
```

### Example 3: Blocked Task

```
User: "pick up where I left off"

Agent:
  1. IDENTIFY: Currently in project worktree
  2. SYNC: Already up to date
  3. LOAD: Project context
  4. STATE: Task 023 blocked - "Waiting for Azure AD app registration"

Output:
  "⚠️ Task 023 is blocked.

   Blocker: Waiting for Azure AD app registration
   Noted on: 2026-01-02

   Has this blocker been resolved? [y/n]

   Or choose another action:
   - 'skip' to move to next non-blocked task
   - 'update' to modify the blocker status"
```

---

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| `pull-from-github` | Step 2 uses sync patterns from this skill |
| `task-execute` | Step 7 hands off to task-execute for actual work |
| `adr-aware` | Step 5 loads ADRs using this always-apply skill |
| `push-to-github` | Use after completing work to commit/push |
| `project-pipeline` | Use if project doesn't exist yet |
| `repo-cleanup` | Use when all tasks complete |

---

## Related Files

- `projects/{name}/current-task.md` - Primary state recovery file
- `projects/{name}/tasks/TASK-INDEX.md` - Task status overview
- `projects/{name}/CLAUDE.md` - Project-specific AI context
- `projects/{name}/CODE-INVENTORY.md` - Code change tracking (if exists)

---

## Tips for AI

- **Always sync with master first** - Prevents painful merge conflicts later
- **Load ALL project files** - Partial context leads to inconsistent work
- **Respect current-task.md** - It's the source of truth for resume points
- **Check context budget early** - Better to compact before loading than run out mid-task
- **Verify PR status** - CI failures should be addressed before adding more code
- **Use CODE-INVENTORY.md** if available - It provides crucial code-level context
- **Don't skip ADR loading** - ADR violations are costly to fix later

---

*This skill ensures seamless project continuation across sessions, PR merges, and context boundaries.*
