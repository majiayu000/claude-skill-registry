---
name: implementation-phase
description: Executes implementation tasks using Test-Driven Development, prevents code duplication through anti-duplication checks, and maintains quality through continuous testing. Use when implementing features from tasks.md, during the /implement phase, or when the user requests TDD-based implementation. (project)
---

<objective>
Execute tasks from tasks.md using Test-Driven Development, preventing code duplication, and maintaining high quality.

Inputs: tasks.md (20-30 tasks), plan.md (implementation plan)
Outputs: Implemented code, test suites, updated tracking files
Expected duration: 2-10 days (varies by complexity)
</objective>

<quick_start>
Execute implementation tasks systematically:

1. Load tech stack constraints from docs/project/tech-stack.md
2. Review task dependencies in tasks.md for parallel work
3. Generate test suite using test-architect (complex features)
4. Execute tasks using TDD (RED → GREEN → REFACTOR)
5. Update task status in NOTES.md after completion
6. Run anti-duplication checks before writing new code
7. Run tests + type-check after each task triplet
8. Validate type safety with type-enforcer (TypeScript)
9. Validate security with security-sentry (auth/API/uploads)
10. Commit implementation with descriptive messages

Key principle: Test first, implement second. Never write code without tests.
</quick_start>

<prerequisites>
Before starting implementation:
- Tasks phase completed (tasks.md exists with 20-30 tasks)
- Plan phase completed (plan.md exists with reuse strategy)
- Development environment set up (dependencies installed)
- Test framework configured (Jest, Pytest, etc.)
- Git working tree clean (no uncommitted changes)

Validate environment with test run before proceeding.
</prerequisites>

<workflow>
<step number="1">
**Load Tech Stack Constraints**

Before writing any code, load technology constraints from docs/project/tech-stack.md:

```bash
# Read tech stack documentation
cat docs/project/tech-stack.md

# Extract: database, framework, libraries, deployment platform
```

Prevents hallucinating wrong technologies (e.g., suggesting MongoDB when PostgreSQL required).

See resources/tech-stack-validation.md for validation checklist.
</step>

<step number="2">
**Review Task Dependencies**

Analyze tasks.md for dependency relationships:

```markdown
# Look for dependencies in tasks.md

T001: Create User model [no dependencies]
T002: Create AuthService [depends: T001]
T003: Create LoginController [depends: T002]
```

Identify parallel work opportunities:

- Independent tasks can run concurrently
- Dependent tasks must run sequentially

See resources/task-batching.md for parallel execution strategy.
</step>

<step number="3">
**Generate Test Suite (Complex Features)**

For complex features (>10 tasks, multiple components), use test-architect agent:

```bash
# Launch test-architect to convert acceptance criteria → tests
# Agent reads tasks.md acceptance criteria
# Generates comprehensive test suite (unit + integration + E2E)
```

Benefits:

- Tests written before implementation (pure TDD)
- Coverage of happy paths, edge cases, error conditions
- Executable specification from acceptance criteria

See resources/tdd-workflow.md#test-architect for detailed usage.
</step>

<step number="4">
**Execute Tasks Using TDD**

For each task, follow RED → GREEN → REFACTOR cycle:

**RED (Write Failing Test)**:

```python
def test_user_can_login_with_valid_credentials():
    """Test user authentication with correct email/password"""
    user = create_user(email="test@example.com", password="secure123")
    result = auth_service.login("test@example.com", "secure123")

    assert result.success is True
    assert result.user.email == "test@example.com"
    assert result.token is not None
```

**GREEN (Minimal Implementation)**:

```python
def login(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        token = generate_jwt(user.id)
        return LoginResult(success=True, user=user, token=token)
    return LoginResult(success=False)
```

**REFACTOR (Clean Up)**:

- Extract magic values to constants
- Remove duplication
- Improve naming
- Add error handling

See resources/tdd-workflow.md for complete RED → GREEN → REFACTOR guide.
</step>

<step number="5">
**Update Task Status**

After completing each task, update NOTES.md:

```markdown
## Implementation Progress

- [x] T001: Create User model (45min, 2025-11-19 10:00)
- [x] T002: Create AuthService (60min, 2025-11-19 11:30)
- [ ] T003: Create LoginController (est. 30min)
```

