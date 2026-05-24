---
name: ab-testing-infrastructure
description: Build high-integrity experimentation frameworks within React applications.
---

# A/B Testing Infrastructure

## Summary
Build high-integrity experimentation frameworks within React applications.

## Key Capabilities
- Assign experiment cohorts deterministically client-side.
- Render variant components without layout shifts.
- Track exposure events accurately upon component mount.

## PhD-Level Challenges
- Avoid 'flicker of original content' (FOOC).
- Ensure statistical significance by preventing tracking errors.
- Manage interactions between overlapping experiments.

## Acceptance Criteria
- Implement an assignment and tracking provider.
- Demonstrate variant rendering with no flicker.
- Document experiment collision handling.
