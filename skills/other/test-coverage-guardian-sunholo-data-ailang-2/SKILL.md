---
name: Test Coverage Guardian
description: Analyze test coverage, identify gaps, detect dead code, and improve test quality. Use when user asks to check coverage, review tests, find untested code, or improve test robustness.
---

# Test Coverage Guardian

Analyze and improve test coverage for the AILANG codebase.

## Quick Start

**Most common usage:**
```bash
# Quick coverage check
make test-coverage-badge  # Shows: "Coverage: 29.9%"

# Detailed coverage report
make test-coverage        # Generates HTML report

# Coverage for specific package
go test -cover ./internal/parser/...
```

## When to Use This Skill

Invoke when user says:
- "Check test coverage"
- "What's untested?"
- "Review the test suite"
- "Find dead code"
- "Tests keep breaking" (brittleness analysis)

## Coverage Commands

### Quick Check
```bash
make test-coverage-badge
# Output: Coverage: 29.9%
```

### Detailed HTML Report
```bash
make test-coverage
# Opens: coverage.html in browser
```

### Per-Package Coverage
```bash
go test -cover ./internal/parser/...
go test -cover ./internal/types/...
go test -cover ./internal/eval/...
```

### Coverage with Profile
```bash
go test -coverprofile=coverage.out ./...
go tool cover -func=coverage.out | grep -E "^total:|0\.0%"
```

## Coverage Standards

| Module | Target | Priority |
|--------|--------|----------|
| lexer | 80%+ | High |
| parser | 80%+ | High |
| types | 80%+ | High |
| eval | 70%+ | Medium |
| effects | 70%+ | Medium |
| repl | 50%+ | Low |

**Critical paths (100% target):**
- Type inference
- Effect checking
- Pattern matching exhaustiveness

## Analysis Workflow

### Step 1: Get Current Coverage

```bash
# Overall coverage
make test-coverage-badge

# Per-package breakdown
go test -cover ./internal/... 2>&1 | grep -E "coverage:|ok"
```

### Step 2: Identify Gaps

```bash
# Find 0% coverage functions
go test -coverprofile=coverage.out ./...
go tool cover -func=coverage.out | grep "0.0%"

# Visual inspection
go tool cover -html=coverage.out
```

### Step 3: Categorize Gaps

| Category | Action |
|----------|--------|
| Core logic uncovered | Write tests (high priority) |
| Error paths uncovered | Add error case tests |
| Dead code (never called) | Consider removal |
| Experimental code | Accept lower coverage |

### Step 4: Report Findings

```markdown
## Coverage Report

### Summary
- Overall: 29.9%
- Core modules: 45%
- Target: 50%+ overall, 80%+ core

### Critical Gaps
1. internal/types/unify.go - row polymorphism (0%)
2. internal/eval/effects.go - effect handlers (15%)

### Dead Code Candidates
- internal/legacy/old_parser.go (0%, no references)

### Recommendations
1. Add unification tests for row types
2. Add effect handler integration tests
3. Remove legacy parser code
```

## Test Quality Checklist

### Anti-Brittleness
- [ ] Tests public APIs, not private implementation
- [ ] Uses interface-based testing where appropriate
- [ ] Tests error types, not exact messages
- [ ] Mocks external dependencies at boundaries
- [ ] Tests behavior, not call sequences

### Good Patterns
- [ ] Table-driven tests for comprehensive inputs
- [ ] Property-based tests for invariants
- [ ] Error path testing
- [ ] Integration tests at module boundaries

### AILANG-Specific
- [ ] Expression-based tests (everything returns value)
- [ ] Effect tracking tests
- [ ] Pattern matching exhaustiveness tests
- [ ] Deterministic execution tests

## CI/CD Monitoring

```bash
# View recent CI runs
gh run list --limit 10

# Check failed run
gh run view <run-id> --log-failed

# Watch run in progress
gh run watch <run-id>
```

**Common CI failures:**
- Example validation failures
- Module path issues
- Coverage regressions

## Example Session

**User**: "Check test coverage"

**Response**:
```
Running coverage analysis...

## Coverage Report

### Overall: 29.9%

### Per-Module Breakdown
  internal/lexer:    85.2%  (good)
  internal/parser:   42.1%  (needs work)
  internal/types:    38.5%  (needs work)
  internal/eval:     25.3%  (low)
  internal/effects:  18.7%  (low)

### Critical Gaps (0% coverage)
1. internal/types/row.go:UnifyRows() - row polymorphism
2. internal/eval/match.go:matchADT() - ADT pattern matching
3. internal/effects/budget.go - entire file

### Recommendations
1. Priority: Add tests for UnifyRows (critical for type system)
2. Add ADT matching tests
3. Review effects/budget.go - possibly dead code

Would you like me to generate test stubs for any of these?
```

## Quality Gates

- No PR should decrease overall coverage
- New features must include tests
- Bug fixes must include regression tests
- Breaking changes require test updates

## Tips

- **Focus on branch coverage**, not just line coverage
- **Test the sad path** - error conditions matter
- **Golden tests** for complex outputs (parser, codegen)
- **Property tests** for mathematical invariants
