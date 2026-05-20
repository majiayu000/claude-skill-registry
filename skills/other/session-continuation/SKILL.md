---
name: session-continuation
description: Project-agnostic guidance for continuing work across Claude sessions. Ensures context recovery, task resumption, and state reconciliation.
---

# Session Continuation Skill

## Purpose

Guide Claude sessions to resume work intelligently by recovering context, identifying in-progress tasks, and reconciling state from previous sessions.

---

## Session Startup Hygiene Protocol (MANDATORY)

**BEFORE accepting user's work request, ALWAYS run these checks:**

### 1. Check Git Status
```bash
git status
```

**Look for:**
- **Uncommitted changes:** Modified or staged files from previous session
  - Action: Ask user "Commit or discard these changes?"
  - Never proceed with new work until resolved
- **Untracked files in `backlog/tasks/`:** Indicates MCP bypass (tasks created via Write instead of MCP tools)
  - Action: STOP immediately and alert user
  - These files won't be indexed by Backlog MCP
- **Current branch:** Feature work vs. main
- **Ahead/behind remote:** Unpushed commits

### 2. Check Backlog State
```bash
# Find orphaned In Progress tasks
mcp__backlog__task_list(status="In Progress")

# Find stale Done tasks needing archive
mcp__backlog__task_list(status="Done", limit=20)
```

**Look for:**
- **"In Progress" tasks:** Should typically be 0-1 (focus on one task at a time)
  - Action: Complete tasks with `task_complete(id)` or reset to "To Do" with `task_edit(id, status="To Do")`
  - Ask user: "Which task should I focus on?"
- **>10 "Done" tasks:** Indicates backlog clutter
  - Action: Archive completed tasks with `task_complete(id)` to move to completed/ folder
  - Keeps active backlog clean and focused

### 3. Report Findings to User

**Present hygiene check results BEFORE starting new work:**

**Example Report:**
```
Session startup hygiene check:

Git status:
- 2 uncommitted files: draft-1.md (1,200 words), research.md (updated citations)
- Recommendation: Commit these before starting new work?

Backlog state:
- 2 tasks In Progress: task-35.2 (first draft), task-36.1 (research)
- 15 tasks Done (not archived)
- Recommendation: Complete task-35.2 or reset to To Do? Archive Done tasks?

Please confirm cleanup approach before I proceed.
```

**This protocol prevents:**
- Lost work from uncommitted changes
- Blocking caused by orphaned In Progress tasks
- Backlog clutter from unarchived Done tasks
- Duplicate work from missing context

---

## Session Start Protocol

**Critical: Assess before acting. Never assume clean slate.**

### 1. Run Mandatory Hygiene Checks (see above)

Complete all cleanup actions before proceeding to context recovery.

### 2. Read Workflow Overview
```bash
# If MCP resources available:
Read backlog://workflow/overview

# If only tools available:
Call: mcp__backlog__get_workflow_overview()
```

**Why:** Understand project-specific task management conventions before searching.

### 3. Read Relevant CLAUDE.md Files

**Always read project documentation to understand current state:**

```bash
# Project root documentation
Read(file_path="/CLAUDE.md")

# If working in subdirectory, read that CLAUDE.md too
Read(file_path="/path/to/subdir/CLAUDE.md")

# Example: Working on Essay 6
Read(file_path="/essays/06-skills-crisis-build-vs-buy/CLAUDE.md")
```

**What to look for:**
- Project status and completion notes
- Known issues and blockers
- Next recommended actions
- Quality standards specific to that component
- Recent work artifacts and decisions

### 4. Search for Relevant Tasks
```bash
# Option 1: List all in-progress (after hygiene cleanup)
mcp__backlog__task_list(status="In Progress")

# Option 2: Search by keyword
mcp__backlog__task_search(query="<project-specific term>")

# Option 3: List recent tasks
mcp__backlog__task_list(limit=10)
```

**Priority order:** In Progress → assigned to you → recently modified → high priority

### 5. Assess Current State
Before responding to user, synthesize:
- Active tasks and their status
- Uncommitted changes and what they represent (if hygiene check found any)
- Blockers or dependencies
- Recommended next action (from CLAUDE.md or task notes)

**Report findings. Don't start work until user confirms direction.**

