---
name: gitlab-packages
description: "Manages GitLab packages. Use for listing, publishing, or downloading packages. Triggers: artifact registry."
---

### Overview
Covers package repository ops.

### Available Tools
- `get_repository_packages`: Retrieve a list of repository packages for a specific GitLab project, optionally filtered by package type.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `package_type` (Optional[str]): Optional. - Filter packages by type (e.g., 'npm', 'maven')
- `publish_repository_package`: Publish a repository package to a specific GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `package_name` (str): Optional. - Name of the package
    - `package_version` (str): Optional. - Version of the package
    - `file_name` (str): Optional. - Name of the package file
    - `status` (Optional[str]): Optional. - Status of the package (e.g., 'default', 'hidden')
    - `ctx` (Optional[Context]): Optional. - MCP context for progress
- `download_repository_package`: Download a repository package from a specific GitLab project.
  - **Parameters**:
    - `project_id` (str): Optional. - Project ID or path
    - `package_name` (str): Optional. - Name of the package
    - `package_version` (str): Optional. - Version of the package
    - `file_name` (str): Optional. - Name of the package file to download

### Usage Instructions
1. Specify package_name/version/file_name.

### Examples
- Publish: `publish_repository_package` with project_id="123", package_name="mypkg", package_version="1.0".
- Download: Similar with file_name.

### Error Handling
- Version conflicts: Use unique versions.
