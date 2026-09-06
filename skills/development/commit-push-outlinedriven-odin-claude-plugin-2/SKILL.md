---
name: commit-push
description: 'Use when asked to commit and push to a feature branch off the default branch, with no pull request. Not for a PR: use commit-push-pr. Not for the checked-out branch: use commit-push-current.'
---

# Commit and push

Commit the working tree and push the branch to `origin`, with no pull request. Commit authoring belongs to `commit`. This skill adds branch placement and the push.

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User asks to commit changes and push or publish them, and does not ask for a pull request. |
| Authority | Human-gated: the write set is local commits, at most one local feature branch, and one push to `origin/<branch>`. The skill states the mutation set (push target and commit list) before the push. Rollback is `git reset --hard <prior-HEAD>` for new commits and `git branch -D <branch>` for a branch this skill created. A pushed commit is reverted, never removed. No remote mutation without the gate. |
| Side effect | Local commits, at most one local feature branch, and one `git push` to `origin`. No pull request. No force push. |
| Done | The working tree is committed and the branch is pushed: `git status --porcelain` is empty and `git rev-list --left-right --count origin/<branch>...HEAD` prints `0 0`. |

## Inputs

- Working-tree state (`git status`, `git diff HEAD`): required, gathered by the skill.
- Current branch and recent history (`git branch --show-current`, `git log --oneline -10`): required, gathered by the skill.
- Remote default branch (`git rev-parse --abbrev-ref origin/HEAD`, then `git ls-remote --symref origin HEAD`, then `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'` verified against `git ls-remote --heads origin <default>`): required for branch placement. When every resolver fails, the skill stops; a default branch is never guessed.
- User decision in detached HEAD state: required only when the repository is in detached HEAD.
- User decision on unpushed local default-branch commits: required only when the local default branch is ahead of `origin/<default>` at branch creation.

## Procedure

1. Gather context: run `git status`, `git diff HEAD`, `git branch --show-current`, `git log --oneline -10`, `git remote`, and `git rev-parse --abbrev-ref origin/HEAD 2>/dev/null || echo DEFAULT_BRANCH_UNRESOLVED`. When `git remote` lists no `origin`, skip the resolution: nothing will be pushed. If HEAD is detached, still run the step 2 detached-HEAD decision; then commit on the current branch at step 4 and end at the step 5 local-only report. Do not classify against a default. Otherwise, strip the `origin/` prefix from the default branch; treat `DEFAULT_BRANCH_UNRESOLVED` or bare `HEAD` as unresolved. When unresolved, run `git ls-remote --symref origin HEAD` and take the branch named by the first `ref: refs/heads/<name>` line. When that fails too, run `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'` and accept its name only when `git ls-remote --heads origin <name>` lists it. When every resolver fails, report `DEFAULT_BRANCH_UNRESOLVED` and stop; never guess `main` or any other default. Done when: tree state, branch, recent history, and default branch are known, or the skill has stopped.
2. Classify the branch state. Done when: HEAD is on the branch that will be pushed, or the skill has stopped.
   - Detached HEAD (empty branch name): ask whether to create a feature branch. Use the platform blocking question tool (`AskUserQuestion` in Claude Code, `request_user_input` in Codex, `ask_question` in Antigravity, `ask_user` in Pi). Fall back to chat only when no blocking tool exists or the call errors. On no, stop. On yes, derive the typed branch name per `commit` and run `git checkout -b <branch>`.
   - Default branch, no work (clean tree, nothing unpushed): report nothing to do and stop.
   - Default branch with work: create a feature branch by step 3. Do not ask. Pushing the default branch is not supported here.
   - Feature branch: continue at step 4.
