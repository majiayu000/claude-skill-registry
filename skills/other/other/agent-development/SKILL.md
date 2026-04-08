---
name: agent-development
description: >
  Generates Claude Code plugin agent .md files: writes YAML frontmatter (name, model,
  color, tools, hooks, disallowedTools), crafts system prompts, and creates triggering
  example blocks with context and commentary. Validates agent structure against naming,
  length, and format constraints. Use when the user asks to create an agent, add an
  agent, write a subagent, configure agent frontmatter, design agent system prompts,
  set agent tools or colors, build an autonomous agent, or add agent hooks.
---

# Agent Development for Claude Code Plugins

Agents are autonomous markdown files with YAML frontmatter that handle multi-step tasks independently. Agents are for autonomous work; commands are for user-initiated actions.

## Workflow

1. Define agent purpose and triggering conditions
2. Create `agents/agent-name.md` with frontmatter + system prompt body
3. Include 2-4 `<example>` blocks in description
4. Validate structure (see constraints below)
5. Test triggering with real scenarios
6. If validation fails: check error recovery table, fix, re-validate

## Agent File Template

```markdown
---
name: agent-identifier
description: Use this agent when [triggering conditions]. Examples:

<example>
Context: [Situation]
user: "[Request]"
assistant: "[Response before triggering]"
<commentary>[Why this agent triggers]</commentary>
</example>

model: inherit
color: blue
tools: ["Read", "Write", "Grep"]
---

You are [role] specializing in [domain].

**Your Core Responsibilities:**
1. [Primary task]
2. [Secondary task]

**Process:**
1. [Step 1]
2. [Step 2]

**Output Format:**
[What to return and how]

**Edge Cases:**
- [Case]: [How to handle]
```

## Frontmatter Reference

| Field | Required | Format | Constraints |
|-------|----------|--------|-------------|
| `name` | Yes | `lowercase-hyphens` | 3-50 chars, start/end alphanumeric, no underscores |
| `description` | Yes | Text + `<example>` blocks | 10-5000 chars, must include triggering conditions |
| `model` | Yes | `inherit\|sonnet\|opus\|haiku` | Use `inherit` unless specific need |
| `color` | Yes | `blue\|cyan\|green\|yellow\|magenta\|red` | Distinct per plugin |
| `tools` | No | Array of tool names | Least-privilege principle; default: all tools |
| `hooks` | No | Array of hook configs | See hooks section |
| `disallowedTools` | No | Array with `Task(AgentName)` | Prevents specific agents from running |

**Color conventions:** blue/cyan = analysis/review, green = success, yellow = validation, red = security, magenta = creative.

**Common tool sets:**
- Read-only: `["Read", "Grep", "Glob"]`
- Code generation: `["Read", "Write", "Grep"]`
- Testing: `["Read", "Bash", "Grep"]`

## Description Field

The description must include triggering conditions and 2-4 `<example>` blocks. Each example needs: `Context`, `user` message, `assistant` response, and `<commentary>` explaining why the agent triggers.

Cover different triggering types across examples:
- **Explicit**: user directly requests the agent's function
- **Proactive**: agent triggers after relevant work without explicit request
- **Implicit**: user implies need without stating it directly

See `references/triggering-examples.md` for detailed patterns and templates.

## Hooks

Agent-level hooks scoped to agent lifecycle:

```yaml
hooks:
  - type: PreToolUse    # Validate before agent uses tools
    once: true          # Runs only once per invocation
  - type: PostToolUse   # React to agent tool results
  - type: Stop          # Cleanup when agent completes
```

Hooks inherit agent context. No command/prompt field needed. See `../hook-development/` for full documentation.

## disallowedTools

Prevent specific agents from being invoked:

```yaml
disallowedTools: ["Task(SWEAgent)", "Task(ExperimentalAgent)"]
```

Also configurable in settings.json and via `--disallowedTools` CLI flag.

## System Prompt Guidelines

The markdown body below the frontmatter becomes the agent's system prompt. Write in second person ("You are...", "You will...").

**Required sections:** Role description, Core Responsibilities, Process steps, Output Format.
**Recommended sections:** Quality Standards, Edge Cases.

**Keep prompts under 10,000 characters.** Optimal range: 500-3,000 characters. If longer, extract reference data into separate files.

See `references/system-prompt-design.md` for analysis, generation, validation, and orchestration prompt patterns.

## Agent Organization

```
plugin-name/
└── agents/
    ├── analyzer.md
    ├── reviewer.md
    └── generator.md
```

All `.md` files in `agents/` are auto-discovered. Agents are namespaced automatically: `agent-name` (single plugin) or `plugin:subdir:agent-name` (with subdirectories).

## Best Practices

- Include 2-4 concrete `<example>` blocks with varied phrasings in description
- Use `inherit` for model unless a specific model is required
- Apply least-privilege tool access
- Assign distinct colors per agent within a plugin
- Write specific, structured system prompts with clear process steps
- Define output format explicitly
- Test triggering with real scenarios before shipping

## Error Recovery

| Problem | Fix |
|---------|-----|
| Agent not triggering | Add more `<example>` blocks with varied phrasings; verify keywords match user intent |
| Name validation fails | Ensure 3-50 chars, lowercase + hyphens only, starts/ends alphanumeric |
| System prompt too long | Keep under 10,000 chars; extract reference data into separate files |
| Agent uses wrong tools | Add explicit `tools` array; verify tool names match exactly |
| Agent color not showing | Confirm color is one of: blue, cyan, green, yellow, magenta, red |
| Description too vague | Add triggering conditions and concrete `<example>` blocks with `<commentary>` |
| Agent triggers incorrectly | Make examples more specific; add negative-case commentary |

## Additional Resources

- `references/system-prompt-design.md` - Prompt patterns for analysis, generation, validation, orchestration agents
- `references/triggering-examples.md` - Example formats and triggering best practices
- `references/agent-creation-system-prompt.md` - The exact prompt from Claude Code
- `examples/agent-creation-prompt.md` - AI-assisted agent generation template
- `examples/complete-agent-examples.md` - Full agent examples for different use cases
- `scripts/validate-agent.sh` - Validate agent file structure
