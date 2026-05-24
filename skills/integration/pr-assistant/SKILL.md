---
name: pr-assistant
description: Creates and updates GitHub pull requests in draft mode. Generates PR title and description from branch commits, shows for approval before executing. Use when the user asks to create a PR, update a PR description, or open a pull request.
user-invocable: true
---

# PR Assistant

Generate a pull request title and description from the current branch, then create or update the PR via `gh` CLI. PRs are always created in **draft mode**.

---

## Before Writing

1. Run `git log --oneline main..HEAD` (or the appropriate base branch) to see all commits on this branch.
2. Run `git diff main...HEAD --stat` to see the scope of changes.
3. Run `gh pr list --head $(git branch --show-current)` to check if a PR already exists for this branch.

---

## Rules

### Analyze the full branch

- Consider ALL commits on the branch, not just the latest.
- Read commit messages and the diff to understand the overall intent.

### Title

- Short: under 70 characters.
- Imperative mood (e.g. "Add user authentication flow").
- Specific and accurate. Do not inflate scope.

### Body structure

Use this format:

```
## Summary
- 1-3 bullet points explaining what this PR does and why.

## Changes
- **<Category>**:
  - Description of change
  - Description of change
- **<Category>**:
  - Description of change

## Test Plan
- [ ] Checklist of how to verify the changes.
```

### Changes section formatting

Group changes by domain or concern, not by git operation (add/modify/remove).
Choose category names that reflect what area of the system is affected.

Common categories (use what fits, invent others as needed):
- **Behavior** — user-facing or system behavior changes
- **Skills** — skill definitions and skill catalog
- **Config** — configuration, schemas, allowlist
- **Manifest** — `.quest-manifest` updates
- **Documentation** — docs, journal entries, guides
- **CI/Workflows** — GitHub Actions, automation
- **Tests** — test additions or changes
- **Security** — security hardening, permissions

Rules:
- Each category gets a bold header with nested bullet descriptions.
- Keep descriptions concise — one line per change, focus on what and why.
- Omit categories with no changes. Only include what is relevant.
- If the PR is very small (1-2 files), a flat bullet list is fine — do not force categories.

### Draft mode (required)

- Always create PRs with the `--draft` flag.
- When updating an existing PR, do not change its draft status.

### Use gh CLI

- Create: `gh pr create --draft --title "..." --body "..."`
- Update: `gh pr edit <number> --title "..." --body "..."`
- Push first if the remote branch is behind: `git push -u origin HEAD`

### Truthfulness

- Do not fabricate motivation or context.
- If intent is unclear, describe only what is visible in the commits and diff.
- Precise but narrow beats confident but wrong.

---

## Trailer

Append this line at the end of the PR body:

```
---
Quest/Co-Authored by Claude Opus 4.6, GPT-5.3 Codex in Collaboration with <github username>
```

Replace:

- **github username** with the repository author's GitHub username (infer from git config, remote URL, or ask if unknown).

Never omit the trailer.

---

## Approval

Always show the intended PR title and full body to the user and wait for explicit approval before executing `gh pr create` or `gh pr edit`. Do not create or update the PR automatically. Present the content as a plain text block and ask the user to confirm.

---

## Output

Output only the final PR title and body. Do not use emojis.
