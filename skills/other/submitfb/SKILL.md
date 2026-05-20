---
description: Submit feedback to tracking system
allowed-tools: Bash
---

# Submit Feedback

Extract from conversation context:
- **Title:** Concise summary (max 80 chars)
- **Description:** Detailed description
- **Type:** bug / feature / general
- **Priority:** low / medium / high / critical
- **Page/Area:** If mentioned, otherwise system

## Show Preview

```
Title: [title]
Type: [type]
Priority: [priority]
Page/Area: [page-or-area]

Description:
[description]
```

## Submit (after confirmation)

```bash
node F:/_CODE/shared-scripts/feedback/submit-feedback.js "Title" "Description" --type [type] --priority [priority] --route [page-or-area]
```

Report result with feedback ID.
