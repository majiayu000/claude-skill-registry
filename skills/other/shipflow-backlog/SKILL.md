---
name: shipflow-backlog
description: Manage backlog items - capture ideas, defer non-urgent tasks, and keep active work focused
disable-model-invocation: false
argument-hint: [optional: add "idea", move "defer", review, clean]
---

## Context

- Current directory: !`pwd`
- **Master TASKS.md** (has a "Backlog" section): !`cat /home/claude/shipflow_data/TASKS.md 2>/dev/null || echo "No master TASKS.md"`
- Local TASKS.md (if exists): !`cat TASKS.md 2>/dev/null || echo "No local TASKS.md"`
- Local BACKLOG.md (if exists): !`cat BACKLOG.md 2>/dev/null || echo "No BACKLOG.md"`
- Project CLAUDE.md: !`head -30 CLAUDE.md 2>/dev/null || echo "No CLAUDE.md"`
- Workspace CLAUDE.md: !`head -20 /home/claude/CLAUDE.md 2>/dev/null || echo "N/A"`
- Code TODOs: !`grep -r "TODO\|FIXME" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" --include="*.py" --include="*.sh" . 2>/dev/null | head -20 || echo "No TODOs found"`

## Multi-project tracking system

**CRITICAL**: This workspace tracks 12 projects from a single master file at `/home/claude/shipflow_data/TASKS.md`.

- The master TASKS.md has a **"Backlog (Ideas Parking Lot)"** section at the bottom — use it as the primary backlog
- When adding backlog items, **always prefix with the project name** (e.g., `- my-robots: CrewAI marketplace publishing`)
- When deferring tasks from a project, move them from the project's active section to the Backlog section in the master file
- When promoting backlog items, move them into the correct project's section in the master file

## Your task

Manage the backlog to keep active work focused and capture future ideas.

### Workspace root detection

If the current directory has no project markers (not inside a specific project) — you are at the **workspace root**. Use **AskUserQuestion**:
- Question: "Which project's backlog should I manage?"
- `multiSelect: false`
- Options:
  - **Full workspace** — "Manage backlog across all projects" (Recommended)
  - One option per project: label = project name, description = backlog item count

### Steps

1. **Understand user intent** from `$ARGUMENTS`:
   - `add [description]`: Add new idea/task to backlog
   - `defer`: Move non-urgent tasks from TASKS.md to backlog
   - `review`: Review backlog items for promotion to active tasks
   - `clean`: Remove outdated/irrelevant backlog items
   - No argument: General backlog organization

2. **If adding to backlog**:
   - Create BACKLOG.md if it doesn't exist
   - Add the idea with context, date, and category
   - Acknowledge addition and ask if it should be active now

3. **If deferring tasks**:
   - Review TASKS.md for low-priority or future items
   - Move them to BACKLOG.md with reason for deferral
   - Keep TASKS.md focused on current sprint/milestone
   - Update TASKS.md to remove deferred items

4. **If reviewing backlog**:
   - Read all backlog items
   - Identify items that should become active tasks:
     - Changed context making them relevant now
     - Prerequisites completed
     - Strategic importance increased
   - Suggest promoting 1-3 items to TASKS.md
   - Explain reasoning for each promotion

5. **If cleaning backlog**:
   - Identify obsolete items (completed elsewhere, no longer relevant, duplicates)
   - Mark items for removal with explanation
   - Ask user to confirm before deleting
   - Archive removed items in a "Discarded" section with date

6. **Organize BACKLOG.md structure**:
   ```markdown
   # Backlog

   ## Future Features
   - [ ] Feature idea (added YYYY-MM-DD)
     - Context: Why this matters
     - Blocked by: Prerequisites

   ## Technical Debt
   - [ ] Refactoring needed (added YYYY-MM-DD)
     - Impact: What improves
     - Effort: Estimated size

   ## Ideas & Research
   - [ ] Exploratory task (added YYYY-MM-DD)
     - Questions to answer
     - Expected outcome

   ## Deferred
   - [ ] Task moved from active (deferred YYYY-MM-DD)
     - Reason: Why deferred
     - Review after: Date or milestone

   ## Discarded
   - [x] Removed item (discarded YYYY-MM-DD)
     - Reason: Why removed
   ```

7. **Harvest code TODOs**:
   - Check for TODO/FIXME comments in codebase (shown in context)
   - Add any significant ones to backlog if not already tracked
   - Note file/line references

### Important

- **Always update the master `/home/claude/shipflow_data/TASKS.md` Backlog section** — even when working in a sub-project directory
- Prefix all backlog items with the project name (e.g., `- tubeflow: Native app feature parity`)
- Keep each project's active section in the master file focused (5-10 items max)
- Backlog section can be larger (20-50 items across all projects)
- Always date entries (added/deferred/discarded)
- Preserve context - why the idea matters
- Use categories to organize
- Review backlog weekly to keep it relevant
- Don't let backlog become a graveyard - actively clean it
- When deferring, explain the reason (helps future review)