Track velocity for remaining tasks:

- Average time per task
- Estimated completion date
- Blockers and dependencies

See resources/task-tracking.md for velocity tracking formulas.
</step>

<step number="6">
**Run Anti-Duplication Checks**

Before writing new code, search for existing implementations:

```bash
# Search for similar functions
grep -r "function login" src/

# Search for similar components
grep -r "class AuthService" src/

# Search for similar patterns
grep -r "validate_email" src/
```

If found:

- Reuse existing code (DRY principle)
- Extract to shared utility if needed
- Refactor duplicated logic

See resources/anti-duplication-checks.md for search patterns.
</step>

<step number="7">
**Continuous Testing**

After completing task triplet (3 tasks), run full test suite:

```bash
# Run all tests
npm test  # or pytest, cargo test, etc.

# Run type checker (TypeScript/Python)
npm run type-check

# Check coverage
npm run test:coverage
# Target: ≥80% coverage
```

Fix failing tests immediately (don't accumulate test debt).

See resources/continuous-testing.md for test cadence strategy.
</step>

<step number="8">
**Type Safety Validation (TypeScript)**

For TypeScript projects, use type-enforcer agent to validate strict type safety:

```bash
# Invoke type-enforcer agent
# Scans for: implicit any, unguarded nulls, missing discriminated unions
# Reports violations with file:line locations
```

Blocks:

- Implicit `any` types (requires explicit type annotations)
- Null/undefined access without guards
- Missing exhaustive pattern matching

See resources/continuous-testing.md#type-enforcer for strict mode requirements.
</step>

<step number="9">
**Security Validation**

For security-sensitive code (auth, API, uploads), use security-sentry agent:

```bash
# Invoke security-sentry agent
# Scans for: SQL injection, XSS, CSRF, secret exposure, insecure dependencies
# Blocks deployment if critical vulnerabilities found
```

Critical scans:

- Authentication/session code
- File upload handlers
- API endpoints accepting user input
- Environment configuration files

See resources/continuous-testing.md#security-sentry for vulnerability patterns.
</step>

<step number="10">
**Commit Implementation**

Commit after each task or task triplet:

```bash
git add src/services/AuthService.ts tests/AuthService.test.ts
git commit -m "feat: implement user authentication service

- Add login() with email/password validation
- Add JWT token generation
- Add password hashing with bcrypt
- Test coverage: 95% (unit + integration)

Implements: T002
Tests: test_user_can_login_with_valid_credentials"
```

Commit message format:

- Type: feat, fix, refactor, test, docs
- Subject: concise description (<75 chars)
- Body: what + why (not how)
- Footer: task reference, test coverage

See resources/commit-strategy.md for commit best practices.
</step>

<step number="11">
**Handle Blocked Tasks**

If task blocked (missing dependency, unclear requirement, external blocker):

1. Document blocker in NOTES.md:

   ```markdown
   ## Blocked Tasks

   - [ ] T005: Stripe payment integration (BLOCKED: awaiting API keys from DevOps)
   ```

2. Move to next independent task
3. Escalate blocker if critical path
4. Update state.yaml with blocker reason

See resources/handling-blocked-tasks.md for escalation strategies.
</step>

<step number="12">
**Validate Implementation Complete**

Before proceeding to /optimize:

```bash
# All tasks completed or blocked?
grep -c "\[ \]" specs/NNN-slug/tasks.md  # Should be 0 or only blocked tasks

# All tests passing?
npm test  # Should be green

# Coverage threshold met?
npm run test:coverage  # Should be ≥80%

# Type check passing?
npm run type-check  # Should be green

# No DRY violations?
# Manual review or use duplication detection tool
```

Update state.yaml: `implementation.status = completed`

Proceed to `/optimize` for code review and production readiness.
</step>
</workflow>

<validation>
After implementation phase, verify:

- All tasks completed (grep "\[x\]" tasks.md shows all tasks checked)
- Or blocked tasks documented with reasons in NOTES.md
- Test coverage ≥80% (unit + integration combined)
- All tests passing (CI pipeline green)
- No code duplication (DRY violations <3 instances)
- Code review checklist passed (resources/code-review-checklist.md)
- Git commits made with descriptive messages (Conventional Commits format)
- Type safety validated (TypeScript strict mode passing)
- Security validated (no critical vulnerabilities from security-sentry)
- Blocked tasks escalated if on critical path
  </validation>

<anti_patterns>
<pitfall name="testing_after_implementation">
**❌ Don't**: Write code first, then write tests afterward
**✅ Do**: Write failing test first (RED), then implement (GREEN), then refactor

**Why**: Writing tests after code leads to:

- Tests that pass implementation (not requirements)
- Lower coverage (hard to test after the fact)
- Design flaws missed (tests reveal design issues early)

**Example** (bad):

```
1. Write login() function
2. Manually test in browser
3. Write test afterward (test passes because code exists)
```

**Example** (good):

```
1. Write test_user_can_login() (fails - no implementation)
2. Implement login() to make test pass
3. Refactor for clarity
```

</pitfall>

<pitfall name="skipping_duplication_checks">
**❌ Don't**: Write new code without searching for existing implementations
**✅ Do**: Search codebase for similar functions/components before writing

**Why**: Leads to:

- Code duplication (DRY violations)
- Inconsistent behavior across codebase
- Higher maintenance burden (fix bugs in multiple places)

**Example** (bad):

```javascript
// New file: utils/emailValidator.js
function validateEmail(email) {
  return /\S+@\S+\.\S+/.test(email);
}

// Didn't search - this already exists in utils/validation.js!
```

**Example** (good):

```bash
# Before writing validateEmail, search:
grep -r "validateEmail" src/
# Found: src/utils/validation.js already has validateEmail()
# Reuse existing function instead of duplicating
```

</pitfall>

<pitfall name="accumulating_test_debt">
**❌ Don't**: Continue implementing when tests are failing
**✅ Do**: Fix failing tests immediately before proceeding

**Why**: Accumulating test failures leads to:

- Unknown which change broke tests
- Harder to debug (multiple changes since last green)
- Loss of confidence in test suite

**Example** (bad):

```
T001: Implemented ✓ (tests passing)
T002: Implemented ✓ (1 test failing - ignore for now)
T003: Implemented ✓ (3 tests failing - will fix later)
# Now: which change broke which test? Unknown.
```

**Example** (good):

```
T001: Implemented ✓ (all tests passing)
T002: Implemented ✓ (1 test failing - STOP, fix immediately)
# Fix test before T003
T003: Implemented ✓ (all tests passing)
```

</pitfall>

<pitfall name="ignoring_type_errors">
**❌ Don't**: Suppress type errors with `@ts-ignore` or `any` types
**✅ Do**: Fix type errors by adding proper type annotations

**Why**: Type errors indicate design issues:

- Null safety violations
- Incorrect function signatures
- Missing type definitions

**Example** (bad):

```typescript
// @ts-ignore
const user = getUser(userId); // Type error suppressed
console.log(user.email); // May crash if user is null
```

**Example** (good):

```typescript
const user: User | null = getUser(userId);
if (user) {
  console.log(user.email); // Type-safe
} else {
  console.error("User not found");
}
```

</pitfall>

<pitfall name="large_uncommitted_changes">
**❌ Don't**: Work for hours/days without committing
**✅ Do**: Commit after each task or task triplet (small, frequent commits)

**Why**: Large uncommitted changes are risky:

- Hard to debug (which change broke what?)
- Hard to review (massive diffs)
- Risk of losing work (no backup)

**Target**: Commit every 1-3 tasks (30-90 minutes of work)
</pitfall>
</anti_patterns>

<best_practices>
<practice name="test_first_discipline">
Always write test before implementation:

1. Write failing test (RED)
2. Implement minimal code to pass (GREEN)
3. Refactor for clarity (REFACTOR)
4. Repeat

Result: Higher coverage, better design, fewer bugs
</practice>

<practice name="continuous_testing">
Run tests frequently (not just at end):

- After each task triplet (3 tasks)
- Before committing
- Before pushing
- In CI pipeline

Result: Catch bugs early, maintain green build
</practice>

<practice name="small_commits">
Commit frequently with clear messages:

- After each task (or task triplet)
- Conventional Commits format
- Include task reference and test coverage

Result: Clear history, easy rollback, reviewable diffs
</practice>

<practice name="tech_stack_validation">
Load tech stack constraints before implementation:

- Read docs/project/tech-stack.md
- Verify database, framework, libraries
- Use documented technologies only

Result: No hallucinated tech choices, consistency
</practice>

<practice name="anti_duplication_checks">
Search before writing new code:

- grep for similar functions
- Check existing services/utilities
- Reuse or extract to shared module

Result: DRY codebase, lower maintenance burden
</practice>
</best_practices>

<success_criteria>
Implementation phase complete when:

- [ ] All tasks completed (grep "\[x\]" tasks.md shows 100% completion)
- [ ] Or blocked tasks documented (NOTES.md lists blockers with reasons)
- [ ] Test coverage ≥80% (run test:coverage to verify)
- [ ] All tests passing (CI pipeline green, no failures)
- [ ] No code duplication (DRY violations <3 instances)
- [ ] Code review checklist passed (resources/code-review-checklist.md)
- [ ] Git commits made (Conventional Commits format)
- [ ] Type safety validated (TypeScript strict mode passing - if applicable)
- [ ] Security validated (security-sentry shows no critical vulnerabilities)
- [ ] state.yaml updated (implementation.status = completed)

Ready to proceed to /optimize phase.
</success_criteria>

<quality_standards>
**Good implementation**:

- Test-first discipline (all code has tests before implementation)
- High coverage (≥80% unit + integration)
- No duplication (DRY violations <3)
- Small commits (1-3 tasks per commit)
- Type-safe (TypeScript strict mode, no `any` types)
- Secure (no vulnerabilities from security-sentry)

**Bad implementation**:

- Tests written after code (low coverage, design flaws)
- Code duplication (DRY violations >5)
- Large uncommitted changes (hours of work, risky)
- Type errors suppressed (`@ts-ignore`, `any` types)
- Security vulnerabilities ignored (SQL injection, XSS, etc.)
  </quality_standards>

<troubleshooting>
**Issue**: Tests failing after implementation
**Solution**: Fix immediately (don't accumulate test debt), use TDD cycle (test first)

**Issue**: Code duplication detected
**Solution**: Extract to shared utility, refactor duplicated logic, run anti-duplication checks before writing

**Issue**: Low test coverage (<80%)
**Solution**: Write missing tests, use test-architect for complex features, follow TDD discipline

**Issue**: Task blocked (missing dependency, unclear requirement)
**Solution**: Document blocker in NOTES.md, move to next independent task, escalate if critical path

**Issue**: Type errors accumulating
**Solution**: Fix immediately, use type-enforcer agent for validation, enable TypeScript strict mode

**Issue**: Large uncommitted changes
**Solution**: Commit frequently (after each task triplet), use small focused commits
</troubleshooting>

<reference_guides>
Core workflow:

- TDD Workflow (resources/tdd-workflow.md) - RED → GREEN → REFACTOR cycle
- Task Batching (resources/task-batching.md) - Parallel execution strategy
- Task Tracking (resources/task-tracking.md) - NOTES.md updates, velocity tracking

Quality gates:

- Tech Stack Validation (resources/tech-stack-validation.md) - Load constraints from tech-stack.md
- Anti-Duplication Checks (resources/anti-duplication-checks.md) - Search patterns, DRY enforcement
- Continuous Testing (resources/continuous-testing.md) - Test cadence, coverage requirements

Advanced topics:

- Handling Blocked Tasks (resources/handling-blocked-tasks.md) - Escalation strategies
- Integration Testing (resources/integration-testing.md) - Multi-component tests
- UI Component Testing (resources/ui-component-testing.md) - React Testing Library
- E2E Testing (resources/e2e-testing.md) - Playwright/Cypress patterns

Reference:

- Common Mistakes (resources/common-mistakes.md) - Anti-patterns to avoid
- Best Practices (resources/best-practices.md) - Proven patterns
- Code Review Checklist (resources/code-review-checklist.md) - Pre-commit validation
- Troubleshooting Guide (resources/troubleshooting.md) - Common blockers
  </reference_guides>
