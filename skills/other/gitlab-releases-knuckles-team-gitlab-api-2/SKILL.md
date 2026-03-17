---
name: gitlab-releases
description: "Manages GitLab releases. Use for creating, updating, deleting releases and assets. Triggers: versioning, deployments."
---

### Overview
Handles release artifacts.

### Available Tools
- `get_releases`: Retrieve a list of releases for a specific GitLab project, optionally filtered.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `include_html_description` (Optional[bool]): Optional. - Whether to include HTML descriptions
    - `sort` (Optional[str]): Optional. - Sort releases by criteria (e.g., 'released_at')
    - `order_by` (Optional[str]): Optional. - Order releases by criteria (e.g., 'asc', 'desc')
- `get_latest_release`: Retrieve details of the latest release in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
- `get_latest_release_evidence`: Retrieve evidence for the latest release in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
- `get_latest_release_asset`: Retrieve a specific asset for the latest release in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `direct_asset_path` (str): Optional. - Path to the asset (e.g., 'assets/file.zip')
- `get_group_releases`: Retrieve a list of releases for a specific GitLab group, optionally filtered.
  - **Parameters**:
    - `group_id` (str): Optional. - Group ID or path
    - `include_html_description` (Optional[bool]): Optional. - Whether to include HTML descriptions
    - `sort` (Optional[str]): Optional. - Sort releases by criteria (e.g., 'released_at')
    - `order_by` (Optional[str]): Optional. - Order releases by criteria (e.g., 'asc', 'desc')
- `download_release_asset`: Download a release asset from a group's release in GitLab.
  - **Parameters**:
    - `group_id` (str): Optional. - Group ID or path
    - `tag_name` (str): Optional. - Tag name of the release (e.g., 'v1.0.0')
    - `direct_asset_path` (str): Optional. - Path to the asset (e.g., 'assets/file.zip')
- `get_release_by_tag`: Retrieve details of a release by its tag in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `tag_name` (str): Optional. - Tag name of the release (e.g., 'v1.0.0')
- `create_release`: Create a new release in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `name` (str): Optional. - Name of the release
    - `tag_name` (str): Optional. - Tag name associated with the release (e.g., 'v1.0.0')
    - `description` (Optional[str]): Optional. - Description of the release
    - `released_at` (Optional[str]): Optional. - Release date in ISO 8601 format
    - `assets` (Optional[Dict]): Optional. - Dictionary of release assets
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `create_release_evidence`: Create evidence for a release in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `tag_name` (str): Optional. - Tag name of the release (e.g., 'v1.0.0')
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `update_release`: Update a release in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `tag_name` (str): Optional. - Tag name of the release to update (e.g., 'v1.0.0')
    - `name` (Optional[str]): Optional. - New name of the release
    - `description` (Optional[str]): Optional. - New description of the release
    - `released_at` (Optional[str]): Optional. - New release date in ISO 8601 format
    - `assets` (Optional[Dict]): Optional. - Updated dictionary of release assets
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `delete_release`: Delete a release in a GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `tag_name` (str): Optional. - Tag name of the release to delete (e.g., 'v1.0.0')
    - `ctx` (Optional[Context]): Optional. - MCP context for progress

### Usage Instructions
1. Tag-based.

### Examples
- Create: `create_release` with project_id="123", tag_name="v1.0", name="Version 1".
- Delete: `delete_release` with tag_name="v1.0".

### Error Handling
- Tag missing: Create tag first.
