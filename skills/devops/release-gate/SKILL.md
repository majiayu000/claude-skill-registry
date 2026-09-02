---
name: release-gate
description: 'Use when the user decides to ship a release. Bumps version, commits, writes release notes, and pushes a signed tag after two explicit human confirmations. Not for running workflow-owned steps by hand — use the CI/CD workflow. Not for PR-based releases — use publish-release-pr.'
disable-model-invocation: true
---

# Release gate

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User decides to ship a release. |
| Authority | Human-only. Preview target and consequence before every publishing, credential, data-at-rest, deployment, or irreversible action. Require explicit confirmation before each. |
| Side effect | Bumps version, commits after explicit confirmation, writes local release notes, creates and pushes a signed tag after a second confirmation. Never runs workflow-owned steps by hand. |
| Done | Version matches tag; commit message reads clean without the diff; release notes house-style; triggered workflow confirmed succeeded (not assumed); no workflow step run by hand; contributions closed with credit; iteration folder retired. |

## Refusals

- Running workflow-owned steps by hand: rejected. The user must run that step through the workflow.
- Releases without confirmation at each irreversible step: rejected. Q1 and Q2 are both required.
- Overwriting an existing version: rejected. Stop and report the conflict.

## Inputs

- Version target (required): the semver or calendar version to release.
- Changelog or commit range (required): the set of changes since the last release.
- Workflow identifier (optional): CI/CD workflow name or dispatch trigger if the repo uses one.
- Contributor list (optional): names or handles to credit in release notes.
- Iteration folder path (optional): working directory to retire after release.

## Procedure

1. Confirm the user intends to release now. If not, stop. **Done when**: the user confirms intent to release or the procedure has stopped.
2. Read the current version from the project manifest. Compute the next version from the user-supplied target. **Done when**: the next version is computed.
3. Draft the release notes from the changelog or commit range. Format to house style: version header, date, categorized changes, contributor credits. **Done when**: the release notes draft is written.
4. Show the user the draft release notes, the version bump, and the commit message that will be created. Ask for explicit confirmation (Q1). **Done when**: Q1 is answered.
5. On confirmation: bump the version in the project manifest. Commit with a clean message that reads without the diff. Push the commit. **Done when**: the version is bumped, the commit is pushed, and the commit message reads clean.
6. Create a signed tag at the new commit. Show the user the tag name, target commit, and push destination. Ask for a second explicit confirmation (Q2). **Done when**: Q2 is answered.
7. On confirmation: push the signed tag. **Done when**: the signed tag is pushed.
8. If a workflow identifier was supplied, trigger the release workflow via the project's dispatch mechanism. Poll or watch for the workflow result. Confirm it succeeded before proceeding. Do not assume success. **Done when**: the workflow is confirmed succeeded or the failure is reported.
9. Close any open contributions or iteration items referenced in the changelog. Credit contributors by name in the release notes. **Done when**: contributions are closed and contributors are credited.
10. If an iteration folder was supplied, retire it (move or archive). Confirm retirement. **Done when**: the iteration folder is retired and confirmed.
11. Report the final state: version, tag SHA, workflow status, notes location, retired iteration folder. **Done when**: the final report is delivered.

## Failure and recovery

- User declines Q1 or Q2: stop immediately. No version bump, commit, tag, or push occurs. Report the declined confirmation and leave all state unchanged.
- Version already exists: stop. Report the conflict. Do not overwrite.
- Commit or tag push fails: stop after the failed push. Report the error and the partial state (e.g., local commit exists but tag was not pushed). The user decides whether to retry or revert locally.
- Workflow fails or times out: report the failure. Do not mark the release as succeeded. The user decides next action.
- **Scope creep detected** (request touches steps owned by the CI/CD workflow, deployment pipeline, or publishing platform): refuse. Report which step is workflow-owned. The user must run that step through the workflow.

Partial results are never reported as success. If any step after Q1 fails, the release is incomplete and the output states exactly which steps succeeded and which did not.

## Output

A release report with version released and tag SHA, commit hash and message, release notes path, workflow run identifier and final status, credited contributors, retired iteration folder path, and done-predicate confirmation or the exact list of failed checks, ordered as listed.
