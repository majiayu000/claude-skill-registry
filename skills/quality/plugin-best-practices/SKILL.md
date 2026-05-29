---
name: plugin-best-practices
description: This skill should be used when the user asks to "validate a plugin", "optimize plugin", "check plugin quality", "review plugin structure", "find plugin issues", "check best practices", "analyze plugin", or mentions plugin validation, optimization, or quality assurance.
argument-hint: (no arguments - provides knowledge only)
user-invocable: false
version: 0.2.0
---

# Plugin Best Practices

Validation guidance for Claude Code plugins. Uses RFC 2119 terms: REQUIRED → MUST, RECOMMENDED → SHOULD, OPTIONAL → MAY.

## Core Principles

- Skills are the preferred extension mechanism; commands reserved for backward compatibility.
- Progressive disclosure protects context: metadata (~50 tokens) -> SKILL.md (~500 tokens target) -> references (2000+ tokens, access only when needed).

## Component Model

**Skills** have two types:
- **Instruction-type** (`user-invocable: true` → declared in `commands`): imperative voice, Phase-based workflows
- **Knowledge-type** (`user-invocable: false` → declared in `skills`): declarative voice, topic-based references

**Agents**: Autonomous subprocesses with isolated context, restricted tools, and 2-4 `<example>` blocks in descriptions.

See `references/component-model.md` for detailed selection criteria. Templates at `${CLAUDE_PLUGIN_ROOT}/examples/`.

## Tool Invocation Patterns

| Tool | Style | Format |
|------|-------|--------|
| Read, Write, Glob, Grep, Edit | Implicit | "Find files...", "Read the file..." |
| Bash | Implicit | "Run `git status`" (describe commands) |
| Task | Implicit | "Launch `plugin-name:agent-name` agent" |
| Skill, AskUserQuestion, TaskCreate | **Explicit** | "**Load skill** using Skill tool", "Use AskUserQuestion tool" |

**Qualified names**: MUST use `plugin-name:component-name` format for plugin components.

**allowed-tools**: NEVER use bare `Bash` - always use filters like `Bash(git:*)`.

See `references/tool-invocations.md` for complete patterns and anti-patterns.

## Severity Levels

- **Critical**: MUST fix before plugin works correctly.
- **Warning**: SHOULD fix for best-practices compliance.
- **Info**: MAY improve (optional).

## Validation Checklist

- SKILL.md token target ~500 (warnings if exceeded, not errors)
- Agents include 2-4 `<example>` blocks in descriptions
- Component names use kebab-case
- Tool invocations avoid explicit phrasing (except Skill, AskUserQuestion, TaskCreate)
- Skills/commands declared in `plugin.json`
- Skill type matches declaration: instruction-type in `commands`, knowledge-type in `skills`

See `references/validation-checklist.md` for complete checklist.

## References

- `references/validation-checklist.md` - Complete quality checklist
- `references/component-model.md` - Component types and selection
- `references/components/[type].md` - Component-specific guides
- `references/tool-invocations.md` - Tool usage patterns
- `references/directory-structure.md` - Layout and naming
- `references/manifest-schema.md` - plugin.json schema

