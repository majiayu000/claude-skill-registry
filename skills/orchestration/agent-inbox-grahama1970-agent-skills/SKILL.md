---
name: agent-inbox
description: >
  File-based inter-agent messaging with headless dispatch. Check inbox, send bugs/requests to other projects,
  automatically spawn headless agents to fix bugs, and track progress via task-monitor.
allowed-tools: Bash, Read
triggers:
  - check your inbox
  - check inbox
  - check messages
  - any messages
  - any pending messages
  - check for messages
  - agent sent you
  - sent you an issue
  - sent you a bug
  - address the bug
  - fix the issue from
  - message from agent
  - inter-agent message
  - send message to
  - send bug to
  - send to project's inbox
  - send to project's /agent-inbox
  - send the bug to
  - notify the agent
  - tell the other agent
  - cross-project message
  - pending issues
  - pending bugs
  - dispatch bug fix
  - headless agent
  - spawn agent
  - report bug to
  - forward message to
  - message extractor project
  - send to the project's inbox
metadata:
  short-description: Inter-agent messaging with headless dispatch and task-monitor integration
provides:
  - inter-agent-messaging
  - headless-dispatch
  - triage-routing
composes:
  - task-monitor
  - memory
---

# Agent Inbox Skill

File-based inter-agent message system with **headless dispatch** and **task-monitor integration**. When bugs are reported, the system can automatically spawn a headless agent (Claude, Codex) with the specified model to fix the issue, tracking progress in real-time.

## Key Features (v2)

- **Headless Dispatch**: Auto-spawn agents when bugs are reported
- **Model Selection**: Choose `sonnet`, `opus-4.5`, `codex-5.2`, or `codex-5.2-high`
- **Task-Monitor Integration**: Live progress tracking (0% → 25% → 50% → 75% → 100%)
- **Verification Gates**: Run test commands before auto-ack
- **Exchange Threading**: Reply to messages, view full threads
- **Auto-Ack**: Automatic acknowledgment when fixes are verified
- **AI Triage**: Automatic severity classification and model recommendation
- **Auto-Routing**: Detect target project from file paths in error messages
- **Webhooks**: POST notifications on status changes
- **Triage Logging**: Audit trail for all classification decisions

## When to Use

- Agent A finds a bug in project B's code
- Agent needs to request help from another project's agent
- Passing information between project workspaces
- Any cross-project agent communication
- **Automated bug-fix workflows with headless agents**

## Proactive Checking (Important!)

**Agents should check inbox automatically when:**

- Starting a new session
- User mentions another agent or project by name
- User says "check your inbox" or similar
- Switching projects or context
- Before starting major work (in case blockers exist)

**If you're an AI agent reading this:** Run `.pi/skills/agent-inbox/agent-inbox check` proactively when the user mentions inter-project communication. Don't wait to be explicitly told.

## Running the Skill (No Global Install Needed)

The repo already includes a wrapper script (`.pi/skills/agent-inbox/agent-inbox`). Run it directly or invoke the Python entrypoint—no global install or PATH hacks required.

```bash
# Preferred: run the bundled wrapper
.pi/skills/agent-inbox/agent-inbox check

# Alternate: call Python explicitly
python .pi/skills/agent-inbox/inbox.py check
```

If you want convenience aliases, you can add the skill folder to `PATH`, but it’s optional and not assumed anywhere in this doc.

## Setup (One-Time)

Register your projects so agent-inbox knows where they are:

```bash
# Register projects (use direct path if agent-inbox not on PATH)
.pi/skills/agent-inbox/agent-inbox register memory /home/user/workspace/memory
.pi/skills/agent-inbox/agent-inbox register scillm /home/user/workspace/litellm

# List registered projects
.pi/skills/agent-inbox/agent-inbox projects

# Check which project current directory maps to
.pi/skills/agent-inbox/agent-inbox whoami

# Unregister if needed
.pi/skills/agent-inbox/agent-inbox unregister old-project
```

## Quick Start

