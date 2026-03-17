---
name: interlock-ops
description: Operational rules for Interlock enforcement and receipts
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(./scripts/claude/*)
---

# Interlock Operations Skill

This skill governs operational behavior for Interlock enforcement.

## Core Rules

### 1. Never Publish Enforcement Heuristics

Enforcement logic is internal. Never commit or document:

- Threshold values for enforcement decisions
- Specific trigger conditions
- Bypass mechanisms or exceptions
- Internal scoring algorithms

**Reason**: Publishing enforcement heuristics enables gaming.

### 2. Every Enforcement Action Must Emit a Receipt

No silent enforcement. Every action must produce:

```json
{
  "action": "refusal|degradation|allowance",
  "timestamp": "2026-01-10T12:00:00Z",
  "reason": "quality_floor_breach",
  "incident_id": "int-123456",
  "confidence": 0.45,
  "threshold": 0.80
}
```

### 3. Receipt Format Changes Require Validation

Before changing receipt schema:

1. Update the schema definition
2. Create positive test fixture
3. Create negative test fixture
4. Run `./scripts/claude/receipt_audit.sh`
5. Verify both positive and negative tests pass

### 4. Any Failure = Degrade/Refuse

Never allow silent passes:

| Scenario | Action |
|----------|--------|
| Validator unavailable | REFUSE |
| Schema mismatch | REFUSE |
| Confidence unknown | REFUSE |
| Timeout | DEGRADE |
| Partial data | DEGRADE |

## Receipt Lifecycle

```
1. EMIT    → Receipt generated at decision point
2. SIGN    → Cryptographic signature applied
3. STORE   → Written to forensic log
4. VERIFY  → Schema validation on read
5. AUDIT   → Periodic integrity check
```

## Validation Commands

```bash
# Full receipt audit with negative tests
./scripts/claude/receipt_audit.sh

# Public safety check (no secrets in receipts)
./scripts/claude/public_safety_check.sh
```

## Schema Files

| File | Purpose |
|------|---------|
| `schemas/interlock_event.schema.json` | Event schema definition |
| `schemas/golden_fixture.jsonl` | Known-good test fixtures |
| `receipts/examples/operatorpack_example_pass.json` | Valid receipt |
| `receipts/examples/operatorpack_example_fail.json` | Invalid receipt (for negative test) |

## Prohibited Actions

- Publishing enforcement thresholds
- Silent passes on validation failures
- Modifying receipts after signing
- Skipping negative tests
- Committing real receipts to public repo
