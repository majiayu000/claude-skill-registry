---
name: tools-json-ops
description: Generic JSON file CRUD operations with path notation support
user-invocable: false
allowed-tools: Read, Write, Edit, Bash
---

# JSON File Operations Skill

Generic JSON file operations with JSON path notation support for field-level access.

## What This Skill Provides

- Read, write, and update any JSON file
- Field-level access using JSON path notation
- Array and object manipulation
- Atomic writes with validation
- Works with any JSON file (including configuration directories)

## When to Activate This Skill

Activate this skill when:
- Reading or writing JSON files
- Performing structured updates to JSON content
- Accessing specific fields within JSON files
- Adding or removing entries from JSON arrays/objects

---

## Workflow: JSON File Operations

**Pattern**: Command Chain Execution

Perform read, write, and update operations on JSON files.

### Parameters

- **file_path** (required): Path to JSON file
- **operation** (required): One of `read`, `read-field`, `write`, `update-field`, `add-entry`, `remove-entry`
- **field** (optional): JSON path for field operations (e.g., `parent.child.field`)
- **value** (optional): Value for write/update operations (JSON string)

### Step 1: Execute Operation

```bash
python3 .plan/execute-script.py plan-marshall:tools-json-ops:{operation} {file_path} [--field {field}] [--value '{value}']
```

### Step 2: Process Result

Parse JSON output:
- `success: true` - Return result value
- `success: false` - Report error message

### Operations Reference

| Operation | Description | Required Params |
|-----------|-------------|-----------------|
| `read` | Read entire file | file_path |
| `read-field` | Read specific field | file_path, field |
| `write` | Write entire content | file_path, value |
| `update-field` | Update specific field | file_path, field, value |
| `add-entry` | Add to array/object | file_path, field, value |
| `remove-entry` | Remove from array/object | file_path, field, value |

### Example Usage

```bash
# Read entire file
python3 .plan/execute-script.py plan-marshall:tools-json-ops:manage-json-file read config.json

# Read specific field
python3 .plan/execute-script.py plan-marshall:tools-json-ops:manage-json-file read-field config.json --field "database.host"

# Update field
python3 .plan/execute-script.py plan-marshall:tools-json-ops:manage-json-file update-field config.json --field "database.port" --value '5432'

# Add to array
python3 .plan/execute-script.py plan-marshall:tools-json-ops:manage-json-file add-entry config.json --field "servers" --value '"new-server"'

# Remove from array
python3 .plan/execute-script.py plan-marshall:tools-json-ops:manage-json-file remove-entry config.json --field "servers" --value '"old-server"'
```

---

## JSON Path Notation

Use dot notation for JSON paths:

| Path | Description |
|------|-------------|
| `field` | Top-level field |
| `parent.child` | Nested object |
| `parent.child.grandchild` | Deep nested field |
| `array[0]` | First array element |
| `array[-1]` | Last array element |

### Special Characters

- Use quotes for keys with special characters: `parent."my-key".field`
- Array indices use bracket notation: `[0]`, `[-1]`

---

## Scripts

| Script | Notation |
|--------|----------|
| manage-json-file | `plan-marshall:tools-json-ops` |

Script characteristics:
- Uses Python stdlib only (json, argparse, pathlib)
- Outputs JSON to stdout
- Exit code 0 for success, 1 for errors
- Supports `--help` flag

---

## Integration Points

### With Scripts Library
- Scripts are discovered via scripts-library.toon
- Use portable notation from Scripts table above

### With manage-memories Skill
- Provides low-level JSON operations used by memory layer

### With manage-run-configuration Skill
- Provides low-level JSON operations for run configuration
