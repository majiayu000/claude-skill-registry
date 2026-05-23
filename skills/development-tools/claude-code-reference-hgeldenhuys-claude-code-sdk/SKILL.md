---
name: claude-code-reference
description: Reference guide for Claude Code extensions. CONSULT BEFORE implementing skills, creating hooks, slash commands, or MCP servers. Use when building Claude Code extensions, understanding extension differences, or troubleshooting extension issues. Covers skills vs commands vs hooks vs MCP disambiguation.
allowed-tools: ["Read"]
---

# Claude Code Extension Reference

Authoritative reference for Claude Code extension types. Consult this before implementing any extension.

## Quick Disambiguation

| Extension Type | Trigger | Purpose | Complexity |
|----------------|---------|---------|------------|
| **Skills** | Automatic (Claude decides) | Add specialized knowledge/workflows | Directory + SKILL.md |
| **Slash Commands** | Manual (`/command`) | Quick reusable prompts | Single .md file |
| **Hooks** | Event-driven (tool use, session) | Automated scripts on events | JSON config + scripts |
| **MCP Servers** | Tool calls (Claude decides) | Connect to external tools/data | Server implementation |

## When to Use Each

### Use Skills When

- Claude should discover and apply knowledge automatically
- You need multiple reference files, scripts, or templates
- Building team workflows requiring standardized guidance
- Creating capabilities that span multiple steps

**NOT for**: Simple prompts, one-off commands, external integrations

### Use Slash Commands When

- You invoke the same prompt repeatedly
- The prompt fits in a single markdown file
- You want explicit control over when it runs
- Quick templates or reminders

**NOT for**: Complex multi-file workflows, automatic discovery

### Use Hooks When

- You need scripts to run on specific events (tool use, session start/end)
- Automating linting, formatting, or validation after file changes
- Adding context before prompts are processed
- Controlling whether Claude can stop or continue

**NOT for**: Adding knowledge, user-invoked actions

### Use MCP Servers When

- Connecting Claude to external tools, databases, or APIs
- Providing new tool capabilities (not just knowledge)
- Building integrations that require authentication
- Exposing resources from external systems

**NOT for**: Adding knowledge about how to use tools (use Skills for that)

## Key Differences

### Skills vs Slash Commands

| Aspect | Skills | Slash Commands |
|--------|--------|----------------|
| Discovery | Automatic (Claude matches description) | Manual (`/command`) |
| Structure | Directory with SKILL.md + resources | Single .md file |
| Complexity | Multi-file, scripts, templates | Simple prompts |
| Scope | Project or personal | Project or personal |

### Skills vs MCP

- **Skills tell Claude HOW** to use tools (knowledge, patterns, workflows)
- **MCP PROVIDES the tools** (actual capabilities, external connections)

Example: MCP server connects Claude to your database. A Skill teaches Claude your data model and query patterns.

### Hooks vs Skills

- **Hooks run scripts** on events (automated, no Claude involvement in execution)
- **Skills add knowledge** to conversations (Claude uses the guidance)

## Reference Files

For detailed implementation guidance, consult these reference files:

| File | Contents |
|------|----------|
| [CONCEPTS.md](./CONCEPTS.md) | Core concepts and architecture |
| [HEADLESS.md](./HEADLESS.md) | Headless mode and SDK usage |
| [SUBAGENTS.md](./SUBAGENTS.md) | Sub-agent implementation |
| [WHATS-NEW.md](./WHATS-NEW.md) | Recent changes and new features |

## Skills Quick Reference

### Required Structure

```
skill-name/
  SKILL.md           # Required (under 500 lines)
  reference.md       # Optional detailed docs
  examples.md        # Optional examples
  scripts/           # Optional utility scripts
```

### YAML Frontmatter

```yaml
---
name: skill-name
description: What it does and when to use it. Include trigger phrases.
allowed-tools: ["Read", "Grep", "Glob"]  # Optional: restricts tools
model: sonnet  # Optional: force specific model
---
```

### Location Hierarchy (higher overrides lower)

