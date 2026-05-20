---
name: claude-oracle
description: Automatic tool discovery across 17 sources — hooks search before planning and after errors, siblings avoid redundant searches
triggers: [PreToolUse, PostToolUse]
---

# Oracle Plugin

Tool discovery. Searches 17 sources in parallel to find relevant skills, plugins, and MCP servers.

## Hooks

| Hook | When | Action |
|------|------|--------|
| **PreToolUse(EnterPlanMode)** | Before planning | Searches for relevant tools before planning |
| **PostToolUse(Bash)** | After errors | Searches for tools that solve the error |

## Commands

| Command | Description |
|---------|-------------|
| `/search-oracle <query> [type]` | Search for tools across all 17 sources |

## Workflows

### Discovery (standalone)

1. `search("query")` — search all sources
2. Review results with install commands
3. Install useful tools: skills, plugins, or MCP servers

### Discovery (with siblings)

1. If **historian** active: `find_similar_queries("query")` first to check if this search was done before
2. `search("query")` — oracle's own search across 17 sources
3. If **praetorian** active: compact the discovery results for future reference
4. Present findings with install commands and note what siblings already provide

### Error Tool Search (standalone)

1. Error triggers PostToolUse hook
2. `search("error description")` — find tools that address this error class
3. Present matching tools with install commands

### Error Tool Search (with siblings)

1. Error triggers PostToolUse hook
2. If **historian** active: `get_error_solutions("error")` checks if solved before
3. `search("error description")` — oracle finds new tools
4. If **gladiator** active: error is also being observed for pattern detection
5. Combined: past solution (historian) + new tools (oracle) + pattern tracking (gladiator)

## Sibling Synergy

| Sibling | Value | How |
|---------|-------|-----|
| **Historian** | Past searches avoid duplicate discovery | Historian checked first, oracle only runs if no history match |
| **Praetorian** | Cached compactions contain prior tool results | Restore before re-searching |
| **Gladiator** | Observations reveal tool gaps | Reflection may suggest searching for tools to fill gaps |

## Data Sources (17)

Smithery Registry, Glama.ai, Official MCP Registry, npm, GitHub marketplace plugins, awesome-mcp-servers, awesome-mcp-lists, awesome-claude-code (ccplugins), awesome-claude-code (jmanhype), awesome-agent-skills, Playbooks.com, SkillsMP, and more.

## Requires

```
claude mcp add oracle -- npx claude-oracle-mcp
```
