---
name: orient
description: "Use at the start of an orchestrator session to understand project state and find available work"
allowed-tools: Read, Bash, Glob, Grep, Task
---

# Project Orientation

You are an orchestrating agent orienting to this project. Your goal is to build comprehensive context and identify parallelizable work streams.

**IMPORTANT**: Use extended thinking (ultrathink) throughout this process. Take your time to deeply analyze the project state.

## Phase 1: Project Discovery

### 1.1 Identify Project Root and Type

```bash
pwd
ls -la
git remote -v 2>/dev/null || echo "Not a git repo"
```

Determine:
- Project name
- Primary language/framework
- Monorepo vs single project

### 1.2 Read Core Documentation

Read these files IN ORDER (skip if not found):

1. **CLAUDE.md** - AI assistant guidelines (HIGHEST PRIORITY)
2. **AGENTS.md** - Multi-agent workflow documentation
3. **PROJECT_SPEC.md** - Project specification and requirements
4. **README.md** - Project overview and setup

For each file found, extract:
- Project purpose and goals
- Key architectural decisions
- Development workflow and commands
- Patterns and conventions to follow

### 1.3 Understand Project Structure

```bash
# Get directory structure (2 levels deep)
find . -type d -maxdepth 2 -not -path '*/\.*' -not -path './node_modules/*' -not -path './.venv/*' -not -path './venv/*' | head -50

# Identify key source directories
ls -la src/ app/ lib/ moneyprinter/ fastapi_backend/ nextjs-frontend/ 2>/dev/null | head -30
```

Map out:
- Source code locations
- Test locations
- Configuration files
- Build/deployment setup

## Phase 1.5: Deep Research (Parallel)

When the project has significant complexity or unfamiliar patterns, run these research agents in parallel using the Task tool to build deeper context:

### Research Agents

1. **repo-research-analyst**
   - Read agent definition: `~/.claude/agents/research/repo-research-analyst.md`
   - Input: Project root path, file structure from Phase 1
   - Output: Convention guide, architecture map, code style patterns
   - Use when: New to the codebase, unfamiliar framework, or complex architecture

2. **git-history-analyzer**
   - Read agent definition: `~/.claude/agents/research/git-history-analyzer.md`
   - Input: Git repository path
   - Output: Contributor expertise areas, decision patterns, hot spots
   - Use when: Need to understand who knows what, or why decisions were made

### Launch Pattern

```
Use Task tool with subagent_type=general-purpose to run research agents in parallel:

Task 1: repo-research-analyst
- Read ~/.claude/agents/research/repo-research-analyst.md
- Analyze project structure and conventions
- Return: architecture summary, conventions guide

Task 2: git-history-analyzer
- Read ~/.claude/agents/research/git-history-analyzer.md
- Analyze git history for patterns
- Return: contributor map, decision patterns
```

### Incorporate Findings

Add research findings to the "CONTEXT FOR NEW SESSIONS" section of the orientation report:
- Key conventions discovered
- Architecture patterns identified
- Expert contributors for different areas
- Historical decisions that inform current work

### Skip Research If

- Already familiar with the codebase
- Small/simple project with clear structure
- Time-sensitive orientation (defer to later)

---

## Phase 1.7: Investigation Recommendation (Optional)

When the project state suggests ambiguity — multiple possible root causes, unclear architecture, or conflicting evidence — consider recommending an investigative dispatch before implementation.

**Indicators:**
- Tests failing with unclear cause
- Recent reverts or fix-on-fix commits in git log
- Task descriptions reference "investigate", "debug", "figure out"
- Stale branches from abandoned parallel work

**If investigation is warranted**, create investigation tasks in beads:

```bash
bd create --title="Investigate hypothesis A: <description>" --type=task --priority=1 --parent <epic-id>
bd create --title="Investigate hypothesis B: <description>" --type=task --priority=1 --parent <epic-id>
```

Then recommend in Phase 5:

"Investigation recommended before implementation dispatch.
Run `/dispatch --plan-first <task-A> <task-B>` to spawn investigators
who will plan their approach before diving in."

**Skip if:** Task board is clear, all ready tasks are straightforward, or user wants to proceed directly.

