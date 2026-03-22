---
name: plugin-creation
version: 3.0.0
description: Use when creating Claude Code plugins - covers skills, commands, agents, hooks, MCP servers, and plugin configuration. Use when user says "create plugin", "make a skill", "add command", "add hooks", "skill authoring", "SKILL.md", "plugin components", "package reusable behavior", "distribute skills", "scaffold plugin", "plugin structure", "write a skill description". NOT for: using existing plugins, installing plugins, plugin marketplace browsing. !`ls .claude-plugin/ 2>/dev/null`
---

# Plugin Creation

Create complete Claude Code plugins with any combination of components.

## When to Use

- "Create a plugin" / "Make a new plugin"
- "Add a skill" / "Create command" / "Make agent"
- "Add hooks" / "Setup MCP server"
- "Configure settings" / "Setup output directory"
- "Package for marketplace"
- NOT for: Using existing plugins (see /plugin command)

## Quick Reference

| Component | Location | Invocation | Best For |
|-----------|----------|------------|----------|
| Skills | `skills/name/SKILL.md` | Model-invoked (auto) | Complex workflows with resources |
| Commands | `commands/name.md` | User (`/command`) | Quick, frequently used prompts |
| Agents | `agents/name.md` | Auto + Manual | Task-specific expertise |
| Hooks | `hooks/hooks.json` | Event-triggered | Automation and validation |
| MCP | `.mcp.json` | Auto startup | External tool integration |

## Before Creating

1. Read `references/01-overview/component-comparison.md` to decide which components needed
2. Determine if this should be a new plugin or add to existing

## Plugin Project Setup

When creating any plugin, also consider:
- `.claude/rules/` with modular project rules (path-scoped if needed for different component directories)
- `CLAUDE.md` at plugin root for project conventions
- README.md and CHANGELOG.md at plugin root (for humans — never inside skill directories)

## Documentation Principles

All plugin documentation should follow lean principles:
- **Current truth only** — no historical narratives or "previously we did X"
- **Replace, don't append** — superseded content gets replaced entirely
- **Delete what's irrelevant** — every edit is a chance to prune
- Read `references/02-philosophy/core-philosophy.md` for full philosophy

## Plugin Initialization

When user says "create plugin", "initialize plugin", "new plugin":

**Option A - Use init script**:
```bash
python scripts/init_plugin.py my-plugin --path ./plugins --components skill,command,hook
```

**Option B - Manual creation**:

1. Create plugin directory structure:
   ```
   plugin-name/
   ├── .claude-plugin/
   │   └── plugin.json
   ├── commands/        # if needed
   ├── agents/          # if needed
   ├── skills/          # if needed
   │   └── skill-name/
   │       └── SKILL.md
   ├── hooks/           # if needed
   │   └── hooks.json
   └── .mcp.json        # if needed
   ```

2. Copy template from `templates/plugin.json.template`

3. Ask user which components they need

## Creating Skills

When user says "add skill", "create skill", "make skill":

1. Read `references/03-skills/writing-skillmd.md` for structure
2. Copy template from `templates/skill/SKILL.md.template`
3. Key requirements:
   - Name: lowercase, hyphens, max 64 chars
   - Description: WHAT it does + WHEN to use it, max 1024 chars, third person
   - Body: imperative instructions, under 500 lines
   - Use progressive disclosure - reference files for details

**Critical**: SKILL.md files are INSTRUCTIONS for Claude, not documentation. Write imperatives telling Claude what to do.

| Documentation (WRONG) | Instructions (CORRECT) |
|----------------------|------------------------|
| "This skill helps with PDF processing" | "Process PDF files using this workflow" |
| "The description field is important" | "Write the description starting with 'Use when...'" |

**Consider these optional frontmatter fields:**
- `model: haiku` for simple lookup/formatting skills, `opus` for complex reasoning
- `context: fork` with `agent: <type>` for heavy operations that would pollute main context
- `disable-model-invocation: true` for command-only skills (no auto-trigger)
- `user-invocable: false` to hide from `/` menu (Claude can still invoke via Skill tool)

