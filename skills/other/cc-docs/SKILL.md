---
name: cc-docs
description: Read Claude Code documentation to learn about features, capabilities, hooks, skills, MCP, subagents, and how to use Claude Code effectively.
---

# Claude Code Documentation

When invoked, read the Claude Code documentation to answer questions or learn about capabilities.

## Documentation Location

Main index: `~/.claude/docs/claude-code-ai-docs.md`
Full docs: `~/.claude/docs/claude-code/`

## How to Use

1. First read `~/.claude/docs/claude-code-ai-docs.md` for overview and structure
2. Then read specific docs based on the question:
   - Skills: `~/.claude/docs/claude-code/build/skills.md`
   - Hooks: `~/.claude/docs/claude-code/build/hooks-guide.md`, `~/.claude/docs/claude-code/reference/hooks.md`
   - Subagents: `~/.claude/docs/claude-code/build/sub-agents.md`
   - MCP: `~/.claude/docs/claude-code/build/mcp.md`
   - Plugins: `~/.claude/docs/claude-code/build/plugins.md`, `~/.claude/docs/claude-code/reference/plugins-reference.md`
   - Slash commands: `~/.claude/docs/claude-code/reference/slash-commands.md`
   - Settings: `~/.claude/docs/claude-code/configuration/settings.md`

## When to Use

- User asks "how do I..." about Claude Code features
- User wants to create skills, hooks, subagents, or plugins
- User asks about Claude Code capabilities
- User needs help with MCP configuration

## Updating Docs

To refresh documentation from the official source:
```bash
cd ~/.claude/docs && python3 ../scripts/scrape_claude_code_docs.py
```

Or reinstall from the toru-claude-agents repo.
