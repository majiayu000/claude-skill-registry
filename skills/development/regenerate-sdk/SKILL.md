---
name: regenerate-sdk
description: Use when your spec changed and you need to regenerate the SDK, or running `speakeasy run`
---

# regenerate-sdk

Use `speakeasy run` to execute the workflow and regenerate SDKs.

## Prerequisites

For non-interactive environments (CI/CD, AI agents), set:
```bash
export SPEAKEASY_API_KEY="<your-api-key>"
```
See `configure-authentication` skill for details.

## Command

```bash
# Run all configured targets
speakeasy run

# Run specific target only
speakeasy run -t <target-name>

# Run with specific source
speakeasy run -s <source-name>

# AI-friendly output mode
speakeasy run --output console
```

## When to Use

- After updating the OpenAPI spec
- After modifying workflow.yaml
- After changing overlays
- To regenerate with latest Speakeasy version

## Example Workflow

```yaml
# .speakeasy/workflow.yaml
workflowVersion: 1.0.0
speakeasyVersion: latest
sources:
  my-api:
    inputs:
      - location: ./openapi.yaml
targets:
  typescript-sdk:
    target: typescript
    source: my-api
    output: ./sdk/typescript
```

## AI-Friendly Output

For commands with large outputs, pipe to `grep` or `tail` to reduce context:
```bash
speakeasy run --output console 2>&1 | tail -50
```

## Troubleshooting

If `speakeasy run` fails, check:
1. Is the OpenAPI spec valid? Run `speakeasy lint openapi -s <spec>`
2. Does the source path exist? Check `inputs.location` in workflow.yaml
3. Are there blocking validation errors? See `diagnose-generation-failure` skill
