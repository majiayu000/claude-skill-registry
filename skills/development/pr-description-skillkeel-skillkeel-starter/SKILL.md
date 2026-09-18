---
name: pr-description
description: Use when the user asks to open a pull request, write a PR description, or summarise a branch for review. Builds the description from the full branch diff against the base and from commit messages, and includes a test plan with real commands.
---

# pr-description

A PR description is a reviewer's map: what changed, why, how to verify, what is risky.

## Procedure
1. Determine base: `git rev-parse --abbrev-ref --symbolic-full-name @{u}` or ask; default `origin/main`. Fetch first: `git fetch origin`.
2. Collect evidence: `git log --oneline <base>..HEAD`, `git diff --stat <base>...HEAD`, and read the diff for anything non-trivial (`git diff <base>...HEAD -- <paths>`).
3. Write, in this order, using the template below. Keep the whole thing under ~250 words unless the diff is large.
4. If `gh` is available and the user asked to open the PR: `gh pr create --title "<subject>" --body "$(cat <<'EOF' ... EOF)"` and print the URL. Otherwise output the markdown.

## Template
```
## Summary
One paragraph: the problem and the approach. Link the issue.

## Changes
- Bullet per logical change, referencing files/modules (not every file).

## Test plan
- [ ] `<exact command>`: what it proves
- [ ] Manual step, if any

## Risk / rollback
What could break, how to revert (`git revert <sha>` or feature flag).
```
The body ends with the Risk / rollback section. Nothing comes after it.

## Rules
- Title ≤ 70 chars, imperative, matches the primary commit type (`feat:`/`fix:`).
- Test plan commands must be ones that actually exist in the repo (check `package.json`, `Makefile`, `pyproject.toml`). Never invent `npm test` if there is no test script.
- Call out schema/migration changes, config changes, and dependency bumps explicitly.
- Do not claim tests pass unless you ran them in this session; say "not run" otherwise.
- No tool attribution footer ("Generated with …", a robot emoji line, Co-Authored-By) unless the repo's CONTRIBUTING or the user asks for it. The harness may append such a line to PR bodies on its own; this skill's output is complete without it, so do not add one and do not leave room for one. If the user wants attribution off everywhere, point them to the attribution setting in Claude Code's settings.json (`includeCoAuthoredBy`).

## Eval
`evals/pr-description/`: fixture branch with 3 commits (feat + fix + docs) and a migration file; expected: migration called out under Risk, test plan uses the repo's real `make test`.
