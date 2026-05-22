---
name: validate-openapi-spec
description: Use when checking if an OpenAPI spec is valid, looking for errors, or running `speakeasy lint`
---

# validate-openapi-spec

Use `speakeasy lint` to check for errors and warnings.

## Command

```bash
speakeasy lint openapi -s <path-to-spec>
```

## Output Categories

| Severity | Meaning | Action |
|----------|---------|--------|
| Error | Blocks SDK generation | Must fix |
| Warning | May cause issues | Should fix |
| Hint | Best practice suggestion | Consider fixing |

## Common Validation Issues

| Issue | Solution |
|-------|----------|
| Missing operationId | Add operationId or use `speakeasy suggest operation-ids` |
| Invalid $ref | Fix the reference path |
| Missing response schema | Add response schema definitions |
| Duplicate operationId | Make operation IDs unique |

## AI-Friendly Output

For commands with large outputs, pipe to `grep` or `tail` to reduce context:
```bash
speakeasy lint openapi -s ./openapi.yaml 2>&1 | grep -E "(error|warning)"
```
