---
name: sdd-verify
description: |
  Verify SDD integrity: traceability links AND test coverage.
  Use when: checking document integrity, validating tests, finding gaps.
  Triggers: "verify sdd", "check integrity", "verify links", "verify tests", "@verifies"
---

# SDD Verification

> `docs/sdd-guidelines.md` §3: "Integrity = Traceability + Testing"

## Two Dimensions

| Dimension | Question | Method | Reference |
|-----------|----------|--------|-----------|
| **Traceability** | Why does this exist? | Link verification | [traceability.md](reference/traceability.md) |
| **Testing** | Does this work? | Execution verification | [testing.md](reference/testing.md) |

Both required. Traceability alone confirms links exist; Testing confirms code works.

## Quick Reference

### Link Types

| Link | From → To | Required |
|------|-----------|----------|
| `@aligns-to` | REQ → Foundation anchor | **Yes** |
| `@derives` | Design → REQ | **Yes** |
| `@verifies` | Behavioral Test → REQ | **Yes** |
| `@rationale` | Any → Decision/reasoning | If non-obvious |
| `@assumes` | Any → Assumption | When applicable |
| `@invalidated-by` | Assumption → Condition | When applicable |
| `@supersedes` | Decision → Prior Decision | When replacing |

### Test Types

| Type | Links To | Level | Directory |
|------|----------|-------|-----------|
| Behavioral | REQ (`@verifies`) | E2E/Integration | `tests/requirements/` |
| Structural | Design (convention) | Unit | `tests/unit/` |

## Instructions

### Full Verification

Run both dimensions:

```
1. Traceability Check
   └── Alignment (Foundation ↔ Requirements)
   └── Derivation (Requirements ↔ Design)
   └── Consistency

2. Test Check
   └── @verifies coverage
   └── Abstraction matching
   └── Test execution status
```

### Partial Verification

| Trigger | Run |
|---------|-----|
| "verify links" | Traceability only |
| "verify tests" | Testing only |
| "verify REQ-001" | Both, scoped to item |

### Verification Triggers

| Point | What to Verify |
|-------|----------------|
| Foundation complete | Human judgment (identity) |
| Requirements complete | Alignment |
| Design complete | Derivation |
| Pre-implementation | Full traceability + behavioral test coverage |
| Post-change | Affected items + downstream |

## Results Handling

### Pass

```yaml
# Update item status
items:
  REQ-001:
    status: verified
    verified_at: 2025-01-17T10:00:00Z
```

### Fail — Self-Resolvable

| Failure | Action |
|---------|--------|
| Missing `@derives` | Add link |
| Missing `@aligns-to` | Add link |
| Missing `@verifies` | Create test |
| Terminology mismatch | Standardize |

After fix: re-verify → mark `verified`.

### Fail — Escalate

| Situation | Why |
|-----------|-----|
| Foundation-level conflict | Identity-defining |
| Conflicting interpretations | Authority needed |
| Security/compliance/legal | Risk implications |
| Resource or cost commitments | Authority required |
| User intent ambiguity | Guessing is dangerous |
| Missing artifact (not link) | Scope decision |
| Test reveals requirement gap | REQ may need update |

```yaml
escalations:
  - id: ESC-001
    type: interpretation
    description: "REQ-003 and REQ-005 conflict"
    items_affected: [REQ-003, REQ-005]
    status: pending
```

## Gap Documentation

```yaml
gaps:
  - id: GAP-001
    severity: critical | major | minor
    type: missing_requirement | missing_design | missing_rationale | missing_test | broken_link | contradiction
    location: spec/requirements.md#REQ-003
    description: "No behavioral test for REQ-003"
    blocking: [implementation]
    owner: unassigned
```

| Severity | Definition | Response |
|----------|------------|----------|
| critical | Blocks implementation | Stop, resolve now |
| major | Blocks verification | Resolve before checkpoint |
| minor | Cosmetic | Track, defer |

## Scope Direction

```
Foundation → Requirements → Design → Implementation
   (Why)        (What)       (How)     (Code)
```

| Change Location | Verify |
|-----------------|--------|
| Upstream (Foundation, REQ) | All downstream |
| Downstream (Design, Impl) | Upstream unaffected if behavioral tests pass |

## State Update

After verification:

```yaml
# .sdd/state.yaml
documents:
  requirements:
    status: verified
    items:
      REQ-001: { status: verified, test: passing }
      REQ-002: { status: verified, test: passing }
      REQ-003: { status: draft, test: missing }

verification:
  traceability:
    alignment: passed
    derivation: passed
  tests:
    requirements:
      REQ-001: passing
      REQ-002: passing
      REQ-003: missing
    design:
      data_model: passing
```

## Checklist

- [ ] All anchors have ≥1 REQ (`@aligns-to` coverage)
- [ ] All design items have `@derives`
- [ ] All REQs have behavioral tests (`@verifies`)
- [ ] Non-obvious choices have `@rationale`
- [ ] Tests match abstraction level
- [ ] Gaps documented with severity/owner
- [ ] State file updated

## References

- [reference/traceability.md](reference/traceability.md) — Link verification details
- [reference/testing.md](reference/testing.md) — Test verification details
- `docs/sdd-guidelines.md` §3 for full specification
