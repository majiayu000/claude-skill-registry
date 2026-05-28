---
name: plugin-best-practices
description: This skill should be used when the user asks to "validate a plugin", "optimize plugin", "check plugin quality", "review plugin structure", "find plugin issues", "check best practices", "analyze plugin", or mentions plugin validation, optimization, or quality assurance.
argument-hint: (no arguments - provides knowledge only)
user-invocable: false
version: 0.2.0
---

# Plugin Best Practices

Validation and optimization guidance for Claude Code plugins.

RFC 2119 terms are mandatory: use only MUST, MUST NOT, SHOULD, SHOULD NOT, MAY. Replace REQUIRED/SHALL with MUST, SHALL NOT with MUST NOT, RECOMMENDED with SHOULD, NOT RECOMMENDED with SHOULD NOT, and OPTIONAL with MAY. See `references/rfc-2119.md`.

## Core Principles

- Skills are the preferred extension mechanism for new plugins, with commands reserved for backward compatibility.

## Component Model

### Skills

Skills are markdown prompts that run in the main conversation context and extend knowledge or provide workflows.

Two skill types are supported:
- **Instruction-type** (`user-invocable: true` → `commands`): imperative voice, phase-based workflows, user-invoked.
- **Knowledge-type** (`user-invocable: false` → `skills`): declarative voice, topic-based references, auto-loaded.

### Agents

Agents are autonomous subprocesses with isolated context and their own system prompts.

Key characteristics:
- Isolated context with a dedicated system prompt in the agent `.md` file.
- Restricted tool allowlists for safety and focus.
- Specialized expertise with judgment over execution details.
- Router-friendly descriptions containing 2–4 `<example>` blocks.

## Selection Guide

- **Instruction-type skills** apply when a user invokes a workflow via slash command and the process is linear.
- **Knowledge-type skills** apply when providing reference knowledge for agents or the main session.
- **Agents** apply when isolation, specialization, and autonomous decision-making are required.

## Templates and Structure

Templates are centralized for reuse across components. See `${CLAUDE_PLUGIN_ROOT}/examples/` for complete templates.

## plugin.json Declaration

| Config | User invocable | Claude invocable | Declare in |
|--------|----------------|------------------|------------|
| `user-invocable: false` | No | Yes | `skills` (knowledge-type) |
| (default) or `user-invocable: true` | Yes | Yes | `commands` (instruction-type) |
| `disable-model-invocation: true` | Yes | No | `commands` (instruction-type, no auto-invoke) |

## Validation Checklist

- Skills are under 500 lines with progressive disclosure to `references/`.
- Agents include clear delegation descriptions and a single responsibility.
- Agent descriptions include 2–4 `<example>` blocks.
- Component names use kebab-case.
- Scripts are executable with shebangs and `${CLAUDE_PLUGIN_ROOT}` paths.
- Tool invocations avoid explicit tool-call phrasing (see `references/tool-invocations.md`).
- Skill references use qualified names (`plugin-name:skill-name`).
- Component paths are relative and start with `./`.
- Components live at plugin root, not inside `.claude-plugin/`.
- Skills and commands are declared in `plugin.json` (recommended).
- Skill type matches manifest and writing style:
  - Instruction-type uses imperative voice.
  - Knowledge-type uses declarative voice.

## Severity Levels

- **Critical**: MUST fix before plugin works correctly.
- **Warning**: SHOULD fix for best-practices compliance.
- **Info**: MAY improve (optional).

## Reference Link Rule

Links to external templates or example files include a one-sentence description of what the target contains before the link.

## Additional Resources

Reference documents live in `references/`:
- **Components**: `references/components/[type].md` — component-specific requirements.
- **Structure**: `references/directory-structure.md` — layout and naming conventions.
- **Manifest**: `references/manifest-schema.md` — plugin.json schema and configuration.
- **Tool Usage**: `references/tool-invocations.md` — tool invocation patterns.
- **MCP Patterns**: `references/mcp-patterns.md` — MCP server integration.
- **Debugging**: `references/debugging.md` — diagnostics for loading failures.
- **CLI Commands**: `references/cli-commands.md` — plugin CLI operations.
- **TodoWrite Tool**: `references/todowrite-usage.md` — TodoWrite usage.

## Prompt Repetition

- Critical rules and safety constraints appear in multiple phases only when execution depends on it.
- Repetition favors concise restatement rather than verbatim duplication.

## Parallel Agent Execution

Parallel execution applies when tasks are independent and results can be merged afterward.

Request pattern:
```markdown
# Explicit parallel request

Launch all agents simultaneously:
- `domain-analyzer` agent
- `quality-validator` agent
- `format-checker` agent

# Or use "in parallel" phrasing

Launch 3 parallel agents to process different aspects independently
```

Best practices:
- "parallel" or "simultaneously" appears explicitly in the request.
- Descriptive style names the agent and intent.
- Consolidation merges findings and resolves conflicts.

Common pattern:
```markdown
1. Sequential setup (if needed)
2. Launch specialized analyses in parallel:
   - `aspect-one-analyzer` agent — first dimension
   - `aspect-two-validator` agent — second dimension
   - `aspect-three-checker` agent — third dimension
3. Consolidate results and present unified output
```
