---
name: using-spool-skills
description: Use when discovering, finding, invoking, or loading skills. Ensures skills are invoked BEFORE responding. Establishes skill priority and usage patterns for OpenCode, Claude Code, and Codex.
---

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

This is not negotiable. This is not optional. You cannot rationalize your way out of this.
</EXTREMELY-IMPORTANT>

## How to Access Skills

### OpenCode

Use the native `skill` tool:

```bash
# List all available skills
skill list

# Load a specific skill
skill load spool-brainstorming
```

Skill locations:
- Project skills: `.opencode/skills/`
- User skills: `~/.config/opencode/skills/`

### Claude Code

Use the `mcp_skill` function:

```
mcp_skill with name="spool-brainstorming"
```

Skill locations:
- Project skills: `.claude/skills/`

### Codex

Read skill files directly:

```bash
cat .codex/skills/spool-brainstorming/SKILL.md
```

Skill locations:
- Project skills: `.codex/skills/`
- User skills: `~/.codex/skills/`

### Detecting Your Harness

- **OpenCode**: Has `skill` tool available, `.opencode/` directory
- **Claude Code**: Has `mcp_skill` function, `.claude/` directory
- **Codex**: Has `.codex/` directory, no native skill tool

# Using Skills

## The Rule

**Invoke relevant or requested skills BEFORE any response or action.** Even a 1% chance a skill might apply means that you should invoke the skill to check. If an invoked skill turns out to be wrong for the situation, you don't need to use it.

## Red Flags

These thoughts mean STOP—you're rationalizing:

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "I can check git/files quickly" | Files lack conversation context. Check for skills. |
| "Let me gather information first" | Skills tell you HOW to gather information. |
| "This doesn't need a formal skill" | If a skill exists, use it. |
| "I remember this skill" | Skills evolve. Read current version. |
| "This doesn't count as a task" | Action = task. Check for skills. |
| "The skill is overkill" | Simple things become complex. Use it. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |
| "This feels productive" | Undisciplined action wastes time. Skills prevent this. |
| "I know what that means" | Knowing the concept ≠ using the skill. Invoke it. |

## Skill Priority

When multiple skills could apply, use this order:

1. **Process skills first** (brainstorming, debugging) - these determine HOW to approach the task
2. **Implementation skills second** (frontend-design, mcp-builder) - these guide execution

"Let's build X" → brainstorming first, then implementation skills.
"Fix this bug" → debugging first, then domain-specific skills.

## Skill Types

**Rigid** (TDD, debugging): Follow exactly. Don't adapt away discipline.

**Flexible** (patterns): Adapt principles to context.

The skill itself tells you which.

## User Instructions

Instructions say WHAT, not HOW. "Add X" or "Fix Y" doesn't mean skip workflows.
