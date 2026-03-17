---
id: todoist-task-management
name: Todoist Task Management
description: Add, list, and close tasks; list projects
role: product
requiredTools:
  - type: mcpService
    serviceType: todoist
---

## Todoist Task Management

When managing tasks in Todoist:

- Use **todoist_add_task** (tool name may have a suffix if multiple Todoist servers exist) to create tasks with natural language due dates.
- Use **todoist_get_tasks** to list active tasks using Todoist filters (e.g. by project, date, label).
- Use **todoist_close_task** to complete a task by ID.
- Use **todoist_get_projects** to list projects and resolve project IDs when the user refers to a project by name.
- Todoist OAuth does not provide refresh tokens; suggest reconnecting if the token is revoked.

## Step-by-step instructions

1. For "add task X": call **todoist_add_task** with content and optional due string (natural language, e.g. "tomorrow", "next Monday"); optionally specify project_id from **todoist_get_projects** if the user named a project.
2. For "list my tasks" or "tasks for project Y": call **todoist_get_tasks** with filter string and/or project_id; summarize task content, due date, and ID.
3. For "complete task Z": call **todoist_close_task** with the task ID; confirm completion to the user.
4. When project is ambiguous: call **todoist_get_projects** and list names/IDs so the user can choose, or infer from context.
5. Keep summaries concise (task content, due, ID); avoid dumping full payloads unless asked.

## Examples of inputs and outputs

- **Input**: "Add a task: Review PR by tomorrow."  
  **Output**: Call **todoist_add_task** with content "Review PR" and due "tomorrow"; confirm "Added task: Review PR (due tomorrow)."

- **Input**: "What tasks are due this week?"  
  **Output**: List of tasks from **todoist_get_tasks** with an appropriate filter (e.g. "due: this week"); summarize content, due date, and ID per task.

- **Input**: "Mark task 12345 as done."  
  **Output**: Call **todoist_close_task** with id 12345; confirm "Task 12345 completed."

## Common edge cases

- **Project not found**: Use **todoist_get_projects** to list projects; say "Project [name] not found" or suggest the closest match.
- **Task not found**: Say "Task [id] not found" and suggest listing tasks to get valid IDs.
- **Natural language due**: **todoist_add_task** accepts natural language (e.g. "tomorrow", "next Friday"); use it when the user gives a relative date.
- **API/OAuth error**: Report that Todoist returned an error; mention that reconnecting may be needed if the token was revoked.

## Tool usage for specific purposes

- **todoist_add_task**: Use to create a task; include content and optional due (natural language) and project_id.
- **todoist_get_tasks**: Use to list active tasks; use filter and/or project_id to scope.
- **todoist_close_task**: Use to complete a task by ID.
- **todoist_get_projects**: Use to list projects and resolve project_id when the user refers to a project by name.
