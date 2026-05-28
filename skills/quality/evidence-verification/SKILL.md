---

# Evidence Verification
name: evidence-verification
description: Use when completing tasks, code reviews, or deployments to verify work with evidence. Collects test results, build outputs, coverage metrics, and exit codes to prove work is complete.
version: 2.0.0
author: SkillForge AI Agent Hub
tags: [quality, verification, testing, evidence, completion]
context: fork
agent: code-quality-reviewer
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash  # For running tests and capturing evidence
This skill teaches agents how to collect and verify evidence before marking tasks complete. Inspired by production-grade development practices, it ensures all claims are backed by executable proof: test results, coverage metrics, build success, and deployment verification.

**Key Principle:** Show, don't tell. No task is complete without verifiable evidence.
user-invocable: false
---

# Evidence Verification

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

# Evidence Verification

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

# Evidence Verification

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
- dist/bundle.js (245 KB)
- dist/styles.css (18 KB)

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

---

# Evidence Verification

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

# Evidence Verification

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

---

# Evidence Verification

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

---

# Evidence Verification

**Remember:** Evidence-first development prevents hallucinations, ensures production quality, and builds confidence. When in doubt, collect more evidence, not less.

## Related Skills

- `unit-testing` - Unit test patterns for generating test evidence
- `integration-testing` - Integration test patterns for component verification
- `security-scanning` - Security scan evidence collection (npm audit, pip-audit)
- `test-standards-enforcer` - Enforce evidence collection standards

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Minimum Coverage | 70% | Industry standard for production-grade code |
| Exit Code Requirement | 0 = pass | Unix standard for success/failure indication |
| Gold Standard Coverage | 80% | Higher bar for critical paths |
| Retry Before Block | 2 attempts | Allow fix attempts before escalation |

## Capability Details

### exit-code-validation
**Keywords:** exit code, return code, success, failure, status, $?, exit 0, non-zero
**Solves:**
- How do I verify command succeeded?
- Check exit codes for evidence (0 = pass)
- Validate build/test success with exit codes
- Capture command exit status in evidence

### test-evidence
**Keywords:** test results, test output, coverage report, test evidence, jest, pytest, test suite, passed, failed
**Solves:**
- How do I capture test evidence?
- Record test results in session state
- Prove tests passed with exit code 0
- Document test coverage percentage
- Capture passed/failed/skipped counts

### build-evidence
**Keywords:** build log, build output, compile, bundle, webpack, vite, cargo build, npm build
**Solves:**
- How do I capture build evidence?
- Record build success with exit code
- Verify compilation without errors
- Document build artifacts created
- Track build duration and warnings

### code-quality-evidence
**Keywords:** linter, lint, eslint, ruff, type check, mypy, typescript, code quality, warnings, errors
**Solves:**
- How do I capture code quality evidence?
- Run linter and capture results
- Execute type checker and record errors
- Document linter errors and warnings count
- Prove code quality checks passed

### deployment-evidence
**Keywords:** deployment, deploy, production, staging, health check, rollback, deployment status
**Solves:**
- How do I verify deployment succeeded?
- Check health endpoints after deploy
- Verify application started successfully
- Document deployment status and environment
- Confirm rollback capability exists

### security-scan-evidence
**Keywords:** security, vulnerability, npm audit, pip-audit, security scan, cve, critical vulnerabilities
**Solves:**
- How do I capture security scan results?
- Run npm audit or pip-audit
- Document critical vulnerabilities found
- Record security scan exit code
- Prove no critical security issues

### evidence-storage
**Keywords:** session state, state.json, evidence storage, record evidence, save results, quality_evidence, context 2.0
**Solves:**
- How do I store evidence in context?
- Update session/state.json with results
- Structure evidence data properly
- Add timestamp to evidence records
- Link to evidence log files

### combined-evidence-report
**Keywords:** evidence report, task completion, verification summary, proof of completion, comprehensive evidence
**Solves:**
- How do I create complete evidence report?
- Combine test, build, and quality evidence
- Create task completion evidence summary
- Document all verification checks run
- Provide comprehensive proof of completion

### evidence-collection-workflow
**Keywords:** evidence workflow, verification steps, evidence protocol, collection process, verification checklist
**Solves:**
- What steps to collect evidence?
- Follow evidence collection protocol
- Run all necessary verification checks
- Complete evidence checklist before marking done
- Ensure minimum evidence requirements met

### quality-standards
**Keywords:** quality standards, minimum requirements, production-grade, gold standard, evidence thresholds
**Solves:**
- What evidence is required to pass?
- Understand minimum vs production-grade standards
- Meet gold standard evidence requirements
- Know when evidence is sufficient
- Validate evidence meets project standards

### evidence-pitfalls
**Keywords:** evidence mistakes, common errors, skip evidence, fake evidence, ignore failures
**Solves:**
- What evidence mistakes to avoid?
- Never skip evidence collection
- Don't fake evidence results
- Don't ignore failed evidence
- Always re-collect after changes
