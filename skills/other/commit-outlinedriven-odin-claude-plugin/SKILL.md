---
name: commit
description: 'Use when asked to commit changes, create a typed branch, format history for a changelog, or rewrite messages of HEAD or an unpushed range. Not for pushing or a PR: use commit-push or commit-push-pr.'
---

# Git commit

Shape commit messages to repository conventions. Two modes: `create` (default) stages and commits working-tree changes as typed, atomic commits; `rewrite` rewords the messages of existing commits over `HEAD` or a short unpushed range while the tree stays byte-identical.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Create: user asks to commit or save staged or unstaged changes, create a typed branch, or format history for changelog generation. Rewrite: user asks to clean up a finished commit message or bring messages of `HEAD` or a short unpushed range to handoff-ready form. |
| Authority | Reversible local: create writes only the local index, a local feature branch, and local commits; rewrite writes only local commit messages, shows the exact commit set before mutation, and never creates or suggests a new commit; rollback is version control, and for rewrite the reflog and the original refs. No remote mutation. |
| Side effect | Create: local working tree, local index, local branch refs, and local commit objects; rollback `git reset --hard <prior-HEAD>` discards new commits and `git branch -D <created-branch>` removes a branch this skill created. Rewrite: commit messages only; the tree stays byte-identical; each rewritten commit is re-signed with its author and committer dates preserved by position. Local history only. |
| Done | Create: each logical concern is committed with a value-communicating message; `git status` confirms success; commit hashes and subjects are reported; history is parseable and auto-generates changelogs, SemVer bumps, and issue closes. Rewrite: `git diff <old>..<new>` is empty, each rewritten commit is signed with the intended dates by position, and `git log` alone carries the handoff with the diff hidden. |

## Inputs

- `mode`: `create` (default) or `rewrite`.
- Current working tree state (`git status`, `git diff HEAD`): required in create mode, gathered by the skill.
- Current branch and recent commit history (`git branch --show-current`, `git log --oneline -10`): required, gathered by the skill.
- Resolved remote default branch (`git rev-parse --abbrev-ref origin/HEAD`): optional; falls back to `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'`, then to `main`.
- Repo commit-message convention in already-loaded project instructions: optional; used directly without re-reading.
- An issue or tracker number, when one exists: optional; prefixed into the branch name and referenced in the commit footer.
- The target platform (GitHub or GitLab): required only when closing issues cross-repo or cross-project.
- User decision on creating a feature branch in detached HEAD state: required only in create mode when the repo is in detached HEAD.
- Rewrite: the target commit or range, `HEAD` (default) or a short unpushed range (`HEAD~N..HEAD`); the intended message text for each target, supplied by the user or derived from the existing message, never invented; confirmation when any target commit is already pushed to a shared remote, required before proceeding.

## Procedure

