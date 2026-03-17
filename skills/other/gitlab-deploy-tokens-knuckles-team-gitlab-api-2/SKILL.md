---
name: gitlab-deploy-tokens
description: "Manages GitLab deploy tokens. Use for creating, listing, or deleting tokens at instance, project, or group levels. Triggers: deploy keys, access tokens."
---

### Overview
Handles deploy tokens for CI/CD access.

### Available Tools
- `get_deploy_tokens`: Retrieve a list of all deploy tokens for the GitLab instance.
- `get_project_deploy_tokens`: Retrieve a list of deploy tokens for a specific GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `token_id` (Optional[int]): Optional. - Deploy token ID
- `create_project_deploy_token`: Create a deploy token for a GitLab project with specified name and scopes.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `name` (str): Optional. - Name of the deploy token
    - `scopes` (List[str]): Optional. - Scopes for the deploy token (e.g., ['read_repository'])
    - `expires_at` (Optional[str]): Optional. - Expiration date (ISO 8601 format)
    - `username` (Optional[str]): Optional. - Username associated with the token
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `delete_project_deploy_token`: Delete a specific deploy token for a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `token_id` (int): Optional. - Deploy token ID
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `get_group_deploy_tokens`: Retrieve deploy tokens for a GitLab group (list or single by ID).
  - **Parameters**:
    - `group_id` (str): Optional. - Group ID or path
    - `token_id` (Optional[int]): Optional. - Deploy token ID for single retrieval
- `create_group_deploy_token`: Create a deploy token for a GitLab group with specified name and scopes.
  - **Parameters**:
    - `group_id` (str): Optional. - Group ID or path
    - `name` (str): Optional. - Name of the deploy token
    - `scopes` (List[str]): Optional. - Scopes for the deploy token (e.g., ['read_repository'])
    - `expires_at` (Optional[str]): Optional. - Expiration date (ISO 8601 format)
    - `username` (Optional[str]): Optional. - Username associated with the token
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `delete_group_deploy_token`: Delete a specific deploy token for a GitLab group.
  - **Parameters**:
    - `group_id` (str): Optional. - Group ID or path
    - `token_id` (int): Optional. - Deploy token ID
    - `ctx` (Optional[Context]): Optional. - MCP context for progress

### Usage Instructions
1. Specify scopes as list (e.g., ["read_repository"]).
2. Use expires_at for time-bound tokens.

### Examples
- Create project token: `create_project_deploy_token` with project_id="123", name="ci-token", scopes=["read_registry"].
- List group tokens: `get_group_deploy_tokens` with group_id="group/path".

### Error Handling
- Duplicate names: Use unique names.
- Revocation: Delete to revoke.
