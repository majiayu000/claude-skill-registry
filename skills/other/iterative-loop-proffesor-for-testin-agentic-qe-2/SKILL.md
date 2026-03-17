---
name: "Iterative Loop"
description: "Implement continuous AI iteration loops for complex development tasks. Use when building features requiring test-driven refinement, implementing tasks with clear success criteria, or automating iterative improvement workflows. Based on the Ralph Wiggum technique from Claude Code plugins."
---

# Iterative Loop

## Overview

The Iterative Loop skill implements **continuous AI-driven development loops** that persist until completion criteria are met. Inspired by the Ralph Wiggum technique, this approach enables autonomous, self-correcting development cycles where the AI sees its previous work in files and git history, iteratively improving until success.

## Core Philosophy

1. **Iteration > Perfection** - Don't aim for perfect on first try; let the loop refine the work
2. **Failures Are Data** - Each failure provides information to improve the next attempt
3. **Clear Criteria** - Success must be objectively measurable (tests, metrics, validations)
4. **Persistence Wins** - Keep trying until success; the loop handles retry logic automatically

## Prerequisites

- Claude Code with session management
- Clear completion criteria (tests, linting, metrics)
- Version control (git) for tracking iterations

---

## Quick Start

### Basic Iterative Development Pattern

```bash
# Define task with clear completion criteria
TASK="Implement user authentication with JWT.
Success criteria:
- All unit tests pass
- Integration tests pass
- No TypeScript errors
- Security audit passes
Output <promise>COMPLETE</promise> when all criteria met."

# Execute iterative loop (conceptual)
while ! task_complete; do
  claude_execute "$TASK"
  check_completion_criteria
done
```

### AQE v3 Integration Example

```bash
# Using claude-flow hooks for iterative task
npx @claude-flow/cli@latest hooks pre-task --description "Implement auth with iteration" --taskId "auth-impl"

# Store iteration state in memory
npx @claude-flow/cli@latest memory store \
  --key "iteration-auth" \
  --value '{"iteration": 1, "maxIterations": 20, "criteria": "all tests pass"}' \
  --namespace iterations
```

---

## Step-by-Step Guide

### Step 1: Define Clear Success Criteria

**Essential**: Every iterative task MUST have objectively measurable completion criteria.

**Good Criteria Examples:**
```markdown
✅ All unit tests pass (npm test returns exit code 0)
✅ Coverage > 80% (coverage report shows 80%+)
✅ No TypeScript errors (tsc --noEmit returns 0)
✅ Linting passes (eslint returns 0)
✅ Performance < 100ms (benchmark shows < 100ms)
```

**Bad Criteria Examples:**
```markdown
❌ "Code looks good" (subjective)
❌ "Works properly" (undefined)
❌ "Well-structured" (no measurable check)
```

### Step 2: Structure the Task with Phases

Break complex tasks into incremental phases:

```markdown
## Task: Implement User Authentication

### Phase 1: Data Layer
- Create User model with Prisma schema
- Write migration
- Run tests: `npm test -- --grep "User model"`
- Criteria: Model tests pass

### Phase 2: Service Layer
- Implement AuthService with JWT
- Add token generation/validation
- Run tests: `npm test -- --grep "AuthService"`
- Criteria: Service tests pass

### Phase 3: API Layer
- Create /auth/login endpoint
- Create /auth/register endpoint
- Run tests: `npm test -- --grep "auth API"`
- Criteria: API tests pass

### Phase 4: Integration
- End-to-end authentication flow
- Run tests: `npm test`
- Criteria: ALL tests pass

Output <promise>AUTH_COMPLETE</promise> when Phase 4 passes.
```

### Step 3: Implement Safety Mechanisms

Always include escape conditions:

```markdown
## Safety Rules

1. **Max Iterations**: Stop after 20 attempts
2. **Stuck Detection**: After 5 iterations without progress:
   - Document what's blocking
   - List attempted approaches
   - Suggest alternative strategies
3. **Critical Errors**: Stop immediately if:
   - Database corruption detected
   - Security vulnerability introduced
   - Breaking changes to existing features
```

### Step 4: Execute with Verification

Each iteration should:
1. Make targeted changes
2. Run verification (tests, lint, build)
3. Analyze results
4. Plan next iteration based on feedback

```bash
# Iteration pattern
1. Read previous state (files, git log)
2. Identify remaining work
3. Implement specific change
4. Run verification suite
5. If all pass -> output completion promise
6. If failures -> analyze and continue iteration
```

---

## Iterative Patterns

### Pattern 1: Test-Driven Iteration

```markdown
## TDD Iteration Task

1. Write failing test for [feature]
2. Implement minimal code to pass test
3. Run `npm test`
4. If test fails -> debug and fix implementation
5. If test passes -> check if more tests needed
6. Repeat until all acceptance tests pass
7. Refactor if needed
8. Output <promise>TDD_COMPLETE</promise>
```

### Pattern 2: Bug Fix Iteration

