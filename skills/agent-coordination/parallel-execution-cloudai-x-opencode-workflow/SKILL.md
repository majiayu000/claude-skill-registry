---
name: parallel-execution
description: CRITICAL skill for executing multiple Task tool calls in a SINGLE message for true parallelism. Essential for efficient multi-task workflows, subagent coordination, and maximizing throughput.
license: MIT
compatibility: opencode
metadata:
  category: workflow
  audience: agents
---

# Parallel Execution

**CRITICAL**: This skill teaches how to execute multiple tasks simultaneously for maximum efficiency.

## The Fundamental Rule

> **ALL Task calls MUST be in a SINGLE assistant message for true parallelism.**

If Task calls are in separate messages, they run SEQUENTIALLY, not in parallel.

---

## Why Parallel Execution Matters

### Sequential (SLOW - AVOID)

```
Message 1: Start Task A
           ↓ wait for completion
Message 2: Start Task B
           ↓ wait for completion
Message 3: Start Task C
           ↓ wait for completion

Total time = A + B + C = 90 seconds (if each takes 30s)
```

### Parallel (FAST - USE THIS)

```
Message 1: Start Task A ─┐
           Start Task B ─┼─ All run simultaneously
           Start Task C ─┘

Total time ≈ max(A, B, C) = 30 seconds
```

**Speedup: 3x faster with 3 parallel tasks**

---

## How to Execute in Parallel

### Step 1: Identify Independent Tasks

Tasks are independent when:
- They don't depend on each other's output
- They don't modify the same files
- They can run in any order

### Step 2: Launch ALL Tasks in ONE Message

```xml
<!-- CORRECT: All tasks in single message = PARALLEL -->
<task>
  <description>Analyze authentication module</description>
  <prompt>Review src/auth for security patterns...</prompt>
</task>

<task>
  <description>Analyze API layer</description>
  <prompt>Review src/api for REST best practices...</prompt>
</task>

<task>
  <description>Analyze database layer</description>
  <prompt>Review src/db for query optimization...</prompt>
</task>
```

### Step 3: Collect and Synthesize Results

After all tasks complete, combine their findings into a unified response.

---

## Parallelization Patterns

### Pattern 1: Task-Based Parallelization

When you have N independent tasks, spawn N subagents:

```
Implementation Plan:
1. Implement auth module
2. Create API endpoints
3. Add database schema
4. Write unit tests
5. Update documentation

Launch 5 parallel subagents:
├─ Subagent 1: Implement auth module
├─ Subagent 2: Create API endpoints
├─ Subagent 3: Add database schema
├─ Subagent 4: Write unit tests
└─ Subagent 5: Update documentation
```

**All 5 in ONE message!**

### Pattern 2: Directory-Based Parallelization

Analyze different directories simultaneously:

```
Codebase Structure:
├── src/auth/
├── src/api/
├── src/db/
└── src/ui/

Launch 4 parallel subagents:
├─ Subagent 1: Analyze src/auth
├─ Subagent 2: Analyze src/api
├─ Subagent 3: Analyze src/db
└─ Subagent 4: Analyze src/ui
```

### Pattern 3: Perspective-Based Parallelization

Review from multiple angles at once:

```
Code Review Perspectives:
- Security vulnerabilities
- Performance bottlenecks
- Test coverage gaps
- Architecture patterns

Launch 4 parallel subagents:
├─ Subagent 1: Security review
├─ Subagent 2: Performance analysis
├─ Subagent 3: Test coverage review
└─ Subagent 4: Architecture assessment
```

### Pattern 4: Adversarial Verification

Use conflicting mandates for thorough review:

```
Verification Subagents (all parallel):
├─ Syntax & Type Checker
├─ Test Runner
├─ Lint & Style Checker
├─ Security Scanner
└─ Build Validator

Then (sequential, after above complete):
├─ False Positive Filter
├─ Missing Issues Finder
└─ Context Validator
```

---

## TodoWrite Integration

When using parallel execution, mark ALL parallel tasks as `in_progress` simultaneously:

### Before Launching Parallel Tasks

```json
{
  "todos": [
    { "content": "Analyze auth module", "status": "in_progress", "activeForm": "Analyzing auth module" },
    { "content": "Analyze API layer", "status": "in_progress", "activeForm": "Analyzing API layer" },
    { "content": "Analyze database layer", "status": "in_progress", "activeForm": "Analyzing database layer" },
    { "content": "Synthesize findings", "status": "pending", "activeForm": "Synthesizing findings" }
  ]
}
```

