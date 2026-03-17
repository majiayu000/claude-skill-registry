---
name: quality-gate
description: Pre-merge quality gate — chains verify, review, and security audit into a pass/fail verdict
disable-model-invocation: true
---

Run the full quality gate before merging. This orchestrates multiple checks into a single pass/fail verdict.

## Gate 1 — Verification (automated)
Run the test and type-check commands (see project config).
- **PASS**: All tests green, zero type errors
- **FAIL**: Any test failure or type error → stop here, fix first

## Gate 2 — Code Quality Audit
Check the codebase for structural issues:

### Layer Violations
- Search for imports that violate the dependency flow (see Layers in project config)
- No lower layer importing from a higher layer

### Dead Code
- Search for unused imports across the source root
- Search for functions/methods with zero callers
- Check for commented-out code blocks (remove or restore)

### Concurrency
- Verify all external resource access is wrapped in the lock mechanism in the service class
- Verify no race conditions in middleware state

### Observability
- Verify all state changes produce audit log entries
- Verify startup/shutdown events are logged
- Verify structured log format is consistent

## Gate 3 — Security Review
Quick security pass:
- [ ] `hmac.compare_digest()` used for all secret comparisons
- [ ] No secrets in error responses (grep for stack trace patterns)
- [ ] No secrets logged at any level
- [ ] Auth enforced on all state-changing endpoints when API key is configured
- [ ] Input validation via Pydantic on all endpoints
- [ ] Rate limiting functional when configured

## Gate 4 — Documentation Currency
- [ ] Project documentation API table matches actual routes
- [ ] Env example file matches all Settings fields
- [ ] OpenAPI metadata present on every endpoint
- [ ] `from __future__ import annotations` in every source file

## Verdict

```
Gate 1 (Verify):    PASS / FAIL
Gate 2 (Quality):   PASS / FAIL (list violations)
Gate 3 (Security):  PASS / FAIL (list findings)
Gate 4 (Docs):      PASS / FAIL (list gaps)
─────────────────────────────────
OVERALL:            PASS / FAIL
```

**PASS** = Safe to merge. All gates green.
**FAIL** = List every failing item with file:line and remediation. Do not merge.