---

## Phase 2: Task State Analysis

### 2.1 Beads Overview

```bash
bd status 2>/dev/null || echo "Beads not configured"
```

### 2.2 Recently Completed Work

```bash
# Recent git activity
git log --oneline -15

# Recently closed tasks
bd list --status closed --sort closed --reverse --limit 10 2>/dev/null
```

Understand:
- What was just completed
- Patterns in recent work
- Momentum and direction

### 2.3 Epic Landscape

Gather epic-level data. This is the primary strategic view.

```bash
# Epic completion status (shows % done, child counts)
bd epic status 2>/dev/null

# All open epics with priority
bd list --type=epic 2>/dev/null

# Full dependency graph across all open issues
bd graph --all --compact 2>/dev/null
```

Classify epics into two tiers based on priority:
- **FOCUS** (P0-P1): Epics to actively progress this session
- **DEFERRED** (P2+): Epics acknowledged but not for now

**If no epics exist**, skip sections 2.4-2.5. Instead run `bd ready` and `bd list` directly, then proceed to Phase 3. The report will use the flat-task fallback template (see Phase 4 edge cases).

### 2.4 Primary Epic Drill-Down

Pick the single highest-priority FOCUS epic that has ready tasks. If multiple FOCUS epics share the same priority, pick the one with the most ready tasks. Drill into it:

```bash
# Task dependency graph within the epic
bd graph <epic-id> 2>/dev/null

# Ready tasks within this epic
bd ready --parent <epic-id> 2>/dev/null

# All children for full picture
bd list --parent <epic-id> 2>/dev/null
```

Gather details for ready and blocked tasks in a single batch:

```bash
# Show details for all children (ready, blocked, in-progress) at once
bd show <task-id-1> <task-id-2> <task-id-3> ...
```

From the output, identify:
- Critical path tasks (block the most downstream work)
- Independent tasks (can run in parallel)
- Research vs implementation tasks
- What each blocked task is waiting on
- What is already in-progress and who is working on it

**If no epic has ready tasks**, note that all focus epics are blocked and show what they're waiting on.

### 2.5 Orphan Tasks

Identify ready tasks not belonging to any epic:

```bash
# All ready tasks globally
bd ready 2>/dev/null
```

Cross-reference this output against the tasks already seen under epics (from `bd list --parent` in 2.4 and `bd epic status` in 2.3). Any task that appears in `bd ready` but was not listed under any epic is an orphan. These should still appear in dispatch recommendations.

### 2.6 Task Board Health Check

Run these 4 diagnostic checks. Report findings but do NOT auto-fix — the orchestrator decides what to act on.

**Check 1: Epic-as-Dependency Anti-Pattern**

Get all epics:
```bash
bd list --type=epic 2>/dev/null
```

For each non-epic open task, run `bd show <task-id>` and inspect the DEPENDS ON / BLOCKED BY fields. If any dependency target is an epic ID (from the list above), flag it.

Report format:
```
ANTI-PATTERN: <task-id> has blocks dependency on epic <epic-id>
  This creates deadlock — task is blocked by epic, but epic can't close until task closes.
  Fix (order matters!):
    bd dep remove <task-id> <epic-id>
    bd update <task-id> --parent <epic-id>
  WARNING: bd dep remove nukes ALL relationship types. Run BEFORE --parent, not after.
```

**Check 2: Orphan Task Affinity**

Extend the Phase 2.5 orphan detection. For each orphan task (ready task with no parent), compare its title and description keywords against existing epic titles/descriptions. If there's a clear match, suggest parenting.

Report format:
```
ORPHAN: <task-id> "<title>" — likely belongs to epic <epic-id> "<epic title>"
  Fix: bd update <task-id> --parent <epic-id>
```

**Check 3: File-Conflict Risk**

For each pair of ready tasks, read their descriptions (from `bd show`). If both mention the same file paths and have no dependency between them, flag a conflict risk.

Report format:
```
FILE CONFLICT RISK: <task-A> and <task-B> both target <file>
  No dependency between them — parallel dispatch may cause merge conflicts.
  Fix: bd dep add <lower-priority-task> <higher-priority-task>
```