```bash
# Send a bug report with model specification (spawns headless Opus agent)
python inbox.py send --to scillm --type bug --model opus-4.5 "
File: scillm/extras/providers.py:328
Error: UnboundLocalError on 'options'
Fix: Rename local variable to avoid shadowing
"

# Send bug with verification command (auto-ack only if test passes)
python inbox.py send --to scillm --type bug --model codex-5.2-high \
  --test "pytest tests/test_providers.py -x" \
  "Race condition in provider initialization"

# Check for pending messages (anytime)
python inbox.py check

# List all pending messages
python inbox.py list

# Read a specific message
python inbox.py read scillm_abc123

# Acknowledge when fixed
python inbox.py ack scillm_abc123 --note "Fixed: renamed to merged_options"
```

## Headless Dispatch (v2)

### Model Selection

When sending bugs, specify which AI model should handle the fix:

| Model            | Command                                        | Use Case                        |
| ---------------- | ---------------------------------------------- | ------------------------------- |
| `sonnet`         | `claude --model sonnet`                        | Simple fixes, typos             |
| `opus-4.5`       | `claude --model opus`                          | Complex analysis, architecture  |
| `codex-5.2`      | `codex --model gpt-5.2-codex`                  | Standard bug fixes              |
| `codex-5.2-high` | `codex --model gpt-5.2-codex --reasoning high` | Deep reasoning, race conditions |

```bash
# Use Opus for complex architectural bug
python inbox.py send --to scillm --type bug --model opus-4.5 "Complex race condition..."

# Use Codex with high reasoning for tricky logic bug
python inbox.py send --to scillm --type bug --model codex-5.2-high "Off-by-one in pagination..."
```

### Dispatch Options

| Option                 | Description                          | Default  |
| ---------------------- | ------------------------------------ | -------- |
| `--model MODEL`        | AI model for headless agent          | `sonnet` |
| `--timeout MINUTES`    | Max time for agent to work           | `30`     |
| `--test COMMAND`       | Verification command before auto-ack | None     |
| `--no-dispatch`        | Disable auto-spawn (manual only)     | False    |
| `--register-path PATH` | Auto-register target project         | None     |
| `--context-file FILE`  | Attach file as context (repeatable)  | None     |

### Context Files

Attach relevant files (stack traces, error logs, code snippets) to help the agent:

```bash
# Attach a single context file
python inbox.py send --to scillm --type bug --model opus-4.5 \
  --context-file /tmp/error.log \
  "Server crash on startup"

# Attach multiple context files
python inbox.py send --to scillm --type bug --model opus-4.5 \
  --context-file src/server.py \
  --context-file /tmp/traceback.txt \
  "Race condition in server initialization"
```

### Memory Recall Pre-Hook

The dispatcher automatically queries `/memory` before spawning agents to find:

- **Similar bugs** that were fixed before
- **Lessons learned** from past solutions
- **Relevant context** from the knowledge base

This context is injected into the agent's prompt:

```
## Prior Solutions from Memory

The following relevant lessons and solutions were found:

**Problem**: Undefined variable in initialization
**Solution**: Import the module at top of file
**Lesson**: Always check imports when seeing undefined variable errors
```

The agent reviews prior solutions first, avoiding reinventing the wheel.

## AI Triage (v2)

When sending bugs or requests, the system automatically performs AI-powered triage:

### Severity Classification

The AI analyzes the message and assigns severity based on:

| Severity   | Priority | Indicators                                    | Model      |
| ---------- | -------- | --------------------------------------------- | ---------- |
| `critical` | critical | crash, data loss, security, production down   | `opus-4.5` |
| `high`     | high     | error, exception, failure, broken, regression | `opus-4.5` |
| `medium`   | normal   | bug, issue, incorrect, unexpected             | `sonnet`   |
| `low`      | low      | typo, cosmetic, enhancement, minor            | `sonnet`   |

```bash
# Triage automatically adjusts priority and model
python inbox.py send --to scillm --type bug "Critical crash in production"
#   AI Triage: priority adjusted to 'critical'
#   AI Triage: model set to 'opus-4.5'
```

### Auto-Routing

The system extracts file paths from error messages and matches them against registered projects:

