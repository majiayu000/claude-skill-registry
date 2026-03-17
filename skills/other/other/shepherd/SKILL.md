---
name: shepherd
description: Merge process -- push, CI check, PR, merge, deploy monitor, prune branches
---

# Shepherd

Guide the merge-to-main process.

## Prepare

Follow `/prepare` if this command did not immediately follow prepare.

## Clean NPM Check

- Push the branch
- Monitor the workflow in GitHub Actions
- Fix any errors (lint, test, typecheck), commit and push

## Create and Merge PR

- Create PR
- Merge once checks pass (use `--merge`, not `--squash`)

## Clean NPM Deploy

- Monitor the workflow in GitHub Actions
- If NPM publish errors (especially pre-1.0), request the operator publish manually
- Once operator publishes, restart the failed workflow and monitor
- Report once NPM Deploy finishes successfully
- Report errors in other jobs but do not resolve unless asked

## Prune Branches

- Return to main, fetch, and pull
- Delete the local and remote feature branches
- Delete local branches orphaned during this session
- Propose and confirm with operator additional local branches without a remote tracking branch to delete

## Known Issues

Do not worry about Build Stacks to Development, Build Stacks to Sandbox, or Deploy Documentation Stack. These stacks are still in beta.

## User Input

<input>
$ARGUMENTS
</input>
