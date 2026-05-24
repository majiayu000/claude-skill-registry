---
name: pr
description: Creates a pull request for the current branch.
unsandboxed: true
---

When asked to create a pull request, follow these steps:

1. Run `git status`. If any of the following conditions apply, stop and report the errors:

   - There are unstaged changes
   - There are untracked files
   - The current branch is the default branch (`main`)

2. Check if this is a stacked PR:

   - Run `git merge-base main HEAD` to find the common ancestor with main
   - Run `git log --oneline <merge-base>..HEAD` to see commits since diverging from main
   - Check if any parent commits are on another feature branch (not main)
   - If so, run `gh pr list --head <parent-branch>` to check if that branch has an open PR
   - If a parent branch has an open PR, this is a **stacked PR**

3. Run `git log main..HEAD --oneline` to see the commit history.

4. Run `git diff` and/or `git show` as necessary to understand the changes.

5. Run `gh pr create` to create a pull request. The PR body should include:

   - A brief narrative description of the PR
   - A summary of the changes (bullet points)
   - A brief description of how the code is tested (narrative, not a checklist)

   **If this is a stacked PR**, add `--draft` to create it as a draft PR.

6. Return the PR URL and any relevant information.
