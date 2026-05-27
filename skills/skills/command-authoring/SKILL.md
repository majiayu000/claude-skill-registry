---
name: command-authoring
description: Guide for authoring slash commands. Use when creating, building, reviewing, or improving commands, learning command best practices, or deciding when to use commands vs skills.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
# model: inherit
---

## Reference Files

Detailed command authoring guidance:

- [command-design-patterns.md](command-design-patterns.md) - Four design patterns with complete examples and when to use each
- [command-creation-process.md](command-creation-process.md) - Step-by-step command creation workflow (7 steps)
- [command-examples.md](command-examples.md) - Real command examples with analysis and best practices

---

## About Commands

Commands are user-invoked shortcuts that provide explicit control over when capabilities are used. They're typed as `/command-name`.

**Key characteristics**:

- **User-invoked** - Typed explicitly as `/command-name` (not auto-triggered)
- **Simple** - Focused instructions or actions rather than complex logic
- **Focused** - Single, clear purpose
- **Explicit** - User controls timing of invocation
- **Discoverable** - Shown in `/help` output

**When to use commands**:

- User wants explicit shortcut for frequent task
- Simple, focused instructions
- User should control timing
- Convenience wrapper for common operations

## Core Philosophy

### Commands Should Be Simple

**Golden rule**: Commands provide focused instructions, they don't implement complex logic.

**Good command** (simple and focused):

```markdown
---
description: Run comprehensive code quality checks
---

# check-quality

Run linting, type checking, and tests on the codebase.

!npm run lint && npm run type-check && npm test
```

**Bad command** (complex logic):

```markdown
# bad-example

# DON'T DO THIS - complex logic in command

First analyze all files, then determine which linters to run, then parse results,
then generate a custom report format, then send notifications...
[50 lines of implementation details]
```

**Why keep it simple**:

- Easier to maintain
- Clear purpose
- Less prone to errors
- Follows single responsibility principle

### Commands Are Explicit

Unlike skills (which auto-trigger), commands require user action.

**Use commands when**:

- User wants control over timing
- Action shouldn't happen automatically
- Frequently-used prompt that deserves shortcut
- Explicit workflow trigger

**Use skills when**:

- Should auto-trigger based on context
- User doesn't need to remember to invoke it
- Complex domain knowledge that enhances conversation

## Command Structure

### Required Elements

Every command must have:

1. **description field** (in frontmatter) - Required for `/help` and model invocation
2. **Command name heading** (# command-name)
3. **Clear purpose** - What the command does

### Optional Elements

Depending on complexity:

- **Usage section** - How to invoke, with/without arguments
- **What It Does** - Detailed explanation
- **Examples** - Sample invocations
- **Use Cases** - When to use the command
- **Output** - What to expect

### Two Patterns

**Pattern 1: Simple Command** (6-10 lines)

- Just frontmatter + brief description
- Minimal documentation
- Clear, focused instructions

**Pattern 2: Documented Command** (30-80 lines)

- Full usage instructions
- Examples and use cases
- Detailed explanation of what happens
- What It Does section

**Choose based on**:

- Complexity of the operation
- Whether arguments need explanation
- How often users will reference it

See [command-design-patterns.md](command-design-patterns.md) for detailed design patterns and examples.

See [command-creation-process.md](command-creation-process.md) for step-by-step creation workflow.

## Commands vs Skills Decision Guide

**📄 See [when-to-use-what.md](../../references/when-to-use-what.md) for complete decision guide including agents and output-styles (shared)**

**Quick guide**:

**Use a Command when**:

- User wants explicit control over timing
- Action should be deliberate, not automatic
- Frequently-used prompt deserves shortcut
- User-initiated workflow
- Simple wrapper around agent/skill

**Use a Skill when**:

- AI should auto-discover capability
- Complex domain knowledge
- Should trigger on user queries automatically
- Needs progressive disclosure with references/
- Automatic workflow assistance

## Common Mistakes to Avoid

1. **Complex logic in command** - Commands should provide focused instructions, not implement complex workflows
2. **Missing description** - Frontmatter description is required
3. **Unclear purpose** - Command should have single, clear focus
4. **Vague purpose** - Be specific about what the command does
5. **Too many arguments** - Keep it simple, 0-2 args typically
6. **Not testing with /help** - Verify command appears correctly
7. **Poor naming** - Use descriptive, action-oriented names

See [command-examples.md](command-examples.md) for complete examples with analysis.

## Tips for Success

1. **Keep commands under 50 lines** unless truly necessary
2. **Stay focused** - one clear purpose per command
3. **Test with `/help`** to verify display
4. **Use descriptive names** - action verbs work well
5. **Make purpose immediately clear** - no guessing
6. **Optional arguments are better** - provide defaults
7. **Start simple** - can always add documentation later

## Related Skills

This skill is part of the authoring skill family:

- **author-agent** - Guide for creating agents
- **author-skill** - Guide for creating skills
- **author-command** - Guide for creating commands (this skill)
- **author-output-style** - Guide for creating output styles

For validation, use the corresponding audit skills:

- **audit-command** - Validate command configurations
- **audit-coordinator** - Comprehensive multi-faceted audits

## Quick Start Checklist

Creating a new command:

- [ ] Identify the purpose and operation
- [ ] Choose descriptive name (kebab-case)
- [ ] Write clear description (50-150 chars)
- [ ] Decide: simple (6-10 lines) or documented (30-80 lines)?
- [ ] Create file at `~/.claude/commands/command-name.md`
- [ ] Add required frontmatter with description
- [ ] Write focused instructions
- [ ] Test with `/help` and invocation
- [ ] Verify arguments work correctly (if any)

## Reference to Standards

For detailed standards and validation:

- **Naming conventions** - Use kebab-case for command names
- **Frontmatter requirements** - description field is required
- **File organization** - `~/.claude/commands/command-name.md`

See `audit-coordinator` skill for comprehensive standards.
