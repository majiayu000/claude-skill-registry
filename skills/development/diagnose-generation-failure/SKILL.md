---
name: diagnose-generation-failure
description: Use when SDK generation failed, seeing "Step Failed: Workflow", or `speakeasy run` errors
---

# diagnose-generation-failure

When SDK generation fails, determine the root cause and fix strategy.

## Diagnosis Steps

1. **Run lint to get detailed errors:**
   ```bash
   speakeasy lint openapi -s <spec-path>
   ```

2. **Categorize issues:**
   - **Fixable with overlays:** Missing descriptions, poor operation IDs
   - **Requires spec fix:** Invalid schema, missing required fields
   - **Requires user input:** Design decisions, authentication setup

## Decision Framework

| Issue Type | Fix Strategy | Example |
|------------|--------------|---------|
| Missing operationId | Overlay | Use `speakeasy suggest operation-ids` |
| Missing description | Overlay | Add via overlay |
| Invalid $ref | **Ask user** | Broken reference needs spec fix |
| Circular reference | **Ask user** | Design decision needed |
| Missing security | **Ask user** | Auth design needed |

## What NOT to Do

- **Do NOT** disable lint rules to hide errors
- **Do NOT** try to fix every issue one-by-one
- **Do NOT** modify source spec without asking
- **Do NOT** assume you can fix structural problems

## Strategy Document

For complex issues, produce a document:

```markdown
## OpenAPI Spec Analysis

### Blocking Issues (require user input)
- [List issues that need human decision]

### Fixable Issues (can use overlays)
- [List issues with proposed overlay fixes]

### Recommended Approach
[Your recommendation]
```
