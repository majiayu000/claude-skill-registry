---
name: gitlab-projects
description: "Manages GitLab projects. Use for listing, editing, archiving, sharing projects. Triggers: repo management."
---

### Overview
Handles project lifecycle.

### Available Tools
- `get_projects`: Retrieve a list of projects, optionally filtered by ownership, search, sort, or visibility or Retrieve details of a specific GitLab project.
  - **Parameters**:
    - `project_id` (Optional[str]): Optional. - Project ID or path
    - `owned` (Optional[bool]): Optional. - Filter projects owned by the authenticated user
    - `search` (Optional[str]): Optional. - Filter projects by search term in name or path
    - `sort` (Optional[str]): Optional. - Sort projects by criteria (e.g., 'created_at', 'name')
    - `visibility` (Optional[str]): Optional. - Filter projects by visibility (e.g., 'public', 'private')
- `get_nested_projects_by_group`: Retrieve a list of nested projects within a GitLab group, including descendant groups.
  - **Parameters**:
    - `group_id` (str): Optional. - Group ID or path
- `get_project_contributors`: Retrieve a list of contributors to a specific GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
- `get_project_statistics`: Retrieve statistics for a specific GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
- `edit_project`: Edit a specific GitLab project's details (name, description, or visibility).
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `name` (Optional[str]): Optional. - New name of the project
    - `description` (Optional[str]): Optional. - New description of the project
    - `visibility` (Optional[str]): Optional. - New visibility of the project (e.g., 'public', 'private')
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `get_project_groups`: Retrieve a list of groups associated with a specific GitLab project, optionally filtered.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `skip_groups` (Optional[List[int]]): Optional. - List of group IDs to exclude
    - `search` (Optional[str]): Optional. - Filter groups by search term in name
- `archive_project`: Archive a specific GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `unarchive_project`: Unarchive a specific GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `delete_project`: Delete a specific GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `share_project`: Share a specific GitLab project with a group, specifying access level.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `group_id` (str): Optional. - Group ID or path to share with
    - `group_access` (str): Optional. - Access level for the group (e.g., 'guest', 'developer', 'maintainer')
    - `expires_at` (Optional[str]): Optional. - Expiration date for the share in ISO 8601 format
    - `ctx` (Optional[Context]): Optional. - MCP context for progress

### Usage Instructions
1. Use visibility for updates.

### Examples
- Edit: `edit_project` with project_id="123", visibility="public".
- Share: `share_project` with project_id="123", group_id="group", group_access="maintainer".

### Error Handling
- Deletion permanent: Confirm first.
