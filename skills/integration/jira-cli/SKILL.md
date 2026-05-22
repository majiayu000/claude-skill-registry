---
name: jira-cli
description: Interact with Jira from the command line to create, list, view, edit, and transition issues, manage sprints and epics, and perform common Jira workflows. Use when the user asks about Jira tasks, tickets, issues, sprints, or needs to manage project work items.
license: MIT
compatibility: Requires jira-cli installed (https://github.com/ankitpokhrel/jira-cli) and configured with `jira init`. Requires JIRA_API_TOKEN environment variable.
metadata:
  author: Colby Timm
  version: "1.0"
---

# Jira CLI

Interact with Atlassian Jira from the command line using [jira-cli](https://github.com/ankitpokhrel/jira-cli).

## When to Use

- User asks to create, view, edit, or search Jira issues/tickets
- User needs to transition issues through workflow states (To Do → In Progress → Done)
- User wants to manage sprints, epics, or boards
- User needs to assign issues, add comments, or log work time
- User asks about their current tasks or sprint progress

## Prerequisites

1. Install jira-cli: `brew install ankitpokhrel/jira-cli/jira-cli` (macOS) or download from [releases](https://github.com/ankitpokhrel/jira-cli/releases)
2. Set API token: `export JIRA_API_TOKEN="your-token"`
3. Initialize: `jira init` and follow prompts

## Issue Commands

### List Issues

```bash
# List issues in current project
jira issue list

# List my assigned issues
jira issue list -a$(jira me)

# List issues by status
jira issue list -s"In Progress"

# List high priority issues
jira issue list -yHigh

# List issues with multiple filters
jira issue list -a$(jira me) -s"To Do" -yHigh --created week

# List issues with raw JQL
jira issue list -q "project = PROJ AND status = 'In Progress'"

# Plain text output for scripting
jira issue list --plain --columns key,summary,status --no-headers
```

### Create Issues

```bash
# Interactive issue creation
jira issue create

# Create with all options specified
jira issue create -tBug -s"Login button not working" -b"Description here" -yHigh --no-input

# Create a story
jira issue create -tStory -s"Add user authentication" -yMedium

# Create with labels and components
jira issue create -tTask -s"Update dependencies" -lmaintenance -l"tech-debt" -Cbackend

# Create and assign to self
jira issue create -tBug -s"Fix crash on startup" -a$(jira me) --no-input
```

### View Issues

```bash
# View issue details
jira issue view ISSUE-123

# View with comments
jira issue view ISSUE-123 --comments 10

# View in plain text
jira issue view ISSUE-123 --plain

# Open issue in browser
jira open ISSUE-123
```

### Edit Issues

```bash
# Edit summary
jira issue edit ISSUE-123 -s"Updated summary"

# Edit description
jira issue edit ISSUE-123 -b"New description"

# Edit priority
jira issue edit ISSUE-123 -yHigh

# Add labels
jira issue edit ISSUE-123 -lnew-label
```

### Transition Issues

```bash
# Move issue to a new status
jira issue move ISSUE-123 "In Progress"

# Move with comment
jira issue move ISSUE-123 "Done" --comment "Completed the task"

# Move and set resolution
jira issue move ISSUE-123 "Done" -RFixed
```

### Assign Issues

```bash
# Assign to self
jira issue assign ISSUE-123 $(jira me)

# Assign to specific user
jira issue assign ISSUE-123 username

# Unassign
jira issue assign ISSUE-123 x
```

### Comments

```bash
# Add a comment
jira issue comment add ISSUE-123 "This is my comment"

# Add comment from editor
jira issue comment add ISSUE-123
```

### Work Logging

```bash
# Log time
jira issue worklog add ISSUE-123 "2h 30m"

# Log time with comment
jira issue worklog add ISSUE-123 "1d 4h" --comment "Completed feature implementation" --no-input
```

### Link & Clone Issues

```bash
# Link two issues
jira issue link ISSUE-123 ISSUE-456 Blocks

# Unlink issues
jira issue unlink ISSUE-123 ISSUE-456

# Clone an issue
jira issue clone ISSUE-123 -s"Cloned: New summary"

# Delete an issue
jira issue delete ISSUE-123
```

## Epic Commands

```bash
# List epics
jira epic list

# List epics in table format
jira epic list --table

# Create an epic
jira epic create -n"Q1 Features" -s"Epic summary" -b"Epic description"

# Add issues to epic
jira epic add EPIC-1 ISSUE-123 ISSUE-456

# Remove issues from epic
jira epic remove ISSUE-123 ISSUE-456
```

## Sprint Commands

```bash
# List sprints
jira sprint list

# List current/active sprint
jira sprint list --current

# List my issues in current sprint
jira sprint list --current -a$(jira me)

# Add issues to sprint
jira sprint add SPRINT_ID ISSUE-123 ISSUE-456
```

## Project & Board Commands

```bash
# List projects
jira project list

# List boards
jira board list

# List releases/versions
jira release list

# Open project in browser
jira open
```

## Utility Commands

```bash
# Get current username
jira me

# Show help
jira --help
jira issue --help

# Setup shell completion
jira completion bash  # or zsh, fish, powershell
```

## Common Flags

| Flag | Description |
| ---- | ----------- |
| `--plain` | Plain text output (no interactive UI) |
| `--raw` | Raw JSON output |
| `--csv` | CSV output |
| `--no-input` | Skip interactive prompts |
| `-t, --type` | Issue type (Bug, Story, Task, Epic) |
| `-s, --summary` | Issue summary/title |
| `-b, --body` | Issue description |
| `-y, --priority` | Priority (Highest, High, Medium, Low, Lowest) |
| `-l, --label` | Labels (repeatable) |
| `-a, --assignee` | Assignee username |
| `-r, --reporter` | Reporter username |
| `-C, --component` | Component name |
| `-P, --parent` | Parent issue/epic key |
| `-q, --jql` | Raw JQL query |
| `--created` | Filter by creation date (-7d, week, month) |
| `--order-by` | Sort field |
| `--reverse` | Reverse sort order |

## Common Workflows

### Start Working on an Issue

```bash
# Assign to self and move to In Progress
jira issue assign ISSUE-123 $(jira me)
jira issue move ISSUE-123 "In Progress"
```

### Complete an Issue

```bash
# Log work and close
jira issue worklog add ISSUE-123 "4h" --no-input
jira issue move ISSUE-123 "Done" --comment "Completed" -RFixed
```

### Daily Standup Review

```bash
# View my current sprint tasks
jira sprint list --current -a$(jira me)
```

### Create and Track a Bug

```bash
# Create bug
jira issue create -tBug -s"App crashes on login" -yHigh -lbug --no-input
# Note the returned issue key, then assign
jira issue assign BUG-123 $(jira me)
jira issue move BUG-123 "In Progress"
```

## Output Examples

| Command | Use Case |
| ------- | -------- |
| `jira issue list --plain` | Script-friendly output |
| `jira issue list --raw` | JSON for parsing |
| `jira issue list --csv` | Export to spreadsheet |

## Limitations

- Requires prior `jira init` configuration
- Some features may vary between Jira Cloud and Server
- Complex custom fields may require `--custom` flag with field IDs
- Rate limits apply based on Jira instance configuration
