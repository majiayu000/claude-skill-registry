---
name: audit
description: Comprehensive module audit — code quality, tests, security, edge cases, and recommendations
disable-model-invocation: true
argument-hint: <module name> (e.g., "attendance", "MemberService", "donations", "visitors")
---

# Module Audit: $ARGUMENTS

Perform a deep, structured audit of the specified module. Identify the relevant controller(s), service(s), repository(ies), DTOs, entities, and tests. Then execute each phase below.

## Phase 0: Module Discovery

Identify ALL files belonging to this module:

1. **Controller(s)**: `src/main/java/.../controllers/*` matching the module name
2. **Service(s)**: `src/main/java/.../services/*` matching the module name
3. **Repository(ies)**: `src/main/java/.../repositories/*` matching the module name
4. **Entity/Model(s)**: `src/main/java/.../models/*` matching the module name
5. **DTO(s)**: `src/main/java/.../dtos/*` matching the module name
6. **Mapper(s)**: `src/main/java/.../mappers/*` matching the module name
7. **Tests**: `src/test/java/.../*` matching the module name
8. **Frontend component(s)**: `/home/reuben/Documents/workspace/past-care-spring-frontend/src/app/**/*` matching the module name

List every file found. If the module name is ambiguous (e.g., "member" could mean Member, MemberDashboard, MemberStatusChange), list all matches and audit the primary one unless the user specified otherwise.

---

## Phase 1: Code Completeness & API Surface

### 1.1 Endpoint Inventory
For each controller, list every endpoint:

| Method | Path | Permission | Roles with Access | Description |
|--------|------|------------|-------------------|-------------|
| GET | /api/... | ENTITY_VIEW_ALL | ADMIN, PASTOR, ... | ... |

### 1.2 CRUD Coverage
Check if the module has complete CRUD operations where applicable:
- [ ] **Create** — POST endpoint exists
- [ ] **Read (single)** — GET by ID endpoint exists
- [ ] **Read (list)** — GET all/paginated endpoint exists
- [ ] **Update** — PUT/PATCH endpoint exists
- [ ] **Delete** — DELETE endpoint exists
- [ ] **Search/Filter** — Query parameters or search endpoint exists
- [ ] **Export** — Export endpoint exists (if applicable for this entity)

Flag any missing operations that would reasonably be expected.

### 1.3 DTO Validation
- [ ] Request DTOs have Jakarta validation annotations (`@NotNull`, `@Size`, `@Email`, etc.)
- [ ] Response DTOs don't expose sensitive fields (passwords, tokens, internal IDs where inappropriate)
- [ ] Field-level error messages are descriptive

### 1.4 Service Layer Completeness
- [ ] All controller endpoints have corresponding service methods
- [ ] Business logic lives in services, not controllers
- [ ] No raw repository calls from controllers

---

## Phase 2: Test Audit

### 2.1 Test Inventory
List all existing tests for this module:

| Test Class | Type | Methods | What It Tests |
|-----------|------|---------|---------------|
| ...Test | Integration | 5 | CRUD operations |

### 2.2 Role Coverage Matrix
For EACH endpoint, check which roles are tested:

| Endpoint | SUPERADMIN | ADMIN | PASTOR | TREASURER | MEMBER_MANAGER | FELLOWSHIP_LEADER | MEMBER |
|----------|------------|-------|--------|-----------|----------------|-------------------|--------|
| GET /api/... | ? | ? | ? | ? | ? | ? | ? |

Mark: ✅ tested (positive), ❌ tested (negative/forbidden), ⬜ NOT TESTED

**Per CLAUDE.md Rule #4**: Every test MUST test ALL 7 user roles with both positive and negative assertions.

### 2.3 Test Quality Assessment
- [ ] Tests use proper Given/When/Then structure
- [ ] Tests verify response body content, not just status codes
- [ ] Error scenarios are tested (not found, invalid input, duplicate)
- [ ] Boundary conditions tested (empty lists, max values, null fields)
- [ ] Tests are independent (no shared mutable state between tests)

