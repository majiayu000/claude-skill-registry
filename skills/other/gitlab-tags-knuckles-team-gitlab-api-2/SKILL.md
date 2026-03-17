---
name: gitlab-tags
description: "Manages GitLab tags. Use for creating, deleting, protecting tags. Triggers: versioning."
---

### Overview
Handles tags and protection.

### Available Tools
- `get_tags`: Retrieve a list of tags for a specific GitLab project, optionally filtered or sorted or Retrieve details of a specific tag in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `name` (Optional[str]): Optional. - Name of the tag to retrieve (e.g., 'v1.0.0')
    - `search` (Optional[str]): Optional. - Filter tags by search term in name
    - `sort` (Optional[str]): Optional. - Sort tags by criteria (e.g., 'name', 'updated')
- `create_tag`: Create a new tag in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `name` (str): Optional. - Name of the tag to create (e.g., 'v1.0.0')
    - `ref` (str): Optional. - Reference (e.g., branch or commit SHA) to tag
    - `message` (Optional[str]): Optional. - Tag message
    - `release_description` (Optional[str]): Optional. - Release description associated with the tag
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `delete_tag`: Delete a specific tag in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `name` (str): Optional. - Name of the tag to delete (e.g., 'v1.0.0')
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `get_protected_tags`: Retrieve a list of protected tags in a specific GitLab project, optionally filtered by name.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `name` (Optional[str]): Optional. - Filter tags by name
- `get_protected_tag`: Retrieve details of a specific protected tag in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `name` (str): Optional. - Name of the protected tag to retrieve (e.g., 'v1.0.0')
- `protect_tag`: Protect a specific tag in a GitLab project with specified access levels.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `name` (str): Optional. - Name of the tag to protect (e.g., 'v1.0.0')
    - `create_access_level` (Optional[str]): Optional. - Access level for creating the tag (e.g., 'maintainer')
    - `allowed_to_create` (Optional[List[Dict]]): Optional. - List of users or groups allowed to create the tag
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `unprotect_tag`: Unprotect a specific tag in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `name` (str): Optional. - Name of the tag to unprotect (e.g., 'v1.0.0')
    - `ctx` (Optional[Context]): Optional. - MCP context for progress

### Usage Instructions
1. Ref for creation.

### Examples
- Create: `create_tag` with project_id="123", name="v1.0", ref="main".
- Protect: `protect_tag` with create_access_level="maintainer".

### Error Handling
- Tag exists: Delete first.
