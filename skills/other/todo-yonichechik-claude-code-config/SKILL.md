---
name: "todo"
description: "Parse input and create todo items"
argument-hint: "[tasks]"
---

Parse user input and create todo items.

**Input**: `$ARGUMENTS` containing todo descriptions

## Process

1. **Validate**: If `$ARGUMENTS` is empty, ask user to provide task descriptions.

2. **Parse**: Intelligently split input into items (numbered lists, comma-separated, natural language, etc.)

3. **Create**: Call TaskCreate tool with:
   - `subject`: Imperative form (what needs to be done)
   - `activeForm`: Present continuous form (what's happening now)
   - `description`: Detailed description of the task
   - Tasks are created with status "pending" by default

4. **Report**: Use TaskList to display tasks.

5. **Execute**: Continue working on next items in task list and push when done.
