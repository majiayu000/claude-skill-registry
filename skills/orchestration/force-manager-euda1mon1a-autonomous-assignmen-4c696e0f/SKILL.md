---
name: force-manager
description: Invoke FORCE_MANAGER for task force assembly and team composition decisions. Use when complex tasks require coordinated multi-agent teams with proper staffing and lifecycle management.
model_tier: sonnet
parallel_hints:
  can_parallel_with: [roster-party, signal-party, context-party]
  must_serialize_with: [safe-schedule-generation, swap-execution]
  preferred_batch_size: 1
context_hints:
  max_file_context: 25
  compression_level: 1
  requires_git_context: true
  requires_db_context: false
escalation_triggers:
  - pattern: "cross-domain"
    reason: "Task forces spanning 3+ coordinator domains require ORCHESTRATOR coordination"
  - keyword: ["capacity exceeded", "overutilization", "resource conflict"]
    reason: "Utilization violations and priority conflicts need escalation"
---

# Force Manager Skill

Task force assembly and lifecycle management specialist. Serves as ORCHESTRATOR's "personnel action officer" - translating high-level objectives into properly staffed, coordinated teams.

## When This Skill Activates

- Complex multi-agent tasks requiring team assembly
- Team composition decisions for coordinated work
- Resource allocation and workload balancing
- Coordinator assignment for task forces
- Lifecycle management of active task forces
- Organizational pattern recognition

## Purpose

FORCE_MANAGER assembles agents into task forces, assigns them to coordinators, and manages task force lifecycles. This agent ensures:
- Right agents for each mission (capability matching)
- Proper coordinator assignment (domain alignment)
- Balanced utilization (no agent overload)
- Lifecycle tracking (activation → operation → deactivation)

**Key Insight:** The right team for the mission - no more, no less.

## Reports To

- **SYNTHESIZER** (Special Staff - Team Assembly)
- Receives mission objectives from ORCHESTRATOR
- Returns task force compositions and assignments

## Agent Identity

Loads: `/home/user/Autonomous-Assignment-Program-Manager/.claude/Agents/FORCE_MANAGER.md`

## Key Workflows

### Workflow 1: Task Force Assembly

```
INPUT: Mission objective + capability requirements
OUTPUT: Assembled task force with coordinator assignment

1. Parse required capabilities
2. Query G1_PERSONNEL for available agents
3. Score agents against requirements:
   - Skill match (40%)
   - Current utilization (30%)
   - Past performance (20%)
   - Model tier efficiency (10%)
4. Select optimal agent mix
5. Identify appropriate coordinator
6. Prepare assignment package
```

### Workflow 2: Coordinator Assignment

```
INPUT: Assembled task force
OUTPUT: Active task force under coordinator command

1. Verify coordinator availability
2. Prepare handoff package with complete context
3. Transfer context with absolute file paths
4. Activate task force (update lifecycle state)
5. Monitor handoff confirmation
6. Report activation to ORCHESTRATOR
```

### Workflow 3: Lifecycle Management

```
States:
  PENDING   → Assembled, awaiting activation
  ACTIVATED → Running under coordinator
  OPERATING → Mid-execution with checkpoints
  COMPLETED → Mission achieved
  FAILED    → Mission failed, requires analysis
  DEACTIVATED → Resources released

Track transitions and manage timeouts
```

### Workflow 4: Parallelization Domain Scoring

**Scoring Matrix:**
| Factor | Weight | High (3) | Medium (2) | Low (1) |
|--------|--------|----------|------------|---------|
| Domain Independence | 3x | Fully independent | Some coupling | Tightly coupled |
| Data Dependencies | 2x | None | One-way | Bidirectional |
| File Overlap | 2x | No overlap | Different dirs | Same dir |
| Serialization Points | 1x | None | One | Multiple |

**Grades:**
- 20-24: HIGH → Spawn all domains in parallel
- 14-19: MEDIUM → Phase some work
- 8-13: LOW → Serialize most work
- 0-7: MINIMAL → Near-sequential

## Integration with Other Skills

### With roster-party
**Coordination:** Use roster-party for comprehensive capability analysis before assembly
```
1. FORCE_MANAGER receives complex mission
2. FORCE_MANAGER spawns roster-party for G-1 analysis
3. roster-party provides agent capabilities, utilization, availability
4. FORCE_MANAGER uses data for task force composition
```

### With qa-party
**Coordination:** FORCE_MANAGER may assemble task forces that use qa-party
```
1. FORCE_MANAGER assembles development task force
2. Task force completes implementation
3. qa-party validates results in parallel
```

## Utilization Management

### Capacity Rules

