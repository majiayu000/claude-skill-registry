---
name: gitlab-branches
description: "Manages GitLab branches. Use for listing, creating, deleting, or querying branches in projects. Triggers: branch operations, git branching."
---

### Overview
This skill handles branch-related tasks in GitLab via MCP tools. Focus on one operation per call for efficiency.

### Available Tools
- `get_branches`: Get branches in a GitLab project, optionally filtered.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `search` (Optional[str]): Optional. - Filter branches by name containing this term
    - `regex` (Optional[str]): Optional. - Filter branches by regex pattern on name
    - `branch` (Optional[str]): Optional. - Branch name
- `create_branch`: Create a new branch in a GitLab project from a reference.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `branch` (str): Optional. - New branch name
    - `ref` (str): Optional. - Reference to create from (branch/tag/commit SHA)
- `delete_branch`: Delete a branch or all merged branches in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `branch` (Optional[str]): Optional. - Branch name to delete
    - `delete_merged_branches` (Optional[bool]): Optional. - Delete all merged branches (excluding protected)
    - `ctx` (Optional[Context]): Optional. - MCP context for progress

### Usage Instructions
1. Identify the project_id (e.g., from query or prior context).
2. Call the appropriate tool with minimal params.
3. Handle pagination if results exceed limits (use MCP's built-in support).

### Examples
- List branches: Call `get_branches` with project_id="my/project" and search="feature".
- Create: `create_branch` with project_id="123", branch="new-feature", ref="main".
- Delete merged: `delete_branch` with project_id="123", delete_merged_branches=true.

### Error Handling
- Missing params: Retry with required fields.
- 404: Branch/project not found—verify IDs.
- Rate limits: Wait and retry.
