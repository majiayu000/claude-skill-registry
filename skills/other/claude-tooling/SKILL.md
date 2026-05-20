---
name: claude-tooling
description: Discover and list all Claude Code skills, agents, plugins, MCP servers, and hooks available in this project
user-invokable: true
disable-model-invocation: true
---

# claude-tooling

Dynamically discover all Claude Code tooling available in this project and present it as a categorized summary.

## Discovery steps

### 1. Project skills

Read all `SKILL.md` files under `.claude/skills/`. For each, extract the `name` and `description` from the YAML frontmatter. Note whether `disable-model-invocation: true` (user-only) or `user-invokable: false` (Claude-only) or neither (both).

### 2. Project agents

List all `.md` files under `.claude/agents/`. For each, read the first paragraph to get a one-line description.

### 3. Installed plugins

Run:

```bash
claude plugins list
```

List each installed plugin and its description.

### 4. MCP servers

Run:

```bash
claude mcp list
```

List each configured MCP server and how it was added (project vs user scope).

### 5. Hooks

Read `.claude/settings.json` and extract the `hooks` section. Summarize each hook: event type, matcher (if any), and what the command does in plain English.

## Output format

Present the results grouped by category. Use this structure:

```
## Project Skills
| Skill | Description | Invocation |
|-------|-------------|------------|
| /skill-name | description | User / Claude / Both |

## Project Agents
| Agent | Description |
|-------|-------------|
| agent-name | one-line description |

## Installed Plugins
| Plugin | Description |
|--------|-------------|
| plugin-name | description |

## MCP Servers
| Server | Scope |
|--------|-------|
| server-name | project / user |

## Active Hooks
| Event | Trigger | Action |
|-------|---------|--------|
| PreToolUse | Edit, Write | Blocks edits to generated/sensitive files |
```

If a category has no entries, omit it entirely.
