---
name: file-manager
description: Reads, writes, and manages files and directories using a secure Python script.
version: 1.1.0
operations:
  read_file:
    side_effects: none
  write_file:
    side_effects: constructive
  delete_file:
    side_effects: destructive
    requires_human_approval: true

# File Manager Skill

## 1. Objective
To provide agents with the ability to persistent store and retrieve information in the filesystem safely.

## 2. Input
*   `operation`: 'read', 'write', 'list', 'exists'.
*   `path`: Relative path from project root.
*   `content`: (For write) String content.

## 3. Process
This skill delegates strict permissions to a Python script.

### Command Structure
```bash
python3 .agent/skills/file-manager/src/file_ops.py [operation] [path] "[content]"
```

### Operations
1.  **Read:** `read_file(path)`
    *   Example: `python3 ... read docs/intro.md`
2.  **Write:** `write_file(path, content)`
    *   Example: `python3 ... write docs/intro.md "# Hello"`
    *   *Note:* Automatically creates parent directories (`mkdir -p`).
3.  **List:** `list_directory(path)`
    *   Example: `python3 ... list src/`
4.  **Check:** `check_exists(path)`
    *   Example: `python3 ... exists config.json`

## 4. Output
JSON Object containing result or error.
```json
{
  "success": true,
  "content": "..."
}
```

## 5. Security
*   **Sandbox:** Operations are strictly limited to the Current Working Directory (CWD).
*   **Rejection:** Paths containing `../` that traverse outside CWD will raise a Security Error.
