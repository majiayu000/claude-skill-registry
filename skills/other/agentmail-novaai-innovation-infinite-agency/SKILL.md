---
name: agentmail
description: Inter-agent communication for tmux sessions. Send and receive messages between AI agents.
version: 1.0.0
author: Konstantin Tumalevich
license: MIT
---

# AgentMail Skill

AgentMail enables communication between AI agents running in different tmux windows through a simple file-based mail system.

## Overview

AgentMail is a CLI tool for inter-agent communication within tmux sessions. Messages are stored in `.agentmail/mailboxes/` as JSONL files, providing persistent, file-locked message queues for each agent.

## Prerequisites

- Must be running inside a tmux session
- AgentMail CLI must be installed and available in PATH
- Messages stored in `.agentmail/` directory

## Core Commands

### Send a Message

```bash
agentmail send <recipient> "<message>"
```

Send a message to another agent. The recipient must be a valid tmux window name.

**Examples:**
```bash
agentmail send agent2 "Can you review the changes in src/api?"
agentmail send -r worker -m "Task completed"
echo "Build succeeded" | agentmail send agent2
```

### Receive Messages

```bash
agentmail receive
```

Read the oldest unread message from your mailbox. Messages are delivered in FIFO order and marked as read after display.

### List Recipients

```bash
agentmail recipients
```

List all tmux windows that can receive messages. Your current window is marked with `[you]`.

### Set Status

```bash
agentmail status <ready|work|offline>
```

Set your availability status:
- `ready` - Available to receive messages and notifications
- `work` - Busy working (suppresses notifications)
- `offline` - Not available (suppresses notifications)

## Workflow

### Checking for Messages

1. Run `agentmail receive` to check for new messages
2. If a message is available, read and process it
3. Optionally reply using `agentmail send`

### Sending Messages

1. Run `agentmail recipients` to see available agents
2. Send your message: `agentmail send <recipient> "<message>"`
3. Confirm delivery via the returned message ID

### Status Management

The plugin automatically manages your status:
- **Session start**: Status set to `ready`
- **Session end**: Status set to `offline`
- **End of turn (Stop)**: Status set to `ready`, checks for new messages

## Message Format

Messages include:
- **ID**: Unique 8-character base62 identifier (a-z, A-Z, 0-9)
- **From**: Sender's tmux window name
- **To**: Recipient's tmux window name
- **Content**: Message body

## Best Practices

1. **Check messages regularly** - Use `agentmail receive` to stay informed
2. **Keep messages concise** - Focus on actionable information
3. **Include context** - Reference files, line numbers, or specific details
4. **Respond promptly** - Other agents may be waiting for your input
5. **Use status appropriately** - Set `work` when focusing on complex tasks

## Integration with Claude Code

This plugin integrates with Claude Code hooks:

- **SessionStart**: Automatically sets status to `ready` and runs onboarding
- **SessionEnd**: Automatically sets status to `offline`
- **Stop**: Sets status to `ready` and checks for new messages

The hooks ensure agents are properly registered and can receive notifications from the mailman daemon.

## Troubleshooting

### "Not in a tmux session"
AgentMail requires tmux. Start a tmux session first.

### "Recipient not found"
The recipient window doesn't exist. Check available windows with `agentmail recipients`.

### "No unread messages"
Your mailbox is empty. Other agents haven't sent you messages yet.

### Messages not being delivered
Ensure the mailman daemon is running: `agentmail mailman --daemon`
