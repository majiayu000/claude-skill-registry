---
name: quality-code-review
description: Perform systematic self-review of code changes before commits using structured
  checklist. Validates architecture boundaries, code quality, test coverage, documentation,
  and project-specific anti-patterns. Use before committing, creating PRs, or when
  user says "review my changes", "self-review", "check my code". Adapts to Python,
  JavaScript, TypeScript, Go, Rust projects.
allowed-tools:
- Read
- Bash
- Grep
- Glob
- Skill
---

# Self Code Review

## Quick Start

Perform systematic self-review of code changes before commits using a structured 8-step checklist.

**Most common use case:**
```
User: "Review my changes before I commit"

→ Run git diff to see changes
→ Execute 8-step review (architecture, quality, tests, docs, anti-patterns, gates)
→ Generate structured report with pass/fail/warnings
→ Fix issues before committing

Result: Clean, quality-validated commit
```

## When to Use This Skill

**Mandatory situations:**
- Before every commit
- Before creating pull requests
- Before merging to main/master
- After completing feature implementation

**User trigger phrases:**
- "review my changes"
- "self-review"
- "check my code"
- "validate before commit"
- "code review"
- "ready to commit?"

## What This Skill Does

Systematic 8-step review process:

1. **Change Discovery** - Identify all modified files via git diff
2. **Architectural Review** - Validate layer boundaries and dependency rules
3. **Code Quality Review** - Check style, logic, performance, security
4. **Test Coverage Review** - Ensure comprehensive test coverage
5. **Documentation Review** - Validate docstrings, README, comments
6. **Anti-Pattern Detection** - Find universal and project-specific anti-patterns
7. **Quality Gates** - Run automated checks (mypy, ruff, pytest)
8. **Review Report Generation** - Structured pass/fail/warning summary

## Review Process

### Step 1: Change Discovery

**Identify modified files:**
```bash
# See all changes
git diff --name-only

# See detailed changes
git diff

# See staged changes
git diff --staged
```

**Output:** List of modified files for review

### Step 2: Architectural Review

**Check layer boundaries (Clean Architecture projects):**
- Domain layer has no external dependencies
- Application layer doesn't import from infrastructure
- Infrastructure implements interfaces from domain
- Interface layer depends only on application/infrastructure

**Use validate-architecture skill if available**

**Checklist:**
- [ ] No circular dependencies between layers
- [ ] Domain layer imports only from domain
- [ ] Application imports from domain only
- [ ] Infrastructure implements domain protocols
- [ ] No business logic in interface layer

### Step 3: Code Quality Review

**Style & Clarity:**
- [ ] Naming is clear and consistent with project conventions
- [ ] Functions/methods are single-purpose (SRP)
- [ ] No magic numbers (use named constants)
- [ ] No commented-out code
- [ ] Proper indentation and formatting

**Logic & Correctness:**
- [ ] Edge cases handled (empty inputs, null, zero)
- [ ] Error handling uses project patterns (ServiceResult, exceptions)
- [ ] No off-by-one errors in loops
- [ ] Proper null/None checks
- [ ] No mutable default arguments (Python)

**Performance:**
- [ ] No N+1 queries (database operations)
- [ ] Appropriate data structures (list vs set vs dict)
- [ ] No unnecessary loops or repeated calculations
- [ ] Lazy evaluation where appropriate

**Security:**
- [ ] No SQL injection risks (use parameterized queries)
- [ ] No hardcoded secrets (API keys, passwords)
- [ ] Input validation for user-provided data
- [ ] Proper authentication/authorization checks

### Step 4: Test Coverage Review

**Required test types:**
1. **Unit tests** - Test business logic in isolation
2. **Integration tests** - Test with real dependencies (if applicable)
3. **E2E tests** - Test through public interface (if applicable)

**Coverage checklist:**
- [ ] Happy path tested
- [ ] Edge cases tested (empty, null, boundary values)
- [ ] Error cases tested (failures, exceptions)
- [ ] All public methods/functions tested
- [ ] Coverage 80%+ for new code

**Run tests:**
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

### Step 5: Documentation Review

