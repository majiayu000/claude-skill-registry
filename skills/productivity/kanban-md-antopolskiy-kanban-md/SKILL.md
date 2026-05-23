---
name: kanban-md
description: >
  Manage project tasks using kanban-md, a file-based kanban board CLI.
  Use when the user mentions tasks, kanban, board, backlog, sprint,
  project management, work items, priorities, blockers, or wants to
  track, create, list, move, edit, or delete tasks. Also use for
  standup, status update, sprint planning, triage, or project metrics.
allowed-tools:
  - Bash(kanban-md *)
  - Bash(kbmd *)
---

# kanban-md

Manage kanban boards stored as Markdown files with YAML frontmatter.
Each task is a `.md` file in `kanban/tasks/`. The CLI is `kanban-md`
(alias `kbmd` if installed via Homebrew).

## Current Board State

!`kanban-md board 2>/dev/null || echo 'No board found — run: kanban-md init --name PROJECT_NAME'`

## Rules

- Use `--compact` for listing commands (`list`, `board`, `metrics`, `log`) to get
  token-efficient one-line output.
- Use `kanban-md show ID` (default table format) to read task details — it includes
  the full body and all fields in a human-readable layout. Only add `--json` when you
  need to pipe the output to another tool or parse fields programmatically.
- Always pass `--yes` when deleting (`kanban-md delete ID --yes`).
- Dates use `YYYY-MM-DD` format.
- Statuses and priorities are board-specific. Check the board state above or run
  `kanban-md board` to discover valid values before using them.
- Default statuses: backlog, todo, in-progress, review, done.
- Default priorities: low, medium, high, critical.

## Decision Tree

| User wants to...                        | Command                                                          |
|-----------------------------------------|------------------------------------------------------------------|
| See board overview / standup            | `kanban-md board --compact`                                      |
| Get a unique agent name (for claims)    | `kanban-md agent-name`                                           |
| List all tasks                          | `kanban-md list --compact`                                       |
| List tasks by status                    | `kanban-md list --compact --status todo,in-progress`             |
| List tasks by priority                  | `kanban-md list --compact --priority high,critical`              |
| List tasks by assignee                  | `kanban-md list --compact --assignee alice`                      |
| List tasks by tag                       | `kanban-md list --compact --tag bug`                             |
| List blocked tasks                      | `kanban-md list --compact --blocked`                             |
| List ready-to-start tasks               | `kanban-md list --compact --not-blocked --status todo`           |
| List tasks with resolved deps           | `kanban-md list --compact --unblocked`                           |
| Find a specific task                    | `kanban-md show ID`                                              |
| Claim next available task               | `kanban-md pick --claim <agent> --status todo --move in-progress`|
| Create a task                           | `kanban-md create "TITLE" --priority P --tags T`                 |
| Create a task with body                 | `kanban-md create "TITLE" --body "DESC"`                         |
| Create and immediately claim a task     | `kanban-md create "TITLE" --priority P --claim <agent>`          |
| Start working on a task                 | `kanban-md move ID in-progress`                                  |
| Advance to next status                  | `kanban-md move ID --next`                                       |
| Move a task back                        | `kanban-md move ID --prev`                                       |
| Complete a task                         | `kanban-md move ID done`                                         |
| Edit task fields                        | `kanban-md edit ID --title "NEW" --priority P`                   |
| Add/remove tags                         | `kanban-md edit ID --add-tag T --remove-tag T`                   |
| Set a due date                          | `kanban-md edit ID --due 2026-03-01`                             |
| Block a task                            | `kanban-md edit ID --block "REASON"`                             |
| Unblock a task                          | `kanban-md edit ID --unblock`                                    |
| Add a dependency                        | `kanban-md edit ID --add-dep DEP_ID`                             |
| Set a parent task                       | `kanban-md edit ID --parent PARENT_ID`                           |
| Append a note to task body              | `kanban-md edit ID --append-body "note" --timestamp`             |
| Hand off a task to review               | `kanban-md handoff ID --claim <agent> --note "…" --release`      |
| Delete a task                           | `kanban-md delete ID --yes`                                      |
| See flow metrics                        | `kanban-md metrics --compact`                                    |
| See activity log                        | `kanban-md log --compact --limit 20`                             |
| See recent activity for a task          | `kanban-md log --compact --task ID`                              |
| Get a board context summary             | `kanban-md context`                                              |
| Initialize a new board                  | `kanban-md init --name "NAME"`                                   |

## Core Commands

### list

```bash
kanban-md list [--status S] [--priority P] [--assignee A] [--tag T] \
  [--sort FIELD] [-r] [-n LIMIT] [--blocked] [--not-blocked] \
  [--parent ID] [--unblocked]
```

