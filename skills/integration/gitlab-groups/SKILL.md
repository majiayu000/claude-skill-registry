---
name: gitlab-groups
description: "Manages GitLab groups. Use for listing, editing groups, subgroups, projects, or merge requests. Triggers: group management, namespaces."
---

### Overview
Handles group structures and contents.

### Available Tools
- `get_groups`: Retrieve a list of groups, optionally filtered by search, sort, ownership, or access level or retrieve a single group by id.
  - **Parameters**:
    - `group_id` (Optional[str]): Optional. - Group ID or path
    - `search` (Optional[str]): Optional. - Filter groups by search term in name or path
    - `sort` (Optional[str]): Optional. - Sort order (e.g., 'asc', 'desc')
    - `order_by` (Optional[str]): Optional. - Field to sort by (e.g., 'name', 'path')
    - `owned` (Optional[bool]): Optional. - Filter groups owned by the authenticated user
    - `min_access_level` (Optional[int]): Optional. - Filter groups by minimum access level (e.g., 10 for Guest)
    - `top_level_only` (Optional[bool]): Optional. - Include only top-level groups (exclude subgroups)
- `edit_group`: Edit a specific GitLab group's details (name, path, description, or visibility).
  - **Parameters**:
    - `group_id` (str): Optional. - Group ID or path
    - `name` (Optional[str]): Optional. - New name for the group
    - `path` (Optional[str]): Optional. - New path for the group
    - `description` (Optional[str]): Optional. - New description for the group
    - `visibility` (Optional[str]): Optional. - New visibility level (e.g., 'public', 'private')
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `get_group_subgroups`: Retrieve a list of subgroups for a specific GitLab group, optionally filtered.
  - **Parameters**:
    - `group_id` (str): Optional. - Group ID or path
    - `search` (Optional[str]): Optional. - Filter subgroups by search term in name or path
    - `sort` (Optional[str]): Optional. - Sort order (e.g., 'asc', 'desc')
    - `order_by` (Optional[str]): Optional. - Field to sort by (e.g., 'name', 'path')
    - `owned` (Optional[bool]): Optional. - Filter subgroups owned by the authenticated user
- `get_group_descendant_groups`: Retrieve a list of all descendant groups for a specific GitLab group, optionally filtered.
  - **Parameters**:
    - `group_id` (str): Optional. - Group ID or path
    - `search` (Optional[str]): Optional. - Filter descendant groups by search term in name or path
    - `sort` (Optional[str]): Optional. - Sort order (e.g., 'asc', 'desc')
    - `order_by` (Optional[str]): Optional. - Field to sort by (e.g., 'name', 'path')
    - `owned` (Optional[bool]): Optional. - Filter descendant groups owned by the authenticated user
- `get_group_projects`: Retrieve a list of projects associated with a specific GitLab group, optionally including subgroups.
  - **Parameters**:
    - `group_id` (str): Optional. - Group ID or path
    - `include_subgroups` (Optional[bool]): Optional. - Include projects from subgroups
    - `search` (Optional[str]): Optional. - Filter projects by search term in name or path
    - `sort` (Optional[str]): Optional. - Sort order (e.g., 'asc', 'desc')
    - `order_by` (Optional[str]): Optional. - Field to sort by (e.g., 'name', 'path')
- `get_group_merge_requests`: Retrieve a list of merge requests associated with a specific GitLab group, optionally filtered.
  - **Parameters**:
    - `group_id` (str): Optional. - Group ID or path
    - `state` (Optional[str]): Optional. - Filter merge requests by state (e.g., 'opened', 'closed')
    - `scope` (Optional[str]): Optional. - Filter merge requests by scope (e.g., 'created_by_me')
    - `milestone` (Optional[str]): Optional. - Filter merge requests by milestone title
    - `search` (Optional[str]): Optional. - Filter merge requests by search term in title or description

### Usage Instructions
1. Use group_id for specifics.
2. Filters: search, sort, owned.

### Examples
- List subgroups: `get_group_subgroups` with group_id="mygroup".
- Get projects: `get_group_projects` with group_id="mygroup", include_subgroups=true.

### Error Handling
- Access denied: Check permissions.
