---
name: create-agent
description: Create a new custom subagent for Task() delegation. Use when adding a reusable agent prompt, when the user asks to "add an agent", or when a complex workflow should be delegated to a specialized agent.
---

# Creating a New Agent

## Official Documentation

- **Primary**: https://code.claude.com/docs/en/sub-agents.md
- **Best Practices**: https://code.claude.com/docs/en/best-practices.md (section: "Create custom subagents")

## File Location

Create `.claude/agents/<agent-name>.md`

## Agent File Format

```yaml
---
name: agent-name                    # Required: lowercase-with-dashes
description: What the agent does and when to delegate to it. Be specific about trigger conditions.
# Optional fields below:
tools: Read, Grep, Glob, Bash       # Comma-separated; inherits all if omitted
disallowedTools: Edit, Write        # Explicitly deny tools
model: sonnet                       # sonnet, opus, haiku, or inherit (default)
permissionMode: default             # default, acceptEdits, dontAsk, bypassPermissions, plan
skills: skill-a, skill-b            # Skills to preload into agent context
---

You are a [role description].

## Your Task

When invoked:
1. First step
2. Second step
3. Third step

## Guidelines

- Specific instruction
- Another instruction

## Output Format

Describe expected output format.
```

## Built-in Subagent Types

Before creating a custom agent, consider if a built-in type suffices:

| Type | Purpose | Tools |
|------|---------|-------|
| `Explore` | Fast codebase search, file discovery | Read-only |
| `Plan` | Architecture, implementation planning | Read-only |
| `Bash` | Command execution | Bash only |
| `general-purpose` | Complex multi-step tasks | All tools |

## Design Principles

**Focus**: One agent, one job. Don't create jack-of-all-trades agents.

**Minimal Tools**: Grant only necessary tools. Read-only agents can't accidentally break things.

**Clear Workflow**: Numbered steps help the agent stay on track.

**Good Description**: Claude uses the description to decide when to delegate. Include:
- What the agent specializes in
- When to use it (trigger conditions)
- "Use proactively when..." if appropriate

## Example: Read-Only Reviewer

```yaml
---
name: lore-checker
description: Verify lore consistency across campaign materials. Use when adding new lore, after writing session logs, or when the user asks to check for contradictions.
tools: Read, Grep, Glob
model: haiku
---

You are a lore consistency checker for TTRPG campaigns.

## Your Task

1. Identify the new or modified lore element
2. Search for related existing lore using Grep
3. Read relevant files
4. Report any contradictions or inconsistencies
5. Suggest resolutions if conflicts found

## Output Format

**Checked**: [element being verified]
**Related Files**: [list of files examined]
**Status**: Consistent / Conflicts Found
**Details**: [explanation]
```

## Checklist

Before committing a new agent:

1. [ ] Name is lowercase-with-dashes
2. [ ] Description explains what AND when to delegate
3. [ ] Tools are minimal for the task
4. [ ] Workflow steps are clear and numbered
5. [ ] Output format is specified
6. [ ] Tested via Task() delegation
