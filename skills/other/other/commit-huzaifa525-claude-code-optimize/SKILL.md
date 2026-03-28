---
name: commit
description: Use when the user wants to commit changes, save work, or create a git commit message.
disable-model-invocation: true
allowed-tools: Bash
---

Generate a commit message and commit staged changes.

## Steps

1. **Check staged changes**
   ```
   git diff --cached --stat
   git diff --cached
   ```

2. **Check recent commit style**
   ```
   git log --oneline -10
   ```

3. **Generate commit message** following Conventional Commits:

   | Prefix | When to Use |
   |--------|------------|
   | `feat:` | New feature |
   | `fix:` | Bug fix |
   | `refactor:` | Code restructure, no behavior change |
   | `docs:` | Documentation only |
   | `test:` | Adding or fixing tests |
   | `chore:` | Build, deps, config changes |
   | `perf:` | Performance improvement |
   | `style:` | Formatting, whitespace |
   | `ci:` | CI/CD changes |

4. **Format rules**
   - Subject line: max 72 characters, imperative mood ("Add" not "Added")
   - Body: wrap at 80 characters, explain WHY not WHAT
   - If multiple changes: use bullet points in body

5. **Commit**
   ```
   git commit -m "type: short description

   - Detail 1
   - Detail 2"
   ```

6. **Show result**
   ```
   git log --oneline -1
   ```

## Pre-Delivery Checklist

Before committing, verify:

- [ ] `git diff --cached` was read (not just `--stat`)
- [ ] Commit prefix matches the change type (feat/fix/refactor/etc.)
- [ ] Subject line is under 72 characters
- [ ] Subject uses imperative mood ("Add" not "Added")
- [ ] No sensitive files staged (.env, credentials, keys)
- [ ] No unrelated changes bundled in the same commit
- [ ] Body explains WHY if the change is non-obvious

## If nothing is staged

Run `git status` and tell the user what files are available to stage.

<!-- Skill by Huzefa Nalkheda Wala | github.com/huzaifa525 | claude-code-optimizer -->