### After Each Task Completes

Mark as completed as results come in:

```json
{
  "todos": [
    { "content": "Analyze auth module", "status": "completed", "activeForm": "Analyzing auth module" },
    { "content": "Analyze API layer", "status": "completed", "activeForm": "Analyzing API layer" },
    { "content": "Analyze database layer", "status": "in_progress", "activeForm": "Analyzing database layer" },
    { "content": "Synthesize findings", "status": "pending", "activeForm": "Synthesizing findings" }
  ]
}
```

---

## When to Parallelize

### Good Candidates

| Scenario | Parallel Approach |
|----------|-------------------|
| Multiple independent analyses | One subagent per analysis |
| Multi-file processing | One subagent per file/directory |
| Different review perspectives | One subagent per perspective |
| Multiple independent features | One subagent per feature |
| Exploratory research | Multiple search strategies |

### When NOT to Parallelize

| Scenario | Why Sequential |
|----------|----------------|
| Tasks with dependencies | B needs A's output |
| Same file modifications | Risk of conflicts |
| Sequential workflows | Order matters (commit → push → PR) |
| Shared state | Race conditions |
| Limited resources | Overwhelming the system |

---

## Performance Impact

| # Parallel Tasks | Sequential Time | Parallel Time | Speedup |
|------------------|-----------------|---------------|---------|
| 2 | 60s | 30s | 2x |
| 3 | 90s | 30s | 3x |
| 5 | 150s | 30s | 5x |
| 10 | 300s | 30s | 10x |

*Assuming each task takes ~30 seconds*

---

## Common Mistakes

### Mistake 1: Separate Messages

```
WRONG (Sequential):
Message 1: "I'll start analyzing the auth module..."
           <task>Analyze auth</task>
Message 2: "Now let me analyze the API..."
           <task>Analyze API</task>

RIGHT (Parallel):
Message 1: "I'll analyze all modules in parallel..."
           <task>Analyze auth</task>
           <task>Analyze API</task>
           <task>Analyze DB</task>
```

### Mistake 2: Announcing Before Acting

```
WRONG:
"I'm going to launch three parallel tasks to analyze the codebase."
[waits for response]
"Now launching the tasks..."

RIGHT:
"Launching three parallel analysis tasks now:"
<task>...</task>
<task>...</task>
<task>...</task>
```

### Mistake 3: Forgetting Synthesis

```
WRONG:
Just dump all task outputs without integration

RIGHT:
After receiving all results, synthesize:
- Identify common themes
- Resolve contradictions
- Prioritize findings
- Create unified recommendations
```

---

## Parallel Execution Checklist

Before launching parallel tasks, verify:

- [ ] Tasks are truly independent
- [ ] No shared file modifications
- [ ] No sequential dependencies
- [ ] All tasks in SINGLE message
- [ ] TodoWrite updated with all `in_progress`
- [ ] Synthesis step planned

---

## Template: Parallel Analysis

```markdown
## Launching Parallel Analysis

I'm analyzing this codebase from multiple perspectives simultaneously.

### Parallel Tasks

<task description="Security Review">
Analyze for security vulnerabilities, focusing on:
- Authentication/authorization
- Input validation
- Secrets handling
</task>

<task description="Performance Review">
Analyze for performance issues, focusing on:
- N+1 queries
- Memory leaks
- Blocking operations
</task>

<task description="Test Coverage Review">
Analyze test coverage, focusing on:
- Missing test cases
- Edge cases
- Integration tests
</task>

### Synthesis (after all complete)

[Combine findings into prioritized report]
```

---

## Quick Reference

```
RULE #1:
  ALL Task calls in SINGLE message = PARALLEL
  Task calls in SEPARATE messages = SEQUENTIAL

PATTERNS:
  Task-based:       One subagent per task
  Directory-based:  One subagent per directory
  Perspective-based: One subagent per viewpoint
  Adversarial:      Multiple competing reviewers

TODOWRITE:
  Mark ALL parallel tasks as in_progress BEFORE launching
  Mark each as completed AFTER receiving results

SPEEDUP:
  N parallel tasks ≈ Nx faster
  (5 tasks @ 30s each: 150s → 30s)

CHECKLIST:
  ☐ Tasks independent?
  ☐ No shared files?
  ☐ No dependencies?
  ☐ All in ONE message?
  ☐ Synthesis planned?
```
