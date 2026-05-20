---
description: Commit changes with well-crafted messages, grouping related files into separate commits
argument-hint: "[optional commit message or instructions]"
---

## Workflow

1. Run these commands in parallel to understand the current state:
   - `git status` — see all tracked/untracked files and staging state
   - `git diff` — see unstaged changes

2. Analyze ALL changes (staged + unstaged) and determine what should be committed:
   - If there are no changes at all, inform the user and stop
   - Do NOT commit files that likely contain secrets (`.env`, credentials, tokens, API keys). Warn the user if such files are present.

3. Group related file changes into logical commits:
   - Do NOT lump all changes into a single commit
   - Examine each changed file and understand what it does
   - Group files that are part of the same logical change together (e.g., a component + its styles + its test = one commit)
   - Each group becomes its own commit
   - If only one logical change exists, one commit is fine

4. For each group, draft a commit message:
   - Write natural, concise descriptions of what changed and why
   - Do NOT use conventional commits format (no `feat:`, `fix:`, `chore:` prefixes)
   - Keep the subject line under 72 characters
   - If the user provided a message or instructions via arguments, incorporate or use that for the relevant commit(s)

5. For each group, stage and commit:
   - `git add <specific files>` for that group only
   - `git commit -m "message"`
   - Repeat for each group in a logical order (foundational changes first)

6. Run `git status` after all commits to verify everything is clean.

7. Report the result: show each commit hash and summary.

## User Arguments

$ARGUMENTS
