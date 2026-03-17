---
name: openapi-workflow
description: Proactive OpenAPI workflow. Triggers when OpenAPI spec files are modified to validate, regenerate code, and verify builds.
---

# OpenAPI Workflow Skill

Automatically runs the OpenAPI workflow when spec files are modified.

## When to Activate

This skill should activate when:
- Files in `backend/api/*.yaml` are modified
- New endpoints are added to OpenAPI spec
- Request/response schemas are changed
- User asks to add/modify API endpoints

## OpenAPI Spec Location

| Type | Path | Purpose |
|------|------|---------|
| API Spec | `backend/api/openapi.yaml` | Public API definition |

## Workflow Steps

### 1. Validate Spec
```bash
python3 scripts/openapi_workflow.py --validate
```

### 2. Generate Code (All Platforms)
```bash
python3 scripts/openapi_workflow.py --codegen
```

This generates:
- **Backend (Go)**: `backend/internal/generated/`
- **iOS (Swift)**: `mobile/ios/App/Generated/`
- **Android (Kotlin)**: `mobile/android/app/src/main/java/.../generated/`
- **Web (TypeScript)**: `web/src/generated/`

### 3. Build Verification
```bash
python3 scripts/openapi_workflow.py --build
```

### 4. Full Workflow (All Steps)
```bash
python3 scripts/openapi_workflow.py --full
```

## Critical Rules

| Rule | Why |
|------|-----|
| Define response schemas properly | Inline schemas don't generate reusable types |
| Use plural file names | REST convention: `users.yaml` not `user.yaml` |
| Always regenerate after spec changes | Generated code must match spec |
| Verify ALL platforms build | API changes affect backend + iOS + Android + web |

## Process

1. Detect OpenAPI spec was modified
2. Run validation to catch syntax/semantic errors
3. Regenerate code for all platforms
4. Run build verification
5. Report any failures

## Output Format

```
## OpenAPI Workflow Results

**Spec Modified**: [file path]
**Validation**: ✅ Passed / ❌ Failed
**Code Generation**: ✅ All platforms / ❌ Failed for [platform]
**Build Verification**: ✅ All platforms / ❌ Failed for [platform]

[Details of any failures]
```

## Reference

- Script: `scripts/openapi_workflow.py`
- Spec: `backend/api/openapi.yaml`
