---
name: agent-workflow
description: Multi-agent development workflow system. Load when orchestrating development tasks, spawning subagents, or managing workflow phases.
allowed-tools: Read, Task, Glob
---
# Agent Workflow System

This skill provides the multi-agent workflow orchestration system.

## When to Use

Load when:
- Starting a new development task
- Spawning subagents for parallel work
- Managing workflow phase transitions
- Coordinating multi-agent collaboration

## Core Concepts

### Workflow Phases
1. REQUIREMENTS - PM gathers and clarifies user needs
2. ARCHITECTURE - Architects design solutions in parallel
3. IMPLEMENTATION - Executor manages parallel implementers
4. VERIFICATION - QA validates the implementation
5. REFLECTION - Capture learnings for evolution

### Agent Hierarchy

**Tier-1 (can spawn subagents):**
- PM - Requirements gathering
- Architect - Technical design
- Roundtable - Design synthesis
- Executor - Implementation orchestration
- QA - System verification

**Tier-2 (focused workers):**
- Explorer - Fast codebase scouting
- Implementer - Focused code writing
- Verifier - Independent verification
- Tester - Test execution
- Contract Resolver - Handle blocked tasks
- Reflector - Extract learnings
- Evolver - System improvement

## Agent Definitions

**Tier-1 Agents:**
- @.claude/agents/pm.md
- @.claude/agents/architect.md
- @.claude/agents/roundtable.md
- @.claude/agents/executor.md
- @.claude/agents/qa.md

**Tier-2 Agents:**
- @.claude/agents/explorer.md
- @.claude/agents/implementer.md
- @.claude/agents/verifier.md
- @.claude/agents/tester.md
- @.claude/agents/contract-resolver.md
- @.claude/agents/reflector.md
- @.claude/agents/evolver.md

## Spawning Pattern

### Custom Agents (Dotagent System)
Use lowercase names matching agent definitions:
```
Task(
  subagent_type: "explorer",    # Fast codebase scouting
  model: "haiku",
  prompt: "Query: ... Output: ..."
)

Task(
  subagent_type: "implementer", # Focused code writing
  model: "sonnet",
  prompt: "Task: ... Boundaries: ... Output: ..."
)

Task(
  subagent_type: "pm",          # Requirements gathering
  model: "sonnet",
  prompt: "Request: ... Output: memory/reports/demand.json"
)
```

### Built-in Agents (Claude Code)
These are different from custom agents above:
```
Task(
  subagent_type: "Explore",     # Built-in: quick codebase exploration
  model: "haiku",
  prompt: "Find all API endpoints..."
)

Task(
  subagent_type: "Plan",        # Built-in: planning agent
  model: "sonnet",
  prompt: "Plan the implementation..."
)
```

### Subagent Type Reference

| Custom (Dotagent) | Model | Purpose |
|-------------------|-------|---------|
| `pm` | sonnet | Requirements gathering |
| `architect` | opus | Technical design |
| `roundtable` | opus | Design synthesis |
| `executor` | sonnet | Implementation orchestration |
| `qa` | sonnet | System verification |
| `explorer` | haiku | Fast codebase scouting |
| `implementer` | sonnet | Focused code writing |
| `verifier` | haiku | Independent verification |
| `tester` | haiku | Test execution |
| `contract-resolver` | sonnet | Handle blocked tasks |
| `reflector` | sonnet | Extract learnings |
| `evolver` | opus | System improvement |

| Built-in (Claude Code) | Purpose |
|------------------------|---------|
| `Explore` | Quick codebase exploration |
| `Plan` | Planning and analysis |
| `general-purpose` | Flexible multi-step tasks |

## Workflow State

@workflows/main.json
@memory/state/phase.json
