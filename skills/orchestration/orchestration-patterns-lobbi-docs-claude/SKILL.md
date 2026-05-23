---
name: Orchestration Patterns
description: This skill should be used when the user asks about "orchestration patterns", "plan-then-execute", "hierarchical decomposition", "blackboard pattern", "event sourcing pattern", "which pattern to use", "parallel execution strategies", or needs to select an orchestration approach for complex multi-agent tasks. Provides comprehensive guidance on 4 orchestration patterns for coordinating multiple agents.
version: 1.0.0
---

# Orchestration Patterns

Establish the appropriate multi-agent coordination strategy by selecting from four proven orchestration patterns based on task characteristics and requirements.

## Pattern Selection Framework

Choose the orchestration pattern based on task complexity and coordination needs:

| Pattern | Best For | Parallelism | State Management |
|---------|----------|-------------|------------------|
| **Plan-then-Execute** | Well-defined tasks with clear steps | Level-based | Centralized |
| **Hierarchical Decomposition** | Complex objectives requiring breakdown | Bottom-up aggregation | Tree-structured |
| **Blackboard** | Collaborative problem-solving | Concurrent contributions | Shared knowledge space |
| **Event Sourcing** | Audit trails and replay capability | Event-driven | Append-only log |

## Pattern 1: Plan-then-Execute (P-t-E)

The most common pattern for structured, multi-phase work. Generate a comprehensive plan, validate it, then execute systematically.

### When to Use
- Tasks with clear, predictable phases
- Requirements are well-defined upfront
- Need for validation before execution
- Standard software development workflows

### Execution Flow
1. **Strategic Planning**: Use master-strategist to analyze requirements
2. **Plan Validation**: Security, compliance, and architecture review
3. **DAG Generation**: Convert plan to directed acyclic graph
4. **Parallel Execution**: Execute independent nodes concurrently
5. **Checkpoint Creation**: Save state at each phase boundary
6. **Dynamic Re-planning**: Adapt when blockers encountered

### Implementation
```
Phase 1: EXPLORE (2+ agents) → Analysis, research, context gathering
Phase 2: PLAN (1-2 agents) → Strategy, architecture, task breakdown
Phase 3: CODE (2-4 agents) → Implementation, parallel development
Phase 4: TEST (2-3 agents) → Unit, integration, E2E testing
Phase 5: FIX (1-2 agents) → Bug fixes, refinements
Phase 6: DOCUMENT (1-2 agents) → Documentation, knowledge transfer
```

## Pattern 2: Hierarchical Decomposition

Recursively break down complex objectives into atomic, executable tasks with clear ownership.

### When to Use
- Large, complex objectives
- Multiple independent workstreams
- Need for parallel team-like execution
- Tasks with natural hierarchical structure

### Decomposition Strategy
1. **Root Task**: High-level objective
2. **Level 1**: Major components (max 5-7 subtasks)
3. **Level 2**: Detailed features (max 5-7 per parent)
4. **Level 3**: Implementation tasks (max 5-7 per parent)
5. **Level 4-5**: Atomic tasks (executable by single agent)

### Depth Limits
- Maximum decomposition depth: 5 levels
- Maximum subtasks per node: 7
- Minimum agents for leaf execution: 1

### Aggregation
- Bottom-up result collection
- Automatic parallelization at each level
- Parent waits for all children before completing

## Pattern 3: Blackboard

Shared knowledge space where multiple agents contribute specialized knowledge collaboratively.

### When to Use
- Complex problems requiring diverse expertise
- No predetermined solution path
- Emergent solutions from collaboration
- Knowledge synthesis across domains

### Components
1. **Blackboard**: Shared data structure with current problem state
2. **Knowledge Sources**: Specialized agents contributing expertise
3. **Control Shell**: Orchestrator determining contribution order

### Implementation
```
Blackboard State:
├── problem_description: string
├── hypotheses: Hypothesis[]
├── partial_solutions: Solution[]
├── constraints: Constraint[]
└── contributions: Contribution[]
```

### Collaboration Flow
1. Initialize blackboard with problem description
2. Knowledge sources monitor blackboard for relevance
3. Agents contribute when they can add value
4. Control shell mediates conflicts
5. Solution emerges from accumulated knowledge

## Pattern 4: Event Sourcing

Event-driven task coordination with complete audit trail and replay capability.

### When to Use
- Audit requirements (SOC2, compliance)
- Need for time-travel debugging
- Replay and recovery scenarios
- Complex state reconstruction needs

### Event Types
```typescript
interface OrchestrationEvent {
  id: string;
  type: 'AgentSpawned' | 'PhaseTransition' | 'Checkpoint' | 'Error' | 'Recovery';
  timestamp: number;
  agentId?: string;
  payload: any;
}
```

### Event Store
- Append-only log (no mutations)
- Events are immutable facts
- State reconstructed from event replay
- Support for temporal queries

### Recovery Capabilities
- Reconstruct any historical state
- Replay from any checkpoint
- Debug by examining event sequence
- Automatic state recovery on failure

## Pattern Combinations

Combine patterns for complex scenarios:

### P-t-E + Hierarchical
Use Plan-then-Execute at the top level with Hierarchical Decomposition for implementation phases.

### Blackboard + Event Sourcing
Shared knowledge space with complete audit trail of contributions.

## Agent Layer Mapping

Map agents to appropriate layers based on pattern:

| Layer | P-t-E Role | Hierarchical Role | Blackboard Role |
|-------|------------|-------------------|-----------------|
| **Strategic** | Plan generation | Root decomposition | Problem framing |
| **Tactical** | DAG scheduling | Level coordination | Contribution selection |
| **Operational** | Task execution | Leaf implementation | Knowledge contribution |
| **Quality** | Validation gates | Aggregation verification | Solution validation |

## Additional Resources

### Reference Files
- **`references/pattern-details.md`** - Detailed implementation guides for each pattern
- **`references/pattern-selection.md`** - Decision tree for pattern selection

### Examples
- **`examples/plan-execute-dag.json`** - Sample DAG for P-t-E pattern
- **`examples/hierarchical-tree.json`** - Sample decomposition tree