3. Create the feature branch from a fresh default tip. A stale local default forks the branch from old history. Run `git fetch --no-tags origin refs/heads/<default>:refs/remotes/origin/<default>` (the explicit refspec materializes the tracking ref even on a single-branch clone), then `git log origin/<default>..HEAD --oneline`. Empty output: the base is `origin/<default>`. Non-empty output: show the list and ask, with the blocking question tool, whether to carry those commits onto the new branch (base `HEAD`) or leave them on the local default (base `origin/<default>`). Never pick silently. Derive the typed branch name per `commit` and run `git checkout -b <branch> <base>`. If checkout refuses because uncommitted changes would be overwritten, run `git stash push -u -m "commit-push: pre-branch <branch>"`, repeat the checkout, then `git stash pop`. If the fetch fails, report and stop; do not branch from HEAD or from an unverified base. Done when: `git branch --show-current` prints the new branch and the working tree carries the work.
4. Author the commits with `commit`. Its message conventions, atomicity rules, and staging discipline apply. Do not restate them here. Its default-branch auto-branching is already satisfied by step 3. Done when: `commit` reports the working tree committed, or reports nothing to commit.
5. Detect the remote with `git remote`. If no `origin` remote exists (empty output, or other remotes but none named `origin`), do not push and do not add or guess a remote. Report local-only and stop. Done when: `origin` is confirmed present, or the local-only result is reported.
6. Preview the push and wait for explicit human approval. Detect a branch new to `origin` by observing the remote: `git ls-remote --heads origin <branch>`. Non-empty output means the branch exists; empty output means it is new; a failed call means the remote cannot be observed, so report and stop without pushing. Existing branch: refresh the tracking tip with `git fetch --no-tags origin refs/heads/<branch>:refs/remotes/origin/<branch>`; when the fetch fails, report and stop without pushing. List `git log --oneline origin/<branch>..HEAD`. New branch: say so, then list the full commit range `git log --oneline origin/<default>..HEAD`; `origin/<default>` comes from the step 3 fetch when this skill created the branch, otherwise materialize it first with `git fetch --no-tags origin refs/heads/<default>:refs/remotes/origin/<default>`. When no fetched base exists (that fetch failed and `origin/<default>` is absent), report and stop without pushing; never fall back to an unanchored or truncated listing. Show the target and the commit list, then wait for the human to approve the exact mutation set (platform blocking question tool, chat fallback). On no answer or refusal, stop with nothing pushed. After approval, re-run the listing and confirm it is unchanged; on any difference, re-preview the new set and wait again. Then push with `git push -u origin HEAD`. Never force-push. Done when: the push is accepted, or the rejection or a stop is reported.
7. Verify: `git status --porcelain` is empty and `git rev-list --left-right --count origin/<branch>...HEAD` prints `0 0`. Done when: both read clean, or the residue is reported.

## Failure and recovery

- Clean tree with nothing to push: report nothing to do. No mutation occurs.
- Detached HEAD and the user declines a branch: stop. No commit is created.
- Stash pop conflicts after branch creation: report the conflict output and the stash ref. Do not resolve them without the user.
- Fetch failure before branching: report and stop. No branch is created, and there is no fallback to HEAD.
- Default branch unresolved after `origin/HEAD`, `git ls-remote --symref origin HEAD`, and verified `gh`: report and stop. Never guess a default branch.
- No fetched base for a new-branch preview (fetch of `<default>` failed and `origin/<default>` is absent): report and stop before the push. The commit set is never previewed from HEAD alone or truncated.
- Tracking-tip refresh fails before an existing-branch preview: report and stop without pushing.
- No `origin` remote: report local-only with the commit list. Never add, invent, or guess a remote.
- Approval of the push refused or absent: stop with nothing pushed. The commits stay local and the branch stays unpushed.
- The commit list changed between approval and push: stop and re-preview the new set before pushing. Never push a set the human has not seen.
- Push rejected on a diverged remote branch: report the rejection and the counts from `git rev-list --left-right --count origin/<branch>...HEAD`. Leave resolution to the user. Never force-push.
- Verification residue (non-empty `git status --porcelain`, or counts other than `0 0`): report the uncommitted files or unpushed commits. Do not claim done.

## Output

The committed working tree on the pushed branch, one `origin` push, and a report naming the branch, the pushed commit hashes and subjects, and the verification result. When no `origin` remote exists or approval is declined, a local-only report naming the commits left unpushed.
