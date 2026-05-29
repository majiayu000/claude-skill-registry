---
name: workflow-orchestration
description: >
  Coordinate structured thinking and multi-agent parallel execution for complex tasks.
  Use when tackling multi-step projects, planning parallel work, breaking down complex
  problems, coordinating specialist tasks, facing architectural decisions, or when user
  mentions "workflow", "orchestration", "multi-step", "coordinate", "parallel execution",
  "structured thinking", "break this down", "plan this out", "how should I approach",
  or needs help planning complex implementations.
---

# Workflow Orchestration

Guide users through structured thinking and recommend appropriate tools for complex tasks.

## Quick Decision

| Situation | Recommendation |
|-----------|----------------|
| Multi-step project, full SDLC | `/core:develop` command |
| Plan only, implement later | `/core:develop --plan-only` |
| Resume existing plan | `/core:develop @path/to/plan.md` |
| Single complex problem needing deep analysis | `/think` command |
| Security-sensitive or high-stakes work | `/core:develop --validate` |
| Strategic decision with long-term impact | `deep-think-partner` agent |
| Simple task, clear steps | Inline guidance (no command needed) |

## When to Orchestrate

Detect these signals for structured thinking:

**Keyword triggers:**
- "workflow", "orchestration", "coordinate", "parallel"
- "multi-step", "sequential", "dependencies"
- "break down", "plan this out", "how should I approach"

**Context triggers:**
- Architectural decisions affecting multiple components
- Multi-file changes requiring coordination
- Problems with unclear scope needing discovery
- Tasks that benefit from specialist agents

## Orchestration Pattern

When structured approach is needed:

```
1. GATE     → Is the request clear and actionable?
2. CONTEXT  → What files/patterns are relevant?
3. PLAN     → What tasks? Parallel vs sequential?
4. EXECUTE  → Deploy specialists, maximize parallelism
5. VALIDATE → Confidence scoring (if needed)
6. REPORT   → Summary with next steps
```

## Command Reference

### `/core:develop <request> [flags]`

Unified SDLC command with 6-phase pipeline and multi-agent orchestration.

**Flags:**
- `--plan-only` - Stop after Phase 2 (save plan, don't implement)
- `--validate` - Enable deep validation with opus agent
- `--phase=N` - Execute specific phase only
- `--auto` - Autonomous mode (no checkpoints)

**Best for:** Feature implementations, refactoring projects, any multi-step development task.

**Resume mode:** `/core:develop @path/to/plan.md` loads existing plan and continues.

### `/think [problem]`

Invoke deep-think-partner for collaborative reasoning.

**Best for:** Single complex problems, decision analysis, reasoning validation, architectural decisions.

## Inline Guidance

For simpler tasks, provide structured thinking directly:

1. **Clarify scope** - What exactly needs to be done?
2. **Identify dependencies** - What must happen first?
3. **Plan sequence** - Parallel where possible, sequential where required
4. **Execute** - Work through each step
5. **Verify** - Check results meet requirements

## Model Tier Strategy

| Task Type | Model | Use Case |
|-----------|-------|----------|
| Gating, routing | haiku | Quick decisions, simple queries |
| Implementation | sonnet | Standard coding, documentation |
| Deep analysis | opus | Architecture, complex reasoning |

## Output

When providing orchestration guidance:

```markdown
## Recommended Approach

**Complexity:** [Low | Medium | High]
**Suggested tool:** [command or inline]

### Why
[Brief explanation of why this approach fits]

### Steps
1. [First step]
2. [Second step]
...
```

## Additional Resources

- [WORKFLOW.md](WORKFLOW.md) - Detailed orchestration patterns
- [EXAMPLES.md](EXAMPLES.md) - Real-world usage scenarios
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions
