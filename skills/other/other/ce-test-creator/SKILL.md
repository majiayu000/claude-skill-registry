---
name: ce-test-creator
description: >
  Design tests to close documented coverage gaps identified by gap analysis,
  without padding. Adapts recommendations for Option A/B/C in the Test Quality
  Method. Use ce-test-author to write tests for already-known targets.
---

# CE Test Creator

This skill implements the **Test Creator** role from ADR-030 and mirrors the
prompt in `docs/improvement/test-quality-method/test_creator.md`.

## Required references

- `docs/improvement/test-quality-method/README.md` (canonical method + options)
- `docs/improvement/test-quality-method/test_creator.md` (full role prompt)

## Use this skill when

- Closing documented coverage gaps.
- Replacing low-value tests with stronger behavioral coverage.
- Adding missing exception, serialization, or contract tests.

## Focus option handling

- **Option A (Test-Focused):** run the full gap-closing workflow.
- **Option B (Code-Focused):** only propose targeted tests when code-focused
  changes expose a coverage-gate failure; otherwise return "no new tests needed."
- **Option C (Full Cycle):** run Option A and coordinate with code-focused
  findings to avoid adding tests that duplicate soon-to-be-pruned paths.

## Core rule

Every new test must add meaningful signal:
- covers unique lines, or
- introduces unique parameter/assertion behavior.

## Workflow

1. Confirm the selected focus option (`A`, `B`, or `C`) and scope work accordingly.
2. Analyze gaps:

```bash
python scripts/over_testing/gap_analyzer.py
python scripts/quality/check_coverage_gates.py
```

3. Prioritize targets:
- Tier 1: public API error paths, serialization round-trips, boundary behavior.
- Tier 2: parameter combinations that exercise distinct contracts.
- Tier 3: expensive integration/viz paths (only when needed).

4. Design tests for behavioral specificity:
- use public APIs only
- assert outputs/side effects, not just object existence
- parameterize where duplication risk is high

5. Cross-check with existing coverage artifacts to avoid duplicates.

## Output contract

For each proposed test include:
- target behavior
- target module/function
- why existing tests do not already cover it
- expected coverage/quality gain
- selected focus option (`A`, `B`, or `C`) and why the proposal fits it

## Constraints

- Avoid implementation-detail coupling.
- Avoid coverage padding.
- Route proposals through `ce-devils-advocate` for risk challenge before
  large batch changes.
