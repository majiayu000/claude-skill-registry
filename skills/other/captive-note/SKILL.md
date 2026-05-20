---
name: captive-note
description: Write content to a Captive note (Today.md, Week.md, etc.) with validation and backup.
disable-model-invocation: true
allowed-tools: Read, Write, Bash
---

# Write Captive Note

This sub-skill writes content to a Captive note in the vault, with validation to prevent accidental data loss.

## Input Arguments

Arguments are passed as key-value pairs:
- `path`: Full path to the note (e.g., `{{VAULT}}/00_Brain/Captive/Today.md`)
- `content`: Markdown content to write

## Instructions

### 1. Validate Path

Verify the path is within the Captive directory:

```
$VAULT/00_Brain/Captive/
```

If path is outside Captive, return error:
```
Error: Path must be within Captive directory. Got: {path}
```

### 2. Check Existing Content

If the file already exists:

1. Read current content
2. If content is non-empty and different from new content:
   - Create a backup at `{filename}.backup.md` in the same directory
   - Log: "Backed up existing content to {backup_path}"

### 3. Write Content

Write the new content to the specified path.

### 4. Verify Write

Read back the file to confirm write succeeded.

## Output

Return structured JSON:

```json
{
  "success": true,
  "path": "/Users/.../00_Brain/Captive/Today.md",
  "backup_created": true,
  "backup_path": "/Users/.../00_Brain/Captive/Today.backup.md",
  "bytes_written": 2048
}
```

Or on error:

```json
{
  "success": false,
  "error": "Description of what went wrong",
  "path": "/Users/.../00_Brain/Captive/Today.md"
}
```

## Error Cases

| Condition | Error Message |
|-----------|---------------|
| Path outside Captive | "Path must be within Captive directory" |
| Vault not found | "Vault directory does not exist: {vault}" |
| Write failed | "Failed to write file: {system_error}" |
| Verification failed | "Write verification failed: content mismatch" |

## Safety

- Always validate path is within Captive before writing
- Always backup existing non-empty content before overwriting
- Never write to Periodic or Semantic directories (use archive sub-skills for those)
