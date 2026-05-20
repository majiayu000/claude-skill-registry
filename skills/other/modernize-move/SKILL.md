---
name: modernize-move
description: >-
  Detects and modernizes outdated Move V1 syntax, patterns, and APIs to Move V2+. Use when upgrading legacy contracts,
  migrating to modern syntax, or converting old patterns to current best practices. NOT for writing new contracts (use
  write-contracts) or fixing bugs.
license: MIT
metadata:
  author: aptos-labs
  version: "1.0"
  category: move
  tags: ["modernization", "migration", "v2", "refactoring", "syntax"]
  priority: high
allowed-tools: Read Glob Grep Write Edit Bash AskUserQuestion
---

# Skill: modernize-move

Detect and modernize outdated Move V1 syntax, patterns, and APIs to Move V2+. Preserves correctness through tiered
transformations with test verification after each tier.

## Essential Principles

Five non-negotiable rules for every modernization:

1. **Test safety net is mandatory** WHY: Modernization must preserve behavior. No tests = no safety net. If no tests
   exist, invoke `generate-tests` skill first to create comprehensive tests before making any changes.

2. **Analyze before modifying** WHY: The user must see exactly what will change and confirm the scope. Never
   surprise-edit code. Present the full analysis report and wait for confirmation.

3. **Tiered execution order** WHY: Syntax changes (Tier 1) are zero-risk. API migrations (Tier 3) change semantics.
   Always apply safest changes first so riskier changes build on a clean, verified foundation.

4. **Verify after each tier** WHY: If tests break, you know exactly which tier caused it. Revert that tier and
   investigate before proceeding. Never apply the next tier on a broken baseline.

5. **Preserve error code values** WHY: Tests use `#[expected_failure(abort_code = N)]`. Changing numeric values breaks
   tests silently. When creating named constants, the numeric value MUST match the original literal.

## When to Use This Skill

- Upgrading Move V1 contracts to V2 syntax
- Migrating `public(friend)` to `package fun`
- Converting `vector::borrow` to index notation
- Converting `while` loops with counters to `for` range loops
- Replacing manual vector iteration with stdlib inline functions (`vector::for_each_ref`, `vector::map`, `vector::fold`,
  etc.) and lambdas
- Replacing magic abort numbers with named constants
- Migrating legacy `coin`/`TokenV1` to modern `fungible_asset`/Digital Assets
- Converting `EventHandle` to `#[event]` pattern
- Upgrading custom signed integer workarounds to native `i8`-`i256` types

## When NOT to Use This Skill

- **Writing new contracts from scratch** — use `write-contracts`
- **Fixing bugs or adding features** — modernization is structural, not functional
- **Optimizing gas usage** — use `analyze-gas-optimization`
- **Auditing security** — use `security-audit` (run AFTER modernization)

## Workflow

### Phase 1: Analyze Contract

**Entry:** User provides a Move contract or project to modernize.

**Actions:**

1. Read all contract source files (`.move` files in `sources/`)
2. Scan for V1 patterns using detection rules from [detection-rules.md](references/detection-rules.md):
   - Grep for Tier 1 patterns (syntax) — highest confidence, most common
   - Grep for Tier 2 patterns (visibility, errors, events)
   - Grep for Tier 3 patterns (API migrations) — flag for manual review
3. Cross-reference coupled patterns (T3-09+T3-10)
4. Categorize each finding: line number, rule ID, pattern name, proposed change, tier, confidence
5. Build the Analysis Report

**Exit:** Analysis Report ready for presentation.

### Phase 2: Present Analysis (GATE 1)

**Entry:** Analysis Report complete.

**Actions:**

1. Present the full Analysis Report to the user in this format:

```
## Modernization Analysis Report

### Summary
- Tier 1 (Syntax): X findings
- Tier 2 (Visibility & Errors): X findings
- Tier 3 (API Migrations): X findings

### Findings

| # | File:Line | Rule | Pattern | Proposed Change | Tier | Confidence |
|---|-----------|------|---------|-----------------|------|------------|
| 1 | src/mod.move:15 | T1-01 | vector::borrow | → index notation | 1 | High |
| ... | ... | ... | ... | ... | ... | ... |

### Tier 3 Warnings (if any)
- T3-03: coin → fungible_asset migration is a major rewrite (X locations)
```

2. Ask the user to choose scope:
   - **`syntax-only`** (Tier 1 only) — zero risk, just cleaner syntax
   - **`standard`** (Tier 1 + Tier 2) — recommended default, syntax + visibility + error constants
   - **`full`** (all tiers) — includes API migrations, higher risk
3. Highlight any Tier 3 items that require major rewrites
4. If scope includes Tier 3, ask the user about deployment context:
   - **Compatible** — Upgrading an already-deployed contract. Breaking changes are excluded even if the scope includes
     them. Rules marked ⚠ Breaking are skipped.
   - **Fresh deploy** — New deployment or willing to redeploy. All changes in the selected scope are applied including
     breaking changes.

**Exit:** User has confirmed scope (and deployment context if Tier 3 is included). Do NOT proceed until confirmed.

### Phase 3: Establish Test Safety Net

**Entry:** User confirmed scope.

**Actions:**

1. Search for existing tests:
   - `#[test_only]` modules within source files
   - `*_tests.move` files
   - `tests/` directory
2. If **no tests found**: stop and invoke `generate-tests` skill to create comprehensive tests first, then return here
3. Run `aptos move test` to establish a passing baseline
4. Record baseline: number of tests, all passing status

**Exit:** All tests pass. Baseline recorded. If tests fail pre-modernization, stop and address test failures first — do
not modernize on a broken test suite.

