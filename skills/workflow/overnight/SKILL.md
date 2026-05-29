---
name: overnight
description: Launch autonomous overnight build session with Ralph Wiggum
---
Overnight autonomous build session. To launch:

1. Ensure Ralph Wiggum is installed: `/plugin list` should show it
2. Check task list: Ask Task Master "what are the next 5 tasks?"
3. Launch loop:
```
/ralph-wiggum:ralph-loop "You are building Kaizen sovereign AI infrastructure. Check .taskmaster/ for current tasks. Run task-master next to get your current task. Complete it fully, run /validate, commit with conventional commits, then mark complete and get next task. Continue until all available tasks are done or you hit a blocker requiring human input. Write progress to .claude/overnight-log.txt" --max-iterations 20 --completion-promise "ALL_TASKS_COMPLETE"
```

Monitor: Check `.claude/overnight-log.txt` and `git log` in the morning.
Override with specific focus: $ARGUMENTS