```bash
# File path in error suggests target project
python inbox.py send --to unknown-project --type bug "
Error in File /home/user/workspace/scillm/providers.py:328
TypeError: cannot access local variable 'options'
"
#   AI Triage: suggested project 'scillm' (using 'unknown-project')
```

### Triage CLI

Manual triage operations:

```bash
# Classify a message
python inbox.py triage classify --message "Critical crash in auth module" --no-llm
# Severity: critical
# Priority: critical
# Model: opus-4.5
# Reasoning: Matched indicators: ['crash']

# Auto-route based on file paths
python inbox.py triage route --message "Error in /home/user/workspace/memory/search.py:45"
# Suggested project: memory

# View triage log for a message
python inbox.py triage log --msg-id scillm_abc123
```

### Controlling Triage

```bash
# Skip AI triage for this message
python inbox.py send --to scillm --type bug --no-triage "Simple typo fix"

# Force user's priority over AI suggestion
python inbox.py send --to scillm --type bug --priority normal --priority-override "Crash that isn't urgent"
```

## Webhooks (v2)

Register webhooks to receive POST notifications on status changes:

```bash
# Register a webhook
python inbox.py triage webhook-add --url "https://example.com/webhook" \
  --events "message_sent,status_changed,message_acked"

# Filter to specific project
python inbox.py triage webhook-add --url "https://example.com/scillm-hook" \
  --events "status_changed" --project scillm

# List webhooks
python inbox.py triage webhook-list

# Remove webhook
python inbox.py triage webhook-remove --url "https://example.com/webhook"
```

### Webhook Events

| Event            | Trigger                                      |
| ---------------- | -------------------------------------------- |
| `message_sent`   | New bug/request sent                         |
| `status_changed` | Status updated (pending → dispatched → done) |
| `message_acked`  | Message acknowledged                         |

### Webhook Payload

```json
{
  "event": "status_changed",
  "timestamp": "2026-01-30T18:00:00Z",
  "data": {
    "msg_id": "scillm_abc123",
    "old_status": "pending",
    "new_status": "in_progress",
    "to": "scillm",
    "from": "extractor",
    "type": "bug",
    "note": "Agent working on fix"
  }
}
```

## Triage Logging (v2)

All triage decisions are logged for audit trail:

```
~/.agent-inbox/
└── triage_logs/
    ├── scillm_abc123_triage.json    # Individual triage log
    └── triage_20260130.jsonl         # Daily aggregate log
```

```bash
# View triage log for a message
python inbox.py triage log --msg-id scillm_abc123 --json
{
  "msg_id": "scillm_abc123",
  "timestamp": "2026-01-30T18:00:00Z",
  "classification": {
    "severity": "critical",
    "priority": "critical",
    "reasoning": "Matched indicators: ['crash', 'security']"
  },
  "routing": {
    "target_project": "scillm",
    "method": "auto"
  }
}
```

### Verification Gate

Use `--test` to require verification before auto-acknowledgment:

```bash
# Only ack if tests pass
python inbox.py send --to scillm --type bug --model opus-4.5 \
  --test "pytest tests/ -x" \
  "Bug in authentication flow"

# Status progression:
# pending → dispatched → in_progress → needs_verification (if test fails) → done
```

## Exchange Threading (v2)

Messages can form threaded exchanges:

```bash
# Send initial bug
python inbox.py send --to scillm --type bug --model sonnet "Bug report..."
# → Message ID: scillm_abc123

# Reply to message (auto-threads)
python inbox.py reply scillm_abc123 "I've started investigating..."
# → Thread: scillm_abc123

# View full thread
python inbox.py thread scillm_abc123
# === Thread: scillm_abc123 (2 messages) ===
# [scillm_abc123] extractor → scillm (bug)
#   ↳ [scillm_def456] scillm → extractor (info)
```

## Task-Monitor Integration (v2)

All bug-fix tasks are automatically tracked in task-monitor:

