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

## Parallel Execution

The CI command uses Make's built-in parallelism (`make -j4 --output-sync=target`) for concurrent execution. No external tools are required beyond GNU Make.

Checks run in two stages:

1. **Preflight (sequential)**: `phpcsfixer → phpmd → phpinsights`
2. **Parallel stage**: static analysis, deptrac, tests+openapi, mutation

Parallel stage groups:

| Group               | Tasks                                                                        | Dependency            |
| ------------------- | ---------------------------------------------------------------------------- | --------------------- |
| **Static Analysis** | composer-validate, check-requirements, check-security, psalm, psalm-security | None (fully parallel) |
| **Architecture**    | deptrac                                                                      | None                  |
| **Tests + OpenAPI** | unit-tests, integration-tests, behat, openapi-diff, spectral, schemathesis   | setup-test-db first   |
| **Mutation**        | infection                                                                    | None                  |

### AI-Friendly Output

Make's `--output-sync=target` flag groups each target's output together after completion, preventing interleaved output from parallel tasks.

## Execution Steps

### Step 1: Run CI

```bash
make ci
```

### Step 2: Check Result

- ✅ **Success**: "✅ CI checks successfully passed!" → Task complete
- ❌ **Failure**: Task fails with error output → Go to Step 3

### Step 3: Fix Failures

Identify failing check from output and apply fix:

| Check           | Command                       | Fix                                                       |
| --------------- | ----------------------------- | --------------------------------------------------------- |
| Code style      | `make phpcsfixer`             | Apply auto-fixes                                          |
| Static analysis | `make psalm`                  | Fix type errors                                           |
| Quality metrics | `make phpinsights`            | Reduce complexity, fix architecture                       |
| Tests           | `make unit-tests`             | Debug failing tests                                       |
| Mutations       | `make infection`              | Add missing test cases                                    |
| Config drift    | `make validate-configuration` | Revert locked-file edits, or use exception workflow below |

### Step 4: Re-run

```bash
make ci
```

Repeat Steps 2-4 until success message appears.

### Locked Configuration Exception Workflow

If CI fails with `Modification of locked configuration file is not allowed`:

1. Check whether the user explicitly requested a locked-config change (for example `deptrac.yaml`).
2. If **no**, treat it as accidental drift:
   - Revert locked-file edits.
   - Re-run `make ci`.
3. If **yes**, follow exception handling:
   - Keep changes in a dedicated config-governance PR (no unrelated code changes).
   - Report the failing command output as expected evidence.
   - Escalate for human approval to merge; autonomous agents must not self-approve or self-merge failed CI.
   - Include rationale: reason for change, impact on quality gates, rollback plan.

Do not normalize red CI merges as routine behavior.

## Alternative Commands

| Command              | Description                        |
| -------------------- | ---------------------------------- |
| `make ci`            | Run parallel CI (default, faster)  |
| `make ci-sequential` | Run sequential CI (fallback)       |
| `make ci-preflight`  | Run mutating preflight checks only |

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
- Edit locked quality config files unless the task explicitly requires a governed config change
- Present a failed CI run as "complete" without marking it as a human exception

## Format (Output)

**Required final output**:

```text
✅ CI checks successfully passed!
```

## Verification Checklist

- [ ] `make ci` executed
- [ ] All checks passed (composer, security, style, psalm, tests, mutations)
- [ ] Output shows "✅ CI checks successfully passed!"
- [ ] Zero test failures
- [ ] Zero escaped mutants
- [ ] No quality threshold decreased
- [ ] Locked config files unchanged, or human exception path explicitly documented

## Rollback

If parallel execution causes issues:

1. Use `make ci-sequential` for the original sequential behavior