**Docstrings:**
- [ ] All public functions/classes have docstrings
- [ ] Docstrings describe purpose (not implementation)
- [ ] Complex logic has inline comments explaining "why" not "what"
- [ ] No redundant docstrings (don't repeat what code says)

**README updates:**
- [ ] New features documented
- [ ] API changes reflected
- [ ] Examples updated if needed

### Step 6: Anti-Pattern Detection

**Universal anti-patterns:**

1. **God Classes** - Classes with 10+ methods or 300+ lines
2. **Long Methods** - Functions 50+ lines
3. **Deep Nesting** - 4+ levels of indentation
4. **Duplicate Code** - Same logic in multiple places
5. **Magic Numbers** - Unexplained constants
6. **Commented Code** - Code commented out instead of deleted
7. **Inconsistent Naming** - Mixed conventions (camelCase vs snake_case)
8. **Mutable Defaults** (Python) - `def func(arg=[])`
9. **Bare Except** - `except:` without specific exception
10. **Missing Type Hints** (Python/TypeScript) - Functions without types

**Project-specific anti-patterns** (check ARCHITECTURE.md):
- Fail-fast violations (try/except around imports)
- Missing ServiceResult usage
- Direct database access (bypassing repository)
- Missing dependency injection
- Skipping validation in constructors

### Step 7: Quality Gates

**Run automated checks:**
```bash
# Type checking
mypy src/

# Linting
ruff check src/

# Tests
pytest tests/

# Coverage
pytest --cov=src --cov-report=term-missing
```

**Pass criteria:**
- [ ] 0 type errors
- [ ] 0 linting errors (or justified suppressions)
- [ ] All tests passing
- [ ] Coverage 80%+ for new code

### Step 8: Review Report Generation

Generate structured report with findings:

**Report template:**
```
## Code Review Report

### Passed Checks (N/8)
- ✅ Change Discovery: 5 files modified
- ✅ Architectural Review: No layer boundary violations
- ✅ Code Quality: No style/logic issues
- ✅ Test Coverage: 85% coverage, all cases tested
- ✅ Documentation: All public APIs documented
- ✅ Anti-Patterns: No universal anti-patterns detected
- ✅ Quality Gates: mypy, ruff, pytest all passing

### Failed Checks (N/8)
- ❌ Test Coverage: Missing edge case tests for empty input
- ❌ Quality Gates: 2 mypy type errors in handlers.py

### Warnings (N)
- ⚠️ Performance: Potential N+1 query in repository method
- ⚠️ Documentation: README not updated for new feature

### Summary
- **Status:** BLOCKED (2 failures)
- **Action Required:**
  1. Add edge case tests for empty input
  2. Fix type errors in handlers.py
  3. Review N+1 query issue
  4. Update README

**DO NOT COMMIT** until all failures resolved.
```

## Integration with Other Skills

**Combine with other validation skills:**

- **validate-architecture** - Automated layer boundary checking
- **run-quality-gates** - Comprehensive quality validation
- **detect-refactor-markers** - Find REFACTOR comments and associated ADRs
- **detect-srp** - Find Single Responsibility Principle violations
- **verify-integration** - Ensure components are connected, not just created

**Workflow:**
1. Make changes
2. Run `quality-code-review` skill (this skill)
3. If architecture issues found → Use `validate-architecture` for details
4. Fix all issues
5. Run `quality-code-review` again
6. Commit when all checks pass

## Language-Specific Adaptations

### Python Projects
**Additional checks:**
- Type hints on all functions (mypy --strict)
- No mutable default arguments
- Proper `__init__` validation
- Use `Protocol` for interfaces
- Dataclasses for value objects

### JavaScript/TypeScript Projects
**Additional checks:**
- TypeScript strict mode enabled
- No `any` types (use proper types)
- Proper error handling (no silent failures)
- ESLint rules passing
- Jest tests with 80%+ coverage

### Go Projects
**Additional checks:**
- Error handling for all errors (no ignored `err`)
- Proper struct naming (exported vs unexported)
- Tests in `_test.go` files
- No global state (use dependency injection)

### Rust Projects
**Additional checks:**
- No `unwrap()` in production code (handle Results)
- Proper error propagation with `?`
- Clippy warnings addressed
- All tests passing

## Expected Outcomes

### All Checks Passing

```
## Code Review Report

### Passed Checks (8/8)
- ✅ Change Discovery: 3 files modified
- ✅ Architectural Review: No violations
- ✅ Code Quality: Clean code, no issues
- ✅ Test Coverage: 92% coverage
- ✅ Documentation: All APIs documented
- ✅ Anti-Patterns: None detected
- ✅ Quality Gates: All passing
- ✅ Report Generated: Review complete

### Summary
- **Status:** READY TO COMMIT
- **Changes:** 3 files, 150 lines added, 20 lines deleted
- **Test Coverage:** 92% (target 80%+)
- **Quality:** All gates passing

PROCEED WITH COMMIT
```

### Checks Failing

```
## Code Review Report

### Passed Checks (5/8)
- ✅ Change Discovery: 5 files modified
- ✅ Architectural Review: No violations
- ✅ Documentation: Properly documented

### Failed Checks (3/8)
- ❌ Test Coverage: Only 45% coverage (target 80%+)
  - Missing tests for error scenarios
  - No integration tests
- ❌ Quality Gates: 3 mypy type errors
  - src/handlers.py:45 - Missing return type
  - src/models.py:12 - Incompatible types
- ❌ Anti-Patterns: 2 issues
  - God class detected: UserService (18 methods)
  - Duplicate code in parse_input() and validate_input()

### Summary
- **Status:** BLOCKED
- **Action Required:**
  1. Add tests for error scenarios (increase coverage to 80%+)
  2. Fix 3 mypy type errors
  3. Refactor UserService (split responsibilities)
  4. Extract common parsing logic to shared utility

DO NOT COMMIT - Fix issues first
```

## Troubleshooting

### Issue: Quality gates failing with many errors

**Symptom:** mypy/ruff/pytest show 10+ errors

**Solution:**
1. Fix one category at a time (start with type errors)
2. Run incremental checks: `mypy src/module.py`
3. Use `ruff check --fix` for auto-fixable issues
4. Prioritize test failures (may cascade from type issues)

### Issue: Low test coverage but tests exist

**Symptom:** Coverage 40-60% despite writing tests

**Solution:**
- Check which lines aren't covered: `pytest --cov=src --cov-report=html`
- Open `htmlcov/index.html` to see missing lines
- Add tests for error branches and edge cases
- Test all public methods, not just happy path

### Issue: Architecture violations unclear

**Symptom:** "Layer boundary violation detected" but unsure where

**Solution:**
- Use `validate-architecture` skill for detailed analysis
- Check import statements in flagged files
- Review ARCHITECTURE.md for project-specific rules
- Compare with existing code in same layer

## Supporting Files

- **[references/review-checklist.md](references/review-checklist.md)** - Comprehensive checklists:
  - Detailed language-specific checks (Python, JS/TS, Go, Rust)
  - Project-specific anti-pattern catalog
  - Security checklist (OWASP top 10)
  - Performance optimization checklist
  - Accessibility checklist (for UI code)

- **[scripts/run-review.sh](scripts/run-review.sh)** - Automated review script:
  - Runs all quality gates
  - Generates coverage report
  - Checks git diff
  - Outputs structured report

## Red Flags to Avoid

1. **Skipping review before commits** - Technical debt compounds
2. **Ignoring quality gate failures** - "I'll fix it later" never happens
3. **Reviewing only happy path** - Edge cases cause production bugs
4. **Skipping test coverage check** - Untested code will break
5. **Approving own code without checklist** - Systematic review catches issues
6. **Committing with failing tests** - Breaks CI/CD pipeline
7. **Ignoring architectural violations** - Erodes system design over time
8. **Skipping documentation updates** - Makes code unmaintainable
9. **Accepting "good enough" code** - Quality degrades incrementally
10. **Not using automated tools** - Manual review misses issues

---

**Key principle:** Systematic review catches issues before they reach production. 10 minutes of review saves hours of debugging.

**Remember:** Every commit is a checkpoint. Make each one clean, tested, and production-ready.
