---
name: commit
description: Commit workflow for ai-standards repo. Formats all markdown files and previews changes before committing.
---

# Commit Workflow

Standard commit workflow for the ai-standards repository.

## Before Every Commit

### 1. Run Markdown Formatter

Format project markdown files using mdformat (excludes opensrc/ which contains external source):

```bash
nix develop -c mdformat skills/ .claude/ agents/ templates/ *.md
```

### 2. Preview Changes

Show files involved and diff preview:

```bash
git status
git diff --stat
git diff
```

### 3. Analyze and Group Changes

Review the changes and determine:

- **Single commit**: All changes are related to one feature/fix
- **Multiple commits**: Changes are unrelated and should be separate

Examples:

- Docs update + new skill → 2 commits
- Rename agent + update references → 1 commit
- Bug fix + unrelated refactor → 2 commits

### 4. Stage and Commit

For single commit:

```bash
git add -A
git commit -m "commit message"
```

For multiple commits, stage selectively:

```bash
git add <related-files>
git commit -m "first commit message"

git add <other-files>
git commit -m "second commit message"
```

## Commit Message Guidelines

- Start with uppercase, imperative mood
- Reference skill/agent names in brackets when applicable: `[powersync] Add sync pattern docs`
- If AI made the changes, include co-author:
  ```
  Co-Authored-By: Claude <noreply@anthropic.com>
  ```

## Output Format

Always show proposed commits with their files:

```
**Commit 1:** `commit message here`
- file1.md
- file2.ts

**Commit 2:** `another commit message`
- file3.md
```

Then wait for user approval before executing.
