---
name: update-tasks-weekly
description: Update the weekly task note with a bullet point linking to reviewed/modified files, then auto-stage the weekly file.
---

# Update Weekly Tasks

Update the current weekly task note with progress, links, and images. After updating, automatically stage the weekly file.

## Task Note Location

The weekly task note lives at `notes/user.mjvolk3.swanki.tasks.weekly.YYYY.WW.md` where `WW` is the ISO week number. Find the current one by checking git status or globbing `notes/user.mjvolk3.swanki.tasks.weekly.2026.*.md`.

## Instructions

1. **Read the current weekly note** to understand existing tasks and structure.
2. **Find today's date section** (`## YYYY.MM.DD`). Create it if it doesn't exist (append below the last dated section -- chronological order, newer at bottom).
3. **For each task entry**, follow this format:
   - **The one-sentence description is the most important part.** It should tell the reader the point of the work without having to open the linked note. Write it so someone scanning the weekly list understands what was done and why. The linked note is for details.
   - Link to the relevant file using dendron wiki-link syntax: `[[dendron.path]]` (no aliases -- `dendron.yml` sets `aliasMode: none`)
   - If the linked file/script generated images, embed them in the linked note (not the weekly note itself).
4. **Auto-stage the weekly file** after editing: run `git add <weekly-note-path>` so it's ready for the next commit.

### Elaborating existing entries

When the user asks to elaborate or update a `#TODO` entry that already exists:

1. **Find the matching entry** in the weekly note by keyword.
2. **Replace the stub** with a detailed one-sentence summary of the actual work done.
3. **Add dendron links** to relevant notes, scratch files, or module notes.
4. **Update status** -- flip `- [ ]` to `- [x]` if the work is complete.
5. Do NOT duplicate the entry -- edit in place.

## Task Entry Format

```markdown
- [x] One-sentence explainer of completed work [[dendron.path.to.note]]
- [ ] One-sentence explainer of pending task [[dendron.path.to.note]]
```

## Linking Rules

- Python source files: `[[swanki.module_name]]` -> maps to `notes/swanki.module_name.md`
- Scratch notes: `[[scratch.YYYY.MM.DD.HHMMSS-title]]` -> maps to `notes/scratch.YYYY.MM.DD.HHMMSS-title.md`
- If a linked note references a script that generates images, those images **must** be included in that linked note using markdown image syntax: `![description](assets/images/image_name.png)`

### Section Anchor Links

When a module note has multiple dated sections, link to the specific section rather than the whole note. Dendron anchor syntax: `[[note.path#anchor-slug]]`.

**CRITICAL: Always verify the H2 header exists before computing an anchor.**

Step 1 -- list actual H2 headers in the target note:

```bash
grep -n "^## " notes/swanki.some_module.md
```

Only use headers that appear in that output. Never compute an anchor for a header you wrote yourself without running this check first -- `###` subsections and assumed headers produce anchors that silently break.

Step 2 -- compute the anchor from the exact header text using the Python one-liner:

**Anchor conversion rules** (Dendron follows GitHub-style slugification):

1. Strip the `## ` prefix
2. Lowercase everything
3. Remove all characters except alphanumeric, whitespace, hyphens (regex: `[^\w\s-]`) -- this strips dots, plus signs, etc.
4. Replace spaces with hyphens
5. Do NOT collapse consecutive hyphens

```bash
python3 -c "import re,sys; h=sys.argv[1]; t=re.sub(r'^#+\s*','',h).lower(); t=re.sub(r'[^\w\s-]','',t); print(t.replace(' ','-'))" "## 2026.02.15 - Add Cloze Card Validation"
```

Always use the one-liner to compute anchors rather than doing the conversion by hand.

**When to use section anchors:**

- When a module note has multiple dated sections and the weekly entry relates to a specific one
- Prefer section links over bare note links for precision

## Files to Skip

Do not create weekly entries for:

- **Tag notes** (`notes/tags.*.md`) -- these are Dendron tag infrastructure, not work items
- **Non-note config/tooling files** (CLAUDE.md, README.md, .claude/skills/, .vscode/) -- mention these inline in the summary of the commit that changed them, but they don't get their own `[[link]]` entry

## Example

```markdown
## 2026.02.04

- [x] Drafted plan for PDF processing pipeline refactor [[scratch.2026.02.04.164340.refactor-plan]]
- [ ] Docker container for testing
- [ ] Documentation improvements
```
