---
name: agent-coordination
description: Coordinate multiple specialized Skills and Task Agents through parallel, sequential, swarm, hybrid, or iterative execution strategies. CRITICAL - Skills use Skill tool (rust-code-quality, architecture-validation, plan-gap-analysis), Task Agents use Task tool (code-reviewer, test-runner, debugger, loop-agent). Use this when orchestrating multi-worker workflows, managing dependencies, or optimizing complex task execution with quality gates.
---

# Agent Coordination

Coordinate multiple specialized agents to solve complex multi-step tasks efficiently through strategic execution patterns.

## Coordination Strategies

### 1. Parallel Coordination

**Use When**: Independent tasks, no dependencies, maximize throughput

**Implementation**:
- Single message with multiple Task tool calls
- All agents start simultaneously
- Results collected and merged

**Example**:
```markdown
Task: "Review code and run tests"

├─ code-reviewer: Review code quality
└─ test-runner: Execute test suite

Execution: One message, both Task tools
```

### 2. Sequential Coordination

**Use When**: Strong dependencies, each task needs previous output

**Implementation**:
- Chain of messages, each waits for previous
- Explicit handoffs between agents
- Output of one is input to next

**Example**:
```markdown
Task: "Implement feature, test it, then review"

└─ feature-implementer: Build feature
   └─ test-runner: Test implementation
      └─ code-reviewer: Review code

Execution: Sequential messages with context transfer
```

### 3. Swarm Coordination

**Use When**: Complex problem needs multiple perspectives

**Implementation**:
- Phase 1: Parallel investigation (multiple Skills or Agents)
- Phase 2: Synthesis (combine findings)
- Phase 3: Coordinated resolution

**Example A - Skill-Based Swarm** (Analysis/Review):
```markdown
Task: "Validate v0.1.0 implementation quality"

Phase 1 [Parallel Skills]:
├─ Skill(command="rust-code-quality")
├─ Skill(command="architecture-validation")
└─ Skill(command="plan-gap-analysis")

Phase 2: Synthesize findings → identify gaps and issues
Phase 3: Create prioritized action plan
```

**Example B - Agent-Based Swarm** (Execution/Testing):
```markdown
Task: "Diagnose performance degradation"

Phase 1 [Parallel Agents]:
├─ Task(subagent_type="debugger", prompt="Profile runtime performance")
├─ Task(subagent_type="code-reviewer", prompt="Analyze code efficiency")
└─ Task(subagent_type="test-runner", prompt="Run performance benchmarks")

Phase 2: Synthesize findings → identify root cause
Phase 3: Apply coordinated fix
```

### 4. Hybrid Coordination

**Use When**: Complex workflows with mixed dependencies

**Implementation**:
- Multiple phases with different strategies
- Parallel within phases, sequential between phases
- Validation gates between phases

**Example**:
```markdown
Task: "Refactor module, update tests, verify"

Phase 1 [Parallel]: Assessment
├─ code-reviewer: Assess current code
└─ test-runner: Run existing tests

Phase 2 [Sequential]: Implementation
└─ refactorer: Apply improvements

Phase 3 [Parallel]: Validation
├─ test-runner: Verify refactored code
└─ code-reviewer: Final quality check
```

### 5. Iterative/Loop Coordination

**Use When**: Tasks require progressive refinement until criteria met

**Implementation**:
- Repeat agent execution with feedback from previous iteration
- Track progress across iterations
- Terminate when success criteria met or convergence detected
- Use loop-agent for orchestration

**Example**:
```markdown
Task: "Iteratively improve code quality until standards met"

Loop Configuration:
- Max Iterations: 5
- Success: All clippy warnings resolved + tests pass
- Agent: refactorer

Execution: loop-agent orchestrates iterations
Iteration 1: refactorer → 15 issues → Continue
Iteration 2: refactorer → 3 issues → Continue
Iteration 3: refactorer → 0 issues ✓ → Success

Use loop-agent for: test-fix-retest cycles, performance optimization loops,
progressive quality improvements, convergence-based refinement
```

## CRITICAL: Understanding Skills vs Task Agents

**There are TWO different types of workers you can coordinate:**

### Skills (invoked via `Skill` tool)
Skills are **instruction sets** that guide Claude directly. They provide specialized knowledge and workflows.

**How to invoke**: `Skill(command="skill-name")`

**Available Skills**:
- `rust-code-quality` - Comprehensive Rust code quality review
- `architecture-validation` - Validate implementation vs architecture plans
- `plan-gap-analysis` - Compare plans vs actual implementation
- `analysis-swarm` - Multi-perspective code analysis (RYAN, FLASH, SOCRATES)
- `test-fix` - Systematic test debugging and fixing
- `build-compile` - Build and compilation management
- `debug-troubleshoot` - Debug async Rust issues
- `feature-implement` - Feature implementation workflow
- `storage-sync` - Storage synchronization between Turso and redb
- `task-decomposition` - Break down complex tasks

