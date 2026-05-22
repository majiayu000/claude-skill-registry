---
name: optimistic-ui-mutation-patterns
description: Implement immediate UI feedback for mutations with robust rollback capabilities.
---

# Optimistic UI Mutation Patterns

## Summary
Implement immediate UI feedback for mutations with robust rollback capabilities.

## Key Capabilities
- Update local cache instantly upon mutation trigger.
- Queue mutations to handle network race conditions.
- Rollback to the correct server state on failure.

## PhD-Level Challenges
- Manage dependency updates for optimistic data.
- Handle cascading optimistic updates correctly.
- Visualize the 'pending' state effectively.

## Acceptance Criteria
- Demonstrate immediate feedback on a slow network.
- Show accurate rollback upon mocked server error.
- Document the mutation queue logic.
