---
name: gitlab-merge-requests
description: "Manages GitLab merge requests. Use for creating, listing MRs across projects or groups. Triggers: PRs, code reviews."
---

### Overview
Covers MR creation and queries.

### Available Tools
- `create_merge_request`: Create a new merge request in a GitLab project with specified source and target branches.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `source_branch` (str): Optional. - Source branch for the merge request
    - `target_branch` (str): Optional. - Target branch for the merge request
    - `title` (str): Optional. - Title of the merge request
    - `description` (Optional[str]): Optional. - Description of the merge request
    - `assignee_id` (Optional[int]): Optional. - ID of the user to assign the merge request to
    - `reviewer_ids` (Optional[List[int]]): Optional. - IDs of users to set as reviewers
    - `labels` (Optional[List[str]]): Optional. - Labels to apply to the merge request
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `get_merge_requests`: Retrieve a list of merge requests across all projects, optionally filtered by state, scope, or labels.
  - **Parameters**:
    - `state` (Optional[str]): Optional. - Filter merge requests by state (e.g., 'opened', 'closed')
    - `scope` (Optional[str]): Optional. - Filter merge requests by scope (e.g., 'created_by_me')
    - `milestone` (Optional[str]): Optional. - Filter merge requests by milestone title
    - `view` (Optional[str]): Optional. - Filter merge requests by view (e.g., 'simple')
    - `labels` (Optional[List[str]]): Optional. - Filter merge requests by labels
    - `author_id` (Optional[int]): Optional. - Filter merge requests by author ID
- `get_project_merge_requests`: Retrieve a list of merge requests for a specific GitLab project, optionally filtered or a single merge request or a single merge request by merge id
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `merge_id` (Optional[int]): Optional. - Merge request ID
    - `state` (Optional[str]): Optional. - Filter merge requests by state (e.g., 'opened', 'closed')
    - `scope` (Optional[str]): Optional. - Filter merge requests by scope (e.g., 'created_by_me')
    - `milestone` (Optional[str]): Optional. - Filter merge requests by milestone title
    - `labels` (Optional[List[str]]): Optional. - Filter merge requests by labels

### Usage Instructions
1. For creation: source/target branches, title.

### Examples
- Create: `create_merge_request` with project_id="123", source_branch="feature", target_branch="main", title="New feature".
- List: `get_project_merge_requests` with project_id="123", state="opened".

### Error Handling
- Conflicts: Resolve before creation.