### Task Agents (invoked via `Task` tool)
Task Agents are **autonomous sub-processes** that execute tasks independently using tools.

**How to invoke**: `Task(subagent_type="agent-name", prompt="...", description="...")`

**Available Task Agents**:

| Agent | Best For | Inputs | Outputs |
|-------|----------|--------|---------|
| **code-reviewer** | Quality, standards | Code changes | Review report, issues |
| **test-runner** | Testing, verification | Code to test | Test results, coverage |
| **feature-implementer** | New functionality | Requirements | Implementation, tests |
| **refactorer** | Code improvement | Code to refactor | Improved code |
| **debugger** | Issue diagnosis | Issue description | Root cause, fix |
| **agent-creator** | Create new agents | Agent requirements | New agent file |
| **goap-agent** | Complex multi-step tasks | Task description | Coordinated execution |
| **loop-agent** | Iterative refinement | Initial state + criteria | Refined result |
| **analysis-swarm** | Multi-perspective analysis | Code/design to analyze | Consensus analysis |

### When to Use Which?

**Use Skills when**:
- You need specialized knowledge/workflow guidance
- The task requires deep domain expertise (Rust quality, architecture validation)
- You want to follow a proven methodology
- Examples: Code quality review, gap analysis, architecture validation

**Use Task Agents when**:
- You need autonomous task execution
- The task requires tool usage (Read, Edit, Bash, etc.)
- You want parallel/independent execution
- Examples: Running tests, implementing features, debugging

### Common Coordination Patterns

**Pattern 1: Skill-Based Swarm** (for analysis tasks)
```
Phase 1 [Parallel Skills]:
├─ Skill(command="rust-code-quality")
├─ Skill(command="architecture-validation")
└─ Skill(command="plan-gap-analysis")

Phase 2: Synthesize findings
Phase 3: Create action plan
```

**Pattern 2: Agent-Based Swarm** (for execution tasks)
```
Phase 1 [Parallel Agents]:
├─ Task(subagent_type="code-reviewer", ...)
├─ Task(subagent_type="test-runner", ...)
└─ Task(subagent_type="debugger", ...)

Phase 2: Aggregate results
Phase 3: Apply fixes
```

**Pattern 3: Hybrid Coordination** (combine Skills and Agents)
```
Phase 1: Skill(command="task-decomposition")  # Plan the work
Phase 2 [Parallel Agents]:                     # Execute in parallel
├─ Task(subagent_type="feature-implementer", ...)
└─ Task(subagent_type="test-runner", ...)
Phase 3: Skill(command="rust-code-quality")   # Validate quality
```

## Coordination Workflow

### Phase 1: Strategy Selection

**Decision Matrix**:
- Independent tasks + Time-critical → **Parallel**
- Strong dependencies + Order matters → **Sequential**
- Complex problem + Multiple perspectives → **Swarm**
- Multi-phase + Mixed dependencies → **Hybrid**
- Progressive refinement + Convergence needed → **Iterative/Loop**

### Phase 2: Agent Assignment

**Match Tasks to Agents**:
1. Capability matching (does agent have required skills?)
2. Workload balancing (distribute evenly)
3. Expertise routing (specialized tasks to expert agents)

### Phase 3: Execution Planning

```markdown
## Execution Plan

### Strategy: [Parallel/Sequential/Swarm/Hybrid]

### Phase 1: [Name]
**Mode**: [Parallel/Sequential]
**Agents**:
- Agent: [name] | Task: [description] | Deps: [dependencies]

**Quality Gate**:
- [Validation criteria]

### Overall Success Criteria:
- [Criterion 1]
- [Criterion 2]
```

### Phase 4: Execution & Monitoring

**Monitoring Checklist**:
- [ ] Agent has started
- [ ] Agent is making progress
- [ ] Agent output meets quality criteria
- [ ] No errors or failures
- [ ] Completion within expected time

### Phase 5: Quality Validation

**Validation Gates** (between phases):
1. Output validation (format, completeness, quality)
2. Success criteria check (phase goals met?)
3. Error handling (can errors be recovered?)

### Phase 6: Result Synthesis

```markdown
## Execution Summary

### Completed Tasks:
- [Task 1]: ✓ [Agent] - [Outcome]

### Deliverables:
- [Item 1]: [Location/Description]

### Quality Validation:
- [Criterion 1]: ✓ Met

### Performance Metrics:
- Total time: [duration]
- Success rate: [percentage]
```

## Communication Patterns

### Agent-to-Agent Handoff

**Context Transfer**:
```markdown
Agent A completes, produces output X

Message to Agent B:
"Previous agent (A) produced X. Use this as input.
Task: [specific instructions for B]
Success criteria: [how to validate]"
```

