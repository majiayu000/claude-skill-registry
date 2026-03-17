---
name: api-contract-validator
description: |
  Validates API contracts for correctness, compatibility, and compliance. Tests REST APIs against
  OpenAPI/Swagger specifications. Detects breaking changes between versions, validates runtime
  responses against schemas, and ensures backward compatibility before deployment.
license: MIT
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebFetch
compatibility:
  claude-code: ">=1.0.0"
metadata:
  version: "1.0.0"
  author: "QuantQuiver AI R&D"
  category: "testing"
  tags:
    - api-testing
    - openapi
    - contract-testing
    - breaking-changes
---

# API Contract Validator

## Purpose

Validates API contracts for correctness, compatibility, and compliance. Tests REST APIs against OpenAPI/Swagger specifications. Detects breaking changes between versions and validates runtime responses against schemas.

## Triggers

Use this skill when:

- "validate API contract"
- "test API endpoints"
- "check for breaking changes"
- "API compatibility test"
- "contract testing"
- "verify OpenAPI spec"

## When to Use

- New API version deployment
- Consumer complaints about changes
- Pre-release validation
- Multi-service integration testing
- Third-party API consumption validation

## When NOT to Use

- Unit testing internal functions (use unit-test-generator)
- Load testing (use performance-benchmark)
- Security testing (use security-test-suite)
- Data quality validation (use data-validation)

---

## Core Instructions

### Validation Categories

| Category | Description | Severity |
| -------- | ----------- | -------- |
| **Schema Compliance** | Response matches OpenAPI schema | Critical |
| **Status Codes** | Correct codes for scenarios | Critical |
| **Breaking Changes** | Backward incompatible changes | Critical |
| **Deprecations** | Deprecated fields/endpoints | Warning |
| **Headers** | Required headers present | Medium |
| **Error Format** | Error responses follow standard | Low |

### Breaking Change Detection

| Change Type | Severity | Example |
| ----------- | -------- | ------- |
| Removed endpoint | Critical | DELETE /api/v1/users removed |
| Removed field | Critical | `user.legacy_id` no longer returned |
| Type change | Critical | `id` changed from string to integer |
| Added required param | Critical | New required `tenant_id` parameter |
| Changed authentication | Critical | API key to OAuth2 |
| Removed enum value | High | Status no longer accepts "pending" |

### Validation Procedure

1. **Specification Analysis Phase**
   - Load OpenAPI/Swagger specification
   - Validate spec structure and completeness
   - Identify all endpoints and schemas
   - Parse security definitions

2. **Breaking Change Detection Phase**
   - Compare current spec to previous version
   - Identify removed endpoints/methods
   - Detect schema changes (fields, types)
   - Flag new required parameters

3. **Runtime Validation Phase** (if enabled)
   - Make HTTP requests to live API
   - Validate response status codes
   - Check response against schema
   - Measure response times

---

## Templates

### Validation Report

```markdown
# API Contract Validation Report

**Generated:** {timestamp}
**Specification:** {spec_path}

## Summary

| Metric | Value |
| ------ | ----- |
| Total Endpoints | {count} |
| Passed | {passed} |
| Failed | {failed} |
| Breaking Changes | {breaking_count} |

## Breaking Changes

### {endpoint_path}

**Type:** {change_type}
**Description:** {description}
**Migration:** {migration_guide}

## Endpoint Tests

| Method | Path | Status | Response Time |
| ------ | ---- | ------ | ------------- |
| {method} | {path} | {status_icon} | {time}ms |
```

---

## Example

**Input**: Compare two OpenAPI specs for breaking changes

**Output**:

```markdown
## Breaking Changes

### /api/users/{id}

**Type:** removed_field
**Description:** Field 'legacy_id' was removed from response
**Migration:** Update consumers to use 'id' field instead

### /api/orders

**Type:** added_required
**Description:** Parameter 'tenant_id' became required
**Migration:** All consumers must now provide tenant_id header
```

---

## Validation Checklist

- [ ] OpenAPI specification is valid and complete
- [ ] All endpoints have documented responses
- [ ] Breaking changes have migration guidance
- [ ] Runtime tests cover all documented endpoints
- [ ] Error responses follow standard format
- [ ] Authentication methods are properly tested

---

## Related Skills

- `unit-test-generator` - For internal function testing
- `security-test-suite` - For API security testing
- `performance-benchmark` - For API load testing
