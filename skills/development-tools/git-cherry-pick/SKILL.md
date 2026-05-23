---
name: git-cherry-pick
description: This skills takes a source branch and a target branch. It will cherry-pick the last commit from the source branch to the target branch. Optionally, it can also create a pull request for the cherry-picked commit by creating a new branch from the target branch, cherry-picking the commit to that branch, and then creating a pull request from that branch to the target branch using the GitHub CLI.
---

# git-cherry-pick

Cherry-picks the last commit from a source branch onto a target branch. Supports an optional pull-request workflow that creates an intermediate branch and opens a PR via the GitHub CLI.

## Installation

```powershell
npx skills add adamdriscoll/skills
```

- **Git** — <https://git-scm.com/downloads>
- **GitHub CLI (`gh`)** — <https://cli.github.com>

## Prerequisites

- **Git** must be installed and available in `PATH`.
- **GitHub CLI (`gh`)** must be installed and authenticated when using `-CreatePullRequest` (run `gh auth login` if needed).

## Script

`scripts/Invoke-GitCherryPick.ps1`

## Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `SourceBranch` | `string` | Yes | The branch whose **last commit** will be cherry-picked. |
| `TargetBranch` | `string` | Yes | The branch to cherry-pick the commit onto. |
| `PullRequestBranch` | `switch` | No | Creates a new branch from `TargetBranch`, cherry-picks there, and pushes to origin instead of committing directly. |
| `CreatePullRequest` | `switch` | No | Opens a pull request from the new branch to `TargetBranch` using `gh`. Requires `-PullRequestBranch`. |

## Usage Examples

### Direct cherry-pick onto target branch

```powershell
.\Invoke-GitCherryPick.ps1 -SourceBranch "feature/my-feature" -TargetBranch "main"
```

Checks out `main`, pulls the latest changes, and cherry-picks the last commit from `feature/my-feature` directly onto it.

### Cherry-pick via a PR branch (no PR created)

```powershell
.\Invoke-GitCherryPick.ps1 -SourceBranch "feature/my-feature" -TargetBranch "main" -PullRequestBranch
```

Creates a new branch named `cherry-pick/feature/my-feature-to-main`, cherry-picks the commit there, and pushes the branch to origin. No pull request is opened.

### Cherry-pick and open a pull request

```powershell
.\Invoke-GitCherryPick.ps1 -SourceBranch "feature/my-feature" -TargetBranch "main" -PullRequestBranch -CreatePullRequest
```

Full workflow: creates the PR branch, cherry-picks the commit, pushes to origin, and calls `gh pr create` to open a pull request from the new branch to `main`.

## Behavior Notes

- The PR branch is automatically named using the pattern `cherry-pick/<SourceBranch>-to-<TargetBranch>`, with any characters that are invalid in git branch names replaced by `-`.
- If a cherry-pick conflict occurs, the script throws an error. Resolve the conflicts manually and run `git cherry-pick --continue` to finish.
- The script uses `git rev-parse` on the source branch, so `SourceBranch` can be any valid git ref (branch name, tag, or commit SHA).