**Dynamic context injection**: Use `` !`command` `` in the skill body to inject runtime state (git status, file contents, etc.) when the skill loads.

**Extended thinking**: Include "ultrathink" in the skill body for tasks requiring deep reasoning.

## Creating Commands

When user says "add command", "create command", "slash command":

1. Read `references/04-commands/writing-commands.md`
2. Copy template from `templates/command/command.md.template`
3. Key requirements:
   - Frontmatter: description, allowed-tools, argument-hint
   - Support `$ARGUMENTS`, `$1`, `$2` for arguments
   - Prefix lines with exclamation mark for bash execution
   - Prefix lines with at-sign for file references

## Creating Agents

When user says "add agent", "create agent", "make agent":

1. Read `references/05-agents/writing-agents.md`
2. Copy template from `templates/agent/agent.md.template`
3. Key requirements:
   - Frontmatter: name, description, tools, model, permissionMode
   - Description should include "Use proactively" for auto-delegation
   - One agent = one clear responsibility

**Consider these agent-specific features:**
- `memory: project` for agents that benefit from cross-session learning (architecture decisions, code review patterns)
- `memory: user` for personal preferences that carry across projects
- `model:` matched to task complexity — `haiku` for lookup/formatting, `sonnet` for balanced tasks, `opus` for complex reasoning
- `tools` restriction to minimum needed (reduces cost and attack surface)
- `disallowedTools` to block specific tools (e.g., `Edit`, `Write` for read-only agents)
- `hooks` in agent frontmatter for scoped validation (runs only when that agent is active)

**Agent teams**: For tasks benefiting from multiple perspectives or parallel research, consider agent teams (competing perspectives, hypothesis investigation, parallel tasks). See `references/05-agents/agent-patterns.md` for team patterns. Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.

## Creating Hooks

When user says "add hooks", "setup hooks", "event handlers":

1. Read `references/06-hooks/writing-hooks.md`
2. Read `references/06-hooks/hook-events.md` for all 18 events
3. Copy template from `templates/hooks/hooks.json.template`
4. Key events:
   - `PreToolUse` - before tool execution (can block)
   - `PostToolUse` - after tool execution (formatting, logging)
   - `SessionStart` - setup, output directories
   - `SessionEnd` - cleanup
   - `UserPromptSubmit` - validation, context injection (can block)
   - `SubagentStart`/`SubagentStop` - agent lifecycle
   - `PreCompact` - inject context before compaction
   - `Notification`, `Stop`, `TaskCompleted`, `TeammateIdle`

**Three handler types** — choose the right one:
- `command` — shell script, fastest, no LLM cost. Use for logging, file ops, env setup.
- `prompt` — single-turn LLM evaluation, zero script overhead. Use for lightweight validation.
- `agent` — multi-turn subagent with tools (Read, Grep, Glob). Use for complex verification.

**Async execution**: Add `"async": true` on command hooks for background operations (logging, analytics) that shouldn't block the main flow.

**MCP tool matching**: Use `mcp__<server>__<tool>` pattern in matchers for PreToolUse/PostToolUse.

## Configuring Plugin

When user says "configure plugin", "setup plugin.json":

1. Read `references/08-configuration/plugin-json.md` for full schema
2. Required fields: `name`
3. Recommended fields: `version`, `description`, `author`, `license`
4. Component paths: `commands`, `agents`, `hooks`, `mcpServers`

## Settings and Output

When user says "configure settings", "setup output", "output directory":

1. Read `references/08-configuration/settings.md` for settings hierarchy
2. Read `references/08-configuration/output-config.md` for output patterns
3. Key environment variables:
   - `${CLAUDE_PLUGIN_ROOT}` - plugin installation directory
   - `${CLAUDE_PROJECT_DIR}` - project root
   - `${CLAUDE_ENV_FILE}` - persistent env vars (SessionStart only)
4. Use SessionStart hook to create output directories

## Testing Plugin

When user says "test plugin", "validate plugin":

