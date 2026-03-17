---
name: ecosystem-guide
description: Guide to spences10's Claude Code ecosystem. Use when user asks which tool to use, how tools relate, or needs help choosing between MCP servers, skills, or CLIs.
---

# Claude Code Ecosystem Guide

A curated set of tools for enhanced Claude Code workflows.

## The Stack

| Tool                  | Type   | Purpose                                                      |
| --------------------- | ------ | ------------------------------------------------------------ |
| **toolkit-skills**    | Plugin | Forced-eval hook + core skills (pair with any skills plugin) |
| **svelte-skills-kit** | Plugin | Svelte/SvelteKit skills (pair with toolkit-skills)           |
| **ccrecall**          | CLI    | Sync transcripts → SQLite for analytics                      |
| **mcp-omnisearch**    | MCP    | Unified search (Tavily, Kagi, GitHub, etc.)                  |
| **mcp-sqlite-tools**  | MCP    | Safe SQLite operations                                       |
| **mcpick**            | CLI    | Toggle MCP servers dynamically                               |
| **research**          | Skill  | Verified source research patterns                            |
| **skill-creator**     | Skill  | Create Claude skills with best practices                     |

## Decision Tree

### "I want skills to activate reliably"

→ **toolkit-skills** - Forced-eval hook evaluates every prompt against available skills. Install alongside any skills plugin.

```bash
claude plugin install toolkit-skills@claude-code-toolkit
```

### "I need to search the web"

→ **mcp-omnisearch** - Web search, GitHub code search, AI answers

### "I need to query a database"

→ **mcp-sqlite-tools** - Read/write SQLite with safety guards

### "I have too many MCPs eating context"

→ **mcpick** - Enable/disable servers per-project

### "I want to track my Claude Code usage"

→ **ccrecall** - Sync transcripts, query with mcp-sqlite-tools

### "I'm building with Svelte/SvelteKit"

→ **svelte-skills-kit** - Runes, routing, data flow patterns (you're here!)

### "I need to research a topic or verify sources"

→ **research skill** - Verified source research, repo cloning patterns

### "I want to create a new Claude skill"

→ **skill-creator skill** - Progressive disclosure, writing guide, CLI reference

## Recommended Setup

```bash
# Core: forced-eval hook + ecosystem skills
claude plugin install toolkit-skills@claude-code-toolkit

# Svelte/SvelteKit skills
claude plugin install svelte-skills@svelte-skills-kit
```

toolkit-skills hook ensures skills from any plugin activate on relevant prompts.

## Links

| Tool                | GitHub                                           |
| ------------------- | ------------------------------------------------ |
| claude-code-toolkit | https://github.com/spences10/claude-code-toolkit |
| svelte-skills-kit   | https://github.com/spences10/svelte-skills-kit   |
| ccrecall            | https://github.com/spences10/ccrecall            |
| mcp-omnisearch      | https://github.com/spences10/mcp-omnisearch      |
| mcp-sqlite-tools    | https://github.com/spences10/mcp-sqlite-tools    |
| mcpick              | https://github.com/spences10/mcpick              |
