---
name: rp-cli
description: "Repo Prompt CLI - proxy MCP client for AI agents to access Repo Prompt's context engineering tools via bash. Build prompts, search code, manage file selections, chat with AI, and export context without MCP configuration."
---

# rp-cli — Repo Prompt CLI

> Proxy MCP client for AI agents to access Repo Prompt via bash commands.
> Version: 1.5.61+

## Overview

`rp-cli` lets AI agents access Repo Prompt's full capabilities through shell commands—no MCP server configuration required. Communicates with running Repo Prompt app over local socket.

**Requirements:**
- Repo Prompt running on Mac
- MCP Server enabled in Repo Prompt settings
- CLI installed (`/usr/local/bin/rp-cli`)

## Quick Reference

```bash
# Verify installation
rp-cli --version

# Core exploration
rp-cli -e 'tree'                              # File tree
rp-cli -e 'tree --mode selected'              # Selected files only
rp-cli -e 'tree --folders'                    # Directories only
rp-cli -e 'workspace list'                    # List all workspaces
rp-cli -e 'search "pattern" --extensions .swift'  # Search code

# File selection
rp-cli -e 'select set src/'                   # Replace selection
rp-cli -e 'select add path/to/file.swift'     # Add to selection
rp-cli -e 'select remove path/to/file.swift'  # Remove from selection
rp-cli -e 'select clear'                      # Clear selection

# Context operations
rp-cli -e 'context'                           # Get full context
rp-cli -e 'context --include prompt,selection,code,files,tree'
rp-cli -e 'read path/to/file.swift'           # Read file contents
rp-cli -e 'structure --scope selected'        # Code structure/codemaps

# AI chat
rp-cli -e 'chat "How does auth work?"'        # Send to AI
rp-cli -e 'chat "Plan refactor" --mode plan'  # Plan mode
rp-cli -e 'chats list'                        # List recent chats

# Prompt management
rp-cli -e 'prompt get'                        # View current prompt
rp-cli -e 'prompt set "New instructions"'     # Replace prompt
rp-cli -e 'prompt append "Additional note"'   # Append to prompt
```

## Command Chaining

Commands chain with `&&` in a single `-e` flag. State carries through:

```bash
rp-cli -e 'workspace switch MyProject && select set src/ && context'
rp-cli -e 'select set src/auth/ && chat "Review this auth flow" --mode plan'
```

## Output Redirection

Write results directly to files:

```bash
rp-cli -e 'tree > /tmp/structure.txt'
rp-cli -e 'context --include files > ~/Desktop/context.md'
rp-cli -e 'prompt export > ~/exports/full-context.md'
```

## Exec Mode Flags

| Flag | Purpose |
|------|---------|
| `-e, --exec <cmd>` | Execute command(s) |
| `-w, --window <id>` | Target specific window |
| `-q, --quiet` | Suppress non-essential output |
| `--raw-json` | JSON output for scripting |
| `--verbose` | Debug/timing info |
| `--fail-fast` | Stop on first error |

## All Commands

| Command | Key Parameters |
|---------|----------------|
| `tree` | `--folders`, `--mode full\|selected` |
| `search`, `grep` | pattern, `--extensions`, `--context-lines` |
| `read`, `cat` | path, `--start-line`, `--limit` |
| `structure`, `map` | paths or `--scope selected` |
| `select`, `sel` | `add\|remove\|set\|clear` paths... |
| `context`, `ctx` | `--include prompt,selection,code,files,tree` |
| `edit`, `replace` | path, search, replace, `--all` |
| `prompt` | `get\|set\|append\|clear\|export` |
| `workspace`, `ws` | `list\|switch\|tabs\|tab` |
| `chat` | message, `--mode chat\|plan\|edit` |
| `chats` | `list\|log`, `--limit` |
| `builder` | instructions, `--response-type plan\|question` |
| `models` | (lists available AI models) |
| `windows` | (lists open windows) |
| `window`, `use` | window ID |
| `file` | `create\|delete\|move` path |
| `call` | tool_name {json_args} |

## MCP Tools (via `call`)

Direct tool invocation with JSON args:

```bash
rp-cli -e 'call read_file {"path":"/tmp/test.txt"}'
rp-cli -e 'call file_search {"pattern":"TODO","filter":{"extensions":[".swift"]}}'
rp-cli -e 'call manage_selection {"op":"get","view":"files"}'
```