### Phase 4: Apply Transformations (with Feedback Loops)

**Entry:** Test baseline established.

**Actions — apply in tier order:**

**Tier 1 (if scope includes it — always):**

1. Apply all Tier 1 syntax changes per [transformation-guide.md](references/transformation-guide.md)
2. Run `aptos move test`
3. If tests fail → revert all Tier 1 changes, investigate which specific change caused failure, fix and retry

**Tier 2 (if scope is `standard` or `full`):** 4. Apply all Tier 2 changes per transformation guide 5. Run
`aptos move test` 6. If tests fail → revert all Tier 2 changes, investigate and fix

**Tier 3 (if scope is `full` only):** 7. Apply Tier 3 changes ONE AT A TIME (not all at once)

- If deployment context is `compatible`: skip any rule marked **⚠ Breaking**. Add to the skipped list with reason
  "breaking change, excluded in compatible mode."
- If deployment context is `fresh deploy`: apply all rules in scope normally.

8. Run `aptos move test` after EACH individual Tier 3 change
9. If tests fail → revert that specific change, note it as skipped, proceed to next Tier 3 item

**Exit:** All approved changes applied, all tests passing.

### Phase 5: Final Verification

**Entry:** All transformations applied.

**Actions:**

1. Run `aptos move test --coverage`
2. Verify test coverage is >= baseline (should be same or better)
3. Generate Modernization Summary Report:

```
## Modernization Summary

### Changes Applied
- Tier 1: X changes (syntax)
- Tier 2: X changes (visibility & errors)
- Tier 3: X changes (API migrations)

### Changes Skipped
- [List any skipped items with reasons]

### Test Results
- Tests: X passing (baseline: Y)
- Coverage: X% (baseline: Y%)

### Files Modified
- [List of modified files]
```

**Exit:** Report presented to user.

## Modernization Scope Quick Reference

| Scope         | Tiers      | Risk        | When to Use                                        |
| ------------- | ---------- | ----------- | -------------------------------------------------- |
| `syntax-only` | Tier 1     | Zero        | Just clean up syntax, no semantic changes          |
| `standard`    | Tier 1+2   | Low         | **Default.** Syntax + visibility + error constants |
| `full`        | Tier 1+2+3 | Medium-High | Full migration including API changes               |

## Tier Quick Reference

| Tier                    | What Changes                                                           | Risk        | Examples                                                                                                                                                          |
| ----------------------- | ---------------------------------------------------------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 — Syntax              | Code reads differently, compiles identically                           | Zero        | `vector::borrow(&v, i)` → `v[i]`, `x = x + 1` → `x += 1`, `while (i < n) { ... i += 1 }` → `for (i in 0..n) { ... }`                                              |
| 2 — Visibility & Errors | Same semantics, cleaner declarations                                   | Low         | `public(friend)` → `package fun`, magic numbers → `E_*` constants                                                                                                 |
| 3 — API Migrations      | Different APIs, same intended behavior. Most are **breaking changes**. | Medium-High | `coin` → `fungible_asset`, `SmartTable` → `BigOrderedMap`, `EventHandle` → `#[event]`, manual loops → stdlib `v.for_each_ref()`/`v.map()`/`v.fold()` with lambdas |

See [detection-rules.md](references/detection-rules.md) for the complete rule catalog (22 rules across 3 tiers).

## Rationalizations to Reject

| Rationalization                                  | Why It's Wrong                                                                 |
| ------------------------------------------------ | ------------------------------------------------------------------------------ |
| "Tests pass so the modernization is correct"     | Tests verify behavior, not code quality. Review changes manually too.          |
| "This contract is simple, skip the analysis"     | Simple contracts can have subtle patterns. Always analyze first.               |
| "Let's do all tiers at once to save time"        | If tests break, you can't isolate which change caused it. Always tier.         |
| "The receiver-style call looks right"            | Must verify the target function declares `self`. False positives are common.   |
| "Error constants can have new names and values"  | Existing tests depend on exact numeric values. Preserve them.                  |
| "No tests exist, but the changes are safe"       | Without tests there is no safety net. Generate tests first.                    |
| "Tier 3 changes are optional, skip the test run" | Every change needs verification. Tier 3 is highest risk — test MORE, not less. |

## Success Criteria

- [ ] Analysis Report presented before any modifications
- [ ] User confirmed modernization scope
- [ ] Test baseline established before changes
- [ ] Tests pass after each tier of changes
- [ ] All error code numeric values preserved
- [ ] No Tier 3 changes applied without `full` scope confirmation
- [ ] Breaking changes excluded when user selected compatible mode
- [ ] Modernization Summary Report generated
- [ ] Test coverage maintained at or above baseline

## Reference Index

| File                                                          | Content                                                         |
| ------------------------------------------------------------- | --------------------------------------------------------------- |
| [detection-rules.md](references/detection-rules.md)           | Complete V1 pattern detection catalog (22 rules across 3 tiers) |
| [transformation-guide.md](references/transformation-guide.md) | Before/after code, safety checks, edge cases per rule           |
| [MOVE_V2_SYNTAX.md](../../../patterns/move/MOVE_V2_SYNTAX.md) | Full V2 syntax reference                                        |
| [OBJECTS.md](../../../patterns/move/OBJECTS.md)               | Modern object model patterns                                    |
| [ADVANCED_TYPES.md](../../../patterns/move/ADVANCED_TYPES.md) | Enums, signed integers, phantom types                           |

**Related skills:** `generate-tests`, `write-contracts`, `security-audit`
