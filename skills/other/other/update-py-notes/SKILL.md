---
name: update-py-notes
description: Update dendron module notes for changed Python files. Checks staged files first, then falls back to modified (unstaged) files. Appends dated sections and stages updated notes. Run before /update-tasks-weekly and /commit.
---

# Update Python Notes

Update dendron module notes for Python files that have changed. Module notes are staged when done. Use `/update-tasks-weekly` separately to update the weekly note.

## Workflow

```
(edit python) -> /update-py-notes -> /update-tasks-weekly -> /commit
```

## Arguments

This skill accepts **optional file path arguments**. Behavior depends on whether arguments are provided:

- **With arguments** (e.g., `/update-py-notes swanki/config.py`): update only the specified files. Uses `git diff HEAD -- <file>` to get the diff (covers both staged and unstaged changes). If a file has no diff against HEAD (e.g., new untracked file), read the full file content instead.
- **No arguments**: auto-discover changed `.py` files (see Step 1 for the staged-then-modified fallback).

If no files are found (no args, nothing staged, nothing modified), inform the user and stop.

## Step 1: Determine target Python files

- **If arguments provided**: use the listed file paths directly. Verify each file exists.
- **If no arguments**, use a two-tier discovery:
  1. **First, check staged files**: run `git diff --cached --name-only -- '*.py'` to get staged `.py` files.
  2. **If nothing is staged**, fall back to **modified (unstaged) files**: run `git diff --name-only -- '*.py'` to get unstaged modified `.py` files.

Report which tier was used (staged vs. modified) so the user knows.

If the resulting list is empty after both tiers, inform the user and stop. Do not proceed to later steps.

## Step 2: Map files to dendron notes

For each target `.py` file, derive the dendron note path by converting path separators to dots and dropping `.py`:

| Python file                        | Dendron note                               |
|------------------------------------|--------------------------------------------|
| `swanki/config.py`                | `notes/swanki.config.md`                   |
| `swanki/processing/pdf_processor.py` | `notes/swanki.processing.pdf_processor.md` |

**Rules:**

- Any `.py` file can be synced -- package modules, scripts, tests, etc.
- Convert path separators to dots and drop `.py`: `swanki/processing/pdf_processor.py` > `swanki.processing.pdf_processor`
- The dendron note is `notes/<dendron_path>.md`
- If the note file does not exist, **create it** with `dendron-cli note write` (see Step 2b).

## Step 2b: Create missing notes

For each target file whose dendron note does **not** exist, create it:

```bash
dendron-cli note write --fname "<dendron_path>"
```

For example, `swanki/processing/new_module.py` with no note:

```bash
dendron-cli note write --fname "swanki.processing.new_module"
```

This creates `notes/swanki.processing.new_module.md` with proper dendron frontmatter. The note is then treated as an existing note in Step 3 (it will get a dated section appended).

**Important:** `dendron-cli` creates notes that end with `---\n` and **no trailing blank line**. When editing these newly created notes, match on the unique `created:` timestamp line + `---` rather than trying to match `---` followed by a blank line.

Track which notes were newly created for the summary in Step 5.

## Step 3: Update each module note

For each module note that exists:

1. **Read the note** to understand its current content.
2. **Read the diff** for the corresponding Python file:
   - If running with **explicit file arguments**: `git diff HEAD -- <python_file>` (covers staged + unstaged). If this returns empty (new untracked file), read the full file content instead.
   - If discovered from **staged files** (tier 1): `git diff --cached -- <python_file>`
   - If discovered from **modified files** (tier 2): `git diff -- <python_file>`
3. **Check for an existing H2 section with today's date** (pattern: `## YYYY.MM.DD`).

### If today's date section already exists

- Read the existing section content.
- Compare it against the diff. If the diff introduces changes not covered by the existing section, **append** new subsections or bullet points to the existing dated section. Do not duplicate information already present.
- If the existing section already covers the diff, do nothing.

### If no section for today's date exists

- **Append** a new H2 section at the bottom of the file (before any trailing blank lines) with this format:

```markdown
## YYYY.MM.DD - Brief Title

One-paragraph summary describing what changed and why.

### Subsection (optional)

- Bullet points with specifics
- Code snippets in fenced blocks where helpful
```

**Writing guidelines (intentional stance -- "why the change, for what"):**

- Lead with **purpose**, not mechanics. Ask: "why does this change exist? what does it enable?" The diff already shows *what* changed; the note should capture *why*.
- The brief title should name the intent (e.g., "Add cloze card validation for missing fields", not "Remove check_fields function")
- The summary paragraph should be 1-3 sentences explaining motivation and impact. Keep it brief.
- Use bullet points sparingly for multi-part changes. Omit trivial details (import reordering, lint fixes) unless they reflect a deliberate decision.
- Include short code snippets only when they clarify a new interface or configuration.
- Follow the note's existing style and level of detail.
- No Unicode emojis (breaks xelatex PDF export).

## Step 4: Stage updated module notes

Run `git add <note_path>` for each module note that was modified in Step 3.

## Step 5: Print summary

After all steps, print a summary:

```
Source: staged files (or: modified files -- nothing was staged)

Created notes:
  - swanki.processing.new_module (new)

Updated module notes:
  - swanki.config (updated existing 2026.02.11 section)
  - swanki.processing.new_module (added new 2026.02.11 section)

All module notes staged. Run /update-tasks-weekly to update the weekly note.
```

## Important Rules

- Create missing dendron notes with `dendron-cli note write` -- never with the Write tool (which would lack proper frontmatter).
- NEVER modify dendron YAML frontmatter (the `---` block at the top of notes).
- NEVER remove or rewrite existing dated sections -- only append to them or add new ones.
- Preserve the existing style and structure of each note.
- No Unicode emojis in any markdown content.
- Do NOT ask extra approval questions -- tool approval prompts are the gates.

## Example Invocations

- `/update-py-notes` -- auto-discover: staged files first, then modified files
- `/update-py-notes swanki/config.py` -- update a specific module
- `/update-py-notes swanki/processing/pdf_processor.py swanki/processing/image_processor.py` -- update multiple files
- "update python notes for config.py"
- "update notes for changed files"
