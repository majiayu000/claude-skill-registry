---
name: code-reviewer
description: Review actual code implementations (Python, JavaScript, TypeScript, React) for correctness, maintainability, security hygiene, and adherence to project patterns. Use when reviewing pull requests to ensure code quality, proper error handling, adequate test coverage mapped to acceptance criteria, and alignment with architecture boundaries and review standards.
---

# Code Reviewer

Review actual code implementations for correctness, maintainability, security hygiene, and adherence to project patterns.

This skill focuses on the code itself and the tests that ship with it, but it must validate test coverage against the **acceptance criteria from the plan/spec**.

---

## Required Inputs (Do Not Start Without These)

To run this review properly, you need:

1. **The PR diff**
2. **The implementation plan or feature spec that includes acceptance criteria**
   - This may be provided in the prompt or is available in the Github Pull Request Description. 
   - If it is missing: **ask for it before reviewing**

If acceptance criteria are unavailable, you may still review code quality and safety, but you must clearly label the review as **incomplete** and explain what you could not validate.

---

## When to Use This Skill

Use this skill when:
- Reviewing pull requests with code changes
- Validating implementations against acceptance criteria
- Checking code quality and maintainability
- Ensuring proper error handling and edge cases
- Validating test coverage against acceptance criteria
- Enforcing architecture boundaries and repo standards

**Do not use** for:
- Reviewing implementation plans (use plan-reviewer skill)
- Architecture design decisions
- Product requirements validation

---

## Severity Model (Use in PR Comments)

Classify findings using these levels, and include the level in each PR comment:

- **Blocker:** Merge must not proceed
- **Must fix:** Should be fixed before merge unless explicitly accepted as debt
- **Should fix:** Important, but can be deferred with a clear reason
- **Nit:** Ignore by default, only mention if explicitly requested

Rule: Avoid comment-only “style polish” and trivial corrections. Prefer high signal feedback.

---

## Review Process

### Step 0: Manifest Validation

Before reviewing code, run `scripts/validate-manifest.sh` to check that all Quest files are listed in `.quest-manifest`. If validation fails, flag it as a **Must fix** — new or renamed files must be added to the manifest before merge.

### Step 1: Architecture Boundaries and Standards

Enforce boundaries and conventions defined in:
- `AGENTS.md`
- `ui/AGENTS.md` (if UI is touched)
- `CODE-REVIEW.md`
- `DOCUMENTATION_STRUCTURE.md`

Check:
- boundaries are respected (no cross-layer leakage)
- imports and dependencies are appropriate
- side effects stay contained in the correct layer
- policy decisions happen in the correct place

If the boundary rules are unclear or missing, flag this as a **Must fix** documentation gap.

---

### Step 2: Correctness and Contracts

Verify the implementation matches intended behavior:

- Core logic correctness
- API contract compatibility and response semantics
- Data invariants (what must always be true)
- Idempotency where relevant (retries, duplicate requests)
- Error semantics (status codes, retryability, failure modes)

Focus on correctness of the behavior, not micro refactors.

---

### Step 3: Code Quality and Maintainability

Review for readability, maintainability, and consistency. See AGENTS.md for coding and architecture philosophy. 
Strive for simple code that is high quality and easy to read. SRP, DRY, KISS, YAGNI are fundamental pillars to follow.

**Python**
- Type hints present where expected
- Clear naming, minimal cleverness
- Exceptions are specific, not generic
- Formatting and lint rules are respected

**JavaScript/TypeScript**
- Avoid `any` unless justified
- Async control flow is correct
- Consistent naming and file structure

**React**
- Hooks usage is correct
- State management is appropriate
- Components are readable and not overly coupled

**Minimal diff rule**
Prefer the smallest change that is correct.
Suggest refactors only when they reduce risk, reduce future change cost, or unblock correctness.

---

### Step 4: Error Handling and Failure Modes

Check:
- failures are handled intentionally, not accidentally
- errors are actionable and consistent with existing patterns
- error messages do not leak secrets or sensitive data
- retries and timeouts are bounded and explicit (where relevant)

---

### Step 5: Test Coverage (Must Map to Plan Acceptance Criteria)

This is required.

1. Extract acceptance criteria from the plan/spec
2. For each acceptance criterion, verify at least one of:
   - a unit test
   - an integration test
   - a UI test
   - an explicit, justified reason why automation is not appropriate

Review tests for:
- coverage of happy path and at least one meaningful failure case
- regression coverage for bug fixes
- determinism and isolation
- realistic boundaries between unit and integration tests

If acceptance criteria exist but tests do not map to them, this is at least a **Must fix**, and often a **Blocker**.

---

### Step 6: Security Hygiene (Tight Scope)

Security review is intentionally narrow and PR-focused:

- No secrets in code, logs, or API responses
- No sensitive data leaks in errors
- Input validation exists at trust boundaries
- Authorization checks exist where required

Do not attempt full dependency audits or broad security assessments here.

---

### Step 7: Observability (When It Matters)

If the code changes production behavior or affects critical workflows, check:
- logs have useful context and are not noisy
- metrics or tracing exist for key paths (if the system uses them)
- errors are debuggable in production

If observability is missing for a risky change, flag as **Should fix** or **Must fix** depending on impact.

---

## Review Output Structure (PR Comment)

Write a PR review that is short and high signal:

### 1. Summary
- Overall assessment in 2 to 5 bullets
- Key risks
- Recommendation: approve / request changes

### 2. Blockers
- Bullet list with concrete fixes

### 3. Must Fix
- Bullet list with concrete fixes

### 4. Should Fix
- Bullet list with concrete fixes

### 5. Test Coverage vs Acceptance Criteria
- A short mapping table or bullet list
- Call out missing tests per acceptance criterion

### 6. Questions
- Only the questions that block merging or block correctness

---

## Principles

1. **Correctness over style**
2. **Boundaries are real:** Enforce architecture rules
3. **Tests must match acceptance criteria**
4. **Security hygiene is non-negotiable**
5. **Prefer minimal diffs**
6. **High signal comments only**
7. **Be explicit about severity**

---

## Success Criteria

A good code review should:
- ✅ Catch correctness issues and contract breaks
- ✅ Enforce architecture boundaries
- ✅ Ensure tests map to acceptance criteria
- ✅ Prevent secret leaks and basic security failures
- ✅ Provide actionable feedback with severity
