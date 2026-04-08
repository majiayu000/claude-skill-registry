---
name: daily-rituals
description: Structured morning, evening, weekly review, and weekly planning workflows. USE WHEN morning routine OR start my day OR evening review OR end of day OR weekly review OR daily checkin OR what should I focus on OR daily ritual OR morning checkin OR evening checkin OR weekly planning OR plan week OR plan my week OR close week OR week retro OR sunday ritual OR full sunday.
user-invocable: false
---

# daily-rituals

Structured rituals that surface system state — inbox health, domain project status, session history, and life context — to help you start, end, and review your work with intention.

## Workflow Routing

| Workflow | Trigger | File |
| :--- | :--- | :--- |
| **morning_checkin** | "morning routine", "start my day", "morning checkin", "what should I focus on" | `workflows/morning_checkin.md` |
| **evening_review** | "evening review", "end of day", "evening checkin", "wrap up" | `workflows/evening_review.md` |
| **weekly_review** | "weekly review", "week in review", "weekly checkin" | `workflows/weekly_review.md` |
| **weekly_planning** | "weekly planning", "plan week", "plan my week" | `workflows/weekly_planning.md` |
| **weekly_closing** | "close week", "week retro", "end week" | `workflows/weekly_closing.md` |
| **sunday_ritual** | "sunday ritual", "full sunday" | `workflows/sunday_ritual.md` |

## System Constants

### Naming Convention
Daily notes MUST follow this format: `DD-MM-YY-XX.md`
- **XX** = Day Suffix (case-sensitive, uppercase)
- **Mapping**:
  - Monday -> **MO**
  - Tuesday -> **TU**
  - Wednesday -> **WE**
  - Thursday -> **TH**
  - Friday -> **FR**
  - Saturday -> **SA**
  - Sunday -> **SU**

### Task Status Legend
The system uses the following checkbox states to track progress:
- `[ ]` To Do (Not started)
- `[/]` In Progress
- `[!]` Blocked (Waiting on external factor)
- `[?]` Paused (Decided to stop for now)
- `[I]` Backlog (Deferred to a later time)
- `[-]` Not Doing (Cancelled/Dropped)
- `[x]` Done (Completed)

## Examples

**Example 1: Start the day with context**
```
User: "morning routine"
-> Invokes morning_checkin workflow
-> Scans Inbox/ for unprocessed items
-> Reads active PROJECT_*.md files for open tasks
-> Checks yesterday's session log
-> Presents: inbox state, top priorities, suggested focus
-> Creates Inbox/Plan/DD-MM-YY.md with intentions
```

**Example 2: End the day with reflection**
```
User: "end of day"
-> Invokes evening_review workflow
-> Reads today's session logs
-> Summarizes accomplishments and progress
-> Captures learnings and blockers
-> Appends review to Inbox/Plan/DD-MM-YY.md
-> Suggests tomorrow's priority
```

**Example 3: Weekly progress check**
```
User: "weekly review"
-> Invokes weekly_review workflow
-> Aggregates task progress across all domains
-> Reviews inbox health (unprocessed count)
-> Checks project status changes
-> Identifies stalled projects
-> Creates weekly summary in Inbox/Plan/
```

**Example 4: Sunday weekly ritual**
```
User: "sunday ritual"
-> Invokes sunday_ritual workflow (orchestrator)
-> If active week exists: runs weekly_closing first
-> Runs weekly_review for progress summary
-> Runs weekly_planning for upcoming week
-> Creates week file in Inbox/Plan/
-> Archives week and daily files to Inbox/Plan/archive/
```

## Data Sources

| Source | What It Provides | How To Read |
| :--- | :--- | :--- |
| `Inbox/Notes/` | Unprocessed note count | `ls` + count files without `status: processed` |
| `Inbox/Dashboards/TASKS.md` | Task aggregation stats | Read frontmatter: `open_tasks`, `total_tasks` |
| `Domains/*/01_PROJECTS/PROJECT_*.md` | Active project status | Grep frontmatter for `status`, `task_open` |
| `.claude/sessions/` | Recent session logs | Read most recent session file |
| `Inbox/Plan/` | Daily and weekly planning files | Read DD-MM-YY.md (daily) and W[X]_YYYY-MM-DD.md (weekly) files |
| `Inbox/Plan/archive/` | Archived daily and weekly files | Historical daily notes, weekly reviews, and closed week files |
