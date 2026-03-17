---
name: agent-organizer
description: Expert in designing, orchestrating, and managing multi-agent systems (MAS). Specializes in agent collaboration patterns, hierarchical structures, and swarm intelligence. Use when building agent teams, designing agent communication, or orchestrating autonomous workflows.
---

# Agent Organizer

## Purpose
Provides expertise in multi-agent system architecture, coordination patterns, and autonomous workflow design. Handles agent decomposition, communication protocols, and collaboration strategies for complex AI systems.

## When to Use
- Designing multi-agent architectures or agent teams
- Implementing agent-to-agent communication protocols
- Building hierarchical or swarm-based agent systems
- Orchestrating autonomous workflows across agents
- Debugging agent coordination failures
- Scaling agent systems for production
- Designing agent memory sharing strategies

## Quick Start
**Invoke this skill when:**
- Designing multi-agent architectures or agent teams
- Implementing agent-to-agent communication protocols
- Building hierarchical or swarm-based agent systems
- Orchestrating autonomous workflows across agents
- Scaling agent systems for production

**Do NOT invoke when:**
- Building single-agent LLM applications (use ai-engineer)
- Optimizing prompts for individual agents (use prompt-engineer)
- Managing agent context windows (use context-manager)
- Handling agent failures and recovery (use error-coordinator)

## Decision Framework
```
Agent System Design:
├── Single task, no coordination → Single agent
├── Parallel independent tasks → Worker pool pattern
├── Sequential dependent tasks → Pipeline pattern
├── Complex interdependent tasks
│   ├── Clear hierarchy → Hierarchical orchestration
│   ├── Peer collaboration → Swarm/consensus pattern
│   └── Dynamic roles → Adaptive agent mesh
└── Human-in-the-loop → Supervisor pattern
```

## Core Workflows

### 1. Agent Team Design
1. Decompose problem into agent responsibilities
2. Define agent capabilities and interfaces
3. Design communication topology (hub, mesh, hierarchy)
4. Implement coordination protocol
5. Add monitoring and observability
6. Test failure scenarios

### 2. Agent Communication Setup
1. Choose message format (structured, natural language, hybrid)
2. Define message routing strategy
3. Implement handoff protocols
4. Add retry and timeout handling
5. Log all inter-agent messages

### 3. Scaling Agent Systems
1. Profile bottlenecks in current architecture
2. Identify parallelization opportunities
3. Implement load balancing across agents
4. Add agent pooling for burst capacity
5. Monitor resource utilization per agent

## Best Practices
- Keep agent responsibilities single-purpose and well-defined
- Use explicit handoff protocols between agents
- Implement circuit breakers for failing agents
- Log all inter-agent communication for debugging
- Design for graceful degradation when agents fail
- Version agent interfaces for backward compatibility

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| God agent | Single agent doing everything | Decompose into specialized agents |
| Chatty agents | Excessive inter-agent messages | Batch communications, async where possible |
| Tight coupling | Agents depend on internal state | Use contracts and interfaces |
| No supervision | Agents run without oversight | Add supervisor or human-in-loop |
| Shared mutable state | Race conditions and conflicts | Use message passing or event sourcing |
