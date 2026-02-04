---
name: status
description: Show sprint progress
allowed-tools: Read, TaskList
model: haiku
user-invocable: true
---

# Status

Show current sprint progress with minimal token usage.

## Process

1. Read `project-meta.json` for sprint context and roadmap
2. Call `TaskList` to get all tasks
3. Display:

```
[project-name] | Sprint: [name]
═════════════════════════════════
Progress: [N]/[N] complete | [N] verified
In Progress: [N] | Ready: [N] | Blocked: [N]

Active:
  → [SID] [subject] (in_progress)

Next:
  [SID] [subject] (ready)
  [SID] [subject] (ready)

Roadmap: [N] epics remaining (~[N] stories)
Historical: [N] tasks completed across [N] sprints
```

## Rules
- Do NOT read source files, only project-meta.json
- Use haiku model for minimal cost
- If no project-meta.json exists, suggest running `audit` or `npx claude-auto-dev --init`
