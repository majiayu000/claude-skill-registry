---
name: gitlab-environments
description: "Manages GitLab environments. Use for creating, updating, deleting, or protecting deployment environments. Triggers: CI/CD environments, deployments."
---

### Overview
Covers environment lifecycle and protection.

### Available Tools
- `get_environments`: Retrieve a list of environments for a GitLab project, optionally filtered by name, search, or states or a single environment by id.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `environment_id` (Optional[int]): Optional. - Environment ID
    - `name` (Optional[str]): Optional. - Filter environments by exact name
    - `search` (Optional[str]): Optional. - Filter environments by search term in name
    - `states` (Optional[str]): Optional. - Filter environments by state (e.g., 'available', 'stopped')
- `create_environment`: Create a new environment in a GitLab project with a specified name and optional external URL.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `name` (str): Optional. - Name of the environment
    - `external_url` (Optional[str]): Optional. - External URL for the environment
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `update_environment`: Update an existing environment in a GitLab project with new name or external URL.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `environment_id` (int): Optional. - Environment ID
    - `name` (Optional[str]): Optional. - New name for the environment
    - `external_url` (Optional[str]): Optional. - New external URL for the environment
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `delete_environment`: Delete a specific environment in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `environment_id` (int): Optional. - Environment ID
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `stop_environment`: Stop a specific environment in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `environment_id` (int): Optional. - Environment ID
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `stop_stale_environments`: Stop stale environments in a GitLab project, optionally filtered by older_than timestamp.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `older_than` (Optional[str]): Optional. - Filter environments older than this timestamp (ISO 8601 format)
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `delete_stopped_environments`: Delete stopped review app environments in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `get_protected_environments`: Retrieve protected environments in a GitLab project (list or single by name).
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `name` (str): Optional. - Name of the protected environment
- `protect_environment`: Protect an environment in a GitLab project with optional approval count.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `name` (str): Optional. - Name of the environment to protect
    - `required_approval_count` (Optional[int]): Optional. - Number of approvals required for deployment
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `update_protected_environment`: Update a protected environment in a GitLab project with new approval count.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `name` (str): Optional. - Name of the protected environment
    - `required_approval_count` (Optional[int]): Optional. - New number of approvals required for deployment
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `unprotect_environment`: Unprotect a specific environment in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `name` (str): Optional. - Name of the environment to unprotect
    - `ctx` (Optional[Context]): Optional. - MCP context for progress

### Usage Instructions
1. Use name and external_url for creation.
2. Protection: Set required_approval_count.

### Examples
- Create: `create_environment` with project_id="123", name="prod", external_url="https://prod.example.com".
- Protect: `protect_environment` with project_id="123", name="prod", required_approval_count=2.

### Error Handling
- State conflicts: Check status before ops.