1. Select the mode. `rewrite` when the user asks to clean up or reword existing commit messages; `create` otherwise. Done when: the mode is selected and its inputs are present or the missing one is reported.
2. Gather context: run `git status`, `git diff HEAD`, `git branch --show-current`, `git log --oneline -10`, and `git rev-parse --abbrev-ref origin/HEAD 2>/dev/null || echo DEFAULT_BRANCH_UNRESOLVED`. Strip the `origin/` prefix from the default branch. If it returned `DEFAULT_BRANCH_UNRESOLVED` or bare `HEAD`, try `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'`; if that also fails, use `main`. Done when: working tree state, branch, recent history, and default branch are known.
3. Determine the commit message convention in priority order: (1) repo conventions in already-loaded project instructions, used directly; (2) a clear pattern in the recent commits from step 2 (conventional commits, ticket prefixes, emoji); (3) the seven-rule style: capitalized imperative subject, 50 chars target and 72 hard, no trailing period, blank line, body wrapped at 72 explaining what and why, never how. If source (1) or (2) uses conventional commits, format the subject as `<type>(<scope>): <subject>` (scope optional) and pick the most precise type from the allowed set with its SemVer effect: `feat` (MINOR), `fix` (PATCH), `docs`, `test`, `build`, `ci`, `chore`, `style` (formatting with no logic change), `ref` or `refactor` (refactoring with no behavior change), `perf`, `meta` (repository metadata), `license`, `revert` (none). Keep the subject ≤ 72 characters, imperative mood, no capital letter, no trailing period. Done when: the convention is determined and, if conventional, the type and SemVer effect are selected.
4. Mode rewrite (messages only; the tree stays byte-identical):
   1. List the exact target set, `HEAD` or `HEAD~N..HEAD`, with `git log --format='%H %an <%ae> %ad %cn <%ce> %cd' <range>` so the set and per-position author and committer dates are visible. Done when: the exact commit set is listed with per-position dates.
   2. Confirm none of the targets are pushed to a shared remote with `git branch -r --contains <sha>`. If any is pushed, stop and require explicit user confirmation before continuing; pushed history is otherwise untouched. Done when: all targets are confirmed unpushed or explicit confirmation is received.
   3. Record each target's original tree SHA (`git rev-parse <sha>^{tree}`) and original author and committer dates, keyed by position in the range; re-signing must preserve these dates by position. Done when: every target's tree SHA and dates are recorded by position.
   4. Rewrite each target's message to handoff-ready form per the convention in step 3. When the diff is hidden, the message must let `git log` alone carry the handoff by stating what changed and why without relying on the diff. Use `git rebase` with `GIT_SEQUENCE_EDITOR` and `git commit --amend`, or `git filter-repo --message-callback`, scoped to the exact range. Never create or suggest a new commit. Done when: every target commit's message is rewritten to handoff-ready form.
   5. Re-sign each rewritten commit with `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE` set to the recorded per-position values; do not let them slip to now. Done when: every rewritten commit is re-signed with its original dates by position.
   6. Verify the done predicate: `git diff <old>..<new>` is empty (tree byte-identical); each rewritten commit's author and committer dates match the recorded per-position values; `git log` for the range carries the handoff with `git show` and the diff hidden. Then stop. Done when: the diff is empty, dates match by position, and the log carries the handoff.
5. Mode create: if `git status` shows a clean working tree (no staged, modified, or untracked files), report nothing to commit and stop. Done when: the working tree is confirmed clean and the skill stops, or changes are confirmed present.
6. Mode create: if the current branch is empty, the repo is in detached HEAD. Ask whether to create a feature branch using the platform blocking question tool (`AskUserQuestion` in Claude Code, `request_user_input` in Codex, `ask_question` in Antigravity, `ask_user` in Pi); fall back to chat only when no blocking tool exists or the call errors, never for an unloaded schema. If yes, derive a typed branch name (step 7), run `git checkout -b <branch-name>`, re-run `git branch --show-current`, and use it for the rest of the workflow. If no, continue with the detached HEAD commit. Done when: the branch decision is made and the branch is confirmed.
7. Mode create: name the branch `<type>/[issue-]<description>`: lowercase, hyphens only, no special characters except `/`. Prefix the issue number when one exists (`feat/42-user-authentication`). Keep the description under 50 characters. Match the type to the work. Done when: the branch name is lowercase, hyphen-separated, typed, under 50 chars.
8. Mode create: determine logical commits. One concern per commit, where a concern is one reason the tree changed. Put two changes in the same commit only when reverting one without the other leaves the tree broken. Split by mechanism, not by file. When one file carries two mechanisms, write the filtered patch out of `git diff -- <file>`, keep only the hunks for one mechanism, and stage it with `git apply --cached <patch>` (confirm this headless form on the first real split, since `git add -p` needs a TTY the agent lacks). A lint, format, or whitespace sweep is its own commit, never folded into a behavior change. Order commits so each leaves the tree building. A commit that only builds with its successor is not atomic, so merge the two or re-cut the split. Done when: commit groups are determined and ordered.
9. Mode create: if the current branch is `main`, `master`, or the resolved default branch, automatically create a feature branch first: derive the typed name from step 7, run `git checkout -b <branch-name>`, confirm with `git branch --show-current`, and use it for the rest of the workflow. Do not ask; committing on the default branch is not an option here. Done when: a feature branch is created and confirmed, or the current branch is already a feature branch.
10. Mode create: for each commit group, run the repo-native verification gate (type-checker and/or linter, whichever it defines) before staging that group. A failing group is not ready to commit. Skip silently if neither is configured. Done when: each group passes its gate or the failing group is named and skipped.
11. Mode create: stage and commit each group in a single call. Prefer naming files over `git add -A` or `git add .`, which can sweep in sensitive files (`.env`, credentials) or unrelated changes. Write the subject concise, imperative, why not what, per step 3's convention; add a body only when a future reader would need motivation or trade-offs. Mark breaking changes with `!` after the type/scope or with a `BREAKING CHANGE:` footer so changelog tools detect the MAJOR bump; body-only descriptions are invisible to them. For `revert`, keep the `This reverts commit <hash>.` line that `git revert` generates. Close issues from the commit footer using a case-insensitive keyword (`close(s/d)`, `fix(es/d)`, `resolve(s/d)`) followed by the reference. On GitHub: `Closes #42`, `Closes owner/repo#99`, or `Closes #42, closes #43`; triggers on merge to the default branch. On GitLab: `Resolves #101`, `Closes group/project#42`, or `Closes #101, closes #102`. To link an issue without closing it, use `Refs #42` (GitHub) or `Refs #101` (GitLab). Never include customer or organization names, user emails, support ticket contents, secrets, or PII. Never add a Claude signature, AI agent attribution, or `Co-authored-by` trailer for Claude or any AI agent. Use a heredoc to preserve formatting:

