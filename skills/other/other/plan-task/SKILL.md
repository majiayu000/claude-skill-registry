---
name: plan-task
description: >-
  Persist multi-step plans and task progress across Claude Code sessions. Use when starting work
  that may span multiple sessions, resuming incomplete plans, or updating task progress. Supports
  two modes: Git-tracked (shared via commits) and Issue-centric (issue tracker as primary source
  of truth, local scratchpad for sessions).
license: MIT
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Plan & Task Persistence

## Goal

Maintain plans and task progress across Claude Code sessions so that work can be resumed without losing context.

## Session Start / Post-Compaction / Session Resume

On new session start, after context compaction, or on session resume, perform the following:

1. **Consume checkpoints**: Check `.claude/context-checkpoints/` for any checkpoint files
   - Read each checkpoint file
   - Integrate modified file lists and user decisions into the active task's `context-*.md`
   - If a checkpoint contains knowledge-worthy findings, invoke `record-knowledge`
   - Delete consumed checkpoint files
2. **Check incomplete work**:
   - **Git-tracked mode**: Read `.claude/tasks/readme.md` for active plans, then read the active task's latest `context-*.md` to restore detailed context
   - **Issue-centric mode**: Check assigned issues (e.g., `gh issue list --assignee=@me`) for open tasks
3. On progress update, also update the issue tracker (comments, checklists) if applicable.

## Progress Update Triggers

- **Explicit**: User says "progress update" or equivalent → execute immediately
- **Implicit**: User signals a break or completion (e.g., "thanks", "taking a break", "that's it for today") → suggest "Shall I update progress?" before proceeding
- **Milestone**: A significant chunk of work is completed → suggest "Shall I update progress?"

Progress update procedure:
1. Check related issues (`gh issue list`)
2. Post a progress comment (completed work, next steps, related work)
3. Update issue checklists if applicable
4. Commit and push if there are pending changes

## Setup

Copy the template files to `.claude/tasks/`:

```bash
mkdir -p .claude/tasks
cp assets/tasks-CLAUDE.md .claude/tasks/CLAUDE.md
cp assets/tasks-readme.md .claude/tasks/readme.md
```

For **Issue-centric mode**, also add `.claude/tasks/` to `.gitignore`.

## Two Modes

Choose the mode that fits your team's workflow:

| | Git-tracked mode | Issue-centric mode |
|---|---|---|
| Primary source of truth | `.claude/tasks/` (committed to Git) | Issue tracker (GitLab, GitHub, Jira, etc.) |
| `.claude/tasks/` role | Shared plan/task storage | Local working memo (gitignored) |
| Team visibility | Via Git commits | Via issue tracker |
| Best for | Small teams, single-repo projects | Teams already using an issue tracker |

### Issue-centric mode

When an issue tracker is the primary source of truth:

- `.claude/tasks/` is **gitignored** — add `.claude/tasks/` to `.gitignore`
- Plans and progress live in the issue tracker; `.claude/tasks/` is a local scratchpad for the current session
- Anything worth sharing with the team belongs in the issue tracker, not in `.claude/tasks/`
- At session start, check assigned issues in your tracker instead of `.claude/tasks/readme.md`

The rest of this document describes **Git-tracked mode**. For issue-centric mode, adapt the procedures below: use `.claude/tasks/` as a local memo and post shared artifacts to the issue tracker.

---

## Git-tracked mode

## When to Use

- Starting a multi-step task that may span multiple sessions
- Resuming work — check `.claude/tasks/readme.md` for incomplete plans
- Updating progress on an existing plan
- Closing out or archiving a completed plan

## Directory Naming

```
.claude/tasks/<slug>-<account>-<date>/           # Without issue reference
.claude/tasks/<slug>-i<issue>-<account>-<date>/  # With issue reference
```

- Separate components with `-` (hyphen)
- Separate words within slug with `_` (underscore)
- Slug uses lowercase alphanumeric only; date is YYYYMMDD
- Example: `docker_migration-alice-20260304/`
- Example: `auth_refactor-i42-bob-20260304/`

## Directory Structure

```
.claude/tasks/
├── readme.md                  # Index of all plans (status and summary)
├── <slug>-<account>-<date>/
│   ├── readme.md              # Handoff notes: current state, next actions, blockers
│   ├── plan-v1.md             # Initial plan (approach, design decisions, context)
│   ├── plan-v2.md             # Revised plan (v1 remains unchanged)
│   ├── todo.md                # Current task progress (frequently updated)
│   ├── context-*.md           # Session context: investigation details, trial & error, decisions
│   └── ...
```

### context-*.md (Session Context Files)

Captures detailed working context that is too granular for plan-vN.md but essential for resuming work after compaction or across sessions. Each file represents a focused context segment.

**Naming**: `context-YYYYMMDD-HHMMSS-topic.md`

**Format**:
```markdown
---
created: YYYY-MM-DD HH:MM:SS
status: active | consumed
tags: "#tag1 #tag2"
---

## HH:MM - <summary>

<details — investigation findings, configuration tried, error messages, decision rationale>
```

