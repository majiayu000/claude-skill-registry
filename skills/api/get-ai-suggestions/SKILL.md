---
name: get-ai-suggestions
description: Use when SDK method names are ugly, wanting to improve operation IDs, or asking "how can I improve my spec"
---

# get-ai-suggestions

Use `speakeasy suggest` for AI-powered improvements.

## Prerequisites

For non-interactive environments (CI/CD, AI agents), set:
```bash
export SPEAKEASY_API_KEY="<your-api-key>"
```
See `configure-authentication` skill for details.

## Commands

```bash
# Suggest better operation IDs (method names)
speakeasy suggest operation-ids -s <spec-path>

# Suggest error type definitions
speakeasy suggest error-types -s <spec-path>

# Output suggestions as overlay file
speakeasy suggest operation-ids -s <spec-path> -o suggested-overlay.yaml
```

## Operation ID Suggestions

Transforms auto-generated names into intuitive SDK method names:
- `get_api_v1_users_list` → `listUsers`
- `post_api_v1_users_create` → `createUser`

## Error Type Suggestions

Analyzes your API and suggests structured error responses:
- Common HTTP error codes (400, 401, 404, 500)
- Custom error schemas

## Applying Suggestions

```bash
# Generate overlay with suggestions
speakeasy suggest operation-ids -s openapi.yaml -o operation-ids-overlay.yaml

# Add to workflow.yaml
sources:
  my-api:
    inputs:
      - location: ./openapi.yaml
    overlays:
      - location: ./operation-ids-overlay.yaml

# Regenerate
speakeasy run
```
