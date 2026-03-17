# Creating Your First Skill

**Step-by-Step Guide to Building a Custom Skill from Scratch**

---

## Overview

Creating custom skills allows you to extend OpenClaw for your specific needs, tools, and workflows. This tutorial walks you through creating a complete skill from scratch, using a practical example.

## What We'll Build

We'll create a **Task Timer** skill that helps track time spent on tasks:

**Features**:
- Start/stop timers
- List active timers
- Generate time reports
- Save time logs

**Tool**: `tt` (a simple CLI timer we'll use)

## Prerequisites

```bash
# Create skills directory if it doesn't exist
mkdir -p ~/.openclaw/skills

# Verify
ls ~/.openclaw/skills
```

## Step 1: Plan Your Skill

Before writing, answer these questions:

### What Problem Does It Solve?

```
Problem: Hard to track time spent on tasks
Solution: Simple timer commands to start/stop tracking
Benefit: Better time awareness, productivity insights
```

### What Tool/Service Does It Use?

```
Tool: tt (task timer CLI)
Alternative: Any time-tracking CLI or API
Installation: npm install -g tt-cli  (example)
```

### What Operations Will It Support?

```
Core operations:
1. Start timer: tt start "Task name"
2. Stop timer: tt stop
3. List timers: tt list
4. Report: tt report --today

Advanced:
5. Pause/resume
6. Tag tasks
7. Export data
```

### What Information Does AI Need?

```
AI needs to know:
- Command syntax
- Common patterns
- Error handling
- Output formatting
- Best practices
```

## Step 2: Create Skill Directory

```bash
# Create skill directory
mkdir -p ~/.openclaw/skills/task-timer

# Navigate to it
cd ~/.openclaw/skills/task-timer
```

## Step 3: Create SKILL.md File

```bash
touch SKILL.md
```

Now open `SKILL.md` in your editor and add content:

### 3.1 Add Metadata

```markdown
---
name: task-timer
description: Track time spent on tasks with simple CLI timer
homepage: https://github.com/example/tt-cli
metadata:
  openclaw:
    emoji: ⏱️
    requires:
      bins: ["tt"]
    install:
      - id: npm
        kind: npm
        package: tt-cli
        bins: ["tt"]
        label: Install Task Timer (npm)
    tags: ["productivity", "time-tracking", "tasks"]
---
```

**Metadata explained**:
- `name`: Unique skill identifier (lowercase, hyphens)
- `description`: One-line summary
- `homepage`: Documentation link
- `emoji`: Visual identifier (optional but fun)
- `requires.bins`: Required binary executables
- `install`: How to install dependencies
- `tags`: Categorization

### 3.2 Add Introduction

```markdown
# Task Timer

Simple CLI time tracking for tasks and projects.

## Quick Start

Start a timer:
```bash
tt start "Write documentation"
# Output: ⏱️  Timer started for "Write documentation"
```

Stop current timer:
```bash
tt stop
# Output: ⏹️  Timer stopped. Duration: 1h 23m
```

View active timers:
```bash
tt list
# Output:
# ⏱️  Write documentation (1h 23m) - running
# ✅ Code review (45m) - completed
```
```

### 3.3 Add Core Usage

```markdown
## Core Commands

### Start Timer

```bash
tt start "Task description"

# With project tag
tt start "Fix bug #123" --project openclaw

# With category
tt start "Team meeting" --category meeting
```

### Stop Timer

```bash
tt stop

# Stop and add note
tt stop --note "Completed feature, needs testing"
```

### List Timers

```bash
# All timers today
tt list

# Filter by project
tt list --project openclaw

# Filter by status
tt list --status running
```

### Reports

```bash
# Today's summary
tt report --today

# This week
tt report --week

# Specific project
tt report --project openclaw --week

# Export to CSV
tt report --week --format csv > time_report.csv
```

## When to Use

Use this skill when user asks to:
- "Start tracking time for..."
- "How long have I been working on...?"
- "Stop the timer"
- "Show my time report"
- "What did I work on today?"
```

### 3.4 Add Patterns and Examples

```markdown
## Common Patterns

### Daily Workflow

```bash
# Morning: Start first task
tt start "Email triage" --category admin

# Switch tasks
tt stop
tt start "Feature development" --project myapp

# Lunch break
tt stop  # Pause tracking

# After lunch
tt start "Code review" --project myapp

# End of day report
tt report --today
```

### Project Time Tracking

```bash
# All time on specific project
tt report --project openclaw --all-time

# Break down by category
tt report --project openclaw --by-category
```

### Multi-tasking

```bash
# Check what's running
tt list --status running

# Stop all timers
tt stop --all

# Resume specific timer
tt resume "Feature development"
```

## Output Formatting

### List Output

```
⏱️  Write documentation (1h 23m) - running
⏱️  Code review (45m) - running
✅ Email triage (22m) - completed
✅ Team meeting (30m) - completed

Total today: 3h 0m
```

### Report Output

```
Time Report - Today (2026-01-31)
================================

By Project:
  openclaw:        4h 15m
  personal:        1h 30m

By Category:
  development:     3h 45m
  meetings:        1h 30m
  admin:          30m

Total:            5h 45m
```

## Tips

1. **Be specific with task names**
   - Good: "Fix user login bug #247"
   - Bad: "Coding"

2. **Use consistent project names**
   - Use same name across timers
   - Enables better reporting

3. **Stop timers when done**
   - Don't leave timers running overnight
   - Check with `tt list` before leaving

4. **Review reports regularly**
   - Daily: Quick sanity check
   - Weekly: Identify time sinks
   - Monthly: Long-term patterns

5. **Tag appropriately**
   - Projects: For project-based time tracking
   - Categories: For activity-based analysis
```

### 3.5 Add Error Handling

```markdown
## Error Handling

### No Timer Running

```
User: "Stop timer"
Error: No timer currently running

Solution: Start a timer first with `tt start "Task"`
```

### Timer Already Running

```
User: "Start new timer"
Error: Timer already running: "Previous task"

Solutions:
- Stop current: `tt stop`
- Switch: `tt stop && tt start "New task"`
```

### Invalid Report Range

```
Error: No data for specified range

Check:
- Date format: YYYY-MM-DD
- Range exists: `tt list --all-time` to see available data
```

## Troubleshooting

### Timer Not Saving

```bash
# Check data directory
tt config --show-data-dir

# Verify permissions
ls -la ~/.tt/

# Reset if needed
tt reset --confirm
```

### Incorrect Time Displayed

```bash
# Check system time
date

# Check timer status
tt list --verbose

# Manually adjust if needed
tt edit <timer-id> --duration 1h30m
```
```

### 3.6 Add Best Practices

```markdown
## Best Practices

### DO:

✅ **Start timers immediately when beginning work**
```bash
# Right when starting
tt start "Morning standup prep"
```

✅ **Use descriptive task names**
```bash
# Good
tt start "Implement user authentication API endpoint"

# Not as helpful
tt start "Coding"
```

✅ **Tag tasks consistently**
```bash
# Use same project names
tt start "Bug fix" --project openclaw
tt start "Feature work" --project openclaw

# Enables: tt report --project openclaw
```

✅ **Review time daily**
```bash
# End-of-day routine
tt report --today
```

### DON'T:

❌ **Leave timers running overnight**
```bash
# Before leaving:
tt stop
tt list  # Verify nothing running
```

❌ **Forget to stop before switching tasks**
```bash
# Always stop before starting new
tt stop
tt start "New task"
```

❌ **Track every tiny interruption**
```bash
# Don't create noise
# Skip: "Got coffee (2 min)"
# Track: Meaningful work blocks
```
```

## Step 4: Test Your Skill

### 4.1 Install the Tool

```bash
# Install tt-cli (example, adjust for your tool)
npm install -g tt-cli

# Verify installation
which tt
tt --version
```

### 4.2 Reload Skills

```bash
openclaw skills reload

# Verify skill loaded
openclaw skills list | grep task-timer
```

### 4.3 Test with AI

```
You: "Use task-timer to start tracking 'Tutorial writing'"

AI: [Reads task-timer skill]
    [Executes]: tt start "Tutorial writing"
    [Response]: "⏱️  Timer started for 'Tutorial writing'"

You: "How long have I been working?"

AI: [Executes]: tt list
    [Response]: "You've been working on 'Tutorial writing' for 23 minutes"
```

## Step 5: Refine and Iterate

### Gather Feedback

Use the skill for a week, then note:
- What works well?
- What's confusing?
- What's missing?
- What could be clearer?

### Update Documentation

```bash
cd ~/.openclaw/skills/task-timer
# Edit SKILL.md with improvements
```

### Reload

```bash
openclaw skills reload
```

## Advanced: Adding References

For complex skills, add reference files:

```bash
mkdir -p ~/.openclaw/skills/task-timer/references

# Create reference files
touch ~/.openclaw/skills/task-timer/references/cli-reference.md
touch ~/.openclaw/skills/task-timer/references/examples.md
```

**cli-reference.md**:
```markdown
# Task Timer CLI Reference

## Commands

### tt start
Start a new timer

Syntax: `tt start <description> [options]`

Options:
- `--project <name>`: Assign to project
- `--category <category>`: Categorize task
- `--billable`: Mark as billable time

Examples:
```bash
tt start "Client work" --project acme --billable
```

[... full command reference ...]
```

**examples.md**:
```markdown
# Task Timer Examples

## Developer Workflow

Morning routine:
```bash
tt start "Email triage" --category admin
# After 15 minutes
tt stop

tt start "Code review" --project main --category development
# After 1 hour
tt stop

tt start "Feature implementation" --project main --category development
```

[... more examples ...]
```

## Real Example: Note-Taking Skill

Here's a complete, real-world skill for a note-taking app:

```markdown
---
name: quick-notes
description: Quick note-taking with tags and search
metadata:
  openclaw:
    emoji: 📝
    requires:
      bins: ["qn"]
---

# Quick Notes

Fast CLI note-taking with tagging and full-text search.

## Quick Start

Create note:
```bash
qn add "Meeting with client discussed new features"
```

Create with tags:
```bash
qn add "Important deadline Friday" --tags urgent,deadline
```

Search notes:
```bash
qn search "client"
qn search --tag urgent
```

## Commands

### Add Note
```bash
qn add "Note content" [options]

Options:
--tags tag1,tag2    Add tags
--notebook name     Specify notebook
--date YYYY-MM-DD   Backdate note
```

### Search
```bash
qn search "keyword"
qn search --tag tagname
qn search --notebook work
qn search --date-from 2026-01-01
```

### List
```bash
qn list                    # Recent notes
qn list --limit 10         # Limit results
qn list --notebook work    # Specific notebook
```

### Edit
```bash
qn edit <note-id>          # Opens in $EDITOR
qn update <note-id> "New content"
```

## Patterns

### Daily Journaling
```bash
# Morning
qn add "Goals for today: Complete tutorial, review PRs" --tags journal,daily

# Evening
qn add "Accomplished: Finished 3 tutorials, reviewed 5 PRs" --tags journal,daily
```

### Meeting Notes
```bash
qn add "Team standup - discussed sprint planning, Tom blocked on API" --tags meeting,team

qn search --tag meeting  # Review all meeting notes
```

### Quick Captures
```bash
# Capture ideas quickly
qn add "App idea: Task timer with Pomodoro integration"
qn add "Research topic: AI prompt engineering patterns"
```

## When to Use

Trigger phrases:
- "Make a note"
- "Remember this"
- "Add to my notes"
- "Search my notes for..."
- "What did I note about...?"

## Best Practices

DO:
- Add tags for easy retrieval
- Use consistent notebook names
- Make notes descriptive
- Search before creating duplicates

DON'T:
- Put sensitive passwords (use 1Password skill)
- Create overly long notes (use Obsidian for that)
- Forget to tag important notes
```

## Summary

Creating a skill:

**Steps**:
1. Plan (problem, tool, operations, AI needs)
2. Create directory: `~/.openclaw/skills/skill-name/`
3. Create SKILL.md with:
   - Metadata (name, description, requirements)
   - Introduction and quick start
   - Core commands and usage
   - Patterns and examples
   - Error handling
   - Best practices
4. Install dependencies
5. Reload skills: `openclaw skills reload`
6. Test with AI
7. Refine based on usage

**Skill Structure**:
```
skill-name/
├── SKILL.md (required)
├── references/ (optional)
│   ├── cli-reference.md
│   └── examples.md
└── assets/ (optional)
    └── [images, config files]
```

**Writing Tips**:
- Clear, concise commands
- Concrete examples
- Common patterns
- Error scenarios
- Best practices

**Next Steps**:
- Practice creating a skill for a tool you use
- Study [Skill Writing Patterns](./04-skill-writing-patterns.md)
- Explore [Skill Examples Library](./05-skill-examples-library.md)
- Learn [Advanced Techniques](./07-advanced-skill-techniques.md)
