---
name: oris-maintainer
description: Maintain the Oris Rust agent runtime with an issue-driven GitHub workflow. Use when Codex is working in the Oris repository and needs to pick up a GitHub issue, turn the issue into scoped code changes, run Rust validation such as cargo fmt and cargo test, publish the oris-runtime crate to crates.io, close the completed issue, and continue to the next iteration.
---

# Oris Maintainer

## Overview

Run Oris as a tight maintenance loop: select the active GitHub issue, implement only the issue-sized change, validate the Rust workspace, release `oris-runtime` when the change is ready, and then close the issue.
Keep the repository state, the issue scope, and the released crate version aligned. Treat each issue as one releasable milestone unless the user says otherwise.

## Workflow

### 1. Sync Issue Context

- Start each issue with the `preflight` and `issue selection` command groups in [command-checklist.md](references/command-checklist.md).
- Check branch and worktree state with `git status --short --branch` before changing anything.
- Verify GitHub access with `gh auth status` before relying on `gh issue` or `gh pr`.
- Use `gh issue list --state open --limit 20` to find the next candidate issue.
- Apply the selection order in [issue-selection.md](references/issue-selection.md) before choosing which issue to work on.
- Use `gh issue view <number>` to read the active issue. Treat the issue body, labels, and comments as the source of truth for scope.
- As soon as the issue is selected as the active work item, record the `in progress` state using [issue-state-machine.md](references/issue-state-machine.md).
- If the roadmap needs to be seeded from CSV, inspect `docs/issues-roadmap.csv` and optionally use `scripts/import_issues_from_csv.sh`.

### 2. Plan the Smallest Releasable Change

- Run the `planning` command group in [command-checklist.md](references/command-checklist.md) before editing files.
- Restate the issue in concrete engineering terms before editing code.
- Classify the issue with [issue-test-matrix.md](references/issue-test-matrix.md) before choosing the validation scope and version default.
- Read only the modules touched by the issue first. Use `rg` to find symbols and call sites quickly.
- Create or use an issue-specific branch such as `codex/issue-<number>-<slug>` when a new branch is needed.
- Inspect [project-map.md](references/project-map.md) if you need the high-value files and workspace layout.
- If the issue changes public API, behavior, or release notes, inspect `crates/oris-runtime/Cargo.toml`, `README.md`, and the latest `RELEASE_*.md`.

### 3. Implement Narrowly

- Use the `development loop` command group in [command-checklist.md](references/command-checklist.md) as the default edit/verify cycle.
- Change only what the issue requires. Avoid opportunistic refactors unless they unblock the issue directly.
- Keep `oris-runtime` publishability in mind. Public API changes, feature flags, and docs updates must remain coherent.
- Update the smallest relevant example if the issue changes developer-facing behavior.
- Preserve unrelated user changes already present in the worktree.

### 4. Validate Before Release

- Run the `pre-release validation` command group in [command-checklist.md](references/command-checklist.md) in order.
- Apply the required test set from [issue-test-matrix.md](references/issue-test-matrix.md). Treat the mapped commands as the minimum validation floor for the chosen issue type.
- Start with `cargo fmt --all`.
- Run the most targeted tests that prove the change first.
- Before publishing, run the broader validation sequence in [validation-and-release.md](references/validation-and-release.md).
- If the change touches persistence, backend startup, or API security, run the matching CI-aligned regression commands from the reference file.
- If local services, secrets, or network access are missing, move the issue to `blocked`, state the exact validation gap, and do not claim full coverage.

### 5. Prepare and Publish `oris-runtime`

