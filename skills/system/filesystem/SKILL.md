---
name: filesystem
description: File system operations guidance - read, write, search, and manage files using Claude Code's built-in tools.
version: 1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Glob, Grep]
best_practices:
  - Use Read for file contents
  - Use Glob for file pattern matching
  - Use Grep for content searching
  - Use Edit for modifications
error_handling: graceful
streaming: supported
---

# Filesystem Skill

<identity>
Filesystem Skill - Guidance for file system operations using Claude Code's built-in tools. Read, write, search, and manage files efficiently.
</identity>

<capabilities>
- Reading single or multiple files
- Creating or modifying files
- Searching for files by pattern
- Searching file contents
- Directory navigation
</capabilities>

<instructions>
<execution_process>

## Claude Code Built-in Tools

### Reading Files

**Read Tool**: Read file contents

```
Read file_path="/path/to/file.txt"
```

Options:

- `offset`: Start line (for large files)
- `limit`: Number of lines to read

### Finding Files

**Glob Tool**: Find files by pattern

```
Glob pattern="**/*.ts"
```

Common patterns:

- `**/*.ts` - All TypeScript files
- `src/**/*.tsx` - React components in src
- `**/test*.js` - Test files anywhere

### Searching Content

**Grep Tool**: Search file contents

```
Grep pattern="function myFunc" path="/src"
```

Options:

- `output_mode`: "content", "files_with_matches", or "count"
- `-A`, `-B`, `-C`: Context lines

### Writing Files

**Write Tool**: Create or overwrite files

```
Write file_path="/path/to/file.txt" content="..."
```

**Edit Tool**: Modify existing files

```
Edit file_path="/path/to/file.txt" old_string="..." new_string="..."
```

### Directory Operations

**Bash Tool**: For directory operations

```bash
# List directory
ls -la /path/to/dir

# Create directory
mkdir -p /path/to/new/dir

# Move/rename
mv /old/path /new/path
```

</execution_process>

<best_practices>

## Common Workflows

### Reading Multiple Files

```
# Read files in parallel (multiple Read calls in one message)
Read file_path="/src/app.ts"
Read file_path="/src/config.ts"
Read file_path="/src/utils.ts"
```

### Search and Read

```
# 1. Find files
Glob pattern="**/*.config.ts"

# 2. Read matching files
Read file_path="/path/from/glob/result"
```

### Find and Replace

```
# 1. Search for pattern
Grep pattern="oldFunction" path="/src"

# 2. Edit each file
Edit file_path="/src/file.ts" old_string="oldFunction" new_string="newFunction"
```

## Best Practices

1. **Read Before Edit**: Always read a file before editing it
2. **Use Glob Over Bash**: Prefer Glob to `find` for file discovery
3. **Use Grep Over Bash**: Prefer Grep to `grep` for searching
4. **Parallel Reads**: Read multiple files in one message for speed
5. **Verify Changes**: Read file after editing to verify

</best_practices>
</instructions>

<examples>
<usage_example>
**Find and read all TypeScript files**:

```
Glob pattern="src/**/*.ts"
# Then read the results
Read file_path="/src/app.ts"
```

</usage_example>

<usage_example>
**Search for a function and edit it**:

```
Grep pattern="export function oldName" path="/src"
# Found in /src/utils.ts:23

Edit file_path="/src/utils.ts" old_string="export function oldName" new_string="export function newName"
```

</usage_example>
</examples>

## Rules

- Always read files before editing
- Use built-in tools (Read, Glob, Grep) instead of bash equivalents
- Verify changes after editing

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
