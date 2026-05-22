---
name: api-contract-validation
description: Detect breaking changes in API contracts (OpenAPI/Swagger specs)
version: 1.0.0
allowed-tools: [Bash, Read]
---

# API Contract Validation Skill

You are the api-contract-validation skill. When invoked, you validate API contracts to prevent breaking changes that could break client applications.

## When to Invoke This Skill

**Invoke this skill when:**
- Making changes to API endpoints
- Modifying request/response schemas
- Before deploying API updates
- Reviewing PRs with API changes
- In CI/CD pipeline for API projects

**Do NOT invoke when:**
- No OpenAPI/Swagger spec exists
- Creating brand new API (no baseline)
- Non-REST APIs (GraphQL, gRPC - different validation)
- Internal APIs with no external clients

---

## Your Task

When invoked:
1. Execute the API contract validation script
2. Read the generated validation report
3. Return a summary to the calling agent

---

## Step 1: Execute API Validation Script

Use the **Bash** tool to run the pre-built validation script:

```bash
python3 .claude/skills/api-contract-validation/validate.py
```

This script will:
- Find OpenAPI/Swagger specification files
- Load baseline (previous version) for comparison
- Compare specs to detect breaking changes
- Identify safe changes
- Generate recommendations
- Create `bazinga/artifacts/{SESSION_ID}/skills/api_contract_validation.json`

---

## Step 2: Read Generated Report

Use the **Read** tool to read:

```bash
bazinga/artifacts/{SESSION_ID}/skills/api_contract_validation.json
```

Extract key information:
- `status` - breaking_changes_detected/safe/no_baseline
- `breaking_changes` - Array of critical/high severity issues
- `warnings` - Medium severity changes
- `safe_changes` - Backward-compatible changes
- `recommendations` - Safe alternatives

---

## Step 3: Return Summary

Return a concise summary to the calling agent:

```
API Contract Validation:
- Specs analyzed: {count}
- Baseline: {exists/created}

⚠️  BREAKING CHANGES: {count}
- Critical: {count}
- High: {count}

Safe changes: {count}

{If breaking changes:}
Top recommendations:
1. {recommendation}
2. {recommendation}

Details saved to: bazinga/artifacts/{SESSION_ID}/skills/api_contract_validation.json
```

---

## Example Invocation

**Scenario: Breaking Change Detected**

Input: Tech Lead reviewing API changes that remove an endpoint

Expected output:
```
API Contract Validation:
- Specs analyzed: 1 (openapi.yaml)
- Baseline: exists

⚠️  BREAKING CHANGES: 3
- Critical (1): Endpoint /api/users/{id} DELETE removed - clients will break
- High (2): Required field "email" removed from /api/users response
            Response status changed from 200 to 404 for /api/orders

Safe changes: 2

Top recommendations:
1. Use API versioning (/v2/api/users) instead of removing endpoint
2. Add "email" field back or create new versioned endpoint
3. Deprecate with 410 Gone status before complete removal

Details saved to: bazinga/artifacts/{SESSION_ID}/skills/api_contract_validation.json
```

**Scenario: First Run (Baseline Created)**

Input: First API contract validation

Expected output:
```
API Contract Validation:
- Specs analyzed: 1 (openapi.yaml)
- Baseline: created

Baseline created from current API specification.
Run this skill again after making API changes to detect breaking changes.

Details saved to: bazinga/artifacts/{SESSION_ID}/skills/api_contract_validation.json
```

**Scenario: All Safe Changes**

Input: Tech Lead reviewing API additions only

Expected output:
```
API Contract Validation:
- Specs analyzed: 1 (openapi.yaml)
- Baseline: exists

✅ No breaking changes detected

Safe changes: 4
- New endpoint added: POST /api/health
- Optional field added to /api/users: "created_at"
- New enum value added: status="archived"
- Documentation updated for /api/orders

All changes are backward-compatible.

Details saved to: bazinga/artifacts/{SESSION_ID}/skills/api_contract_validation.json
```

---

## Error Handling

**If no specs found:**
- Return: "No OpenAPI/Swagger specs found. Cannot validate API contracts."

**If spec parsing fails:**
- Return: "Failed to parse spec: {error}. Check spec format."

**If no baseline:**
- Create baseline from current spec
- Return: "Baseline created for future comparisons."

---

## Notes

- The script handles all spec parsing and comparison logic
- Endpoint removal is CRITICAL (breaks existing clients)
- Field removal from responses is HIGH severity
- Adding optional fields is safe
- Type widening (int → float) may be safe depending on clients
- Always suggest versioning over breaking changes
