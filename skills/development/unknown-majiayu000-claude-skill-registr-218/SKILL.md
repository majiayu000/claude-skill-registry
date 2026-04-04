---
name: subagents-creator
description: Guide for defining and using Claude subagents effectively. Use when (1) creating new subagent types, (2) learning how to delegate work to specialized subagents, (3) improving subagent delegation prompts, (4) understanding subagent orchestration patterns, or (5) debugging ineffective subagent usage.
---

# Subagents Creator

This skill provides guidance for defining, using, and improving Claude subagents—the specialized agents that handle specific domains like `explore`, `librarian`, `oracle`, and `frontend-ui-ux-engineer`.

## Quick Start

### Delegating Work

When delegating to subagents, use the **mandatory 7-section structure**:

```
1. TASK: Atomic, specific goal (one action per delegation)
2. EXPECTED OUTCOME: Concrete deliverables with success criteria
3. REQUIRED SKILLS: Which skill to invoke
4. REQUIRED TOOLS: Explicit tool whitelist (prevents tool sprawl)
5. MUST DO: Exhaustive requirements - leave NOTHING implicit
6. MUST NOT DO: Forbidden actions - anticipate and block rogue behavior
7. CONTEXT: File paths, existing patterns, constraints
```

### Choosing a Subagent

See [subagent-types.md](references/subagent-types.md) for detailed guidance on which subagent to use:
- **`explore`**: Contextual grep for codebases
- **`librarian`**: Reference search (docs, OSS, web)
- **`oracle`**: Deep reasoning for architecture/complex decisions
- **`frontend-ui-ux-engineer`**: Visual UI/UX changes

## Defining New Subagents

**Only create subagents when**: The task domain has distinct tooling, expertise, or patterns that benefit from specialization.

See [delegation-patterns.md](references/delegation-patterns.md) for:
- Subagent definition templates
- When to create a new subagent vs using existing ones
- Naming and description guidelines

## Common Pitfalls

See [common-pitfalls.md](references/common-pitfalls.md) for:
- Vague delegation prompts and why they fail
- Over-delegating trivial tasks
- Subagent misalignment with task type
- Anti-patterns in agent orchestration

## Best Practices

1. **One action per delegation**: Combine tasks in parallel calls, not one call
2. **Be exhaustive**: "MUST DO" and "MUST NOT DO" sections prevent drift
3. **Background everything**: Use `background_task` for `explore` and `librarian`
4. **Explicit tool lists**: Prevent subagents from using unauthorized tools
5. **Verify results**: Check that delegated work meets expectations before proceeding

## Delegation Example

```python
# GOOD: Specific, exhaustive
background_task(
    agent="explore",
    prompt="""
    1. TASK: Find all authentication implementations
    2. EXPECTED OUTCOME: List of files with auth logic, patterns used
    3. REQUIRED SKILLS: explore
    4. REQUIRED TOOLS: Grep, Read
    5. MUST DO: Search for 'jwt', 'session', 'auth' patterns; identify middleware; list all endpoints
    6. MUST NOT DO: Don't modify any files; don't run build/test commands
    7. CONTEXT: Working in ./src directory, looking for Express.js patterns
    """
)

# BAD: Vague, implicit expectations
background_task(
    agent="explore",
    prompt="Find auth stuff in the codebase"
)
```

## Reference Files

- [subagent-types.md](references/subagent-types.md) - When to use each subagent type
- [delegation-patterns.md](references/delegation-patterns.md) - Prompt templates and patterns
- [common-pitfalls.md](references/common-pitfalls.md) - Anti-patterns and how to avoid them
