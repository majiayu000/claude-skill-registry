---
description: Mark feedback completed or auto-create and complete
allowed-tools: Bash Read
---

# Done Command

**Args:** `$ARGUMENTS`

## Mode Detection

- First arg is 20+ alphanumeric chars -> complete existing feedback
- First arg has spaces/is descriptive -> auto-create and complete

## Complete Existing

```bash
node F:/_CODE/shared-scripts/feedback/fetch-feedback.js <id> completed "admin notes"
```

## Auto-Create (Quick Log)

```bash
node F:/_CODE/shared-scripts/feedback/submit-feedback.js "Title" "Description" --type feature --page system --user admin
node F:/_CODE/shared-scripts/feedback/fetch-feedback.js <new-id> completed "Title"
node F:/_CODE/shared-scripts/feedback/fetch-feedback.js <new-id> internal-only true
```

Parse feedback ID from submit output to use in subsequent commands.