1. Enterprise: Managed settings
2. Personal: `~/.claude/skills/`
3. Project: `.claude/skills/`
4. Plugin: Bundled with plugins

### Naming Rules

- Lowercase letters, numbers, hyphens only
- Maximum 64 characters
- Use gerund form (`writing-skills` not `skill-writer`)

## Slash Commands Quick Reference

### Required Structure

```
.claude/commands/command-name.md  # Project command
~/.claude/commands/command-name.md  # Personal command
```

### Frontmatter Options

```yaml
---
allowed-tools: Bash(git:*), Read, Write
argument-hint: [arg1] [arg2]
description: Brief description
model: claude-3-5-haiku-20241022
disable-model-invocation: false
---
```

### Features

- `$ARGUMENTS` - All arguments passed
- `$1`, `$2`, etc. - Positional arguments
- `!`git status`` - Execute bash before command
- `@file.ts` - Reference files

### Namespacing

- `.claude/commands/frontend/test.md` creates `/test` (shows "project:frontend")
- Project commands override personal commands with same name

## Hooks Quick Reference

### Configuration Location

```json
// ~/.claude/settings.json (user)
// .claude/settings.json (project)
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your-script.sh"
          }
        ]
      }
    ]
  }
}
```

### Hook Events

| Event | When | Use For |
|-------|------|---------|
| `PreToolUse` | Before tool executes | Validate, modify, or block tool calls |
| `PostToolUse` | After tool completes | Format, lint, log changes |
| `PermissionRequest` | User shown permission dialog | Auto-approve or deny |
| `UserPromptSubmit` | User submits prompt | Validate, add context |
| `Stop` | Claude finishes responding | Check if work is complete |
| `SubagentStop` | Subagent finishes | Check subagent completion |
| `SessionStart` | Session begins | Load context, set env vars |
| `SessionEnd` | Session ends | Cleanup, logging |
| `Notification` | Notifications sent | Custom notification handling |
| `PreCompact` | Before compaction | Preserve important context |

### Matcher Patterns

- Exact: `Write` matches only Write tool
- Regex: `Edit|Write` matches either
- `*` or empty: matches all tools

### Exit Codes

- `0`: Success (stdout shown in verbose mode)
- `2`: Blocking error (stderr fed to Claude)
- Other: Non-blocking error

## MCP Quick Reference

### Adding Servers

```bash
# Remote HTTP (recommended)
claude mcp add --transport http name https://url

# Remote SSE (deprecated)
claude mcp add --transport sse name https://url

# Local stdio
claude mcp add --transport stdio name -- npx -y package
```

### Scopes

- `local` (default): Your project only
- `project`: Shared via `.mcp.json`
- `user`: All your projects

### Management Commands

```bash
claude mcp list              # List servers
claude mcp get <name>        # Get details
claude mcp remove <name>     # Remove server
/mcp                         # In Claude Code: status and auth
```

### MCP Tool Naming

Tools follow pattern: `mcp__<server>__<tool>`

Example: `mcp__github__search_repositories`

## Common Misconceptions

### Misconception: Skills are like slash commands

**Reality**: Skills are automatically discovered based on description matching. Slash commands require explicit `/command` invocation.

### Misconception: Hooks add knowledge to Claude

**Reality**: Hooks run scripts on events. They can inject context (via stdout for UserPromptSubmit/SessionStart) but don't teach Claude new concepts.

### Misconception: MCP servers teach Claude how to use tools

**Reality**: MCP servers provide tools. Skills teach Claude how and when to use those tools effectively.

### Misconception: I need MCP for external APIs

**Reality**: Claude has built-in WebFetch and WebSearch. Use MCP when you need authenticated access, complex tool logic, or custom data sources.

### Misconception: Skills execute code

**Reality**: Skills provide knowledge. They can bundle scripts that Claude executes using Bash, but the skill itself doesn't run code.

## Troubleshooting

### Skill Not Triggering

1. Check description includes trigger phrases users would say
2. Verify SKILL.md path: `~/.claude/skills/name/SKILL.md` or `.claude/skills/name/SKILL.md`
3. Restart Claude Code after changes
4. Run `claude --debug` to see loading errors

