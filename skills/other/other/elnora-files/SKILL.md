---
name: elnora-files
description: >
  This skill should be used when the user asks to "list files", "read a file",
  "get file content", "view protocol output", "file versions", "version history",
  "download protocol", "upload a file", "fork a file", "working copy",
  or any task involving Elnora Platform file management.
---

# Elnora Files

Manage files on the Elnora AI Platform. Files are protocol outputs, templates, datasets, and other artifacts attached to projects. The platform tracks version history for every file, supports working copies for edit-in-place workflows, and allows forking files across projects.

## Organization Context

All list, create, and upload tools accept an optional `org_id` parameter (UUID).
When provided, the operation targets that organization instead of the user's
active org. The user must be a member of the target org.

## Concepts

- **File**: A document stored in a project. Has metadata (name, type, size) and content.
- **Version**: An immutable snapshot of file content. Every change creates a new version.
- **Working copy**: A mutable draft of a file for editing. Commit to save changes as a new version.
- **Fork**: Copy a file to another project, preserving content but creating an independent copy.
- **Promote**: Change a file's visibility level (e.g., to organization library).
- **All IDs are UUIDs** (e.g., `bfdc6fbd-40ed-4042-9ea7-c79a5ec90085`).

## MCP Tools

### elnora_list_files

List files in a project or workspace.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `project_id` | uuid | No | - | Filter by project UUID |
| `page` | integer | No | 1 | Page number (min: 1) |
| `page_size` | integer | No | 25 | Results per page (min: 1, max: 100) |

Returns paginated results:

```json
{
  "items": [
    {
      "id": "<UUID>",
      "name": "pcr-protocol.md",
      "mimeType": "text/markdown",
      "size": 2048,
      "createdAt": "...",
      "updatedAt": "..."
    }
  ],
  "page": 1,
  "totalCount": 5,
  "hasNextPage": false
}
```

### elnora_get_file

Get file metadata (name, type, size, timestamps) without content.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file_id` | uuid | Yes | File UUID |

Use this to inspect a file before reading its content.

### elnora_get_file_content

Retrieve the full content of a file.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file_id` | uuid | Yes | File UUID |

Returns the raw file content. Use this to read protocol outputs, templates, or any file stored on the platform.

### elnora_create_file

Create a new empty file in a project.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_id` | uuid | Yes | Project UUID |
| `name` | string | Yes | Filename (min: 1, max: 255 chars) |
| `file_type` | string | No | File type / MIME type |
| `folder_id` | uuid | No | Folder UUID to place the file in |

Returns the created file object with its `id`. The file is created empty; use `elnora_create_version` to add content.

### elnora_upload_file

Upload a text file with content in a single call.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Filename (min: 1, max: 255 chars) |
| `content` | string | Yes | File content (min: 1, max: 100,000 chars) |
| `file_type` | string | No | MIME type (default: text/markdown) |

Use this for quick uploads when you have the content ready. For structured project placement, use `elnora_create_file` + `elnora_create_version` instead.

### elnora_update_file

Update file metadata (rename or move to a different folder).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file_id` | uuid | Yes | File UUID |
| `name` | string | No | New filename (min: 1, max: 255 chars) |
| `folder_id` | uuid | No | New folder UUID |

Must provide at least one of `name` or `folder_id`.

### elnora_archive_file

Archive (permanently delete) a file. **Destructive -- confirm with user first.**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file_id` | uuid | Yes | File UUID |

### elnora_download_file

Download a file (returns a download URL or content).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file_id` | uuid | Yes | File UUID |

## Version Management

### elnora_get_file_versions

Get version history for a file. Use this to track how a protocol evolved across iterations.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `file_id` | uuid | Yes | - | File UUID |
| `page` | integer | No | 1 | Page number (min: 1) |
| `page_size` | integer | No | 25 | Results per page (min: 1, max: 100) |

Returns paginated list of versions with timestamps and metadata.

### elnora_get_version_content