1. Read `references/09-testing/testing.md`
2. Run `claude --debug` to see plugin loading
3. Validate plugin.json syntax
4. Test each component:
   - Skills: Ask questions matching description
   - Commands: Run `/command-name`
   - Agents: Check `/agents` listing
   - Hooks: Trigger events manually

## Packaging for Marketplace

When user says "package plugin", "publish plugin", "marketplace":

1. Read `references/10-distribution/packaging.md`
2. Create `marketplace.json` in repository root
3. Update README with installation instructions
4. Version using semantic versioning (MAJOR.MINOR.PATCH)

## Decision Framework

Before creating a component, verify it's the right choice:

| Component | Use When |
|-----------|----------|
| Skill | Complex workflow, needs resources, auto-triggered by context |
| Command | User should trigger explicitly, quick one-off prompts |
| Agent | Specialized expertise, own context window, proactive delegation |
| Hook | Event-based automation, validation, logging |
| MCP | External API/service, custom tools, database access |

**The 5-10 Rule**: Done 5+ times? Will do 10+ more? Create a skill or command.

## References

### Overview
- `references/01-overview/what-are-plugins.md` - Plugin overview
- `references/01-overview/what-are-skills.md` - Skills overview
- `references/01-overview/what-are-commands.md` - Commands overview
- `references/01-overview/what-are-agents.md` - Agents overview
- `references/01-overview/what-are-hooks.md` - Hooks overview
- `references/01-overview/what-are-mcp.md` - MCP overview
- `references/01-overview/component-comparison.md` - When to use what

### Philosophy
- `references/02-philosophy/core-philosophy.md` - Design principles
- `references/02-philosophy/decision-frameworks.md` - Decision trees
- `references/02-philosophy/anti-patterns.md` - What to avoid

### Components
- `references/03-skills/anthropic-skill-standards.md` - Official Anthropic skill standards and checklist
- `references/03-skills/skill-patterns.md` - Five skill patterns (Sequential, Multi-MCP, Iterative, Context-Aware, Domain-Specific)
- `references/03-skills/` - Skill creation guides
- `references/04-commands/` - Command creation guides
- `references/05-agents/` - Agent creation guides
- `references/06-hooks/` - Hook creation guides
- `references/06-hooks/cross-platform-hooks.md` - Windows/macOS/Linux support
- `references/07-mcp/` - MCP overview

### Configuration
- `references/08-configuration/plugin-json.md` - Plugin manifest
- `references/08-configuration/marketplace-json.md` - Marketplace config
- `references/08-configuration/settings.md` - Settings hierarchy
- `references/08-configuration/output-config.md` - Output configuration

### Testing & Distribution
- `references/09-testing/testing.md` - Testing guide (all components)
- `references/09-testing/debugging.md` - Debugging guide
- `references/09-testing/cli-reference.md` - CLI commands reference
- `references/10-distribution/packaging.md` - Packaging guide
- `references/10-distribution/marketplace.md` - Marketplace guide
- `references/10-distribution/versioning.md` - Version strategy
- `references/10-distribution/complete-examples.md` - Full plugin examples

## Examples

Working example plugins in `examples/`:
- `examples/simple-greeter-plugin/` - Minimal plugin with one skill
- `examples/full-featured-plugin/` - Complete plugin with skill, commands, hooks

## Templates

All templates are in the `templates/` directory:
- `templates/skill/SKILL.md.template`
- `templates/command/command.md.template`
- `templates/agent/agent.md.template`
- `templates/hooks/hooks.json.template`
- `templates/hooks/run-hook.cmd.template` - Cross-platform hook wrapper
- `templates/plugin.json.template`
- `templates/marketplace.json.template`
- `templates/settings.json.template`
- `templates/mcp.json.template`

## Scripts

- `scripts/init_plugin.py` - Initialize new plugin with selected components
- `scripts/init_skill.py` - Initialize standalone skill
- `scripts/validate_skill.py` - Validate skill structure
- `scripts/package_skill.py` - Package skill for distribution