### 2.4 Test Gap Analysis
List specific tests that should exist but don't:
1. Missing role coverage (from matrix above)
2. Missing error/edge case scenarios
3. Missing tenant isolation tests
4. Missing E2E/Playwright tests

**Calculate completion rate**: `(tested scenarios / total expected scenarios) × 100%`

---

## Phase 3: Security Audit

### 3.1 Tenant Isolation (CRITICAL)
For each service method that accesses tenant-scoped data:

| Method | Entity | @Transactional? | Isolation Method | Secure? |
|--------|--------|-----------------|-----------------|---------|
| getAllX() | X | Yes/No | Filter/Explicit/None | ✅/❌ |

Check:
- [ ] Entity extends `TenantBaseEntity`?
- [ ] All public service methods have `@Transactional` or `@Transactional(readOnly = true)`?
- [ ] `findAll()` calls are within transactional context?
- [ ] `findById()` results are validated against current church? (`findById()` **bypasses** Hibernate filters — explicit church check required)
- [ ] Custom `@Query` methods include `WHERE e.church.id = :churchId`?
- [ ] SUPERADMIN exception is properly handled?
- [ ] Private/helper methods that call repository don't bypass isolation?

### 3.2 Permission Enforcement
- [ ] All controller endpoints have `@RequirePermission` or `@PreAuthorize`
- [ ] Permissions exist in `Permission.java`
- [ ] Permissions are assigned to correct roles in `Role.java`
- [ ] Permissions exist in frontend `permission.enum.ts`
- [ ] Permission names follow naming convention: `{ENTITY}_{ACTION}[_{SCOPE}]`

### 3.3 IDOR (Insecure Direct Object Reference)
Check if any endpoint allows accessing resources belonging to another church or user by manipulating IDs:

- [ ] **Cross-church resource access**: Can Church A admin access Church B's resources by guessing IDs?
- [ ] **Horizontal privilege escalation**: Can a MEMBER view another member's private data (pastoral notes, financial history)?
- [ ] **Vertical privilege escalation**: Can lower roles perform higher-role actions (MEMBER creating users, PASTOR elevating own role)?
- [ ] **Fellowship scope enforcement**: Does FELLOWSHIP_LEADER access stay scoped to their fellowship?
- [ ] **Cross-resource IDOR**: Can a user add another church's member to their fellowship?
- [ ] **ID enumeration**: Do error responses distinguish "not found" from "forbidden"? (Should not — return 404 for both to avoid confirming resource existence)

For each `findById()` or path-parameter endpoint:
```
Is the returned resource validated to belong to the requesting user's church/scope?
```

### 3.4 SQL Injection Prevention
- [ ] No raw SQL string concatenation (`"SELECT ... WHERE name = '" + input + "'"`)
- [ ] All `@Query` methods use parameterized `:param` syntax
- [ ] Native queries (`nativeQuery = true`) use parameter binding, not string interpolation
- [ ] Search/filter endpoints don't pass user input directly into queries
- [ ] Sort/order parameters are validated against an allowlist (not passed raw to `Sort.by()`)
- [ ] Pagination parameters (`page`, `size`) are bounds-checked

### 3.5 XSS (Cross-Site Scripting) Prevention
- [ ] User-supplied text fields (names, descriptions, notes) are not rendered as raw HTML
- [ ] API responses use `Content-Type: application/json` (prevents browser script execution)
- [ ] No endpoint returns user input in HTML responses
- [ ] Fields that accept rich text are sanitized before storage
- [ ] Search query parameters are not reflected unsanitized in error messages

Common payloads to consider in the module's text fields:
```
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
javascript:alert('XSS')
{{constructor.constructor('alert(1)')()}}
```

### 3.6 Sensitive Data Leakage
Check all response DTOs and error responses in this module:

- [ ] **Passwords**: No password or hash (`$2a$`, `$2b$` BCrypt prefix) in responses
- [ ] **Tokens**: No refresh tokens, JWT secrets, or API keys in responses
- [ ] **Stack traces**: Error responses don't expose `java.lang.*`, `NullPointerException`, `.java:` line numbers
- [ ] **File paths**: No `/home/`, `/var/`, `/src/main/` paths in responses
- [ ] **Internal IDs**: No database sequence values or Hibernate internals leaked
- [ ] **PII exposure by role**: Lower roles don't see fields meant for higher roles (e.g., MEMBER shouldn't see other members' phone numbers, pastoral notes)
- [ ] **Email/user enumeration**: Failed lookups don't confirm whether a resource exists (use generic "not found" messages)

