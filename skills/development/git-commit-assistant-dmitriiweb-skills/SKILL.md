---
name: git-commit-assistant
description: Generate high-quality conventional git commit messages and, with user approval, run the commit. Use when drafting or refining commit messages, validating commit quality, or committing staged work while avoiding noisy histories.
---

# Git Commit Assistant

## Quick start
- Review staged changes and ensure they cover a single concern.
- Choose `<type>(optional-scope)` and write an imperative 50-72 character summary.
- Add body for why/decisions/trade-offs; footers for breaking changes or issue references.
- Show the message in a fenced code block, ask for approval to commit, then commit only if approved.
- See `references/commit_rules.md` for full rules and examples.

## Workflow
1) Inspect changes  
   - Check `git status` and `git diff --cached` to confirm what will be committed.  
   - If changes mix concerns or include formatting noise, ask to split or stage appropriately.

2) Select type/scope  
   - Allowed types: feat, fix, refactor, docs, test, chore, build, ci, perf, style.  
   - Scope is optional; keep it short (e.g., `api`, `auth`, `deps`).

3) Draft the message  
   - Summary: imperative, no trailing period, describe what/why, not implementation detail.  
   - Body (only if valuable): why the change was needed, key decisions, trade-offs; wrap to ~72 chars.  
   - Footers (when relevant): breaking changes, migration notes, issue references (e.g., `Closes #123`).

4) Quality gate  
   - Message intent must match the staged diff; avoid kitchen-sink commits.  
   - Do not mix formatting-only changes with functional work.  
   - Avoid noisy summaries like `update`, `fix stuff`, `changes`, `wip`.

## Confirmation and commit
- Present the message in a fenced code block and ask the user to accept.  
- On approval:  
  - Confirm staged changes are correct; surface unstaged items before committing.  
  - Run `git commit -m "<summary>"` with additional `-m "<body>"` / `-m "<footers>"` as needed.  
  - If the commit fails, report the error and pause for guidance.  
- If the user declines, revise the message or wait for more information.

## Reference
- `references/commit_rules.md`: conventional format, output pattern, quality gate, example output.
