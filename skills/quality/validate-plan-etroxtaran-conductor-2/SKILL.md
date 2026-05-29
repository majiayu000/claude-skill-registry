---
name: validate-plan
description: Review the plan for security and architecture risks before implementation.
---

# Validate Plan

## When to use

- Before implementation starts.

## Instructions

1. Run `/validator-security` and `/validator-architecture` in parallel.
2. Consolidate results into:
   - approved / needs_changes / rejected
   - blocking issues
   - required plan edits
