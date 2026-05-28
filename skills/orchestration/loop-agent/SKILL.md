---
name: loop-agent
description: Execute workflow agents iteratively for refinement and progressive improvement. Use when tasks require repetitive refinement, multi-iteration improvements, progressive optimization, or feedback loops until quality criteria are met.
---

# Loop Agent Skill: Iterative Workflow Execution

Enable iterative refinement workflows through systematic loop execution with convergence detection, progress tracking, and intelligent termination.

## Quick Reference

Use loop-agent when:
- Code needs iterative refinement until quality standards met
- Tests need repeated fix-validate cycles
- Performance requires progressive optimization
- Quality improvements need multiple passes
- Feedback loops are necessary for convergence

## When to Use This Skill

### Ideal Scenarios

**Code Refinement**:
- Iterative code review → fix → review cycles
- Progressive refactoring with validation
- Quality improvement until standards met
- Incremental cleanup and optimization

**Testing & Validation**:
- Fix failures → retest → fix → retest loops
- Progressive test coverage improvement
- Iterative performance tuning
- Security hardening cycles

**Optimization**:
- Performance optimization until targets met
- Resource usage reduction iterations
- Progressive complexity reduction
- Convergence-based improvements

**Documentation & Analysis**:
- Iterative documentation enhancement
- Progressive analysis deepening
- Coverage improvement loops
- Quality refinement cycles

### NOT Appropriate For

- Single-pass tasks (use appropriate specialized agent)
- Purely parallel work with no dependencies (use parallel-execution)
- Simple linear workflows (use sequential coordination)
- One-time analysis (use appropriate analysis agent)

## Core Concepts

### Loop Termination Modes

**1. Fixed Iteration Count**
```markdown
Run exactly N iterations regardless of results
Use when: Known number of refinement passes needed
Example: "Run 3 quality improvement iterations"
```

**2. Criteria-Based Termination**
```markdown
Continue until success criteria met (with max limit)
Use when: Specific quality/performance targets exist
Example: "Optimize until response time < 100ms (max 10 iterations)"
```

**3. Convergence Detection**
```markdown
Stop when improvements become negligible
Use when: Optimal result unknown, stop at diminishing returns
Example: "Refactor until <5% quality improvement over 3 iterations"
```

**4. Hybrid Mode**
```markdown
Combine multiple termination conditions
Use when: Complex requirements with multiple stop signals
Example: "Min 2 iterations, max 15, stop when quality > 90% OR converged"
```

## Loop Planning Template

```markdown
## Loop Execution Plan: [Task Name]

### Objective
[What iterative improvement to achieve]

### Loop Configuration
- **Mode**: [Fixed / Criteria / Convergence / Hybrid]
- **Max Iterations**: [N]
- **Min Iterations**: [N] (optional)
- **Success Criteria**:
  - [ ] Criterion 1: [specific, measurable]
  - [ ] Criterion 2: [specific, measurable]
- **Convergence**: [threshold]% improvement over [N] iterations (optional)

### Agent Sequence Per Iteration
1. [Agent/Action]: [purpose]
2. [Agent/Action]: [purpose]
3. Validation: [how to measure progress]
4. Decision: [continue/stop logic]

### Success Definition
All success criteria met OR converged OR max iterations

### Progress Metrics
- [Metric 1]: [how to measure]
- [Metric 2]: [how to measure]
- [Improvement]: [how to calculate delta]
```

## Execution Patterns

### Pattern 1: Simple Refinement Loop

```markdown
Task: "Iteratively improve code quality"

Configuration:
- Max Iterations: 5
- Success: All clippy warnings resolved + rustfmt clean
- Agent: refactorer

Loop:
Iteration 1:
  - refactorer: Fix issues
  - Validate: Check clippy + rustfmt
  - Metrics: 15 warnings → Continue

Iteration 2:
  - refactorer: Fix remaining issues
  - Validate: Check clippy + rustfmt
  - Metrics: 3 warnings → Continue

Iteration 3:
  - refactorer: Final cleanup
  - Validate: Check clippy + rustfmt
  - Metrics: 0 warnings ✓ → Success (criteria met)

Result: 3 iterations, quality standards achieved
```

### Pattern 2: Test-Fix-Validate Loop

```markdown
Task: "Fix all test failures"

Configuration:
- Max Iterations: 10
- Success: 100% tests passing
- Agents: test-runner → debugger → refactorer

Loop:
Iteration 1:
  - test-runner: Run tests → 42/50 passing
  - debugger: Analyze 8 failures
  - refactorer: Apply fixes
  - test-runner: Rerun → 47/50 passing → Continue

Iteration 2:
  - test-runner: Run tests → 47/50 passing
  - debugger: Analyze 3 failures
  - refactorer: Apply fixes
  - test-runner: Rerun → 50/50 passing ✓ → Success

Result: 2 iterations, all tests passing
```

