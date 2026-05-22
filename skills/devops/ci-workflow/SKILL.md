---
name: ci-workflow
description: Run comprehensive CI checks before committing changes. Use when the user asks to run CI, run quality checks, validate code quality, or before finishing any task that involves code changes.
---

# CI Workflow Skill

## Context (Input)

- Code changes exist in the working directory
- Ready to validate code quality before commit/PR
- Need to ensure all quality standards are met

## Task (Function)

Execute `make ci` and ensure ALL quality checks pass with success message.

**Success Criteria**: Output ends with "✅ CI checks successfully passed!"

## Execution Steps

### Step 1: Run CI

```bash
make ci
```

### Step 2: Check Result

- ✅ **Success**: "✅ CI checks successfully passed!" → Task complete
- ❌ **Failure**: "❌ CI checks failed:" → Go to Step 3

### Step 3: Fix Failures

Identify failing check from output and apply fix:

| Check           | Command            | Fix                                 |
| --------------- | ------------------ | ----------------------------------- |
| Code style      | `make phpcsfixer`  | Apply auto-fixes                    |
| Static analysis | `make psalm`       | Fix type errors                     |
| Quality metrics | `make phpinsights` | Reduce complexity, fix architecture |
| Tests           | `make unit-tests`  | Debug failing tests                 |
| Mutations       | `make infection`   | Add missing test cases              |

### Step 4: Re-run

```bash
make ci
```

Repeat Steps 2-4 until success message appears.

## Constraints (Parameters)

**NEVER decrease these thresholds**:

- min-quality: 100%
- min-complexity: 93%
- min-architecture: 100%
- min-style: 100%
- mutation MSI: 100%
- test coverage: 100%

**DO NOT**:

- Lower quality thresholds
- Skip failing checks
- Commit without "✅ CI checks successfully passed!" message
- Run commands outside Docker container (use `make` or `docker compose exec php`)

## Format (Output)

**Required final output**:

```
✅ CI checks successfully passed!
```

## Verification Checklist

- [ ] `make ci` executed
- [ ] All checks passed (composer, security, style, psalm, tests, mutations)
- [ ] Output shows "✅ CI checks successfully passed!"
- [ ] Zero test failures
- [ ] Zero escaped mutants
- [ ] No quality threshold decreased
