---
name: uni-productivity
description: |
  Productivity tools via uni CLI. Use when user wants to send Slack messages, search Notion, manage Linear issues, or handle Todoist tasks.
  Services: slack, notion, linear, todoist.
allowed-tools: Bash(uni:*), Bash(~/.local/bin/uni:*)
---

# Productivity Tools (uni)

## Slack

Requires SLACK_BOT_TOKEN.

```bash
uni slack channels list                 # List channels
uni slack channels info general         # Channel info
uni slack messages general              # Read messages
uni slack messages general --limit 20   # Last 20
uni slack send general "Hello team!"    # Send message
uni slack send "#general" "Update"      # With # prefix
uni slack users list                    # List users
uni slack users info @username          # User info
```

## Notion

Requires NOTION_TOKEN.

```bash
uni notion search "project notes"       # Search pages
uni notion pages <page-id>              # View page
uni notion databases list               # List databases
uni notion databases query <db-id>      # Query database
```

## Linear

Issue tracking. Uses OAuth.

```bash
uni linear auth                         # Authenticate
uni linear issues                       # List open issues
uni linear issues list --team ENG       # By team
uni linear issues list --filter closed  # Closed issues
uni linear issues get ENG-123           # Issue details
uni linear issues create "Fix bug" -t ENG
uni linear issues update ENG-123 --priority 1
uni linear issues close ENG-123
uni linear issues search "login bug"
uni linear projects                     # List projects
uni linear teams                        # List teams
uni linear comments list ENG-123        # Comments
uni linear comments add ENG-123 "Fixed!"
```

## Todoist

Task management. Uses OAuth.

```bash
uni todoist auth                        # Authenticate
uni todoist tasks                       # List tasks
uni todoist tasks list --project Work   # By project
uni todoist tasks list --filter today   # Today's tasks
uni todoist tasks add "Buy groceries"
uni todoist tasks add "Report" --due tomorrow --priority 4
uni todoist tasks done "Buy groceries"  # Complete
uni todoist tasks delete "Old task"
uni todoist projects                    # List projects
uni todoist projects create "Work"
uni todoist labels                      # List labels
uni todoist comments list "Task"        # Comments
uni todoist comments add "Task" "Note"
```