### Hook Not Running

1. Check JSON syntax in settings file
2. Verify matcher pattern matches tool name (case-sensitive)
3. Check script is executable: `chmod +x script.sh`
4. Use full paths with `$CLAUDE_PROJECT_DIR`

### MCP Server Not Connecting

1. Check server status: `/mcp`
2. Verify URL or command is correct
3. For OAuth servers, authenticate via `/mcp`
4. Check timeout: `MCP_TIMEOUT=10000 claude`

### Slash Command Not Appearing

1. Verify file location: `.claude/commands/name.md`
2. Check YAML frontmatter syntax
3. Ensure description frontmatter is set (required for SlashCommand tool)
4. Restart Claude Code

## Extension Decision Flowchart

```
Need to extend Claude Code?
            |
            v
    Is it knowledge/guidance?
        |           |
       YES         NO
        |           |
        v           v
   Single file?   External tool/data?
     |    |        |           |
    YES   NO      YES         NO
     |    |        |           |
     v    v        v           v
 Command  Skill   MCP      Event-driven?
                               |    |
                              YES   NO
                               |    |
                               v    v
                             Hook  Reconsider need
```

## Plugin Marketplaces

Distribute plugins (skills, hooks, commands, agents, MCP servers) via marketplaces:

### Creating a Marketplace

```json
// .claude-plugin/marketplace.json
{
  "name": "my-marketplace",
  "owner": { "name": "Your Name" },
  "plugins": [
    {
      "name": "my-skill",
      "source": "./plugins/my-skill",
      "description": "What it does"
    }
  ]
}
```

### Plugin Sources

| Type | Source Format |
|------|---------------|
| Relative path | `"./plugins/name"` |
| GitHub | `{"source": "github", "repo": "owner/repo"}` |
| Git URL | `{"source": "url", "url": "https://..."}` |

### Installing from Marketplaces

```bash
# Add a marketplace
/plugin marketplace add owner/repo

# Install a plugin
/plugin install plugin-name@marketplace-name

# Update marketplace
/plugin marketplace update
```

### Team Configuration

```json
// .claude/settings.json
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {"source": "github", "repo": "your-org/plugins"}
    }
  }
}
```

See: https://code.claude.com/docs/en/plugin-marketplaces

## Deep-Dive Skills

For detailed implementation guidance, install these companion skills:

| Skill | Purpose | Install |
|-------|---------|---------|
| `creating-hooks` | All 10 hook events with examples | `cp -r skills/creating-hooks ~/.claude/skills/` |
| `creating-mcp-servers` | MCP server creation and integration | `cp -r skills/creating-mcp-servers ~/.claude/skills/` |
| `transcript-intelligence` | Search past sessions | `cp -r skills/transcript-intelligence ~/.claude/skills/` |
| `writing-skills` | Best practices for skill creation | `cp -r skills/writing-skills ~/.claude/skills/` |

**From npm package:**
```bash
# If installed via: bun add claude-code-sdk
ln -s node_modules/claude-code-sdk/skills/creating-hooks ~/.claude/skills/
ln -s node_modules/claude-code-sdk/skills/creating-mcp-servers ~/.claude/skills/
ln -s node_modules/claude-code-sdk/skills/transcript-intelligence ~/.claude/skills/
ln -s node_modules/claude-code-sdk/skills/writing-skills ~/.claude/skills/
```

**From GitHub:**
```bash
git clone https://github.com/hgeldenhuys/claude-code-sdk /tmp/sdk
cp -r /tmp/sdk/skills/* ~/.claude/skills/
```

## Version Information

This reference is based on Claude Code documentation as of January 2025. For the latest information:

- Skills: https://code.claude.com/docs/en/skills
- Slash Commands: https://code.claude.com/docs/en/slash-commands
- Hooks: https://code.claude.com/docs/en/hooks
- MCP: https://code.claude.com/docs/en/mcp
- Plugin Marketplaces: https://code.claude.com/docs/en/plugin-marketplaces
