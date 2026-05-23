---
# VERSION: 2.43.0
name: loop
description: "Execute task with Ralph Loop pattern: Execute -> Validate -> Iterate until VERIFIED_DONE. Enforces iteration limits per model (Claude: 25, MiniMax: 50, MiniMax-lightning: 100). Use when: (1) iterative fixes needed, (2) running until quality passes, (3) automated task completion. Triggers: /loop, 'loop until done', 'iterate', 'keep trying', 'fix until passing'."
user-invocable: true
---

# Loop - Ralph Loop Pattern

Execute -> Validate -> Iterate until VERIFIED_DONE.

## Quick Start

```bash
/loop "fix all type errors"
/loop "implement tests until 80% coverage"
ralph loop "fix lint errors"
```

## Pattern

```
     EXECUTE
        |
        v
    +---------+
    | VALIDATE |
    +---------+
        |
   Quality    YES    +---------------+
   Passed? --------> | VERIFIED_DONE |
        |            +---------------+
        | NO
        v
    +---------+
    | ITERATE | (max iterations)
    +---------+
        |
        +-------> Back to EXECUTE
```

## Iteration Limits

| Model | Max Iterations | Use Case |
|-------|----------------|----------|
| Claude (Sonnet/Opus) | 25 | Complex reasoning |
| MiniMax M2.1 | 50 | Standard tasks |
| MiniMax-lightning | 100 | Extended loops |

## Workflow

### 1. Execute Task
```yaml
# Attempt implementation
Edit/Write/Bash as needed
```

### 2. Validate
```yaml
# Run quality gates
ralph gates
```

### 3. Check & Iterate
```yaml
# If validation fails and under limit
iteration += 1
if iteration <= MAX:
    continue  # Back to Execute
else:
    report "Max iterations reached"
```

## Loop Types

### Fix Loop
```bash
/loop "fix all type errors"
```
Repeatedly fix errors until build passes.

### Coverage Loop
```bash
/loop "increase test coverage to 80%"
```
Add tests until coverage target met.

### Lint Loop
```bash
/loop "fix all lint warnings"
```
Fix lint issues until clean.

### Build Loop
```bash
/loop "fix build errors"
```
Fix compilation errors until success.

## Exit Conditions

### Success (VERIFIED_DONE)
- Quality gates pass
- Tests pass
- No remaining errors

### Failure (MAX_ITERATIONS)
- Iteration limit reached
- Report remaining issues
- Ask user for guidance

### Manual Exit
- User interrupts
- Critical error detected
- Deadlock detected

## Integration

- Core pattern for all Ralph tasks
- Used by /orchestrator in Step 5
- Hooks enforce limits automatically

## Anti-Patterns

- Never exceed iteration limits
- Never loop without validation step
- Never ignore failing tests
- Never loop on same error repeatedly (detect deadlock)