Get the content of a specific historical file version. Essential for comparing versions or reviewing past protocol iterations.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file_id` | uuid | Yes | File UUID |
| `version_id` | uuid | Yes | Version UUID |

Get version IDs from `elnora_get_file_versions` first.

### elnora_create_version

Create a new version of a file with updated content.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file_id` | uuid | Yes | File UUID |
| `content` | string | No | Version content (max: 100,000 chars) |

Each call creates a new immutable version. The file's current content becomes this version.

### elnora_restore_version

Restore a file to a specific previous version.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file_id` | uuid | Yes | File UUID |
| `version_id` | uuid | Yes | Version UUID to restore |

Get version IDs from `elnora_get_file_versions` first.

## Working Copies

Working copies let you edit a file in place before committing changes.

### elnora_create_working_copy

Create a mutable working copy of a file for editing.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file_id` | uuid | Yes | File UUID |
| `task_id` | uuid | No | Associated task UUID |

### elnora_commit_working_copy

Commit the working copy back to the file, saving changes as a new version.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file_id` | uuid | Yes | File UUID |

## Cross-Project Operations

### elnora_fork_file

Fork (copy) a file to another project. Creates an independent copy in the target project.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file_id` | uuid | Yes | Source file UUID |
| `target_project_id` | uuid | Yes | Target project UUID |

### elnora_promote_file

Change a file's visibility level (e.g., promote to organization library).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file_id` | uuid | Yes | File UUID |
| `visibility` | string | Yes | Target visibility level |

## Agent Workflow Recipes

### Read a protocol from a project

1. Call `elnora_list_files` with `project_id` to browse files
2. Call `elnora_get_file_content` with the target file's `id`

### Upload a protocol template

1. Call `elnora_upload_file` with `name` and `content`
2. Use the returned file `id` in `elnora_send_message` via `file_ids` to reference it in a task

### Track protocol evolution

1. Call `elnora_get_file_versions` to see all versions
2. Call `elnora_get_file_content` to read current content
3. Use `elnora_restore_version` if you need to revert

### Edit a file with working copies

1. Call `elnora_create_working_copy` with the file ID
2. Make edits (the working copy is mutable)
3. Call `elnora_commit_working_copy` to save changes as a new version

### Copy a file to another project

1. Get the source file ID from `elnora_list_files` or `elnora_search_files`
2. Get the target project ID from `elnora_list_projects`
3. Call `elnora_fork_file` with both IDs

### Reference a file in a task conversation

Use file IDs from `elnora_list_files` as `file_ids` in `elnora_send_message` or `context_file_ids` in `elnora_create_task` to give the AI context about existing protocols or datasets.

## Presigned URL Upload (Large/Binary Files)

For files too large for inline upload (>100KB) or binary files, use the two-step presigned URL flow:

### elnora_initiate_upload

Start a multi-step file upload. Returns a presigned URL for uploading content directly to storage.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `project_id` | uuid | Yes | Project UUID |
| `file_name` | string | Yes | Filename (min: 1, max: 255 chars) |
| `content_type` | string | No | MIME type (default: application/octet-stream) |
| `file_size_bytes` | integer | Yes | File size in bytes |

Returns a presigned URL and file ID. PUT the file content to the URL, then confirm.

### elnora_confirm_upload

Confirm that a file upload to the presigned URL has completed.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file_id` | uuid | Yes | File UUID from `elnora_initiate_upload` |

## Search Inside Files

### elnora_search_file_content

Full-text search inside file bodies. Finds content within protocols and documents, not just metadata.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | Yes | - | Search query (min: 1, max: 1,000 chars) |
| `page` | integer | No | 1 | Page number |
| `page_size` | integer | No | 25 | Results per page (max: 100) |

## Token Efficiency

All file tools support optional `compact` and `fields` parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `compact` | boolean | false | Strip null/empty values (~30-40% token savings) |
| `fields` | string | all | Comma-separated field names (e.g., "id,name") |
