---
name: gitlab-members
description: "Manages GitLab members. Use for listing members in groups or projects. Triggers: user access, permissions."
---

### Overview
Handles membership queries.

### Available Tools
- `get_group_members`: Retrieve a list of members in a specific GitLab group, optionally filtered by query or user IDs.
  - **Parameters**:
    - `group_id` (str): Optional. - Group ID or path
    - `query` (Optional[str]): Optional. - Filter members by search term in name or username
    - `user_ids` (Optional[List[int]]): Optional. - Filter members by user IDs
    - `skip_users` (Optional[List[int]]): Optional. - Exclude specified user IDs
    - `show_seat_info` (Optional[bool]): Optional. - Include seat information for members
- `get_project_members`: Retrieve a list of members in a specific GitLab project, optionally filtered by query or user IDs.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `query` (Optional[str]): Optional. - Filter members by search term in name or username
    - `user_ids` (Optional[List[int]]): Optional. - Filter members by user IDs
    - `skip_users` (Optional[List[int]]): Optional. - Exclude specified user IDs

### Usage Instructions
1. Filters: query, user_ids.

### Examples
- Group members: `get_group_members` with group_id="mygroup", query="john".
- Project: Similar for projects.

### Error Handling
- No members: Empty list is valid.
