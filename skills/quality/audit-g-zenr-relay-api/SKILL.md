---
name: audit
description: Full codebase audit — dead code, layer violations, concurrency, observability, code quality
---

Run a comprehensive codebase audit across 7 dimensions. Report findings by severity.

## 1. Layer Boundary Audit
Check dependency flow is never reversed (see Layers in project config):
- Scan imports in core layer — must NOT import from API or service layers
- Scan imports in service layer — must NOT import from API layer
- Scan imports in API layer — should only import from service, models, and core exceptions
- Check for circular imports between any modules

## 2. Dead Code Audit
- Find unused imports in every source file under the source root
- Find functions/methods with zero callers (search codebase for each public function name)
- Find commented-out code blocks (> 3 consecutive commented lines)
- Find unused variables (assigned but never read)
- Check `__init__.py` files for stale exports

## 3. Concurrency Audit
- Verify ALL external resource access in the service class is inside the lock mechanism
- Check middleware for thread-safe counter access
- Verify no shared mutable state between request handlers
- Check for potential deadlocks (nested lock acquisition)

## 4. Observability Audit
- Verify ALL state-changing service methods produce audit log entries
- Verify startup/shutdown events are logged with appropriate levels
- Verify error paths log before raising (not silently propagating)
- Check log format consistency
- Verify no `print()` statements in source root

## 5. Code Quality Audit
- Check for DRY violations (duplicated logic across files)
- Check for overly long functions (> 50 lines)
- Check for deeply nested conditionals (> 3 levels)
- Check for magic numbers/strings (should be constants or config)
- Verify all functions have return type annotations
- Verify future annotations pattern is followed (see stack concepts in project config)

## 6. API Contract Audit
- Verify every endpoint has `response_model` (no raw dict returns)
- Verify every endpoint has `summary` and `description`
- Verify every endpoint declares `responses` with status codes
- Verify the error response model is used consistently for all error responses
- Verify static routes before parameterized routes in each router
- Check for missing HTTP status codes in responses dict

## 7. Test Coverage Audit
- For each endpoint in the API layer, verify tests exist for:
  - Success path (2xx)
  - Validation error (422)
  - Service/device error (503)
- For each service method, verify tests exist for:
  - Happy path
  - Error/exception path
  - Audit log output (if state-changing)
- Check for assertion quality (not just status code, verify response body)
- Check for proper fixture cleanup (dependency overrides cleared)

## Output Format

```
AUDIT RESULTS
═════════════

1. Layer Boundaries:    PASS / X violations
2. Dead Code:           PASS / X items found
3. Concurrency:         PASS / X issues
4. Observability:       PASS / X gaps
5. Code Quality:        PASS / X issues
6. API Contracts:       PASS / X gaps
7. Test Coverage:       PASS / X missing tests

FINDINGS BY SEVERITY:
  Critical: X
  High:     X
  Medium:   X
  Low:      X
```

List each finding with file:line reference and specific remediation.