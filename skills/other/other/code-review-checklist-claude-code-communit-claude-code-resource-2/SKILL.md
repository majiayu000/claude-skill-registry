---
name: code-review-checklist
description: Comprehensive code review criteria covering correctness, readability, maintainability, security, performance, and testing. Reference when reviewing code changes or preparing code for review.
---

# Code Review Checklist

## Review Philosophy

A code review is a collaborative conversation, not a gatekeeping exercise. The goals are:

1. **Catch bugs** before they reach production.
2. **Share knowledge** across the team.
3. **Maintain consistency** in style and architecture.
4. **Improve the code** incrementally.

Review the code, not the author. Be specific, be kind, and suggest alternatives rather than only pointing out problems.

---

## Severity Classification

Classify every comment to set expectations:

| Severity | Meaning | Action Required |
|---|---|---|
| **Blocker** | Bug, security flaw, data loss risk, or broken build. | Must fix before merge. |
| **Major** | Design issue, missing test, or significant maintainability concern. | Should fix before merge. |
| **Minor** | Style inconsistency, naming nit, or small improvement. | Fix if convenient; OK to defer. |
| **Suggestion** | Alternative approach, future improvement idea, or "did you consider...?" | No action required. |

Prefix comments with the severity: `[Blocker]`, `[Major]`, `[Minor]`, `[Suggestion]`.

---

## 1. Correctness Checklist

Does the code do what it is supposed to do?

- [ ] **Requirements met.** Does the change implement the described feature or fix the described bug completely?
- [ ] **Edge cases handled.** What happens with null, empty, zero, negative, very large, or unexpected inputs?
- [ ] **Error handling.** Are exceptions caught at the right level? Are error messages helpful? Do errors propagate correctly?
- [ ] **Return values.** Are all code paths returning the correct type and value? Are there missing returns?
- [ ] **Off-by-one.** Are loop bounds, array indices, and string slices correct? Inclusive vs. exclusive?
- [ ] **Type safety.** Are types correct? Are there implicit coercions that could cause surprises (e.g., `"1" + 1`)?
- [ ] **Concurrency.** If concurrent, are shared resources protected? Are there potential race conditions or deadlocks?
- [ ] **Data integrity.** Are database transactions used where needed? Is there a risk of partial writes?
- [ ] **Backward compatibility.** Does this change break existing callers, APIs, or stored data?
- [ ] **Idempotency.** If the operation is retried, does it produce the same result?

---

## 2. Readability Checklist

Can a new team member understand this code without asking the author?

- [ ] **Naming.** Do variable, function, and class names clearly express their purpose? Avoid abbreviations unless universally understood.
- [ ] **Function length.** Are functions short enough to understand at a glance (under 20-30 lines)? If not, can they be decomposed?
- [ ] **Single responsibility.** Does each function do one thing? Does each class have one reason to change?
- [ ] **Comments.** Are comments explaining WHY, not WHAT? Is there dead commented-out code that should be removed?
- [ ] **Complexity.** Are nested conditionals minimized? Can guard clauses replace deep nesting?
- [ ] **Consistency.** Does the code follow existing patterns and conventions in the codebase?
- [ ] **Magic values.** Are there unexplained numbers or strings? Should they be named constants?
- [ ] **Code flow.** Can you follow the execution path without jumping around? Is control flow straightforward?
- [ ] **Formatting.** Is indentation, spacing, and line length consistent with the project style?
- [ ] **Dead code.** Is there unreachable code, unused imports, or unused variables?

---

## 3. Maintainability Checklist

Will this code be easy to change six months from now?

