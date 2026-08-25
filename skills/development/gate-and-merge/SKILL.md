---
name: gate-and-merge
description: 'Use when a set of open PRs needs landing together: run the QA gate ladder on each, fix minor findings on the PR branch, comment the blocking ones, and merge the stack parent-first. Use when the user says "land these PRs", "merge the stack", "clear the PR queue", or names a merge train. Fixing one PR review thread goes to resolve-pr-feedback; diagnosing a red check goes to gh-fix-ci.'
---

# Gate and Merge

One serial loop: gate a PR, act on its findings, merge it, move to the next. Serial because every merge changes the base the next PR is gated against. The human authorizes the queue once, and authorizes every push to a branch they do not own. The gates decide the rest.

## One ladder, one scale, three actions

Do not build a mechanical prefilter plus a separate QA pass. A draft flag and an unhandled nil are both findings, differing only in what produced them. The severity table is the single routing authority:

| Severity | Decidable definition | Action |
|---|---|---|
| `blocking` | The PR cannot merge, or merging ships a wrong result reachable on a plausible input. | One PR review carrying every blocking finding, via `gh pr review <n> --comment --body-file -`. Hold the PR, continue the queue. |
| `minor` | A defect with no reachable behavioral impact, or a convention violation, whose fix touches only files the PR already changed and adds no new behavior. | Fix on the PR head branch as one follow-up commit, push, re-gate, merge. |
| `none` | No finding. | Merge. |

The `minor` bound is mechanical rather than a judgment call: `gh pr diff <n> --name-only` is the allowlist, and a fix needing a file outside that set is `blocking` by definition, because it is no longer a touch-up of this PR. Use `--comment` rather than `--request-changes`, because the ask was to comment and a comment records the findings without seizing the approval state.

## Gate 1: mergeability

One bulk call, and this is the exact field list. Never add `statusCheckRollup` here — at `--limit 60` the bulk call plus `statusCheckRollup` returns `HTTP 502: 502 Bad Gateway` while the same call without it returns 21 KB and exits 0:

```
gh pr list --state open --limit 100 --json number,title,url,headRefName,baseRefName,headRefOid,isDraft,mergeable,mergeStateStatus,reviewDecision,maintainerCanModify
```

- `isDraft: true` is blocking with no comment, because a draft is not asking.
- `mergeable: "CONFLICTING"` is blocking and takes the conflict path below.
- `mergeable: "UNKNOWN"` means GitHub is still computing, so re-read once, then blocking.
- `reviewDecision: "CHANGES_REQUESTED"` is blocking, because a human already blocked it and the ladder does not overrule a human.

Never gate on `mergeStateStatus`. `cli/cli` PR 14252 reported `mergeStateStatus: "BLOCKED"` with `mergeable: "MERGEABLE"`, every `statusCheckRollup` conclusion `SUCCESS`, and `reviewDecision: "REVIEW_REQUIRED"`. The field folds branch protection into the same value as a real defect, so gating on `BLOCKED` holds every PR in a review-required repo. The field name reads like the gate and is not one.

### Conflict path

Resolve on the PR head branch, never inside the merge. Merge the base into the PR branch, resolve with `resolving-merge-conflicts`, push. A resolution buried in a merge commit is a change nobody reviewed. The global `merge.mergiraf.driver` handles supported languages through gitattributes, so check `git config --get merge.mergiraf.driver`, and where it is unset resolve the file triple by hand with `mergiraf merge <base> <left> <right> -o <out> -p <path>`.

## Gate 2: checks

Per PR because the bulk rollup 502 forces it:

```
gh pr view <n> --json number,headRefOid,statusCheckRollup
```

A `CheckRun` entry carries `conclusion` and a legacy status context carries `state`, so read `conclusion` and fall back to `state`. Any value outside `SUCCESS`, `SKIPPED`, `NEUTRAL` is blocking, and the finding names the check and its `detailsUrl`. Route the diagnosis to `gh-fix-ci` rather than debugging CI inside the queue. An entry whose `status` is not `COMPLETED` is still running, so `gh pr checks <n> --watch --fail-fast`, then re-read. A queue that merges on a pending check merges red.

## Gate 3: scope

```
gh pr diff <n> --name-only
```

A file set spanning unrelated subsystems under a title naming one concern is blocking as mixed concerns, because that mixing is what makes the revert impossible later. A lockfile or generated path alongside source is blocking; a PR that is only that is one concern and passes.

## Gate 4: diff QA

```
gh pr diff <n>
```

Read the whole diff once. The rule that makes this a gate rather than an opinion dump: a finding names a reachable input or state that produces the wrong result, with `file:line`. A line that is merely unlovely is not a finding. Six classes, ordered by what actually breaks:

1. Wrong on a plausible input, meaning an unhandled empty, missing, or boundary value on a path the change introduces.
2. Trust boundary, meaning untrusted input reaching a sink unvalidated, or a credential in the diff.
3. Resource and error path, meaning an acquired resource with no release on the failure path, a swallowed error, or a partial write with no rollback.
4. Concurrency, meaning shared state written without the lock its neighbours take, or an await between a read and its dependent write.
5. Contract drift, meaning a changed signature, error string, config key, or wire field with a caller left behind. This is the one class that must search rather than read: `grep` the old name tree-wide, and a surviving caller is blocking.
6. Convention, meaning the diff introduces a second way to do what the repo already does one way.

Classes 1 to 5 are blocking when the wrong result is reachable. Class 6, and a cosmetic instance of 1 to 5, are minor when the fix stays inside the PR file set.

## Gate 5: test debt

A behavior change with no test that fails without it is minor where the repo has a suite the change fits, and blocking where the change touches a trust boundary or data at rest. Never demand a test for plumbing.

## Stack order

A PR whose `baseRefName` equals another open PR's `headRefName` is that PR's child, and everything else is a root. Order topologically, parents first, roots by ascending number. Across 60 open `cli/cli` PRs this edge rule recovered a real 8-deep chain: 14177, 14178, 14179, 14180, 14181, 14182, 14183, 14184, 14200. Print the order as a tree and take one yes before the first merge. After a parent merges GitHub retargets its children, so re-read the child's `baseRefName` at its turn rather than trusting the graph drawn at the start.

## The minor-fix loop

Two sequencing traps stated as instructions:

1. `gh pr checkout <n>` into a worktree, since `worktree` owns the isolation. Edit, make one commit whose subject names the gate that caught it, push.
2. `maintainerCanModify: false` on a cross-repo PR makes the push impossible, so the fix becomes a comment carrying the patch. Same finding, different delivery, one path rather than a second flow.
3. The push moves `headRefOid` and restarts CI, so re-run Gate 2 against the new head before merging. Merging on the pre-fix oid merges unverified code.
4. `gh pr merge <n> --merge --match-head-commit <current headRefOid>`. The flag is the race guard, refusing if the head moved again under a concurrent push.

## Report

One line per PR: merged, held with the gate that held it and the comment URL, or fixed-then-merged with the follow-up SHA.

## Boundaries

- Diagnosing a red check goes to `gh-fix-ci`.
- One PR review thread goes to `resolve-pr-feedback`.
- A written review with no merge goes to `pr-review`.
- An interactive finding-by-finding walk goes to `show-review`.
- A gate override needs the user to name the gate and the PR, and a blanket skip is refused.
