---
name: audit-validation-wrapper
description:
  Validation wrapper that tests TDMS and Documentation Standards integration
  during comprehensive audit
---

# Audit Validation Wrapper

**Version:** 1.0 **Purpose:** Validate TDMS and Documentation Standards
integration during comprehensive audit execution

**What This Does:** Wraps the `audit-comprehensive` skill with validation
checkpoints at each stage to ensure:

- JSONL outputs comply with `JSONL_SCHEMA_STANDARD.md`
- S0/S1 findings have required `verification_steps`
- TDMS field mapping will work correctly
- Intake deduplication functions properly

---

## Overview

```
audit-validation-wrapper (this skill)
    │
    ├── Stage 0: Pre-Audit
    │   └── Capture MASTER_DEBT.jsonl baseline
    │
    └── audit-comprehensive (orchestrator)
            │
            ├── Stage 1 (4 domain audits in parallel)
            │   ├── audit-code
            │   ├── audit-security
            │   ├── audit-performance
            │   └── audit-refactoring
            │   └── [VALIDATE domain JSONL outputs]
            │
            ├── Stage 2 (3 domain audits in parallel)
            │   ├── audit-documentation
            │   ├── audit-process
            │   └── audit-engineering-productivity
            │   └── [VALIDATE domain JSONL outputs]
            │
            └── Stage 3 (sequential)
                └── audit-aggregator
                └── [VALIDATE + TDMS intake dry-run]
    │
    └── Post-Audit
        ├── Compare MASTER_DEBT.jsonl before/after
        └── Generate VALIDATION_REPORT.md
```

---

## Execution Flow

### Stage 0: Pre-Audit Baseline (MANDATORY)

**Before running any audits:**

```bash
node scripts/audit/validate-audit-integration.js capture-baseline
```

This captures:

- MASTER_DEBT.jsonl item count
- Last DEBT-XXXX ID assigned
- File content hash (SHA256)
- Severity distribution

**Verify baseline captured:**

```bash
cat docs/audits/comprehensive/validation-state.json | grep -A5 '"baseline"'
```

**Failure Handling:**

- If MASTER_DEBT.jsonl unreadable → ABORT entire audit
- If file doesn't exist → OK (will be created during intake)

---

### Stage 1: Technical Core Audits

**Run Stage 1 of audit-comprehensive as normal, then validate:**

```bash
node scripts/audit/validate-audit-integration.js validate-stage 1
```

**What gets validated:**

| File                             | Checks                                      |
| -------------------------------- | ------------------------------------------- |
| audit-code-findings.jsonl        | Schema compliance, S0/S1 verification_steps |
| audit-security-findings.jsonl    | Schema compliance, S0/S1 verification_steps |
| audit-performance-findings.jsonl | Schema compliance, TDMS field mapping       |
| audit-refactoring-findings.jsonl | Schema compliance, unique fingerprints      |

**Exit Codes:**

- `0` = All validations passed, continue to Stage 2
- `1` = Blocking S0/S1 issues found, MUST fix before proceeding

**If Stage 1 validation fails:**

1. Review blocking issues in console output
2. Fix S0/S1 findings in the domain audit
3. Re-run failed domain audit
4. Re-run `validate-stage 1`

---

### Stage 2: Supporting Audits

**Run Stage 2 of audit-comprehensive as normal, then validate:**

```bash
node scripts/audit/validate-audit-integration.js validate-stage 2
```

**What gets validated:**

| File                               | Checks                                      |
| ---------------------------------- | ------------------------------------------- |
| audit-documentation-findings.jsonl | Schema compliance, unique fingerprints      |
| audit-process-findings.jsonl       | Schema compliance, S0/S1 verification_steps |

**Same failure handling as Stage 1.**

---

### Stage 3: Aggregation

**Run Stage 3 of audit-comprehensive (aggregator), then validate:**

```bash
node scripts/audit/validate-audit-integration.js validate-stage 3
```

**What gets validated:**

| File                      | Checks                                          |
| ------------------------- | ----------------------------------------------- |
| aggregated-findings.jsonl | Deduplication worked, no duplicate fingerprints |

**Then validate TDMS intake will work:**

```bash
node scripts/audit/validate-audit-integration.js validate-tdms-intake docs/audits/comprehensive/aggregated-findings.jsonl
```

**This runs `intake-audit.js --dry-run` and validates:**

- Script runs without errors
- Field mapping (fingerprint→source_id, etc.) works
- Reports how many items will be added vs duplicates skipped

**If intake dry-run fails:**

1. Check intake-audit.js exists
2. Check JSONL file has valid content
3. Review mapping errors in console output
4. Fix JSONL issues in aggregator output

---

### Post-Audit: Compare and Report

