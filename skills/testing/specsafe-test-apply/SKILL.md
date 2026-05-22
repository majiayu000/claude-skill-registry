---
name: specsafe-test-apply
description: Apply tests - development mode
argument-hint: "[spec-id]"
disable-model-invocation: true
---

Guide implementation for active spec:
- Read requirements and existing tests
- Implement one requirement at a time
- Follow cycle: Plan → Implement → Test → Commit
- Map every change to requirement IDs
- Never modify tests to make them pass (fix the code)
- Update PROJECT_STATE.md (TEST-CREATE → TEST-APPLY)

Ask: "Which requirement should we tackle next?"
