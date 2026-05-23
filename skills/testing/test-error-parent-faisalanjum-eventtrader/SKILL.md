---
name: test-error-parent
description: Parent that calls error-prone child to test error propagation
context: fork
allowed-tools:
  - Skill
  - Write
  - Read
---

# Error Propagation Test

**Goal**: Test what parent sees when child skill fails.

## Task

1. Record that you're starting
2. Call `/test-error-child` (which will deliberately fail)
3. Capture EVERYTHING you receive back - error messages, return values, etc.
4. Write results to `earnings-analysis/test-outputs/error-parent-result.txt`

Include:
- What the child skill returned (full text)
- Whether you received an error message
- Whether you know the child failed
- How you could detect failure programmatically
