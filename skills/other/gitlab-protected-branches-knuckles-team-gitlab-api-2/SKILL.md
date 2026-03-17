---
name: gitlab-protected-branches
description: "Manages protected branches in GitLab. Use for protecting/unprotecting branches, code owner approvals. Triggers: branch protection."
---

### Overview
Secures branches.

### Available Tools
- `get_protected_branches`: Retrieve a list of protected branches in a specific GitLab project or Retrieve details of a specific protected branch in a GitLab project..
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `branch` (Optional[str]): Optional. - Name of the branch to retrieve (e.g., 'main')
- `protect_branch`: Protect a specific branch in a GitLab project with specified access levels.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `branch` (str): Optional. - Name of the branch to protect (e.g., 'main')
    - `push_access_level` (Optional[str]): Optional. - Access level for pushing (e.g., 'maintainer')
    - `merge_access_level` (Optional[str]): Optional. - Access level for merging (e.g., 'developer')
    - `unprotect_access_level` (Optional[str]): Optional. - Access level for unprotecting (e.g., 'maintainer')
    - `allow_force_push` (Optional[bool]): Optional. - Whether force pushes are allowed
    - `allowed_to_push` (Optional[List[Dict]]): Optional. - List of users or groups allowed to push
    - `allowed_to_merge` (Optional[List[Dict]]): Optional. - List of users or groups allowed to merge
    - `allowed_to_unprotect` (Optional[List[Dict]]): Optional. - List of users or groups allowed to unprotect
    - `code_owner_approval_required` (Optional[bool]): Optional. - Whether code owner approval is required
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `unprotect_branch`: Unprotect a specific branch in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `branch` (str): Optional. - Name of the branch to unprotect (e.g., 'main')
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `require_code_owner_approvals_single_branch`: Require or disable code owner approvals for a specific branch in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `branch` (str): Optional. - Name of the branch to set approval requirements for (e.g., 'main')
    - `code_owner_approval_required` (bool): Optional. - Whether code owner approval is required
    - `ctx` (Optional[Context]): Optional. - MCP context for progress

### Usage Instructions
1. Access levels: push/merge.

### Examples
- Protect: `protect_branch` with project_id="123", branch="main", push_access_level="maintainer".
- Code owners: `require_code_owner_approvals_single_branch` with code_owner_approval_required=true.

### Error Handling
- Already protected: Update instead.
