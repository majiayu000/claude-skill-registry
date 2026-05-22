---
name: Agent Inbox
description: Check and process messages from autonomous AILANG agents. Use when starting a session, after agent handoffs, or when checking for completion notifications.
---

# Agent Inbox

**Check for messages from autonomous agents at session start and process completion notifications.**

## Quick Start

**Most common usage:**
```bash
# List all messages
ailang messages list

# Show only unread messages
ailang messages list --unread

# Read full message content
ailang messages read MSG_ID

# Acknowledge (mark as read)
ailang messages ack MSG_ID
ailang messages ack --all

# Send a message
ailang messages send user "Your message" --title "Title" --from "agent-name"

# Send bug/feature to GitHub (for cross-instance visibility)
ailang messages send user "Bug report" --type bug --github
```

**Expected output (at session start):**
```
📬 AGENT INBOX: 2 unread message(s) from autonomous agents
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ID: msg_20251210_143021_abc123
From: sprint-executor
Title: Sprint M-S1 complete
Time: 2025-12-10T14:30:21Z

ID: msg_20251210_143055_def456
From: stapledon
Title: Parser Bug
Time: 2025-12-10T14:30:55Z
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## When to Use This Skill

**Invoke this skill when:**
- **Session starts** - First action in every Claude Code session (required by CLAUDE.md)
- **After handoffs** - When you've sent work to autonomous agents
- **Periodic checks** - User asks "any updates from agents?"
- **Debugging** - To see agent communication history

## Storage Backend

All messages stored in SQLite database:
- **Location**: `~/.ailang/state/collaboration.db`
- **Accessible via**: CLI (`ailang messages`) and Collaboration Hub dashboard
- **Message statuses**: `unread`, `read`, `archived`, `deleted`

## Available Commands

### List Messages

```bash
ailang messages list                    # All messages
ailang messages list --unread           # Only unread
ailang messages list --inbox user       # Filter by inbox
ailang messages list --from agent-name  # Filter by sender
ailang messages list --json             # JSON output
ailang messages list --limit 50         # Limit results
```

### Read Full Message

```bash
ailang messages read MSG_ID             # Full content, marks as read
ailang messages read MSG_ID --peek      # View without marking read
ailang messages read MSG_ID --json      # JSON output
```

### Acknowledge Messages

```bash
ailang messages ack MSG_ID              # Mark specific message as read
ailang messages ack --all               # Mark all as read
ailang messages ack --all --inbox user  # Mark all in inbox as read
```

### Un-acknowledge (Mark Unread)

```bash
ailang messages unack MSG_ID            # Move back to unread
```

### Send Messages

```bash
# Basic send (local only - for coordination)
ailang messages send INBOX "message" --title "Title" --from "agent"

# With GitHub sync (for bugs/features - cross-instance visibility)
ailang messages send INBOX "message" --type bug --github
ailang messages send INBOX "message" --type feature --github
ailang messages send INBOX "message" --github --repo owner/repo
```

### Import from GitHub

```bash
ailang messages import-github                    # Import from default repo
ailang messages import-github --repo owner/repo  # Specific repo
ailang messages import-github --labels bug,help  # Filter by labels
ailang messages import-github --dry-run          # Preview without importing
```

## Workflow

### 1. Session Start Check (REQUIRED)

**SessionStart hook runs automatically and shows unread messages.**

**If messages exist:**
- Read and summarize each message to user
- Identify message type (completion, error, handoff)
- Ask user if they want action taken
- Acknowledge after handling: `ailang messages ack --all`

### 2. Process Completion Notifications

**When agent reports completion:**
```bash
# 1. Read the full message
ailang messages read MSG_ID

# 2. Review results mentioned in payload
ls -la eval_results/baselines/v0.4.2/

# 3. Report to user
echo "Sprint complete! Results at: eval_results/baselines/v0.4.2/"

# 4. Acknowledge after processing
ailang messages ack MSG_ID
```

### 3. Handle Error Reports

**When agent reports errors:**
```bash
# 1. Read the full error details
ailang messages read MSG_ID

# 2. Check logs if mentioned
cat .ailang/state/logs/sprint-executor.log

# 3. Diagnose and report to user
echo "Agent encountered error: Tests failing at milestone 3/5"

# 4. Either fix manually or send corrective instructions
```

### 4. Respond to Agent or User

```bash
# Send response to an agent
ailang messages send sprint-executor "Approved, proceed" \
  --title "Approval" --from "user"

# Send notification to user inbox
ailang messages send user "Issue resolved" \
  --title "Status update" --from "claude-code"
