---
name: review-code
description: Perform a senior-engineer code review when the user asks to review code, review a PR, review changes, or check code quality
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Bash
argument-hint: "[file path, PR number, or branch name]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: review, quality, code
---

# Review Code

## Overview

Perform a thorough, senior-engineer-level code review that goes beyond style nits to evaluate security, performance, correctness, and maintainability. Adapt the review depth based on the type of change.

## Workflow

1. **Read project conventions** — Check for `.chalk/docs/engineering/` files, especially:
   - `*coding-style*` or `*conventions*` for project-specific style rules
   - `*architecture*` for system design context
   - `*security*` for security requirements
   - Any `AGENTS.md` or contributing guides in the repo root
   - Store these conventions mentally; every review comment must respect project norms

2. **Determine what to review** — Based on `$ARGUMENTS`:
   - If a file path: review that file in full
   - If a PR number: run `gh pr diff <number>` to get the diff, and `gh pr view <number>` for context
   - If a branch name: run `git diff main...<branch>` (or the project's default branch)
   - If nothing specified: run `git diff --cached` for staged changes, or `git diff` for unstaged
   - Also read `git log --oneline -5` on the branch for commit context

3. **Classify the change type** — This determines the review checklist:
   - **Feature**: Full review across all dimensions
   - **Bugfix**: Focus on root cause correctness and regression test presence
   - **Refactor**: Focus on behavior preservation and test coverage
   - **Dependency update**: Focus on changelog review, breaking changes, and supply chain risk
   - **Config/CI change**: Focus on environment parity and secret exposure

4. **Read the full context** — Do not review a diff in isolation:
   - Read the complete files that were modified (not just the diff hunks)
   - Read tests related to the changed code
   - Read interfaces, types, or contracts that the changed code implements
   - Read callers of any modified public APIs

5. **Review across all dimensions** — Evaluate each dimension systematically. Not every dimension applies to every change; skip those that genuinely do not apply.

6. **Write the review** — Use the output format below. Be specific: reference file names, line numbers, and code snippets. Every finding must include a concrete suggestion.

## Review Dimensions

### Security
- **Injection**: SQL injection, XSS, command injection, template injection. Check all user inputs that reach queries, DOM, or shell commands.
- **Authentication & Authorization**: Are auth checks present and correct? Can this endpoint be accessed without proper permissions? Are there IDOR vulnerabilities?
- **Data exposure**: Are secrets, tokens, or PII logged, returned in API responses, or stored insecurely? Check error messages for information leakage.
- **Input validation**: Are inputs validated, sanitized, and bounded? Check for missing length limits, type coercion issues, and prototype pollution.
- **Dependency risk**: Are new dependencies from trusted sources? Do they have known CVEs? Are they actively maintained?

### Performance
- **N+1 queries**: Database calls inside loops. Check ORM usage for eager/lazy loading issues.
- **Unnecessary computation**: Repeated calculations that could be memoized. Expensive operations in hot paths.
- **Payload size**: Large API responses that could be paginated. Unbounded list queries missing LIMIT clauses.
- **Rendering**: Unnecessary re-renders in UI frameworks. Missing memoization on expensive component trees. Bundle size impact of new imports.
- **Concurrency**: Race conditions, missing locks, deadlock potential. Async operations without proper error handling or cancellation.

### Error Handling
- **Missing catch blocks**: Async operations without error handling. Promise chains without `.catch()`.
- **Generic error swallowing**: `catch (e) {}` or `catch (e) { log(e) }` without recovery or user feedback.
- **Silent failures**: Functions that return `null`/`undefined` on error instead of throwing or returning a Result type.
- **Error propagation**: Are errors surfaced to the user with actionable messages? Are they logged with enough context for debugging?
- **Boundary errors**: Off-by-one, null/undefined access, empty array handling, division by zero.

### Naming & Readability
- **Clarity**: Do names communicate intent? Is the code self-documenting or does it need comments?
- **Consistency**: Does the code follow the project's existing patterns and naming conventions?
- **Complexity**: Are functions too long or doing too many things? Is nesting too deep? Can conditionals be simplified?
- **Dead code**: Unreachable code, unused imports, commented-out blocks that should be removed.

### Test Coverage
- **Are changes tested?**: New behavior should have corresponding tests. Modified behavior should have updated tests.
- **Test quality**: Do tests verify behavior or just exercise code? Are assertions meaningful?
- **Edge cases**: Are boundary conditions tested? Empty inputs, max values, concurrent access, error scenarios?
- **Test isolation**: Do tests depend on external state, ordering, or timing? Are they deterministic?

### Breaking Changes
- **API contracts**: Changed request/response shapes, removed fields, renamed endpoints.
- **Database schema**: Migrations that alter existing columns, remove tables, or change constraints.
- **Configuration**: New required environment variables, changed config format, removed flags.
- **Backwards compatibility**: Can this be deployed without coordinating with consumers? Is a migration path provided?

## Change-Type Checklists

### Feature Review
- [ ] All review dimensions evaluated
- [ ] Happy path works correctly
- [ ] Error paths handled gracefully
- [ ] Edge cases considered (empty state, max load, concurrent users)
- [ ] Tests cover new behavior
- [ ] No hardcoded values that should be configurable
- [ ] Logging/observability added for new operations
- [ ] Feature flag wrapping if needed for gradual rollout

### Bugfix Review
- [ ] Root cause correctly identified (not just symptoms patched)
- [ ] Fix addresses the root cause, not a workaround
- [ ] Regression test added that would have caught this bug
- [ ] No other code paths affected by the same root cause
- [ ] Error handling improved to surface this class of bug earlier

### Refactor Review
- [ ] Behavior is preserved (same inputs produce same outputs)
- [ ] Existing tests still pass without modification (or modifications are justified)
- [ ] Code is measurably simpler (fewer branches, clearer names, less duplication)
- [ ] No accidental behavior changes hidden in the refactor

### Dependency Update Review
- [ ] Changelog reviewed for breaking changes
- [ ] Major version bumps justified and migration guide followed
- [ ] No known CVEs in the new version
- [ ] Lock file updated and committed
- [ ] Transitive dependency changes reviewed

## Output

Structure the review as follows:

```markdown
## Code Review: <brief title>

**Change type**: Feature | Bugfix | Refactor | Dependency Update | Config
**Risk level**: Low | Medium | High
**Files reviewed**: <count>

### Findings

#### Blockers (must fix before merge)

**[BLOCKER]** <File:Line> — <Title>
<Description of the issue. Why it matters. What could go wrong.>
```suggestion
// Suggested fix with actual code
```

#### Warnings (should fix, but not a merge blocker)

**[WARNING]** <File:Line> — <Title>
<Description and suggestion>

#### Suggestions (would improve the code)

**[SUGGESTION]** <File:Line> — <Title>
<Description and suggestion>

#### Nitpicks (style preferences, take or leave)

**[NITPICK]** <File:Line> — <Title>
<Description>

### Summary

<2-3 sentence overall assessment. Is this ready to merge? What is the main concern?>
```

## Severity Guidelines

- **Blocker**: Security vulnerability, data loss risk, crash in production, breaking change without migration, test that does not test what it claims.
- **Warning**: Performance issue in a hot path, missing error handling that will cause poor UX, missing test for critical behavior, code that will be hard to maintain.
- **Suggestion**: Better naming, simpler approach, additional test case for an edge case, documentation improvement.
- **Nitpick**: Style preference not covered by project conventions, minor formatting, import ordering.

## Review Principles

- **Assume competence**: The author made their choices for reasons. If something looks wrong, consider that you might be missing context. Ask before declaring.
- **Be specific**: "This could be improved" is not helpful. "This could cause an N+1 query when `users` has more than 100 items; consider eager loading with `.include(:posts)`" is helpful.
- **Suggest, do not demand**: Phrase suggestions as "Consider..." or "What about..." for non-blockers. Reserve imperative language for actual blockers.
- **Praise good work**: If something is well-designed or cleverly handled, say so. Reviews are not just for finding faults.
- **Proportional effort**: A 5-line config change does not need 20 review comments. Scale your review depth to the change's risk and complexity.

## Anti-patterns

- **All nitpicks, no substance** — A review full of formatting comments that misses a SQL injection is worse than no review. Always check security and correctness before style.
- **Rubber-stamp approval** — "LGTM" without evidence of reading the code. Every approval must demonstrate that the reviewer understood the change.
- **Reviewing only the diff** — The diff shows what changed, not whether the change is correct in context. Read the surrounding code.
- **Ignoring error paths** — The happy path usually works. Reviews earn their value by catching unhandled errors, edge cases, and failure modes.
- **Not considering edge cases** — Empty lists, null values, concurrent modifications, network failures, clock skew. Think about what happens when things go wrong.
- **Bikeshedding** — Spending 10 comments debating a variable name while a missing auth check goes unnoticed. Prioritize by impact.
- **Tone problems** — "Why would you do this?" is not a review comment. "I think X would work better here because Y" is. Be constructive.
- **Reviewing code you do not understand** — If you do not understand the domain or the technology, say so. A confident-sounding wrong review is dangerous.