### 3.7 Token & Session Security
If the module handles authentication, tokens, or session state:

- [ ] Expired tokens return 401 (not 200 with partial data)
- [ ] Invalid/malformed tokens return 401
- [ ] Missing `Authorization` header returns 401
- [ ] Token with wrong signature returns 401
- [ ] Refresh token rotation invalidates old tokens

### 3.8 State-Based Access Control
- [ ] **Subscription enforcement**: Does the module check subscription status? Premium features should return 402 when subscription expired
- [ ] **Account state**: Locked/deactivated accounts cannot access this module's endpoints
- [ ] **Entity state**: Archived/deleted entities cannot be modified
- [ ] **Tier limits**: Member count limits, storage limits enforced if applicable

### 3.9 Bulk Operation Security
If the module has bulk/batch endpoints (import, export, bulk delete):

- [ ] Bulk operations require appropriate permissions (IMPORT/EXPORT permissions)
- [ ] Bulk operations validate ALL IDs belong to the requesting church (can't slip in cross-tenant IDs)
- [ ] Bulk import validates data before insertion (no injection via CSV/Excel)
- [ ] Bulk export doesn't leak fields that the requesting role shouldn't see
- [ ] Rate limiting or size limits on bulk operations to prevent DoS

### 3.10 Input Validation & Boundary Security
- [ ] Very long input (>10,000 chars) handled gracefully (no OOM, no untruncated DB write)
- [ ] Special characters (`\0`, unicode, RTL markers) don't break processing
- [ ] Negative IDs, zero IDs handled (return 400, not 500)
- [ ] File uploads validated: type, size, content (not just extension)
- [ ] Date inputs validated (no future dates where inappropriate, no impossible ranges)

### 3.11 Security Test Coverage
Check if dedicated security tests exist for this module:

| Security Category | Test Exists? | Test File | Notes |
|-------------------|-------------|-----------|-------|
| Tenant isolation | ✅/❌ | ... | Cross-church data access |
| IDOR | ✅/❌ | ... | Direct object reference manipulation |
| SQL injection | ✅/❌ | ... | Malicious query parameters |
| XSS | ✅/❌ | ... | Script injection in text fields |
| Data leakage | ✅/❌ | ... | Sensitive fields in responses |
| RBAC | ✅/❌ | ... | All 7 roles tested |
| Bulk operation | ✅/❌ | ... | Cross-tenant IDs in bulk |

Reference test files (check if they cover this module's endpoints):
- `SqlInjectionPreventionTest.java`
- `XssPreventionTest.java`
- `SensitiveDataLeakageTest.java`
- `IdorPreventionTest.java`
- `EdgeCaseSecurityTest.java`
- `CrossTenantAccessTest.java`
- `RoleBasedAccessControlTest.java`

Flag any category where this module has NO test coverage.

---

## Phase 4: Edge Cases & Error Handling

### 4.1 Null Safety
- [ ] Null checks on optional fields before access
- [ ] `Optional` properly handled (no `.get()` without `.isPresent()`)
- [ ] Nullable database columns handled in mappers

### 4.2 Boundary Conditions
- [ ] Empty list handling (returns `[]`, not null or error)
- [ ] Zero/negative values handled (amounts, counts, IDs)
- [ ] String length limits enforced (matching DB column sizes)
- [ ] Date range validations (start before end)
- [ ] Pagination edge cases (page 0, negative page, huge page size)

### 4.3 Percentage/Rate Calculations
- [ ] Division by zero prevented with `total > 0` checks
- [ ] Percentages use the correct capping strategy per the classification below

**MUST be capped at 100%** (use `Math.min(value, 100.0)`):
These represent ratios where the numerator is a subset of the denominator — exceeding 100% is a bug.

| Metric | Why |
|--------|-----|
| Attendance rate | Can't attend more sessions than exist |
| Profile completeness | Can't complete more fields than exist |
| Goal/task completion rate | Can't complete more steps than defined |
| Visitor → Member conversion rate | Converted count ≤ total visitors |
| Member retention rate | Retained ≤ total members |
| Budget utilization (expense vs. budget) | Overspend is tracked separately, utilization caps at 100% |
| SMS delivery rate | Delivered ≤ sent |
| Check-in rate | Checked in ≤ registered |
| Read/open rate (notifications) | Opened ≤ sent |

**CAN exceed 100%** (do NOT cap):
These represent progress toward a target or relative change — exceeding 100% is valid and expected.

| Metric | Why |
|--------|-----|
| Campaign progress (raised vs. goal) | Fundraising commonly exceeds the goal |
| Pledge fulfillment (paid vs. pledged) | Overpayment is possible and valid |
| Donation vs. previous period (growth %) | Growth can exceed 100% |
| Fund balance change (%) | A fund can more than double |
| Membership growth rate (%) | Congregation can more than double |
| Event registration vs. capacity | Waitlists / oversubscription |
| Welfare disbursement vs. contributions | Can disburse more than collected (from reserves) |

**When auditing**: Identify which category each percentage calculation in the module falls into. Flag any capped metric that is missing `Math.min()`, and flag any uncapped metric that incorrectly uses `Math.min()`.

### 4.4 Concurrency & Data Integrity
- [ ] Optimistic locking (`@Version`) for entities updated by multiple users
- [ ] Unique constraints enforced at DB level (not just application level)
- [ ] Cascading deletes won't orphan related records

### 4.5 Error Responses
- [ ] Consistent error response format (field-level errors for validation)
- [ ] Meaningful error messages (not generic "Internal Server Error")
- [ ] Proper HTTP status codes (400 for validation, 403 for forbidden, 404 for not found)
- [ ] No stack traces or sensitive info leaked in error responses

---

## Phase 5: Code Quality

### 5.1 Architecture
- [ ] Follows Controller → Service → Repository pattern
- [ ] No circular dependencies
- [ ] Proper use of DTOs (no entity exposure in API responses)
- [ ] Mappers are used consistently (not inline mapping in some places, mapper in others)

### 5.2 Date/Time Types
- [ ] Timestamps use `Instant` (not `LocalDateTime` or `Date`)
- [ ] Date-only fields use `LocalDate`
- [ ] Migrations use `DATETIME` or `TIMESTAMP` for Instant fields

### 5.3 Naming Consistency
- [ ] Endpoint paths follow REST conventions
- [ ] Method names are descriptive and consistent
- [ ] DTO field names match between request/response and entity

---

## Phase 6: Audit Report

### Summary

| Category | Score | Issues |
|----------|-------|--------|
| Code Completeness | ?/10 | ... |
| Test Coverage | ?% | ... |
| Security | ?/10 | ... |
| Edge Case Handling | ?/10 | ... |
| Code Quality | ?/10 | ... |
| **Overall** | **?/10** | |

### Critical Issues (fix immediately)
List any CRITICAL security vulnerabilities or data integrity risks.

### High Priority (fix soon)
List issues that affect correctness or could cause bugs.

### Medium Priority (improve)
List code quality and maintainability improvements.

### Low Priority (nice to have)
List minor improvements and suggestions.

### Missing Tests (prioritized)
Numbered list of specific tests to write, ordered by importance:
1. [Most critical missing test]
2. [Next most critical]
3. ...

### Recommendations
Actionable suggestions for improving the module, including:
- Specific code changes with file paths and line numbers
- New tests to write
- Refactoring opportunities
- Performance improvements if applicable

---

## Execution Instructions

1. **Use parallel agents** (Task tool with Explore subagent) to read all module files simultaneously
2. **Read every file thoroughly** — do not skim or assume
3. **Cross-reference** controller permissions with Role.java assignments
4. **Check the frontend** for matching permission guards and API calls
5. **Be specific** — always include file paths, line numbers, and code snippets
6. **Be honest** — if something is well-implemented, say so. Don't manufacture issues.
7. **Prioritize** — critical security issues first, style nits last
