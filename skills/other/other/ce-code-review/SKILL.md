---
name: ce-code-review
description: >
  Review code changes for CE coding standards, ADR conformance, and behavior or API
  regression risk.
---

# CE Code Review

You are reviewing code for conformance with calibrated_explanations standards.
Work through each review dimension below and produce a finding per violation.

Load `references/review_dimensions.md` for full dimension details with code examples.

---

## Review dimensions (summary)

1. **Module boundary (ADR-001)** — CRITICAL: `core/` must never import `plugins/` internals.
2. **Lazy imports** — CRITICAL: `matplotlib`, `pandas`, `joblib` must be function-scoped.
3. **Future annotations** — REQUIRED: every `.py` file starts with `from __future__ import annotations`.
4. **Docstrings (Numpy style)** — REQUIRED: `Parameters` -> `Returns` -> `Raises` -> `Notes` -> `Examples`.
5. **Exception handling (ADR-002)** — REQUIRED: use CE exception hierarchy, not bare `ValueError`.
6. **Fallback visibility** — CRITICAL: every fallback needs `_LOGGER.info()` + `warnings.warn(UserWarning)`.
7. **Type hints** — REQUIRED: avoid `Any` without documented reason; prefix private with `_`.
8. **Deprecation (ADR-011)** — REQUIRED: use `deprecate()` helper; 2 minor releases before removal.
9. **CE-First compliance** — public methods return calibrated types; assert fitted + calibrated.

---

## Quick-check command

```bash
make local-checks-pr               # fast required checks
make local-checks                  # full checks (only needed for main-branch gates)
pre-commit run --all-files         # linting, ruff, mypy subset
```

---

## Review Report Template

```
CE Code Review: <module/PR name>
=================================
ADR-001 module boundary:    PASS / FAIL
  violations: <list file:line>

Lazy imports:               PASS / FAIL
  eager heavy imports:      <list>

Future annotations:         PASS / FAIL
  missing in:               <list>

Docstrings (numpy style):   PASS / FAIL
  missing sections in:      <list fn:section>

Exception handling:         PASS / FAIL
  bare exceptions at:       <list>

Fallback visibility:        PASS / FAIL
  missing warn()/log() at:  <list>

Type hints:                 PASS / FAIL
  untyped parameters:       <list>

Deprecation (ADR-011):      PASS / FAIL / N_A

CE-First compliance:        PASS / FAIL

Overall: CONFORMANT / NON-CONFORMANT (<N> issues)
```

## Evaluation Checklist

- [ ] All 9 dimensions checked.
- [ ] ADR-001 boundary violations are blocking (must fix before merge).
- [ ] Fallback visibility violations are blocking.
- [ ] Lazy-import violations are blocking.
- [ ] Report produced with file:line references for each issue.
