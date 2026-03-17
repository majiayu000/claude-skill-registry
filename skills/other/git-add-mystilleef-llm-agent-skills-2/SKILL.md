---
name: git-add
description:
  Autonomously select files to stage for an atomic Git commit. Use when
  the agent wants to stage selected files for a git commit. Only stages
  selected files, but does not commit them.
---

# Agent protocol: Stage atomic git changes

**Goal:** Stage a single, cohesive set of related file changes for an
atomic commit.

**When:** Use when the agent wants to stage selected files for a git
commit.

**`NOTE`:** _Use this skill only for staging selected files, but not
committing them._

## Primary directives

- Study `references/` files `ONLY` if more than one file exists to
  stage.

- **`NEVER`** use `git add .` or `git add -A`.
- **`NEVER`** use `git checkout` or `git restore`.
- Assume a file in both `staged` and `unstaged` states needs staging.
- Stage files explicitly: `git add <file1> <file2> ...`.
- Leave unrelated changes `unstaged`.
- Isolate `.gitignore` changes; stage them in a separate commit.
- Except for `.gitignore`, **`DON'T`** edit any files

## Git directives

Git commands (use `--no-pager` and `--no-ext-diff` for diffs):

### For `unstaged` changes

```bash
git --no-pager diff --no-ext-diff --stat --minimal --patience --histogram \
    --find-renames --summary --no-color -U10 <file_group>
```

### For staged changes

```bash
git --no-pager diff --staged --no-ext-diff --stat --minimal --patience \
    --histogram --find-renames --summary --no-color -U10
```

### For repository status

```bash
git status --porcelain=v2 --branch
```

### For staging files

```bash
git add <file1> <file2> ...
```

## Efficiency directives

- Optimize all operations for token and context efficiency
- Single-file shortcut: If one tracked `unstaged` file, stage
  immediately (skip reference study)
- Batch git operations on file groups, avoid individual file processing
- Use parallel execution when possible
- Analyze tracked files via `git diff`; read non-ignored `untracked`
  files; omit ignored files
- Reduce token usage

---

## Workflow

**Exception:** If exactly one tracked `unstaged` file exists, stage it
immediately and skip steps below.

1. Study references files
2. Review repository status to identify all modified/new/`untracked`
   files
3. Update `.gitignore` following reference guidelines
4. Select smallest group of `unstaged` files forming single logical
   change
5. Stage the atomic group
6. Output status as first line, then bullet list of staged files

## Output

**Files modified:**

- Staging area - Files added to git staging area

**Status communication:**

First line of output indicates status:

- `SUCCESS: staged N files for atomic commit` - Files staged
  successfully
- `WARN: no files available to stage` - No `unstaged` changes found
- `ERROR: [message]` - Failed to stage files

**Following lines (when SUCCESS):** bullet point list of staged files
