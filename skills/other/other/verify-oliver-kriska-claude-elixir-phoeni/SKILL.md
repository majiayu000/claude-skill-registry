---
name: phx:verify
description: Full verification loop for Elixir/Phoenix changes. Use after completing any code implementation to catch issues before committing. Run before creating PRs, after fixing bugs, or whenever you want to confirm compile, format, and tests all pass together.
effort: low
---

# Verification Loop

Complete verification workflow for Elixir/Phoenix projects. Run this after making changes to ensure code quality before commits or PRs.

## Iron Laws

1. **Run in order** — Later steps assume earlier ones pass; running tests against code with compile warnings produces misleading failures
2. **Fix issues immediately** — Batching fixes hides which change caused which failure, making debugging harder than the original problem
3. **Warnings are errors** — Unused variables and deprecated calls accumulate silently until they mask real problems; `--warnings-as-errors` catches them early
4. **Full Dialyzer before PR** — Type mismatches caught in review cost 10x more than catching them locally; Dialyzer finds issues tests often miss

## Verification Sequence

Execute these commands in order, stopping on any failure:

### Step 1: Compilation (Fast Feedback)

```bash
mix compile --warnings-as-errors
```

Catches: Undefined functions, missing modules, type mismatches, unused variables

### Step 2: Formatting

```bash
mix format --check-formatted
```

If fails: Run `mix format` and re-check

### Step 3: Credo Analysis

```bash
mix credo --strict
```

Address all issues marked as consistency or design problems

### Step 4: Run Tests

```bash
# For specific context changes
mix test test/my_app/[changed_context]_test.exs --trace

# For full test suite
mix test --trace
```

All tests must pass

### Step 5: Dialyzer (Pre-PR Required)

```bash
mix dialyzer
```

No new warnings allowed. First run builds PLT cache (slow).

**Handling Dialyzer warnings**: Prefer fixing over suppressing.
If suppression is necessary, add to `.dialyzer_ignore.exs` with
a comment explaining why. Never suppress warnings you don't
understand — investigate first.

## Quick Reference

| Step | Command | Time | When Required |
|------|---------|------|---------------|
| Compile | `mix compile --warnings-as-errors` | Fast | Always |
| Format | `mix format --check-formatted` | Fast | Always |
| Credo | `mix credo --strict` | Medium | Always |
| Test | `mix test --trace` | Medium | Always |
| Dialyzer | `mix dialyzer` | Slow | Before PR |

## Usage

After making code changes:

1. Run `/phx:verify` to execute the full loop
2. Address any failures before proceeding
3. Commit only after all checks pass

For partial verification during development, run individual steps as needed.
