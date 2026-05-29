---
name: toolfs-filesystem
description: Access files and directories from mounted local filesystems. Use this skill when the user requests file operations such as "Read this file", "Write to that file", "List directory contents", or "Check if file exists".
metadata:
  author: toolfs
  version: "1.0.0"
  module: filesystem
---

# ToolFS Filesystem

Access files and directories from mounted local filesystems. Provides read, write, and list operations with session-based access control and audit logging.

## How It Works

1. **Mount Points**: Local directories are mounted to virtual paths under `/toolfs/<mount_point>`
2. **Path Resolution**: Virtual paths are resolved to actual local filesystem paths
3. **Permission Control**: Access is controlled by session permissions and mount read-only settings
4. **Audit Logging**: All operations are logged for security and debugging

## Usage

### Read File

**ToolFS Path:**
```
/toolfs/<mount_point>/<relative_path>
```

**Example:**
```json
GET /toolfs/data/project/config.json

// Response (file content)
{
  "version": "1.0.0",
  "settings": {
    "debug": true,
    "log_level": "info"
  }
}
```

### Write File

**ToolFS Path:**
```
/toolfs/<mount_point>/<relative_path>
```

**Example:**
```json
PUT /toolfs/data/project/output.txt
Content-Type: text/plain

Processing completed successfully.
Generated 42 files.
Total size: 1024 KB

// Response
{
  "success": true,
  "bytes_written": 65
}
```

**Note**: Write operations require write permissions on the mount and will fail on read-only mounts.

### List Directory

**ToolFS Path:**
```
/toolfs/<mount_point>/<relative_path>
```

**Example:**
```json
LIST /toolfs/data/project/

// Response
[
  "config.json",
  "output.txt",
  "src/",
  "docs/"
]
```

Directories are indicated with a trailing `/`.

### Check File Status (Stat)

**ToolFS Path:**
```
STAT /toolfs/<mount_point>/<relative_path>
```

**Example:**
```json
STAT /toolfs/data/project/config.json

// Response
{
  "path": "/toolfs/data/project/config.json",
  "size": 256,
  "is_dir": false,
  "mod_time": "2024-01-15T12:00:00Z"
}
```

## When to Use This Skill

Use Filesystem skill when you need to:

- **Read Files**: Access configuration files, data files, or documents
- **Write Files**: Save outputs, logs, or generated content
- **List Directories**: Browse directory structures
- **Check Existence**: Verify files or directories exist
- **File Operations**: Perform standard filesystem operations

Common use cases:
- "Read the config file from the project directory"
- "Write the output to a file"
- "List all files in the src directory"
- "Check if settings.json exists"

## Mount Points

Mount points are created when local directories are mounted to ToolFS:

```go
// Mount a local directory
fs.MountLocal("/project_data", true)  // Read-only mount
fs.MountLocal("/workspace", false)    // Read-write mount
```

Access paths:
- `/toolfs/project_data/` → mounted local directory
- `/toolfs/workspace/` → mounted local directory

## Path Resolution

- **Virtual Path**: `/toolfs/<mount_point>/path/to/file.txt`
- **Resolved Path**: `<local_mount_directory>/path/to/file.txt`

## Output Format

Filesystem operations return standardized result structures:

```json
{
  "type": "file",
  "source": "/toolfs/<mount_point>/<path>",
  "content": "file content or directory listing",
  "metadata": {
    "size": 1024,
    "is_dir": false,
    "mod_time": "..."
  },
  "success": true,
  "error": "error message if failed"
}
```

## Present Results to User

When presenting filesystem results:

```
✓ File read successfully

Path: /toolfs/data/project/config.json
Size: 256 bytes
Modified: 2024-01-15T12:00:00Z

Content:
{
  "version": "1.0.0",
  "settings": {
    "debug": true,
    "log_level": "info"
  }
}
```

```
✓ File written successfully

Path: /toolfs/data/project/output.txt
Bytes written: 65
```

```
✓ Directory listing

Path: /toolfs/data/project/
Items: 4

config.json
output.txt
src/
docs/
```

## Troubleshooting

### Access Denied Error

If you get an `access_denied` error:

1. Verify the session has access to the requested path
2. Check if the mount point exists
3. Ensure write permissions if performing write operations
4. Verify the mount is not read-only (for writes)

### File Not Found

If a file operation fails:

1. Verify the path is correct
2. Check if the file or directory exists
3. Ensure the mount point is properly configured
4. Verify relative path is correct from mount root

### Read-Only Mount

If write operations fail on a read-only mount:

1. Check mount configuration (read-only vs read-write)
2. Create a read-write mount for write operations
3. Use a different mount point with write permissions

## Best Practices

1. **Use Appropriate Mounts**: Use read-only mounts for safety, read-write only when needed
2. **Path Validation**: Always validate paths before operations
3. **Error Handling**: Check file existence before read/write operations
4. **Session Isolation**: Each session has independent access control
5. **Audit Logs**: Review audit logs for security and debugging

---

*This skill is part of ToolFS. See [main SKILL.md](../SKILL.md) for overview.*

