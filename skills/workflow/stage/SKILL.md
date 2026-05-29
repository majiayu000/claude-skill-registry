---
name: stage
description: Smart staging with auto-detected file blocks and interactive override. Use before /commit.
---

# Smart Stage

Stage files for commit using auto-detected logical blocks. The user picks which blocks to stage via interactive selection.

## Workflow

```
/stage -> /commit
```

## Step 1: Scan unstaged/untracked files

Run `git status` (never use `-uall` flag) to get the full picture of modified, deleted, and untracked files.

If there are no unstaged or untracked changes, inform the user and stop.

## Step 2: Auto-detect file blocks

Group related files into logical blocks based on these rules (applied in order of priority):

### The Commit Trio rule

Any block that contains a `.py` file under `swanki/` or `tests/` MUST also include:

1. The paired dendron note (`notes/<dendron-path>.md`) -- if it exists in the changed file list
2. The paired test file (`tests/.../<test_file>.py`) or source file -- if it exists in the changed file list
3. The current weekly note (`notes/user.mjvolk3.swanki.tasks.weekly.*.md`) -- always pulled into any block containing Python files

The weekly note appears in the FIRST Python block only (not duplicated across blocks). This enforces the project's atomic commit rule: source + note + weekly travel together.

### Block detection rules (in priority order)

1. **Python trio**: a `.py` source file + its `notes/<dendron-path>.md` + its `tests/` counterpart + the weekly note. Multiple related `.py` files in the same package can be grouped into one block (e.g., all files under `swanki/processing/`).
2. **Skill bundles**: all files under a `.claude/skills/<name>/` directory grouped together
3. **Config clusters**: related config files (e.g., `.pre-commit-config.yaml` + `pyproject.toml` when both have lint-related changes)
4. **Shell scripts + notes**: `.sh` files paired with their `notes/scripts.<name>.md` counterpart
5. **Standalone notes**: `notes/*.md` files not already paired with Python or shell files
6. **Other files**: anything not covered above (configs, docs, etc.)

A file should only appear in one block. If a file could fit multiple blocks, use the highest-priority rule.

## Step 3: Present blocks to user

Display numbered blocks with file lists. Mark the weekly note explicitly so the user sees it:

```
Detected file blocks:
[1] Processing package (4 files):
    swanki/processing/pdf_processor.py
    swanki/processing/image_processor.py
    notes/swanki.processing.pdf_processor.md
    notes/user.mjvolk3.swanki.tasks.weekly.2026.08.md  (weekly)
[2] Scripts: scripts/dendron-tree.sh
[3] Standalone notes: notes/scratch.2026.02.11.*.md (3 files)
```

## Step 4: User picks blocks

Use `AskUserQuestion` with `multiSelect: true` to let the user choose which blocks to stage. Options:

- Each detected block as a selectable option
- "All" to stage everything

## Step 5: Pre-stage reminders

Print reminders as informational text (not blocking):

- If selected files include `.py` under `swanki/` or `tests/`: "Python files detected. Consider running `/update-py-notes` and `/ruff` first."

## Step 6: Stage selected blocks

- Run `git add <files>` for chosen blocks (explicit file paths, never `git add -A` or `git add .`)
- Use `git rm` for deleted files
- Never stage `.env`, credentials, or secrets -- warn the user if detected

## Step 7: Confirm

Run `git diff --cached --name-status` to show what is now staged.

## Important Rules

- NEVER run `git add -A` or `git add .`
- NEVER stage `.env`, credentials, secrets, or similar sensitive files -- warn the user
- Use `git rm` for deleted files
- The user's tool approval prompt is the gate -- do NOT ask extra confirmation questions
- A file appears in exactly one block
- Do NOT ask extra approval questions -- tool approval prompts are the gates
- The weekly note is always included with the first Python block -- never staged alone as a separate block when Python files are present

## Example Invocations

- `/stage` -- interactive staging of all changes
- "stage my changes"
- "stage files for commit"
