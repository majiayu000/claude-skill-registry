---
name: todoist-rs
cluster: community
description: "Todoist: tasks, projects, labels, filters, reminders, Karma, API, IFTTT/Zapier integration"
tags: ["todoist","tasks","gtd","productivity"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "todoist task project label filter reminder karma api"
---

# todoist-rs

## Purpose
This skill enables interaction with the Todoist API via a Rust-based client, allowing programmatic management of tasks, projects, labels, filters, reminders, and Karma. Use it to automate productivity workflows by integrating with Todoist's REST API.

## When to Use
Use this skill for GTD-based task management, such as adding tasks in response to user queries, syncing projects with other tools, or handling reminders via API calls. Apply it in scenarios requiring automation, like daily task reviews or IFTTT/Zapier triggers for productivity apps.

## Key Capabilities
- CRUD operations on tasks: Create, read, update, delete tasks using Todoist's API endpoints.
- Manage projects and labels: Add, rename, or archive projects; assign labels to tasks.
- Handle filters and reminders: Query tasks with custom filters; set due dates and reminders.
- Access Karma and productivity stats: Retrieve user Karma scores and activity logs.
- API integrations: Support for IFTTT/Zapier via webhooks, using Todoist's API for event triggers.

## Usage Patterns
Initialize the Todoist client with your API key from an environment variable, then chain method calls for operations. Always handle authentication first. For CLI usage, wrap the Rust library in a script; for code, import the crate and use async methods. Pass parameters like task content or project IDs directly in function calls. Test in a development environment before production to avoid rate limits.

## Common Commands/API
Use the Todoist API endpoints via the todoist-rs crate. Set the API key via `$TODOIST_API_KEY`. Example code snippets:

- Add a task:
  ```rust
  use todoist::Todoist;
  let client = Todoist::new(std::env::var("TODOIST_API_KEY").unwrap());
  client.add_task("Buy milk", Some("Shopping")).await;
  ```

- Get tasks with a filter:
  ```rust
  let tasks = client.get_tasks(&[("filter", "overdue")]).await.unwrap();
  for task in tasks { println!("{}", task.content); }
  ```

- Update a project:
  Use PUT /projects/{id} endpoint; in code:
  ```rust
  client.update_project(123, "New Project Name").await;
  ```

- Common CLI flags (if wrapping in a tool): `--api-key $TODOIST_API_KEY --project-id 123 --task "Do something"`.
- Config format: Store API key in a .env file as `TODOIST_API_KEY=your_token`, then load with `std::env::var`.

## Integration Notes
Integrate with IFTTT/Zapier by setting up webhooks on Todoist's API events (e.g., new task created). Use the skill's API calls to trigger actions: for IFTTT, point to POST /tasks; for Zapier, use the Todoist app in Zapier with this skill's methods. Pass data like task IDs via JSON payloads. Ensure the API key is securely handled in env vars, and test integrations with sample events to verify data flow.

## Error Handling
Check for API errors like 401 (unauthorized) by verifying the `$TODOIST_API_KEY` before requests. Handle rate limits (e.g., 429 status) with exponential backoff in code. Use Rust's Result types for error propagation:
  ```rust
  match client.add_task("Task", None).await {
      Ok(_) => println!("Success"),
      Err(e) => eprintln!("Error: {}", e),
  }
  ```
Log detailed errors (e.g., network failures) and retry transient issues. Validate inputs like project IDs to prevent 404 errors.

## Concrete Usage Examples
1. **Add a task with a label**: When a user says "Add a shopping task", use the skill to create a task in the "Shopping" project: Initialize client, call `client.add_task("Buy groceries", Some("Shopping")).await`, then confirm with the user.
2. **Query overdue tasks**: For a daily reminder, fetch overdue tasks: Use `client.get_tasks(&[("filter", "overdue")]).await`, loop through results, and notify the user with task details.

## Graph Relationships
- Related to: productivity (e.g., gtd skills), task-management (e.g., other todo apps), api-clients (e.g., rest-api wrappers).
- Connects to: IFTTT/Zapier integrations for automation, community cluster skills for collaborative tools.