- **Maximum utilization:** 80% per agent
- **Warning threshold:** 75% utilization
- **Query G1_PERSONNEL** before every assignment
- **Balance workload** across available agents

### Conflict Resolution

When multiple missions need same agent:
1. Flag resource conflict immediately
2. Present trade-off analysis to ORCHESTRATOR
3. Await priority decision
4. Document resolution

## Output Format

### Task Force Assembly Report

```markdown
## Task Force Assembly Report

### Mission
[Restated objective]

### Task Force Composition
| Agent | Role | Archetype | Model Tier | Rationale |
|-------|------|-----------|------------|-----------|
| [name] | [role] | [type] | [tier] | [why selected] |

### Coordinator Assignment
**Assigned To**: [COORD_X]
**Rationale**: [why this coordinator]
**Alternative**: [backup if primary unavailable]

### Lifecycle Plan
- **Activation**: [trigger condition]
- **Duration**: [estimated time]
- **Checkpoints**: [milestone points]
- **Deactivation**: [completion criteria]

### Resource Analysis
- **Total Agents**: [count]
- **Utilization Impact**: [capacity effect]
- **Risk Level**: [low/medium/high]

### Recommendations
[Any organizational patterns observed]
```

## Aliases

- `/force` - Quick invocation for team assembly
- `/team-assembly` - Explicit team composition task

## Usage Examples

### Example 1: End-to-End Feature Implementation
```
Use the force-manager skill to assemble a task force for implementing
swap auto-cancellation feature end-to-end.

Required capabilities:
- Database schema design
- Service layer implementation
- ACGME compliance validation
- Test coverage (unit + integration)
- API documentation

Constraints:
- Maximum 5 agents
- Model tier budget: 4 sonnet, 1 opus
- No frontend changes

Return: Task force composition and coordinator assignment.
```

### Example 2: Cross-Domain Task Force
```
Use the force-manager skill to assemble a team for resilience
framework enhancements spanning multiple domains.

Required capabilities:
- Resilience metric calculation
- Schedule analysis
- Frontend dashboard updates
- Documentation updates

This is a cross-domain task. Determine if single coordinator can
manage or if ad-hoc task force is needed.
```

### Example 3: Capacity Check
```
Use the force-manager skill to check if we have capacity for a
new P1 task without overloading any agents.

Task: Schedule validation improvements
Estimated effort: 2-3 agents for 4 hours

Query G1_PERSONNEL for current utilization and availability.
```

## Common Failure Modes

| Failure Mode | Symptom | Recovery |
|--------------|---------|----------|
| **Capability Gap** | Missing critical skill | Request additional agent from G1_PERSONNEL; escalate if unavailable |
| **Utilization Overload** | Agent assigned at/near 80% | Remove agent; find alternative; escalate if no capacity |
| **Context Loss in Handoff** | Agents report missing context | Issue corrected handoff with complete context; update template |
| **Coordinator Mismatch** | Wrong domain assignment | Reassign to correct coordinator; document correct routing |
| **Resource Conflicts** | Multiple missions want same agent | Present conflict to ORCHESTRATOR with trade-off analysis |

## Escalation Rules

| Situation | Escalate To | Reason |
|-----------|-------------|--------|
| Cross-domain task force (3+ domains) | ORCHESTRATOR | Coordination complexity |
| Resource conflict between missions | ORCHESTRATOR | Priority decision needed |
| Agent utilization would exceed 80% | ORCHESTRATOR | Capacity approval |
| Organizational pattern recommendation | ORCHESTRATOR + ARCHITECT | Structural change |
| Mission cannot be staffed | ORCHESTRATOR | Scope/resource mismatch |

## Quality Checklist

Before completing task force assembly:

- [ ] All required capabilities covered
- [ ] No agent exceeds 80% utilization
- [ ] Coordinator appropriate for domain
- [ ] Handoff package complete with context
- [ ] Success criteria measurable
- [ ] Timeline realistic for scope
- [ ] Escalation path defined
- [ ] Lifecycle plan documented

## Context Isolation Awareness

**CRITICAL:** Spawned agents have isolated context windows. When delegating to FORCE_MANAGER:

- Provide complete mission context
- Include all file paths (absolute)
- List available agents with utilization
- Specify constraints explicitly
- Include prior decisions from ORCHESTRATOR

**Handoff packages must be self-contained** - agents don't inherit parent context.

## References

- Agent roster: Consult G1_PERSONNEL
- Coordinator specs: `.claude/Agents/COORD_*.md`
- Agent factory patterns: `.claude/Agents/AGENT_FACTORY.md`
- Delegation patterns: `.claude/dontreadme/synthesis/PATTERNS.md`

---

*"The right team for the mission. Every agent counts, every role matters."*
