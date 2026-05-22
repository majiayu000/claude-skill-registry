---
name: commit
description: Prepare and create git commits in this repository using Conventional Commits; use when the user asks to commit or split commits for a task.
---

# Commit

## Communication

- Communicate with the developer in Japanese.
- Write code comments and commit messages in English.

## Commit message

Follow Conventional Commits: <https://www.conventionalcommits.org/en/v1.0.0/>

```text
<type>[optional scope]: <description>

[optional body]
```

Use these types:

- fix
- feat
- chore
- docs
- refactor
- test

Use scope when clear (directory name or skill name). Examples:

- docs(python-fastapi-ddd-skill): expand DDD reference notes
- chore(codex): adjust local SKILL instructions

## Commit workflow

- Review changes with `git status` and `git diff`.
- This repo has no mandatory pre-commit command; do not run Node/bun/turbo checks.
- If the user explicitly asks to commit everything (e.g., "全体", "全部", "commit all"), include all working tree changes without asking for confirmation.
- Otherwise, do not ask about unrelated changes. Leave unrelated files untouched and stage only the files relevant to the task.
- Do not bundle all task changes into a single commit. Split commits by logical change units and scope/intent (e.g., README updates vs feature changes).
- Commit directly without extra confirmation.
- After committing, report a brief summary of created commits.
- Push only when the user asks.
- Do not amend commits unless the user asks.

## Allowed dot directories

- `.claude`
- `.codex`
- `.cursor`
- `.vscode`
- `.kiro`
