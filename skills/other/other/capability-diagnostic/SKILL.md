---
name: capability-diagnostic
description: "Diagnose agent failures by identifying missing capabilities. Use when an agent fails a task, produces wrong output, or needs escalation. Provides a decision tree for failure analysis."
---

# Capability Diagnostic

## When to Use
Run this diagnostic when an agent:
- Fails a task (test failures, wrong output, incomplete work)
- Produces output that doesn't match the expected schema
- Gets blocked by enforcement hooks repeatedly
- Takes significantly longer than expected on a straightforward task

## Failure Analysis Decision Tree

### Step 1: Did the agent have the right tools?
- Check `allowed-tools` in agent spec (if any)
- Check if enforcement hooks blocked required tool calls
- **Fix**: Add missing tools to agent spec, or adjust hook configuration

### Step 2: Did the agent have the right context?
- Check which skills were preloaded (agent spec `skills` field)
- Was the task specification complete and unambiguous?
- Did the agent need information from files it didn't read?
- **Fix**: Add missing skills to agent spec, improve task prompt

### Step 3: Did the agent have sufficient model capability?
- Haiku struggles with: design decisions, cross-module reasoning, ambiguous specs
- Sonnet struggles with: subtle bugs, architecture-sensitive changes, performance optimization
- Opus handles: complex reasoning, cross-cutting concerns, deep analysis
- **Fix**: Escalate to next model tier (see `escalation` skill)

### Step 4: Was the task specification ambiguous?
- Did the agent ask clarifying questions? (sign of ambiguity)
- Did the agent make assumptions that turned out wrong?
- Could two reasonable agents interpret the spec differently?
- **Fix**: Rewrite task spec with explicit inputs, outputs, and constraints

### Step 5: Was it an infrastructure issue?
- Hook blocking (enforce-orchestrator-delegation, protect-hooks)
- Context window exhaustion (agent ran out of context mid-task)
- Transient errors (classifyHandoffIfNeeded, MCP connection drops, network timeouts)
- Git worktree conflicts (locked files, stale worktrees from crashed agents)
- SQLite lock contention (multiple agents accessing ReviewDb simultaneously)
- MCP server unavailable (Serena LSP not responding, Linear API rate limited)
- **Fix**: For transient errors, retry with fresh context. For persistent infrastructure, report and fix root cause.

## Output Format
After diagnosis, report:
```
Diagnosis: [tool gap | context gap | model gap | spec gap | infrastructure]
Root cause: [one sentence]
Fix: [specific action to take]
```

## Common Patterns
| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Hook blocks Write/Edit | Orchestrator trying to code | Delegate to coder agent |
| Agent ignores instructions | Context overload or wrong skills | Check preloaded skills, reduce context |
| Tests fail on agent's code | Model tier too low for task complexity | Escalate model tier |
| Agent asks many questions | Task spec is ambiguous | Rewrite spec with zero ambiguity |
| Agent produces wrong format | Missing output schema | Add structured output to task prompt |
| MCP tool call fails silently | Server not connected or rate limited | Check MCP status, retry after delay |
| Agent edits wrong file | Missing file organization context | Add project structure to task prompt |
| classifyHandoffIfNeeded error | Transient infrastructure bug | Respawn agent with same prompt |
| Agent stalls mid-task | Context window exhaustion | Break task into smaller pieces |
| Git conflict on commit | Multiple agents on same file | Enforce file ownership per agent |
