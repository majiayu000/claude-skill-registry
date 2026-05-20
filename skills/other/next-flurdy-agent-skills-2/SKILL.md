---
name: next
description: >
  Pick the next bead to work on. Shows ready tasks (no blockers), applies user
  preferences for ordering (priority, type, recency), and helps select work.
allowed-tools: "Read,Bash(bd:*),AskUserQuestion"
version: "1.0.0"
author: "flurdy"
---

# Next - Pick Your Next Bead

Help select the next bead to work on based on readiness and user preferences.

## When to Use

- Starting a new work session
- Finished a task and need to pick the next one
- Want to see what's available to work on
- Need help prioritizing between multiple options

## Usage

```
/next                    # Show ready beads, ranked by suitability
/next task               # Auto-pick the next most suitable task and start it
/next quick              # Auto-pick an easy win task and start it
/next bug                # Auto-pick the next most important bug and fix it
/next <bead-id>          # Start working on specific bead
```

## What This Skill Does

1. **Find Ready Work**
   - Run `bd list --ready` to get open, unblocked tasks
   - Excludes `in_progress` beads (another session may be working on them)
   - Show current in-progress work if any (for awareness, not selection)

2. **Rank by Suitability**
   - Apply priority ranking algorithm (see below)
   - Bugs generally rank higher than features at same priority
   - Epics rank lower (they represent larger work)

3. **Present Options**
   - Show top 5 candidates with key details
   - Include: ID, title, priority, type, age
   - Ask user to pick or provide different criteria

4. **Start Work**
   - Mark selected bead as in_progress
   - Show full bead details
   - Suggest first steps if description includes them

## Examples

```bash
# Show ready work ranked by suitability
/next

# Auto-pick and start the next most suitable task
/next task

# Auto-pick an easy win (quick task)
/next quick

# Auto-pick the next most important bug and start fixing
/next bug

# Start a specific bead
/next gauge-abc
```

## Output Format

```
## Ready to Work (5 of 12 open)

| # | ID        | Pri | Type    | Parent/Subs | Title                          |
|---|-----------|-----|---------|-------------|--------------------------------|
| 1 | gauge-abc | P1  | bug     | -           | Fix login timeout issue        |
| 2 | gauge-def | P2  | feature | 3 subtasks  | Add export to CSV              |
| 3 | gauge-ghi | P2  | task    | gauge-def   | Update dependencies            |
| 4 | gauge-jkl | P3  | feature | -           | Dark mode toggle               |
| 5 | gauge-mno | P3  | task    | 2 subtasks  | Refactor auth service          |

Currently in progress: gauge-xyz "Implement caching layer"

Which would you like to work on? (1-5, or specify ID, or "task" to auto-pick)
```

## Implementation

When invoked:

1. Check for current open, not in-progress elsewhere, work:
   ```bash
   bd list --status=open
   ```

2. Get ready (unblocked) beads with open status only, excluding P4 backlog:
   ```bash
   bd list --ready --priority-max=3
   ```

   **Important**:
   - Use `bd list --ready` (not `bd ready`) to exclude `in_progress` beads
   - Use `--priority-max=3` to exclude P4 backlog items (P4 = future/someday, never auto-pick)
   - Another session may be working on in_progress items - picking them up causes conflicts

3. Parse command argument:
   - (none): Show ranked list, ask user to pick
   - `task`: Auto-select top-ranked bead and start it
   - `quick`: Auto-select an easy win task and start it
   - `bug`: Auto-select top-ranked bug and start it (see Bug Mode below)
   - `<bead-id>`: Start that specific bead

4. If specific bead ID provided:
   ```bash
   bd show <id>
   bd update <id> --status=in_progress
   ```

5. Otherwise, present top 5 options and ask user to choose

6. On selection:
   - Mark as in_progress
   - Show full details with `bd show`
   - If bead has description with steps, highlight first step

## Handling Edge Cases

- **No ready beads (P0-P3)**: Show blocked beads and what's blocking them; mention P4 backlog exists if any, but don't auto-pick
- **All open beads in progress**: Warn that another session may be working on them; ask user if they want to see in_progress beads anyway (may cause conflicts)
- **User picks in_progress bead**: Warn that another session may be working on it; require explicit confirmation before starting
- **Invalid ID**: Show error and list valid options
- **User says "skip"**: Show next 5 options

## Priority Ranking Algorithm

Rank ready beads in this order (first match wins):

| Rank | Criteria                        |
|------|---------------------------------|
| 1    | Any P0 issue (any type)         |
| 2    | P1 bug                          |
| 3    | P2 bug                          |
| 4    | P1 feature or task              |
| 5    | P1 epic                         |
| 6    | P2 feature or task              |
| 7    | P3 bug, feature, or task        |
| 8    | P2 epic                         |
| 9    | P3 epic                         |
| 10   | Any other non-P4 issue          |

**Important**: P4 items are backlog/future work and must NEVER be auto-picked. Always use `--priority-max=3` to exclude them. Only show P4 items if user explicitly requests them.

## Quick Task Heuristics

When `/next quick` is used, prefer:
1. Type: task > bug > feature (tasks are usually smaller)
2. Priority: P3 > P2 > P1 (lower priority = less complex)
3. Exclude epics (too large for quick wins)
4. Title keywords: "fix", "update", "add" > "implement", "refactor", "redesign"

## Bug Mode

When `/next bug` is used:

1. **Filter to open bugs only** (excluding P4 backlog):

   ```bash
   bd list --ready --type=bug --priority-max=3
   ```

2. **Rank by priority**: P0 > P1 > P2 > P3 (highest priority bug first, P4 excluded)

3. **Auto-select and start** the top-ranked bug

4. **Continue fixing bugs** if the completed bug was minor:
   - After completing a bug fix, assess if it was minor (small change, localized fix)
   - If minor AND there's remaining context (related code still fresh), auto-pick the next bug
   - Continue this loop until:
     - A bug requires significant work (not minor)
     - No more ready bugs remain
     - Context would be lost (unrelated area of codebase)

### Minor Bug Criteria

A bug is considered **minor** if:

- Fix touches ≤ 3 files
- Change is ≤ 50 lines total
- No architectural changes required
- Fix is localized (single component/module)

### Context Continuity

Continue to next bug automatically when:

- Next bug is in same or adjacent files
- Next bug is in same module/component
- Fix for previous bug provides context for next bug

Stop and ask user when:

- Next bug is in completely different area of codebase
- Next bug appears complex (P0/P1 with unclear scope)
- 3+ bugs have been fixed in sequence (natural checkpoint)
