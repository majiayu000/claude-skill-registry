---
name: gitlab-merge-rules
description: "Manages GitLab merge approval rules. Use for approvals, rules at project/group levels. Triggers: code reviews, approvals."
---

### Overview
Handles approval configurations.

### Available Tools
- `get_project_level_merge_request_approval_rules`: Retrieve project-level merge request approval rules for a GitLab project details of a specific project-level merge request approval rule.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `approval_rule_id` (int): Optional. - Approval rule ID
- `create_project_level_rule`: Create a new project-level merge request approval rule.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `name` (str): Optional. - Name of the approval rule
    - `approvals_required` (Optional[int]): Optional. - Number of approvals required
    - `rule_type` (Optional[str]): Optional. - Type of rule (e.g., 'regular')
    - `user_ids` (Optional[List[int]]): Optional. - List of user IDs required to approve
    - `group_ids` (Optional[List[int]]): Optional. - List of group IDs required to approve
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `update_project_level_rule`: Update an existing project-level merge request approval rule.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `approval_rule_id` (int): Optional. - Approval rule ID
    - `name` (Optional[str]): Optional. - New name for the approval rule
    - `approvals_required` (Optional[int]): Optional. - New number of approvals required
    - `user_ids` (Optional[List[int]]): Optional. - Updated list of user IDs required to approve
    - `group_ids` (Optional[List[int]]): Optional. - Updated list of group IDs required to approve
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `delete_project_level_rule`: Delete a project-level merge request approval rule.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `approval_rule_id` (int): Optional. - Approval rule ID
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `merge_request_level_approvals`: Retrieve approvals for a specific merge request in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `merge_request_iid` (int): Optional. - Merge request IID
- `get_approval_state_merge_requests`: Retrieve the approval state of a specific merge request in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `merge_request_iid` (int): Optional. - Merge request IID
- `get_merge_request_level_rules`: Retrieve merge request-level approval rules for a specific merge request in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `merge_request_iid` (int): Optional. - Merge request IID
- `approve_merge_request`: Approve a specific merge request in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `merge_request_iid` (int): Optional. - Merge request IID
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `unapprove_merge_request`: Unapprove a specific merge request in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `merge_request_iid` (int): Optional. - Merge request IID
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `get_group_level_rule`: Retrieve merge request approval settings for a specific GitLab group.
  - **Parameters**:
    - `group_id` (str): Optional. - Group ID or path
- `edit_group_level_rule`: Edit merge request approval settings for a specific GitLab group.
  - **Parameters**:
    - `group_id` (str): Optional. - Group ID or path
    - `allow_author_approval` (Optional[bool]): Optional. - Whether authors can approve their own merge requests
    - `allow_committer_approval` (Optional[bool]): Optional. - Whether committers can approve merge requests
    - `allow_overrides_to_approver_list` (Optional[bool]): Optional. - Whether overrides to the approver list are allowed
    - `minimum_approvals` (Optional[int]): Optional. - Minimum number of approvals required
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `get_project_level_rule`: Retrieve merge request approval settings for a specific GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
- `edit_project_level_rule`: Edit merge request approval settings for a specific GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `allow_author_approval` (Optional[bool]): Optional. - Whether authors can approve their own merge requests
    - `allow_committer_approval` (Optional[bool]): Optional. - Whether committers can approve merge requests
    - `allow_overrides_to_approver_list` (Optional[bool]): Optional. - Whether overrides to the approver list are allowed
    - `minimum_approvals` (Optional[int]): Optional. - Minimum number of approvals required
    - `ctx` (Optional[Context]): Optional. - MCP context for progress

### Usage Instructions
1. Use approvals_required, user/group IDs.

### Examples
- Create rule: `create_project_level_rule` with project_id="123", name="review", approvals_required=2.
- Approve MR: `approve_merge_request` with project_id="123", merge_request_iid=1.

### Error Handling
- Insufficient approvals: Check state.
