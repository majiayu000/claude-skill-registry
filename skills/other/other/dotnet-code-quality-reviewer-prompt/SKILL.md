---
name: dotnet-code-quality-reviewer-prompt
description: Use when a .NET/C# implementation task is complete and needs quality-focused code review, especially xUnit test quality (behavioral tests, assertion counts, NSubstitute mock boundaries, anti-patterns like getter/setter tests)
---

# .NET Code Quality Reviewer Prompt Template

## Overview

Prompt template for dispatching a .NET code quality review subagent. Core principle: verify that .NET code is well-built (clean, tested, maintainable) with special focus on test quality -- tests should catch real bugs, not verify trivial property assignments.

## When to Use

- After a .NET implementation task is complete and you need a quality-focused code review
- When you want to validate test quality beyond basic coverage (behavioral testing, structure, mock boundaries)
- When dispatching a unified code review that checks both spec compliance and code quality in a single pass

## When NOT to Use

- For non-.NET code -- the checklist is .NET/C#-specific (NSubstitute, xUnit, EF Core patterns)
- For general architecture or design reviews without implementation code to inspect

## Quick Reference

| Section | Focus |
|---------|-------|
| Behavioral Testing | Tests catch bugs, not verify structure |
| Test Structure | Max 3 assertions, naming, Theory/InlineData usage |
| Test Infrastructure | CustomWebApplicationFactory, IClassFixture, SQLite |
| Mock Boundaries | NSubstitute for infrastructure only, no domain mocks |
| EF Core Patterns | N+1 queries, AsNoTracking, DbContext lifetime |
| Coverage | Edge cases, error paths, happy+failure |
| Anti-Patterns | CanSetProperties, MockVerifyOnly, DomainMock, etc. |

## Required Dependency

**REQUIRED PLUGIN:** `superpowers`

- Provides `code-reviewer` agent and `requesting-code-review/code-reviewer.md` base template
- Base template handles: git diff inspection, standard review checklist (code quality, architecture, testing, requirements, production readiness)
- Base template output format: Strengths, Issues by severity, Recommendations, Assessment with merge verdict
- This skill adds .NET test quality criteria via `ADDITIONAL_REVIEW_CRITERIA`

## Placeholder Variables

| Variable | Source |
|---|---|
| `WHAT_WAS_IMPLEMENTED` | From implementer subagent's completion report |
| `PLAN_OR_REQUIREMENTS` | Plan file path + task number, e.g. "Task 3 from _docs/plans/feature-x.md" |
| `BASE_SHA` | Commit SHA before implementation (`git log`) |
| `HEAD_SHA` | Current commit after implementation (typically `HEAD`) |
| `DESCRIPTION` | One-line task summary |

## Common Mistakes

- **Applying to non-.NET code** -- checklist is xUnit/NSubstitute/EF Core-specific. Will produce false positives on other stacks.
- **Forgetting placeholder variables** -- template breaks if `BASE_SHA`/`HEAD_SHA` are left as placeholders. Get actual SHAs from `git log`.
- **Missing superpowers plugin** -- dispatch targets `superpowers:code-reviewer`. Task tool call fails without it.
- **NSubstitute as universal rule** -- checklist mandates NSubstitute as a project convention. Adjust if your project uses Moq or FakeItEasy.

## Dispatch Template

This skill provides `ADDITIONAL_REVIEW_CRITERIA` for a unified review that checks both spec compliance and code quality in a single pass. The reviewer subagent loads this skill via the Skill tool and follows its criteria checklist.

Dispatch by calling the Task tool with the `superpowers:code-reviewer` agent, instructing it to load this skill:

```
Task tool (superpowers:code-reviewer):
  Use template at requesting-code-review/code-reviewer.md

  WHAT_WAS_IMPLEMENTED: [from implementer's report]
  PLAN_OR_REQUIREMENTS: Task N from [plan-file]
  BASE_SHA: [commit before task]
  HEAD_SHA: [current commit]
  DESCRIPTION: [task summary]

  ADDITIONAL_REVIEW_CRITERIA: |
    ## .NET Test Quality Review Checklist

    Review ALL test files in the diff. For each test, apply these checks:

    ### Behavioral Testing
    - [ ] No getter/setter tests (flag: `CanSetProperties`, `CanSetName`, `HasInitializedCollections`, `IsNullable`, `HasEmptyDefault`)
    - [ ] Every test catches a real bug — ask "what bug does this prevent?" If answer is "none", flag it
    - [ ] Tests verify outcomes (returned data, DB state, domain state), not mock interactions (`Received()`, `Verify()`)
    - [ ] No assertion-less tests (every test has at least one Assert)
    - [ ] Integration tests assert response body or DB state, not just HTTP status code

    ### Test Structure
    - [ ] Max 3 assertions per test (single logical assertion OK even if multiple Assert calls)
    - [ ] Naming follows `MethodName_Scenario_ExpectedBehavior`
    - [ ] `[Theory]`+`[InlineData]` used when testing same behavior with multiple inputs
    - [ ] No "and" in test names (split into separate tests)

    ### Test Infrastructure
    - [ ] Shared `CustomWebApplicationFactory` used for integration tests (not inline `WebApplicationFactory<Program>`)
    - [ ] `IClassFixture<CustomWebApplicationFactory>` pattern (not new factory per test)
    - [ ] Setup helpers in shared `TestHelpers` class (not duplicated across test files)
    - [ ] No test-only methods added to production classes
    - [ ] SQLite in-memory with kept-alive connection (NOT EF InMemory provider)

    ### Mock Boundaries
    - [ ] Infrastructure mocked: DbContext, IHttpClientFactory, ILogger, TimeProvider, external APIs
    - [ ] Domain NOT mocked: entities, value objects, pure functions use real instances
    - [ ] NSubstitute used (not Moq, not FakeItEasy) — project convention, adjust if your project differs
    - [ ] Mock setup is <50% of test code

    ### EF Core Patterns
    - [ ] No N+1 queries — eager load with `.Include()` or use projections (`.Select()`) instead of lazy-loading in loops
    - [ ] Read-only queries use `.AsNoTracking()` to avoid unnecessary change tracking overhead
    - [ ] DbContext lifetime is scoped (not singleton/transient) — verify DI registration
    - [ ] Migrations are clean — no empty migrations, no manual SQL unless justified, migration order matches commit history
    - [ ] No business logic in migrations — data transforms belong in domain services or one-time scripts
    - [ ] Queries use server-side evaluation — flag `.ToList()` before `.Where()` or LINQ that forces client evaluation

    ### Coverage
    - [ ] Edge cases tested (null, empty, boundary values)
    - [ ] Error paths tested (invalid input, not found, unauthorized)
    - [ ] All new public methods have at least one test
    - [ ] Happy path + at least one failure path per endpoint

    ### Anti-Patterns to Flag
    Flag these by name in review:
    - **CanSetProperties**: Test that only verifies property assignment
    - **IsNullable**: Test that only checks default null values
    - **HasEmptyDefault**: Test that only checks empty collection initialization
    - **MockVerifyOnly**: Test where only assertion is `Received()` or `Verify()`
    - **DuplicateFactory**: `new WebApplicationFactory<Program>()` instead of shared fixture
    - **AssertionOverload**: Test with >3 assertions testing unrelated things (Important); >5 unrelated assertions is Critical
    - **DomainMock**: `Substitute.For<DomainEntity>()` on domain objects
    - **Assertionless**: Test with zero assertions — passes silently, catches nothing
    - **StatusCodeOnly**: Integration test that only checks `EnsureSuccessStatusCode()` or status code without verifying body/DB

    ### Severity Guide
    - **Critical**: getter/setter tests, domain mocking, no tests for new methods, >5 unrelated assertions, assertion-less tests
    - **Important**: missing Theory, >3 unrelated assertions, duplicate factory, mock-verify-only, status-code-only integration tests
    - **Minor**: naming convention, missing edge case test
```

**Code reviewer returns:** Strengths, Issues (Critical/Important/Minor), Assessment -- with specific test quality findings using the checklist above.
