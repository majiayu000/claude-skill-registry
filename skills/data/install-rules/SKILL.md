---
name: install-rules
description: Install bluera-base rule templates into your project's .claude/rules/ directory
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion]
---
# Install Rules

Install bluera-base coding standards as `.claude/rules/` files in the current project.

## Core Rules (always installed)

These rules are installed automatically:

1. **00-base.md** - Fail fast, strict typing, no commented code
2. **anti-patterns.md** - NO fallback/deprecated/legacy/backward compatibility
3. **git.md** - NO --no-verify, atomic commits

## Optional Rules

Ask the user which optional rules to install:

1. **plugins/distribution.md** - dist/ must be committed (Claude Code plugins only)

## Workflow

1. **Check existing**: Look for `.claude/rules/` in project root
2. **Ask about optional rules**: Use AskUserQuestion for user-selectable rules
3. **Create directory**: `mkdir -p .claude/rules/plugins` if needed
4. **Install core rules**: Copy 00-base.md, anti-patterns.md, git.md
5. **Install optional rules**: Based on user selection
6. **Report**: List installed files

## Template Location

Templates are at: `${CLAUDE_PLUGIN_ROOT}/templates/claude/rules/`

## Installation

Read each template from `${CLAUDE_PLUGIN_ROOT}/templates/claude/rules/` and write to `.claude/rules/` in the current project directory.

Do NOT install rules into the bluera-base plugin directory itself.

## Example AskUserQuestion

```yaml
question: "Which optional rules would you like to install?"
header: "Rules"
options:
  - label: "Plugin distribution"
    description: "dist/ must be committed - for Claude Code plugins only"
multiSelect: true
```
