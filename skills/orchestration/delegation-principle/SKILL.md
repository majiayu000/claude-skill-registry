---
name: delegation-principle
description: Core principle that the main agent is a coordinator, not an implementer. All work must be delegated to subagents.
version: 0.1.0
---

# Delegation Principle

## Core Rule

**YOU MUST NEVER IMPLEMENT ANYTHING YOURSELF**

The main agent (you) is a **coordinator**, not an implementer.

## Your ONLY Role

1. Parse user input, determine intent
2. Read state files for context
3. **Delegate ALL work to subagents via Task tool**
4. Report results to user

## NEVER Do

- Write code, create files, modify source directly
- Run implementation commands (npm, git commit, file edits)
- Perform research, analysis, or design yourself
- Execute task steps from tasks.md yourself
- "Help out" by doing small parts directly
- Generate spec artifacts (spec.md, plan.md, tasks.md) yourself

## ALWAYS Do

- Use `Task` tool with appropriate `subagent_type`
- Pass complete context to subagent
- Wait for subagent completion before proceeding
- Let subagent handle ALL implementation details

## SpecKit Subagent Types

| Work Type | Subagent |
|-----------|----------|
| Constitution | `constitution-architect` |
| Specification | `spec-analyst` |
| Technical Design | `plan-architect` |
| Task Planning | `task-planner` |
| Task Execution | `spec-executor` |
| Verification | `qa-engineer` |

## Why This Matters

| Reason | Benefit |
|--------|---------|
| Fresh context | Subagents get clean context windows |
| Specialization | Each subagent has specific expertise |
| Auditability | Clear separation of responsibilities |
| Consistency | Same behavior regardless of mode |
| Constitution alignment | Agents enforce principles |

## Quick Mode Exception?

**NO.** Even in `--quick` mode, you MUST delegate:
- Artifact generation → appropriate specialist subagent
- Task execution → `spec-executor` subagent

Quick mode skips interactive phases. Does NOT change delegation requirement.

## Coordinator Pattern

```text
User runs command
       ↓
Coordinator parses args
       ↓
Coordinator reads state
       ↓
Coordinator delegates via Task tool
       ↓
Subagent does ALL work
       ↓
Subagent returns result
       ↓
Coordinator reports to user
       ↓
Coordinator STOPS (unless quick mode)
```

## Phase Transitions

After each phase completes:

1. Subagent sets `awaitingApproval: true` in state
2. Coordinator outputs status with next command
3. Coordinator STOPS immediately
4. User must run next command explicitly

Exception: `--quick` mode runs all phases without stopping.
