---
name: migrate-api
description: Migrate API from one version to the next with backwards compatibility (Sofia + Daniel's workflow)
disable-model-invocation: true
---

Migrate the API: $ARGUMENTS

## Step 1 — Identify Breaking Changes
Read the current API and identify what needs to change:
- Renamed or removed endpoints
- Changed request/response schemas
- Changed authentication flow
- Changed error response format
- Changed URL paths or parameter names

Categorize each change:
- **Breaking**: Clients will fail without code changes
- **Additive**: New fields/endpoints — existing clients unaffected
- **Deprecation**: Old behavior still works but is discouraged

## Step 2 — Design the New Version
Create the new API version structure in a new version directory under the API layer.

### Rules:
- Previous version endpoints MUST continue working unchanged
- New version endpoints live in a new router with updated version prefix
- Shared logic stays in the service layer — NOT duplicated per version
- New Pydantic models can extend or replace previous models

## Step 3 — Implement New Version
1. Create new version directory with router files
2. Add new Pydantic models to the models file (suffix with version if different)
3. Register the new version router in the app factory
4. Previous version router remains registered and functional

## Step 4 — Deprecation Headers
Add deprecation headers to previous version endpoints:
```python
response.headers["Deprecation"] = "true"
response.headers["Sunset"] = "<date>"
response.headers["Link"] = '<new-version-url>; rel="successor-version"'
```

## Step 5 — Tests
- Previous version tests MUST still pass unchanged (backwards compatibility)
- Write new tests for new version endpoints in a new test file
- Test that previous version responses include deprecation headers

## Step 6 — Documentation
- Update project documentation with both version endpoint tables
- Update OpenAPI description noting deprecation
- Add migration guide for consumers

## Step 7 — Verify
Run the test command and the type-check command (see project config).
ALL tests pass — both versions.