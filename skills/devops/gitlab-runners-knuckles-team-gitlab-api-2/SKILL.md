---
name: gitlab-runners
description: "Manages GitLab runners. Use for registering, updating, deleting runners at various levels. Triggers: CI infrastructure."
---

### Overview
Covers runner setup.

### Available Tools
- `get_runners`: Retrieve a list of runners in GitLab, optionally filtered by scope, type, status, or tags or Retrieve details of a specific GitLab runner..
  - **Parameters**:
    - `runner_id` (Optional[int]): Optional. - ID of the runner to retrieve
    - `scope` (Optional[str]): Optional. - Filter runners by scope (e.g., 'active')
    - `type` (Optional[str]): Optional. - Filter runners by type (e.g., 'instance_type')
    - `status` (Optional[str]): Optional. - Filter runners by status (e.g., 'online')
    - `tag_list` (Optional[List[str]]): Optional. - Filter runners by tags
- `update_runner_details`: Update details for a specific GitLab runner.
  - **Parameters**:
    - `runner_id` (int): Optional. - ID of the runner to update
    - `description` (Optional[str]): Optional. - New description of the runner
    - `active` (Optional[bool]): Optional. - Whether the runner is active
    - `tag_list` (Optional[List[str]]): Optional. - List of tags for the runner
    - `run_untagged` (Optional[bool]): Optional. - Whether the runner can run untagged jobs
    - `locked` (Optional[bool]): Optional. - Whether the runner is locked
    - `access_level` (Optional[str]): Optional. - Access level of the runner (e.g., 'ref_protected')
    - `maximum_timeout` (Optional[int]): Optional. - Maximum timeout for the runner in seconds
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `pause_runner`: Pause or unpause a specific GitLab runner.
  - **Parameters**:
    - `runner_id` (int): Optional. - ID of the runner to pause or unpause
    - `active` (bool): Optional. - Whether the runner should be active (True) or paused (False)
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `get_runner_jobs`: Retrieve jobs for a specific GitLab runner, optionally filtered by status or sorted.
  - **Parameters**:
    - `runner_id` (int): Optional. - ID of the runner to retrieve jobs for
    - `status` (Optional[str]): Optional. - Filter jobs by status (e.g., 'success', 'failed')
    - `sort` (Optional[str]): Optional. - Sort jobs by criteria (e.g., 'created_at')
- `get_project_runners`: Retrieve a list of runners in a specific GitLab project, optionally filtered by scope.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `scope` (Optional[str]): Optional. - Filter runners by scope (e.g., 'active')
- `enable_project_runner`: Enable a runner in a specific GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `runner_id` (int): Optional. - ID of the runner to enable
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `delete_project_runner`: Delete a runner from a specific GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `runner_id` (int): Optional. - ID of the runner to delete
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `get_group_runners`: Retrieve a list of runners in a specific GitLab group, optionally filtered by scope.
  - **Parameters**:
    - `group_id` (str): Optional. - Group ID or path
    - `scope` (Optional[str]): Optional. - Filter runners by scope (e.g., 'active')
- `register_new_runner`: Register a new GitLab runner.
  - **Parameters**:
    - `token` (str): Optional. - Registration token for the runner
    - `description` (Optional[str]): Optional. - Description of the runner
    - `tag_list` (Optional[List[str]]): Optional. - List of tags for the runner
    - `run_untagged` (Optional[bool]): Optional. - Whether the runner can run untagged jobs
    - `locked` (Optional[bool]): Optional. - Whether the runner is locked
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `delete_runner`: Delete a GitLab runner by ID or token.
  - **Parameters**:
    - `runner_id` (Optional[int]): Optional. - ID of the runner to delete
    - `token` (Optional[str]): Optional. - Token of the runner to delete
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `verify_runner_authentication`: Verify authentication for a GitLab runner using its token.
  - **Parameters**:
    - `token` (str): Optional. - Runner token to verify
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `reset_gitlab_runner_token`: Reset the GitLab runner registration token.
  - **Parameters**:
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `reset_project_runner_token`: Reset the registration token for a project's runner in GitLab.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `reset_group_runner_token`: Reset the registration token for a group's runner in GitLab.
  - **Parameters**:
    - `group_id` (str): Optional. - Group ID or path
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `reset_token`: Reset the authentication token for a specific GitLab runner.
  - **Parameters**:
    - `runner_id` (int): Optional. - ID of the runner to reset the token for
    - `token` (str): Optional. - Current token of the runner
    - `ctx` (Optional[Context]): Optional. - MCP context for progress

### Usage Instructions
1. Use tokens for registration.

### Examples
- Register: `register_new_runner` with token="abc123".
- Enable: `enable_project_runner` with runner_id=1.

### Error Handling
- Token invalid: Reset.
