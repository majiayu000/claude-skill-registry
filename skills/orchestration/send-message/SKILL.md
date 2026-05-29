---
name: send-message
description: Send a message to the orchestrator. Use for blockers, progress updates, requesting review, or communicating status during autonomous execution.
---

# Send Message

```bash
nancy msg <type> "<message>"
```

Types: `blocker`, `progress`, `review-request`

Examples:

```bash
nancy msg blocker "Cannot proceed: missing API credentials"
nancy msg progress "Completed database migration"
nancy msg review-request "Feature complete, ready for verification"
```
