---
name: vigilante-issue-implementation-on-nx
description: Implement a GitHub issue end-to-end when Vigilante dispatches work for an Nx monorepo.
---

# Vigilante Nx Issue Implementation

## Focus
- Read the prompt for the detected stack, workspace hints, and shared local-service contract before changing code.
- Limit edits and validation to the affected Nx apps or libs unless broader changes are required.
- If local services are required, call `vigilante-local-service-dependencies` first and then use the shared `docker-compose-launch` contract instead of writing ad hoc Compose logic.

## Workflow
- Follow the base `vigilante-issue-implementation-on-monorepo` workflow for issue comments, validation, push, and PR creation.
- Use Nx-native workspace commands when they exist and match the touched projects.
- Keep service startup scoped to the assigned worktree and only for implementation or test dependencies.