```bash
# Start task-monitor TUI (in separate terminal)
python .pi/skills/task-monitor/monitor.py

# Send bug - automatically registers task
python inbox.py send --to scillm --type bug --model opus-4.5 "Bug..."
# [task-monitor] Registered task: bug-fix-scillm_abc123

# View progress in TUI:
# ┌─────────────────────────────────────────────────────────────┐
# │  bug-fix-scillm_abc123        [=========>    ] 50%         │
# │  [opus-4.5] Bug fix from extractor                         │
# │  Status: in_progress                                        │
# └─────────────────────────────────────────────────────────────┘
```

### Status Progression

| Status               | Progress | Description                          |
| -------------------- | -------- | ------------------------------------ |
| `pending`            | 0%       | Message received, not yet dispatched |
| `dispatched`         | 25%      | Headless agent spawned               |
| `in_progress`        | 50%      | Agent actively working               |
| `needs_verification` | 75%      | Fix attempted, test failed           |
| `done`               | 100%     | Fix verified and auto-acked          |

## Dispatcher Daemon (v2)

The dispatcher watches the inbox and auto-spawns agents:

```bash
# Start dispatcher daemon (background)
python dispatcher.py start

# Start in foreground (for debugging)
python dispatcher.py start --foreground

# Check dispatcher status
python dispatcher.py status
# Dispatcher: RUNNING (PID 12345)
# Pending messages: 5
# Ready to dispatch: 2

# Stop dispatcher
python dispatcher.py stop

# List supported models
python dispatcher.py models
```

## CLI Commands (Wrapper ≙ `python inbox.py`)

### `register` - Register a project (one-time setup)

```bash
.pi/skills/agent-inbox/agent-inbox register <name> <path>

# Examples:
.pi/skills/agent-inbox/agent-inbox register memory /home/user/workspace/memory
.pi/skills/agent-inbox/agent-inbox register scillm /home/user/workspace/litellm
```

### `unregister` - Remove a project

```bash
.pi/skills/agent-inbox/agent-inbox unregister <name>
```

### `projects` - List registered projects

```bash
.pi/skills/agent-inbox/agent-inbox projects
.pi/skills/agent-inbox/agent-inbox projects --json
```

### `whoami` - Show detected project for current directory

```bash
.pi/skills/agent-inbox/agent-inbox whoami
```

### `send` - Send a message to another project

```bash
python inbox.py send --to PROJECT --type TYPE --priority PRIORITY "message"

# Types: bug, request, info, question
# Priority: low, normal, high, critical

# v2 Options:
# --model {sonnet,opus-4.5,codex-5.2,codex-5.2-high}  AI model for headless agent
# --timeout MINUTES                                   Agent timeout (default: 30)
# --test COMMAND                                      Verification command
# --no-dispatch                                       Disable auto-spawn
# --reply-to MSG_ID                                   Reply to existing message
# --register-path PATH                                Auto-register target project
# --dry-run                                           Show message JSON without sending

# Examples:
python inbox.py send --to memory --type request "Please add 'proved_only' parameter to search()"
python inbox.py send --to scillm --type bug --model opus-4.5 --priority critical "Server crashes on startup"

# With verification command
python inbox.py send --to scillm --type bug --model codex-5.2-high \
  --test "pytest tests/ -x" \
  "Race condition in worker pool"

# Auto-register project path when sending
python inbox.py send --to new-project --type bug --register-path /path/to/project "Bug..."

# Read message from stdin (useful for multi-line)
cat error.log | python inbox.py send --to scillm --type bug --model sonnet
```

### `list` - List messages

```bash
.pi/skills/agent-inbox/agent-inbox list                      # All pending
.pi/skills/agent-inbox/agent-inbox list --project scillm     # For specific project
.pi/skills/agent-inbox/agent-inbox list --status done        # Completed messages
.pi/skills/agent-inbox/agent-inbox list --json               # JSON output
```

### `read` - Read a specific message

```bash
.pi/skills/agent-inbox/agent-inbox read MSG_ID
.pi/skills/agent-inbox/agent-inbox read MSG_ID --json
```

### `ack` - Acknowledge/complete a message

```bash
.pi/skills/agent-inbox/agent-inbox ack MSG_ID
.pi/skills/agent-inbox/agent-inbox ack MSG_ID --note "Fixed in commit abc123"
```