**Available tools (14):**
- `apply_edits` — File edits (search/replace or rewrite)
- `chat_send` — AI chat (modes: chat, plan, edit)
- `chats` — List/view chat history
- `context_builder` — Auto-build context for tasks
- `file_actions` — Create, delete, move files
- `file_search` — Search by path/content
- `get_code_structure` — Codemaps for files/dirs
- `get_file_tree` — ASCII directory tree
- `list_models` — Available AI model presets
- `manage_selection` — Curate file selection
- `manage_workspaces` — Workspace operations
- `prompt` — Get/set shared prompt
- `read_file` — Read file contents
- `workspace_context` — Full context snapshot

## Multi-Window / Multi-Tab

```bash
# Target specific window
rp-cli -w 1 -e 'workspace list'
rp-cli -w 2 -e 'context'

# List and target tabs
rp-cli -e 'workspace tabs'
rp-cli -e 'workspace tab "Feature Work" && context'
```

## Workflow Shorthand Flags

One-liner alternatives:

```bash
rp-cli --workspace MyProject --select-set src/ --export-context ~/out.md
rp-cli --chat "Review this code" --mode plan
```

| Flag | Purpose |
|------|---------|
| `--workspace <name>` | Switch workspace |
| `--select-add <paths>` | Add to selection |
| `--select-set <paths>` | Replace selection |
| `--export-context <file>` | Export context to file |
| `--export-prompt <file>` | Export prompt to file |
| `--chat <message>` | Send chat message |
| `--builder <instructions>` | Run Context Builder |

## Script Files (.rp)

Save repeatable workflows:

```bash
# daily-export.rp
workspace switch Frontend
select set src/components/
context --all > ~/exports/frontend.md

workspace switch Backend
select set src/api/
context --all > ~/exports/backend.md
```

Run with:
```bash
rp-cli --exec-file ~/scripts/daily-export.rp
```

## One-Shot Flags (Quick Lookups)

```bash
rp-cli -l                    # List all MCP tools
rp-cli -l explore            # List tools in group
rp-cli -d search             # Detailed help for command
rp-cli -d context            # Detailed help for context
```

## Interactive Mode (REPL)

For exploration and debugging:

```bash
rp-cli -i                    # Start REPL
rp-cli -i -w 1               # REPL with window pre-selected
```

Inside REPL: `help`, `history`, `set`, `status`

## Help System

```bash
rp-cli --help                # Quick reference
rp-cli --help-interactive    # REPL mode
rp-cli --help-scripting      # Scripts and workflow flags
rp-cli --help-advanced       # Tab targeting, routing
rp-cli -d <command>          # Detailed command help
```

## Common Workflows

### Export Context for External Use

```bash
rp-cli -e 'select set src/features/auth/ && context --include prompt,selection,code,files > /tmp/auth-context.md'
```

### Search and Select Results

```bash
rp-cli -e 'search "class.*ViewModel" --extensions .swift'
# Review results, then select relevant files
rp-cli -e 'select set src/ViewModels/'
```

### Plan a Feature

```bash
rp-cli -e 'select set src/features/checkout/ && builder "Add Apple Pay support" --response-type plan'
```

### Code Review via Chat

```bash
rp-cli -e 'select set src/auth/ && chat "Review this code for security issues" --mode plan'
```

## Troubleshooting

**"command not found: rp-cli"**
- Install from Repo Prompt: Settings → MCP Server → "Install CLI to PATH"
- Open new terminal after install

**Connection failures**
- Ensure Repo Prompt is running
- Enable MCP Server in Repo Prompt settings
- Use `--wait-for-server 5` in scripts

**Operations hang**
- Some operations need approval in Repo Prompt UI
- Check for dialog in the app

**Codex CLI sandbox issues**
- Codex sandbox may block socket connection
- Solutions: Use MCP directly, escalate permissions, or run outside Codex

## Integration with Agent Workflows

Use `rp-cli` to leverage Repo Prompt's context building before tackling complex tasks:

```bash
# 1. Build context for a task
rp-cli -e 'builder "Implement user authentication" --response-type plan' > /tmp/plan.md

# 2. Export full context
rp-cli -e 'prompt export > /tmp/full-context.md'

# 3. Use context in your agent workflow
cat /tmp/full-context.md
```

---

*Repo Prompt: https://repoprompt.com*
*Documentation: https://repoprompt.com/docs#s=rp-cli*