Sort fields: id, status, priority, created, updated, due. `-r` reverses.
`--unblocked` shows tasks whose dependencies are all at terminal status.

### create

```bash
kanban-md create "TITLE" [--status S] [--priority P] [--assignee A] \
  [--tags T1,T2] [--due YYYY-MM-DD] [--estimate E] [--body "TEXT"] \
  [--parent ID] [--depends-on ID1,ID2] [--claim AGENT]
```

Prints the created task ID and summary. `--claim` immediately claims the task for an agent,
combining creation and claiming in one step.

### show

```bash
kanban-md show ID
kanban-md show ID --json   # only when piping to another tool
```

Default format shows all fields including the body in a readable layout.
Use `--json` only when you need to parse fields programmatically.
For the JSON schema, see [references/json-schemas.md](references/json-schemas.md).

### agent-name

```bash
kanban-md agent-name
```

Generates a random two-word identifier (e.g. `frost-maple`) to use as a claim name.
Run once per agent session and remember the result.

### edit

```bash
kanban-md edit ID[,ID,...] [--title T] [--status S] [--priority P] [--assignee A] \
  [--add-tag T] [--remove-tag T] [--due YYYY-MM-DD] [--clear-due] \
  [--estimate E] [--body "TEXT"] [-a "TEXT"] [--started YYYY-MM-DD] [--clear-started] \
  [--completed YYYY-MM-DD] [--clear-completed] [--parent ID] \
  [--clear-parent] [--add-dep ID] [--remove-dep ID] \
  [--block "REASON"] [--unblock] \
  [--claim AGENT] [--release] [-t]
```

Only specified fields are changed. Prints a confirmation message.
`-a` / `--append-body` appends text to the existing body without replacing it.
`-t` / `--timestamp` prefixes a timestamp line when appending.
`--claim` claims (or renews a claim on) the task for the agent.
`--release` releases the claim on the task.
Accepts comma-separated IDs for bulk edits.

### move

```bash
kanban-md move ID[,ID,...] STATUS
kanban-md move ID --next
kanban-md move ID --prev
kanban-md move ID STATUS --claim AGENT
```

Auto-sets Started on first move from initial status. Auto-sets Completed on move to terminal status.
Accepts comma-separated IDs for bulk moves. `--claim` claims the task during the move (useful when
resuming a parked task).

### pick

```bash
kanban-md pick --claim AGENT [--status S] [--move STATUS] [--tags T1,T2]
```

Atomically finds the highest-priority unclaimed, unblocked task and claims it. Use `--status` to
restrict which column to pick from. Use `--move` to simultaneously move the task to a new status.
Replaces the slower list → claim → move sequence.

### handoff

```bash
kanban-md handoff ID --claim AGENT [--note "TEXT"] [--block "REASON"] [--release] [-t]
```

Moves the task to `review`, appends a handoff note, and optionally marks it blocked and/or releases
the claim. Use when parking work for another agent or waiting on user input. `-t` adds a timestamp.

### context

```bash
kanban-md context [--sections in-progress,blocked,overdue,recently-completed] \
  [--days N] [--write-to FILE]
```

Generates a markdown board summary suitable for embedding in `CLAUDE.md` or `AGENTS.md`.
`--write-to` writes (or updates) the summary inside a delimited block in the target file.

### delete

```bash
kanban-md delete ID --yes
```

Always pass `--yes` (non-interactive context requires it).

### board

```bash
kanban-md board
```

Shows board overview: task counts per status, WIP utilization,
blocked/overdue counts, priority distribution.

### metrics

```bash
kanban-md metrics [--since YYYY-MM-DD]
```

Shows throughput (7d/30d), avg lead/cycle time, flow efficiency,
aging items.

### log

```bash
kanban-md log [--since YYYY-MM-DD] [--limit N] [--action TYPE] \
  [--task ID]
```

Action types: create, move, edit, delete, block, unblock.

### Global Flags

All commands accept: `--json`, `--table`, `--compact` (alias `--oneline`), `--dir PATH`, `--no-color`.

## Workflows

### Daily Standup

1. `kanban-md board --compact` — board overview
2. `kanban-md list --compact --status in-progress` — in-flight work
3. `kanban-md list --compact --blocked` — stuck items
4. `kanban-md metrics --compact` — throughput and aging
5. Summarize: completed, active, blocked, aging items

### Triage New Work

1. `kanban-md list --compact --status backlog --sort priority -r` — review backlog
2. For items to promote: `kanban-md move ID todo`
3. For new items: `kanban-md create "TITLE" --priority P --tags T`
4. For stale items: `kanban-md delete ID --yes`

