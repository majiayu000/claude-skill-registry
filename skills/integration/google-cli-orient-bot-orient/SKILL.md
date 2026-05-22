---
name: google-cli
description: Use the gog CLI to interact with Google Workspace services (Calendar, Gmail, Tasks, Drive, Docs, Slides, Sheets). This skill is for coding agents that have Bash access and prefer CLI tools over MCP tools. Use when asked to check calendar, send emails, manage tasks, or access Google services from the terminal.
---

# Google CLI (gog)

The `gog` CLI provides access to Google Workspace services from the terminal. Use this instead of MCP tools when you have Bash access (coding agents in Cursor/Claude Code).

## Prerequisites

- `gog` CLI installed (`which gog` should return `/usr/local/bin/gog`)
- Authenticated via `gog auth login`

## Quick Reference

```bash
# Check authentication status
gog auth status

# List available accounts
gog auth list
```

## Calendar Operations

### List Upcoming Events

```bash
# List events for the next 7 days (default)
gog calendar events

# List events for specific date range
gog calendar events --from="2026-01-15" --to="2026-01-20"

# List events from a specific calendar
gog calendar events primary

# Output as JSON (for parsing)
gog calendar events --json

# Search for events by keyword
gog calendar search "standup"
```

### Create Events

```bash
# Quick event creation
gog calendar create primary --title="Team Meeting" --start="2026-01-15T14:00:00" --end="2026-01-15T15:00:00"

# With location and description
gog calendar create primary \
  --title="Sprint Planning" \
  --start="2026-01-20T10:00:00" \
  --end="2026-01-20T11:30:00" \
  --location="Conference Room A" \
  --description="Q1 sprint planning meeting"

# Add attendees
gog calendar create primary \
  --title="1:1 Meeting" \
  --start="2026-01-16T09:00:00" \
  --end="2026-01-16T09:30:00" \
  --attendees="colleague@company.com"
```

### Manage Events

```bash
# Get event details
gog calendar event <calendarId> <eventId>

# Update an event
gog calendar update primary <eventId> --title="Updated Title"

# Delete an event
gog calendar delete primary <eventId>

# Respond to invitation
gog calendar respond primary <eventId> --response=accepted
```

### Advanced Calendar

```bash
# Check free/busy for scheduling
gog calendar freebusy "email1@company.com,email2@company.com" --from="2026-01-15" --to="2026-01-16"

# Find conflicts in your calendar
gog calendar conflicts --days=7

# Set focus time
gog calendar focus-time --from="2026-01-15T09:00:00" --to="2026-01-15T12:00:00"

# Set out of office
gog calendar out-of-office --from="2026-01-20" --to="2026-01-24"
```

## Gmail Operations

### Read Emails

```bash
# Search emails (Gmail query syntax)
gog gmail search "is:unread"
gog gmail search "from:ceo@company.com"
gog gmail search "subject:urgent after:2026/01/01"
gog gmail search "has:attachment"

# Get recent emails with JSON output
gog gmail search "is:unread" --json

# Get specific message
gog gmail get <messageId>

# Get message metadata only
gog gmail get <messageId> --format=metadata
```

### Send Emails

```bash
# Send a simple email
gog gmail send \
  --to="recipient@company.com" \
  --subject="Meeting Follow-up" \
  --body="Thank you for the meeting today."

# Send with CC
gog gmail send \
  --to="main@company.com" \
  --cc="manager@company.com" \
  --subject="Project Update" \
  --body="Here's the weekly update..."

# Send with attachment
gog gmail send \
  --to="team@company.com" \
  --subject="Report" \
  --body="Please find attached." \
  --attach="/path/to/report.pdf"
```

### Organize Emails

```bash
# List labels
gog gmail labels list

# Modify thread labels
gog gmail thread modify <threadId> --add-labels="IMPORTANT" --remove-labels="INBOX"
```

## Tasks Operations

### List Tasks

```bash
# List all task lists
gog tasks lists list

# List tasks in a specific list
gog tasks list <tasklistId>

# Show completed tasks too
gog tasks list <tasklistId> --show-completed

# Output as JSON
gog tasks list <tasklistId> --json
```

### Manage Tasks

```bash
# Add a new task
gog tasks add <tasklistId> --title="Review PR #123"

# Add with due date
gog tasks add <tasklistId> --title="Submit report" --due="2026-01-20"

# Add with notes
gog tasks add <tasklistId> --title="Prepare slides" --notes="For the Q1 review meeting"

# Mark task complete
gog tasks done <tasklistId> <taskId>

# Update task
gog tasks update <tasklistId> <taskId> --title="Updated title"

# Delete task
gog tasks delete <tasklistId> <taskId>
```

## Drive Operations

```bash
# List files in root
gog drive list

# List files in folder
gog drive list <folderId>

# Search files
gog drive search "name contains 'report'"

# Download file
gog drive download <fileId> --output="/path/to/save"

# Upload file
gog drive upload /path/to/file --parent=<folderId>
```

## Docs/Slides/Sheets

```bash
# Export Google Doc as PDF
gog docs export <docId> --format=pdf --output="document.pdf"

# Export as docx
gog docs export <docId> --format=docx --output="document.docx"

# Get slides presentation info
gog slides info <presentationId>

# Get sheet data
gog sheets get <spreadsheetId> <range>
```

## Common Patterns for Agents

### Check Today's Schedule

```bash
# Get today's events in a parseable format
gog calendar events --from="$(date +%Y-%m-%d)" --to="$(date -v+1d +%Y-%m-%d)" --json
```

### Check Unread Emails

```bash
# Get unread count and subjects
gog gmail search "is:unread newer_than:1d" --json | jq '.threads | length'
```

### Quick Task Creation from Issue

```bash
# Create task linked to JIRA issue
gog tasks add "@default" --title="PROJ-123: Implement feature X" --due="2026-01-20"
```

### Find Available Meeting Time

```bash
# Check team availability
gog calendar freebusy "tom@company.com,alice@company.com" \
  --from="$(date +%Y-%m-%d)" \
  --to="$(date -v+5d +%Y-%m-%d)" \
  --json
```

## Output Formats

| Flag      | Description            | Use Case           |
| --------- | ---------------------- | ------------------ |
| `--json`  | JSON output            | Parsing in scripts |
| `--plain` | TSV output             | Simple parsing     |
| (default) | Colored human-readable | Interactive use    |

## When to Use CLI vs MCP Tools

| Task                        | Use CLI               | Use MCP             |
| --------------------------- | --------------------- | ------------------- |
| Quick calendar check        | `gog calendar events` | -                   |
| Send email                  | `gog gmail send`      | -                   |
| Complex slides manipulation | -                     | `ai_first_slides_*` |
| Presentation updates        | -                     | `ai_first_slides_*` |
| WhatsApp integration        | -                     | `whatsapp_*`        |
| Slack integration           | -                     | `ai_first_slack_*`  |

**Rule of thumb:** Use CLI for simple read/write operations. Use MCP tools for complex operations that need the assistant's context or don't have CLI equivalents.
