---
name: audit-tests
description: Test quality audit — event replay, GEDCOM round-trip, domain edge cases, API contracts
context: fork
agent: Explore
---

# Test Quality Audit

You are a **Test Architect** auditing the test suite for real failure-mode protection, not just coverage numbers.

## What to Do

Review test files across the codebase and evaluate whether they protect against actual failure modes.

### Step 1: Load Context

Read these files:
- `docs/TESTING-STRATEGY.md` — test organization and critical scenarios
- `docs/ARCHITECTURAL-INVARIANTS.md` — test invariants (TS-*)
- `docs/INTEGRATION-MATRIX.md` — entity completeness status

### Step 2: Check Event Sourcing Test Coverage

Search for event-related tests:
- Is every event type tested for creation, serialization, deserialization?
- Are aggregate replays tested (apply event sequence, verify state)?
- Is `DecodeEvent()` tested for all event types?
- Are projection rebuilds tested (replay from empty)?
- Is event version migration tested?

### Step 3: Check GEDCOM Round-Trip Testing

Read tests in `internal/gedcom/`:
- Is there an import → export → re-import equivalence test?
- Are edge cases covered (empty files, Unicode, non-standard tags)?
- Is data loss detection tested?
- Are GEDCOM version differences handled?

### Step 4: Check Domain Edge Cases

Read tests in `internal/domain/`:
- Are validation boundaries tested (empty strings, max lengths, invalid enums)?
- Are relationship edge cases covered (circular refs, self-referential)?
- Are date edge cases tested (partial dates, ranges)?
- Are concurrent modification scenarios tested (optimistic locking)?

### Step 5: Check API Contract Tests

Read tests in `internal/api/`:
- Do tests verify request validation (missing fields, wrong types)?
- Are error response formats tested against OpenAPI spec?
- Is pagination tested (empty, single page, multi-page, boundaries)?
- Are tests database-implementation-independent?

### Step 6: Check Cross-Feature Scenarios

Look for integration tests matching TESTING-STRATEGY.md critical scenarios:
- Entity lifecycle: create → update → query → delete → verify
- Search after create: create → search → verify appears
- Import then query: GEDCOM import → API query → verify accessible
- Dual database: same tests running against PostgreSQL and SQLite

### Step 7: Assess Test Quality

Sample 5-6 test files:
- Are tests table-driven where appropriate?
- Are assertions specific (exact values, not just `!= nil`)?
- Are test helpers organized and reusable?
- Are tests deterministic (no time-based flakiness)?
- Are tests fast (in-memory backends where possible)?

## Output Format

### Test Quality Audit Report

#### Scorecard

| Dimension | Score (0-5) | Notes |
|-----------|-------------|-------|
| ES Test Coverage | | |
| GEDCOM Round-Trip | | |
| Domain Edge Cases | | |
| API Contracts | | |
| Cross-Feature Scenarios | | |
| Test Quality | | |
| DB Parity | | |

#### Top Findings

List up to 10 findings, risk-ranked. For each:
- **Severity**: Critical / High / Medium / Low
- **Category**: Which dimension
- **Finding**: One-sentence summary
- **Evidence**: Specific files, functions, line numbers
- **Impact**: What breaks if unaddressed
- **Suggestion**: Concrete fix

#### Issue-Ready Tickets

Up to 5 GitHub-issue-ready items with title, description, acceptance criteria, affected files.

#### Manual Verification

Up to 5 items requiring human judgment.
