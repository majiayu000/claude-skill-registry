---
name: commit
description: Stage and commit vault changes with UK English conventional commit messages
disable-model-invocation: true
tools: Bash
---

# Commit Vault Changes

Stage and commit changes to the vault with properly formatted UK English conventional commit messages.

## Usage

```
/commit                    # Auto-detect changes and commit
/commit -m "message"       # Commit with a specific message
/commit --amend            # Amend the previous commit (use sparingly)
```

## Workflow

### 1. Review Changes

```bash
git status
git diff --stat
```

### 2. Stage Changes

Stage specific files rather than using `git add -A`:

- **Never stage**: `.env`, credentials, `.secrets.baseline` (unless updated by detect-secrets)
- **Use `git add -u`** for modified/deleted files with Unicode filenames (avoids octal encoding issues)
- **Use `git lfs track`** first for large binary files (PPTX, PDF >100MB)

### 3. Compose Commit Message

Follow these conventions:

- **UK English** spelling (e.g., "organise", "summarise", "colour")
- **Imperative mood** in subject line (e.g., "Add meeting note" not "Added meeting note")
- **Subject line** under 72 characters
- **Body** explains the "why" not the "what" (the diff shows the what)
- **Always include** the co-author tag

### 4. Commit Format

```
<type>: <subject>

<optional body>

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

**Types:**

| Type       | When to Use                                    |
| ---------- | ---------------------------------------------- |
| `Add`      | New notes, skills, scripts, templates          |
| `Update`   | Enhancements to existing notes or config       |
| `Fix`      | Bug fixes, broken links, frontmatter errors    |
| `Refactor` | Restructuring without changing meaning         |
| `Archive`  | Moving notes to Archive/                       |
| `Remove`   | Deleting deprecated content                    |
| `Docs`     | Documentation-only changes (CLAUDE.md, READMEs)|

### 5. Pre-commit Checks

The vault has pre-commit hooks that may:
- Run `detect-secrets` (may need `.secrets.baseline` update)
- Check for large files (use git LFS for >100MB)
- Fix trailing whitespace and EOF

If the hook modifies files, re-stage with `git add -u` then commit again.

### 6. Post-commit

Run `git status` to verify the commit succeeded and working tree is clean.

## Important

- **Never force push** to main without explicit user confirmation
- **Never use `--no-verify`** unless the user explicitly requests it
- If `git commit` fails with `PermissionError` on `~/.cache/pre-commit/`, use `dangerouslyDisableSandbox: true`