- Run the `release execution` command group in [command-checklist.md](references/command-checklist.md) in order. Do not skip ahead to `cargo publish`.
- Publish only from an intentional state after validation passes.
- Confirm the target crate version in `crates/oris-runtime/Cargo.toml`.
- Choose the version bump with [versioning-policy.md](references/versioning-policy.md) before editing `crates/oris-runtime/Cargo.toml`.
- Start from the issue type default bump. Deviate only if the shipped impact is higher than the default mapping, and record the reason explicitly in the working notes or release note draft.
- Apply an intentional version bump for the issue before publish. Use the policy file instead of intuition so patch, minor, and any deferred major decision stay explicit.
- Draft or update `RELEASE_v<version>.md` before publish. Summarize only the changes shipped in this release, with the current issue as the primary source.
- Use the exact structure in [release-notes.md](references/release-notes.md) so the crate version, shipped change summary, and validation block stay consistent.
- Prefer `cargo publish -p oris-runtime --all-features --dry-run` before the real publish when possible.
- Use the exact release sequence in [validation-and-release.md](references/validation-and-release.md).
- If any release step fails, follow [publish-failure.md](references/publish-failure.md) exactly. Stop the loop, keep the issue open, and report the failure precisely.

### 6. Close the Issue and Loop

- Finish with the `release finalization` command group in [command-checklist.md](references/command-checklist.md).
- Push the branch and any release tag needed by the chosen workflow.
- Determine the repository default branch dynamically with `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`.
- Open a PR targeting the default branch using `gh pr create`. The PR body must include `Closes #<number>`, a one-line behavior summary, the validation commands run, and the released crate version.
- Enable auto-merge with `gh pr merge --auto --squash` so the PR merges automatically once required checks pass. If auto-merge is not enabled on the repository, merge manually after review instead.
- Record the `released` state comment on the issue before the PR merges so the issue timeline shows the crate version shipped.
- Close the issue only after the PR has successfully merged. If auto-merge is pending, leave the issue open until merge is confirmed.
- Leave a short closeout comment on the issue with the PR number that completed the merge.
- Return to `gh issue list --state open` and continue with the next issue.

## Operating Rules

- Do not close an issue if validation or publish is incomplete.
- Do not bump crate versions speculatively. Bump versions only as part of a real release, and keep the crate version, git tag, release note, and issue closeout text consistent.
- Do not reuse stale release notes. Each shipped crate version should have a matching `RELEASE_v<version>.md` file that reflects the actual contents of that release.
- Do not assume `gh` authentication, crates.io credentials, or network access. Verify each dependency before using it.
- Prefer narrow commands while iterating: `rg`, `cargo test -p oris-runtime <pattern>`, and file-targeted reads.
- Do not move on to the next issue after a failed publish. Resolve the release state first or leave the repository in a clearly blocked state.
- Keep one explicit issue status visible while the issue is open: `in progress`, `blocked`, or `released`.
- Treat the command checklist as the default execution contract. Deviate only when the issue scope clearly requires a narrower subset, and state that deviation explicitly.
- Treat the issue type as the default release class. If the final version bump differs from the issue type default, state the reason explicitly.
- Surface blocked steps immediately when the workflow needs secrets, external services, or explicit user approval.

## References

- Read [project-map.md](references/project-map.md) to orient yourself in this repository before large changes.
- Read [command-checklist.md](references/command-checklist.md) at the start of each issue and follow the relevant command groups in order.
- Read [issue-selection.md](references/issue-selection.md) before selecting the next issue from the open queue.
- Read [issue-state-machine.md](references/issue-state-machine.md) before changing issue status, posting blocker comments, or closing the issue.
- Read [issue-test-matrix.md](references/issue-test-matrix.md) before choosing validation commands.
- Read [versioning-policy.md](references/versioning-policy.md) before changing the crate version.
- Read [validation-and-release.md](references/validation-and-release.md) before broad validation, version bumps, or any crates.io publish.
- Read [release-notes.md](references/release-notes.md) before drafting `RELEASE_v<version>.md`.
- Read [publish-failure.md](references/publish-failure.md) when any release step or `cargo publish` command fails.
- Read [issue-closeout.md](references/issue-closeout.md) before posting the final issue comment or closing the issue.
