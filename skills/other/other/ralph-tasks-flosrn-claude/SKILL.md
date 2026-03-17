---
name: ralph-tasks
description: This skill should be used when the user asks to "add a task for Ralph", "list Ralph tasks", "remove Ralph task", "setup Ralph tasks", or mentions ralph-tasks, task queue for AI agent, or autonomous task management. Manages a JSON-based task queue for Ralph autonomous loop.
argument-hint: "<command> [args]"
---

<objective>
Manage a task queue for the Ralph autonomous AI coding loop. Provides commands to add, list, remove tasks, and run a continuous execution loop that processes tasks one by one until completion.
</objective>

<quick_start>
```bash
/ralph-tasks setup                           # Initialize in project
/ralph-tasks add Add authentication          # Add task (quotes optional)
/ralph-tasks add Add dark mode -s            # Add with context search
/ralph-tasks add Fix bug --search            # Same with --search
/ralph-tasks list                            # List all tasks
/ralph-tasks remove 1                        # Remove task #1
/ralph-tasks wake-up                         # Show loop command
```

**Multi-task:** Add multiple tasks in one message - they're processed in parallel.
</quick_start>

<commands>
| Command | Description |
|---------|-------------|
| `setup` | Initialize .claude/ralph-tasks/ with all files |
| `add <task>` | Add a task (quotes optional) |
| `add <task> -s` | Add with codebase context search |
| `list` | Show all tasks with status |
| `remove <id>` | Remove task by ID |
| `wake-up` | Show command to start loop |

**Aliases:** `add tasks`, `add task`, `list tasks`, `remove task`
</commands>

<file_structure>
```
{project}/.claude/ralph-tasks/
├── tasks.json       # Task queue
├── wake-up.sh       # Main loop script
├── prompt.md        # Agent instructions
└── progress.txt     # Accumulated learnings
```
</file_structure>

<entry_point>
**FIRST ACTION:** Load `steps/action-init.md`

This step parses the command and routes to the appropriate action file.
</entry_point>

<action_files>
| Action | File | Purpose |
|--------|------|---------|
| init | `steps/action-init.md` | Parse command and route |
| setup | `steps/action-setup.md` | Initialize ralph-tasks |
| add | `steps/action-add.md` | Add task to queue |
| add-search | `steps/action-add-search.md` | Add task with context |
| list | `steps/action-list.md` | Display tasks |
| remove | `steps/action-remove.md` | Remove task by ID |
| wake-up | `steps/action-wake-up.md` | Show loop instructions |
</action_files>

<state_variables>
| Variable | Type | Description |
|----------|------|-------------|
| `{command}` | string | Parsed command (setup, add, list, remove, wake-up) |
| `{task_description}` | string | Task description (for add) |
| `{task_id}` | number | Task ID (for remove) |
| `{search_mode}` | boolean | Whether --search/-s flag is set |
| `{project_path}` | string | Current project path |
| `{tasks_dir}` | string | Path to .claude/ralph-tasks/ |
</state_variables>

<critical_rules>
🛑 NEVER run wake-up.sh automatically - user must run it themselves
🛑 NEVER modify tasks.json without proper JSON handling (use jq)
✅ ALWAYS use atomic file updates (write to tmp, then mv)
✅ ALWAYS load only the current action file (progressive disclosure)
</critical_rules>

<success_criteria>
✅ Commands parsed correctly and routed to action files
✅ Each action executes its specific task
✅ Progressive loading minimizes context usage
</success_criteria>
