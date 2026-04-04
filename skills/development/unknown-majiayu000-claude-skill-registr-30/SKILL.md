---
name: git-pr-merge
description: Conducts an audit of a Pull Request, merges it into main, and synchronizes the local environment. Use this skill when a PR is ready for final review and integration.
trigger: always_on
---

This skill focuses on the "Gatekeeper" role, ensuring that only high-quality, verified code enters the `main` branch.

## PR Merge & Sync Workflow

1.  **Audit**:
    -   Inspect the PR diff using `gh pr diff [id]`. Focus on source code changes, excluding third-party packages or generated binaries.
    -   Create an audit report in `audit_reports/audit_PR-[id].md` confirming compliance with tech specs and UI guides.

2.  **Merge Execution**:
    -   Once the user approves the audit, perform the merge: `gh pr merge [id] --merge --delete-branch` (if it''s a feature branch).
    -   For core `dev` branches, use `--merge` to integrate into `main`.

3.  **Local Sync**:
    -   Switch to `main` and pull the latest changes: `git checkout main; git pull origin main`.
    -   Switch back to `dev` and merge `main` to ensure the local development branch is up-to-date: `git checkout dev; git merge main`.
    -   Push the updated `dev` branch to the remote: `git push origin dev`.

4.  **Verification**:
    -   Verify that the local state is clean and ready for the next task.


