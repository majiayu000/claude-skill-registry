---
name: agent-run-orchestrator
description: "Run section orchestrators to coordinate multi-component workflows. Use when starting work on a section."
mcp_fallback: none
category: agent
user-invocable: false
---

# Run Orchestrator

Invoke section orchestrators to coordinate complex development workflows.

## When to Use

- Starting work on new section
- Coordinating multiple parallel components
- Managing complex workflows
- Need hierarchical task coordination

## Quick Reference

```bash
# Run orchestrator for section
./scripts/run_orchestrator.sh foundation

# Monitor section progress
./scripts/monitor_section_progress.sh
```

## Orchestrator Workflow

1. **Review Plans** - Understand section specifications
2. **Break Down** - Divide into manageable components
3. **Delegate** - Assign to appropriate design/specialist agents
4. **Monitor** - Track progress and blockers
5. **Integrate** - Coordinate results
6. **Escalate** - Handle blocking issues

## Hierarchy

```text
Section Orchestrator (L1)
  ↓ delegates to
Module Design Agent (L2)
  ↓ delegates to
Component Specialist (L3)
  ↓ delegates to
Implementation Engineer (L4)
```

## Orchestrator Levels

**L0**: Chief Architect - Strategic architecture decisions

**L1**: Section Orchestrators

- Foundation Orchestrator
- Shared Library Orchestrator
- Tooling Orchestrator
- Paper Implementation Orchestrator
- CI/CD Orchestrator
- Agentic Workflows Orchestrator

**L2**: Module Design Agents - Coordinate modules within sections

## Agent Hierarchy Context

Orchestrators are the coordination hub between high-level planning and implementation teams.
They decompose work from section level to component level, enabling parallel development.

## References

- `/agents/hierarchy.md` - Complete orchestrator structure
- `/agents/delegation-rules.md` - Coordination patterns
- `.claude/agents/` - Orchestrator configurations
