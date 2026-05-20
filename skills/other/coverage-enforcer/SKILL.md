---
name: vibe-coverage-enforcer
description: Enforces tiered test coverage standards with three dimensions — line coverage by tier, spec-to-test traceability, and spec-to-code implementation mapping. Use before claiming code is complete.
user-invocable: true
---

# vibe-coverage-enforcer

Coverage numbers don't guarantee quality, but low coverage guarantees surprise.

## When to Use This Skill

- Before claiming a feature is complete
- After writing tests, to verify coverage meets standards
- During periodic coverage health checks
- When deciding "do I need more tests?"
- After `vibe-spec-sync` updates the spec — verify tests still cover requirements

## When NOT to Use This Skill

- Prototype/spike code that will be rewritten
- Generated code (API clients, schema types)
- Configuration files
- When the user explicitly says coverage isn't a priority for this task

## Three Coverage Dimensions

### Dimension 1: Line Coverage (by Tier)

Not all code needs the same coverage:

| Tier | Target | What's Included |
|------|--------|----------------|
| **Critical** | >=90% | Security, authentication, authorization, payment/billing, data integrity, encryption |
| **Business** | >=80% | Core business logic, API handlers, state management, validation |
| **General** | >=70% | Utilities, formatting, UI components, logging |
| **Exempt** | N/A | Generated code, test helpers, one-time scripts |

### Dimension 2: Spec-to-Test Coverage

Which spec requirements have corresponding tests?

1. **Parse requirements** from the spec document — each atomic requirement gets an ID
2. **Scan test files** for traceability markers:
   - Comment markers: `# req:[REQ-ID]` or `// req:[REQ-ID]`
   - Function name patterns: `test_req_[REQ-ID]_*`
3. **Map**: requirement → test function(s) or UNCOVERED
4. **Report**: X/N requirements covered (Y%)

### Dimension 3: Spec-to-Code Coverage

Which spec requirements have corresponding implementations?

1. **For each requirement**, search the codebase for implementing code
2. **Evidence**: Note which file(s) and function(s) implement each requirement
3. **Map**: requirement → implementation location(s) or NOT_IMPLEMENTED
4. **Report**: X/N requirements implemented (Y%)

## Steps

1. **Run line coverage** for the project:
   - Go: `go test -cover ./...` or `go test -coverprofile=coverage.out ./...`
   - JS/TS: `npm test -- --coverage`
   - Python: `pytest --cov`

2. **Classify packages/modules** into tiers

3. **Compare actual vs. target** for each package (Dimension 1)

4. **If a spec document exists**, run Dimensions 2 and 3:
   - Find the spec (same logic as `vibe-spec-sync` Step 1)
   - Extract requirements with IDs
   - Scan tests for traceability markers
   - Map requirements to implementations

5. **Report all dimensions**

## Output Format

### Coverage Report

#### Dimension 1: Line Coverage

**Overall**: X%

| Package/Module | Tier | Actual | Target | Status |
|---------------|------|--------|--------|--------|
| auth/ | Critical | 92% | 90% | PASS |
| handlers/ | Business | 75% | 80% | FAIL (-5%) |
| utils/ | General | 68% | 70% | FAIL (-2%) |

#### Dimension 2: Spec-to-Test Coverage

**Spec**: [path/to/spec.md]
**Requirements Covered**: X/N (Y%)

| REQ ID | Requirement | Test(s) | Status |
|--------|-------------|---------|--------|
| AUTH-001 | Login requires email + password | test_login_credentials | COVERED |
| AUTH-002 | Lockout after 5 failed attempts | — | UNCOVERED |
| CACHE-001 | Cache TTL is 24 hours | test_req_CACHE001_ttl | COVERED |

#### Dimension 3: Spec-to-Code Coverage

**Requirements Implemented**: X/N (Y%)

| REQ ID | Requirement | Implementation | Status |
|--------|-------------|---------------|--------|
| AUTH-001 | Login requires email + password | src/auth.py:login() | IMPLEMENTED |
| AUTH-002 | Lockout after 5 failed attempts | — | NOT IMPLEMENTED |
| CACHE-001 | Cache TTL is 24 hours | src/cache.py:get() | IMPLEMENTED |

### Summary

| Dimension | Score | Target | Status |
|-----------|-------|--------|--------|
| Line Coverage (Critical) | 92% | 90% | PASS |
| Line Coverage (Business) | 75% | 80% | FAIL |
| Line Coverage (General) | 68% | 70% | FAIL |
| Spec-to-Test | 8/12 (67%) | 100% | FAIL |
| Spec-to-Code | 10/12 (83%) | 100% | FAIL |

### Action Required
1. `handlers/` needs +5% line coverage — suggest testing: [specific untested functions]
2. AUTH-002 not implemented and not tested — implement first, then test
3. 4 requirements lack tests — run `vibe-adversarial-test-generation` in spec-driven mode

### Suggested Tests
```
[Specific test skeletons for uncovered requirements, with req:[ID] markers]
```
