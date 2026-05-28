---
name: response-timestamps
description: Automatically adds timestamps and execution duration to all Claude responses
type: guardrail
enforcement: suggest
priority: high
---

# Response Timestamp Guardrail

## Purpose
Ensure all Claude responses include start timestamp, end timestamp, and execution duration for tracking and accountability.

## Rules

### At Response Start
Begin every response with:
```
🕒 Response Started: [YYYY-MM-DD HH:MM:SS TIMEZONE]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### At Response End
End every response with:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🕒 Response Completed: [YYYY-MM-DD HH:MM:SS TIMEZONE]
⏱️  Execution Duration: [X minutes Y seconds]
```

### Format Requirements
- Use ISO 8601 format: `YYYY-MM-DD HH:MM:SS TIMEZONE`
- Always include timezone (PST, UTC, EST, UTC, etc.)
- Calculate duration from start to completion
- Use emojis for visual clarity (🕒 for time, ⏱️ for duration)
- Include separator lines for visual distinction

### Example
```
🕒 Response Started: 2025-12-07 14:30:45 PST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Response content here]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🕒 Response Completed: 2025-12-07 14:32:18 PST
⏱️  Execution Duration: 1 minute 33 seconds
```

## Exceptions
None - this applies to ALL responses without exception.