### `check` - Check inbox (for hooks)

```bash
python inbox.py check                     # Check current project
python inbox.py check --project scillm    # Check specific project
python inbox.py check --all               # Check all registered projects
python inbox.py check --quiet             # Just return count (exit code 1 if messages)
```

### `update-status` - Update message status (v2)

```bash
python inbox.py update-status MSG_ID STATUS [--note NOTE]

# Status values: pending, dispatched, in_progress, needs_verification, done
# Examples:
python inbox.py update-status scillm_abc123 in_progress --note "Agent working"
python inbox.py update-status scillm_abc123 done --note "Fixed in commit xyz"
```

### `reply` - Reply to a message (v2)

```bash
python inbox.py reply MSG_ID "Reply message"

# Auto-sets thread_id and parent_id
# Reply goes TO the original sender

# Example:
python inbox.py reply scillm_abc123 "I've started investigating this bug"
python inbox.py reply scillm_abc123 --type info --model sonnet "Here's what I found..."
```

### `thread` - View message thread (v2)

```bash
python inbox.py thread THREAD_ID
python inbox.py thread THREAD_ID --json

# Shows all messages in chronological order with relationships
```

## Integration with Claude Code Hooks

Add to your project's `.claude/settings.json`:

```json
{
  "hooks": {
    "on_session_start": [
      ".pi/skills/agent-inbox/agent-inbox check --project $(basename $PWD) || true"
    ]
  }
}
```

Or add to your shell profile to check on every new terminal:

```bash
# ~/.bashrc or ~/.zshrc
alias claude-start='.pi/skills/agent-inbox/agent-inbox check --project $(basename $PWD); claude'
```

## Message Format

Messages are stored as JSON in `~/.agent-inbox/`:

```
~/.agent-inbox/
├── pending/           # Unprocessed messages
│   └── scillm_abc123.json
├── done/              # Acknowledged messages
│   └── memory_def456.json
├── logs/              # Dispatch logs (v2)
│   └── scillm_abc123_20260130_123456.log
├── task_states/       # Task-monitor state files (v2)
│   └── bug-fix-scillm_abc123.json
├── triage_logs/       # AI triage decision logs (v2)
│   ├── scillm_abc123_triage.json
│   └── triage_20260130.jsonl
├── webhooks.json      # Registered webhooks (v2)
└── projects.json      # Project registry
```

### Message Schema (v2)

```json
{
  "id": "scillm_abc123",
  "to": "scillm",
  "from": "extractor",
  "type": "bug",
  "priority": "critical",
  "priority_source": "ai_triage",
  "status": "in_progress",
  "created_at": "2026-01-11T20:30:00Z",
  "message": "File: providers.py:328\nError: UnboundLocalError...",

  // v2 dispatch config (if model specified)
  "dispatch": {
    "model": "opus-4.5",
    "auto_spawn": true,
    "timeout_minutes": 30,
    "test_command": "pytest tests/ -x"
  },

  // v2 AI triage (auto-added for bugs/requests)
  "triage": {
    "severity": "critical",
    "reasoning": "Matched indicators: ['crash', 'security']",
    "complexity": "moderate",
    "affected_area": "authentication"
  },
  "triage_suggested_project": "scillm",

  // v2 threading (if part of exchange)
  "thread_id": "scillm_abc123",
  "parent_id": null,

  // v2 status tracking
  "status_updated_at": "2026-01-11T20:35:00Z",
  "status_notes": [
    { "status": "dispatched", "note": "PID: 12345", "at": "..." },
    { "status": "in_progress", "note": "Agent working", "at": "..." }
  ]
}
```

### Task State File (v2)

```json
{
  "completed": 2,
  "total": 4,
  "status": "in_progress",
  "description": "[opus-4.5] Bug fix from extractor",
  "current_item": "Working on providers.py",
  "stats": {
    "inbox_msg_id": "scillm_abc123",
    "from_project": "extractor",
    "to_project": "scillm",
    "model": "opus-4.5",
    "priority": "high"
  },
  "last_updated": "2026-01-11T20:35:00Z"
}
```

