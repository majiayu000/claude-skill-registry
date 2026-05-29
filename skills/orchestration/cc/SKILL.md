---
name: cc
description: Short slash command wrapper for Claude relay sessions. Use when the user wants concise /cc commands like /cc projects, /cc on <project>, /cc tail, /cc off, or /cc <message> to continue talking to Claude Code in the current project session.
metadata: {"openclaw":{"emoji":"⚡","requires":{"bins":["tmux","claude"],"skills":["claude-relay"]}}}
---

# cc

Short operator commands for Claude Code relay sessions.

**Requires**: `claude-relay` skill must be installed.

## Script

All commands execute via:

```bash
{baseDir}/scripts/cc.sh <raw-args>
```

## Command routing

Parse user input and route:

- `projects` / `list` → list available projects from map + project root
- `on <project>` / `start <project>` → start or reuse Claude session (fuzzy match)
- `off [project]` / `stop [project]` → stop session (default: last project)
- `tail [project] [lines]` → show recent output (default: 120 lines)
- `status` → list active relay sessions
- `/cc` (no args) → show inline button menu (if platform supports)
- `/cc on` (no project) → show project picker buttons
- Any other text → **relay mode send** (see below)

For the "any other text" case: if the first token resolves to an active project session, treat it as explicit project target and use remaining text as the message.

## Relay mode

After `on <project>`, enter relay mode. **This is the critical behavior contract**:

1. **ALL user messages are forwarded to Claude Code** — no exceptions. Do NOT interpret, answer, or act on the message yourself. You are a transparent pipe.
2. Forward via `scripts/cc.sh send` → wait for output → return final result only.
3. The ONLY messages NOT forwarded are cc commands themselves: `off`, `tail`, `status`, `projects`, `/cc`.
4. Relay mode ends on `off`, `stop`, or `/cc` menu invocation.

Example:
```
[relay mode active, project=marvis]
User: "帮我查一下这个 bug 的原因"
→ cc.sh send marvis "帮我查一下这个 bug 的原因"
→ wait for Claude Code output
→ return result to user
WRONG: answering the question yourself
```

For button specs, output formatting, approval handling, and callback routing, see [relay-mode.md](references/relay-mode.md).

## Key principles

- **Never self-answer in relay mode**: forward everything, return only Claude Code's output.
- **Final result only**: one message per interaction, no progress updates.
- **Choices → buttons**: numbered menus in Claude Code output become inline buttons.
- **Tool call discipline**: button/menu messages = tool call + `NO_REPLY`, no surrounding text.

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CLAUDE_RELAY_DIR` | (auto-detected) | Path to claude-relay skill directory |
| `CLAUDE_RELAY_ROOT` | `$HOME/projects` | Root directory for project discovery |
| `CLAUDE_RELAY_MAP` | `<relay-skill-dir>/projects.map` | Path to project alias map file |
