---
name: journal
version: 1.0.0
description: '[Utilities] Write some journal entries.'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Write journal entries documenting significant technical events, decisions, or incidents.

**Workflow:**
1. **Capture** -- Record the event, context, and impact
2. **Write** -- Create structured journal entry in plans/reports/

**Key Rules:**
- Use for significant events: bugs found, architectural decisions, incidents
- Follow report naming convention from plan context
- Break work into todo tasks; add final self-review task

Use the `journal-writer` subagent to explore the memories and recent code changes, and write some journal entries.
Journal entries should be concise and focused on the most important events, key changes, impacts, and decisions.
Keep journal entries in the `./docs/journals/` directory.

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
