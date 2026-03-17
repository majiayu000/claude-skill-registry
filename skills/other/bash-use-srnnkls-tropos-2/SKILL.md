---
name: bash-use
description: Ultra-concise bash command patterns. Use when constructing shell commands or one-liners.
---

# Bash Use Skill

Patterns for interactive bash commands, one-liners, and CLI usage.

---

## When to Use

- Constructing shell commands
- Writing one-liners
- Interactive CLI usage
- Command debugging or improvement

---

## Quick Reference

**Quote paths with spaces:**
```bash
cd "/path with spaces/dir"
```

**Relative paths with rm:**
```bash
rm -rf ./build  # Not $HOME/...
```

**Chain commands:**
```bash
cmd1 && cmd2 && cmd3  # Stop on failure
cmd1; cmd2; cmd3      # Continue regardless
```

**Command substitution:**
```bash
result=$(command)  # Not `command`
```

**Check command exists:**
```bash
command -v jq &>/dev/null || echo "not found"
```

**Output redirection:**
```bash
command 2>&1        # Stderr to stdout
command &>/dev/null # Suppress all
```

**Process substitution:**
```bash
diff <(cmd1) <(cmd2)
```

---

## Full Guidelines

**Read:** `~/.claude/skills/code-implement/resources/loqui/languages/bash/reference/commands.md`

Use Read tool to access (paths outside cwd require direct reads).

---

## Anti-Patterns Checklist

- ✘ Unquoted paths with spaces
- ✘ Absolute paths with `rm`
- ✘ Using `;` when `&&` is needed
- ✘ Backticks instead of `$()`

---

## Related Skills

- **code-implement**: Language-specific patterns (includes bash)
- **code-test**: TDD workflow
