---
context: fork
model: haiku
---

# /task

Quick-create a task linked to a project, optionally with subtasks.

## Usage

```
/task <title>
/task <title> for <project>
/task <title> due <date>
/task <title> priority high
/task <title> with subtasks
```

## Examples

```
/task Review ADR draft
/task Complete security assessment for MyProject due Friday
/task Update architecture diagram priority high for CloudMigration
/task Platform Migration Tasks with subtasks
```

## Instructions

1. Parse the command for:
   - **title**: Task description (required)
   - **project**: Project to link (after "for")
   - **dueBy**: Hard deadline (after "due") - parse natural language
   - **doDate**: When to start working (after "start" or "do")
   - **priority**: high/medium/low (after "priority")
   - **subtasks**: If "with subtasks" mentioned, prompt for subtask titles

2. Defaults:
   - priority: medium
   - dueBy: null
   - doDate: null
   - project: null (or infer from recent context)
   - parentTask: null
   - subtasks: []

3. Generate filename: `Task - {{title}}.md`

4. Create task in vault root:

```markdown
---
type: Task
title: {{ title }}
created: {{ DATE }}
modified: {{ DATE }}
completed: false
priority: {{ priority }}
doDate: {{ do_date or null }}
dueBy: {{ due_date or null }}
project: {{ project_link or null }}
assignedTo: ["[[Your Name]]"]
parentTask: {{ parent_task_link or null }}
subtasks: {{ subtask_links or [] }}
tags: []
---

# {{title}}

## Description

{{title expanded if needed}}

## Acceptance Criteria

- [ ]

## Subtasks

{{list of subtask links if any}}

## Notes

## Related

{{project link if provided}}
```

5. If project provided:
   - Format as wiki-link: `"[[Project - MyProject]]"`
   - Fuzzy match project name if partial

6. If due date provided:
   - Parse natural language: "Friday" → next Friday's date
   - "tomorrow" → tomorrow's date
   - "next week" → Monday of next week
   - Format as YYYY-MM-DD

7. If subtasks requested:
   - Prompt for subtask titles (or parse from context)
   - Create each subtask as a separate Task note
   - Link subtasks in parent's `subtasks` array
   - Set each subtask's `parentTask` field to parent

8. Subtask conventions:
   - Parent task: `subtasks: ["[[Task - Subtask 1]]", "[[Task - Subtask 2]]"]`
   - Child task: `parentTask: "[[Task - Parent Task]]"`
   - Parent completion: only mark complete when all subtasks complete
   - Child inherits project/priority from parent unless overridden

9. After creating:
   - Confirm creation with file path
   - Show task summary
   - List any created subtasks
   - Suggest adding to daily note