If no tasks document target files: "Target files not documented in task descriptions — cannot detect file conflicts."

**Check 4: Redundant Transitive Dependencies**

Parse `bd graph --all --compact` output. For each direct dependency edge A→C, check if there's an alternate path A→...→C through other nodes. If so, the direct edge is redundant noise.

Report format:
```
REDUNDANT: <task-A> → <task-C> (path exists: A → B → C)
  Fix: bd dep remove <task-A> <task-C>
  WARNING: Only run if A and C have no parent-child relationship.
```

## Phase 3: Codebase Health Check

### 3.1 Test Status

```bash
# Quick test run to verify health
uv run pytest --tb=no -q 2>&1 | tail -10  # Python
pnpm test 2>&1 | tail -10                  # Node
```

### 3.2 Git State

```bash
git status
git branch -a | head -20
git worktree list
git stash list
```

Check for:
- Uncommitted changes
- Active worktrees/branches (parallel work in progress)
- Stashed work that needs attention

## Phase 4: Synthesis & Recommendations

After gathering all information, provide a structured orientation report. The report is organized as a **layered drill-down**: strategic overview → focused epic → actionable tasks.

```
===============================================
PROJECT ORIENTATION REPORT
===============================================

PROJECT IDENTITY
----------------
Name: <project name>
Purpose: <1-2 sentence description>
Stack: <key technologies>
Repo: <git remote URL>

HEALTH CHECK
------------
Git branch: <current branch>
Working tree: <clean/dirty>
Active branches: <count and purpose>
Test health: <passing/failing count>
Recently completed: <list last 3-5 items>

TASK BOARD HEALTH
-----------------
<If all checks pass:> All 4 checks passed.
<If issues found:>
<List each finding with its fix commands>

═══════════════════════════════════════════════
EPIC LANDSCAPE
═══════════════════════════════════════════════

▸ FOCUS EPICS (P0–P1) — progress these now
──────────────────────────────────────────────
<For each P0-P1 epic, show:>

  <epic-id>  <title>                          <status-icon> <completion%>
             <total> children: <done>✓ <ready>○ <blocked>● <in-progress>◐

<Example:>
  bd-10  Implement auth system               ◐ 40%
         10 children: 4✓ 3○ 2● 1◐

  bd-25  API rate limiting                    ○ 0%
         5 children: 0✓ 2○ 3●

▸ DEFERRED EPICS (P2+) — acknowledged, not now
──────────────────────────────────────────────
<For each P2+ epic, single line:>

  <epic-id>  <title>                          <completion%>

<Example:>
  bd-40  Admin dashboard redesign            0%
  bd-55  Migrate to new ORM                  15%

▸ DEPENDENCY MAP — how epics relate
──────────────────────────────────────────────
<Include the output of `bd graph --all --compact` here.>
<If no inter-epic dependencies, write: "No cross-epic dependencies defined.">

═══════════════════════════════════════════════
PRIMARY EPIC: <epic-id> — <epic title>
═══════════════════════════════════════════════

<This section drills into the single highest-priority FOCUS epic
that has ready tasks. Show its full task structure.>

▸ TASK DEPENDENCY GRAPH
──────────────────────────────────────────────
<Include the output of `bd graph <epic-id>` here.>
<This shows execution layers — layer 0 can start immediately,
higher layers depend on lower layers.>

▸ READY TASKS — can start immediately
──────────────────────────────────────────────
<For each ready task in this epic:>

  <task-id>  <title>
             Type: <feature/task/research>  Priority: <P0-P4>
             Blocks: <what this unblocks when done, or "nothing">

▸ IN PROGRESS — already claimed
──────────────────────────────────────────────
<For each in-progress task in this epic. Omit section if none.>

  <task-id>  <title>
             Assignee: <assignee or "unassigned">

▸ BLOCKED TASKS — waiting on dependencies
──────────────────────────────────────────────
<For each blocked task in this epic:>

  <task-id>  <title>
             Waiting on: <list of blocking task-ids and titles>

═══════════════════════════════════════════════
DISPATCH RECOMMENDATION
═══════════════════════════════════════════════

▸ ORPHAN TASKS — ready work outside any epic
──────────────────────────────────────────────
<Any ready tasks not belonging to an epic. Omit if none.>

  <task-id>  <title>
             Type: <type>  Priority: <P0-P4>

▸ RECOMMENDED STREAMS
──────────────────────────────────────────────
The following tasks can be executed simultaneously:

Stream 1: <task-id> - <title>
  Epic: <epic-id> - <epic title> (or "orphan" if no parent epic)
  Priority: <P0-P4>  Type: <feature/task/research>
  Rationale: <why this should be worked on>
  Blocks: <what this unblocks when done>
  Start command: /start-task <task-id>

Stream 2: <task-id> - <title>
  Epic: <epic-id> - <epic title> (or "orphan" if no parent epic)
  Priority: <P0-P4>  Type: <feature/task/research>
  Rationale: <why this should be worked on>
  Blocks: <what this unblocks when done>
  Start command: /start-task <task-id>

Stream 3: <task-id> - <title>
  Epic: <epic-id> - <epic title> (or "orphan" if no parent epic)
  Priority: <P0-P4>  Type: <feature/task/research>
  Rationale: <why this should be worked on>
  Blocks: <what this unblocks when done>
  Start command: /start-task <task-id>

<Streams may draw from the primary epic, other focus epics, or orphan tasks.
Prioritize tasks from the primary epic but include tasks from other focus epics
if they are independent and parallelizable.>

BLOCKERS & RISKS
----------------
<Any issues that could impede progress>
- <blocker 1>
- <blocker 2>

CONTEXT FOR NEW SESSIONS
------------------------
Key things any agent working on this project should know:
- <important pattern or convention>
- <gotcha or common mistake>
- <architectural constraint>

===============================================
END ORIENTATION REPORT
===============================================
```

