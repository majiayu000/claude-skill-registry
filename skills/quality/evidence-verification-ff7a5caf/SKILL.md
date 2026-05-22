---
name: evidence-verification
description: Use when completing tasks, code reviews, or deployments to verify work with evidence. Collects test results, build outputs, coverage metrics, and exit codes to prove work is complete.
version: 1.0.0
author: SkillForge AI Agent Hub
tags: [quality, verification, testing, evidence, completion]
---

# Evidence-Based Verification Skill

**Version:** 1.0.0
**Type:** Quality Assurance
**Auto-activate:** Code review, task completion, production deployment

## Overview

This skill teaches agents how to collect and verify evidence before marking tasks complete. Inspired by production-grade development practices, it ensures all claims are backed by executable proof: test results, coverage metrics, build success, and deployment verification.

**Key Principle:** Show, don't tell. No task is complete without verifiable evidence.

---

## When to Use This Skill

### Auto-Activate Triggers
- Completing code implementation
- Finishing code review
- Marking tasks complete in Squad mode
- Before agent handoff
- Production deployment verification

### Manual Activation
- When user requests "verify this works"
- Before creating pull requests
- During quality assurance reviews
- When troubleshooting failures

---

## Core Concepts

### 1. Evidence Types

**Test Evidence**
- Exit code (must be 0 for success)
- Test suite results (passed/failed/skipped)
- Coverage percentage (if available)
- Test duration

**Build Evidence**
- Build exit code (0 = success)
- Compilation errors/warnings
- Build artifacts created
- Build duration

**Deployment Evidence**
- Deployment status (success/failed)
- Environment deployed to
- Health check results
- Rollback capability verified

**Code Quality Evidence**
- Linter results (errors/warnings)
- Type checker results
- Security scan results
- Accessibility audit results

### 2. Evidence Collection Protocol

```markdown
## Evidence Collection Steps

1. **Identify Verification Points**
   - What needs to be proven?
   - What could go wrong?
   - What does "complete" mean?

2. **Execute Verification**
   - Run tests
   - Run build
   - Run linters
   - Check deployments

3. **Capture Results**
   - Record exit codes
   - Save output snippets
   - Note timestamps
   - Document environment

4. **Store Evidence**
   - Add to shared context
   - Reference in task completion
   - Link to artifacts
```

### 3. Verification Standards

**Minimum Evidence Requirements:**
- ✅ At least ONE verification type executed
- ✅ Exit code captured (0 = pass, non-zero = fail)
- ✅ Timestamp recorded
- ✅ Evidence stored in context

**Production-Grade Requirements:**
- ✅ Tests run with exit code 0
- ✅ Coverage >70% (or project standard)
- ✅ Build succeeds with exit code 0
- ✅ No critical linter errors
- ✅ Security scan passes

---

## Evidence Collection Templates

### Template 1: Test Evidence

Use this template when running tests:

```markdown
## Test Evidence

**Command:** `npm test` (or equivalent)
**Exit Code:** 0 ✅ / non-zero ❌
**Duration:** X seconds
**Results:**
- Tests passed: X
- Tests failed: X
- Tests skipped: X
- Coverage: X%

**Output Snippet:**
```
[First 10 lines of test output]
```

**Timestamp:** YYYY-MM-DD HH:MM:SS
**Environment:** Node vX.X.X, OS, etc.
```

### Template 2: Build Evidence

Use this template when building:

```markdown
## Build Evidence

**Command:** `npm run build` (or equivalent)
**Exit Code:** 0 ✅ / non-zero ❌
**Duration:** X seconds
**Artifacts Created:**
- dist/bundle.js (XXX KB)
- dist/styles.css (XXX KB)

**Errors:** X
**Warnings:** X

**Output Snippet:**
```
[First 10 lines of build output]
```

**Timestamp:** YYYY-MM-DD HH:MM:SS
```

### Template 3: Code Quality Evidence

Use this template for linting and type checking:

```markdown
## Code Quality Evidence

**Linter:** ESLint / Ruff / etc.
**Command:** `npm run lint`
**Exit Code:** 0 ✅ / non-zero ❌
**Errors:** X
**Warnings:** X

**Type Checker:** TypeScript / mypy / etc.
**Command:** `npm run typecheck`
**Exit Code:** 0 ✅ / non-zero ❌
**Type Errors:** X

**Timestamp:** YYYY-MM-DD HH:MM:SS
```

### Template 4: Combined Evidence Report

Use this comprehensive template for task completion:

