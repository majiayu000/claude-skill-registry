---
name: clean-downloads
description: Propose and execute a cleanup of the user's Downloads folder — sort into subfolders by type and age, flag duplicates and large files. Always plan first, never delete. Use when the user runs /clean-downloads.
allowed-tools:
  - Bash
  - Read
  - Glob
  - AskUserQuestion
---

# /clean-downloads — Tame the Downloads Folder

You organize `~/Downloads`. You move and sort; you **never delete** — anything that looks like trash goes to a `_review-before-deleting/` folder for the user to empty themselves.

## Steps

1. **Survey.** List the folder: count files, total size, oldest file, biggest five files. Report in three lines.
2. **Propose the plan.** A short table: destination folders (e.g., `pdfs/`, `images/`, `installers/`, `archives/`, `_review-before-deleting/`), what goes where, and how many files each. Duplicates (same name + size) and anything over 500 MB get called out individually.
3. **Wait for approval.** The user may edit the plan — folders, rules, exceptions. Only proceed on an explicit yes.
4. **Execute with `mv` only.** No `rm`, ever.
5. **Report.** What moved where, what was flagged, what was left untouched.

## Rules

- Never touch anything downloaded in the last 24 hours — it may be mid-use.
- When unsure where something belongs, leave it in place and say so.
- This skill operates outside the project folder — say that out loud before step 1 so the user knows the blast radius.
