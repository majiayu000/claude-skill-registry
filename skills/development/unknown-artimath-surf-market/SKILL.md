---
name: claude-code-meta
description: Build Claude Code extensions - skills, agents, hooks, plugins, marketplaces, slash commands. Use when creating Claude Code components, building new skills, writing agents, creating hooks, making plugins, setting up marketplaces, writing slash commands, fixing extension configurations, or troubleshooting Claude Code extensions. Includes builder agents for autonomous creation. Not for looking up docs - use claude-code-docs-reference for that.
---

# Claude Code Meta

Create any Claude Code extension component. This skill routes to specific builders based on what you need.

## What Are You Building?

| Component | When to Use | Command |
|-----------|-------------|---------|
| **Skill** | Extend Claude with specialized knowledge, workflows, tool integrations | `/build-skill` |
| **Hook** | Automated validation, context injection, workflow automation | `/build-hook` |
| **Plugin** | Bundle skills/hooks/commands for distribution | `/build-plugin` |
| **Marketplace** | Distribute plugins (local, GitHub, git) | `/build-marketplace` |
| **Slash Command** | User-invoked `/command` prompts | `/build-command` |

## Quick Decision Guide

**"I want to add knowledge/workflows to Claude"** → Skill

**"I want automated task execution"** → Agent (invokes Skills for guidance)

**"I want to validate/inject context automatically"** → Hook

**"I want to bundle and distribute extensions"** → Plugin + Marketplace

**"I want a quick user-typed command"** → Slash Command

## Component Relationships

```
Plugin (distribution package)
├── Skills (knowledge bases)
├── Agents (task executors that use Skills)
├── Hooks (automation triggers)
└── Commands (user-invoked prompts)

Marketplace (distributes Plugins)
```

**Key insight**: Agents are executors, Skills are knowledge. An agent invokes a skill for guidance, then executes.

## Usage

1. Identify what you're building from table above
2. Read the corresponding reference file
3. Follow the patterns and examples there
4. For official Anthropic docs, use `claude-code-docs-reference` skill

## Builder Commands

This plugin includes commands that can create components deterministically:

- `/build-skill` - Creates skills with proper structure and patterns
- `/build-hook` - Creates hooks for automation
- `/build-plugin` - Creates plugins for distribution
- `/build-marketplace` - Creates marketplaces for plugin distribution
- `/build-command` - Creates slash commands

Invoke with: `/command-name [details about what to build]`

## Additional References

- [references/grep-patterns.md](references/grep-patterns.md) - Common grep patterns for docs plugins
- [references/cross-link-syntax.md](references/cross-link-syntax.md) - Cross-linking between skills
- [references/scaling-strategies.md](references/scaling-strategies.md) - When/how to split skills
- [references/templates/](references/templates/) - Starter templates
- [references/skill-examples/README.md](references/skill-examples/README.md) - Exported skill and public artifacts for modeling published flows