### Pattern 3: Performance Optimization Loop

```markdown
Task: "Optimize API response time"

Configuration:
- Max Iterations: 15
- Success: Response time < 50ms
- Convergence: <5% improvement over 3 iterations
- Agents: debugger (profile) → refactorer (optimize)

Loop:
Iteration 1: 320ms → Profile + optimize → 180ms (44% improvement)
Iteration 2: 180ms → Profile + optimize → 95ms (47% improvement)
Iteration 3: 95ms → Profile + optimize → 48ms (49% improvement)
→ Success (< 50ms target met)

Result: 3 iterations, 85% performance improvement
```

### Pattern 4: Multi-Agent Quality Loop

```markdown
Task: "Comprehensive quality improvement"

Configuration:
- Max Iterations: 8
- Success: All agents report "no issues" for 2 consecutive iterations
- Agents: [Parallel] code-reviewer + test-runner + debugger

Loop:
Iteration 1:
  - code-reviewer: 10 issues
  - test-runner: 5 failures
  - debugger: 2 performance issues
  - refactorer: Fix all
  → Clean count: 0 → Continue

Iteration 2:
  - code-reviewer: 2 issues
  - test-runner: 0 failures ✓
  - debugger: 0 issues ✓
  - refactorer: Fix remaining
  → Clean count: 0 → Continue

Iteration 3:
  - code-reviewer: 0 issues ✓
  - test-runner: 0 failures ✓
  - debugger: 0 issues ✓
  → Clean count: 1 → Continue (need 2 consecutive)

Iteration 4:
  - All clean again
  → Clean count: 2 → Success

Result: 4 iterations, comprehensive quality achieved
```

### Pattern 5: Convergence-Based Optimization

```markdown
Task: "Optimize until diminishing returns"

Configuration:
- Max Iterations: 20
- Convergence: <10% improvement over 3 iterations
- Metric: Code complexity score
- Agent: refactorer

Loop:
Iteration 1: Complexity 150 (baseline)
Iteration 2: Complexity 120 (20% improvement)
Iteration 3: Complexity 100 (17% improvement)
Iteration 4: Complexity 88 (12% improvement)
Iteration 5: Complexity 80 (9% improvement)
Iteration 6: Complexity 75 (6% improvement)
Iteration 7: Complexity 72 (4% improvement)

Analysis:
- Iterations 5-7: 9%, 6%, 4% improvement (average 6.3%)
- Below 10% threshold → Converged

Result: 7 iterations, stopped at diminishing returns
```

## Progress Tracking

### Iteration Tracking Table

```markdown
| Iteration | Metric 1 | Metric 2 | Improvement | Decision |
|-----------|----------|----------|-------------|----------|
| 1         | 70%      | 5/10     | baseline    | Continue |
| 2         | 82%      | 7/10     | +17%/+2     | Continue |
| 3         | 91%      | 9/10     | +11%/+2     | Success ✓|

Termination: Success criteria met at iteration 3
```

### Convergence Analysis

```markdown
## Convergence Tracking

Quality Score History: [5.0, 6.5, 7.8, 8.5, 8.9, 9.1]

Improvement per iteration:
- I1→I2: 30%
- I2→I3: 20%
- I3→I4: 9%
- I4→I5: 5%
- I5→I6: 2%

Last 3 iterations: 9%, 5%, 2% (average 5.3%)
Convergence threshold: 10%
→ Converged (diminishing returns detected)
```

## Termination Conditions

### Condition 1: Success Criteria Met

```markdown
Success Criteria:
✓ All tests passing (50/50)
✓ Code coverage > 90% (92%)
✓ No clippy warnings (0)
✓ Performance targets met (<50ms achieved)

→ STOP: All criteria satisfied (Iteration 3)
```

### Condition 2: Convergence Detected

```markdown
Convergence Configuration:
- Threshold: <10% improvement
- Window: 3 iterations

Recent improvements: 7%, 5%, 3%
Average: 5% (below 10% threshold)

→ STOP: Converged at iteration 8 (diminishing returns)
```

### Condition 3: Max Iterations Reached

```markdown
Max Iterations: 10
Current: Iteration 10

Progress:
- Started: 60% quality
- Now: 88% quality
- Target: 95% quality (not met)

→ STOP: Iteration limit reached
→ Recommendation: Consider extending limit or adjusting approach
```

### Condition 4: No Progress Detected

