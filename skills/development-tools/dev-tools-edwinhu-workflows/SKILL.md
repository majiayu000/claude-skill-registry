---
name: dev-tools
description: "This skill should be used when the user asks 'what development tools are available', 'list dev plugins', 'what MCP servers can I use', 'enable code intelligence', 'what testing tools exist', or needs to discover development plugins like serena, playwright, or context7. Use this for general development tool discovery; use ds-tools for data science-specific tools."
user-invocable: false
---

# Available Development Tools

Plugins and skills for development workflows. For data science tools (WRDS, LSEG, notebooks), see `/ds-tools`.

## Code Intelligence Plugins

| Plugin | Description | Enable Command |
|--------|-------------|----------------|
| `serena` | Semantic code analysis, refactoring, symbol navigation | `claude --enable-plugin serena@claude-plugins-official` |
| `pyright-lsp` | Python type checking and diagnostics | `claude --enable-plugin pyright-lsp@claude-plugins-official` |
| `context7` | Up-to-date library/framework docs lookup | `claude --enable-plugin context7@claude-plugins-official` |

## Testing & Automation Plugins

| Plugin | Description | Enable Command |
|--------|-------------|----------------|
| `playwright` | Browser automation, E2E testing, screenshots | `claude --enable-plugin playwright@claude-plugins-official` |

## Workflow Plugins (Already Enabled)

| Plugin | Description |
|--------|-------------|
| `ralph-loop` | Self-referential iteration loops |

## When to Enable

- **serena**: Complex refactoring, finding symbol references, understanding large codebases
- **context7**: Need current docs for React, FastAPI, Next.js, etc.
- **playwright**: Testing web UIs, scraping, taking screenshots
- **pyright-lsp**: Python projects needing strict type checking

## Usage

```bash
claude --enable-plugin <plugin-name>  # Enable for current session
```
