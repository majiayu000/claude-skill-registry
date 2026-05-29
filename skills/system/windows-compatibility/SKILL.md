---
name: windows-compatibility
description: Guidelines for working on Windows with Git Bash. Use bash/POSIX syntax for shell commands, not CMD or PowerShell syntax, since the Bash tool runs through Git Bash.
version: 2.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash]
globs: '**/*'
best_practices:
  - Always use bash syntax for Bash tool commands
  - Use cross-platform Node.js APIs when possible
  - Test file path handling for Windows backslashes
error_handling: graceful
streaming: supported
---

# Windows Compatibility Skill

<identity>
You are an expert at writing cross-platform code that works correctly on Windows systems running Git Bash.
</identity>

## Critical Rule: Bash Tool Uses Git Bash

**The Bash tool runs commands through Git Bash (`/usr/bin/bash`), NOT Windows CMD or PowerShell.**

This means:

- Use **bash/POSIX syntax** for all shell commands
- Do NOT use Windows CMD syntax (`if not exist`, `copy`, `del`)
- Do NOT use PowerShell syntax (`Remove-Item`, `New-Item`)

## Command Syntax Reference

### Directory Operations

| Task             | ✅ Correct (Bash)      | ❌ Wrong (CMD)      | ❌ Wrong (PowerShell)          |
| ---------------- | ---------------------- | ------------------- | ------------------------------ |
| Create directory | `mkdir -p path/to/dir` | `mkdir path\to\dir` | `New-Item -ItemType Directory` |
| Check if exists  | `[ -d "path" ] && ...` | `if exist path ...` | `Test-Path path`               |
| Remove directory | `rm -rf path/to/dir`   | `rmdir /s /q path`  | `Remove-Item -Recurse`         |
| List files       | `ls -la`               | `dir`               | `Get-ChildItem`                |

### File Operations

| Task              | ✅ Correct (Bash)                        | ❌ Wrong (CMD)     | ❌ Wrong (PowerShell) |
| ----------------- | ---------------------------------------- | ------------------ | --------------------- |
| Create empty file | `touch file.txt` or `echo "" > file.txt` | `echo. > file.txt` | `New-Item file.txt`   |
| Copy file         | `cp src dest`                            | `copy src dest`    | `Copy-Item`           |
| Move file         | `mv src dest`                            | `move src dest`    | `Move-Item`           |
| Delete file       | `rm file.txt`                            | `del file.txt`     | `Remove-Item`         |
| Read file         | `cat file.txt`                           | `type file.txt`    | `Get-Content`         |

### Conditional Operations

| Task                   | ✅ Correct (Bash)                | ❌ Wrong (CMD)               |
| ---------------------- | -------------------------------- | ---------------------------- |
| If directory exists    | `[ -d "path" ] && echo "exists"` | `if exist path\ echo exists` |
| If file exists         | `[ -f "file" ] && echo "exists"` | `if exist file echo exists`  |
| Multi-line conditional | `if [ condition ]; then ... fi`  | `if condition ( ... )`       |

### Path Handling

- Use **forward slashes** in bash: `.claude/context/memory/`
- Git Bash auto-converts Windows paths, but prefer forward slashes
- Quote paths with spaces: `"path with spaces/file.txt"`

## Common Mistakes to Avoid

### ❌ Windows CMD Multi-line If

```batch
# WRONG - Git Bash cannot parse this
if not exist "path" mkdir "path"
if not exist "other" mkdir "other"
```

### ✅ Bash Equivalent

```bash
# CORRECT - Use bash syntax
mkdir -p path other
# Or with explicit check:
[ -d "path" ] || mkdir -p path
```

### ❌ Touch Command Failure Handling

```bash
# WRONG - touch may not exist on Windows, fails silently
touch file.txt 2>/dev/null
```

### ✅ Portable Alternative

```bash
# CORRECT - echo works everywhere in bash
echo "" > file.txt
# Or use mkdir -p for directories (never fails if exists)
mkdir -p path/to/dir
```

## Node.js Cross-Platform Tips

When writing JavaScript/Node.js code:

```javascript
// Use path.join() for cross-platform paths
const filePath = path.join(__dirname, 'subdir', 'file.txt');

// Use fs.mkdir with recursive option
fs.mkdirSync(dirPath, { recursive: true });

// Check platform if needed
if (process.platform === 'win32') {
  // Windows-specific handling
}
```

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:** Record any new patterns or exceptions discovered.

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
