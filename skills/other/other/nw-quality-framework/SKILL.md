---
name: nw-quality-framework
description: Quality gates - 11 commit readiness gates, build/test protocol, validation checkpoints, and quality metrics
user-invocable: false
disable-model-invocation: true
---

# Quality Framework

## Commit Readiness Gates (11)

All pass before committing:

1. Active acceptance test passes (not skipped, not ignored)
2. All unit tests pass
3. All integration tests pass
4. All other enabled tests pass
5. Code formatting validation passes
6. Static analysis passes
7. Build validation passes (all projects)
8. No test skips in execution (ignores OK during progressive implementation)
9. Test count within behavior budget
10. No mocks inside hexagon
11. Business language in tests verified

Note: Reviewer approval (formerly Gate 12) and Testing Theater detection (formerly Gate 13) enforced at deliver-level Phase 4 (Adversarial Review via /nw-review), not per step.

## Quality Gates by Category
- **Architecture**: all layers touched | integration points validated | stack proven E2E | pipeline functional
- **Implementation**: real functionality (not placeholders) | automated pipeline | happy path coverage | production patterns
- **Business Value**: meaningful user value | testable AC | measurable success metrics
- **Real Data**: golden masters present | edge cases tested | no silent errors | API assumptions documented
- **Test Integrity**: every test falsifiable | behavioral assertions only | no circular verification | no mock-dominated tests | no assertion-free tests | no fixture theater (see below)

## Testing Theater Pattern 8: Fixture Theater

**Definition**: Acceptance tests pass because test fixtures create the expected
end-state directly, rather than exercising production code through the driving port.
Tests verify the correct outcome from the WRONG source.

**Detection**: After GREEN phase, run `git diff --name-only`. If `files_to_modify`
from the roadmap step have NO changes but tests flipped from RED to GREEN, this is
Fixture Theater. The test fixtures are implementing the feature, not production code.

**Litmus test**: Delete the new production code (or revert production files to
pre-GREEN state). If tests still pass, it's Fixture Theater.

**Prevention**:
1. Post-GREEN wiring check: every file in `files_to_modify` MUST appear in `git diff`
2. Acceptance test Given steps set up PRECONDITIONS, never the expected end-state
3. If `git diff --stat` shows only test files changed after GREEN, BLOCK the COMMIT

## Build and Test Protocol

After every TDD cycle, Mikado leaf, or atomic transformation:

```bash
# 1. BUILD
dotnet build --configuration Release --no-restore

# 2. TEST
dotnet test --configuration Release --no-build --verbosity minimal

# 2.5. QUALITY VALIDATION (before committing)
# - Edge cases tested (null, empty, malformed, boundary)
# - No silent error handling (all errors logged/alerted)
# - Real data golden masters included where applicable
# - API assumptions documented

# 3. COMMIT (if tests pass)
# Use appropriate format below

# 4. ROLLBACK (if tests fail)
git reset --hard HEAD^  # Maintain 100% green discipline
```

For commit message formats, load the collaboration-and-handoffs skill.

## Validation Checkpoints
- **Pre-work**: all tests passing | code smell detection complete | execution plan created
- **During work**: atomic transformation safety | 100% test pass rate | commit after each step | level sequence adherence
- **Post-work**: quality metrics quantified | architectural compliance validated | test suite integrity maintained

## Quality Metrics

Track: cyclomatic complexity (reduction) | maintainability index (improvement) | technical debt ratio (reduction) | test coverage (maintenance) | test effectiveness (75-80% mutation kill rate at Phase 2.25) | code smells (systematic elimination across 22 types).

For mutation testing integration, load the property-based-testing skill.

## Object Calisthenics (Application + Domain Layers)

9 design constraints for clean OOP code in the hexagonal core (Jeff Bay,
ThoughtWorks Anthology). Apply during GREEN and COMMIT phases.

### Rules

| # | Rule | Rationale | Layer |
|---|------|-----------|-------|
| 1 | One indentation level per method | Forces decomposition | Domain, Application |
| 2 | No `else` keyword | Guard clauses, early returns | Domain, Application |
| 3 | Wrap all primitives and strings | Value objects | Domain |
| 4 | First-class collections | Domain collection types | Domain |
| 5 | One dot per line | Law of Demeter | Domain, Application |
| 6 | No abbreviations | Intention-revealing names | All |
| 7 | Small entities (<50 LOC classes, <10 LOC methods) | SRP | Domain, Application |
| 8 | Max 2 instance variables per class | Promotes decomposition | Domain |
| 9 | No getters/setters | Tell, don't ask | Domain, Application |

### Rule 9 Relaxation Policy

Getters are acceptable in these cases:
- DTOs/response objects at port boundaries (serialization needs)
- CQRS read models (query-optimized projections)
- Value objects with computed properties (e.g., Money.amount)
- Framework requirements (ORM mapping, serialization)

Rule 9 applies strictly to domain entities and application services.
Behavior through commands, not data access.

### Scope

- Applies to: Domain layer, Application layer (inside the hexagon)
- Does NOT apply to: Adapters, infrastructure, DTOs, configuration
- Enforcement phase: GREEN (writing new code) + COMMIT (refactoring)

## Dimension 9: Environmental Realism

### 9a: WS Strategy Audit

- Is the WS strategy declared in wave-decisions.md? (A/B/C/D)
- Does the WS implementation match the declared strategy?
- For strategies B/D: is CI configured to run with real adapters?

### 9b: Adapter Coverage Audit (Structured Table)

For EVERY driven port adapter, complete this table:

| Port | InMemory Behavior | Cannot Model | Covered By |
|------|-------------------|-------------|------------|
| (port name) | (what InMemory returns) | (real condition it can't model) | (test name that covers the gap) |

If "Covered By" is empty for any row, the test suite has a blind spot. Flag as HIGH.

### 9d: Test Double Input Validation Audit

For EVERY InMemory test double, verify it validates inputs like the real adapter:

| Test Double | Validates None? | Validates empty strings? | Validates ranges? | Matches real preconditions? |
|-------------|----------------|------------------------|-------------------|---------------------------|
| (double name) | YES/NO | YES/NO | YES/NO | YES/NO |

If any cell is NO, the test double is a liar — it accepts inputs the real adapter rejects. Flag as HIGH.

A permissive test double creates invisible wiring bugs: tests pass, production crashes.

### 9c: External Boundary Audit

For EVERY external system (subprocess, API, DB):
- Is there a contract or smoke test?
- Is it in CI or local-only?
- What is the cost per run?

Consequence rules:
- No contract or smoke test for an external system → flag as HIGH
- Contract test is local-only for a CI-triggered adapter → flag as HIGH
- Cost per run undocumented → flag as MEDIUM
