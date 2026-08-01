---
name: code-consistency-validator
description: 'Validates type consistency across Rust, TypeScript, PostgreSQL boundaries.
  Use when reviewing code, debugging type mismatches, or validating API contracts.
  Triggers on: check consistency, validate typ'
---

---
name: code-consistency-validator
description: Validates type consistency across Rust, TypeScript, PostgreSQL boundaries. Use when reviewing code, debugging type mismatches, or validating API contracts. Triggers on: check consistency, validate types, find mismatches, cross-language.
---

# Code Consistency Validator

Validates type consistency across Rust, TypeScript, and PostgreSQL boundaries.

## When to Use

- Reviewing code for type mismatches
- Debugging precision loss issues
- Validating API contracts between languages
- Checking BigInt/Number conversions
- Auditing cross-language data flow

## Workflow

### Step 1: Run Quick Grep

Use provided grep commands to find potential issues.

### Step 2: Check Critical Patterns

Look for Number() on wei/balance, parseInt without radix.

### Step 3: Generate Report

Report findings using severity levels (CRITICAL/WARNING/INFO).

---

## Critical Type Mappings

| Rust | TypeScript | PostgreSQL |
|------|------------|------------|
| i64/u64 | bigint (not number!) | BIGINT |
| U256 | string | DECIMAL(36,18) |
| f64 | number | DOUBLE PRECISION |

## 🔴 CRITICAL Patterns
```typescript
Number(response.profit_wei)  // ❌ Precision loss!
parseInt(hexBalance)         // ❌ Missing radix!
JSON.stringify({ amount: BigInt(x) })  // ❌ Fails!
```

## Quick Grep
```bash
grep -rn "Number(" --include="*.ts" | grep -E "(wei|balance|amount)"
grep -rn "parseInt(" --include="*.ts" | grep -v ", 10)" | grep -v ", 16)"
```

## Report Format

🔴 CRITICAL (funds at risk)
🟠 WARNING (potential bugs)
🟡 INFO (style)
✅ VALIDATED