### Synchronization Points

**Parallel Convergence**:
1. Wait for all agents to complete
2. Collect outputs from each
3. Validate each output
4. If all valid → proceed, else handle errors

**Quality Gates**:
1. Validate all outputs from phase
2. Check success criteria
3. Decision: proceed / retry / adjust / abort

## Error Handling

### Recovery Strategies

**Retry**: For transient failures (max 2-3 attempts)
**Alternative Approach**: Different agent or technical approach
**Plan Adjustment**: Remove optional tasks, simplify requirements
**Graceful Degradation**: Partial completion with documentation

### Failure Scenarios

| Scenario | Response |
|----------|----------|
| Agent reports failure | Analyze reason, retry with adjusted params or find alternative |
| Quality gate fails | Stop dependent tasks, diagnose, fix, re-execute |
| Blocked dependency | Identify blocker, work around, reorder if possible |

## Best Practices

### DO:
✓ Use **Skill tool** for analysis/review tasks (rust-code-quality, architecture-validation, plan-gap-analysis)
✓ Use **Task tool** for execution tasks (code-reviewer, test-runner, feature-implementer)
✓ Choose appropriate strategy for task dependencies
✓ Match workers (Skills/Agents) to tasks based on capabilities
✓ Validate at quality gates before proceeding
✓ Provide clear context in handoffs
✓ Monitor progress during execution
✓ Handle errors gracefully with recovery
✓ Aggregate results comprehensively

### DON'T:
✗ **Use Task tool with skill names** (e.g., Task(subagent_type="rust-code-quality") → ERROR!)
✗ **Use Skill tool with agent names** (e.g., Skill(command="code-reviewer") → May not work as expected)
✗ Force parallel execution when dependencies exist
✗ Assign tasks to inappropriate workers
✗ Skip quality validation
✗ Proceed after failed quality gates
✗ Provide insufficient context

## Coordination Metrics

### Efficiency Metrics
- **Execution Time**: Track total time and per-agent time
- **Resource Utilization**: Agents active / available
- **Throughput**: Tasks completed / time

### Quality Metrics
- **Success Rate**: Tasks successful / total (should be >95%)
- **Quality Gate Passage**: All gates should pass (100%)
- **Rework Rate**: Tasks requiring retry (should be <10%)

## Integration with GOAP Agent

The GOAP agent uses this skill as its core coordination engine:

1. Decompose task (task-decomposition skill)
2. Select coordination strategy (this skill)
3. Assign agents to tasks (this skill)
4. Execute coordination (this skill + parallel-execution skill)
5. Validate and report (this skill)

## Troubleshooting Common Errors

### Error: "Agent type 'X' not found"

**Cause**: Trying to use a **Skill name** with the **Task tool**

**Example of Error**:
```
Task(subagent_type="rust-code-quality", ...)
→ ERROR: Agent type 'rust-code-quality' not found
```

**Solution**: Use the **Skill tool** instead:
```
Skill(command="rust-code-quality")
→ SUCCESS
```

**Available Task Agents ONLY**:
- code-reviewer
- test-runner
- feature-implementer
- refactorer
- debugger
- agent-creator
- goap-agent
- loop-agent
- analysis-swarm

**Everything else is a Skill** - use `Skill(command="...")`

### Quick Reference: Which Tool to Use?

| Task Type | Tool | Example |
|-----------|------|---------|
| Rust code quality review | **Skill** | `Skill(command="rust-code-quality")` |
| Architecture validation | **Skill** | `Skill(command="architecture-validation")` |
| Plan gap analysis | **Skill** | `Skill(command="plan-gap-analysis")` |
| Multi-perspective analysis | **Skill** | `Skill(command="analysis-swarm")` |
| Run tests | **Task** | `Task(subagent_type="test-runner", ...)` |
| Review code changes | **Task** | `Task(subagent_type="code-reviewer", ...)` |
| Implement feature | **Task** | `Task(subagent_type="feature-implementer", ...)` |
| Debug issues | **Task** | `Task(subagent_type="debugger", ...)` |
| Refactor code | **Task** | `Task(subagent_type="refactorer", ...)` |
| Iterative refinement | **Task** | `Task(subagent_type="loop-agent", ...)` |

### Mnemonic
- **Skills** = Knowledge/Methodology (invoked with `Skill` tool)
- **Agents** = Autonomous Executors (invoked with `Task` tool)

## Summary

Effective agent coordination requires:
- **Right tool** (Skill vs Task) for the worker type
- **Right strategy** for the task structure
- **Right workers** (Skills/Agents) for each sub-task
- **Clear communication** and context transfer
- **Quality validation** at key checkpoints
- **Graceful error handling** and recovery
- **Comprehensive result synthesis**

Use this skill to coordinate any multi-agent workflow effectively.
