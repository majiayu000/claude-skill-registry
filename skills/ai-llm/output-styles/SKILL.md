---
name: output-styles
description: Understanding output styles in Claude Code (deprecated feature). Use when user asks about customizing Claude's behavior, output styles, or explanatory/learning modes.
---

# Claude Code Output Styles

## Deprecation Status
Output styles are **deprecated** as of November 5, 2025. The feature has been automatically converted to plugins and is no longer supported.

## What Output Styles Were

Output styles allowed customization of Claude Code's behavior beyond software engineering tasks. They directly modified the system prompt while preserving core capabilities like file operations and script execution.

## Built-in Styles (Deprecated)

**Default**: Standard software engineering assistance

**Explanatory**: Provides educational 'Insights' in between helping you complete software engineering tasks

**Learning**: Collaborative mode where Claude shares insights and requests user contributions, marked with `TODO(human)` comments

## How They Worked

Output styles excluded default code generation instructions and substituted custom system prompt guidance instead. This differed from `CLAUDE.md` or `--append-system-prompt`, which only appended context rather than replacing the base prompt.

## Migration Path

Users should transition to:

1. **SessionStart hooks** - for adding context at session start via plugin-based automation
2. **Subagents** - for specialized AI assistants with custom system prompts and specific tool permissions
3. **Plugins** - the primary replacement, with more powerful and flexible ways to customize Claude Code's behavior

## Installation Example

The explanatory output style is available as a plugin:

```
/plugin marketplace add anthropics/claude-code
/plugin install explanatory-output-style@claude-code-plugins
```

## Recommended Alternatives

For customizing Claude Code's behavior, use:
- **Plugins** for distributable, reusable customizations
- **Subagents** for task-specific specialized assistants
- **SessionStart hooks** for session initialization context
- **CLAUDE.md** for project-specific context
- `--append-system-prompt` for session-specific instructions