**After actual TDMS intake runs:**

```bash
# Compare to baseline
node scripts/audit/validate-audit-integration.js compare-baseline

# Generate final report
node scripts/audit/validate-audit-integration.js generate-report
```

**Report location:** `docs/audits/comprehensive/VALIDATION_REPORT.md`

**Report contents:**

- Pre-audit baseline metrics
- Stage-by-stage validation results
- TDMS intake validation (dry-run + actual)
- Field mapping verification
- Overall status: PASS/FAIL with details

---

## Integration with audit-comprehensive

This skill **wraps** audit-comprehensive by adding validation checkpoints. The
recommended workflow:

### Option A: Manual Integration

Run audit-comprehensive stages manually with validation after each:

```
1. /audit-validation-wrapper capture-baseline
2. Run Stage 1 of /audit-comprehensive
3. /audit-validation-wrapper validate-stage 1
4. Run Stage 2 of /audit-comprehensive
5. /audit-validation-wrapper validate-stage 2
6. Run Stage 3 of /audit-comprehensive
7. /audit-validation-wrapper validate-stage 3
8. /audit-validation-wrapper validate-tdms-intake
9. Run actual TDMS intake
10. /audit-validation-wrapper compare-baseline
11. /audit-validation-wrapper generate-report
```

### Option B: Automated Wrapper (Recommended)

Use this skill as the entry point. It will:

1. Capture baseline automatically
2. Invoke audit-comprehensive
3. Run validation after each stage checkpoint
4. Block on S0/S1 verification failures
5. Generate final validation report

**Usage:**

```
User: /audit-validation-wrapper

Claude: Starting validated comprehensive audit...

[Stage 0: Capturing baseline]
✓ MASTER_DEBT.jsonl: 868 items, DEBT-0884 last ID

[Invoking /audit-comprehensive]
...audit-comprehensive runs with standard flow...

[Stage 1 Checkpoint - Validating]
✓ audit-code-findings.jsonl: 45 findings, 0 blocking
✓ audit-security-findings.jsonl: 12 findings, 0 blocking
...

[Stage 2 Checkpoint - Validating]
...

[Stage 3 Checkpoint - Validating]
✓ aggregated-findings.jsonl: 97 unique findings
✓ TDMS intake dry-run: 89 new, 8 duplicates

[Post-Audit Validation]
✓ MASTER_DEBT.jsonl: +89 items (DEBT-0885 to DEBT-0973)
✓ Field mapping verified

📄 Validation Report: docs/audits/comprehensive/VALIDATION_REPORT.md
```

---

## Failure Handling Matrix

| Checkpoint | Failure                          | Action               |
| ---------- | -------------------------------- | -------------------- |
| Pre-Audit  | MASTER_DEBT.jsonl unreadable     | ABORT                |
| Stage 1-2  | Missing JSONL output             | WARN, continue       |
| Stage 1-2  | S0/S1 without verification_steps | BLOCK until fixed    |
| Stage 1-2  | Schema validation errors         | WARN, log to report  |
| Stage 3    | Aggregator fails                 | WARN, individual OK  |
| Stage 3    | Duplicate fingerprints           | INFO (expected)      |
| Post-Audit | Intake dry-run fails             | BLOCK actual intake  |
| Post-Audit | Content hash collision           | INFO (dedup working) |

---

## Validation Script Commands

The validation script provides these commands:

```bash
node scripts/audit/validate-audit-integration.js <command>

Commands:
  capture-baseline              Capture MASTER_DEBT.jsonl state
  validate-jsonl <file>         Validate single JSONL file
  validate-stage <1|2|3>        Validate all outputs for a stage
  validate-tdms-intake <file>   Test intake with --dry-run
  compare-baseline              Compare current vs baseline
  generate-report               Generate VALIDATION_REPORT.md
  help                          Show usage
```

---

## Documentation References

- [JSONL_SCHEMA_STANDARD.md](docs/templates/JSONL_SCHEMA_STANDARD.md) - Schema
  requirements
- [intake-audit.js](scripts/debt/intake-audit.js) - TDMS intake script
- [audit-comprehensive](../.claude/skills/audit-comprehensive/SKILL.md) - Main
  audit orchestrator
- [validate-audit.js](scripts/validate-audit.js) - Existing S0/S1 validation

---

## Related Skills

- `/audit-comprehensive` - The main audit orchestrator this wraps
- `/audit-code`, `/audit-security`, etc. - Individual domain audits
- `/verify-technical-debt` - Manual debt verification workflow

---

## Version History

| Version | Date       | Description                                |
| ------- | ---------- | ------------------------------------------ |
| 1.0     | 2026-02-03 | Initial version for TDMS/DocStd validation |
