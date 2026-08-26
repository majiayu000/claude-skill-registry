---
name: hook-development
description: "Use when creating, modifying, or debugging Claude Code hooks — PreToolUse, PostToolUse, Stop, SubagentStop, SessionStart, SessionEnd, UserPromptSubmit, PreCompact, Notification. Covers the plugin `hooks/hooks.json` wrapper format vs. the user `settings.json` direct format, matchers, security patterns, `$CLAUDE_PLUGIN_ROOT` portability, lifecycle limitations, and debugging. Trigger on \"add a hook\", \"validate tool use\", \"block dangerous commands\", \"enforce completion\", \"hook-based automation\"."
disable-model-invocation: true
---

# hook-development

Canonical skill: `skills/hook-development/SKILL.md`

Read that file and follow it exactly. Resolve relative links against `skills/hook-development/`, not this wrapper.

Cursor has no Skill tool. Treat "invoke the hook-development skill" as: Read `skills/hook-development/SKILL.md`.
