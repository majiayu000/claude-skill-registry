---
name: collaboration
description: Behavioral workflows and collaboration patterns for code review, agent coordination, and branch management. Use this skill when coordinating multi-agent work, managing code review processes, completing feature branches, or resolving productive disagreements between valid approaches.
version: 1.0.0
---

# Collaboration Skill Domain

This skill domain provides behavioral workflows and collaboration patterns that enhance how agents work together, review code, and manage development processes. Unlike domain-specific technical skills (like frontend-design or test-driven-development), these workflows focus on coordination, communication, and process management.

## Why Collaboration Skills Are Separate

Collaboration skills are distinguished from domain-specific skills because they:

- **Focus on process over implementation** - Guide how to work, not what to build
- **Apply across all domains** - Code review works for frontend, backend, or any code
- **Coordinate multi-agent workflows** - Manage parallel work and agent dispatch
- **Handle behavioral patterns** - Address productive tensions and decision-making
- **Enhance existing workflows** - Layer on top of domain skills for better outcomes

## Available Workflows

### Code Review Workflows

**Request Review** (`workflows/request-review.md`)
- Dispatch code-reviewer subagent to validate implementation against requirements
- Use after completing tasks, implementing features, or before merging
- Catches issues before they cascade into larger problems

**Receive Review** (`workflows/receive-review.md`)
- Process code review feedback with technical rigor
- Use when receiving code review feedback, especially if unclear or questionable
- Ensures thoughtful implementation, not blind acceptance

### Agent Coordination Workflows

**Dispatch Parallel Agents** (`workflows/dispatch-agents.md`)
- Use multiple Claude agents to investigate and fix independent problems concurrently
- Use when facing 3+ independent failures without shared state or dependencies
- Accelerates resolution of unrelated issues

**Subagent-Driven Development** (`workflows/subagent-dev.md`)
- Execute implementation plans by dispatching fresh subagents for each task
- Use when executing plans with independent tasks, using review gates between tasks
- Maintains focus and enables parallel progress

### Development Process Workflows

**Finish Development Branch** (`workflows/finish-branch.md`)
- Complete feature development with structured options for merge, PR, or cleanup
- Use when implementation is complete, tests pass, and ready to integrate
- Provides clear decision framework for branch completion

**Preserve Productive Tensions** (`workflows/preserve-tensions.md`)
- Recognize when disagreements reveal valuable context
- Use when oscillating between equally valid approaches with different priorities
- Preserves multiple valid approaches instead of forcing premature resolution

## Workflow Selection Guide

### When You've Completed Implementation

1. **All tests passing, ready to integrate?** → Use `finish-branch.md`
2. **Want validation before proceeding?** → Use `request-review.md`
3. **Received feedback to process?** → Use `receive-review.md`

### When Managing Multiple Tasks

1. **Executing a multi-task plan?** → Use `subagent-dev.md`
2. **Multiple independent failures?** → Use `dispatch-agents.md`

### When Facing Disagreement or Uncertainty

1. **Oscillating between valid approaches?** → Use `preserve-tensions.md`
2. **Review feedback seems questionable?** → Use `receive-review.md`

## Integration with Domain Skills

Collaboration workflows complement domain-specific skills:

- **With frontend-design**: Request review after implementing UI components
- **With test-driven-development**: Use subagent-dev to implement test-first workflows
- **With any technical work**: Finish branch when feature is complete

The collaboration domain provides the "how" of working effectively, while domain skills provide the "what" of technical implementation.

## Common Patterns

### Feature Development Lifecycle

```
1. Plan feature implementation
2. Use subagent-dev to execute tasks in parallel
3. Request review after each task completion
4. Receive and process review feedback
5. Finish branch when all work is validated
```

### Parallel Investigation

```
1. Identify 3+ independent failures
2. Dispatch parallel agents to investigate each
3. Collect findings from all agents
4. Request review of proposed fixes
5. Implement validated solutions
```

### Handling Productive Disagreement

```
1. Notice oscillation between valid approaches
2. Preserve tensions to capture both perspectives
3. Document trade-offs and priorities
4. Choose approach based on current context
5. Request review to validate decision
```

## Notes

- These workflows can be combined - request review during subagent-dev
- Not all workflows apply to every situation - use judgment
- Collaboration skills enhance but don't replace technical judgment
- When in doubt, requesting review is rarely wrong