```markdown
Iteration 5: 10 issues
Iteration 6: 10 issues (no change)
Iteration 7: 10 issues (no change)

→ STOP: No progress for 3 iterations (stuck)
→ Recommendation: Manual intervention required
```

## Best Practices

### DO:
✓ Define clear, measurable success criteria
✓ Set reasonable max iteration limits (5-15 typical)
✓ Track metrics consistently across iterations
✓ Provide context from previous iterations to agents
✓ Validate progress after each iteration
✓ Detect convergence early (save resources)
✓ Stop when criteria met (avoid over-iteration)
✓ Document final state and improvements

### DON'T:
✗ Use loops for single-pass tasks
✗ Set very high iteration limits (>20 needs justification)
✗ Skip validation between iterations
✗ Lose context across iterations
✗ Continue after convergence (waste resources)
✗ Ignore stuck/no-progress signals
✗ Use loops when simpler patterns work
✗ Forget to define termination criteria

## Error Handling

### Agent Failure Mid-Loop

```markdown
Iteration 4: Agent fails with error

Options:
1. Retry iteration (if transient error)
2. Adjust agent parameters and retry
3. Skip to next iteration
4. Stop loop and report

Decision factors:
- Is this iteration critical?
- Can we proceed without it?
- Will the error repeat?
```

### Quality Gate Failure

```markdown
Iteration 3: Validation shows degradation

Quality: 85% → 78% (regression)

Response:
1. Analyze what went wrong
2. Revert changes from iteration 3
3. Adjust agent approach
4. Retry iteration 3 with fix
```

### Infinite Loop Prevention

```markdown
Safety Mechanisms:
1. Hard max iterations (default: 20)
2. Timeout per iteration (default: 30 min)
3. Total loop timeout (default: 4 hours)
4. No-progress detection (3 static iterations)
5. Manual stop capability

→ Prevents runaway loops
```

## Integration

### With GOAP Agent

```markdown
GOAP can use loop-agent as a phase:

Phase 1: Initial implementation (feature-implementer)
Phase 2: Iterative refinement (loop-agent)
Phase 3: Final validation (code-reviewer)
```

### With Specialized Agents

```markdown
Loop-agent coordinates agents iteratively:
- code-reviewer: Review-fix-review cycles
- test-runner: Test-fix-test loops
- refactorer: Progressive improvement
- debugger: Iterative debugging
```

### With Skills

```markdown
Use skills within loop iterations:
- rust-code-quality: For quality validation
- test-fix: For systematic test fixing
- build-compile: For build validation
```

## Quick Examples

### Example 1: Quick Quality Loop

```markdown
Task: "Fix all clippy warnings"

Loop: loop-agent
- Max: 5 iterations
- Success: 0 clippy warnings
- Agent: refactorer

Result: 3 iterations, all warnings fixed
```

### Example 2: Performance Loop

```markdown
Task: "Optimize query speed"

Loop: loop-agent
- Max: 10 iterations
- Success: <100ms OR converged (<5% improvement)
- Agents: debugger → refactorer

Result: 6 iterations, 75% faster, converged
```

### Example 3: Test Fixing Loop

```markdown
Task: "Get all tests passing"

Loop: loop-agent
- Max: 8 iterations
- Success: 100% tests pass
- Agents: test-runner → debugger → refactorer

Result: 4 iterations, 50/50 tests passing
```

## Success Metrics

### Loop Efficiency
- Average iterations to success (track over time)
- Convergence rate (how fast improvements diminish)
- Time per iteration (identify bottlenecks)

### Quality Improvement
- Initial vs final state (quantitative)
- Total improvement percentage
- Improvement per iteration (trend)

### Resource Usage
- Total time consumed
- Agent utilization per iteration
- Wasted iterations (after convergence)

## Summary

Loop Agent enables iterative refinement through:

1. **Flexible Termination**: Fixed, criteria, convergence, or hybrid modes
2. **Progress Tracking**: Monitor improvements across iterations
3. **Agent Coordination**: Execute workflows repeatedly with context
4. **Convergence Detection**: Stop at diminishing returns
5. **Quality Assurance**: Validate each iteration
6. **Error Recovery**: Handle failures within loops
7. **Resource Optimization**: Avoid unnecessary iterations

Use loop-agent when tasks benefit from iterative refinement, progressive improvement, or feedback loops until quality goals are achieved.

**Common Use Cases**:
- Code quality improvement loops
- Test-fix-validate cycles
- Performance optimization iterations
- Documentation refinement
- Progressive enhancements
- Convergence-based workflows

Transform one-shot processes into iterative excellence with systematic loop execution.