```markdown
## Bug Fix Task

1. Write failing test that reproduces bug
2. Implement fix
3. Run test suite
4. If reproduction test fails -> analyze why fix didn't work
5. If other tests fail -> fix regressions
6. If all tests pass -> output <promise>BUG_FIXED</promise>

Max iterations: 10
After 5 iterations without fix:
- Document root cause analysis
- Suggest alternative approaches
```

### Pattern 3: Coverage Improvement Iteration

```markdown
## Coverage Improvement Task

Target: 80% line coverage

1. Run coverage analysis
2. Identify uncovered code paths
3. Write test for highest-impact uncovered path
4. Run tests with coverage
5. If coverage >= 80% -> output <promise>COVERAGE_ACHIEVED</promise>
6. If coverage < 80% -> continue iteration

Max iterations: 30
Progress check: If coverage doesn't improve for 3 iterations -> analyze blockers
```

### Pattern 4: Performance Optimization Iteration

```markdown
## Performance Optimization Task

Target: Response time < 100ms

1. Run performance benchmark
2. Identify slowest operation
3. Implement optimization
4. Run benchmark again
5. If target met -> output <promise>PERF_TARGET_MET</promise>
6. If not improved -> try different approach

Max iterations: 15
Record metrics each iteration for trend analysis
```

---

## Integration with Claude Flow

### Memory-Enhanced Iteration

```bash
# Store iteration state
npx @claude-flow/cli@latest memory store \
  --key "current-iteration" \
  --value '{"task": "auth", "iteration": 5, "lastResult": "2 tests failing"}' \
  --namespace iterations

# Search for similar past iterations
npx @claude-flow/cli@latest memory search \
  --query "auth implementation" \
  --namespace iterations

# Learn from successful completions
npx @claude-flow/cli@latest hooks post-task \
  --taskId "auth-impl" \
  --success true \
  --quality 0.9
```

### Swarm-Coordinated Iteration

For complex tasks, use multiple agents iterating in parallel:

```bash
# Initialize swarm for parallel iteration
npx @claude-flow/cli@latest swarm init --topology mesh --max-agents 5

# Spawn specialized iterators
Task("Iterate on unit tests", "Fix failing unit tests until all pass", "tester")
Task("Iterate on integration", "Fix integration tests until all pass", "tester")
Task("Iterate on performance", "Optimize until benchmarks pass", "performance-engineer")
```

---

## Best Practices

### Prompt Engineering for Iteration

**Include:**
- Explicit completion criteria with verification commands
- Phase-based breakdown for complex tasks
- Safety limits (max iterations)
- Progress tracking instructions
- Stuck detection and recovery procedures

**Example Well-Structured Prompt:**
```markdown
## Task: Implement Feature X

### Success Criteria (ALL must pass):
1. `npm test` exits with code 0
2. `npm run lint` exits with code 0
3. `npm run typecheck` exits with code 0
4. No console.log statements in production code

### Phases:
1. Write failing tests
2. Implement feature
3. Fix any failures
4. Clean up and refactor

### Safety:
- Max iterations: 20
- After 10 iterations: summarize blockers
- Stop if security issues detected

### Completion:
When ALL success criteria pass, output:
<promise>FEATURE_X_COMPLETE</promise>
```

### When to Use Iterative Loops

**Ideal for:**
- Well-defined tasks with measurable success
- Test-driven development
- Bug fixing with reproducible tests
- Coverage improvement
- Performance optimization
- Linting/formatting fixes

**Not ideal for:**
- Tasks requiring human judgment
- Design decisions
- Vague or subjective goals
- One-time operations
- Production debugging without tests

---

## Troubleshooting

### Issue: Infinite Loop / No Progress

**Symptoms**: Same errors repeat without improvement

**Solutions**:
1. Increase specificity in completion criteria
2. Add "stuck detection" with alternative approaches
3. Lower max iterations
4. Break task into smaller phases

### Issue: False Completion

**Symptoms**: Loop ends but task not actually complete

**Solutions**:
1. Add more verification commands
2. Make completion criteria more explicit
3. Add integration tests alongside unit tests

### Issue: Regression in Later Iterations

**Symptoms**: Previously passing tests fail after new changes

**Solutions**:
1. Add regression check step
2. Use git to compare iterations
3. Implement smaller, targeted changes

---

## Related Skills

- [tdd-london-chicago](../tdd-london-chicago/) - TDD approaches for iterative development
- [qe-iterative-loop](../qe-iterative-loop/) - AQE v3 fleet-specific iteration patterns
- [hooks-automation](../hooks-automation/) - Claude Flow hooks for automation

## Resources

- [Ralph Wiggum Technique](https://ghuntley.com/ralph/) - Original methodology
- [Ralph Orchestrator](https://github.com/mikeyobrien/ralph-orchestrator) - Orchestration tools
- [Claude Code Plugins](https://github.com/anthropics/claude-code) - Official plugins

---

**Origin**: Based on Ralph Wiggum plugin from claude-code repository (anthropics/claude-code)
**Adapted for**: Agentic QE v3 with Claude Flow integration