### Sprint Planning

1. `kanban-md board --compact` — current state
2. `kanban-md list --compact --status backlog,todo --sort priority -r` — candidates
3. Promote selected: `kanban-md move ID todo`
4. Assign: `kanban-md edit ID --assignee NAME`
5. Set deadlines: `kanban-md edit ID --due YYYY-MM-DD`

### Complete a Task

1. `kanban-md move ID done` — marks complete, sets Completed timestamp
2. `kanban-md show ID --json` — verify status and timestamps

### Track a Bug

1. `kanban-md create "Fix: DESCRIPTION" --priority high --tags bug`
2. `kanban-md edit ID --body "Steps to reproduce: ..."`

### Track a Dependency Chain

1. Create parent: `kanban-md create "Epic title"`
2. Create subtask: `kanban-md create "Subtask" --parent PARENT_ID`
3. Or add dependency: `kanban-md create "Task B" --depends-on TASK_A_ID`
4. List unresolved: `kanban-md list --compact --blocked`

## Agent Cheatsheet

Quick-reference for the agent task lifecycle. These are combination commands — multiple flags
in one call to minimize round-trips. Replace `<agent>` with your session's `agent-name` output.

### Session start

```bash
kanban-md agent-name                             # generate a unique claim name; remember it
kanban-md board --compact                        # orient: what's active, blocked, overdue
```

### Claim next task (atomic pick + move)

```bash
# Pick highest-priority unclaimed task from todo and move it to in-progress in one step
kanban-md pick --claim <agent> --status todo --move in-progress

# If todo is empty, pick from backlog
kanban-md pick --claim <agent> --status backlog --move in-progress

# Read the full task after picking
kanban-md show <ID>
```

### Create and claim in one shot

```bash
# Create a task and immediately claim it
kanban-md create "TITLE" --priority high --tags bug --claim <agent>

# Add a body separately (or use --body inline if short)
kanban-md edit <ID> --body "Steps to reproduce: ..."
```

### Progress note (renews claim, appends without overwriting)

```bash
# Leave a timestamped note while keeping your claim active
kanban-md edit <ID> -a "Implemented X, running tests." -t --claim <agent>
```

### Finish task (release claim + mark done)

```bash
# Run from board home, after merging
kanban-md edit <ID> --release
kanban-md move <ID> done
```

### Park / handoff (moves to review, appends note, releases claim)

```bash
# Waiting on user decision or external action
kanban-md handoff <ID> --claim <agent> \
  --note "Ready to merge: branch task/<ID>-…; waiting for: ..." \
  -t --release

# Blocked on something specific
kanban-md handoff <ID> --claim <agent> \
  --block "Reason for block" \
  --note "What's needed to unblock and next step." \
  -t --release
```

### Resume a parked task

```bash
kanban-md edit <ID> --claim <agent>                  # re-claim
kanban-md edit <ID> --unblock --claim <agent>        # unblock (if it was blocked)
kanban-md move <ID> in-progress --claim <agent>      # move back to in-progress
```

### Bulk operations (comma-separated IDs)

```bash
# Tag multiple tasks at once
kanban-md edit <ID1>,<ID2>,<ID3> --add-tag layer-3

# Move multiple tasks
kanban-md move <ID1>,<ID2> todo

# List with combined filters
kanban-md list --compact --status backlog --priority high,critical --sort priority -r
kanban-md list --compact --not-blocked --status todo   # tasks ready to start
kanban-md list --compact --status in-progress,review   # all active/parked work
```

## Pitfalls

- **DO** use `--compact` for listing, board, metrics, and log commands — it is the most token-efficient format.
- **DO** use `kanban-md show ID` (default format) to read task details — it is readable and includes the full body.
- **DO** pass `--yes` on delete. Without it, the command hangs waiting for stdin.
- **DO** use `pick --claim <agent> --status todo --move in-progress` rather than list → edit → move — it's atomic and prevents claim races.
- **DO** use `-a` / `--append-body` with `--claim <agent>` when adding progress notes — this renews the claim and appends without overwriting the body.
- **DO NOT** use `--json` unless you are piping output to another tool or parsing fields programmatically. Default and `--compact` formats are sufficient for reading.
- **DO NOT** hardcode status or priority values. Read them from `kanban-md board --compact`.
- **DO NOT** use `--next` or `--prev` without checking current status. They fail at boundary statuses.
- **DO NOT** pass both `--status` and `--next`/`--prev` to move. Use one or the other.
- **DO** quote task titles with special characters: `kanban-md create "Fix: the 'login' bug"`.
