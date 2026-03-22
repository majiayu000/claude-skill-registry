---
name: elnora-folders
description: >
  Use this skill when the user asks about "Elnora folders", "project folders",
  "organize files", "move folder", "create folder", "rename folder",
  "delete folder", or any task involving folder management within Elnora projects.
---

# Elnora Folders

Manage folders within Elnora projects via MCP tools. Folders organize files
hierarchically inside a project.

## Organization Context

All folder tools accept an optional `org_id` parameter (UUID). When provided,
the operation targets that organization instead of the user's active org. The
user must be a member of the target org.

## Core Concepts

- **Folders** exist within a project and organize files into a hierarchy.
- Folders can be nested — a folder can have a **parent folder**.
- Moving a folder to root means setting no parent.
- **Deleting a folder is destructive** — always confirm with the user before proceeding.

## Tools Reference

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `elnora_list_folders` | List folders in a project | `project_id` |
| `elnora_create_folder` | Create a new folder | `project_id`, `name`, optional `parent_id` |
| `elnora_rename_folder` | Rename a folder | `project_id`, `folder_id`, `name` |
| `elnora_move_folder` | Move a folder to a new parent | `project_id`, `folder_id`, optional `parent_id` |
| `elnora_delete_folder` | Delete a folder | `project_id`, `folder_id` |

### Parameter Details

- **`project_id`** (required): The UUID of the project containing the folders.
- **`folder_id`** (required for rename/move/delete): The UUID of the target folder.
- **`parent_id`** (optional): The UUID of the parent folder. Omit to place at root level.
- **`name`** (required for create/rename): The folder name.

## Common Workflows

### Browse project folder structure

1. `elnora_list_folders` with `project_id` to see all folders and their hierarchy

### Create a nested folder

1. `elnora_list_folders` to find the parent folder's ID
2. `elnora_create_folder` with `project_id`, `name`, and `parent_id`

### Move a folder to root

1. `elnora_move_folder` with `project_id` and `folder_id`, omitting `parent_id`

### Reorganize folders

1. `elnora_list_folders` to see current structure
2. `elnora_move_folder` to relocate folders as needed
3. `elnora_rename_folder` to update names if required

### Delete a folder

1. **Confirm with the user first** — deletion is destructive
2. `elnora_delete_folder` with `project_id` and `folder_id`

## ID Format

All IDs are UUIDs (e.g., `bfdc6fbd-40ed-4042-9ea7-c79a5ec90085`).
