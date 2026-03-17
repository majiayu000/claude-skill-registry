---
name: git-cp
version: 1.0.0
description: '[Git] Stage, commit and push all code in the current branch'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Stage all files, create a meaningful commit based on changes, and push to remote repository.

**Workflow:**
1. **Stage** — Add all modified files to staging area
2. **Commit** — Create descriptive commit message based on actual changes
3. **Push** — Push to remote repository

**Key Rules:**
- Delegates to `git-manager` subagent for execution
- Commit message must reflect actual changes, not be generic
- Break work into todo tasks; add final self-review task

Use `git-manager` agent to stage all files, create a meaningful commit based on the changes and push to remote repository.

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
