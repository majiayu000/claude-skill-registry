---
name: reduce-delegate-framework
description: Apply R&D framework to optimize prompts and context. Use when optimizing context window usage, reducing prompt size, delegating to specialized agents, or applying systematic context management.
allowed-tools: Read, Grep, Glob
---

# Reduce & Delegate Framework Skill

Apply the R&D framework to optimize prompts, workflows, and context management.

## Purpose

There are only two ways to manage context: **Reduce** and **Delegate**. This skill helps you systematically apply both strategies to any context optimization challenge.

## When to Use

- Context window approaching limits
- Agent performance degrading over conversation
- Prompts growing unwieldy
- Workflows consuming too many tokens
- Need to scale agent work

## The R&D Analysis Process

### Step 1: Identify the Context Problem

Categorize the issue:

| Problem Type | Indicator | Primary Strategy |
| --- | --- | --- |
| Context Rot | Old info guiding decisions | Reduce (fresh instance) |
| Context Pollution | Unfocused, tangential | Reduce (remove irrelevant) |
| Toxic Context | Contradictory behavior | Reduce (clear conflicts) |
| Context Overflow | Approaching limits | Delegate (offload work) |

### Step 2: Apply Reduce Strategies

For each context element, ask:

1. Is this necessary for the current task?
2. Can this be loaded on-demand instead?
3. Is this information stale or outdated?
4. Does this contradict other context?

Reduction techniques:

| Technique | Application |
| --- | --- |
| Fresh instance | New task type, reset history |
| Output styles | Control verbosity, reduce tokens |
| Focused reads | Specific files vs directories |
| Priming commands | Replace static memory |
| MCP cleanup | Remove unused servers |

### Step 3: Apply Delegate Strategies

For complex or parallel work, ask:

1. Does this subtask need different context?
2. Can this run independently?
3. Would a specialized agent perform better?
4. Is there parallel work opportunity?

Delegation techniques:

| Technique | Application |
| --- | --- |
| Sub-agents | Focused tasks with isolated context |
| Background agents | Parallel work, async execution |
| Agent experts | Domain-specific knowledge |
| Spec files | Handoff between agents |

## Optimization Workflow

```text
1. Measure current context state
   - Use /context command
   - Check token consumption

2. Analyze composition
   - What's consuming most tokens?
   - What's unnecessary?

3. Apply Reduce
   - Remove unnecessary context
   - Start fresh if needed
   - Control output verbosity

4. Apply Delegate
   - Offload subtasks
   - Use specialized agents
   - Enable parallel work

5. Verify improvement
   - Measure new state
   - Compare performance
```

## Common Optimization Patterns

### Pattern: Bloated Memory File

**Before:**

```markdown
# CLAUDE.md (5KB+)
Contains: everything about the project
```

**After (Reduce):**

```markdown
# CLAUDE.md (1KB)
Contains: only universals

# .claude/commands/prime.md
Contains: task-specific context loading
```

### Pattern: Long Conversation

**Problem:** Multi-turn conversation with context rot

**Solution (Reduce):**

1. Start fresh instance
2. Use priming command to load current state
3. Continue with clean context

### Pattern: Complex Research Task

**Before:**

```text
Primary agent does research -> context polluted
Primary agent implements -> struggles with focus
```

**After (Delegate):**

```text
Primary agent delegates research -> sub-agent
Sub-agent returns summary -> primary continues
Primary agent implements -> clean context
```

### Pattern: Parallel Independent Tasks

**Before:**

```text
Task A -> Task B -> Task C (sequential, context accumulates)
```

**After (Delegate):**

```text
Task A (agent 1) \
Task B (agent 2)  -> Aggregate results
Task C (agent 3) /
```

## Output Format

When optimizing, report:

```json
{
  "analysis": {
    "current_state": "Context at 80% capacity",
    "primary_issue": "Long conversation with accumulated history",
    "secondary_issues": ["Verbose tool outputs", "Unused MCP servers"]
  },
  "reduce_recommendations": [
    {
      "action": "Start fresh instance",
      "impact": "Reset accumulated history",
      "effort": "Low"
    },
    {
      "action": "Apply concise output style",
      "impact": "50% reduction in output tokens",
      "effort": "Low"
    }
  ],
  "delegate_recommendations": [
    {
      "action": "Create research sub-agent",
      "impact": "Isolate research context",
      "effort": "Medium"
    }
  ],
  "expected_improvement": "40-60% context reduction"
}
```

## Decision Matrix

When to Reduce vs Delegate:

| Situation | Reduce | Delegate |
| --- | --- | --- |
| Stale context | X |  |
| Irrelevant context | X |  |
| Conflicting context | X |  |
| Complex subtask |  | X |
| Parallel work |  | X |
| Domain expertise needed |  | X |
| Context overflow | X | X |

## Key Quote

> "There are only two ways to manage your context window: Reduce and Delegate. Every technique fits into one or both of these buckets."

## Cross-References

- @rd-framework.md - Framework reference
- @context-audit skill - Audit before optimizing
- @context-layers.md - Understanding what to optimize
- @context-rot-vs-pollution.md - Diagnosing the problem

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
