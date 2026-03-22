---
name: shipflow-priorities
description: Analyze and reorder tasks by priority using impact/effort matrix
disable-model-invocation: false
argument-hint: [optional priority criteria: impact, effort, blockers, quick-wins]
---

## Context

- Current directory: !`pwd`
- **Master TASKS.md** (multi-project dashboard): !`cat /home/claude/shipflow_data/TASKS.md 2>/dev/null || echo "No master TASKS.md"`
- Local TASKS.md (if exists): !`cat TASKS.md 2>/dev/null || echo "No local TASKS.md"`
- Git branch and status: !`git status --short --branch 2>/dev/null || echo "Not a git repo"`
- Recent commits: !`git log --oneline -5 2>/dev/null || echo "N/A"`
- Project CLAUDE.md: !`head -40 CLAUDE.md 2>/dev/null || echo "No CLAUDE.md"`
- Workspace CLAUDE.md: !`head -20 /home/claude/CLAUDE.md 2>/dev/null || echo "N/A"`

## Multi-project tracking system

**CRITICAL**: This workspace tracks 12 projects from a single master file at `/home/claude/shipflow_data/TASKS.md`.

- **Always prioritize within `/home/claude/shipflow_data/TASKS.md`** — this is the single source of truth
- The master file has a Dashboard table and per-project sections — prioritize across ALL projects, not just the current directory
- When re-ranking, update the Dashboard table's "Top Priority" column to reflect the new P0 for each project
- If the user specifies a project name as argument, focus prioritization on that project's section only

## Your task

Analyze all tasks and reorganize them by priority using a smart prioritization framework.

### Workspace root detection

If the current directory has no project markers (no `package.json`, no `src/` dir) BUT contains multiple project subdirectories — you are at the **workspace root**. Use **AskUserQuestion**:
- Question: "Which project(s) should I prioritize?"
- `multiSelect: true`
- Options:
  - **All projects** — "Re-prioritize across the entire workspace" (Recommended)
  - One option per project with active tasks: label = project name, description = number of open tasks
- Read project list from `/home/claude/shipflow_data/PROJECTS.md`

### Steps

1. **Parse existing tasks**:
   - Read all tasks from TASKS.md (shown in context)
   - Categorize by status: completed, in progress, todo
   - Identify task dependencies and blockers

2. **Analyze each uncompleted task** using criteria:
   - **Impact**: How much value does this deliver? (High/Medium/Low)
   - **Effort**: How much work is required? (High/Medium/Low)
   - **Blockers**: Does this unblock other tasks? (Yes/No)
   - **Dependencies**: What must be done first?
   - **Risk**: What happens if we delay this?

3. **Apply prioritization logic**:
   - P0 (Critical): Blockers, high impact + low effort, security/bugs
   - P1 (High): High impact + medium effort, important features
   - P2 (Medium): Medium impact, or high effort without clear blocker
   - P3 (Low): Nice to have, low impact, can wait

4. **Consider user's criteria** (`$ARGUMENTS`):
   - `impact`: Prioritize by business/user value
   - `effort`: Show quick wins first (low effort, high impact)
   - `blockers`: Prioritize tasks that unblock others
   - `quick-wins`: Focus on high-impact, low-effort tasks
   - If no argument, use balanced approach

5. **Update TASKS.md** with priority sections:
   ```markdown
   # Tasks

   ## Completed
   - [x] Done items

   ## 🔴 P0 - Critical (Do First)
   - [ ] Blocker task [Impact: High | Effort: Low | Unblocks: 3 tasks]

   ## 🟠 P1 - High Priority
   - [ ] Important task [Impact: High | Effort: Medium]

   ## 🟡 P2 - Medium Priority
   - [ ] Standard task [Impact: Medium | Effort: Medium]

   ## 🟢 P3 - Low Priority
   - [ ] Nice to have [Impact: Low | Effort: High]

   ## Notes
   - Priority last updated: [date]
   - Prioritization criteria: [criteria used]
   ```

6. **Provide priority summary**:
   - List P0 tasks with why they're critical
   - Suggest which P0 task to start immediately
   - Note any dependencies or prerequisites
   - Highlight quick wins if present

### Important

- **Always update the master `/home/claude/shipflow_data/TASKS.md`** — even when working in a sub-project directory
- Use Edit tool to update TASKS.md with priority markers
- Be realistic about impact/effort assessments
- Consider technical debt alongside features
- Flag tasks with missing context as needing refinement
- Explain your prioritization reasoning clearly
- If tasks seem equally important, break ties by effort (prefer low effort)
- Update "Priority last updated" timestamp
- Update the master Dashboard table's "Top Priority" column to reflect the new highest-priority task per project