## Environment Variables

| Variable               | Description                             | Default                 |
| ---------------------- | --------------------------------------- | ----------------------- |
| `AGENT_INBOX_DIR`      | Inbox directory location                | `~/.agent-inbox`        |
| `TASK_MONITOR_API_URL` | Task-monitor HTTP API URL               | `http://localhost:8765` |
| `CLAUDE_PROJECT`       | Current project name (for `from` field) | auto-detected           |

## Workflow Examples

### Manual Workflow (v1)

**Agent A (extractor project) finds bug:**

```bash
python inbox.py send --to scillm --type bug --priority high "
Bug in scillm/extras/providers.py:328
Error: UnboundLocalError: cannot access local variable 'options'
Suggested fix: Rename to merged_options
"
```

**User switches to scillm project, Agent B fixes and acknowledges:**

```bash
python inbox.py ack scillm_a1b2c3d4 --note "Fixed: renamed to merged_options"
```

### Automated Workflow with Headless Dispatch (v2)

**Step 1: Agent A sends bug with model specification**

```bash
# From extractor project
python inbox.py send --to scillm --type bug --model opus-4.5 \
  --test "pytest tests/test_providers.py -x" "
Race condition in provider initialization.
Error: Worker threads occasionally read stale config.
Stack trace: [...]
"
# Output:
# [task-monitor] Registered task: bug-fix-scillm_abc123
# Message sent: scillm_abc123
#   From: extractor -> To: scillm
#   Model: opus-4.5 (auto_spawn=True)
```

**Step 2: Dispatcher daemon picks up the message**

```bash
# Dispatcher running in background detects new message
# [dispatcher] Found 1 message(s) ready for dispatch
# [dispatcher] Spawning agent for scillm_abc123 with model opus-4.5
# [dispatcher] Started process 12345
```

**Step 3: Task-monitor shows real-time progress**

```
┌───────────────────────────────────────────────────────────┐
│  bug-fix-scillm_abc123      [=========>      ] 50%        │
│  [opus-4.5] Bug fix from extractor                        │
│  Status: in_progress | Working on providers.py            │
└───────────────────────────────────────────────────────────┘
```

**Step 4: Verification runs before auto-ack**

```bash
# [dispatcher] Running verification: pytest tests/test_providers.py -x
# [dispatcher] Verification PASSED for scillm_abc123
# [dispatcher] Fix completed and acked for scillm_abc123
```

**Step 5: Message auto-acked, moved to done/**

```bash
python inbox.py list --status done
# ✅ scillm_abc123: ack_note="Fix verified. Test: pytest tests/..."
```

### Threaded Exchange Example

```bash
# Agent A reports bug
python inbox.py send --to scillm --type bug --model sonnet "Bug in X"
# → scillm_abc123

# Agent B asks for clarification (threading)
python inbox.py reply scillm_abc123 "Can you provide the stack trace?"
# → extractor_def456 (thread: scillm_abc123)

# Agent A provides more info
python inbox.py reply extractor_def456 "Stack trace: [...]"
# → scillm_ghi789 (thread: scillm_abc123)

# View full exchange
python inbox.py thread scillm_abc123
# === Thread: scillm_abc123 (3 messages) ===
# [scillm_abc123] extractor → scillm (bug)
#   ↳ [extractor_def456] scillm → extractor (question)
#     ↳ [scillm_ghi789] extractor → scillm (info)
```

## Python API

```python
from inbox import (
    register_project, unregister_project, list_projects,
    send, list_messages, read_message, ack_message, check_inbox
)

# Setup (one-time)
register_project("memory", "/home/user/workspace/memory")
register_project("scillm", "/home/user/workspace/litellm")
list_projects()  # {"memory": "/home/...", "scillm": "/home/..."}

# Send
send("scillm", "Bug report...", msg_type="bug", priority="high")

# List
messages = list_messages(project="scillm")

# Read
msg = read_message("scillm_abc123")

# Ack
ack_message("scillm_abc123", note="Fixed")

# Check (returns count)
count = check_inbox(project="scillm", quiet=True)
```
