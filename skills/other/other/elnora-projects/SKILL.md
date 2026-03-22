---
name: elnora-projects
description: >
  This skill should be used when the user asks to "list projects", "create a project",
  "get project details", "show my Elnora projects", "new project", "project members",
  "add member", "remove member", "change role", "archive project",
  or any task involving Elnora Platform project management.
---

# Elnora Projects

Manage projects on the Elnora AI Platform. Projects are the top-level containers for tasks (conversations) and files (protocol outputs). Each project has members with roles that control access.

## Organization Context

All list and create tools accept an optional `org_id` parameter (UUID). When
provided, the operation targets that organization instead of the user's active
org. The user must be a member of the target org.

## Concepts

- **Project**: A workspace containing tasks and files. Has a name, description, icon, and member list.
- **Member roles**: `owner` (full control, cannot be removed), `admin` (manage members and settings), `member` (create tasks and files).
- **Archive**: Soft-deletes a project. **This hides all tasks and files in the project.** Always confirm with the user first.
- **All IDs are UUIDs** (e.g., `bfdc6fbd-40ed-4042-9ea7-c79a5ec90085`).

## MCP Tools

### elnora_list_projects

List all projects you have access to.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | integer | No | 1 | Page number (min: 1) |
| `page_size` | integer | No | 25 | Results per page (min: 1, max: 100) |

Returns paginated results:

```json
{
  "items": [
    {
      "id": "<UUID>",
      "name": "Protocol Lab",
      "description": "PCR and cloning protocols",
      "icon": "...",
      "isDefault": false,
      "isArchived": false,
      "memberCount": 3,
      "myRole": "owner",
      "createdAt": "...",
      "updatedAt": "..."
    }
  ],
  "page": 1,
  "pageSize": 25,
  "totalCount": 4,
  "totalPages": 1,
  "hasNextPage": false
}
```

Key fields: `id` (needed for all other operations), `name`, `myRole`, `memberCount`.

### elnora_get_project

Get full details for a single project, including its member list.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_id` | uuid | Yes | Project UUID |

Returns project detail with `members` array:

```json
{
  "id": "<UUID>",
  "name": "Protocol Lab",
  "description": "...",
  "icon": "...",
  "memberCount": 2,
  "myRole": "owner",
  "members": [
    {
      "id": "<UUID>",
      "userId": 42,
      "email": "user@example.com",
      "displayName": "Jane Doe",
      "role": "owner",
      "createdAt": "..."
    }
  ]
}
```

Use this to check membership and roles before performing operations.

### elnora_create_project

Create a new project.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Project name (min: 1, max: 200 chars) |
| `description` | string | No | Project description (max: 2,000 chars) |
| `icon` | string | No | Project icon/emoji (max: 50 chars) |

Returns the created project with its new `id`. The creating user becomes the owner.

### elnora_update_project

Update project metadata.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_id` | uuid | Yes | Project UUID |
| `name` | string | No | New name (min: 1, max: 200 chars) |
| `description` | string | No | New description (max: 2,000 chars) |
| `icon` | string | No | New icon (max: 50 chars) |

Must provide at least one of `name`, `description`, or `icon`.

### elnora_archive_project

Archive (soft-delete) a project. **This hides all tasks and files in the project. Confirm with the user before calling.**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_id` | uuid | Yes | Project UUID |

## Member Management

### elnora_list_project_members

List all members of a project.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_id` | uuid | Yes | Project UUID |

Returns an array of members with `userId`, `email`, `displayName`, and `role`.

### elnora_add_project_member

Add a user to a project.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_id` | uuid | Yes | Project UUID |
| `user_id` | string | Yes | User ID to add (max: 255 chars) |
| `role` | string | No | Role to assign (default: "Member", max: 100 chars) |

### elnora_remove_project_member

Remove a user from a project.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_id` | uuid | Yes | Project UUID |
| `user_id` | string | Yes | User ID to remove (max: 255 chars) |

Cannot remove the project owner.

### elnora_update_project_member_role

Change a project member's role.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_id` | uuid | Yes | Project UUID |
| `user_id` | string | Yes | User ID (max: 255 chars) |
| `role` | string | Yes | New role (max: 100 chars) |

### elnora_leave_project

Leave a project you are a member of.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_id` | uuid | Yes | Project UUID |

Owners cannot leave their own project without transferring ownership first.

## Pagination

List endpoints return page-based pagination:

```json
{
  "items": [...],
  "page": 1,
  "pageSize": 25,
  "totalCount": 50,
  "totalPages": 2,
  "hasNextPage": true
}
```

If `hasNextPage` is true, increment `page` and call again.

## Agent Workflow Recipes

### Find a project by name

1. Call `elnora_list_projects` to get all projects
2. Scan the `items` array for a matching `name`
3. Use the `id` for subsequent operations

### Create a project and start generating protocols

1. Call `elnora_create_project` with a `name` and `description`
2. Call `elnora_create_task` with the new project's `id` and an `initial_message`
3. Read the response with `elnora_get_task_messages`

### Check project membership before adding someone

1. Call `elnora_get_project` to see current members
2. If the user is not already a member, call `elnora_add_project_member`

### Transfer effective ownership

1. Call `elnora_update_project_member_role` to promote another member to owner/admin
2. The original owner remains but the new member now has elevated access