**Lifecycle**:
- **active**: Being written to during the current session
- **consumed**: Content has been integrated into knowledge entries or a new plan revision; kept for reference but not actively read on session start

**Source of truth hierarchy**:

| Information | Source of truth | Mirrors |
|-------------|----------------|---------|
| Plan approach & rationale | plan-vN.md | issue body |
| Task progress | todo.md | issue checklists |
| Detailed working context | context-*.md | (not mirrored) |
| Team-shared knowledge | knowledge entries | (not mirrored) |
| Team visibility & progress | issue | (authoritative) |
| Session handoff | readme.md | (not mirrored) |

## Creating a Plan

1. Create `.claude/tasks/<slug>-<account>-<date>/` following the naming convention
2. **Search related knowledge**: Grep `.claude/knowledge/entries/` for tags and keywords related to the plan's topic. Look for:
   - Past pitfalls (`#pitfall`) that may recur
   - Design decisions and their rationale
   - Related tooling or configuration knowledge
3. Write `plan-v1.md` with: approach, design decisions, background, completion criteria. If related knowledge was found in step 2, include a **Related Knowledge** section:
   ```markdown
   ## Related Knowledge
   - [entry title](../../knowledge/entries/slug.md) — why it's relevant
   ```
4. **Capture detailed context**: If the plan involves context too detailed for `plan-v1.md` (investigation results, API behavior, configuration specifics, design trade-off analysis), create `context-YYYYMMDD-HHMMSS-topic.md` in the task directory. Plans summarize *what* and *why*; context files preserve the *details* that future sessions need to resume work. Only invoke `record-knowledge` for findings that are universally valuable to the team beyond this specific task
5. Write `todo.md` with a checkbox task list
6. Write `readme.md` with the plan's purpose and current state
7. Add an entry to `.claude/tasks/readme.md`
8. **Issue sync**: If linked to an issue, update the issue body with the plan summary (approach, phases, completion criteria)

## Working on Tasks

- Update `todo.md` only — do not modify plan files
- Mark task status: `- [ ]` (pending) → `- [~]` (in progress) → `- [x]` (done)
- Record discovered issues or blockers indented below the relevant task
- Add new task lines to `todo.md` as work expands
- **Capture context incrementally**: When detailed findings emerge during work (investigation results, root causes, configuration specifics, trial & error), write them to `context-*.md` in the task directory. This is automated by the PostToolUse hook for file changes, but also write manually for reasoning, decisions, and analysis that don't correspond to file edits. This ensures details survive context compaction
- **Promote to knowledge selectively**: Only invoke `record-knowledge` for findings that are universally valuable beyond this specific task (team-shared pitfalls, reusable patterns, tool quirks). Task-specific details stay in `context-*.md`
- **Issue sync**: When updating `todo.md` or `readme.md`, also update the linked issue (if any) with the same progress. This is not optional — if an issue link exists, keep it in sync

### Issue Tracker Sync

If the plan is linked to an issue in your project's issue tracker:

- Check the issue for updates before starting work on `.claude/tasks/`
- Reflect any direction changes or new comments into `.claude/tasks/`
- Include the issue reference in commit messages
- Update the issue body or post a progress comment when task status changes

## Revising a Plan

- Do NOT edit existing `plan-vN.md` files — create `plan-vN+1.md` instead
- Reset `todo.md` to match the new plan (carry over incomplete items)
- Update `<slug>/readme.md` with which version is current and why the revision was needed
- Claude Code reads only the latest `plan-vN.md` and `todo.md`
- **Issue sync**: If linked to an issue, update the issue body to reflect the revised plan

## Committing Progress

- Commit when task progress changes (completion, blockers found, etc.)
- If linked to an issue, report progress there as well

## Pausing or Completing Work

### On session end or interruption

- Update `<slug>/readme.md` with handoff notes: current state, next actions, any blockers
- Mark completed context files as `status: consumed` if their content has been fully integrated
- Next session starts by checking `.claude/tasks/readme.md` for incomplete plans and reading active `context-*.md` files

### On plan completion

- Mark all tasks in `todo.md` as done
- Update `<slug>/readme.md` state to "completed"
- Move the entry in `.claude/tasks/readme.md` from the active table to the completed table
- **Issue sync**: If linked to an issue, update the issue with completion status and final summary
- **Knowledge extraction (retrospective)**: Review the completed work and extract lessons learned:
  1. Scan `context-*.md` files and `todo.md` for blockers, workarounds, and unexpected discoveries
  2. Check for overlap with existing knowledge entries to avoid duplication — Grep `.claude/knowledge/entries/` for key terms from the findings
  3. Compare the plan (what was expected) with the actual outcome (what happened)
  4. For each piece of **team-valuable** tacit knowledge found (not task-specific details), invoke `record-knowledge` to create an entry
  5. If related knowledge entries were referenced in the plan, update them with new findings
  6. Mark all context files as `status: consumed`
- **Retrospective prompt**: Notify the user with a brief summary:
  - What was completed
  - What knowledge was promoted from context to entries
  - Ask: "Are there lessons from this work not yet captured?"
