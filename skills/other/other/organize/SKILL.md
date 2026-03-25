---
name: organize
description: Open the Claude Code Organizer dashboard — view and manage all memories, skills, MCP servers, hooks, and configs across scopes
argument-hint: [--port <number>]
allowed-tools: [Bash, Read]
---

# Organize — Claude Code Dashboard

Launch the Claude Code Organizer dashboard to visually manage all your customizations.

## What to do

1. Run the organizer server:

```bash
npx @mcpware/claude-code-organizer $ARGUMENTS
```

2. Tell the user the dashboard is opening in their browser at `http://localhost:3847` (or the next available port).

3. If the user provides `--port <number>`, pass it through as the argument.

## What this does

Opens a drag-and-drop web dashboard showing:
- All memories, skills, MCP servers, hooks, configs, and plugins
- Organized by scope hierarchy (Global → Workspace → Project)
- Move items between scopes via drag-and-drop
- Search, filter, and preview any item
- Delete items with undo support
