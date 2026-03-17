---
name: debugging-methodology
description: Use when the Developer is investigating bugs, troubleshooting errors, performing root cause analysis, fixing failing tests, or diagnosing unexpected behavior. Activates when debugging, fixing issues, or analyzing error logs.
version: 1.0.0
---

# Debugging Methodology

## When This Applies

Apply this guidance when:
- Investigating a reported bug
- Troubleshooting failing tests or errors
- Diagnosing unexpected behavior
- Performing root cause analysis

## Systematic Debugging Process

### Step 1: Reproduce

Before fixing anything:
1. Understand the expected behavior vs actual behavior
2. Find the minimal steps to reproduce the issue
3. Identify if it's deterministic or intermittent
4. Note the environment (OS, language version, dependencies)

### Step 2: Isolate

Narrow down the problem area:
1. **Binary search** — Comment out half the code, does it still fail? Narrow further.
2. **Input isolation** — What specific input triggers the bug?
3. **Component isolation** — Which component is responsible?
4. **Version isolation** — Did it work before? When did it break? (`git bisect`)

### Step 3: Understand

Before writing the fix:
1. Read the code around the bug carefully — understand the intent
2. Check if the bug is in your code or a dependency
3. Understand WHY it's broken, not just WHERE
4. Check for similar patterns elsewhere that might have the same bug

### Step 4: Fix

Apply the minimal fix:
1. Change only what's necessary to fix the root cause
2. Don't refactor surrounding code in the same task
3. Handle edge cases the fix might introduce
4. Verify the fix resolves the original reproduction steps

### Step 5: Verify

Confirm the fix is correct:
1. Run the reproduction steps — the bug should be gone
2. Run existing tests — nothing new should break
3. Check edge cases around the fix
4. Note what regression test the Integrator should add

## Common Bug Categories

| Category | Symptoms | Where to Look |
|----------|----------|---------------|
| **Off-by-one** | Wrong count, missing first/last item | Loop boundaries, array indices |
| **Null reference** | Crash on property access | Uninitialized variables, optional chains |
| **Race condition** | Intermittent failures | Async code, shared state, parallel operations |
| **Type mismatch** | Wrong values, silent failures | String/number conversions, API responses |
| **State mutation** | Unexpected changes | Shared references, missing deep copies |
| **Missing validation** | Bad data propagates | Input boundaries, API contracts |

## Debugging Tools

- **Read the error stack trace** — Start from the bottom (your code), not the top
- **Add strategic logging** — Log inputs, outputs, and state at key points
- **Use assertions** — Add temporary assertions to verify assumptions
- **Check recent changes** — `git log` and `git diff` for what changed recently
- **Read the docs** — For library/framework issues, check documentation and changelogs

## Reporting the Fix

When submitting a bug fix for review, communicate:
1. What the bug was (root cause)
2. How to reproduce it
3. What the fix does and why
4. What edge cases were considered
5. What regression test should be added
