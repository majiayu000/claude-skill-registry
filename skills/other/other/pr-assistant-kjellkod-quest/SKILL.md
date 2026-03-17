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
<Single sentence capturing the full intent — what this PR does and why.>
- Supporting bullet with additional context if needed.
- Supporting bullet with additional context if needed.

> [!WARNING or !IMPORTANT or !NOTE — only if applicable]
> Alert content here. Most PRs should have NO callouts.

## Changes
- **<Category>**:
  - Description of change referencing `specific_file.js` or `functionName()` where helpful
  - Description of change
- **<Category>**:
  - Description of change

## Test Plan
- [ ] Concrete verification step describing what to do and what to expect
- [ ] Another verification step
Watch for: <known risk or edge case, if any>
```

### Summary section

- Start with a single sentence that captures the full "what + why" of the PR. This is the line a reviewer reads to decide how deeply to engage.
- Follow with 1-2 supporting bullets if needed for additional context.

### Callouts (optional — use sparingly)

Use GitHub callout syntax **only when something needs to jump out** before a reviewer digs into the details. Most PRs should have zero callouts.

| Callout | Use when... |
|---------|-------------|
| `> [!WARNING]` | Breaking change, data migration, or irreversible action |
| `> [!IMPORTANT]` | Reviewer must do something specific (e.g. "needs env var set before deploy") |
| `> [!NOTE]` | Non-obvious context that prevents confusion (e.g. "intentionally duplicates X because...") |

Rules:
- Place callouts between `## Summary` and `## Changes`.
- If every PR has a callout, reviewers start ignoring them. Reserve them for exceptions.
- Do not use callouts as decoration or to repeat what the summary already says.

### Changes section formatting

Group changes by domain or concern, not by git operation (add/modify/remove).
Choose category names that reflect what area of the system is affected.

Reference specific file names, function names, config keys, and constants inline with backticks where they help a reviewer understand or locate the change.

Common categories (use what fits, invent others as needed):
- **Behavior** — user-facing or system behavior changes
- **API / Functions** — new, changed, or removed function signatures
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

### Test Plan section

Each checkbox should be a concrete verification step — what to do and what result to expect. A reviewer reading the list should be able to pull the branch and verify without guessing.

Rules:
- Use checkboxes (`- [ ]`) for every verification step.
- Describe the action and the expected outcome in one line (e.g. "Run X, confirm Y").
- Only include steps that a human needs to perform. Skip anything CI already covers (linting, syntax checks, type checks).
- If there is a known risk or edge case worth watching, add a `Watch for:` line at the end — no checkbox, just a heads-up.
- Keep it short. 2-5 steps is typical. If you need more, the PR may be too large.

### Bot-generated content

If a bot appends an auto-generated summary to the PR, leave it in place. Do not duplicate or conflict with its content in the human-written sections.

When updating an existing PR body, preserve bot-managed sections exactly:

- If the body contains bot-managed sections or hidden anchors/comments, keep those blocks unchanged.
- Regenerate only the human-authored section.
- Never remove, rewrite, or reorder bot-managed blocks, badges, or hidden anchors/comments.

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
