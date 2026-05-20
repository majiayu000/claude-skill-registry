---
name: mcp-skills
description: Registry of MCP-derived skills with progressive disclosure. Use when asked about "github", "assistant-ui", "chrome-devtools", "playwright", "shadcn", "undetected-chromedriver", "logfire", "magicui", "livekit", "ToolUI", "generative UI", "chat components", "PR", "issues", "repository", "browser automation", "E2E testing", "screenshot", "console logs", "network requests", "performance tracing", "stealth browser", "bot detection bypass", "web scraping", "observability", "tracing", "exceptions", "Magic UI", "bento-grid", "animations", "voice agents", "real-time audio", "WebRTC", "UI components", "MCP tools", or any converted MCP server. Provides 90%+ context savings compared to native MCP loading.
version: 1.0.0
title: "Mcp Skills"
status: active
---

# MCP Skills Registry

Central directory for all MCP-derived skills. Each sub-skill wraps an MCP server with progressive disclosure.

## Available Skills

| Skill | Tools | Trigger Keywords |
|-------|-------|------------------|
| assistant-ui | 2 | ToolUI, generative UI, chat components, assistant-ui docs |
| chrome-devtools | 26 | browser automation, E2E testing, screenshot, console, network, performance, Core Web Vitals |
| github | 26 | PR, issues, repository, commits, code search |
| livekit-docs | 7 | LiveKit, voice agents, real-time audio, WebRTC, agents SDK, rooms, tracks, Python agents |
| logfire | 4 | Pydantic Logfire, observability, tracing, exceptions, spans, logs, SQL queries |
| magicui | 8 | Magic UI, React components, animations, bento-grid, marquee, shimmer, particles |
| mcp-undetected-chromedriver | 16 | stealth browser, bot detection bypass, web scraping, anti-detection, PDF export |
| playwright | 22 | Playwright, browser testing, automation, clicks, forms, screenshots, navigation, tabs |
| shadcn | 7 | shadcn/ui, UI components, React components, Tailwind, component registry, examples, button, card, dialog, form, table, accordion, toast |

See `index.json` for the full list, or browse sub-directories.

## ⚠️ These Are Skill Wrappers, NOT Native MCP Tools

You CANNOT call `mcp__shadcn__*`, `mcp__github__*`, etc. directly - those don't exist.
These skills wrap MCP servers via a central executor.py.

## Usage

**Step 1: Read the skill's SKILL.md** (from project root):

```bash
cat .claude/skills/mcp-skills/<skill-name>/SKILL.md

# Example: shadcn skill
cat .claude/skills/mcp-skills/shadcn/SKILL.md
```

**Step 2: Use the central executor.py** (from project root):

```bash
# List available skills
python .claude/skills/mcp-skills/executor.py --skills

# List tools in a skill
python .claude/skills/mcp-skills/executor.py --skill github --list

# Get tool schema
python .claude/skills/mcp-skills/executor.py --skill github --describe create_issue

# Call a tool
python .claude/skills/mcp-skills/executor.py --skill github --call '{"tool": "create_issue", "arguments": {...}}'
```

## Context Efficiency

| Scenario | Native MCP (all servers) | This Registry | Savings |
|----------|--------------------------|---------------|---------|
| Idle | 40-100k tokens | ~150 tokens | 99%+ |
| Using 1 skill | 40-100k tokens | ~5k tokens | 90%+ |
| After execution | 40-100k tokens | ~150 tokens | 99%+ |

## How It Works

1. **Registry loads first** - This file (~150 tokens)
2. **User requests a tool** - e.g., "create a GitHub PR"
3. **Sub-skill loads** - Only the relevant skill's SKILL.md (~4k tokens)
4. **Executor runs** - External process, 0 context tokens
5. **Result returned** - Context drops back to registry only

## Adding New Skills

Use the `mcp-to-skill-converter` skill:

```bash
cd .claude/skills/mcp-to-skill-converter
python mcp_to_skill.py --name <server-name>
# Outputs to .claude/skills/mcp-skills/<server-name>/
```

## Skill Structure

The registry has a central executor with per-skill configs:

```
.claude/skills/mcp-skills/
├── executor.py              # Central executor for ALL skills
├── SKILL.md                 # This registry file
├── index.json               # Skill metadata registry
└── <skill-name>/
    ├── SKILL.md             # Tool documentation
    ├── mcp-config.json      # Server config
    └── package.json         # Dependencies
```

---

*This registry enables progressive disclosure of MCP servers as Claude Skills.*
