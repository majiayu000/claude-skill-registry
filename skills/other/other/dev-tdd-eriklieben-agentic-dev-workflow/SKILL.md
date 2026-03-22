---
version: 1.1.0
name: dev-tdd
description: >
  Test-driven development workflow. Auto-detects backend (.NET) and frontend
  (Angular/TypeScript) from project files. Loops RED→GREEN→REFACTOR cycles
  until 80%+ coverage is reached. Filter with "dotnet" or "angular" to target
  one stack. Use when the user says "TDD", "write tests first", "test-driven",
  or invokes /dev-tdd.
disable-model-invocation: true
user-invocable: true
argument-hint: "[dotnet | angular] [feature description]"
---

# TDD — Unified Entry Point

Routes to the appropriate backend and/or frontend TDD skill, then drives
RED→GREEN→REFACTOR cycles until the coverage target is met.

## Step 1: Detect Stack

1. **Explicit filter** — if the user passed `dotnet` or `angular`, use that stack
2. **Context from the feature** — if the feature description mentions API/endpoint/aggregate → .NET, if it mentions component/page/signal → Angular
3. **Project detection**:
   - .NET: any `*.csproj`, `*.sln` file exists
   - Angular: `angular.json` or `package.json` with `@angular/core` exists
4. **workflow.json fallback**:
   - `type: "api"` or `type: "library"` → .NET
   - `type: "frontend"` → Angular

Unlike verification/dependency, TDD typically targets **one stack at a time** — a feature is usually backend or frontend, not both. If both are detected and no filter given, ask the user which stack this feature targets.

## Step 2: Plan Test Cases

Before writing any code, analyze the feature and propose test cases:

```
Feature: Profile email verification

  Test Cases
  ──────────
  1. VerifyEmail_WithCorrectCode_ShouldSucceedAndSetEmail
  2. VerifyEmail_WithExpiredCode_ShouldFail
  3. VerifyEmail_WithWrongCode_ShouldFail
  4. VerifyEmail_WhenAlreadyVerified_ShouldReturnAlreadyVerified
  5. VerifyEmail_WithNullCode_ShouldThrowValidation

  ───────────────────────────────────────────────
  Proceed?  [y]es  [e]dit list  [a]dd more tests
```

Wait for user input. This ensures alignment on what to test before writing anything.

## Step 3: TDD Loop

Read the appropriate sub-skill for patterns and conventions:
- .NET: `.claude/skills/dev-tdd-backend/SKILL.md`
- Angular: `.claude/skills/dev-tdd-frontend/SKILL.md`

Then loop through each test case:

### For each test case:

#### RED — Write a failing test

Write the test following the sub-skill's conventions (naming, AAA pattern, etc.).
Run it to confirm it fails:

```
  [1/5] VerifyEmail_WithCorrectCode_ShouldSucceedAndSetEmail
  RED   ✗ test fails (method not implemented) — expected
```

#### GREEN — Write minimal code to pass

Implement just enough production code to make the test pass.
Run the test again:

```
  GREEN ✓ test passes
```

#### REFACTOR — Improve while green

Clean up the implementation if needed. Run tests to confirm still passing.

```
  REFACTOR ✓ tests still green
```

### After each test case, show progress:

```
  Progress
  ────────
  ✓ 1. VerifyEmail_WithCorrectCode_ShouldSucceedAndSetEmail
  ✓ 2. VerifyEmail_WithExpiredCode_ShouldFail
  ▸ 3. VerifyEmail_WithWrongCode_ShouldFail          ← next
  · 4. VerifyEmail_WhenAlreadyVerified_ShouldReturnAlreadyVerified
  · 5. VerifyEmail_WithNullCode_ShouldThrowValidation

  Tests: 2/5 done  |  All passing
  ──────────────────────────────────────
  [c]ontinue  [s]kip to coverage check  [q]uit
```

Continue to next test case unless user intervenes.

## Step 4: Coverage Check

After all planned test cases are done, run coverage:

```bash
# .NET
dotnet test --collect:"XPlat Code Coverage" --results-directory ./TestResults

# Angular
npx vitest run --coverage
```

Present the results:

```
  Coverage Report
  ───────────────
  Overall:        74%  (target: 80%)
  ProfileAggregate:  68%  ← below target
  EmailService:      82%  ✓
  VerifyEndpoint:    71%  ← below target

  Uncovered areas in ProfileAggregate:
  - Line 42-48: error path when stream is empty
  - Line 63-67: concurrent verification guard

  Uncovered areas in VerifyEndpoint:
  - Line 28-35: authorization failure path

  ────────────────────────────────────────
  Add tests for uncovered areas?  [y]es  [p]ick  [s]kip
```

## Step 5: Coverage Loop

If coverage is below 80% and user chose `y` or `p`:

1. Identify the uncovered code paths
2. Propose additional test cases for them
3. Run more RED→GREEN→REFACTOR cycles
4. Re-check coverage
5. Repeat until 80%+ or user skips

```
  Additional Test Cases (for coverage)
  ─────────────────────────────────────
  6. VerifyEmail_WhenStreamEmpty_ShouldThrowAggregateNotFound
  7. VerifyEmail_WhenConcurrentVerification_ShouldFailWithConflict
  8. VerifyEndpoint_WithUnauthorized_ShouldReturn401

  ───────────────────────────────────
  Proceed?  [y]es  [p]ick  [s]kip
```

After each round, re-check coverage:

```
  Coverage: 74% → 83%  ✓ target met

  Result: 8 tests, all passing, 83% coverage
```

## Step 6: Summary

```
  TDD Complete
  ────────────
  Feature:   Profile email verification
  Stack:     .NET (xUnit + NSubstitute)
  Tests:     8 written, 8 passing
  Coverage:  83% (target: 80% ✓)
  Files:
    new  tests/Api.Tests/Domain/ProfileVerifyEmailTests.cs
    mod  src/Domain/Aggregates/Profile.cs
    mod  src/Api/Endpoints/ProfileEndpoints.cs
```

## Flags

| Flag | Behavior |
|------|----------|
| `dotnet` | Use .NET TDD workflow |
| `angular` | Use Angular TDD workflow |
| `--target N` | Override coverage target (default: 80) |
| (feature description) | What to build test-first |
