---
name: bash-tools
description: Proper usage of Bash and file operation tools. Use this skill when executing shell commands, writing files, or when tempted to use echo/cat/heredoc to pipe content to files. Prevents permission circumvention patterns like piping multiline content through echo instead of using Write tool. Covers Bash tool, Write tool, Edit tool, and Read tool best practices.
---

# Bash Tools

Guidelines for proper tool selection when executing commands or modifying files.

## Core Principle

**Use specialized file tools for file operations. Use Bash only for actual shell commands.**

Never use Bash to circumvent file operation permissions. If Write tool is blocked, that's intentional - do not work around it with `echo`, `cat`, or heredocs.

## Tool Selection Decision Tree

```
Need to create/overwrite a file?
├── YES → Use Write tool (NOT echo/cat/heredoc)
└── NO → Continue...

Need to edit part of a file?
├── YES → Use Edit tool (NOT sed/awk)
└── NO → Continue...

Need to read file contents?
├── YES → Use Read tool (NOT cat/head/tail)
└── NO → Continue...

Need to search file contents?
├── YES → Use Grep tool (NOT grep/rg in Bash)
└── NO → Continue...

Need to find files by pattern?
├── YES → Use Glob tool (NOT find/ls in Bash)
└── NO → Continue...

Is this an actual shell command? (git, npm, docker, make, etc.)
├── YES → Use Bash tool
└── NO → Reconsider - probably need a file tool
```

## Prohibited Patterns

These patterns attempt to circumvent Write tool permissions and MUST NOT be used:

| Pattern | Why It's Wrong | Correct Approach |
|---------|---------------|------------------|
| `echo "content" > file.py` | Bypasses Write permissions | Use Write tool |
| `cat << 'EOF' > file.py` | Heredoc bypasses permissions | Use Write tool |
| `printf '%s' "$content" > file` | Same as echo bypass | Use Write tool |
| `tee file.py <<< "content"` | Redirect bypass | Use Write tool |

See [references/permission-patterns.md](references/permission-patterns.md) for comprehensive examples.

## Tool References

- [Write Tool](references/write-tool.md) - Creating and overwriting files
- [Bash Tool](references/bash-tool.md) - Running shell commands
- [Edit Tool](references/edit-tool.md) - Modifying existing files
- [Read Tool](references/read-tool.md) - Reading file contents

## When Write Tool is Blocked

If the Write tool is blocked for a file:

1. **Accept the block** - It exists for a reason
2. **Ask the user** if they want to allow the operation
3. **Do NOT** attempt to use Bash to write the file instead

The permission system protects the user. Circumventing it defeats its purpose.

## Updating This Skill

When encountering new permission circumvention patterns or tool usage issues, see [references/updating-skill.md](references/updating-skill.md).

## Quick Reference

| Task | Tool | NOT This |
|------|------|----------|
| Create file | Write | `echo > file` |
| Edit file | Edit | `sed -i` |
| Read file | Read | `cat file` |
| Search content | Grep | `grep pattern` |
| Find files | Glob | `find . -name` |
| Git commands | Bash | - |
| npm/yarn | Bash | - |
| docker/make | Bash | - |
| Run tests | Bash | - |
