---
name: goals
description: List and manage cross-session goals and milestones. Use for tracking multi-session work, viewing progress, or managing milestones.
---

# Goal Management

Manage goals and milestones that persist across Claude Code sessions.

**Command:** $ARGUMENTS

## Instructions

Parse the command and use the appropriate `mcp__mira__goal` action:

### No arguments or "list"
- Use `action="list"` to show all goals
- Display: title, status, progress %, priority
- Highlight in-progress and blocked goals

### "add <title>" or "create <title>"
- Use `action="create"` with the title
- Ask for description and priority if not provided
- Suggest adding milestones after creation

### "show <id>" or "progress <id>"
- Use `action="get"` with the goal_id
- Show full details including all milestones
- Display completion status for each milestone

### "milestone <goal_id> <title>"
- Use `action="add_milestone"`
- Add a new milestone to the specified goal
- Ask for weight if not provided (default: 1)

### "complete <milestone_id>"
- Use `action="complete_milestone"`
- Mark the milestone as done
- Show updated goal progress

### "done <goal_id>"
- Use `action="update"` with status="completed"
- Mark the entire goal as complete

## Example Usage

```
/mira:goals                           # List all goals
/mira:goals add Implement auth system # Create new goal
/mira:goals show 103                  # Show goal details
/mira:goals milestone 103 Add tests   # Add milestone
/mira:goals complete 17               # Complete milestone
```