---

## Finding Existing Work

### Task Discovery Pattern

**1. Broad search first:**
```bash
mcp__backlog__task_list(status="In Progress", limit=20)
```

**2. Narrow by assignment:**
```bash
mcp__backlog__task_list(assignee="<your-name>", limit=10)
```

**3. Keyword search for topic:**
```bash
mcp__backlog__task_search(query="essay", status="In Progress")
```

**4. View full context:**
```bash
mcp__backlog__task_view(id="task-XX")
```

### What to Extract from Tasks

**From task metadata:**
- Title and description (what needs doing)
- Status (To Do, In Progress, Done)
- Assignee (who's responsible)
- Dependencies (what must complete first)
- Priority (urgency)

**From task notes:**
- Implementation plan (architectural decisions)
- Progress updates (what's been tried)
- Blockers (issues encountered)
- Commit references (where work is stored)

**From acceptance criteria:**
- Definition of done
- Quality standards
- Verification steps

---

## Resuming In-Progress Tasks

### Context Recovery Checklist

**Before continuing work:**

1. **Read task plan** (`task_view` → Implementation Plan section)
   - What approach was decided?
   - What architectural decisions were made?
   - Are there known issues flagged?

2. **Check implementation notes** (`task_view` → Notes section)
   - What's been completed?
   - Where did previous session stop?
   - Are there partial commits?

3. **Review git history**
   ```bash
   git log --oneline -10
   git diff
   ```
   - What was committed?
   - What's uncommitted (work in progress)?
   - Does git state match task notes?

4. **Identify continuation point**
   - Don't restart completed subtasks
   - Don't re-research already gathered information
   - Pick up where previous session left off

### Common Continuation Scenarios

**Scenario A: Task marked "In Progress" with commits**
- Previous session made progress and committed
- Read commits to understand what's done
- Continue with next subtask in plan

**Scenario B: Task marked "In Progress" with uncommitted changes**
- Previous session was interrupted mid-work
- Review uncommitted changes to understand intent
- Option 1: Commit work if complete
- Option 2: Continue work if incomplete
- Option 3: Discard if wrong direction (confirm with user)

**Scenario C: Task marked "In Progress" with no changes**
- Task was started but no progress made
- Previous session may have been planning-only
- Check task notes for decisions/blockers
- Start execution if plan exists

**Scenario D: Multiple tasks "In Progress"**
- Previous session was coordinating parallel work
- Identify highest priority or most advanced
- Complete one before switching (avoid context thrash)

---

## Context from Previous Session

### User Provides Handoff Message

**Common pattern:** User pastes final message from previous session:

```
Example handoff:
"Completed: task-35.1 (research compilation)
In Progress: task-35.2 (first draft - 40% done)
Blocked: task-35.3 (waiting for draft completion)
Next: Finish draft, then move to critique"
```

**Your response:**

1. **Verify against current state:**
   ```bash
   mcp__backlog__task_view(id="task-35.2")
   git status
   ```

2. **Reconcile discrepancies:**
   - Handoff says 40% done → Check files/commits for evidence
   - If missing: Ask user if work was committed
   - If present: Confirm continuation point

3. **Extract actionable items:**
   - What was completed (mark Done if not already)
   - What's in progress (resume here)
   - What's blocked (understand dependency)
   - Recommended next action (execute or propose alternative)

4. **Report reconciliation:**
   "Verified: task-35.1 is complete with commit abc123. Task-35.2 shows draft-1.md at 2,100 words (target 4,000-5,000). Resuming draft generation from Section 3."

### No Handoff Provided

**User says:** "Continue where we left off"

**Your protocol:**

1. Check In Progress tasks
2. Check git status
3. Synthesize state
4. Propose next action
5. Wait for confirmation

**Example response:**
"Found task-35.2 (first draft) marked In Progress. Git shows draft-1.md with 2,100 words uncommitted. Last commit was research completion. Recommend: Continue draft to 4,000-5,000 words, then commit. Proceed?"

---

## Session Handoff Protocol

### Ending a Session

**Before closing conversation, document:**

1. **Completed work:**
   - Task IDs marked Done
   - Commits with messages and SHAs
   - Files created/modified

2. **In-progress work:**
   - Task IDs still active
   - Current state (percentage, section, blocker)
   - Where to resume

3. **Blocked work:**
   - Task IDs waiting on dependencies
   - What's blocking (missing input, decision needed)
   - Estimated unblock timing

4. **Recommended next actions:**
   - What should happen next session
   - Priority order if multiple options
   - Dependencies to check

### Handoff Template

```
## Session Summary

**Completed:**
- [task-35.1] Research compilation → commit abc123
- [task-35.5] Editorial standards → commit def456

**In Progress:**
- [task-35.2] First draft (2,100/4,000 words, Section 3 incomplete)
  Resume: Continue Section 3, then Sections 4-5

**Blocked:**
- [task-35.3] Critique (waiting for draft completion)
  Unblock: After task-35.2 completes

**Next Session:**
1. Finish task-35.2 (first draft)
2. Commit draft when complete
3. Start task-35.3 (critique)
```

**Update task notes with this summary:**
```bash
mcp__backlog__task_edit(
  id="task-35.2",
  notesAppend=["Session ended: 2,100 words complete. Resume at Section 3."]
)
```

---

## Handling Stale State

### Detecting Stale State

**Indicators:**
- Task marked "In Progress" but last modified >24 hours ago
- No commits/notes since marked In Progress
- Multiple tasks In Progress with no clear priority
- Git shows uncommitted changes but task notes silent

### Resolution Pattern

**1. Assess legitimacy:**
- Is work actually in progress? (check files, commits)
- Was session interrupted? (no notes but partial work exists)
- Was task abandoned? (no evidence of work)

**2. Update task state:**

**If work exists but incomplete:**
```bash
mcp__backlog__task_edit(
  id="task-XX",
  notesAppend=["Resuming after interruption. Found partial work in <file>."]
)
```

**If task should be reset:**
```bash
mcp__backlog__task_edit(
  id="task-XX",
  status="To Do",
  notesAppend=["Reset to To Do - no progress evidence found."]
)
```

**If task should be completed:**
```bash
mcp__backlog__task_complete(id="task-XX")
# Then add completion notes
```

**3. Handle uncommitted changes:**

**If changes are valuable:**
```bash
git add <files>
git commit -m "[task-XX] Recovered work from previous session"
```

**If changes are experimental/broken:**
- Confirm with user before discarding
- Consider stashing: `git stash save "WIP from previous session"`

---

## Quick Start Checklist

**Every new session, before responding to user:**

### Hygiene Checks (MANDATORY - Do First)
- [ ] Run `git status` to check uncommitted work and untracked files
- [ ] Call `task_list(status="In Progress")` to find orphaned tasks
- [ ] Call `task_list(status="Done", limit=20)` to check for backlog clutter
- [ ] **Report hygiene findings to user BEFORE starting work**
- [ ] **Wait for user direction on cleanup actions**

### Context Recovery (After Hygiene Cleanup)
- [ ] Read `backlog://workflow/overview` or call `get_workflow_overview()`
- [ ] Read `/CLAUDE.md` (project overview)
- [ ] Read subdirectory `CLAUDE.md` if working in specific component
- [ ] Search for relevant tasks (after hygiene cleanup)
- [ ] If user provided handoff, call `task_view(id=...)` to verify
- [ ] Synthesize current state (completed, in-progress, blocked)
- [ ] Report findings to user with recommended next action
- [ ] Wait for user confirmation before executing work

**Never assume:**
- Clean slate (previous session may have left work)
- Task state is accurate (verify against files/commits)
- User wants to continue last task (ask for priorities)
- Backlog is clean (always run hygiene checks)

**Always verify:**
- Git status is clean (no uncommitted changes)
- Backlog state is focused (0-1 In Progress tasks, <10 Done tasks)
- What was done (commits, notes)
- What's pending (tasks, dependencies)
- What's blocked (missing inputs, decisions)

---

## Integration with Project Workflows

**This skill is project-agnostic.** Combine with project-specific skills:

- **Research compilation:** Continue gathering sources from where previous session stopped
- **Essay drafting:** Resume writing at last completed section
- **Code implementation:** Continue from last commit, check for breaking changes
- **Review processes:** Pick up review checklist from last verified item

**Key principle:** Never duplicate work. Always recover context before acting.