```markdown
## Task Completion Evidence

### Task: [Task description]
### Agent: [Agent name]
### Completed: YYYY-MM-DD HH:MM:SS

### Verification Results

| Check | Command | Exit Code | Result |
|-------|---------|-----------|--------|
| Tests | `npm test` | 0 | ✅ 45 passed, 0 failed |
| Build | `npm run build` | 0 | ✅ Bundle created (234 KB) |
| Linter | `npm run lint` | 0 | ✅ No errors, 2 warnings |
| Types | `npm run typecheck` | 0 | ✅ No type errors |

### Coverage
- Statements: 87%
- Branches: 82%
- Functions: 90%
- Lines: 86%

### Evidence Files
- Test output: `.claude/quality-gates/evidence/tests-2025-XX-XX.log`
- Build output: `.claude/quality-gates/evidence/build-2025-XX-XX.log`

### Conclusion
All verification checks passed. Task ready for review.
```

---

## Step-by-Step Workflows

### Workflow 1: Code Implementation Verification

**When:** After writing code for a feature or bug fix

**Steps:**

1. **Save all files** - Ensure changes are written

2. **Run tests**
   ```bash
   npm test
   # or: pytest, cargo test, go test, etc.
   ```
   - Capture exit code
   - Note passed/failed counts
   - Record coverage if available

3. **Run build** (if applicable)
   ```bash
   npm run build
   # or: cargo build, go build, etc.
   ```
   - Capture exit code
   - Note any errors/warnings
   - Verify artifacts created

4. **Run linter**
   ```bash
   npm run lint
   # or: ruff check, cargo clippy, golangci-lint run
   ```
   - Capture exit code
   - Note errors/warnings

5. **Run type checker** (if applicable)
   ```bash
   npm run typecheck
   # or: mypy, tsc --noEmit
   ```
   - Capture exit code
   - Note type errors

6. **Document evidence**
   - Use Template 4 (Combined Evidence Report)
   - Add to shared context under `quality_evidence`
   - Reference in task completion message

7. **Mark task complete** (only if all evidence passes)

### Workflow 2: Code Review Verification

**When:** Reviewing another agent's code or user's PR

**Steps:**

1. **Read the code changes**

2. **Verify tests exist**
   - Are there tests for new functionality?
   - Do tests cover edge cases?
   - Are existing tests updated?

3. **Run tests**
   - Execute test suite
   - Verify exit code 0
   - Check coverage didn't decrease

4. **Check build**
   - Ensure project still builds
   - No new build errors

5. **Verify code quality**
   - Run linter
   - Run type checker
   - Check for security issues

6. **Document review evidence**
   - Use Template 3 (Code Quality Evidence)
   - Note any issues found
   - Add to context

7. **Approve or request changes**
   - Approve only if all evidence passes
   - If issues found, document them with evidence

### Workflow 3: Production Deployment Verification

**When:** Deploying to production or staging

**Steps:**

1. **Pre-deployment checks**
   - All tests pass (exit code 0)
   - Build succeeds
   - No critical linter errors
   - Security scan passes

2. **Execute deployment**
   - Run deployment command
   - Capture output

3. **Post-deployment checks**
   - Health check endpoint responds
   - Application starts successfully
   - No immediate errors in logs
   - Smoke tests pass

4. **Document deployment evidence**
   ```markdown
   ## Deployment Evidence

   **Environment:** production
   **Timestamp:** YYYY-MM-DD HH:MM:SS
   **Version:** vX.X.X

   **Pre-Deployment:**
   - Tests: ✅ Exit 0
   - Build: ✅ Exit 0
   - Security: ✅ No critical issues

   **Deployment:**
   - Command: `kubectl apply -f deployment.yaml`
   - Exit Code: 0 ✅

   **Post-Deployment:**
   - Health Check: ✅ 200 OK
   - Smoke Tests: ✅ All passed
   - Error Rate: <0.1%
   ```

5. **Verify rollback capability**
   - Ensure previous version can be restored
   - Document rollback procedure

---

## Evidence Storage

### Where to Store Evidence

**Shared Context** (Primary)
```json
{
  "quality_evidence": {
    "tests_run": true,
    "test_exit_code": 0,
    "coverage_percent": 87,
    "build_success": true,
    "build_exit_code": 0,
    "linter_errors": 0,
    "linter_warnings": 2,
    "timestamp": "2025-11-02T10:30:00Z"
  }
}
```

