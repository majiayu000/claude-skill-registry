---
name: claude-code-slash-commands
description: This skill should be used when the user asks to "create a command", "write a slash command", "build a plugin command", or wants to add custom commands to Claude Code.
---

# Slash Command Development

Create custom slash commands for Claude Code.

## Quick Reference

You MUST read these references for detailed guidance:

- [Official Documentation](./references/official-docs.md) - Anthropic's slash command guide

## Command Structure

Commands are Markdown files in specific locations:

| Scope | Location | Description suffix |
|-------|----------|-------------------|
| Project | `.claude/commands/` | `(project)` |
| Personal | `~/.claude/commands/` | `(user)` |
| Plugin | `commands/` in plugin root | `(plugin)` |

## Basic Command

```markdown
---
description: Brief description of what this command does
---

Your prompt instructions here.
```

## Frontmatter Options

```yaml
---
allowed-tools: Bash(git:*), Read
argument-hint: [filename] [options]
description: What this command does
model: claude-3-5-haiku-20241022
disable-model-invocation: false
context: fork
---
```

| Field | Purpose |
|-------|---------|
| `allowed-tools` | Tools the command can use |
| `argument-hint` | Shows in autocomplete (e.g., `[message]`) |
| `description` | Brief description (required for SlashCommand tool) |
| `model` | Specific model to use |
| `disable-model-invocation` | Prevent programmatic invocation |
| `context: fork` | Run in isolated sub-agent context, preventing side effects on main agent state |

## Arguments

**All arguments:**
```markdown
Fix issue #$ARGUMENTS following our coding standards
```

**Positional arguments:**
```markdown
Review PR #$1 with priority $2 and assign to $3
```

## Dynamic Content

<!-- NOTE: Avoid isolated special chars in backticks due to bug #12762 -->
<!-- See: https://github.com/anthropics/claude-code/issues/12762 -->

**Bash execution** (prefix with exclamation mark):
```text
Current branch: EXCLAMATION`git branch --show-current`
Recent commits: EXCLAMATION`git log --oneline -5`
```
Replace EXCLAMATION with the exclamation mark character - workaround for [bug #12762](https://github.com/anthropics/claude-code/issues/12762).

**File references** (prefix with at-sign):
```markdown
Review the implementation in @src/utils/helpers.js
```

## Namespacing

Subdirectories group related commands:

- `.claude/commands/frontend/test.md` → `/test` shows `(project:frontend)`
- `.claude/commands/backend/test.md` → `/test` shows `(project:backend)`

## Checklist

- [ ] Description filled in frontmatter
- [ ] `argument-hint` if command takes arguments
- [ ] `allowed-tools` if using Bash or specific tools
- [ ] Test with `/command-name --help` style invocation
