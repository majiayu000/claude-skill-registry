---
id: notion-project-tracking
name: Notion Project Tracking
description: Query databases, track tasks, status updates
role: product
requiredTools:
  - type: mcpService
    serviceType: notion
---

## Notion Project Tracking

When tracking projects or tasks in Notion:

- Query databases with filters and sorts to list tasks or items by status, assignee, or date.
- Read database schema (properties) before querying so filters use valid values.
- When creating database pages, include required properties and use the correct types.
- For status updates, use update database page to change status or other properties.
- Summarize results clearly (e.g. count by status, list of open items).

## Step-by-step instructions

1. Identify the target database (and optionally workspace) from the user’s question.
2. If needed, read the database schema to get property names and allowed values for filters.
3. Query the database with filters (status, assignee, date) and sort as needed; summarize counts and key items.
4. For “create task”: use create database page with required properties and correct types.
5. For “update status” (or other property): use update database page with the page ID and new values.

## Examples of inputs and outputs

- **Input**: “What tasks are open for Project X?”  
  **Output**: Count and short list (title, status, assignee) from a database query filtered by project and status.

- **Input**: “Mark task Y as Done.”  
  **Output**: Confirm the task and new status; call update database page; then “Updated [title] to Done.”

## Common edge cases

- **Database not found**: Say so and suggest checking the database name or listing available databases.
- **Invalid filter value**: Check schema for allowed values (e.g. status options) and retry or ask the user.
- **Missing required property on create**: Read schema, list required properties, and ask or infer values before creating.
- **API/oauth error**: Report Notion error and suggest reconnecting or retrying.

## Tool usage for specific purposes

- **Query database**: Use to list tasks by status, assignee, project, or date; use filters and sort; then summarize.
- **Read database/schema**: Use before querying or creating so filters and new pages use valid property names and types.
- **Create database page**: Use to add a task; include all required properties.
- **Update database page**: Use to change status or other properties on an existing task.
