---
name: commit-message
description: Use when the user asks to commit, write a commit message, or stage-and-commit changes. Produces a Conventional Commits message derived from the actual staged diff, never from memory of what was edited.
---

# commit-message

Write commit messages from evidence (the diff), not from recollection.

## Procedure
1. Run `git status --porcelain` and `git diff --cached --stat`. If nothing is staged, ask whether to stage all tracked changes (`git add -u`) or specific paths. Never `git add -A` silently (untracked junk, secrets).
2. Read the staged diff: `git diff --cached`. If it exceeds ~400 lines, read `--stat` plus the hunks of the 5 largest files.
3. Classify the change: `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `build`, `ci`, `chore`. Pick ONE. If the diff mixes types, say so and offer to split into two commits.
4. Scope = the top-level directory or module most touched (`auth`, `api`, `cli`). Omit when the change is cross-cutting.
5. Subject: imperative, ≤ 50 chars, no trailing period. `fix(auth): reject expired refresh tokens`.
6. Body only when the *why* is not obvious from the diff: 1 to 3 lines, wrap at 72. Reference issues as `Refs #123` / `Closes #123` on their own line.
7. Show the message, then commit with a heredoc so newlines survive:
   ```bash
   git commit -m "$(cat <<'MSG'
   fix(auth): reject expired refresh tokens

   Tokens past `exp` were accepted because the check used `<` instead of `<=`.
   Closes #412
   MSG
   )"
   ```
8. Print `git log -1 --stat` as proof.

## Rules
- Never describe changes that are not in the staged diff.
- Never include secrets, tokens, or internal URLs in the message.
- Do not add "Co-Authored-By" or tool attribution unless the repo's CONTRIBUTING or the user asks for it.
- If tests were not run, do not claim they pass in the message.

## Eval
`evals/commit-message/`: fixture repo with a staged two-file bug fix; expected: `fix(...)` subject ≤ 50 chars, body mentions the off-by-one, no unrelated files described.