### Report Edge Cases

Handle these gracefully:

- **No epics exist**: Skip the EPIC LANDSCAPE and PRIMARY EPIC sections entirely. Replace them with a flat task section:
  ```
  ═══════════════════════════════════════════════
  TASK OVERVIEW (no epics defined)
  ═══════════════════════════════════════════════
  Total open: <count>
  Ready (no blockers): <count>
  In progress: <count>
  ```
  Then proceed directly to DISPATCH RECOMMENDATION, omitting the "Epic:" line from each stream.

- **No dependencies defined**: Show the DEPENDENCY MAP section but write "No cross-epic dependencies defined. Consider adding dependencies with `bd dep add`."
- **No ready tasks in primary epic**: Show the PRIMARY EPIC section with only IN PROGRESS and BLOCKED TASKS. Note what needs to complete before work can proceed.
- **All epics same priority**: Show all as FOCUS. Add a note: "All epics are the same priority — consider differentiating with `bd update <id> --priority <N>`."
- **Primary epic has no children**: Show it in FOCUS EPICS but note "No tasks decomposed yet — consider breaking down with `bd create --parent <epic-id>`."

## Phase 5: Ready for Action

After presenting the orientation report, **ALWAYS offer `/dispatch` as the primary action when there are 2+ ready tasks.**

Present the following call-to-action:

---

"Orientation complete. **Recommended next step:**

```
/dispatch
```

This will spawn parallel Claude Code workers for the ready tasks. Each worker will:
1. Auto-receive their task assignment via the handoff queue
2. Create a task-specific branch for isolation
3. Run `/start-task <task-id>` automatically
4. Work autonomously until completion

You stay in THIS session as the orchestrator to coordinate as workers complete.

---

**Alternative options:**

1. **Dispatch workers** - Run `/dispatch` to spawn parallel workers (RECOMMENDED)
2. **Manual parallel** - Open separate terminals and run `/start-task <id>` in each
3. **Work solo** - Pick one task with `/start-task <id>` in this session
4. **Deep dive** - Explore a specific task or area in more detail
5. **Coordinate** - Help manage existing parallel work as tasks complete

What would you like to do?"

---

**CRITICAL**: You MUST present `/dispatch` prominently. Do not bury it in a list of options. The whole point of orientation is to enable parallel execution via dispatch.

Await user direction before taking action.
