---
name: ln-62-repository-publisher
description: "Validates, commits, pushes, and remotely verifies approved repository changes. Use when publication is requested; not for releases, package publishing, or announcements."
---

# Repository Publisher

Publish only changes the user has authorized, then verify the result from the remote source.

## Tool Routing

| Need | Preferred capability | Fallback |
|---|---|---|
| Scope, staging, history, and synchronization | Native Git CLI | Stop if equivalent Git evidence is unavailable |
| Repository validation | Project-native commands and installed validators | Documented manual checks |
| Remote branch and CI state | Authenticated hosting CLI or connector | Git remote evidence plus direct workflow URLs |
| Clean-source verification | Temporary clone and isolated host configuration | Remote raw files plus `BLOCKED` for install evidence |
| Static-site verification | Deployment workflow plus direct HTTP request | Hosting API deployment state |
| Current marketplace behavior | Official host documentation | Mark assumptions and avoid destructive retries |

Prefer compact Git output first, then open the full diff for files that will be staged. Never pipe commands in a way that hides the failing exit code.

Use hosting APIs for remote facts and Git for repository facts. A local marketplace directory cannot prove that a Git-backed user update works.

## Checklist

- [ ] Confirm the user explicitly requested a commit and push and identify the intended branch.
- [ ] Read repository instructions, release rules, and the current branch policy before mutation.
- [ ] Check `git status -sb`, staged and unstaged diffs, untracked files, remotes, and recent commit style.
- [ ] Identify unrelated user changes; do not stage them without explicit whole-worktree authorization.
- [ ] Inspect deletions and generated files as carefully as edited text.
- [ ] Check whether behavior, installation commands, catalogs, layout, or the public site require matching documentation updates.
- [ ] Do not create a changelog merely because one is absent; follow the repository's documented release policy.
- [ ] Do not change plugin versions, tags, or release metadata during an ordinary publication.
- [ ] For marketplace edits, confirm the stable marketplace identifier is unchanged unless an intentional migration was approved.
- [ ] Confirm Claude and Codex catalogs contain the same plugin names in the same order.
- [ ] Confirm plugin descriptions and source paths agree with canonical manifests.

## Validation Routing

- [ ] Discover and run repository-native validation commands before generic checks.
- [ ] For changed skills, run the installed skill validator or perform its documented manual fallback.
- [ ] For changed plugins, run the installed plugin validator or perform its documented manual fallback.
- [ ] Run the strict Claude marketplace validator when applicable.
- [ ] Run catalog parity, JSON parsing, stale-reference, local-link, and whitespace checks required by the repository.
- [ ] Run only relevant product tests; do not invent a heavyweight release gate absent from repository policy.
- [ ] Stop before commit on a confirmed failing required check unless the user explicitly accepts the failure.
- [ ] Record skipped checks with the exact missing dependency or environment.

## Synchronization and Commit

- [ ] Fetch the target remote and compare local HEAD with the remote branch before committing.
- [ ] If histories diverge, stop and report the commits on both sides; do not force-push or rewrite history implicitly.
- [ ] Stage explicit paths when the worktree is mixed; use whole-worktree staging only when the user approved all changes.
- [ ] Review the cached diff and diffstat after staging.
- [ ] Remove secrets, local caches, temporary artifacts, and unintended credentials from the staged set.
- [ ] Match the repository's commit-message convention and summarize the entire staged change.
- [ ] Do not add an automated co-author or signature unless repository policy or the user requests it.
- [ ] Create the commit and capture its full SHA.
- [ ] Push to the authorized branch without changing branch protections or using force.

## Remote Verification

- [ ] Confirm the remote branch resolves to the pushed commit using both Git and the hosting API when available.
- [ ] Watch required CI runs for that commit until completion; report direct run URLs and failures.
- [ ] If the static site changed, wait for deployment and verify live content with a cache-busting request.
- [ ] If marketplace content changed, clone the public remote into a clean temporary directory and validate that clone.
- [ ] Test marketplace add/update and at least one plugin install from the Git source in isolated host configuration.
- [ ] Verify the installed plugin resolves under the stable marketplace identifier and expected version.
- [ ] Keep temporary host configuration isolated from the user's active settings and remove it safely afterward.
- [ ] Recheck the local worktree and confirm local HEAD equals the remote branch.

## Safety Gates

- [ ] Never expose authentication tokens or credential values in output.
- [ ] Never create a release, tag, package publication, discussion, or pull request unless explicitly requested.
- [ ] Never delete remote branches or alter the default branch as a side effect.
- [ ] Never treat a successful push as proof that CI, marketplace refresh, or deployment succeeded.
- [ ] Return `BLOCKED` rather than bypassing branch protection, authentication, or required checks.

## Verdict

- `PUBLISHED` — commit, push, required CI, and applicable remote verification succeeded.
- `PARTIAL` — the push succeeded but a non-destructive remote check is pending or failed.
- `BLOCKED` — publication did not complete because authorization, synchronization, validation, or remote access failed.

## Output Contract

Return:

1. Published scope and excluded changes.
2. Branch, commit SHA, and remote URL.
3. Validation commands and results.
4. CI and deployment URLs.
5. Clean-source installation or update evidence when applicable.
6. Verdict.
7. Residual risks and any manual follow-up.

If publication is `PARTIAL`, state whether the pushed commit is safe to leave in place and what observable event would close the remaining check.

Do not call the result `PUBLISHED` until the remote commit and every applicable required workflow are observable.
