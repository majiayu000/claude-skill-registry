---
name: task-implementation
description: Execute next task from Implementation Plan. Use when user asks to implement next task, start next feature, or continue implementation.
---

# Task Implementation

## Workflow

1. Review `docs/Implementation Plan.md` to identify next pending task by priority order
2. Review `docs/PROJECT_OVERVIEW.md` to understand project context
3. Assess task size and choose approach:
   - **Small**: Implement directly
   - **Medium**: Design complete solution before coding
   - **Large**: Review `.cursor\skills\task-splitting\SKILL.md` to break into 2-3 subtasks
4. Implement with edge case tests to maintain coverage (Design for Testability)
5. Run `make ci` to verify
6. Review `.cursor\skills\docs-maintenance\SKILL.md` to update documentation
