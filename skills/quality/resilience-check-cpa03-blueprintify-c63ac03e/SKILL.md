---
name: resilience-check
description: Checklist for reliability engineering
---

## Procedure

1. Check for `try/catch` blocks around async operations.
2. Verify timeouts are set on external calls.
3. Ensure fallbacks exist for failed data fetches.
4. Validate input types at boundaries.
5. Check for proper error logging.
