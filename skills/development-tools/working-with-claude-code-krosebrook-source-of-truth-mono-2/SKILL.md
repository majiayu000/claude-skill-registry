---
name: working-with-claude-code
description: Use when working with Claude Code CLI, plugins, hooks, MCP servers, skills, configuration, or any Claude Code feature - provides comprehensive official documentation for all aspects of Claude Code
---

# Working with Claude Code

## Overview

This skill provides complete, authoritative documentation for Claude Code directly from docs.claude.com. Instead of guessing about configuration paths, API structures, or feature capabilities, read the official docs stored in this skill's references directory.

## When to Use

Use this skill when:
- Creating or configuring Claude Code plugins
- Setting up MCP servers
- Working with hooks (pre-commit, session-start, etc.)
- Writing or testing skills
- Configuring Claude Code settings
- Troubleshooting Claude Code issues
- Understanding CLI commands
- Setting up integrations (VS Code, JetBrains, etc.)
- Configuring networking, security, or enterprise features

## Quick Reference

| Task | Read This File |
|------|---------------|
| Create a plugin | `plugins.md` then `plugins-reference.md` |
| Set up MCP server | `mcp.md` |
| Configure hooks | `hooks.md` then `hooks-guide.md` |
| Write a skill | `skills.md` |
| CLI commands | `cli-reference.md` |
| Troubleshoot issues | `troubleshooting.md` |
| General setup | `setup.md` or `quickstart.md` |
| Configuration options | `settings.md` |

## Documentation Organization

All documentation is stored as individual markdown files in `references/`. Use the Read tool to access specific documentation:

```
references/
├── overview.md              # Claude Code introduction
├── quickstart.md           # Getting started guide
├── setup.md                # Installation and setup
├── plugins.md              # Plugin development
├── plugins-reference.md    # Plugin API reference
├── plugin-marketplaces.md  # Plugin marketplaces
├── skills.md               # Skill creation
├── mcp.md                  # MCP server integration
├── hooks.md                # Hooks overview
├── hooks-guide.md          # Hooks implementation guide
├── slash-commands.md       # Slash command reference
├── sub-agents.md           # Subagent usage
├── settings.md             # Configuration reference
├── cli-reference.md        # CLI command reference
├── common-workflows.md     # Common usage patterns
├── interactive-mode.md     # Interactive mode guide
├── headless.md             # Headless mode guide
├── output-styles.md        # Output customization
├── statusline.md           # Status line configuration
├── memory.md               # Memory and context management
├── checkpointing.md        # Checkpointing feature
├── analytics.md            # Usage analytics
├── costs.md                # Cost tracking
├── monitoring-usage.md     # Usage monitoring
├── data-usage.md           # Data usage policies
├── security.md             # Security features
├── iam.md                  # IAM integration
├── network-config.md       # Network configuration
├── terminal-config.md      # Terminal configuration
├── model-config.md         # Model configuration
├── llm-gateway.md          # LLM gateway setup
├── amazon-bedrock.md       # AWS Bedrock integration
├── google-vertex-ai.md     # Google Vertex AI integration
├── vs-code.md              # VS Code integration
├── jetbrains.md            # JetBrains integration
├── devcontainer.md         # Dev container support
├── github-actions.md       # GitHub Actions integration
├── gitlab-ci-cd.md         # GitLab CI/CD integration
├── third-party-integrations.md  # Other integrations
├── legal-and-compliance.md # Legal information
├── troubleshooting.md      # Troubleshooting guide
└── migration-guide.md      # Migration guide
```

## Workflow

### For Specific Questions

1. Identify the relevant documentation file from the list above
2. Use Read tool to load: `@references/filename.md`
3. Find the answer in the official documentation
4. Apply the solution

**Example:**
```
User: "How do I create a Claude Code plugin?"
→ Read @references/plugins.md
→ Follow the official plugin creation steps
```

### For Broad Topics

When exploring a topic, start with the overview document, then drill into specific files:

- **Extending Claude Code**: Start with `plugins.md`, `skills.md`, or `mcp.md`
- **Configuration**: Start with `settings.md` or `setup.md`
- **Integrations**: Check relevant integration file (vs-code.md, github-actions.md, etc.)
- **Troubleshooting**: Start with `troubleshooting.md`

### For Uncertain Topics

Use Grep tool to search across all documentation:

```bash
pattern: "search term"
path: ~/.claude/skills/working-with-claude-code/references/
```

## Updating Documentation

The skill includes `scripts/update_docs.js` to fetch the latest documentation from docs.claude.com.

Run when:
- Documentation seems outdated
- New Claude Code features are released
- Official docs have been updated

```bash
node ~/.claude/skills/working-with-claude-code/scripts/update_docs.js
```

The script:
1. Fetches llms.txt from docs.claude.com
2. Extracts all Claude Code documentation URLs
3. Downloads each page to `references/`
4. Reports success/failures

## Common Patterns

### Plugin Development

Read `plugins.md` for overview, then `plugins-reference.md` for API details.

### MCP Server Setup

Read `mcp.md` for configuration format and examples.

### Hook Configuration

Read `hooks.md` for overview, then `hooks-guide.md` for implementation details.

### Skill Creation

Read `skills.md` for the complete skill authoring guide.

## What This Skill Does NOT Do

- This skill provides **documentation access**, not procedural guidance
- For workflows on **how to build** plugins/skills, use the `extending-claude-code` skill (when available)
- This skill is a **reference library**, not a tutorial

## Red Flags

If you find yourself:
- Guessing about configuration file locations → Read `settings.md`
- Speculating about API structures → Read relevant reference doc
- Unsure about hook names → Read `hooks.md`
- Making assumptions about features → Search the docs first

**Always consult the official documentation before guessing.**
