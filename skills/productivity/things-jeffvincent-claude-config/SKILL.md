---
name: things-3-manager
description: "macOS only: Manage Things 3 tasks - add, search, list, and complete tasks using natural language. Requires Things 3 app installed."
version: 2.0.0
location: user
allowed-tools: [Bash, Read, Write]
---

# Things 3 Task Management (macOS Only)

Manage your Things 3 tasks through natural language. This skill dispatches to focused sub-skills for specific operations.

**Platform:** macOS only (Things 3 is a Mac app)

## When to Apply

Use this skill when:
- User is on macOS with Things 3 installed
- User wants to add/create tasks or projects
- User wants to view today's tasks or inbox
- User wants to search for tasks
- User wants to complete/mark tasks as done

**Do NOT use when:**
- User is on Windows/Linux (Things 3 not available)
- User mentions other task apps (Todoist, OmniFocus, etc.)

## Sub-Skills

| Intent | Sub-Skill | Example |
|--------|-----------|---------|
| Add tasks | `skills/add-task.md` | "Add task to write blog post" |
| View today | `skills/list-today.md` | "What's on my plate today?" |
| View inbox | `skills/list-inbox.md` | "Show my inbox" |
| Search tasks | `skills/search.md` | "Find tasks tagged urgent" |
| Complete tasks | `skills/complete-task.md` | "Mark task ABC-123 done" |

## Quick Reference

### Library Imports
```python
import os, sys
sys.path.insert(0, os.path.expanduser('~/.claude/skills/things/lib'))

from reader import ThingsReader   # Database queries
from writer import ThingsWriter   # URL scheme operations
from helpers import ThingsFormatter  # Display formatting
```

### Common Operations
```python
# List tasks
tasks = ThingsReader.get_today()
tasks = ThingsReader.get_inbox()
tasks = ThingsReader.search(query="blog", status="incomplete")

# Add task
ThingsWriter.add_task(title="New task", when="today", tags=["work"])

# Complete task
ThingsWriter.complete_task("task-uuid")

# Format output
print(ThingsFormatter.format_task_list(tasks, verbose=True, show_uuid=True))
```

## Setup

See `README.md` for installation and configuration instructions.

**Quick install:**
```bash
cd ~/.claude/skills/things && pip3 install -r requirements.txt
```

## Identifying Discrete Tasks

**IMPORTANT:** Not everything that looks like an action item should become a Things task. Apply these filters:

### ✅ Create Tasks For

**Discrete actions with clear completion:**
- "Deliver plan by Jan 17"
- "Schedule meeting with X"
- "Send email to Y about Z"
- "Review document and provide feedback"
- "Update spreadsheet with Q4 data"
- "Create presentation for board meeting"

**Characteristics of real tasks:**
- Has a verb + specific object
- Can be marked "done" at a point in time
- Usually has a deadline or timeframe
- Represents single deliverable or interaction

### ❌ Do NOT Create Tasks For

**Strategic mindsets / ongoing approaches:**
- "Own entire product mentality"
- "Feel pain when platform inconsistent"
- "Think about cross-product-line value"
- "Be more responsive"
- "Pick more fights"

**Framing guidance / communication style:**
- "Frame work using X framing"
- "Apply Y test measurement"
- "Use Z terminology when discussing"
- "Position work as competitive necessity"

**Conceptual frameworks:**
- "Prioritize by user exposure"
- "Focus on crawl-walk-run"
- "Consider frequency × breadth"

**Why these aren't tasks:**
- No discrete completion point
- Ongoing mental models or approaches
- How to think/communicate, not what to do
- Can't check off as "done"

### Examples from Real Meetings

**From "Jeff - deliver these 7 things":**

| Item | Real Task? | Reasoning |
|------|-----------|-----------|
| "Deliver plan by Jan 17" | ✅ Yes | Discrete deliverable with deadline |
| "Frame all work using X framing" | ❌ No | Communication style, not action |
| "Apply Jeff Bell Test measurement" | ❌ No | Ongoing evaluation approach |
| "Own entire product mentality" | ❌ No | Mindset shift, not discrete action |
| "Schedule 3-hour working session" | ✅ Yes | Specific action with completion |
| "Prioritize by user exposure" | ❌ No | Prioritization framework |
| "Figure out skeleton key scope" | ⚠️ Maybe | Could be discrete if time-boxed research task |

### When Uncertain

Ask yourself:
1. **Can I mark this "done" at a specific moment?** If no → not a task
2. **Does this have a verb + deliverable?** If no → not a task
3. **Is this how to think vs what to do?** If "how to think" → not a task
4. **Would completing this once be sufficient?** If no (ongoing) → not a task

**Exceptions:**
- "Figure out X" CAN be a task if it's time-boxed research with deliverable (e.g., "Spend 2 hours figuring out skeleton key scope, write up findings")
- "Review X and decide Y" CAN be a task (discrete decision point)

## Dispatching

When user requests Things 3 operations:

1. **Identify intent** from natural language
2. **Filter for discrete tasks** (see "Identifying Discrete Tasks" above)
3. **Read the appropriate sub-skill** for detailed instructions
4. **Execute** using the library functions
5. **Report results** clearly to user

### Intent Mapping

| User Says | Intent | Action |
|-----------|--------|--------|
| "Add...", "Create task...", "New task..." | Add | Read `skills/add-task.md` |
| "What's today?", "Show today", "My tasks" | List Today | Read `skills/list-today.md` |
| "Inbox", "What needs organizing?" | List Inbox | Read `skills/list-inbox.md` |
| "Find...", "Search...", "Show tasks with..." | Search | Read `skills/search.md` |
| "Complete...", "Done...", "Finished..." | Complete | Read `skills/complete-task.md` |

## Limitations

- **macOS only** - Things 3 database only exists on Mac
- **No iOS sync** - Cannot access Things on mobile
- **Auth token needed** for completing tasks (see README.md)
