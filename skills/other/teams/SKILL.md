---
name: teams
description: |
  Agent Teams orchestration for multi-instance parallel work. Use when:
  - User mentions "use teams", "parallel agents", "split work", "fan out"
  - Task has 3+ independent workstreams
  - Large-scale refactoring across unrelated files
  - User says "divide and conquer", "multi-instance"
context: fork
agent: maestro
---

# Agent Teams Orchestration

Delegates to the Maestro agent for coordinating multiple independent Claude Code instances.

## When to Use Teams

| Scenario | Teams? | Why |
|----------|--------|-----|
| 3+ independent file areas | Yes | Maximum parallelism |
| Frontend + Backend + Tests | Yes | No file conflicts |
| Sequential dependent work | No | Use subagents instead |
| Quick single investigation | No | Overhead not worth it |
| Large codebase analysis | Yes | Independent context per agent |
| Competing approaches | Yes | Explore in parallel |

## Prerequisites

- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS: "1"` must be set (enabled by default in cc-settings)
- For split panes: tmux or iTerm2 recommended

## Output

Report: team composition, task assignments, coordination strategy, and progress.
