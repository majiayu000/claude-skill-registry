---
name: traceability-audit
description: Verifies that every PRD requirement has a linked Test Case and Code Implementation.
role: prod-pm
triggers:
  - trace requirements
  - audit scope
  - req coverage
  - missing tests
  - traceability matrix
---

# traceability-audit Skill

This skill ensures "What was ordered" == "What was delivered".

## 1. The Trace Chain
`PRD (Req ID)` -> `Design (Mock ID)` -> `Task (T-ID)` -> `Commit (Hash)` -> `Test Case (Test ID)`

## 2. Methodology
1.  **Extract Requirements**: Parse `PRD.md` for `req-001`, `req-002`.
2.  **Search Tests**: `grep` test files for `@req(req-001)`.
3.  **Identify Gaps**:
    - Req exists, Test missing -> **Gap**.
    - Req missing, Test exists -> **Gold Plating** (Unrequested feature).

## 3. Coverage Analysis
- **Code Coverage**: Lines of code executed (e.g., 96%).
- **Requirement Coverage**: % of Requirements with at least 1 passing test (Target: 100%).

## 4. The Matrix
Generate a table:
| Req ID | Description | File Reff | Test Ref | Status |
|---|---|---|---|---|
| R-101 | "User logs in" | `auth.ts` | `auth.test.ts` | ✅ PASS |
| R-102 | "User logs out" | `auth.ts` | `auth.test.ts` | ❌ FAIL |
