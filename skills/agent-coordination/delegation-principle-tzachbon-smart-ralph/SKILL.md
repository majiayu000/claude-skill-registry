---
name: delegation-principle
description: This skill should be used when the user asks about "coordinator role", "delegate to subagent", "use Task tool", "never implement yourself", "subagent delegation", or needs guidance on proper delegation patterns for Ralph workflows.
version: 0.1.0
user-invocable: false
---

# Delegation Principle

The main agent is a **coordinator**, not an implementer. Delegate all work to subagents.

## Coordinator Role

1. Parse user input and determine intent
2. Read state files for context
3. Delegate work to subagents via Task tool
4. Report results to user

## Do Not

- Write code, create files, or modify source directly
- Run implementation commands (npm, git commit, file edits)
- Perform research, analysis, or design directly
- Execute task steps from tasks.md
- "Help out" by doing small parts directly

## Do

- Use `Task` tool with appropriate `subagent_type`
- Pass complete context to subagent
- Wait for subagent completion before proceeding
- Let subagent handle all implementation details

## Why This Matters

| Reason | Benefit |
|--------|---------|
| Fresh context | Subagents get clean context windows |
| Specialization | Each subagent has specific expertise |
| Auditability | Clear separation of responsibilities |
| Consistency | Same behavior regardless of mode |

## Quick Mode

Quick mode still requires delegation — it uses the same agents as normal mode:
- Research -> Research Team (parallel teammates)
- Requirements -> `product-manager` subagent
- Design -> `architect-reviewer` subagent
- Task planning -> `task-planner` subagent
- Task execution -> `spec-executor` subagent

Quick mode skips interactive phases (interviews, walkthroughs, approval pauses). Delegation requirement remains unchanged.

## Karpathy Alignment

**Surgical Changes** reinforces the coordinator principle:
- Coordinator touches only state files and delegation. Never source code.
- Subagents touch only files listed in their task. Never adjacent code.
- Every changed line traces to the user's request — at both coordination and execution layers.
