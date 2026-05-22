---
name: agent-ops-api-review
description: "Platform/Language agnostic API delivery and correctness auditor. Use when project contains API endpoints to verify contract alignment, endpoint behavior, and test coverage."
category: analysis
invokes: [agent-ops-state, agent-ops-tasks]
invoked_by: [agent-ops-critical-review, agent-ops-validation]
state_files:
  read: [constitution.md, baseline.md, focus.md, issues/*.md]
  write: [focus.md, issues/*.md]
---

# Skill: agent-ops-api-review

> Platform/Language agnostic API delivery and correctness auditor

---

## Purpose

Perform a **critical, thorough, evidence-based audit** of an API implementation and its endpoints. Verify that the API:
- Produces the **expected outcomes**
- Behaves correctly across success and failure paths
- Matches its **OpenAPI/Swagger contract**
- Has **adequate tests** to prove required behavior

**No credit without evidence.** Spec is not proof. Tests are not proof unless they assert required outcomes.

---

## Triggers

- Project contains API endpoints (REST, GraphQL, gRPC)
- OpenAPI/Swagger spec exists
- User requests API review
- `agent-ops-critical-review` detects API patterns

---

## Inputs

You will be given some or all of:
- Repository / codebase / diff
- OpenAPI/Swagger spec (file or generated)
- Unit test suite
- Optional: CI logs, runtime logs, sample requests/responses

If the OpenAPI spec is not available, identify where it should exist and treat missing spec as a finding.

---

## Non-Negotiable Rules

- **No credit without evidence**
- **Spec is not proof** — implementation must match it
- **Tests are not proof** unless they assert required outcomes and would fail on regression
- Every claim must cite **concrete locations** (files/endpoints/tests/spec paths)

---

## Mandatory Audit Outputs

### 1. Endpoint Inventory

List all endpoints, grouped by resource/domain:
- Method + route + auth requirement
- Request/response shape references (OpenAPI path refs if available)

### 2. Contract Alignment Matrix

For each endpoint:

| Endpoint | Spec Ref | Impl Ref | Tests Ref | Status |
|----------|----------|----------|-----------|--------|
| GET /users | paths./users.get | user_router.py:45 | test_users.py:12 | aligned |
| POST /users | paths./users.post | user_router.py:78 | — | untested |

Status values: `aligned | partially_aligned | misaligned | unverifiable`

### 3. Findings

Each finding must include:
- **Severity**: `must_fix | strongly_recommended | discuss`
- **Category**: Which audit axis (A1-A10)
- **Endpoint(s) affected**
- **File references**
- **Evidence**
- **Actionable recommendation**

### 4. Test Gap Assessment

- What is proven by unit tests
- What cannot be proven without integration tests
- Minimum required integration tests to establish confidence

### 5. Verdict

- **PASS**: No `must_fix` and no `misaligned` endpoints
- **FAIL**: Any `must_fix` or `misaligned` endpoint

---

## Mandatory Audit Axes

Explicitly evaluate each axis. If not applicable, say why.

### A1: OpenAPI Contract Correctness & Drift

- Does the OpenAPI spec reflect actual API behavior?
- Are operationIds stable and meaningful?
- Are schemas precise (required fields, formats, nullability)?
- Are error responses specified and accurate?
- Are examples present and representative?

**Flag**: spec drift, underspecified schemas, missing error models

### A2: Endpoint Behavior & Outcome Verification

For each endpoint:
- Does it produce the expected **domain outcome**, not just a response?
- Are side effects correct (create/update/delete/idempotency)?
- Are status codes correct and consistent?
- Are edge cases handled (empty, invalid, not found, conflict)?

**Flag**: wrong status codes, incorrect behavior, missing edge cases

### A3: Request Validation & Error Semantics

- Is input validation explicit and consistent?
- Are validation errors structured and stable (machine-readable)?
- Are error codes/messages consistent across endpoints?
- Clear distinction between 4xx (client) vs 5xx (server) vs 409 (conflict)?
- Are errors ever swallowed or turned into "200 with error payload"?

**Flag**: inconsistent error shapes, silent failures, leaking internal details

### A4: Authentication, Authorization, and Tenant Boundaries

- Are endpoints protected appropriately?
- Are authorization rules enforced server-side?
- Are tenant boundaries enforced (if multi-tenant)?
- Is identity propagated and validated correctly?

**Flag**: auth bypass risk, missing authorization checks, privilege escalation

### A5: Pagination, Filtering, Sorting, and Field Selection (HIGH SCRUTINY)

#### Field Selection / Sparse Fieldsets
- Is it specified in OpenAPI?
- Does implementation whitelist fields (no arbitrary property exposure)?
- Are invalid field selections rejected with clear errors?

#### Filtering & Sorting
- Are filters validated and whitelisted?
- Is filter syntax consistent?
- Are unknown filters rejected (not ignored)?

#### Pagination
- Cursor vs offset semantics clear?
- Limits enforced?
- Deterministic ordering guaranteed?

**Flag**: field selection leaking sensitive data, injection risks, unstable paging

### A6: Idempotency, Concurrency, and Caching

- Are PUT/PATCH/POST idempotency rules clear and honored?
- Are idempotency keys supported where required?
- Are concurrency controls present (ETag/If-Match) if needed?
- Are cache headers correct?

**Flag**: duplicate side effects on retries, lost updates

### A7: Resource Modeling & API Evolution

- Consistent resource naming and hierarchy?
- Versioning strategy (URL/header/content negotiation)?
- Backward compatibility expectations?
- Deprecation policy?

**Flag**: breaking changes without version bump, inconsistent modeling

### A8: Content Negotiation, Media Types, and Serialization

- Are content types explicit and correct?
- Are nullability and optional fields stable?
- Are time/date formats consistent and documented?
- Are enums stable?

**Flag**: ambiguous serialization, inconsistent date formats

### A9: Observability, Correlation, and Operability

- Request IDs / correlation IDs present?
- Structured logging around failures?
- Metrics around key endpoints?
- Rate limiting (if required)?
- Are sensitive values excluded from logs?

**Flag**: inability to debug production issues, sensitive leakage

### A10: Testing Strategy (Unit vs Integration vs Contract)

**Unit tests prove**:
- Handler logic (pure outcomes)
- Validation logic
- Error mapping

**Integration tests required when**:
- Behavior depends on routing/middleware/auth pipeline
- Serialization/deserialization matters
- DB/transaction boundaries matter
- OpenAPI contract needs proof

**Contract tests required when**:
- Clients depend on OpenAPI schema stability
- Multiple services integrate

**Flag**: tests only assert status codes, mocking away critical pipeline behavior

---

## Severity Rules

### must_fix
- Misaligned OpenAPI vs implementation for public endpoints
- Incorrect status codes or error semantics
- Auth/tenant boundary weakness
- Field selection/filtering security risks
- Untested critical behavior

### strongly_recommended
- Partial contract coverage
- Missing integration tests for pipeline-dependent behavior
- Inconsistent patterns causing client breakage risk

### discuss
- Spec ambiguity
- Alternative evolution strategies

---

## Output Format

```markdown
# API Audit Report

## Scope
What was reviewed (repo/diff/spec/tests).

## Endpoint Inventory
### Resource: Users
- GET /users (paths./users.get → user_router.py:45)
- POST /users (paths./users.post → user_router.py:78)

## Contract Alignment Matrix
| Endpoint | Spec Ref | Impl Ref | Tests Ref | Status |
|----------|----------|----------|-----------|--------|

## Findings

### Must Fix
- **[F001] Missing auth check on DELETE /users/{id}**
  - Endpoint: DELETE /users/{id}
  - Evidence: user_router.py:120 has no @require_auth decorator
  - Impact: Any user can delete any other user
  - Recommendation: Add authorization check

### Strongly Recommended
...

### Discuss
...

## Test Gap Assessment
- **Proven by unit tests**: Validation logic, error mapping
- **Requires integration tests**: Auth pipeline, OpenAPI contract
- **Minimum integration test set**: [list]

## Verdict
PASS | FAIL
```

---

## Forbidden Behaviors

- ❌ Generic "best practices" lists
- ❌ Speculative scalability advice
- ❌ "Looks fine" without evidence
- ❌ Accepting OpenAPI or tests as proof without alignment verification

---

## End Condition

Every endpoint accounted for with:
- Spec alignment status
- Implementation evidence
- Test evidence
- Explicit gaps and required tests