**Evidence Files** (Secondary)
- `.claude/quality-gates/evidence/` directory
- One file per verification run
- Format: `{type}-{timestamp}.log`
- Example: `tests-2025-11-02-103000.log`

**Task Completion Messages**
- Include evidence summary
- Link to detailed evidence files
- Example: "Task complete. Tests passed (exit 0, 87% coverage), build succeeded."

---

## Quality Standards

### Minimum Acceptable

✅ **Tests executed** with captured exit code
✅ **Timestamp** recorded
✅ **Evidence stored** in context

### Production-Grade

✅ **Tests pass** (exit code 0)
✅ **Coverage ≥70%** (or project standard)
✅ **Build succeeds** (exit code 0)
✅ **No critical linter errors**
✅ **Type checker passes**
✅ **Security scan** shows no critical issues

### Gold Standard

✅ All production-grade requirements
✅ **Coverage ≥80%**
✅ **No linter warnings**
✅ **Performance benchmarks** within thresholds
✅ **Accessibility audit** passes (WCAG 2.1 AA)
✅ **Integration tests** pass
✅ **Deployment verification** complete

---

## Common Pitfalls

### ❌ Don't Skip Evidence Collection

**Bad:**
```
"I've implemented the login feature. It should work correctly."
```

**Good:**
```
"I've implemented the login feature. Evidence:
- Tests: Exit code 0, 12 tests passed, 0 failed
- Build: Exit code 0, no errors
- Coverage: 89%
Task complete with verification."
```

### ❌ Don't Fake Evidence

**Bad:**
```
"Tests passed" (without actually running them)
```

**Good:**
```
"Tests passed. Exit code: 0
Command: npm test
Output: Test Suites: 3 passed, 3 total
Timestamp: 2025-11-02 10:30:15"
```

### ❌ Don't Ignore Failed Evidence

**Bad:**
```
"Build failed with exit code 1, but the code looks correct so marking complete."
```

**Good:**
```
"Build failed with exit code 1. Errors:
- TypeError: Cannot read property 'id' of undefined (line 42)
Fixing the error now before marking complete."
```

### ❌ Don't Collect Evidence Only Once

**Bad:**
```
"Tests passed yesterday, so the code is still good."
```

**Good:**
```
"Re-running tests after today's changes.
New evidence: Exit code 0, 45 tests passed, coverage 87%"
```

---

## Integration with Other Systems

### Context System Integration

Evidence is automatically tracked in shared context:

```typescript
// Context structure includes:
{
  quality_evidence?: {
    tests_run: boolean;
    test_exit_code?: number;
    coverage_percent?: number;
    build_success?: boolean;
    linter_errors?: number;
    timestamp: string;
  }
}
```

### Quality Gates Integration

Evidence collection feeds into quality gates:
- Quality gates check if evidence exists
- Block task completion if evidence missing
- Escalate if evidence shows failures

### Squad Mode Integration

In parallel execution:
- Each agent collects evidence independently
- Studio Coach validates evidence before sync
- Blocked tasks don't waste parallel cycles

---

## Quick Reference

### Evidence Collection Checklist

```markdown
Before marking task complete:

- [ ] Tests executed
- [ ] Test exit code captured (0 = pass)
- [ ] Build executed (if applicable)
- [ ] Build exit code captured (0 = pass)
- [ ] Code quality checks run (linter, types)
- [ ] Evidence documented with timestamp
- [ ] Evidence added to shared context
- [ ] Evidence summary in completion message
```

### Common Commands by Language/Framework

**JavaScript/TypeScript:**
```bash
npm test                 # Run tests
npm run build           # Build project
npm run lint            # Run ESLint
npm run typecheck       # Run TypeScript compiler
```

**Python:**
```bash
pytest                  # Run tests
pytest --cov           # Run tests with coverage
ruff check .           # Run linter
mypy .                 # Run type checker
```

**Rust:**
```bash
cargo test             # Run tests
cargo build            # Build project
cargo clippy           # Run linter
```

**Go:**
```bash
go test ./...          # Run tests
go build               # Build project
golangci-lint run      # Run linter
```

---

## Examples

See `/skills/evidence-verification/examples/` for:
- Sample evidence reports
- Real-world verification scenarios
- Integration examples

---

## Version History

**v1.0.0** - Initial release
- Core evidence collection templates
- Verification workflows
- Quality standards
- Integration with context system

---

**Remember:** Evidence-first development prevents hallucinations, ensures production quality, and builds confidence. When in doubt, collect more evidence, not less.