```

## GitHub Integration (Bi-directional)

### Message Types and Routing

| Type | Purpose | Goes to GitHub? |
|------|---------|-----------------|
| `bug` | Bug report | Yes (with `--github`) |
| `feature` | Feature request | Yes (with `--github`) |
| `general` | Coordination | No (local only) |

**Routing guidance:**
- **Bugs and features** → Use `--github` for visibility across all AILANG instances
- **Coordination messages** → Local only, for agent-to-agent communication
- **Instructions from humans** → Create GitHub issues, they'll be imported automatically

### Sending to GitHub (Agent → GitHub)

```bash
# Bug reports and feature requests go to GitHub for visibility
ailang messages send user "Parser crash" --type bug --github
ailang messages send user "Need async support" --type feature --github
```

### Importing from GitHub (GitHub → Local)

```bash
# Runs automatically on session start (if auto_import: true in config)
ailang messages import-github

# Or manually with filters
ailang messages import-github --labels help-wanted
```

### Human Instructions via GitHub

You can write instructions as GitHub issues and have agents pick them up:

1. Create issue on GitHub with `ailang-message` label
2. Next session, `import-github` runs automatically
3. Issue appears in agent's inbox as a message
4. Agent reads and acts on the instructions

### Configuration

Create `~/.ailang/config.yaml`:

```yaml
github:
  expected_user: YourGitHubUsername   # REQUIRED: Must match gh auth status
  default_repo: sunholo-data/ailang   # Default repo for issues
  create_labels:
    - ailang-message
  watch_labels:
    - ailang-message
  auto_import: true                   # Auto-import on session start
```

**Prerequisites:**
1. Install GitHub CLI: `brew install gh`
2. Authenticate: `gh auth login`
3. Check account: `gh auth status`
4. Switch if needed: `gh auth switch --user USERNAME`

**Auto-label creation:** Labels are automatically created if they don't exist:
- `from:agent-name` (purple) - who sent the message
- `bug` (red), `feature` (cyan), `general` (light blue)
- `ailang-message` (blue) - identifies AILANG messages

## Correlation IDs

**Messages support correlation IDs for tracking handoff chains:**

```json
{
  "message_id": "msg_20251210_103045_abc123",
  "correlation_id": "sprint_M-S1",
  "from_agent": "sprint-executor",
  "to_inbox": "user",
  "title": "Sprint complete",
  "payload": "All milestones complete"
}
```

**Benefits:**
- Track entire workflow: design-doc → sprint-plan → execution
- Filter messages by workflow
- Debug multi-agent interactions
- Resume work from where you left off

**For complete specification**, see [`resources/message_format.md`](resources/message_format.md)

## Message Types (Payloads)

### Completion Notification
```json
{
  "type": "sprint_complete",
  "correlation_id": "sprint_M-S1",
  "payload": {
    "sprint_id": "M-S1",
    "milestones_complete": 5,
    "result": "All tests passing"
  }
}
```

### Error Report
```json
{
  "type": "error",
  "correlation_id": "sprint_M-S1",
  "payload": {
    "error": "Tests failing: 5 benchmarks broken",
    "details": ".ailang/state/logs/sprint-executor.log"
  }
}
```

### Handoff Instruction
```json
{
  "type": "plan_ready",
  "correlation_id": "sprint_M-S1",
  "payload": {
    "sprint_id": "M-S1",
    "plan_path": "design_docs/planned/M-S1-plan.md"
  }
}
```

## Resources

### Message Format Reference
See [`resources/message_format.md`](resources/message_format.md) for complete message format specification.

### Troubleshooting Guide
See [`resources/troubleshooting.md`](resources/troubleshooting.md) for common issues and solutions.

## CLI Command Reference

| Command | Purpose |
|---------|---------|
| `ailang messages list` | View all messages |
| `ailang messages list --unread` | View only unread |
| `ailang messages read MSG_ID` | View full message |
| `ailang messages ack MSG_ID` | Mark as read |
| `ailang messages ack --all` | Mark all as read |
| `ailang messages unack MSG_ID` | Mark as unread |
| `ailang messages send INBOX "msg"` | Send message |
| `ailang messages reply MSG_ID "text"` | Reply to GitHub issue thread |
| `ailang messages import-github` | Import from GitHub |
| `ailang messages watch` | Watch for new messages |
| `ailang messages cleanup` | Remove old messages |

**Aliases:** `msg` is an alias for `messages`
```bash
ailang msg list        # Same as: ailang messages list
```

## Notes

- **Required by CLAUDE.md**: Session start check is mandatory
- **SQLite backend**: All messages in `~/.ailang/state/collaboration.db`
- **Hook integration**: SessionStart hook auto-imports GitHub issues and shows unread
- **Auto-marking**: Messages marked as read when using `ailang messages read`
- **Message lifecycle**: Unread → Read → Archived (optional)
- **GitHub sync**: Optional, for bugs/features that need cross-instance visibility
