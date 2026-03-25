---
name: commit
description: Generate conventional commit messages from staged changes and commit
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

## If nothing is staged

Run `git status` and tell the user what files are available to stage.

<!-- Skill by Huzefa Nalkheda Wala | github.com/huzaifa525 | claude-code-optimizer -->