```bash
git add file1 file2 file3 && git commit -m "$(cat <<'EOF'
feat: add first-class subject line here

Optional body explaining the change and why it was needed.

Closes #42
EOF
)"
```

Done when: each group is staged and committed with a value-communicating message.
12. Mode create: run `git status` after the commit to verify success. Report the commit hash(es) and subject line(s). Done when: `git status` confirms success and hashes and subjects are reported.

## Failure and recovery

- Clean working tree: report nothing to commit and stop; no mutation occurs.
- Detached HEAD with no branch decision: stop and report that a branch is required to attach the work; no commit is created.
- Verification gate failure for a group: that group is not ready to commit; do not stage or commit it. Already-committed groups remain; uncommitted groups are left unstaged. Report which group failed and the gate output.
- Sensitive or unrelated file detected during staging: exclude it by naming files explicitly; never use `git add -A` or `git add .`.
- Non-conforming branch or commit name: do not create or amend it. Correct the name in place (rename the branch with `git branch -m`, or rewrite the unpushed commit) and re-check against the format before proceeding.
- Breaking change stated only in the body: add `!` or a `BREAKING CHANGE:` footer; do not rely on body text.
- Issue reference placed in the subject line: move it to the footer and re-verify the keyword and reference syntax for the target platform.
- Any mutation that has already been pushed: stop and surface the pushed ref rather than force-rewriting shared history.
- Rewrite pushed target without confirmation: stop. Do not rewrite. Report which commits are pushed and await confirmation.
- Rewrite tree drift: if `git diff <old>..<new>` is non-empty, the rewrite touched the tree. Abort, discard the rewritten history, and restore the original refs from the reflog. Report the drift.
- Rewrite date slip: if any rewritten commit's author or committer date does not match the recorded per-position value, abort and restore the original refs from the reflog. Re-signing must preserve dates by position.
- Rewrite non-converged: if verification cannot pass after one corrective pass, stop and report the exact failing check (empty diff, date match, or handoff in log). Do not pretend the done predicate holds.
- Partial result: groups already committed are real commits and remain; the blocked result names the uncommitted groups and the failure reason. Rollback for a created feature branch is `git branch -D <branch-name>`; rollback for new commits is `git reset --hard <prior-HEAD>`; rollback for a rewrite is the reflog and the original refs.
- Never swallow a git error or report the done predicate when `git status` does not confirm success.

## Output

Create: local commits (one per concern, each with a conventional-commits message carrying SemVer effect and issue-closing footers) on a typed local branch, plus a report of hash(es), subject line(s), and confirming `git status`. History is parseable so tooling can auto-generate changelogs, enforce SemVer bumps, and close referenced issues on merge to the default branch. Rewrite: rewritten local history over the target range with handoff-ready messages, the tree byte-identical to the original, and each commit re-signed with dates preserved by position, plus a report naming the commit set and the verification results (empty diff, dates matched, log carries the handoff).