- [ ] **DRY (Don't Repeat Yourself).** Is there duplicated logic that should be extracted into a shared function?
- [ ] **Coupling.** Is the code tightly coupled to specific implementations? Could dependency injection improve flexibility?
- [ ] **Abstraction level.** Are high-level and low-level concerns mixed? (e.g., business logic mixed with SQL queries or HTTP handling)
- [ ] **Configuration.** Are environment-specific values (URLs, timeouts, thresholds) configurable rather than hardcoded?
- [ ] **Module boundaries.** Does the change respect existing module/package boundaries? Does it introduce circular dependencies?
- [ ] **API design.** Are public interfaces minimal and well-defined? Can internal details change without affecting callers?
- [ ] **Migration path.** If this changes a schema, API, or data format, is there a migration plan?
- [ ] **Documentation.** Are public APIs documented? Are complex algorithms explained?
- [ ] **Deprecation.** If replacing old code, is the old code marked as deprecated with a removal timeline?
- [ ] **Feature flags.** For risky or incremental changes, should the new behavior be behind a feature flag?

---

## 4. Security Checklist

Could this code be exploited by a malicious actor?

- [ ] **Input validation.** Is all user input validated and sanitized before use?
- [ ] **SQL injection.** Are database queries parameterized? No string concatenation for SQL.
- [ ] **XSS (Cross-Site Scripting).** Is user-generated content escaped before rendering in HTML?
- [ ] **CSRF (Cross-Site Request Forgery).** Are state-changing endpoints protected with CSRF tokens?
- [ ] **Authentication.** Are protected routes/resources properly gated behind authentication?
- [ ] **Authorization.** Does the code verify the user has permission to access/modify the specific resource?
- [ ] **Secrets.** Are API keys, passwords, or tokens hardcoded? They should be in environment variables or a secrets manager.
- [ ] **Logging.** Are sensitive data (passwords, tokens, PII) excluded from logs?
- [ ] **Dependency vulnerabilities.** Are new dependencies from trusted sources? Have they been audited?
- [ ] **File handling.** Are uploaded files validated for type and size? Are paths sanitized to prevent directory traversal?
- [ ] **Rate limiting.** Are public-facing endpoints protected against abuse?
- [ ] **HTTPS.** Are external API calls using HTTPS? Are certificates validated?

---

## 5. Performance Checklist

Will this code perform acceptably under expected load?

- [ ] **Algorithmic complexity.** Is the algorithm appropriate for the data size? Is O(n^2) acceptable here?
- [ ] **Database queries.** Are queries indexed? Are there N+1 query problems? Are results paginated?
- [ ] **Caching.** Should results be cached? If caching exists, is invalidation handled correctly?
- [ ] **Payload size.** Are API responses, database fetches, or file reads bounded in size?
- [ ] **Lazy loading.** Are expensive resources loaded only when needed?
- [ ] **Connection pooling.** Are database/HTTP connections pooled and reused, not created per request?
- [ ] **Async / non-blocking.** Are I/O operations non-blocking where appropriate? Are there unnecessary `await`s on non-dependent operations?
- [ ] **Memory.** Are large data sets streamed rather than loaded entirely into memory?
- [ ] **Startup impact.** Does this change slow down application startup?
- [ ] **Monitoring.** Are new critical code paths instrumented with metrics or tracing?

---

## 6. Testing Checklist

Is the change adequately tested?

- [ ] **Tests exist.** Does every new behavior have at least one test?
- [ ] **Tests pass.** Do all tests pass in CI? Have you run them locally?
- [ ] **Happy path tested.** Are the primary use cases covered?
- [ ] **Edge cases tested.** Are boundary values, empty inputs, and error conditions tested?
- [ ] **Regression test.** If this is a bug fix, is there a test that would have caught the bug?
- [ ] **Test quality.** Do tests assert on behavior, not implementation details?
- [ ] **Test isolation.** Do tests run independently? No shared mutable state between tests?
- [ ] **Test readability.** Can you understand what each test verifies from its name and body?
- [ ] **Mocking.** Are mocks used judiciously? Are they mocking the right boundaries (I/O, not business logic)?
- [ ] **Coverage.** Is coverage maintained or improved? Are critical paths covered?
- [ ] **Flakiness.** Do new tests depend on timing, external services, or non-deterministic data?

---

## How to Give Constructive Feedback

### Do
- **Be specific.** Point to exact lines. Explain the problem concretely.
- **Explain why.** Not just "change this" but "this could cause X because Y."
- **Suggest alternatives.** Provide a code snippet or link to a pattern.
- **Ask questions.** "What happens if X is null here?" is better than "You forgot a null check."
- **Acknowledge good work.** Call out clever solutions, clean refactoring, or good test coverage.
- **Distinguish severity.** A nit is not a blocker. Label them differently.
- **Offer to pair.** If the change is complex, offer to discuss live.

### Do Not
- **Do not attack the person.** "This code is bad" vs. "This function could be simplified by..."
- **Do not bikeshed.** Do not block a PR over trivial style preferences that are not in the style guide.
- **Do not pile on.** If another reviewer already made a point, a thumbs-up is enough.
- **Do not be vague.** "This is confusing" is not actionable. Say what is confusing and why.
- **Do not rewrite.** If you would rewrite the entire approach, have a conversation first — do not do it through line comments.

### Comment Templates

```
[Blocker] Bug: `items.length` will throw if `items` is null.
Consider adding a null check: `if (!items?.length) return [];`

[Major] Missing test: This new validation logic does not have
a corresponding test for the rejection case.

[Minor] Naming: `d` is ambiguous. Consider `durationMs` or
`elapsedDays` to clarify the unit.

[Suggestion] You could use `Array.flatMap()` here to combine
the map and filter into one pass. Not required though.
```

---

## Reviewer Responsibilities

- [ ] Respond to review requests within one business day.
- [ ] Review the full diff, not just the files you are familiar with.
- [ ] Pull the branch and run it locally for non-trivial changes.
- [ ] Check CI results before approving.
- [ ] Re-review after changes are made to your feedback.
- [ ] Approve explicitly when satisfied; do not leave PRs in limbo.

---

## Author Responsibilities

- [ ] Self-review your diff before requesting review.
- [ ] Keep PRs small (under 400 lines of meaningful changes).
- [ ] Write a clear PR description explaining what, why, and how.
- [ ] Link to the issue or spec being implemented.
- [ ] Respond to all comments, even if just "Done" or "Acknowledged."
- [ ] Do not merge until all blocker/major comments are resolved.
- [ ] Squash fixup commits before merging if the project convention requires it.

---

## Review Workflow

1. **Skim first.** Read the PR description and get the big picture.
2. **Architecture pass.** Review the overall design and file structure.
3. **Detailed pass.** Go file by file, line by line, applying the checklists above.
4. **Test pass.** Read the tests. Do they cover the right cases?
5. **Run it.** For anything non-trivial, check out the branch and run it.
6. **Summarize.** Leave an overall summary comment with your verdict.
