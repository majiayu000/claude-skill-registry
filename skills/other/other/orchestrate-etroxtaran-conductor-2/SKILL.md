---
name: orchestrate
tags:
  technology: [python]
  feature: [workflow]
  priority: critical
summary: Coordinate multi-agent workflow through all phases
version: 1
---

# Orchestrate

## When to use

- Running the full Conductor workflow
- Coordinating between multiple agents
- Managing phase transitions

## Workflow Phases

1. **Discovery**: Understand requirements
2. **Planning**: Create task breakdown
3. **Validation**: Review plan with agents
4. **Implementation**: Execute tasks (TDD)
5. **Verification**: Verify all tests pass

## Instructions

### Phase 1: Discovery
- Run `/discover` skill
- Summarize requirements
- Identify gaps

### Phase 2: Planning
- Run `/plan` skill
- Create task breakdown
- Define dependencies

### Phase 3: Validation
- Request reviews from agents
- Check thresholds (score >= 6.0)
- Address blocking issues

### Phase 4: Implementation
- Execute tasks in dependency order
- Use TDD approach
- Record progress

### Phase 5: Verification
- Run all tests
- Collect agent approvals (score >= 7.0)
- Document completion

## State Management

Store state in SurrealDB:
- Current phase
- Task status
- Agent responses
- Blocking issues

## Commands

```bash
# Start workflow
python -m orchestrator --project <name> --start

# Check status
python -m orchestrator --project <name> --status

# Resume
python -m orchestrator --project <name> --resume
```
